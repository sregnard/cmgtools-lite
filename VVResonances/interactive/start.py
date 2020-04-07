import ROOT
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *
import os
from array import array

from DoubleBscalefactors import *
from DoubleBefficiencies import *

DONORMMC       = 0
DONORMDATA     = 0
DONORMMCASDATA = 0
DOSIGNALSHAPES = 0
DOSIGNALYIELDS = 0
DOSIGNALCTPL   = 0
DORESONANT     = 0
DONONRESONANT  = 0
DONORMMCCR     = 0
DONORMDATACR   = 0
DONONRESONANTCR= 0
DOXWW = 0
DOXWZ = 0
DOXWH = 0
RENORMNONRES   = 0
REMOVE2018ELEHEM1516 = 0


MERGELEPNONRES = 0
MERGEPURNONRES = 0
MERGECATNONRES = 0


###############################################
###############################################
#################  PARAMETERS  ################
###############################################
###############################################

minMJJ=20.0
maxMJJ=210.0

minMVV=600.0
maxMVV=5000.0

binsMJJ={}
binsMJJ['bb']=19
binsMJJ['nobb']=38
binsMJJ['allC']=95
binsMVV={}
binsMVV['bb']  =176
binsMVV['nobb']=176
binsMVV['allC']=176


outDir='Inputs_Run2/'
os.system('mkdir -p '+outDir)

ntuples='ntuples'


tau21SF={ ## TBU 
    'HP' : '( (year==2016)*1.00 + (year==2017)*1.00 + (year==2018)*1.00 )',
    'LP' : '( (year==2016)*1.00 + (year==2017)*1.00 + (year==2018)*1.00 )',
    }

bbSFWW_2016 = DoubleBsf_M2_B_80X
bbSFWZ_2016 = DoubleBsf_M2_B_80X
bbSFWH_2016 = DoubleBsf_M2_S_80X
bbEffWW_2016 = EffMC_M2_XWW_2016
bbEffWZ_2016 = EffMC_M2_XWZ_2016
bbEffWH_2016 = EffMC_M2_XWH_2016
bbSFWW_2017 = DoubleBsf_M2_B_94X
bbSFWZ_2017 = DoubleBsf_M2_B_94X
bbSFWH_2017 = DoubleBsf_M2_S_94X
bbEffWW_2017 = EffMC_M2_XWW_2017
bbEffWZ_2017 = EffMC_M2_XWZ_2017
bbEffWH_2017 = EffMC_M2_XWH_2017
bbSFWW_2018 = DoubleBsf_M2_B_102X
bbSFWZ_2018 = DoubleBsf_M2_B_102X
bbSFWH_2018 = DoubleBsf_M2_S_102X
bbEffWW_2018 = EffMC_M2_XWW_2018
bbEffWZ_2018 = EffMC_M2_XWZ_2018
bbEffWH_2018 = EffMC_M2_XWH_2018
bbWgtWW={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWW_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2016[ptcut])+')/(1-'+str(bbEffWW_2016[ptcut])+'))') for ptcut,sf in bbSFWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2017[ptcut])+')/(1-'+str(bbEffWW_2017[ptcut])+'))') for ptcut,sf in bbSFWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2018[ptcut])+')/(1-'+str(bbEffWW_2018[ptcut])+'))') for ptcut,sf in bbSFWW_2018))+'))',
    }
bbWgtWZ={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2016[ptcut])+')/(1-'+str(bbEffWZ_2016[ptcut])+'))') for ptcut,sf in bbSFWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2017[ptcut])+')/(1-'+str(bbEffWZ_2017[ptcut])+'))') for ptcut,sf in bbSFWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2018[ptcut])+')/(1-'+str(bbEffWZ_2018[ptcut])+'))') for ptcut,sf in bbSFWZ_2018))+'))',
    }
bbWgtWH={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2016[ptcut])+')/(1-'+str(bbEffWH_2016[ptcut])+'))') for ptcut,sf in bbSFWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2017[ptcut])+')/(1-'+str(bbEffWH_2017[ptcut])+'))') for ptcut,sf in bbSFWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2018[ptcut])+')/(1-'+str(bbEffWH_2018[ptcut])+'))') for ptcut,sf in bbSFWH_2018))+'))',
    }
print bbWgtWW['bb']
print bbWgtWW['nobb']


lumi16=35920
lumi17=41530
lumi18=59740
lumiTotal=lumi16+lumi17+lumi18
lumiWeight2016="("+str(lumi16)+"/"+str(lumiTotal)+")"
lumiWeight2017="("+str(lumi17)+"/"+str(lumiTotal)+")"
lumiWeight2018="("+str(lumi18)+"/"+str(lumiTotal)+")"


cuts={}

cuts['common'] = '1'
cuts['common'] = cuts['common'] + '*(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*((run>500) + (run<500)*lnujj_sfWV)' ## changed from lnujj_sf to lnujj_sfWV for 2016 
cuts['common'] = cuts['common'] + '*(lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0)'
cuts['common'] = cuts['common'] + '*(Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&(Flag_eeBadScFilter*(run>500)+(run<500))&&Flag_badMuonFilter)'
if REMOVE2018ELEHEM1516:
    cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&abs(lnujj_l1_l_pdgId)==11&&(-1.55<lnujj_l1_l_phi)&&(lnujj_l1_l_phi<-0.9)&&(-2.5<lnujj_l1_l_eta)&&(lnujj_l1_l_eta<-1.479)))'
## new cut on pT/M:
cuts['common'] = cuts['common'] + '*(lnujj_l1_pt/lnujj_LV_mass>0.4&&lnujj_l2_pt/lnujj_LV_mass>0.4)'
## ensure orthogonality with VBF analysis:
cuts['common'] = cuts['common'] + '*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'
## lumi-based reweighting for MC
cuts['common'] = cuts['common'] + '*( (run>500) + (run<500)*((year==2016)*'+lumiWeight2016+'+(year==2017)*'+lumiWeight2017+'+(year==2018)*'+lumiWeight2018+') )'

cuts['nob'] = '(lnujj_nMediumBTags==0)'
cuts['b'] = '(lnujj_nMediumBTags>0)'
cuts['CR'] = cuts['common'] + '*' + cuts['b'] + '*lnujj_btagWeight'
cuts['common'] = cuts['common'] + '*' + cuts['nob'] + '*lnujj_btagWeight'

cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['allL'] = '(abs(lnujj_l1_l_pdgId)==11||abs(lnujj_l1_l_pdgId)==13)'
leptons=['e','mu']
leptonsMerged=['allL']

Vtagger='(lnujj_l2_tau2/lnujj_l2_tau1-(-0.08)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt))'
thrHP=0.55
thrLP=0.96
cuts['HP'] = '('+Vtagger+'<'+str(thrHP)+')'
cuts['LP'] = '('+str(thrHP)+'<='+Vtagger+'&&'+Vtagger+'<'+str(thrLP)+')'
cuts['allP'] = '('+cuts['HP']+'||'+cuts['LP']+')'
purities=['HP','LP']
puritiesMerged=['allP']

bbtag='(lnujj_l2_btagBOOSTED>0.8)'
cuts['bb'] = bbtag
cuts['nobb'] = '(!'+bbtag+')'
cuts['allC'] = '1'
categories=['bb','nobb']
categoriesMerged=['allC']


cuts['resW']  ='(lnujj_l2_mergedVTruth==1&&!(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'
cuts['resTop']='(lnujj_l2_mergedVTruth==1&&(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'


renormWJets2016='0.8727054353'
renormWJets2017='0.699592444047'
renormWJets2018='0.728005348312'
renormWJets3Yrs=",".join([renormWJets2016,renormWJets2017,renormWJets2018])
renormWJetsRun2='0.760376974966'


WWTemplate="ntuples2016/BulkGravToWWToWlepWhad_narrow,ntuples2017/BulkGravToWWToWlepWhad_narrow,ntuples2018/BulkGravToWWToWlepWhad_narrow"
BRWW=2.*0.327*0.6760

WZTemplate="ntuples2016/WprimeToWZToWlepZhad_narrow,ntuples2017/WprimeToWZToWlepZhad_narrow,ntuples2018/WprimeToWZToWlepZhad_narrow"
BRWZ=0.327*0.6991

WHTemplate="ntuples2016/WprimeToWHToWlepHinc_narrow,ntuples2017/WprimeToWHToWlepHinc_narrow,ntuples2018/WprimeToWHToWlepHinc_narrow"
BRWH=0.327

resWTemplate = "ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WWToLNuQQ,ntuples2017/WWToLNuQQ,ntuples2018/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2017/WZTo1L1Nu2Q,ntuples2018/WZTo1L1Nu2Q,ntuples2016/ZZTo2L2Q,ntuples2017/ZZTo2L2Q,ntuples2018/ZZTo2L2Q,ntuples2016/T_tW,ntuples2017/T_tW,ntuples2018/T_tW,ntuples2016/TBar_tW,ntuples2017/TBar_tW,ntuples2018/TBar_tW"
resTopTemplate = resWTemplate
nonResTemplate = "ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WJetsToLNu_HT,ntuples2017/WJetsToLNu_HT,ntuples2018/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT,ntuples2017/DYJetsToLL_M50_HT,ntuples2018/DYJetsToLL_M50_HT,ntuples2016/T_tW,ntuples2017/T_tW,ntuples2018/T_tW,ntuples2016/TBar_tW,ntuples2017/TBar_tW,ntuples2018/TBar_tW"
allMCTemplate = "ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WWToLNuQQ,ntuples2017/WWToLNuQQ,ntuples2018/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2017/WZTo1L1Nu2Q,ntuples2018/WZTo1L1Nu2Q,ntuples2016/ZZTo2L2Q,ntuples2017/ZZTo2L2Q,ntuples2018/ZZTo2L2Q,ntuples2016/T_tW,ntuples2017/T_tW,ntuples2018/T_tW,ntuples2016/TBar_tW,ntuples2017/TBar_tW,ntuples2018/TBar_tW,ntuples2016/WJetsToLNu_HT,ntuples2017/WJetsToLNu_HT,ntuples2018/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT,ntuples2017/DYJetsToLL_M50_HT,ntuples2018/DYJetsToLL_M50_HT"
dataTemplate = "ntuples2016/SingleElectron,ntuples2017/SingleElectron,ntuples2018/EGamma,ntuples2016/SingleMuon,ntuples2017/SingleMuon,ntuples2018/SingleMuon,ntuples2016/MET,ntuples2017/MET,ntuples2018/MET"

VJetsTemplate = "ntuples2016/WJetsToLNu_HT,ntuples2017/WJetsToLNu_HT,ntuples2018/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT,ntuples2017/DYJetsToLL_M50_HT,ntuples2018/DYJetsToLL_M50_HT"




def efficiency1D(plotter,var,bins,denom,num):    
    h1 = plotter.drawTH1Binned(var,denom,"1",bins)
    h2 = plotter.drawTH1Binned(var,denom+"*"+num,"1",bins)
    
#    graph=ROOT.TGraphAsymmErrors()
#    graph.Divide(h2,h1)
    h2.Divide(h1)
    return h2


def efficiency2D(plotter,var,binsx,binsy,denom,num):
    h1 = plotter.drawTH2Binned(var,denom,"1",binsx,binsy)
    h2 = plotter.drawTH2Binned(var,denom+"*"+num,"1",binsx,binsy)
    h2.Divide(h1)
    return h2


def makeEff():
    f=ROOT.TFile("trigger.root","RECREATE")
    f.cd()
    g=efficiency1D(VJets,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['e'],'HLT_ELE']),'HLT_MET120')
    g.Write("MET_ELE_MC")
    g=efficiency1D(data,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['e'],'HLT_ELE']),'HLT_MET120')
    g.Write("MET_ELE_DATA")
    g=efficiency1D(VJets,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['mu'],'HLT_MU']),'HLT_MET120')
    g.Write("MET_MU_MC")
    g=efficiency1D(data,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['mu'],'HLT_MU']),'HLT_MET120')
    g.Write("MET_MU_DATA")


    g=efficiency2D(VJets,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['e'],'HLT_MET120']),'HLT_ELE')
    g.Write("ELE_MC")
    g=efficiency2D(data,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['e'],'HLT_MET120']),'HLT_ELE')
    g.Write("ELE_DATA")

    g=efficiency2D(VJets,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['mu'],'HLT_MET120']),'HLT_MU')
    g.Write("MU_MC")
    g=efficiency2D(data,"lnujj_l1_l_eta:lnujj_l1_l_pt",[50,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['mu'],'HLT_MET120']),'HLT_MU')
    g.Write("MU_DATA")
    
    f.Close()





def getPlotters(samples,isData=False,corr="1"):
    sampleTypes=samples.split(',')
    dataPlotters=[]


    filelist = [g for flist in [[(path+'/'+f) for f in os.listdir("ntuples"+'/'+path)] for path in os.listdir("ntuples")] for g in flist]
    for filename in filelist:
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue

                dataPlotters.append(TreePlotter('ntuples/'+fname+'.root','tree'))
                if not isData:    
                    dataPlotters[-1].setupFromFile('ntuples/'+fname+'.pck')
                    dataPlotters[-1].addCorrectionFactor('xsec','tree')
                    dataPlotters[-1].addCorrectionFactor('genWeight','tree')
                    dataPlotters[-1].addCorrectionFactor('puWeight','tree')
                    dataPlotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
    return  dataPlotters


def compare(p1,p2,var,cut1,cut2,bins,mini,maxi,title,unit,leg1,leg2):
    canvas = ROOT.TCanvas("canvas","")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    canvas.cd()
    legend = ROOT.TLegend(0.62,0.2,0.92,0.4,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)


    h1=p1.drawTH1(var,cut1,"1",bins,mini,maxi,title,unit)
    h2=p2.drawTH1(var,cut2,"1",bins,mini,maxi,title,unit)
    h1.DrawNormalized("HIST")
    h2.DrawNormalized("SAME")
    legend.AddEntry(h1,leg1,"LF")
    legend.AddEntry(h2,leg2,"P")
    legend.Draw()

    pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
#    text = pt.AddText(0.01,0.3,"CMS Preliminary 2016")
#    text = pt.AddText(0.25,0.3,"#sqrt{s} = 13 TeV")
    pt.Draw()   


    return canvas,h1,h2,legend,pt





nonResPlotters = getPlotters(allMCTemplate,0,cuts['nonres'])
nonRes = MergedPlotter(nonResPlotters)

vjetsPlotters = getPlotters(VJetsTemplate,0)
vjets = MergedPlotter(vjetsPlotters)

ttvvPlotters = getPlotters(resWTemplate,0)
ttvv = MergedPlotter(ttvvPlotters)

resWPlotters = getPlotters(allMCTemplate,0,cuts['resW'])
resW = MergedPlotter(resWPlotters)

resTPlotters = getPlotters(allMCTemplate,0,cuts['resTop'])
resTop = MergedPlotter(resTPlotters)


signalPlotters = getPlotters(WWTemplate,0)
signal = MergedPlotter(signalPlotters)


dataPlotters = getPlotters(dataTemplate,1)
data = MergedPlotter(dataPlotters)


#Fill properties
nonRes.setFillProperties(1001,ROOT.kAzure-9)
vjets.setFillProperties(1001,ROOT.kAzure-9)
#BKG.setFillProperties(1001,ROOT.kAzure-9)
ttvv.setFillProperties(1001,ROOT.kSpring-5)
resW.setFillProperties(1001,ROOT.kSpring-5)
resTop.setFillProperties(1001,ROOT.kSpring+2)



#W.setFillProperties(1001,ROOT.kSpring-5)
#QCD.setFillProperties(1001,ROOT.kGray)


#Stack for lnu+J
lnujjStack = StackPlotter()
#lnujjStack.addPlotter(QCD,"QCD","QCD multijet","background")
lnujjStack.addPlotter(vjets,"WJets","V+Jets","background")
#lnujjStack.addPlotter(BKG,"Bkg","V+Jets","background")
lnujjStack.addPlotter(ttvv,"top","top/VV","background")
#lnujjStack.addPlotter(W,"W","W","background")
lnujjStack.addPlotter(data,"data_obs","Data","data")




