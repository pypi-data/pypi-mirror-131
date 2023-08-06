import pandas as pd, numpy as np,pickle
import plotly.express as px, plotly.graph_objects as go
from dorianUtils.configFilesD import ConfigDashTagUnitTimestamp
from dorianUtils.configFilesD import ConfigDashRealTime
from dorianUtils.configFilesD import ConfigDashSpark
import subprocess as sp, os,re,glob, datetime as dt
from dateutil import parser
import time
import sys
pd.options.mode.chained_assignment = None  # default='warn'
class EmptyClass():pass

class SmallPowerMaster():
    def __init__(self):
        self.appDir  = os.path.dirname(os.path.realpath(__file__))
        self.confFolder = self.appDir + '/confFiles/'
        from PIL import Image # new import
        self._loadcolorPalettes()
        self.imgpeintre  = Image.open(self.confFolder + 'peintrepalette.jpeg')
        self.sylfenlogo  = Image.open(self.confFolder +  'logo_sylfen.png')
        self.constantsFile = self.confFolder + 'materialConstants.pkl'
        self._loadConstants()
        listCalculatedTags = ['STK_0'+str(k)+'.ET.SUM' for k in range(1,5)]
        self.unitDefaultColors = {
            'blacks':['%','TOR','RGB','watchdog','ETAT','Courbe','CMD','SN','u.a'],
            'magentas':['V DC'],
            'cyans':['A'],
            'oranges':['W','W AC','VAR AC','VA AC','kW AC','Kvar AC','KVA AC','kW DC','Wth','W DC'],
            'blues':['mbarg','barg','Pa'],
            'reds':['Nl/min','g/min','kg/h','m3/h','Nm3/s'],
            'greens':['°C'],
            'yellows':['microS/cm','h']
        }
        # internalTags = {
        #     'SEH1.FUITEAIR_FT.DS':{''},
        #     'SEH1.FUITEAIR_FT.DS':{''},
        # }

    def _loadConstants(self):
        self.cst = EmptyClass()
        if not os.path.exists(self.constantsFile):
            print(self.constantsFile,' converted to .pkl')
            self._dumpConfFiles()
        self.dfConstants=pickle.load(open(self.constantsFile,'rb'))
        for k in self.dfConstants.index:
            setattr(self.cst,k,self.dfConstants.loc[k].value)

    def _loadcolorPalettes(self):
        import pickle
        colPal = pickle.load(open(self.confFolder+'palettes.pkl','rb'))
        colPal['reds']     = colPal['reds'].drop(['Misty rose',])
        colPal['greens']   = colPal['greens'].drop(['Honeydew',])
        colPal['blues']    = colPal['blues'].drop(['Blue (Munsell)','Powder Blue','Duck Blue','Teal blue'])
        colPal['magentas'] = colPal['magentas'].drop(['Pale Purple','English Violet'])
        colPal['cyans']    = colPal['cyans'].drop(['Azure (web)',])
        colPal['yellows']  = colPal['yellows'].drop(['Light Yellow',])
        self.colorPalettes = colPal
        self.colorshades = ['greens','blues','reds','magentas','oranges','yellows','cyans','blacks']
        for c in self.colorshades:
            self.colorPalettes[c]=self.colorPalettes[c].sample(frac=1)

    def _buildColorCode(self):
        dftagColorCode = pd.read_csv(self.confFolder + 'color_codeTags.csv',index_col=0,keep_default_na=False)
        from plotly.validators.scatter.marker import SymbolValidator
        raw_symbols = pd.Series(SymbolValidator().values[2::3])
        listLines=pd.Series(["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"])
        d={}
        for k,v in self.unitDefaultColors.items():
            for l in v:d[l]=k
        self.unitDefaultColors=d
        self.allHEXColors=pd.concat([k['hex'] for k in self.colorPalettes.values()])
        self.allHEXColors=self.allHEXColors[~self.allHEXColors.index.duplicated()]

        tag = 'SIS.BAS_N2_PT_02_HM05'
        def assignRandomColor2Tag(tag):
            unitTag=self.getUnitofTag(tag[0]).strip()
            shadeTag=self.unitDefaultColors[unitTag]
            color=self.colorPalettes[shadeTag]['hex'].sample(n=1)
            return color.index[0]

        dftcc_color=dftagColorCode.reset_index()
        # generate random color/symbol/line for tags who are not in color_codeTags.csv
        dfRandomColorsTag = pd.DataFrame([k for k in self.dfPLC.index if k not in list(dftcc_color.TAG)])
        dfRandomColorsTag['colorName'] = dfRandomColorsTag.apply(lambda x: assignRandomColor2Tag(x),axis=1)
        dfRandomColorsTag['symbol'] =pd.DataFrame(raw_symbols.sample(n=len(dfRandomColorsTag),replace=True)).set_index(dfRandomColorsTag.index)
        dfRandomColorsTag['line'] = pd.DataFrame(listLines.sample(n=len(dfRandomColorsTag),replace=True)).set_index(dfRandomColorsTag.index)
        dfRandomColorsTag.columns=dftcc_color.columns
        dftcc_color = pd.concat([dfRandomColorsTag,dftcc_color])
        # dftcc_color['colorHEX'] = dfRandomColorsTag.apply(lambda x: self.allHEXColors.loc[x['colorName']],axis=1)
        self.dftagColorCode=dftcc_color.set_index('TAG')

    def _load_plcfile(self):
        self.plcfile = glob.glob(self.confFolder + '*.xlsm')[0]
        plcfilepkl = self.plcfile[:-5]+'.pkl'
        if not os.path.exists(plcfilepkl):
            self._convertplcfilesmallPower()
        self.dfPLC = pickle.load(open(plcfilepkl,'rb'))
        self.enumModeHUB = pickle.load(open(self.confFolder + 'enumModeHUB.pkl','rb'))

    def _convertplcfilesmallPower(self):
        ##############################
        start=time.time()
        #find the plcfile .xlsm
        import glob,pickle
        self.plcfile = glob.glob(self.confFolder + '/*.xlsm')[0]
        # get the enumerations of hub sytem modes
        enumModeHUB = pd.read_excel(self.plcfile,sheet_name='Enumérations',skiprows=1).iloc[:,1:3].dropna()
        enumModeHUB=enumModeHUB.set_index(enumModeHUB.columns[0]).iloc[:,0]
        enumModeHUB.index=[int(k) for k in enumModeHUB.index]
        for k in range(100):
            if k not in enumModeHUB.index:
                enumModeHUB.loc[k]='undefined'
        enumModeHUB = enumModeHUB.sort_index()
        enumModeHUB=enumModeHUB.to_dict()
        pickle.dump(enumModeHUB,open(self.confFolder + 'enumModeHUB.pkl','wb'))
        print('loading enum xlsm file  in {:.2f} milliseconds'.format((time.time()-start)*1000))
        # PLCFILE
        start = time.time()
        dfPLC = pd.read_excel(self.plcfile,sheet_name='FichierConf_Jules')
        dfPLC = dfPLC.set_index('TAG')

        pickle.dump(dfPLC,open(self.confFolder + self.plcfile.split('/')[-1][:-5]+'.pkl','wb'))
        print('loading conf jules xlsm file  in {:.2f} milliseconds'.format((time.time()-start)*1000))

    def _dumpConfFiles(self):
        ##### material Constants
        dfConstants=pd.read_excel(self.confFolder + 'materialConstants.xlsx',sheet_name='thermo')
        dfConstants.columns=['description','variableName','value','unit']
        dfConstants = dfConstants.set_index('variableName').dropna()
        # dfConstants = dfConstants[['value','description','unit']]
        pickle.dump(dfConstants,open(self.confFolder + 'materialConstants.pkl','wb'))

    # ==============================================================================
    #                   computation functions/INDICATORS
    # ==============================================================================
    def repartitionPower(self,timeRange,expand='groups',groupnorm='percent',**kwargs):
        dfs=[]
        armoireTotal = self.getTagsTU('SEH0\.JT.*JTW_')
        dfPtotal = self.DF_loadTimeRangeTags(timeRange,armoireTotal,**kwargs)

        if expand=='tags':
            puissancesTotales = self.getTagsTU('JTW_00')
            powertags = self.getTagsTU('JTW')
            powertags = [t for t in powertags if t not in armoireTotal+puissancesTotales]
            df = self.DF_loadTimeRangeTags(timeRange,powertags,**kwargs)
            return df
            # fig = px.area(df,x='timestamp',y='value',color='tag',groupnorm=groupnorm)
            fig = px.area(df,groupnorm=groupnorm)

        elif expand=='groups':
            pg = {}
            pg['armoire'] = self.getTagsTU('EPB.*JTW')
            pg['enceinte thermique'] = self.getTagsTU('STB_HER.*JTW.*HC20')
            pg['chauffant stack'] = self.getTagsTU('STB_STK.*JTW.*HC20')
            pg['alim stack'] = self.getTagsTU('STK_ALIM.*JTW')
            pg['chauffant GV'] = self.getTagsTU('STG.*JTW')
            pg['blowers'] = self.getTagsTU('BLR.*JTW')
            pg['pompes'] = self.getTagsTU('PMP.*JTW')
            d = pd.DataFrame.from_dict(pg,orient='index').melt(ignore_index=False).dropna()['value']
            d = d.reset_index().set_index('value')
            allTags = list(d.index)

            df = self.DF_loadTimeRangeTags(timeRange,allTags,**kwargs)
            df = df.melt(value_name='value',var_name='tag',ignore_index=False)
            df['group']=df.tag.apply(lambda x:d.loc[x])
            # df.melt(var)

            fig=px.area(df,x=df.index,y='value',color='group',groupnorm=groupnorm,line_group='tag')
            fig.update_layout(legend=dict(orientation="h"))
            return fig
        # try:
        #     traceP = go.Scatter(x=dfPtotal.index,y=dfPtotal.iloc[:,0],name='SEH0.JT_01.'+ whichPower+'(puissance totale)',
        #         mode='lines+markers',marker=dict(color='blue'))
        #     fig.add_trace(traceP)
        # except:
        #     print('total power SEH0.JT_01.'+ whichPower +'IS EMPTY')
        # fig.update_layout(yaxis_title='power in W')

        return df,dfPtotal

    def bilanEchangeur(self,timeRange_Window,tagDebit='L400',echangeur='CND_03',**kwargs):
        cdn1_tt = self.getTagsTU(echangeur + '.*TT')
        debitEau = self.getTagsTU(tagDebit + '.*FT')
        listTags = cdn1_tt + debit
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if df.empty:
            return df
        debitEau_gs = df[debitEau]*1000/3600
        deltaT = df[cdn3_tt[3]]-df[cdn3_tt[1]]
        puissance_echangee = debitEau_gs*self.cst.Cp_eau_liq*deltaT
        varUnitsCalculated = {
            'debit eau(g/s)':{'unit':'g/s','var':debitEau_gs},
            'delta température ' + echangeur:{'unit':'°C','var':deltaT},
            'puissance echangée ' + echangeur:{'unit':'W','var':puissance_echangee},
        }
        return df, varUnitsCalculated

    def bilanValo(self,timeRange_Window,**kwargs):
        '''
        - timeRange_Window : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''
        debit_eau = self.getTagsTU('L400.*FT')#kg/h
        cdn1_tt = self.getTagsTU('CND_01.*TT')
        cdn3_tt = self.getTagsTU('CND_03.*TT')
        hex1_tt = self.getTagsTU('HPB_HEX_01')
        hex2_tt = self.getTagsTU('HPB_HEX_02')
        vannes  = self.getTagsTU('40[2468].*TV')
        vanne_hex1, vanne_hex2, vanne_cdn3, vanne_cdn1 = vannes

        t_entree_valo='_TT_02.HM05'
        t_sortie_valo='_TT_04.HM05'
        listTags = debit_eau + cdn1_tt + cdn3_tt + hex1_tt + hex2_tt + vannes

        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if df.empty:
            return df

        debitEau_gs = df[debit_eau].squeeze()*1000/3600
        nbVannes = df[vannes].sum(axis=1)##vannes NF 0=fermée
        debitUnitaire = debitEau_gs/nbVannes

        deltaT = df[cdn3_tt[3]]-df[cdn3_tt[1]]
        echange_cnd3 = debitUnitaire*self.cst.Cp_eau_liq*deltaT

        varUnitsCalculated = {
            'debit eau(g/s)':{'unit':'g/s','var':debitEau_gs},
            'nombres vannes ouvertes':{'unit':'#','var':nbVannes},
            'debit eau unitaire':{'unit':'g/s','var':debitUnitaire},
            'delta température':{'unit':'°C','var':deltaT},
            'puissance echange condenseur 3':{'unit':'W','var':echange_cnd3},
        }
        return df, varUnitsCalculated

    def rendement_GV(self,timeRange_Window,activePower=True,wholeDF=False,**kwargs):
        '''
        - activePower : active or apparente power
        - timeRange_Window : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''

        debit_eau = self.getTagsTU('L213_H2OPa.*FT')#g/min
        if activePower:p_chauffants = self.getTagsTU('STG_01a.*JTW')
        else: p_chauffants = self.getTagsTU('STG_01a.*JTVA')
        t_entree_GV = self.getTagsTU('GWPBH_TT')
        t_sortie_GV = self.getTagsTU('L036.*TT')
        TT07 = self.getTagsTU('STG_01a.*TT_02')

        listTags = debit_eau+p_chauffants+t_entree_GV + t_sortie_GV+TT07
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if df.empty:
            return df
        df = df[listTags]
        debitEau_gs = df[debit_eau].squeeze()/60

        #calcul
        power_chauffe_eau_liq = debitEau_gs*self.cst.Cp_eau_liq*(100-df[t_entree_GV].squeeze())
        power_chauffe_eau_liq = power_chauffe_eau_liq.apply(lambda x :max(0,x))
        power_vapo_eau = debitEau_gs*self.cst.Cl_H2O
        power_chauffe_vap = debitEau_gs*self.cst.Cp_eau_vap*(df[t_sortie_GV].squeeze()-100)
        power_chauffe_vap = power_chauffe_vap.apply(lambda x :max(0,x))
        power_total_chauffe = power_chauffe_eau_liq + power_vapo_eau +  power_chauffe_vap
        power_elec_chauffe = df[p_chauffants].sum(axis=1)
        rendement_GV = power_total_chauffe/power_elec_chauffe*100
        rendement_GV_rollmean= rendement_GV.rolling('3600s').mean()
        varUnitsCalculated = {
            'puissance chauffe eau liquide':{'unit':'W','var':power_chauffe_eau_liq},
            'puissance vaporisation eau':{'unit':'W','var':power_vapo_eau},
            'puissance chauffe vaporisation':{'unit':'W','var':power_chauffe_vap},
            'puissance totale de chauffe':{'unit':'W','var':power_total_chauffe},
            'puissance electrique de chauffe':{'unit':'W','var':power_elec_chauffe},
            'rendement GV':{'unit':'%','var':rendement_GV},
            'rendement GV (moyennes)':{'unit':'%','var':rendement_GV},
        }
        return df,varUnitsCalculated

    def pertesThermiquesStack(self,timeRange_Window,fuel='N2',wholeDF=False,activePower=True,**kwargs):
        air_entreeStack = self.getTagsTU('HTBA.*HEX_02.*TT.*01')[0]
        air_balayage = self.getTagsTU('HPB.*HEX_02.*TT.*02')[0]
        fuel_entreeStack = self.getTagsTU('HTBF.*HEX_01.*TT.*01')[0]
        TstackAir = self.getTagsTU('GFC_02.*TT')[0]
        TstackFuel = self.getTagsTU('GFC_01.*TT')[0]
        debitAir = self.getTagsTU('l138.*FT')[0]
        debitFuel = self.getTagsTU('l032.*FT')[0]
        p_chauffants = self.getTagsTU('STK_HER.*JTW')

        listTags = [air_entreeStack,air_balayage,fuel_entreeStack,TstackAir,TstackFuel,debitAir,debitFuel]+p_chauffants

        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if df.empty:
            return df
        df = df[listTags]
        cp_fuel,M_fuel = self.dfConstants.loc['Cp_' + fuel,'value'],self.dfConstants.loc['Mmol_' + fuel,'value']
        cp_air,M_air = self.cst.Cp_air,self.cst.Mmol_Air
        debitAir_mols = df[debitAir].squeeze()/22.4/60
        debitAirBalayage_mols = df[debitAir].squeeze()/22.4/60
        debitFuel_mols = df[debitFuel].squeeze()/22.4/60
        surchauffe_Air  = (df[TstackAir]-df[air_entreeStack])*cp_air*M_air*debitAir_mols
        surchauffe_Fuel = (df[TstackFuel]-df[fuel_entreeStack])*cp_fuel*M_fuel*debitFuel_mols
        surchauffe_AirBalayage = (df[TstackAir]-df[air_entreeStack])*cp_air*M_air*debitAirBalayage_mols
        total_puissance_surchauffe_gaz = surchauffe_Air + surchauffe_Fuel + surchauffe_AirBalayage
        puissance_four = df[p_chauffants].sum(axis=1)
        pertes_stack = puissance_four/total_puissance_surchauffe_gaz

        varUnitsCalculated = {
            'debit air(mol/s)':{'unit':'mol/s','var':debitAir_mols},
            'debit fuel(mol/s)':{'unit':'mol/s','var':debitFuel_mols},
            'surchauffe air':{'unit':'W','var':surchauffe_Air},
            'surchauffe fuel':{'unit':'W','var':surchauffe_Fuel},
            'surchauffe air balayage':{'unit':'W','var':surchauffe_AirBalayage},
            'total puissance surchauffe gaz':{'unit':'W','var':total_puissance_surchauffe_gaz},
            'puissance four':{'unit':'W','var':puissance_four},
            'pertes stack':{'unit':'W','var':pertes_stack},
        }
        return df,varUnitsCalculated

    def rendement_blower(self,timeRange_Window,activePower=True,**kwargs):
        debitAir = self.getTagsTU('138.*FT')
        pressionAmont_a,pressionAmont_b = self.getTagsTU('131.*PT')
        pressionAval = self.getTagsTU('138.*PT')[0]
        puissanceBlowers = self.getTagsTU('blr.*02.*JT')
        t_aval = self.getTagsTU('l126')
        listTags = debitAir+[pressionAmont_a,pressionAmont_b]+[pressionAval]+t_aval+puissanceBlowers

        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            df = df[listTags]
            debitAirNm3 = df[debitAir]/1000/60
            deltaP2a_Pa = (df[pressionAval]-df[pressionAmont_a])*100
            deltaP2b_Pa = (df[pressionAval]-df[pressionAmont_b])*100
            deltaP_moyen = (deltaP2a_Pa + deltaP2b_Pa)/2
            p_hydraulique = debitAirNm3.squeeze()*deltaP_moyen
            p_elec = df[puissanceBlowers].sum(axis=1)
            rendement_blower = p_hydraulique/p_elec

        varUnitsCalculated = {
            'debit air(Nm3/s)':{'unit':'Nm3/s','var':debitAirNm3},
            'deltap blower a':{'unit':'Pa','var':deltaP2a_Pa},
            'deltap blower b':{'unit':'Pa','var':deltaP2b_Pa},
            'deltap moyen':{'unit':'mbarg','var':deltaP_moyen},
            'puissance hydraulique':{'unit':'W','var':deltaP_moyen},
            'puissance electrique':{'unit':'W','var':p_elec},
            'rendement blower':{'unit':'%','var':rendement_blower},
            }
        return df,varUnitsCalculated

    def rendement_pumpRecircuFroid(self,timeRange_Window,activePower=True,**kwargs):
        ### compliqué débit amont
        debitAmont   = self.getTagsTU('303.*FT')+''#???
        debitAval = self.getTagsTU('L032.*FT')
        t_aval = self.getTagsTU('L032.*TT')
        pressionAval = ''#???
        puissancePump = self.getTagsTU('gwpbh.*pmp_01.*JTW')
        listTags = debitAmont + debitAval +t_aval + pressionAval + puissancePump

        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if df.empty:
            return df
        df = df[listTags]
        dfPump = pd.DataFrame()
        dfPump['debit eau total(Nm3/s)'] = (df['debit eau1(g/min)']+df['debit eau2(g/min)'])/1000000/60
        Pout = df['pressionAval(mbarg)']*100
        dfPump['puissance hydraulique(W)'] = dfPump['debit eau total(Nm3/s)']*dfPump['pression sortie(Pa)']
        dfPump['rendement pompe'] = dfPump['puissance hydraulique(W)']/df['puissance pump(W)']*100
        dfPump['cosphiPmp'] = df['puissance pump(W)']/(df['puissance pump(W)']+df['puissance pump reactive (VAR)'])
        varUnitsCalculated = {

        }
        df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
        df = pd.concat([df,dfPump],axis=1)
        return df,varUnitsCalculated

    def cosphi(self,timeRange_Window,**kwargs):
        extVA = 'JTVA_HC20'
        extVAR ='JTVAR_HC20'
        extW ='JTW'
        tagsVA = self.getTagsTU(extVA)
        tagsVAR = self.getTagsTU(extVAR)
        tagsJTW = self.getTagsTU(extW)
        racineVA = [tag.split(extVA)[0] for tag in tagsVA]
        racineVAR = [tag.split(extVAR)[0] for tag in tagsVAR]
        racineW = [tag.split(extW)[0] for tag in tagsJTW]
        tags4Cosphi = list(set(racineVA)&set(racineW))

        jtvas,jtws=[],[]
        for t in tags4Cosphi:
            jtvas.append([tag for tag in tagsVA if t in tag][0])
            jtws.append([tag for tag in tagsJTW if t in tag][0])

        listTags = jtvas + jtws
        if isinstance(timeRange_Window,list):
            df = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else:
            df = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if df.empty:
            return df
        cosphi = {t:{'unit':'cosphi','var':df[jtva].squeeze()/df[jtw].squeeze()} for jtva,jtw,t in zip(jtvas,jtws,tags4Cosphi)}
        # cosphi = {jtva+'/'+jtw:{'unit':'cosphi','var':df[jtva].squeeze()/df[jtw].squeeze()} for jtva,jtw in zip(jtvas,jtws)}
        return df,cosphi

    def getModeHub(self,timeRange_Window,**kwargs):
        modeSystem = 'SEH1.Etat.HP41'
        if isinstance(timeRange_Window,list) :
            dfmodeHUB = self.DF_loadTimeRangeTags(timeRange_Window,[modeSystem],**kwargs)
        else :
            dfmodeHUB   = self.realtimeTagsDF([modeSystem],timeWindow=timeRange_Window,**kwargs)

        dfmodeHUB=dfmodeHUB.astype(int)
        dfmodeHUB.columns=['value']
        dfmodeHUB['mode hub']=dfmodeHUB.applymap(lambda x:self.enumModeHUB[x])
        return dfmodeHUB

    def fuiteAir(self,timeRange_Window,**kwargs):
        airAmont = self.getTagsTU('l138.*FT')[0]
        airAval = self.getTagsTU('l118.*FT')[0]
        Istacks = self.getTagsTU('STK.*IT.*HM05')
        Tfour = self.getTagsTU('STB_TT_02')[0]
        pressionCollecteur = self.getTagsTU('GFC_02.*PT')[0]
        pressionDiffuseur = self.getTagsTU('GFD_02.*PT')[0]

        listTags =[airAmont,airAval]+Istacks+[Tfour]+[pressionCollecteur,pressionDiffuseur]
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
            # df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,rs=rs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)

        if df.empty:
            return pd.DataFrame()
        df = df[listTags]

        # sum courant stacks
        Itotal = df[Istacks].sum(axis=1)
        # production O2
        F = self.dfConstants.loc['FAR'].value
        Po2mols = Itotal*25/(4*F) ##25 cells
        Po2Nlmin = Po2mols*22.4*60
        # fuite air
        # QairAval = df[airAval] + Po2Nlmin
        QairAval = df[airAval] - Po2Nlmin
        fuiteAir = df[airAmont]-(QairAval)
        txFuite = fuiteAir/df[airAmont]*100
        coefficientDeFuite = fuiteAir/df[pressionDiffuseur]

        dfmodeHUB=self.getModeHub(timeRange_Window,**kwargs)
        # dfmodeHUB=self.getModeHub(timeRange_Window,rs=rs)

        varUnitsCalculated = {
            'courrant stacks total':{'unit':'A','var':Itotal},
            'production O2(mol/s)':{'unit':'mol/s','var':Po2mols},
            'production O2(Nl/min)':{'unit':'Nl/min','var':Po2Nlmin},
            'flux air aval(aval + production O2)':{'unit':'Nl/min','var':QairAval},
            'fuite air':{'unit':'Nl/min','var':fuiteAir},
            'taux de fuite air':{'unit':'%','var':txFuite},
            'coefficient de fuite':{'unit':'N/min/mbar','var':coefficientDeFuite},
            'mode hub':{'unit':'mode hub','var':dfmodeHUB['value']}
        }
        # update mode and hovers
        listTexts={'mode hub':dfmodeHUB['mode hub']}
        return df,varUnitsCalculated,listTexts

    def fuitesFuel(self,timeRange_Window,**kwargs):
        '''
        Gonflage :
        - L035 ou L040 fermées et L039 fermée et L027 fermée
        - fuites fuel BF = L303 + L041 (+ Somme i x 25 / 2F)  note : normalement dans ce mode le courant est nul.
        Boucle fermée recirculation à froid (mode pile)
        - L026 et L029 fermées, L027 ouverte, L035 OU L040 fermées
        - fuites fuel BF = L303 + L041 + Somme i x 25 / 2F
        Boucle ouverte (fonctionnement électrolyse ou boucle ouverte pendant les transitions) :
        - (L035 ET L040 ouvertes) ou L026 ouverte ou L029 ouverte
        - fuite ligne fuel BO = L303 + L041 + Somme i x 25 / 2F – L025
        Fonctionnement mode gaz naturel :
        - L027 fermée, L039 ouverte
        - fuites fuel BO = (L032 – L303) x 4 + L303 + L041 + Somme i x 25 / 2F – L025
        En résumé : trois calculs possibles du débit de fuite fuel
        Le même calcul pour les cas 1 et 2 qui sont « fermés »
        Un calcul pour le mode ouvert électrolyse ou boucle ouverte pendant les transitions
        Un calcul pour le mode gaz naturel.
        '''

        vanne26 = self.getTagsTU('l026.*ECV')[0]#NO
        vanne27 = self.getTagsTU('l027.*ECV')[0]#NO
        vanne29 = self.getTagsTU('l029.*ECV')[0]#NF
        vanne35 = self.getTagsTU('l035.*ECV')[0]#NF
        vanne39 = self.getTagsTU('l039.*ECV')[0]#NF
        vanne40 = self.getTagsTU('l040.*ECV')[0]#NF
        vannes = [vanne26,vanne27,vanne29,vanne35,vanne39,vanne40]
        Istacks = self.getTagsTU('STK.*IT.*HM05')

        L025=self.getTagsTU('l025.*FT')[0]
        L032=self.getTagsTU('l032.*FT')[0]
        L041=self.getTagsTU('l041.*FT')[0]
        L303=self.getTagsTU('l303.*FT')[0]
        Tfour = self.getTagsTU('STB_TT_02')
        pressionStacks = self.getTagsTU('GF[CD]_01.*PT')

        debits =[L303,L041,L032,L025]
        listTags = vannes+Istacks+debits+pressionStacks+Tfour

        start = time.time()
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if df.empty:
            print('no data could be loaded')
            return pd.DataFrame()

        print('loading data in {:.2f} milliseconds'.format((time.time()-start)*1000))
        #############################
        # compute Hydrogen production
        #############################

        Itotal = df[Istacks].sum(axis=1)
        F = self.dfConstants.loc['FAR'].value
        PH2mols = Itotal*25/(2*F) ##25 cells
        PH2Nlmin = PH2mols*22.4*60

        #############################
        # dtermine mode fuel
        #############################

        # convert vannes to bool
        for v in vannes:df[v]=df[v].astype(bool)
        dfModes={}
        # ~df[vanne]==>fermé si NF mais df[vanne]==>ouvert si NO
        # Gonflage :
        # L035 ou L040 fermées et L039 fermée et L027(NO==>0:ouvert) fermée
        dfModes['gonflage'] = (~df[vanne35] | ~df[vanne40]) & (~df[vanne39]) & (df[vanne27])
        # fuites fuel BF = L303 + L041 (+ Somme i x 25 / 2F)  note : normalement dans ce mode le courant est nul.

        # Boucle fermée recirculation à froid (mode pile):
        # L026(NO) et L029 fermées, L027(NO) ouverte, L035 OU L040 fermées
        dfModes['recircuFroidPile']=(df[vanne26]) & (~df[vanne29]) & (~df[vanne27]) & (~df[vanne35]) | (~df[vanne40])
        # fuites fuel BF = L303 + L041 + Somme i x 25 / 2F
        fuitesFuelBF = df[L303] + df[L041] + PH2Nlmin

        # Boucle ouverte (fonctionnement électrolyse ou boucle ouverte pendant les transitions) :
        # (L035 ET L040 ouvertes) ou L026(NO) ouverte ou L029 ouverte
        dfModes['bo_electrolyse']=(df[vanne35] & df[vanne40]) | (~df[vanne26]) | (df[vanne29])
        # - fuites fuel BO = (L032 – L303) x 4 + L303 + L041 + Somme i x 25 / 2F – L025
        fuitesFuelBO = df[L303] + df[L041] + PH2Nlmin - df[L025]
        # Fonctionnement mode gaz naturel :
        # - L027(NO) fermée, L039 ouverte
        dfModes['gaz_nat']=(df[vanne27] & df[vanne39])
        fuitesFuelBO_GN = (df[L032] - df[L303])*4 + df[L303] + df[L041] + PH2Nlmin - df[L025]
        # - fuites fuel BO = (L032 – L303) x 4 + L303 + L041 + Somme i x 25 / 2F – L025

        # check wether they are multiple modes or exclusive modes
        dfModeFuel= [v.apply(lambda x: k+'/' if x==True else '') for k,v in dfModes.items()]
        dfModeFuel = pd.concat(dfModeFuel,axis=1).sum(axis=1).apply(lambda x : x[:-1])
        modesFuel = {v:k for k,v in enumerate(dfModeFuel.unique())}
        modeFuelInt = dfModeFuel.apply(lambda x:modesFuel[x])

        #determine if pileBF or pileBO
        pileBF = [k for k in modesFuel.keys() if 'recircuFroidPile' in k or 'gonflage' in k]
        pileBF = dfModeFuel.apply(lambda x: True if x in pileBF else False)
        dfs=pd.concat([fuitesFuelBO,fuitesFuelBF],axis=1)
        dfs.columns=['BO','BF']
        dfs['pileBF'] = pileBF

        #get fuel fuites in either mode
        fuitesFuel =dfs.apply(lambda x: x['BO'] if x['pileBF'] else x['BF'],axis=1)

        # Vérif débitmètres ligne fuel BF = L032 FT – L303 – L025
        verifDebitmetre = df[L032]-df[L303]-df[L025]

        # get mode Hub
        dfmodeHUB=self.getModeHub(timeRange_Window,**kwargs)

        # define names and scales
        varUnitsCalculated ={
            'courrant stacks total':{'unit':'A','var':Itotal},
            'production H2(mol/s)':{'unit':'mol/s','var':PH2mols},
            'production H2(Nl/min)':{'unit':'Nl/min','var':PH2Nlmin},
            'fuites fuel BF':{'unit':'Nl/min','var':fuitesFuelBF},
            'fuites fuel BO':{'unit':'Nl/min','var':fuitesFuelBO},
            'fuites fuel':{'unit':'Nl/min','var':fuitesFuel},
            'debit 32 - 303 - 25':{'unit':'Nl/min','var':verifDebitmetre},
            'pile BF':{'unit':'etat Pile BF','var':pileBF.astype(int)},
            'mode_Fuel':{'unit':'etat mode Fuel','var':modeFuelInt},
            'mode hub':{'unit':'mode hub','var':dfmodeHUB['value']}
            }

        listTexts={'mode_Fuel':dfModeFuel,'mode hub':dfmodeHUB['mode hub']}
        print('figure computed in in {:.2f} milliseconds'.format((time.time()-start)*1000))
        return df,varUnitsCalculated,listTexts

    # ==============================================================================
    #                   graphic functions
    # ==============================================================================
    def update_lineshape_fig(self,fig,style='default'):
        if style=='default':
            fig.update_traces(line_shape="linear",mode='lines+markers')
            names = [k.name for k in fig.data]
            vanneTags   = [k for k in names if 'ECV' in k]
            commandTags = [k for k in names if '.HR36' in k]
            boolTags = [k for k in names if self.getUnitofTag(k) in ['ETAT','CMD','Courbe']]
            hvTags=vanneTags+commandTags+boolTags
            fig.for_each_trace(
                lambda trace: trace.update(line_shape="hv",mode='lines+markers') if trace.name in hvTags else (),
            )
        elif style in ['markers','lines','lines+markers']:
            fig.update_traces(line_shape="linear",mode=style)
        elif style =='stairs':
            fig.update_traces(line_shape="hv",mode='lines')
        return fig

    def standardLayout(self,fig,ms=6):
        fig.update_yaxes(showgrid=False)
        fig.update_traces(marker_size=ms)
        fig.update_layout(height=800)
        fig.update_traces(hovertemplate='    <b>%{y:.2f} <br>     %{x|%H:%M:%S}')

    def updatecolortraces(self,fig):
        for tag in fig.data:
            colName=self.dftagColorCode.loc[tag.name,'colorName']
            colTag=self.allHEXColors.loc[colName]
            # print(tag.name,colName,colTag)
            tag.marker.color = colTag
            tag.line.color = colTag
            tag.marker.symbol = self.dftagColorCode.loc[tag.name,'symbol']
            tag.line.dash = self.dftagColorCode.loc[tag.name,'line']
        return fig

    def updatecolorAxes(self,fig):
        for ax in fig.select_yaxes():
            unit    = ax.title.text.strip()
            axColor = self.unitDefaultColors[unit][:-1]
            ax.title.font.color = axColor
            ax.tickfont.color   = axColor
            ax.gridcolor        = axColor

    def plotIndicator(self,df,varUnitsCalculated,listTexts={}):
        dfCalc = pd.concat([pd.DataFrame(s['var']) for s in varUnitsCalculated.values()],axis=1)
        dfCalc.columns = list(varUnitsCalculated.keys())
        unitGroups={}
        unitGroups.update({k:v['unit'] for k,v in varUnitsCalculated.items()})
        df2_plot=pd.concat([dfCalc,df])
        unitGroups.update({t:self.getUnitofTag(t) for t in df.columns})

        fig = self.utils.multiUnitGraph(df2_plot,unitGroups)
        # fig = self.multiUnitGraphSP(df2_plot,unitGroups)
        fig = self.updateLayoutStandard(fig)
        # update mode and hovers
        vanneTags=[k for k in df.columns if 'ECV' in k]
        fig.for_each_trace(
            lambda trace: trace.update(line_shape="hv") if trace.name in vanneTags else (),
        )
        hovertemplatemode='<b>%{y:.2f}' + '<br>     mode:%{text}'
        for k,v in listTexts.items():
            fig.update_traces(selector={'name':k},
                    hovertemplate=hovertemplatemode,
                    text=v,line_shape='hv')
        return fig

    def multiUnitGraphShades(self,df):
        tagMapping = {t:self.getUnitofTag(t) for t in df.columns}
        fig = self.utils.multiUnitGraph(df,tagMapping)
        dfGroups = self.utils.getLayoutMultiUnit(tagMapping)[1]
        listCols = dfGroups.color.unique()
        for k1,g in enumerate(listCols):
            colname = self.colorshades[k1]
            shades = self.colorPalettes[colname]['hex']
            names2change = dfGroups[dfGroups.color==g].index
            fig.update_yaxes(selector={'gridcolor':g},
                        title_font_color=colname[:-1],gridcolor=colname[:-1],tickfont_color=colname[:-1])
            shade=0
            for d in fig.data:
                if d.name in names2change:
                    d['marker']['color'] = shades[shade]
                    d['line']['color']   = shades[shade]
                    shade+=1
            fig.update_yaxes(showgrid=False)
            fig.update_xaxes(showgrid=False)

        # fig.add_layout_image(dict(source=self.imgpeintre,xref="paper",yref="paper",x=0.05,y=1,
        #                             sizex=0.9,sizey=1,sizing="stretch",opacity=0.5,layer="below"))
        # fig.update_layout(template="plotly_white")
        fig.add_layout_image(
            dict(
                source=self.sylfenlogo,
                xref="paper", yref="paper",
                x=0., y=1.02,
                sizex=0.12, sizey=0.12,
                xanchor="left", yanchor="bottom"
            )
        )
        return fig

    def multiUnitGraphSP(self,df,tagMapping=None):
        if not tagMapping:tagMapping = {t:self.getUnitofTag(t) for t in df.columns}
        # print(tagMapping)
        fig = self.utils.multiUnitGraph(df,tagMapping)
        self.standardLayout(fig)
        self.updatecolorAxes(fig)
        fig=self.updatecolortraces(fig)
        return fig

class ConfigFilesSmallPower(ConfigDashTagUnitTimestamp,SmallPowerMaster):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,folderPkl):
        SmallPowerMaster.__init__(self)
        ConfigDashTagUnitTimestamp.__init__(self,folderPkl,self.confFolder)
        SmallPowerMaster._load_plcfile(self)
        self.dfPLC= self.dfPLC[self.dfPLC['DATASCIENTISM']]
        # self.dfPLC= self.dfPLC.set_index('TAG')
        self.legendTags = pd.read_csv(self.confFolder + 'tagLegend.csv')
        self.powerGroups = pd.read_csv(self.confFolder +'powerGroups.csv',index_col=0)
        self._buildColorCode()

    def getListTagsPower(self):
        return self.utils.flattenList([self.getTagsTU(self.powerGroups.loc[k].pattern) for k in self.powerGroups.index])

    def _categorizeTagsPerUnit(self,df):
        dfPLC1 = self.dfPLC[self.dfPLC.TAG.isin(df.columns)]
        unitGroups={}
        for u in dfPLC1.UNITE.unique():
            unitGroups[u]=list(dfPLC1[dfPLC1.UNITE==u].TAG)
        return unitGroups

    def calculatedTags(self,tags,**kwargs):
        dfs=[]
        for tag in tags:
            if re('STK_0[1-4].ET.SUM',tag):
                listTags = self.getTagsTU(tag[:-3]+'HM05')
                df = self.DF_loadTimeRangeTags(listTags=listTags,**kwargs)
                df = df.sum(axis=1)
                df.columns=[tag]
                dfs.append(df)
        return dfs

class ConfigFilesSmallPowerSpark(ConfigDashSpark,SmallPowerMaster):
    def __init__(self,sparkData,sparkConfFile,confFile=None):
        SmallPowerMaster.__init__(self)
        ConfigDashSpark.__init__(sparkData,sparkConfFile,confFile=confFile)
        self.usefulTags = pd.read_csv(self.appDir+'/confFiles/predefinedCategories.csv',index_col=0)
        self.dfPLC = self.__buildPLC()

    def __buildPLC(self):
        return self.dfPLC[self.dfPLC.DATASCIENTISM==True]

class AnalysisPerModule(ConfigFilesSmallPower):
    def __init__(self,folderPkl):
        ConfigFilesSmallPower.__init__(self,folderPkl)
        self.modules = self._loadModules()
        self.listModules = list(self.modules.keys())

    def _buildEauProcess(self):
        eauProcess={}
        eauProcess['pompes']=['PMP_04','PMP_05']
        eauProcess['TNK01'] = ['L219','L221','L200','L205','GWPBC_TNK_01']
        eauProcess['pompe purge'] = ['GWPBC_PMP_01','L202','L210']
        eauProcess['toStack'] = ['L036','L020','GFD_01']
        return eauProcess

    def _buildGV(self):
        GV = {}
        GV['temperatures GV1a'] = ['STG_01a_TT']
        GV['commande GV1a'] = ['STG_01a_HER']
        GV['commande GV1b'] = ['STG_01b_HER']
        GV['ligne gv1a'] = ['L211','L213_H2OPa']
        GV['ligne gv1b'] = ['L211','L213_H2OPb']
        GV['temperatures GV1b'] = ['STG_01b_TT']
        return GV

    def _buildValo(self):
        Valo = {}
        Valo['amont-retour'] = ['GWPBC_PMP_02','L400','L416','L413']
        Valo['echangeur 1'] = ['HPB_HEX_01','L402','L114','L117']
        Valo['condenseur 1'] = ['HPB_CND_01','L408','L404','L021','L022']
        Valo['echangeur 2'] = ['HPB_HEX_02','L404','L115','L116']
        Valo['condenseur 2'] = ['HPB_CND_02','L406','L046','L045']
        Valo['batiment'] = ['GWPBC-HEX-01','L414','L415']
        return Valo

    def _buildGroupeFroid(self):
        groupFroid = {}
        groupFroid['groupe froid'] = ['HPB_CND_03','L417','L418','L056','L057']
        return groupFroid

    def _buildBalayage(self):
        Balayage = {}
        Balayage['echangeur'] = ['HTBA_HEX_01','L133','L134','L135','HPB_RD_01']
        Balayage['stack'] = ['STB_TT_01','STB_TT_02']
        Balayage['blowers'] = ['GWPBH_BLR','L136']
        Balayage['explosimetre'] = ['SFTB_AT_01']
        return Balayage

    def _buildStackBox(self):
        stackBox = {}
        stackBox['chauffants enceinte'] = ['SEH1.STB_HER']
        stackBox['chauffants stacks'] = ['SEH1.STB_STK_0[1-4]_HER']
        stackBox['stack 1'] = ['STB_STK_01']
        stackBox['stack 2'] = ['STB_STK_02']
        stackBox['stack 3'] = ['STB_STK_03']
        stackBox['stack 4'] = ['STB_STK_04']
        stackBox['debits'] = ['STB_GFD','STB_FUEL','STB_GFC','STB_GDC']
        return stackBox

    def _loadModules(self):
        modules = {}
        modules['eau process']=self._buildEauProcess()
        modules['GV']=self._buildGV()
        modules['groupe froid']=self._buildGroupeFroid()
        modules['valo']=self._buildValo()
        modules['balayage']=self._buildBalayage()
        modules['stackbox']=self._buildStackBox()
        return modules

    def _categorizeTagsPerUnit(self,module):
        '''module : {'eauProcess','groupe froid','GV','valo'...} given by self.listModules'''
        mod=self.modules[module]
        ll = self.utils.flattenList([self.listTagsModule(mod,g)[1] for g in mod])
        dfPLC1 = self.dfPLC[self.dfPLC.TAG.isin(ll)]
        unitGroups={}
        for u in dfPLC1.UNITE.unique():
            unitGroups[u]=list(dfPLC1[dfPLC1.UNITE==u].TAG)
        return unitGroups

    # ==========================================================================
    #                     Global module functions
    # ==========================================================================

    def listTagsModule(self,module,group):
        groupList=module[group]
        lplc=pd.concat([self.getTagsTU(pat,ds=False,cols='tdu') for pat in groupList])
        lds=self.utils.flattenList([self.getTagsTU(pat,ds=True) for pat in groupList])
        return lplc,lds

    def listTagsAllModules(self,module,groups=[]):
        mod=self.modules[module]
        LPLC = {g:self.listTagsModule(mod,g)[0] for g in mod}
        LDS = {g:self.listTagsModule(mod,g)[1] for g in mod}
        return LPLC,LDS

    def getDictGroupUnit(self,module,groupsOfModule):
        dictdictGroups = {}
        allgroupsofModule = self.listTagsAllModules(module)[1]
        if not groupsOfModule:groupsOfModule=list(allgroupsofModule.keys())
        groupsOfModule={g:allgroupsofModule[g] for g in groupsOfModule}
        for group,listTags in groupsOfModule.items():
            dictdictGroups[group] = {t:self.utils.detectUnit(self.getUnitofTag(t)) + ' in ' + self.getUnitofTag(t) for t in listTags}

        listTags=self.utils.flattenList([v for v in groupsOfModule.values()])
        return dictdictGroups,listTags
    # ==========================================================================
    #                           GRAPH FUNCTIONS
    # ==========================================================================
    def figureModule(self,module,timeRange,groupsOfModule=None,axisSpace=0.04,hspace=0.02,vspace=0.1,colmap='jet',**kwargs):
        '''
        module : name of the module
        groupsOfModule : list of names of subgroups from the module
        '''
        dictdictGroups,listTags=self.getDictGroupUnit(module,groupsOfModule)
        df  = self.DF_loadTimeRangeTags(timeRange,listTags,**kwargs)
        fig = self.utils.multiUnitGraphSubPlots(df,dictdictGroups,
                        axisSpace=axisSpace,horizontal_spacing=hspace,vertical_spacing=vspace,colormap='jet',
                        subplot_titles=groupsOfModule)
        return fig

    def figureModuleUnits(self,module,timeRange,listUnits=[],grid=None,**kwargs):
        from plotly.subplots import make_subplots
        unitGroups=self._categorizeTagsPerUnit(module)
        if not listUnits: listUnits = list(unitGroups.keys())
        if not grid:grid=self.utils.optimalGrid(len(listUnits))
        fig = make_subplots(rows=grid[0], cols=grid[1],
                                vertical_spacing=0.01,horizontal_spacing=0.1,shared_xaxes=True)
        rows,cols=self.utils.rowsColsFromGrid(len(listUnits),grid)
        for k,r,c in zip(listUnits,rows,cols):
            print(k)
            listTags = unitGroups[k]
            df = self.DF_loadTimeRangeTags(timeRange,listTags,**kwargs)
            df=df.ffill().bfill()
            for l in df.columns:
                fig.add_scatter(y=df[l],x=df.index, mode="lines",
                                name=l, row=r, col=c)
            fig.update_yaxes(title_text=self.utils.detectUnit(k) + ' ( '+ k + ' ) ', row=r, col=c)
            # fig.update_yaxes(color='#FF0000')

        fig.update_xaxes(matches='x')
        fig.update_traces(hovertemplate='<b>%{y:.2f}',)
        fig.update_layout(title={"text": module})
        return fig

    def updateFigureModule(self,fig,module,groupsOfModule,hg,hs,vs,axSP,lgd=False):
        self.utils.printListArgs(module,groupsOfModule,hg,hs,vs,axSP)
        dictdictGroups = self.getDictGroupUnit(module,groupsOfModule)[0]
        figLayout = self.utils.getLayoutMultiUnitSubPlots(dictdictGroups,axisSpace=axSP,
                                                        horizontal_spacing=hs,vertical_spacing=vs)
        fig.layout = figLayout[0].layout
        fig.update_traces(marker=dict(size=5))
        fig.update_traces(hovertemplate='<b>%{y:.2f}')
        fig.update_yaxes(showgrid=False)
        fig.update_layout(height=hg)
        fig.update_layout(showlegend=lgd)
        fig.update_xaxes(matches='x')

        return fig

    def plotQuick(self,df,duration='short',title='',form='df'):
        df=df.ffill().bfill()
        if form=='step': plt.step(x=df.index,y=df.iloc[:,0],)
        if form=='multi': mpl.multiYmpl(df)
        if form=='df': df.plot(colormap='jet')
        datenums=md.date2num(df.index)
        if duration=='short': xfmt = md.DateFormatter('%H:%M')
        else: xfmt = md.DateFormatter('%b-%d')
        ax=plt.gca()
        plt.xticks( rotation=25 )
        # ax.xaxis.set_major_formatter(xfmt)
        # ax.set_ylabel('timestamp')
        mpl.plt.title(title)

class ConfigFilesSmallPower_RealTime(ConfigDashRealTime,SmallPowerMaster):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,connParameters):
        SmallPowerMaster.__init__(self)
        ConfigDashRealTime.__init__(self,self.confFolder,connParameters)
        SmallPowerMaster._load_plcfile(self)
        self.dfPLC= self.dfPLC[self.dfPLC['DATASCIENTISM']]
        self.legendTags = pd.read_csv(self.confFolder + 'tagLegend.csv')
        self.powerGroups = pd.read_csv(self.confFolder +'powerGroups.csv',index_col=0)
        self._buildColorCode()


    def calculatedTags(self,tags,**kwargs):
        dfs=[]
        for tag in tags:
            if len(re.findall('STK_0[1-4].ET.SUM',tag))>0:
                listTags = self.getTagsTU(tag[:-4]+'.*HM05')
                df = self.realtimeTagsDF(tags=listTags,**kwargs)
                # df = self.realtimeTagsDF(tags=listTags,timeWindow=tw)
                dfs.append(pd.DataFrame(df.sum(axis=1),columns=[tag]))
        df = pd.concat(dfs)
        return df
