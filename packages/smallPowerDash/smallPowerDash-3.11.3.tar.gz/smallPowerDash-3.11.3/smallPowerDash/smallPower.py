#!/bin/python
# #######################
# #   GLOBAL VARIABLES  #
# # COMPUTER DEPENDENT  #
# #######################
import os, time, datetime as dt,importlib,pickle
import pandas as pd,numpy as np
from dorianUtils.utilsD import Utils
import comUtils
importlib.reload(comUtils)

import socket
namePC = socket.gethostname()
dbParameters = {
    'host'     : "localhost",
    'port'     : "5432",
    'dbname'   : "jules",
    'user'     : "postgres",
    'password' : "sylfenbdd"
}
NAMESPACE_BECKHOFF = "ns=4;s=GVL."
DATABASE_SIZE_SECONDS=60*10

if 'sylfen' in os.getenv('HOME'):
    baseFolder   = '/home/sylfen/share/dataScientismProd/'
    ENDPOINTURL_BECKHOFF = "opc.tcp://10.10.38.100:4840"
    # PORTBECKHOFF = 502
else:
    baseFolder = '/home/dorian/data/sylfenData/'
    # ENDPOINTURL_BECKHOFF = "opc.tcp://127.0.0.1:65000"
    ENDPOINTURL_BECKHOFF = "opc.tcp://10.10.38.100:4840"
    dbParameters['dbname']   : "juleslocal"

folderpkl = baseFolder + 'smallPowerData/'
FileSystem = comUtils.FileSystem
fs = FileSystem()
appdir = os.path.dirname(os.path.realpath(__file__))
parentdir = fs.getParentDir(appdir)
confFolder = parentdir + 'smallPowerDash/confFiles/'

# ==============================================================================
#                           CONFIGURATIONS
OpcuaConfigMaster = comUtils.OpcuaConfigMaster
SimulatorOPCUA = comUtils.SimulatorOPCUA
DumpingOPCUAClient = comUtils.DumpingOPCUAClient
StreamingVisualisationMaster = comUtils.StreamingVisualisationMaster
class ConfigSmallPower(OpcuaConfigMaster):
    def __init__(self):
        OpcuaConfigMaster.__init__(self,
        folderpkl,confFolder,dbParameters,
        ENDPOINTURL_BECKHOFF,
        nameSpace=NAMESPACE_BECKHOFF,
        dbTimeWindow=DATABASE_SIZE_SECONDS,parkingTime=60*1
        )

class Simulator_SP(ConfigSmallPower,SimulatorOPCUA):
    def __init__(self):
        ConfigSmallPower.__init__(self)
        SimulatorOPCUA.__init__(self,speedflowdata=1000,volatilitySimu=15)

class DumpingClient_SP(ConfigSmallPower,DumpingOPCUAClient):
    def __init__(self):
        ConfigSmallPower.__init__(self)
        DumpingOPCUAClient.__init__(self)

class StreamingVisualisation_SP(ConfigSmallPower,StreamingVisualisationMaster):
    def __init__(self):
        ConfigSmallPower.__init__(self)
        StreamingVisualisationMaster.__init__(self)
class EmptyClass():pass

import plotly.express as px
import plotly.graph_objects as go
class SmallPowerMaster():
    def __init__(self):
        from PIL import Image # new import
        self._loadcolorPalettes()
        self.imgpeintre  = Image.open(self.confFolder + 'peintrepalette.jpeg')
        self.sylfenlogo  = Image.open(self.confFolder +  'logo_sylfen.png')
        self.constantsFile = self.confFolder + 'materialConstants.pkl'
        self._loadConstants()
        listCalculatedTags = ['STK_0'+str(k)+'.ET.SUM' for k in range(1,5)]
        self.utils = Utils()
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
        self._buildColorCode()
        # internalTags = {
        #     'SEH1.FUITEAIR_FT.DS':{''},
        #     'SEH1.FUITEAIR_FT.DS':{''},
        # }
        self.enumFile = self.confFolder + 'enumModeHUB.pkl'
        if os.path.exists(self.enumFile):
            self.enumModeHUB = pickle.load(open(self.enumFile,'rb'))
        else :
            self._dumpConfFiles()


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

    def _dumpConfFiles(self):
        ##### material Constants
        dfConstants=pd.read_excel(self.confFolder + 'materialConstants.xlsx',sheet_name='thermo')
        dfConstants.columns=['description','variableName','value','unit']
        dfConstants = dfConstants.set_index('variableName').dropna()
        # dfConstants = dfConstants[['value','description','unit']]
        pickle.dump(dfConstants,open(self.confFolder + 'materialConstants.pkl','wb'))
        ##### get the enumerations of hub sytem modes
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
        self.enumModeHUB = pickle.load(open(self.enumFile,'rb'))

    # ==============================================================================
    #                   computation functions/INDICATORS
    # ==============================================================================
    def getModeHub(self,timeRange,*args,**kwargs):
        modeSystem = 'SEH1.Etat.HP41'
        dfmodeHUB = self.df_loadtagsrealtime([modeSystem],timeRange,*args,**kwargs)
        dfmodeHUB = dfmodeHUB.dropna().astype(int)
        dfmodeHUB.columns=['value']
        dfmodeHUB['mode hub']=dfmodeHUB.applymap(lambda x:self.enumModeHUB[x])
        return dfmodeHUB

    def repartitionPower(self,timeRange,*args,expand='groups',groupnorm='percent',**kwargs):
        dfs=[]
        armoireTotal = self.getTagsTU('SEH0\.JT.*JTW_')
        dfPtotal = self.df_loadtagsrealtime(armoireTotal,timeRange,*args,**kwargs)

        if expand=='tags':
            puissancesTotales = self.getTagsTU('JTW_00')
            powertags = self.getTagsTU('JTW')
            powertags = [t for t in powertags if t not in armoireTotal+puissancesTotales]
            df = self.df_loadtagsrealtime(powertags,timeRange,*args,**kwargs)
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

            df = self.df_loadtagsrealtime(allTags,timeRange,*args,**kwargs)
            df = df.melt(value_name='value',var_name='tag',ignore_index=False)
            df['group']=df.tag.apply(lambda x:d.loc[x])
            fig=px.area(df,x=df.index,y='value',color='group',groupnorm=groupnorm,line_group='tag')
            fig.update_layout(legend=dict(orientation="h"))
            try:
                for k in dfPtotal.columns:
                    fig.add_traces(go.Scatter(x=dfPtotal.index,y=dfPtotal[k],name=k,
                        mode='lines+markers',marker=dict(color='blue')))
            except:
                print('total power not available')
            fig.update_layout(yaxis_title='power in W')
            self.standardLayout(fig)
        return fig,None

    def bilan_echangeur(self,timeRange,tagDebit='L400',echangeur='CND_03',**kwargs):
        cdn1_tt = self.getTagsTU(echangeur + '.*TT')
        debitEau = self.getTagsTU(tagDebit + '.*FT')
        listTags = cdn1_tt + debit
        if isinstance(timeRange,list) :
            df   = self.df_loadtagsrealtime(listTags,timeRange,**kwargs)
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

    def bilan_valo(self,timeRange,*args,**kwargs):
        '''
        - timeRange : int if realTime==True --> ex : 60*30*2
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

        if isinstance(timeRange,list) :
            df   = self.df_loadtagsrealtime(listTags,timeRange,*args,**kwargs)
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

    def rendement_GV(self,timeRange,*args,activePower=True,wholeDF=False,**kwargs):
        '''
        - activePower : active or apparente power
        - timeRange : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''

        debit_eau = self.getTagsTU('L213_H2OPa.*FT')#g/min
        if activePower:p_chauffants = self.getTagsTU('STG_01a.*JTW')
        else: p_chauffants = self.getTagsTU('STG_01a.*JTVA')
        t_entree_GV = self.getTagsTU('GWPBH_TT')
        t_sortie_GV = self.getTagsTU('L036.*TT')
        TT07 = self.getTagsTU('STG_01a.*TT_02')

        listTags = debit_eau+p_chauffants+t_entree_GV + t_sortie_GV+TT07
        df = self.df_loadtagsrealtime(listTags,timeRange,*args,**kwargs)
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

    def pertes_thermiques_stack(self,timeRange,*args,fuel='N2',activePower=True,**kwargs):
        air_entreeStack = self.getTagsTU('HTBA.*HEX_02.*TT.*01')[0]
        air_balayage = self.getTagsTU('HPB.*HEX_02.*TT.*02')[0]
        fuel_entreeStack = self.getTagsTU('HTBF.*HEX_01.*TT.*01')[0]
        TstackAir = self.getTagsTU('GFC_02.*TT')[0]
        TstackFuel = self.getTagsTU('GFC_01.*TT')[0]
        debitAir = self.getTagsTU('l138.*FT')[0]
        debitFuel = self.getTagsTU('l032.*FT')[0]
        p_chauffants = self.getTagsTU('STK_HER.*JTW')

        listTags = [air_entreeStack,air_balayage,fuel_entreeStack,TstackAir,TstackFuel,debitAir,debitFuel]+p_chauffants

        if isinstance(timeRange,list) :
            df   = self.df_loadtagsrealtime(listTags,timeRange,**kwargs)
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

    def rendement_blower(self,timeRange,*args,activePower=True,**kwargs):
        debitAir = self.getTagsTU('138.*FT')
        pressionAmont_a,pressionAmont_b = self.getTagsTU('131.*PT')
        pressionAval = self.getTagsTU('138.*PT')[0]
        puissanceBlowers = self.getTagsTU('blr.*02.*JT')
        t_aval = self.getTagsTU('l126')
        listTags = debitAir+[pressionAmont_a,pressionAmont_b]+[pressionAval]+t_aval+puissanceBlowers

        df   = self.df_loadtagsrealtime(listTags,timeRange,*args,**kwargs)
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

    def rendement_pumpRecircuFroid(self,timeRange,*args,activePower=True,**kwargs):
        ### compliqué débit amont
        debitAmont   = self.getTagsTU('303.*FT')+''#???
        debitAval = self.getTagsTU('L032.*FT')
        t_aval = self.getTagsTU('L032.*TT')
        pressionAval = ''#???
        puissancePump = self.getTagsTU('gwpbh.*pmp_01.*JTW')
        listTags = debitAmont + debitAval +t_aval + pressionAval + puissancePump
        df   = self.df_loadtagsrealtime(listTags,timeRange,*args,**kwargs)
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

    def cosphi(self,timeRange,*args,**kwargs):
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
        if isinstance(timeRange,list):
            df = self.df_loadtagsrealtime(listTags,timeRange,*args,**kwargs)
        if df.empty:
            return df
        cosphi = {t:{'unit':'cosphi','var':df[jtva].squeeze()/df[jtw].squeeze()} for jtva,jtw,t in zip(jtvas,jtws,tags4Cosphi)}
        # cosphi = {jtva+'/'+jtw:{'unit':'cosphi','var':df[jtva].squeeze()/df[jtw].squeeze()} for jtva,jtw in zip(jtvas,jtws)}
        return df,cosphi

    def fuitesAir(self,timeRange,*args,**kwargs):
        airAmont = self.getTagsTU('l138.*FT')[0]
        airAval = self.getTagsTU('l118.*FT')[0]
        Istacks = self.getTagsTU('STK.*IT.*HM05')
        Tfour = self.getTagsTU('STB_TT_02')[0]
        pressionCollecteur = self.getTagsTU('GFC_02.*PT')[0]
        pressionDiffuseur = self.getTagsTU('GFD_02.*PT')[0]

        listTags =[airAmont,airAval]+Istacks+[Tfour]+[pressionCollecteur,pressionDiffuseur]
        if isinstance(timeRange,list) :
            df   = self.df_loadtagsrealtime(listTags,timeRange,*args,**kwargs)

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

        dfmodeHUB=self.getModeHub(timeRange,*args,**kwargs)
        # dfmodeHUB=self.getModeHub(timeRange,rs=rs)

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

    def fuitesFuel(self,timeRange,*args,**kwargs):
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
        df = self.df_loadtagsrealtime(listTags,timeRange,*args,**kwargs)
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
        dfmodeHUB=self.getModeHub(timeRange,**kwargs)

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

    def standardLayout(self,fig,ms=6,h=800):
        fig.update_yaxes(showgrid=False)
        fig.update_traces(marker_size=ms)
        fig.update_traces(hovertemplate='    <b>%{y:.2f} <br>     %{x|%H:%M:%S}')
        if not h==None:
            fig.update_layout(height=800)

    def updatecolortraces(self,fig):
        for tag in fig.data:
            colName=self.dftagColorCode.loc[tag.name,'colorName']
            colTag=self.allHEXColors.loc[colName]
            # print(tag.name,colName,colTag)
            tag.marker.color = colTag
            tag.line.color = colTag
            tag.marker.symbol = self.dftagColorCode.loc[tag.name,'symbol']
            tag.line.dash = self.dftagColorCode.loc[tag.name,'line']

    def updatecolorAxes(self,fig):
        for ax in fig.select_yaxes():
            titleAxis = ax.title.text
            if not titleAxis==None:
                unit    = titleAxis.strip()
                axColor = self.unitDefaultColors[unit][:-1]
                ax.title.font.color = axColor
                ax.tickfont.color   = axColor
                ax.gridcolor        = axColor

    def plotIndicator(self,df,varUnitsCalculated,listTexts={}):
        if isinstance(df,type(go.Figure())):
            return df

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

    def multiUnitGraphSP(self,df,tagMapping=None,**kwargs):
        if not tagMapping:tagMapping = {t:self.getUnitofTag(t) for t in df.columns}
        # print(tagMapping)
        fig = self.utils.multiUnitGraph(df,tagMapping,**kwargs)
        self.standardLayout(fig)
        self.updatecolorAxes(fig)
        self.updatecolortraces(fig)
        return fig

class SmallPowerComputer(SmallPowerMaster,StreamingVisualisation_SP):
    def __init__(self,*args,**kwargs):
        StreamingVisualisation_SP.__init__(self,*args,**kwargs)
        SmallPowerMaster.__init__(self)
