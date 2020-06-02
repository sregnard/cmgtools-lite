import ROOT
import os, sys
from array import array

from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="Run2",help="2016 or 2017 or 2018 or Run2")
parser.add_option("-C","--CMSlabel",dest="CMSlabel",type=int,default=0,help="0:None 1:CMS 2:CMS Preliminary 3:CMS Supplementary")
(options,args) = parser.parse_args()



LIKETEMPLATES = 0 ## classifies the backgrounds as nonRes/resW/resTop like in templates
prs = "b1" if not LIKETEMPLATES else "b2"

RENORMFROMLOWMASSSB = 1




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
lumiValue=""
if YEAR=="2016":
  lumiValue=str(lumi16)
elif YEAR=="2017":
  lumiValue=str(lumi17)
elif YEAR=="2018":
  lumiValue=str(lumi18)
elif YEAR=="Run2":
  lumiValue=str(lumiTotal)
lumiWeight2016="("+str(lumi16)+"/"+str(lumiTotal)+")"
lumiWeight2017="("+str(lumi17)+"/"+str(lumiTotal)+")"
lumiWeight2018="("+str(lumi18)+"/"+str(lumiTotal)+")"



def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  #canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  canvas.SaveAs(name+".png")
  #canvas.SaveAs(name+".eps")
  #os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  #os.system("rm "+name+".eps")

def cmsLabel(canvas):
  if options.CMSlabel==0:
    cmslabel_not(canvas,YEAR,11)
  elif options.CMSlabel==1:
    cmslabel_final(canvas,YEAR,11)
  elif options.CMSlabel==2:
    cmslabel_prelim(canvas,YEAR,11)
  elif options.CMSlabel==3:
    cmslabel_suppl(canvas,YEAR,11)



def getPlotters(samples,sampleDir,isData=False,corr="1"):
    sampleTypes=samples.split(',')
    plotters=[]
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
                print 'Adding file',fname
                plotters.append(TreePlotter(sampleDir+'/'+fname+'.root','tree'))
                if not isData:
                    plotters[-1].setupFromFile(sampleDir+'/'+fname+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
                    plotters[-1].addCorrectionFactor(corr,'flat')
    return plotters


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
cuts['common'] = cuts['common'] + '*(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*((run>500) + (run<500)*lnujj_sfWV)' ## changed from lnujj_sf to lnujj_sfWV for 2016
cuts['common'] = cuts['common'] + '*(lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0)'
cuts['common'] = cuts['common'] + '*(Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&(Flag_eeBadScFilter*(run>500)+(run<500))&&Flag_badMuonFilter)'
## excluding the problematic HEM15/16 region:
cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&abs(lnujj_l1_l_pdgId)==11&&(-1.55<lnujj_l1_l_phi)&&(lnujj_l1_l_phi<-0.9)&&(-2.5<lnujj_l1_l_eta)&&(lnujj_l1_l_eta<-1.479)))'
## new cut on pT/M:
cuts['common'] = cuts['common'] + '*(lnujj_l1_pt/lnujj_LV_mass>0.4&&lnujj_l2_pt/lnujj_LV_mass>0.4)'
## lumi-based reweighting for MC:
if YEAR=="Run2":
    cuts['common'] = cuts['common'] + '*( (run>500) + (run<500)*((year==2016)*'+lumiWeight2016+'+(year==2017)*'+lumiWeight2017+'+(year==2018)*'+lumiWeight2018+') )'

cuts['nob'] = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'
## Caution: the b-tag veto is not in 'common' here

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




ttbar='TT_pow,TTHad_pow,TTLep_pow,TTSemi_pow'
singletop='T_tW,TBar_tW'
diboson='WWToLNuQQ,WZTo1L1Nu2Q,ZZTo2L2Q'
vhiggs='WminusLNuHBB,WplusLNuHBB,WminusH_HToBB_WToLNu,WplusH_HToBB_WToLNu,ZH_HToBB_ZToLL'
electronPD='SingleElectron_,EGamma_'


## 1) backgrounds classified by physics process
QCDPlotters = getPlotters('QCD_HT',ntuplesMC,False)
QCD = MergedPlotter(QCDPlotters)
VJetsPlotters = getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT',ntuplesMC,False)
VJets = MergedPlotter(VJetsPlotters)
TopPlotters = getPlotters(ttbar+','+singletop,ntuplesMC,False)
top = MergedPlotter(TopPlotters)
TTPlotters = getPlotters(ttbar,ntuplesMC,False)
TT = MergedPlotter(TTPlotters)
STPlotters = getPlotters(singletop,ntuplesMC,False)
ST = MergedPlotter(STPlotters)
VVPlotters = getPlotters(diboson,ntuplesMC,False)
VV = MergedPlotter(VVPlotters)
#VHPlotters = getPlotters(vhiggs,ntuplesMC,False)
#VH = MergedPlotter(VHPlotters)
#TopVVVHPlotters = getPlotters(ttbar+','+singletop+','+diboson+','+vhiggs,ntuplesMC,False)
#topVVVH = MergedPlotter(TopVVVHPlotters)

## 2) backgrounds classified by non-resonant / resonant contributions, like in makeInputs
nonResPlotters = getPlotters(ttbar+','+singletop+",WJetsToLNu_HT,DYJetsToLL_M50_HT",ntuplesMC,False,cuts['nonres'])
nonRes = MergedPlotter(nonResPlotters)
resPlotters = getPlotters(ttbar+','+diboson+','+singletop,ntuplesMC,False,cuts['res'])
res = MergedPlotter(resPlotters)
#resWPlotters = getPlotters(ttbar+','+diboson+','+singletop,ntuplesMC,False,cuts['resW'])
#resW = MergedPlotter(resWPlotters)
#resTopPlotters = getPlotters(ttbar+','+diboson+','+singletop,ntuplesMC,False,cuts['resTop'])
#resTop = MergedPlotter(resTopPlotters)


#SigPlotters = getPlotters('BulkGravToWWToWlepWhad_narrow_1400',ntuplesMC,False)
#sig = MergedPlotter(SigPlotters)


DATAPlotters = getPlotters(electronPD+',SingleMuon_,MET_',ntuplesData,True)
data = MergedPlotter(DATAPlotters)



## Fill properties

QCD.setFillProperties(1001,ROOT.kGray)
VJets.setFillProperties(1001,ROOT.kAzure-9)
top.setFillProperties(1001,ROOT.kSpring-5)
TT.setFillProperties(1001,ROOT.kSpring-5)
ST.setFillProperties(1001,ROOT.kSpring+2)
VV.setFillProperties(1001,ROOT.kOrange-2)
#VH.setFillProperties(1001,ROOT.kRed-9)
#topVVVH.setFillProperties(1001,ROOT.kSpring+5)

nonRes.setFillProperties(1001,ROOT.TColor.GetColor("#A5D2FF"))#ROOT.kBlue+1)#ROOT.kAzure-9)
res.setFillProperties(1001,ROOT.TColor.GetColor("#60B037"))#ROOT.kGreen+1)#ROOT.kSpring-5)
#resW.setFillProperties(1001,ROOT.TColor.GetColor("#37B04D"))#ROOT.kGreen+1)#ROOT.kSpring-5)
#resTop.setFillProperties(1001,ROOT.TColor.GetColor("#C3D631"))#ROOT.kGreen+1)#ROOT.kSpring-5)

#sig.setFillProperties(1001,ROOT.kRed+1)



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
    #lnujjStack.addPlotter(top,"top","top","background")
    lnujjStack.addPlotter(ST,"ST","single top","background")
    lnujjStack.addPlotter(TT,"TT","t#bar{t}","background")
    #lnujjStack.addPlotter(topVVVH,"topVVVH","top, VV, VH","background")

#lnujjStack.addPlotter(sig,"WWsig","G_{Bulk}#rightarrowWW, m = 1.4 TeV","signal")

lnujjStack.addPlotter(data,"data_obs","Data","data")


'''
## Stack for res. bkgd splitting tests
resStack = StackPlotter()
resStack.addPlotter(res,"res","resonant","background")
#'''





plots = [
  #( "", "", , , , "", "" ),
  ( "nVert",                  "nVert",                       60,  0.,  60.,   "N primary vertices", ""    ),
  ( "lnujj_l1_l_pt",          "lnujj_l1_l_pt",               100, 0.,  1000., "lepton p_{T}",       "GeV" ),
  ( "lnujj_l1_l_eta",         "lnujj_l1_l_eta",              60,  -3., 3.,    "lepton #eta",        ""    ),
  ( "lnujj_l1_l_phi",         "lnujj_l1_l_phi",              80,  -4., 4.,    "lepton #phi",        ""    ),
  ( "met_pt",                 "met_pt",                      100, 0.,  1000., "E_{T}^{miss}",       "GeV" ),
  ( "met_phi",                "met_phi",                     80,  -4., 4.,    "#phi(E_{T}^{miss})", ""    ),
  ( "lnujj_l1_pt",            "lnujj_l1_pt",                 100, 0.,  1000., "W p_{T}",            "GeV" ),
  ( "lnujj_l1_mt",            "lnujj_l1_mt",                 60,  0.,  150.,  "W m_{T}",            "GeV" ),
  ( "lnujj_l2_pt",            "lnujj_l2_pt",                 100, 0.,  1000., "jet p_{T}",          "GeV" ),
  ( "lnujj_l2_eta",           "lnujj_l2_eta",                60,  -3., 3.,    "jet #eta",           ""    ),
  ( "lnujj_l2_phi",           "lnujj_l2_phi",                80,  -4., 4.,    "jet #phi",           ""    ),
  ( "mjet",                   "lnujj_l2_softDrop_mass",      100, 0.,  250.,  "m_{jet}",            "GeV" ),
  #( "mjet",                   "lnujj_l2_softDrop_mass",      45,  30., 210.,  "m_{jet}",            "GeV" ),
  #( "mjet",                   "lnujj_l2_softDrop_mass",      60,  0.,  240.,  "m_{jet}",            "GeV" ),
  ( "mWV",                    "lnujj_LV_mass",               88,  600.,5000., "m_{WV}",             "GeV" ),
  ( "highestOtherBTag",       "lnujj_highestOtherBTag",      40,  -1., 1.,    "highest b tag",      ""    ),
  ( "tau21",                  "lnujj_l2_tau2/lnujj_l2_tau1", 50,  0.,  1.,    "#tau_{21}",          ""    ),
  ( "tau21DDTold",            "lnujj_l2_tau2/lnujj_l2_tau1-(-0.06845)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)", 50,  0.,  1.,    "#tau_{21}^{DDT} (old)", "" ),
  ( "tau21DDT",               "lnujj_l2_tau2/lnujj_l2_tau1-(-0.08376)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)", 50,  0.,  1.,    "#tau_{21}^{DDT}",       "" ),
  ( "N2b1",                   "lnujj_l2_N2b1",               50,  0.,  0.5,   "N_{2}^{(1)}",        ""    ),
  ( "N2b1DDT",                "lnujj_l2_N2b1-(-0.013916)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)",              50,  0.,  0.5,   "N_{2}^{(1), DDT}",      "" ),
  ( "N2b2",                   "lnujj_l2_N2b2",               50,  0.,  0.5,   "N_{2}^{(2)}",        "",   ),
  ( "DoubleB",                bbtagger,                      50,  -1., 1.,    "DoubleB",            "",   ),
  ( ("minsubjetdeepcsv","minsubjetcsv")[YEAR=="2016"],   "min(lnujj_l2_s1BTag,lnujj_l2_s2BTag)",    50,   0.,  1., "min. subjet "+("DeepCSV","CSV")[YEAR=="2016"], "" ),
  ( "rhoprime",               "log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)",   140,  -2., 5., "#rho'", "" ),
  ( "lnujj_nLooseBTags",      "lnujj_nLooseBTags",           5,   0.,  5.,    "N loose b tags",     ""    ),
  ( "lnujj_nMediumBTags",     "lnujj_nMediumBTags",          5,   0.,  5.,    "N medium b tags",    ""    ),
  ( "lnujj_nTightBTags",      "lnujj_nTightBTags",           5,   0.,  5.,    "N tight b tags",     ""    ),
  #( "lnujj_l2_minpts1pts2overpts1pluspts2", "min(lnujj_l2_softDrop_s1_pt,lnujj_l2_softDrop_s2_pt)/(lnujj_l2_softDrop_s1_pt+lnujj_l2_softDrop_s2_pt)", 50,  0.,  1.,    "SD min(p_{T,s1}, p_{T,s2}) / (p_{T,s1} + p_{T,s2})",""    ),
  #( "lnujj_l2_gen_pt",        "lnujj_l2_gen_pt",             100, 0.,  1000., "gen jet p_{T}",      "GeV" ),
  #( "lnujj_l2_gen_eta",       "lnujj_l2_gen_eta",            60,  -3., 3.,    "gen jet #eta",       ""    ),
  #( "run",                    "run",                         120,270000.,330000.,"run number",      ""    ),
  ( "run",                    "run",                         200,290000.,310000.,"run number",      ""    ),
  ( "lnujj_vbfDEta",          "lnujj_vbfDEta",               100,0.,6.,       "#Delta#eta_{dijet}", ""    ),
  ( "lnujj_vbfMass",          "lnujj_vbfMass",               100,0.,1500.,    "m_{dijet}",          "GeV" ),
  ( "lnujj_nJets",            "lnujj_nJets",                 13,0.,12.,       "N_{jets}",           ""    ),
]


#'''
renormFactorLMSB = 1.
if RENORMFROMLOWMASSSB:
    cutsLMSB = '*'.join([cuts['common'],cuts['SR'],"(lnujj_l2_softDrop_mass>30&&lnujj_l2_softDrop_mass<50)"])
    pl_ = plots[11]
    stack_ = lnujjStack.drawStackWithRatio(pl_[1],cutsLMSB,lumiValue,pl_[2],pl_[3],pl_[4],pl_[5],pl_[6])
    renormFactorLMSB = stack_['ratio']
    print "Renormalization factor for W+jets in the signal region, computed as the data/bkgd ratio in the [30, 50 GeV] mjet sideband: ", renormFactorLMSB

#for r in ['0','AccMVV','CR','SB','SR']:
#for r in ['CR','SR']:
for r in ['CR','SB']: ## uncomment this one for the plots of analysis note
#for r in ['0']:
#for r in ['AccMVV']:
#for r in ['Acc']:
#for r in ['CR']:
#for r in ['SBL']:
#for r in ['SB']:
#for r in ['SRMVV']:
#for r in ['SR']:
  for l in leptons: #leptonsMerged:
    for p in puritiesMerged: #purities:
      for c in categoriesMerged: #categories:

            cat=l+"_"+p+"_"+c

            #if ('all' in cat) and (cat!="allL_allP_allC"): continue
            #if cat!="allL_allP_allC": continue
            #if not(r=='SB' and l=='e'): continue

            cut='*'.join([cuts['common'],cuts[r],cuts[l],cuts[p],cuts[c]])

            for i,pl in enumerate(plots):

                if not(i in [0,1,2,4,6,7,8,9,11,12,16,20]): continue ## uncomment this one for the plots of analysis note
                #if i!=0: continue
                #if i!=11: continue
                #if i!=26: continue
                #if not(i in [0,11]): continue
                #if not(i in [2,3,5]): continue
                #if not(i in [1,4,8]): continue
                #if not(i in [23,24,25]): continue


                myLumi = lumiValue

                if RENORMFROMLOWMASSSB and (r in ['SBL','SB','SR']):
                    myLumi = lumiValue+'*'+str(renormFactorLMSB)
                    print "Renormalizing the expected yield in the signal region with the data/bkgd ratio of the low-mjet sideband: ", renormFactorLMSB


                #'''
                res = lnujjStack.drawStackWithRatio(pl[1],cut,myLumi,pl[2],pl[3],pl[4],pl[5],pl[6])
                cmsLabel(res['canvas'])
                saveCanvas(res['canvas'],outDir+'/'+r+'_'+prs+'_'+cat+'_'+YEAR+'_'+pl[0])
                #'''
                '''
                res = lnujjStack.drawStack(pl[1],cut,myLumi,pl[2],pl[3],pl[4],pl[5],pl[6])
                cmsLabel(res['canvas'])
                res['legend'].Clear()
                saveCanvas(res['canvas'],outDir+'/'+r+'_'+prs+'_'+cat+'_'+YEAR+'_'+pl[0])
                #'''


                '''
                if (r in ['CR']):
                    renormFactorCR = res['ratio']
                    print "Data/bkgd ratio in the top enriched control region: ", renormFactorCR
                #'''
