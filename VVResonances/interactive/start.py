import ROOT
import os, sys
from array import array

from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.CMS_lumi import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="Run2",help="2016 or 2017 or 2018 or Run2")
parser.add_option("-C","--CMSlabel",dest="CMSlabel",type=int,default=0,help="0:None 1:CMS 2:CMS Preliminary 3:CMS Supplementary")
(options,args) = parser.parse_args()



LIKETEMPLATES = 0 ## classify the backgrounds as nonRes and res, like in templates
REMOVEBKGDKFAC = 0 ## remove the Madgraph background NLO k-factors
RESCALEWJETS = 1 ## rescale the W+jets yields



YEAR=options.year
if YEAR not in ["2016","2017","2018","Run2"]:
    parser.error("year must be 2016, 2017, 2018, or Run2")

outDir='ControlPlots'+YEAR
os.system('mkdir -p '+outDir)

if YEAR=="Run2":
    ntuples='ntuples'
else:
    ntuples='ntuples'+YEAR
ntuplesMC=ntuples
ntuplesData=ntuples


## change the CMS_lumi variables (see CMS_lumi.py)
lumi16=35920
lumi17=41530
lumi18=59740
lumiTotal=lumi16+lumi17+lumi18
lumiWeight2016="("+str(lumi16)+"/"+str(lumiTotal)+")"
lumiWeight2017="("+str(lumi17)+"/"+str(lumiTotal)+")"
lumiWeight2018="("+str(lumi18)+"/"+str(lumiTotal)+")"





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


def getPlotters(samples,sampleDir,isData=False,corr="1"):
    sampleTypes=samples.split(',')
    plotters=[]
    pcuts=[]
    filelist=[]

    if sampleDir=='ntuples':
        filelist = [g for flist in [[(path+'/'+f) for f in os.listdir(sampleDir+'/'+path)] for path in os.listdir(sampleDir)] for g in flist]
    else:
        filelist = os.listdir(sampleDir)

    for filename in filelist:
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                fpath=sampleDir+'/'+fname
                print 'Adding file', fpath

                plotters.append(TreePlotter(fpath+'.root','tree'))

                ## Fix for cuts and weights for which the branches differ between years:
                if "ntuples2016" in fpath:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*L1PrefireWeight')
                elif "ntuples2017" in fpath:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)*Flag_rerunEcalBadCalibFilter*L1PrefireWeight')
                elif "ntuples2018" in fpath:
                    pcuts.append('(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET)*Flag_rerunEcalBadCalibFilter')
                else:
                    sys.exit("Year not found, aborting.")

                if not isData:
                    plotters[-1].setupFromFile(fpath+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
                    ##plotters[-1].addCorrectionFactor('lnujj_sfWV','branch')
                    ##plotters[-1].addCorrectionFactor('lnujj_btagWeight','branch')
                    plotters[-1].addCorrectionFactor(corr,'flat')

                    #''' ## remove the Madgraph background NLO k-factors
                    if REMOVEBKGDKFAC:
                        if fname.find("WJetsToLNu_HT")!=-1:
                            wjetsAntiKFactor = 1./1.21
                            plotters[-1].addCorrectionFactor(wjetsAntiKFactor,'flat')
                            print '  reweighting '+fpath+' '+str(wjetsAntiKFactor)
                        elif fname.find("DYJetsToLL_M50_HT")!=-1:
                            dyAntiKFactor = 1./1.23
                            plotters[-1].addCorrectionFactor(dyAntiKFactor,'flat')
                            print '  reweighting '+fpath+' '+str(dyAntiKFactor)
                    #'''

                    #''' ## rescale the W+jets yields (the current factors were computed from 30 < mjet < 50 GeV, on top of the NLO k-factors)
                    if RESCALEWJETS:
                        if fname.find("WJetsToLNu_HT")!=-1: 
                            wjetsFactor=1.
                            if   "ntuples2016" in fpath:  wjetsFactor = 0.96
                            elif "ntuples2017" in fpath:  wjetsFactor = 0.86
                            elif "ntuples2018" in fpath:  wjetsFactor = 0.79
                            plotters[-1].addCorrectionFactor(wjetsFactor,'flat')
                            print '  reweighting '+fpath+' '+str(wjetsFactor)
                    #'''

    return MergedPlotter(plotters,pcuts)


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
    h2.DrawNormalized("HISTSAME")#"SAME")
    legend.AddEntry(h1,leg1,"LF")
    legend.AddEntry(h2,leg2,"LF")#"P")
    legend.Draw()

    pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
    pt.Draw()

    return canvas,h1,h2,legend,pt







cuts={}

cuts['common'] = '1'
#cuts['common'] = cuts['common'] + '*(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)' ## FIXME: HLT flags are temporarily handled via pcuts
cuts['common'] = cuts['common'] + '*((run>500) + (run<500)*lnujj_sfWV)'
cuts['common'] = cuts['common'] + '*(lnujj_nOtherLeptons==0&&nlljj==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0)'
cuts['common'] = cuts['common'] + '*(Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&(Flag_eeBadScFilter*(run>500)+(run<500))&&(Flag_BadMuonFilter*(year==2016)+Flag_BadPFMuonFilter*(year!=2016)))'

## exclude 2018 events where the selected electron is in the problematic HEM15/16 region:
cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&abs(lnujj_l1_l_pdgId)==11&&(-1.55<lnujj_l1_l_phi)&&(lnujj_l1_l_phi<-0.9)&&(-2.5<lnujj_l1_l_eta)&&(lnujj_l1_l_eta<-1.479)))'
## exclude 2018 events where the selected V jet is in the problematic HEM15/16 region:
cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&(-1.55<lnujj_l2_phi)&&(lnujj_l2_phi<-0.9)&&(-2.5<lnujj_l2_eta)&&(lnujj_l2_eta<-1.479)))'
## new cut on pT/M:
cuts['common'] = cuts['common'] + '*(lnujj_l1_pt/lnujj_LV_mass>0.4&&lnujj_l2_pt/lnujj_LV_mass>0.4)'
## lumi-based reweighting for MC:
if YEAR=="Run2":
    cuts['common'] = cuts['common'] + '*( (run>500) + (run<500)*((year==2016)*'+lumiWeight2016+'+(year==2017)*'+lumiWeight2017+'+(year==2018)*'+lumiWeight2018+') )'

cuts['nob'] = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'
## Caution: unlike in makeInputs, the b-tag veto is not in 'common' here

cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['allL'] = '(abs(lnujj_l1_l_pdgId)==11||abs(lnujj_l1_l_pdgId)==13)'
leptons=['e','mu']
leptonsMerged=['allL']

Vtagger='(lnujj_l2_tau2/lnujj_l2_tau1-(-0.08)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt))'
thrHP='0.50'
thrLP='0.80'
cuts['HP'] = '('+Vtagger+'<'+thrHP+')'
cuts['LP'] = '('+thrHP+'<='+Vtagger+'&&'+Vtagger+'<'+thrLP+')'
cuts['allP'] = '('+cuts['HP']+'||'+cuts['LP']+')'
purities=['HP','LP']
puritiesMerged=['allP']

bbtagger='lnujj_l2_btagBOOSTED'
bbtag='(lnujj_l2_btagBOOSTED>0.8)'
cuts['bb'] = bbtag+'*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'
cuts['nobb'] = '(!'+bbtag+')'+'*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'
cuts['allC'] = '1'
cuts['vbf'] = '(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500)'
categories=['bb','nobb','vbf']
categoriesMerged=['allC']


cuts['nonres']='(lnujj_l2_mergedVTruth==0)'
cuts['res']   ='(lnujj_l2_mergedVTruth==1)'
#cuts['resW']  ='(lnujj_l2_mergedVTruth==1&&!(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'
#cuts['resTop']='(lnujj_l2_mergedVTruth==1&&(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'


minMJJ=20.0
maxMJJ=210.0

minMVV=600.0
maxMVV=5000.0



cuts['acceptance']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV}&&lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
cuts['acceptanceMVV']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceMJJ']= "(lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ)
cuts['blinding'] = "((lnujj_l2_softDrop_mass<70)||(150<lnujj_l2_softDrop_mass))"

cuts['0'] = "1"
cuts['AccMVV'] = cuts['acceptanceMVV']
cuts['Acc'] = cuts['acceptance']
cuts['AccBW'] = cuts['acceptance']+'*lnujj_btagWeight'
cuts['CR'] = '*'.join([cuts['b'],cuts['allL'],cuts['allC'],cuts['allP'],cuts['acceptance']])
cuts['SBL'] = '*'.join([cuts['nob'],cuts['allL'],cuts['allC'],cuts['acceptance'],cuts['blinding']])
cuts['SB'] = '*'.join([cuts['nob'],cuts['allL'],cuts['allC'],cuts['allP'],cuts['acceptance'],cuts['blinding']])
cuts['SRMVV'] = '*'.join([cuts['nob'],cuts['allL'],cuts['allC'],cuts['allP'],cuts['acceptanceMVV'],"(lnujj_l2_softDrop_mass>10)"])
cuts['SR'] = '*'.join([cuts['nob'],cuts['allL'],cuts['allC'],cuts['allP'],cuts['acceptance']])




ttbar='TT_pow_pythia,TTHad_pow,TTLep_pow,TTSemi_pow'
singletop='T_tW,TBar_tW,T_tch,TBar_tch'
diboson='WWToLNuQQ,WZTo1L1Nu2Q,ZZTo2L2Q'
vhiggs='WminusLNuHBB,WplusLNuHBB,WminusH_HToBB_WToLNu,WplusH_HToBB_WToLNu,ZH_HToBB_ZToLL'


## 1) backgrounds classified by physics process
QCD   = getPlotters('QCD_HT',ntuplesMC,False)
VJets = getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT',ntuplesMC,False)
Top   = getPlotters(ttbar+','+singletop,ntuplesMC,False)
TT    = getPlotters(ttbar,ntuplesMC,False)
ST    = getPlotters(singletop,ntuplesMC,False)
VV    = getPlotters(diboson,ntuplesMC,False)
#VH   = getPlotters(vhiggs,ntuplesMC,False)
#TopVVVH = getPlotters(ttbar+','+singletop+','+diboson+','+vhiggs,ntuplesMC,False)

## 2) backgrounds classified by non-resonant / resonant contributions, like in makeInputs
nonRes = getPlotters(ttbar+','+singletop+",WJetsToLNu_HT,DYJetsToLL_M50_HT",ntuplesMC,False,cuts['nonres'])
res    = getPlotters(ttbar+','+diboson+','+singletop,ntuplesMC,False,cuts['res'])
#resW   = getPlotters(ttbar+','+diboson+','+singletop,ntuplesMC,False,cuts['resW'])
#resTop = getPlotters(ttbar+','+diboson+','+singletop,ntuplesMC,False,cuts['resTop'])


#Sig = getPlotters('BulkGravToWWToWlepWhad_narrow_1400',ntuplesMC,False)


DATA = getPlotters('SingleElectron_,EGamma_,SingleMuon_,MET_,SinglePhoton_',ntuplesData,True)



## Fill properties

QCD.setFillProperties(1001,ROOT.kGray)
VJets.setFillProperties(1001,ROOT.kAzure-9)
Top.setFillProperties(1001,ROOT.kSpring-5)
TT.setFillProperties(1001,ROOT.kSpring-5)
ST.setFillProperties(1001,ROOT.kSpring+2)
VV.setFillProperties(1001,ROOT.kOrange-2)
#VH.setFillProperties(1001,ROOT.kRed-9)
#TopVVVH.setFillProperties(1001,ROOT.kSpring+5)

nonRes.setFillProperties(1001,ROOT.TColor.GetColor("#A5D2FF"))#ROOT.kBlue+1)#ROOT.kAzure-9)
res.setFillProperties(1001,ROOT.TColor.GetColor("#60B037"))#ROOT.kGreen+1)#ROOT.kSpring-5)
#resW.setFillProperties(1001,ROOT.TColor.GetColor("#37B04D"))#ROOT.kGreen+1)#ROOT.kSpring-5)
#resTop.setFillProperties(1001,ROOT.TColor.GetColor("#C3D631"))#ROOT.kGreen+1)#ROOT.kSpring-5)

#Sig.setFillProperties(1001,ROOT.kRed+1)



## Stack for lnu+J
lnujjStack = StackPlotter()

if LIKETEMPLATES:
    lnujjStack.addPlotter(nonRes,"nonRes","W+jets","background")
    lnujjStack.addPlotter(res,"res","W+V/t","background")
    #lnujjStack.addPlotter(resW,"resW","W peak","background")
    #lnujjStack.addPlotter(resTop,"resTop","top peak","background")
else:
    lnujjStack.addPlotter(QCD,"QCD","QCD multijet","background")
    #lnujjStack.addPlotter(VH,"VH","VH","background")
    lnujjStack.addPlotter(VV,"VV","VV","background")
    lnujjStack.addPlotter(VJets,"WJets","V+Jets","background")
    #lnujjStack.addPlotter(Top,"top","top","background")
    lnujjStack.addPlotter(ST,"ST","single top","background")
    lnujjStack.addPlotter(TT,"TT","t#bar{t}","background")
    #lnujjStack.addPlotter(TopVVVH,"topVVVH","top, VV, VH","background")

#lnujjStack.addPlotter(Sig,"WWsig","G_{Bulk}#rightarrowWW, m = 1.4 TeV","signal")

lnujjStack.addPlotter(DATA,"data_obs","Data","data")







