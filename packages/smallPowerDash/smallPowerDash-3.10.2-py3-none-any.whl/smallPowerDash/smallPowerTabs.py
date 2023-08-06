import datetime as dt, pickle, time, os,re,pandas as pd
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px, plotly.graph_objects as go
from dorianUtils.utilsD import Utils
from dorianUtils.dccExtendedD import DccExtended
import dorianUtils.dashTabsD as tabsD
import smallPowerDash.configFilesSmallPower as cfs

class SmallPowerTab():
    def __init__(self):
        self.listIndicators = [
            # 'repartitions puissances(groups)','repartitions puissances(tags)',
            'fuites air','fuites fuel',
            'rendement GV','rendement blowers',
            'bilan valo','bilan condenseur','pertes stack','cosphi']

    def selectIndicator(self,timeRange,indicator,rs,applyMethod):
        print(indicator)
        if indicator == 'rendement GV':
            df_tuple = self.cfg.rendement_GV(timeRange,rs=rs,applyMethod=applyMethod)
        elif indicator == 'rendement blowers':
            df_tuple = self.cfg.rendement_blower(timeRange,rs=rs,applyMethod=applyMethod)
        elif indicator == 'bilan valo':
            df_tuple = self.cfg.bilanValo(timeRange,rs=rs,applyMethod=applyMethod)
        elif indicator == 'pertes stack':
            df_tuple = self.cfg.pertesThermiquesStack(timeRange,rs=rs,applyMethod=applyMethod)
        elif indicator == 'cosphi':
            df_tuple = self.cfg.cosphi(timeRange,rs=rs,applyMethod=applyMethod)
        elif indicator == 'repartitions puissances(groups)':
            df_tuple = self.cfg.repartitionPower(timeRange,expand='groups',rs=rs,applyMethod=applyMethod)
        elif indicator == 'repartitions puissances(tags)':
            df_tuple = self.cfg.repartitionPower(timeRange,expand='tags',rs=rs,applyMethod=applyMethod)
        elif indicator == 'fuites air':
            df_tuple = self.cfg.fuiteAir(timeRange,rs=rs,applyMethod=applyMethod)
        elif indicator == 'fuites fuel':
            df_tuple = self.cfg.fuitesFuel(timeRange,rs=rs,applyMethod=applyMethod)
        else:
            print()
            print('indicator selector should be one of :' + '; '.join(self.listIndicators))
            print('============================================')
        return df_tuple

    def addWidgets(self,dicWidgets):
        widgetLayout,dicLayouts = [],{}
        for wid_key,wid_val in dicWidgets.items():
            if 'dd_indicator'==wid_key:
                widgetObj = self.dccE.dropDownFromList(
                    self.baseId + wid_key, self.listIndicators, 'indicator : ',value=wid_val)
            else:
                print('component :' + wid_key +' not found')
                sys.exit()

            for widObj in widgetObj:widgetLayout.append(widObj)
        return widgetLayout

class ModuleTab(SmallPowerTab):
    def __init__(self,folderPkl,app,baseId='tmo0_',widthGraph=86):
        super().__init__(app,baseId)
        self.cfg = cfs.AnalysisPerModule(folderPkl)
        self.widthGraph = widthGraph
        self.tabLayout = self._buildModuleLayout()
        self.tabname = 'modules'
        self._define_callbacks()

    def _buildModuleLayout(self):
        dicWidgets = {
                    'pdr_time' : {'tmin':self.cfg.listFilesPkl[0],'tmax':self.cfg.listFilesPkl[-1]},
                    'in_timeRes':'auto','dd_resampleMethod':'mean',
                    'dd_style':'lines','dd_cmap':'prism',
                    'btn_export':0,
                    'block_multiAxisSettings':None
                    }
        basicWidgets = self.dccE.basicComponents(dicWidgets,self.baseId)

        dd_modules = self.dccE.dropDownFromList(self.baseId+'dd_modules',
                        list(self.cfg.modules.keys()),'Select your module: ',value = 'GV')

        dd_moduleGroup = self.dccE.dropDownFromList(self.baseId+'dd_moduleGroup',[],
                            'Select the graphs to display: ',value = 0,multi=True)

        cl_units = [dcc.Checklist(id=self.baseId+'check_unit',
                        options=[{'label': 'unit', 'value':'unit'}],value= 'unit')]

        widgetLayout = basicWidgets + dd_modules+dd_moduleGroup+cl_units
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=self.widthGraph)

    def _define_callbacks(self):
        @self.app.callback(
        Output(self.baseId + 'dd_moduleGroup', 'options'),
        Input(self.baseId + 'dd_modules','value'),
        Input(self.baseId + 'check_unit','value'),
        )
        def updateGraph(module,unitGroup):
            if not unitGroup : l = self.cfg.listTagsAllModules(module)[1]
            else : l= list(self.cfg._categorizeTagsPerUnit(module).keys())
            options = [{'label':t,'value':t} for t in l]
            return options

        listInputsGraph = {
            'pdr_timeBtn':'n_clicks',
            'dd_resampleMethod' : 'value',
            'dd_cmap':'value',
            'dd_style':'value',
            'in_heightGraph':'value',
            'in_axisSp':'value',
            'in_hspace':'value',
            'in_vspace':'value',
            }
        listStatesGraph = {
            'graph':'figure',
            'dd_modules':'value',
            'check_unit':'value',
            'dd_moduleGroup':'value',
            'in_timeRes' : 'value',
            'pdr_timeStart' : 'value',
            'pdr_timeEnd':'value',
            'pdr_timePdr':'start_date',
        }
        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        Output(self.baseId + 'pdr_timeBtn', 'n_clicks'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        State(self.baseId+'pdr_timePdr','end_date'))
        def updateGraph(timeBtn,rsmethod,colmap,style,hg,axsp,hs,vs,fig,module,unitGroup,listGroups,rs,date0,date1,t0,t1):
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            # triggerList = ['dd_modules','dd_moduleGroup','pdr_timeBtn','dd_resampleMethod']
            triggerList = ['pdr_timeBtn','dd_resampleMethod']
            if not timeBtn or trigId in [self.baseId+k for k in triggerList] :
                timeRange = [date0+' '+t0,date1+' '+t1]
                if not unitGroup :
                    fig = self.cfg.figureModule(module,timeRange,groupsOfModule=listGroups,rs=rs,applyMethod=rsmethod)
                else :
                    fig = self.cfg.figureModuleUnits(module,timeRange,listUnits=listGroups,rs=rs,applyMethod=rsmethod)
            else :fig = go.Figure(fig)
            if not unitGroup :fig = self.cfg.updateFigureModule(fig,module,listGroups,hg,hs,vs,axsp)
            else : fig = fig.update_layout(height=hg)
            # fig = self.updateLegend(fig,lgd)
            return fig,timeBtn

        @self.app.callback(
        Output(self.baseId + 'btn_export','children'),
        Input(self.baseId + 'btn_export', 'n_clicks'),
        State(self.baseId + 'graph','figure'))
        def exportClick(btn,fig):
            fig = go.Figure(fig)
            if btn>0:self.utils.exportDataOnClick(fig,baseName='proof')
            return 'export Data'

class IndicatorTab(SmallPowerTab,tabsD.TabMaster):
    def __init__(self,app,cfg,baseId='it_'):
        SmallPowerTab.__init__(self)
        tabsD.TabMaster.__init__(self,app,cfg,
            self.selectIndicator,
            # self.multiUnitGraphSP,
            cfg.plotIndicator,
            # cfg.update_lineshape_fig,
            None,
            tabname='indicators',baseId=baseId
        )
        dicSpecialWidgets = {'dd_indicator':'fuites air'}
        self._buildLayout(dicSpecialWidgets,realTime=False)
        self._define_callbacks()

    def _define_callbacks(self):
        self._define_basicCallbacks(['export','datePickerRange'])
        @self.app.callback(
            Output(self.baseId + 'graph', 'figure'),
            Output(self.baseId + 'error_modal_store', 'data'),
            Input(self.baseId + 'dd_indicator','value'),
            Input(self.baseId + 'pdr_timeBtn','n_clicks'),
            Input(self.baseId + 'dd_resampleMethod','value'),
            Input(self.baseId + 'dd_style','value'),
            State(self.baseId + 'graph','figure'),
            State(self.baseId + 'in_timeRes','value'),
            State(self.baseId + 'pdr_timeStart','value'),
            State(self.baseId + 'pdr_timeEnd','value'),
            State(self.baseId + 'pdr_timePdr','start_date'),
            State(self.baseId + 'pdr_timePdr','end_date')
            )
        def updateIndicatorGraph(indicator,timeBtn,rsMethod,style,previousFig,rs,date0,date1,t0,t1):
            timeRange = [date0+' '+t0,date1+' '+t1]
            triggerList=['dd_indicator','pdr_timeBtn','dd_resampleMethod']
            fig,errCode = tabsD.TabMaster.updateGraph(self,previousFig,triggerList,style,
                            [timeRange,indicator,rs,rsMethod],[])
            return fig,errCode

class RealTimeIndicatorTab(SmallPowerTab,tabsD.TabMaster):
    def __init__(self,app,cfg,baseId='it_rt_'):
        SmallPowerTab.__init__(self)
        tabsD.TabMaster.__init__(self,app,cfg,
            self.selectIndicator,
            # self.multiUnitGraphSP,
            cfg.plotIndicator,
            # cfg.update_lineshape_fig,
            None,
            tabname='indicators',baseId=baseId
        )
        dicSpecialWidgets = {'dd_indicator':'rendement blowers'}
        self._buildLayout(dicSpecialWidgets,realTime=True)
        self._define_callbacks()

    def _define_callbacks(self):
        self._define_basicCallbacks(['export','ts_freeze','refreshWindow'])
        @self.app.callback(
            Output(self.baseId + 'graph', 'figure'),
            Output(self.baseId + 'error_modal_store', 'data'),
            Input(self.baseId + 'dd_indicator','value'),
            Input(self.baseId + 'dd_resampleMethod','value'),
            Input(self.baseId + 'dd_style','value'),
            Input(self.baseId + 'interval','n_intervals'),
            Input(self.baseId + 'btn_update','n_clicks'),
            Input(self.baseId + 'st_freeze','data'),
            State(self.baseId + 'graph','figure'),
            State(self.baseId + 'in_timeWindow','value'),
            State(self.baseId + 'in_timeRes','value'),
            State(self.baseId + 'ts_freeze','value'),
            )
        def updateIndicatorGraph(indicator,rsMethod,style,n,updateBtn,timeRange,previousFig,tw,rs,freezeMode):
            triggerList = ['interval','btn_update','st_freeze','dd_typeTags','dd_resampleMethod']

            if freezeMode:
                fig,errCode = self.updateGraph(previousFig,triggerList,style,
                                [timeRange,indicator,tw*60,rs,rsMethod],[])
            else:
                fig,errCode = self.updateGraph(previousFig,triggerList,style,
                                        [indicator,tw*60,rs,rsMethod],[])
            return fig,errCode

# ==============================================================================
#                        FROM DORIANUTILS.DASHTABSD
# ==============================================================================
class TabMultiUnit_SP(tabsD.TabMultiUnits):
    def __init__(self,app,cfg):
        tabsD.TabMultiUnits.__init__(self,app,cfg,
            cfg.DF_loadTimeRangeTags,
            cfg.multiUnitGraphSP,
            cfg.update_lineshape_fig,
            baseId = 'mut_sp_',
            defaultTags = cfg.getTagsTU('GFC')
            )

class RealTimeTabMultiUnit_SP(tabsD.RealTimeTagMultiUnit):
    def __init__(self,app,cfg):
        tabsD.RealTimeTagMultiUnit.__init__(self,app,cfg,
            cfg.realtimeTagsDF,
            cfg.multiUnitGraphSP,
            cfg.update_lineshape_fig,
            baseId = 'mut_rt_sp_',
            defaultTags = cfg.getTagsTU('GFC')
        )

class TabSelectedTags_SP(tabsD.TabSelectedTags):
    def __init__(self,app,cfg):
        tabsD.TabSelectedTags.__init__(self,app,cfg,
            cfg.DF_loadTimeRangeTags,
            cfg.plotTabSelectedData,
            cfg.update_lineshape_fig,
            baseId = 'stt_sp_',
            defaultCat='Temperatures du gv1a'
        )

class RealTimeTabSelectedTags_SP(tabsD.RealTimeTabSelectedTags):
    def __init__(self,app,cfg):
        tabsD.RealTimeTabSelectedTags.__init__(self,app,cfg,
            cfg.realtimeTagsDF,
            cfg.plotTabSelectedData,
            cfg.update_lineshape_fig,
            baseId = 'stt_rt_sp_',
            defaultCat='Temperatures du gv1a'
        )

class TabUnitSelector_SP(tabsD.TabUnitSelector):
    def __init__(self,app,cfg):
        tabsD.TabUnitSelector.__init__(self,app,cfg,
            cfg.DF_loadTimeRangeTags,
            cfg.plotTabSelectedData,
            cfg.update_lineshape_fig,
            baseId = 'ust_sp_',
        )

class TabMultiUnitSelectedTags_SP(tabsD.TabMultiUnitSelectedTags):
    def __init__(self,app,cfg):
        tabsD.TabMultiUnitSelectedTags.__init__(self,app,cfg,
            cfg.DF_loadTimeRangeTags,
            cfg.multiUnitGraphSP,
            cfg.update_lineshape_fig,
            defaultCat='Temperatures du gv1a',
            baseId = 'must_sp_',
        )

class RealTimeMultiUnitSelectedTags_SP(tabsD.RealTimeMultiUnitSelectedTags):
    def __init__(self,app,cfg):
        tabsD.RealTimeMultiUnitSelectedTags.__init__(self,app,cfg,
            cfg.realtimeTagsDF,
            cfg.multiUnitGraphSP,
            cfg.update_lineshape_fig,
            baseId = 'must_rt_sp_',
            defaultCat='Temperatures du gv1a',
)

class RealTimeDoubleMultiUnits_SP(tabsD.RealTimeDoubleMultiUnits):
    def __init__(self,app,cfg):
        tabsD.RealTimeDoubleMultiUnits.__init__(self,app,cfg,
            cfg.realtimeTagsDF,
            cfg.doubleMultiUnitGraph,
            cfg.update_lineshape_fig,
            baseId = 'dmut_rt_sp_',
            defaultTags1=cfg.getTagsTU('GFC')
)
