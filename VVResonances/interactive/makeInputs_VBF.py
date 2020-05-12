import ROOT
import os, sys
from DoubleBscalefactors import *
from DoubleBefficiencies import *

#import optparse
#parser = optparse.OptionParser()
#parser.add_option("-y","--year",dest="year",type=int,default=2016,help="2016 or 2017 or 2018")
#(options,args) = parser.parse_args()
#
#if options.year not in [2016,2017,2018]:
#    parser.error("year must be 2016, 2017, or 2018")
#YEAR=options.year



DONORMMC       = 1
DONORMDATA     = 1
DONORMMCASDATA = 1
DOSIGNALSHAPES = 1
DOSIGNALYIELDS = 1
DOSIGNALCTPL   = 1
DORESONANT     = 1
DONONRESONANT  = 1

DONORMMCCR     = 0
DONORMDATACR   = 0
DORESONANTCR   = 0
DONONRESONANTCR= 0

DOXWW = 1
DOXWZ = 1
DOXWH = 1
DOVBFXWW = 1




###############################################
###############################################
#################  PARAMETERS  ################
###############################################
###############################################


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
    'vbf' : '1',
    'allC': '1',
    }
bbWgtWZ={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2016[ptcut])+')/(1-'+str(bbEffWZ_2016[ptcut])+'))') for ptcut,sf in bbSFWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2017[ptcut])+')/(1-'+str(bbEffWZ_2017[ptcut])+'))') for ptcut,sf in bbSFWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2018[ptcut])+')/(1-'+str(bbEffWZ_2018[ptcut])+'))') for ptcut,sf in bbSFWZ_2018))+'))',
    'vbf' : '1',
    'allC': '1',
    }
bbWgtWH={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2016[ptcut])+')/(1-'+str(bbEffWH_2016[ptcut])+'))') for ptcut,sf in bbSFWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2017[ptcut])+')/(1-'+str(bbEffWH_2017[ptcut])+'))') for ptcut,sf in bbSFWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2018[ptcut])+')/(1-'+str(bbEffWH_2018[ptcut])+'))') for ptcut,sf in bbSFWH_2018))+'))',
    'vbf' : '1', 
    'allC': '1',
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
#cuts['common'] = cuts['common'] + '*(Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&(Flag_eeBadScFilter*(run>500)+(run<500))&&Flag_BadPFMuonFilter)' ## 2 new flags are missing in some ntuples

## excluding the problematic HEM15/16 region:
cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&abs(lnujj_l1_l_pdgId)==11&&(-1.55<lnujj_l1_l_phi)&&(lnujj_l1_l_phi<-0.9)&&(-2.5<lnujj_l1_l_eta)&&(lnujj_l1_l_eta<-1.479)))'
## new cut on pT/M:
cuts['common'] = cuts['common'] + '*(lnujj_l1_pt/lnujj_LV_mass>0.4&&lnujj_l2_pt/lnujj_LV_mass>0.4)'
## lumi-based reweighting for MC:
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
thrHP='0.50'
thrLP='0.80'
cuts['HP'] = '('+Vtagger+'<'+thrHP+')'
cuts['LP'] = '('+thrHP+'<='+Vtagger+'&&'+Vtagger+'<'+thrLP+')'
cuts['allP'] = '('+cuts['HP']+'||'+cuts['LP']+')'
purities=['HP','LP']
puritiesMerged=['allP']

bbtag='(lnujj_l2_btagBOOSTED>0.8)'
cuts['bb'] = bbtag+'*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'
cuts['nobb'] = '(!'+bbtag+')'+'*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'
cuts['allC'] = '1'
cuts['vbf'] = '(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500)'
categories=['bb','nobb','vbf']
categoriesMerged=['allC']


#cuts['resW']  ='(lnujj_l2_mergedVTruth==1&&!(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'
#cuts['resTop']='(lnujj_l2_mergedVTruth==1&&(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'
cuts['res']   ='(lnujj_l2_mergedVTruth==1)'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'



## get W+jets yield from low-mjet sideband:
renormWJets2016='0.8727054353'
renormWJets2017='0.699592444047'
renormWJets2018='0.728005348312'
renormWJets3Yrs=",".join([renormWJets2016,renormWJets2017,renormWJets2018])
renormWJetsRun2='0.760376974966'

## get resonant yield from CR:
renormRes = {
'mu': {
        'HP':{'nobb':0.96,'bb':0.96,'vbf':0.96},
        'LP':{'nobb':0.88,'bb':0.79,'vbf':0.88},
      },
'e': {
        'HP':{'nobb':0.96,'bb':0.96,'vbf':0.96},
        'LP':{'nobb':0.88,'bb':0.81,'vbf':0.88},
      },
}

## get non-resonant MVV slope from CR (also hardcoded in vvMake2DTemplateWithKernels.py):
renormNonResMvvSlope = {
    'HP':{'nobb':-2.1e-4, 'bb':-2.65e-4,'vbf':0.},
    'LP':{'nobb':-2.57e-4,'bb':-2.61e-4,'vbf':0.},
}




WWTemplate="ntuples2016/BulkGravToWWToWlepWhad_narrow,ntuples2017/BulkGravToWWToWlepWhad_narrow,ntuples2018/BulkGravToWWToWlepWhad_narrow"
BRWW=2.*0.327*0.6760

WZTemplate="ntuples2016/WprimeToWZToWlepZhad_narrow,ntuples2017/WprimeToWZToWlepZhad_narrow,ntuples2018/WprimeToWZToWlepZhad_narrow"
BRWZ=0.327*0.6991

WHTemplate="ntuples2016/WprimeToWHToWlepHinc_narrow,ntuples2017/WprimeToWHToWlepHinc_narrow,ntuples2018/WprimeToWHToWlepHinc_narrow"
BRWH=0.327

VBFWWTemplate='ntuples2016/VBF_RadionToWW_narrow,ntuples2017/VBF_RadionToWW_narrow,ntuples2018/VBF_RadionToWW_narrow'
BRVBFWW=1.0

resTemplate = "ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WWToLNuQQ,ntuples2017/WWToLNuQQ,ntuples2018/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2017/WZTo1L1Nu2Q,ntuples2018/WZTo1L1Nu2Q,ntuples2016/ZZTo2L2Q,ntuples2017/ZZTo2L2Q,ntuples2018/ZZTo2L2Q,ntuples2016/T_tW,ntuples2017/T_tW,ntuples2018/T_tW,ntuples2016/TBar_tW,ntuples2017/TBar_tW,ntuples2018/TBar_tW"
#resWTemplate = resTemplate
#resTopTemplate = resTemplate
nonResTemplate = "ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WJetsToLNu_HT,ntuples2017/WJetsToLNu_HT,ntuples2018/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT,ntuples2017/DYJetsToLL_M50_HT,ntuples2018/DYJetsToLL_M50_HT,ntuples2016/T_tW,ntuples2017/T_tW,ntuples2018/T_tW,ntuples2016/TBar_tW,ntuples2017/TBar_tW,ntuples2018/TBar_tW"
allMCTemplate = "ntuples2016/TT_pow,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WWToLNuQQ,ntuples2017/WWToLNuQQ,ntuples2018/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2017/WZTo1L1Nu2Q,ntuples2018/WZTo1L1Nu2Q,ntuples2016/ZZTo2L2Q,ntuples2017/ZZTo2L2Q,ntuples2018/ZZTo2L2Q,ntuples2016/T_tW,ntuples2017/T_tW,ntuples2018/T_tW,ntuples2016/TBar_tW,ntuples2017/TBar_tW,ntuples2018/TBar_tW,ntuples2016/WJetsToLNu_HT,ntuples2017/WJetsToLNu_HT,ntuples2018/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT,ntuples2017/DYJetsToLL_M50_HT,ntuples2018/DYJetsToLL_M50_HT"

data2016Template = "ntuples2016/SingleElectron,ntuples2016/SingleMuon,ntuples2016/MET"
data2017Template = "ntuples2017/SingleElectron,ntuples2017/SingleMuon,ntuples2017/MET"
data2018Template = "ntuples2018/EGamma,ntuples2018/SingleMuon,ntuples2018/MET"
dataTemplate = data2016Template + "," + data2017Template + "," + data2018Template




minMJJ=20.0
maxMJJ=210.0

minMVV=600.0
maxMVV=5000.0

binsMJJ={}
binsMJJ['bb']=19
binsMJJ['nobb']=38
binsMJJ['vbf']=19
binsMJJ['allC']=38 #95
binsMVV={}
binsMVV['bb']=176
binsMVV['nobb']=176
binsMVV['vbf']=176
binsMVV['allC']=176


fspline={}
fspline['bb']=2
fspline['nobb']=2
fspline['vbf']=2
fspline['allC']=2 #10

limitTailFit2D={}
limitTailFit2D['bb']=1200
limitTailFit2D['nobb']=1600
limitTailFit2D['vbf']=1200
limitTailFit2D['allC']=1600


minMXSigShapeParam = 799
maxMXSigShapeParam = 5001
minMXSigYieldParam = 999
maxMXSigYieldParam = 4501


cuts['acceptance']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV}&&lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
cuts['acceptanceMVV']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceMJJ']= "(lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ)

cuts['acceptanceGEN']= "(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMJJ=10,maxMJJ=300,minMVV=500,maxMVV=10000)
cuts['acceptanceGENMVV']= "(lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMVV=500,maxMVV=5000)
cuts['acceptanceGENMJJ']= "(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMJJ=minMJJ-5,maxMJJ=maxMJJ+5,minMVV=minMVV,maxMVV=maxMVV)






###############################################
###############################################
###################  SIGNAL  ##################
###############################################
###############################################


def makeSignalShapesMJJ(filename,template,forceHP="",forceLP=""):
    for l in leptonsMerged:
        for p in purities:
            for c in categories:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c]])

                rootFile=outDir+filename+"_MJJ_"+p+"_"+c+".root"
                debugFile=outDir+"debugJJ_"+filename+"_MJJ_"+p+"_"+c
                doExp = not(p=='HP' or p=='NP')
                force = forceHP if p=='HP' else forceLP
                cmd='vvMakeSignalMJJShapes.py -s "{template}" -m {minMX} -M {maxMX} -c "{cut}" -o "{rootFile}" -d "{debugFile}" -V "lnujj_l2_softDrop_mass" -x {minMJJ} -X {maxMJJ} -e {doExp} {force} {ntuples}'.format(template=template,minMX=minMXSigShapeParam,maxMX=maxMXSigShapeParam,cut=cut,rootFile=rootFile,debugFile=debugFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=int(doExp),force=("-f "+force) if force!="" else "",ntuples=ntuples)
                os.system(cmd)

                jsonFile=outDir+filename+"_MJJ_"+p+"_"+c+".json"
                debugFile=outDir+"debugSignalShape_"+filename+"_MJJ_"+p+"_"+c+".root"
                print 'Making JSON ', jsonFile
                if p=='HP' or p=='NP':
                    cmd='vvMakeJSON.py -o "{jsonFile}" -d "{debugFile}" -g "mean:pol5,sigma:pol4,alpha:pol0,n:pol0,alpha2:pol0,n2:pol0,slope:pol0,f:pol0" -m {minMX} -M {maxMX} {rootFile}'.format(jsonFile=jsonFile,debugFile=debugFile,minMX=minMXSigShapeParam,maxMX=maxMXSigShapeParam,rootFile=rootFile)
                else:
                    cmd='vvMakeJSON.py -o "{jsonFile}" -d "{debugFile}" -g "mean:pol5,sigma:pol4,alpha:pol0,n:pol0,alpha2:pol0,n2:pol0,slope:pol4,f:pol4" -m {minMX} -M {maxMX} {rootFile}'.format(jsonFile=jsonFile,debugFile=debugFile,minMX=minMXSigShapeParam,maxMX=maxMXSigShapeParam,rootFile=rootFile)
                os.system(cmd)


def makeSignalShapesMVV(filename,template):
    for l in leptonsMerged:
        for p in purities:
            for c in categories:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],cuts['acceptanceMJJ']])

                rootFile=outDir+filename+"_MVV_"+p+"_"+c+".root"
                debugFile=outDir+"debugVV_"+filename+"_MVV_"+p+"_"+c
                cmd='vvMakeSignalMVVShapes.py -s "{template}" -m {minMX} -M {maxMX} -c "{cut}" -o "{rootFile}" -d "{debugFile}" -v "lnujj_LV_mass" -b {binsMVV} -x {minMVV} -X {maxMVV} {ntuples}'.format(template=template,minMX=minMXSigShapeParam,maxMX=maxMXSigShapeParam,cut=cut,rootFile=rootFile,debugFile=debugFile,binsMVV=1000,minMVV=0,maxMVV=10000,ntuples=ntuples)
                os.system(cmd)

                jsonFile=outDir+filename+"_MVV_"+p+"_"+c+".json"
                debugFile=outDir+"debugSignalShape_"+filename+"_MVV_"+p+"_"+c+".root"
                print 'Making JSON ', jsonFile
                cmd='vvMakeJSON.py -o "{jsonFile}" -d "{debugFile}" -g "MEAN:pol1,SIGMA:pol1,ALPHA1:pol4,N1:pol0,ALPHA2:pol3,N2:pol0" -m {minMX} -M {maxMX} {rootFile}'.format(jsonFile=jsonFile,debugFile=debugFile,minMX=minMXSigShapeParam,maxMX=maxMXSigShapeParam,rootFile=rootFile)
                os.system(cmd)


def makeSignalYields(filename,template,branchingFraction,sfP={'HP':'1','LP':'1'},sfC={'bb':'1','nobb':'1','vbf':'1','allC':'1'}):
    for l in leptons:
        for p in purities:
            for c in categories:
                cut = "*".join([cuts['common'],cuts[l],cuts[p],cuts[c],cuts['acceptance'],sfP[p],sfC[c]])

                yieldFile=outDir+filename+"_"+l+"_"+p+"_"+c+"_yield"
                debugFile=outDir+"debugSignalYield_"+filename+"_"+l+"_"+p+"_"+c
                cmd='vvMakeSignalYields.py -s {template} -m {minMX} -M {maxMX} -c "{cut}" -o {output} -d "{debugFile}" -V "lnujj_LV_mass" -x {minMVV} -X {maxMVV} -f "pol4" -b {BR} {ntuples}'.format(template=template,minMX=minMXSigYieldParam,maxMX=maxMXSigYieldParam,cut=cut,output=yieldFile,debugFile=debugFile,minMVV=0.,maxMVV=10000.,BR=branchingFraction,ntuples=ntuples)
                os.system(cmd)






###############################################
###############################################
##########  NON-RESONANT BACKGROUND  ##########
###############################################
###############################################


def makeBackgroundShapesMVVConditional(name,filename,template,addCut="1"):
    inCR = ("CR" in name)

    cut='*'.join([cuts['CR' if inCR else 'common'],cuts['allL'],cuts['allP'],cuts['allC'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=outDir+filename+"_"+name+"_detectorResponse.root"
    cmd='vvMake2DDetectorParam.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt" -b "100,150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000" {rwwj} {ntuples}'.format(rootFile=resFile,samples=template,cut=cut,rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
    os.system(cmd)

    for p in purities:
        for c in categories:
            cut='*'.join([cuts['CR' if inCR else 'common'],cuts['allL'],cuts[p],addCut,cuts['acceptanceMJJ'],cuts['acceptanceGENMVV']])

            rootFile=outDir+filename+"_"+name+"_"+p+"_"+c+"_COND2D.root"
            cmd='vvMake2DTemplateWithKernels.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_gen_partialMass,lnujj_l2_softDrop_mass" -u "(1+0.0004*lnujj_l2_gen_pt),(1+0.000001*lnujj_l2_gen_pt*lnujj_l2_gen_pt)" -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ} -r {res} -l {limitTailFit2D} {rwwj} -t 2 {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV['allC'],minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,limitTailFit2D=limitTailFit2D['allC'],rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
            os.system(cmd)

            ## store gen distributions, just for control plots:
            rootFile=outDir+filename+"_GEN.root"
            cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}" -o "{rootFile}" -v "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}" {rwwj} {ntuples}'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV['allC'],bins=binsMJJ[c],MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=1,name=name+"_"+p+"_"+c,data=0,rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
            os.system(cmd)


def makeBackgroundShapesMJJSpline(name,filename,template,addCut="1"):
    inCR = ("CR" in name)

    for l in leptons:
        for p in purities:
            for c in categories:
                cut='*'.join([cuts['CR' if inCR else 'common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceMVV'],'(1+0.17*exp(-0.5*(TMath::Log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)+0.44)^2))'])
                rootFile=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                cmd='vvMake1DTemplateSpline.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_l2_softDrop_mass" -V "lnujj_l2_softDrop_mass_high,lnujj_l2_softDrop_mass_low" -u "(exp(-0.5*(TMath::Log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)+0.44)^2)),(0.05*lnujj_l2_softDrop_mass)" -b {binsMJJ} -x {minMJJ} -X {maxMJJ} -f {fspline} {rwwj} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,fspline=fspline[c],rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
                os.system(cmd)


def mergeBackgroundShapes(name,filename):
    for l in leptons:
        for p in purities:
            for c in categories:
                inputy=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                inputx=outDir+filename+"_"+name+"_"+p+"_"+c+"_COND2D.root"
                rootFile=outDir+filename+"_"+name+"_2D_"+l+"_"+p+"_"+c+".root"
                cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -s "MVVScale:MVVScale,Diag:Diag" -S "logWeight:logWeight,MJJScale:MJJScale,SD:SD,PT:PTY,OPT:OPTY" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
                os.system(cmd)






###############################################
###############################################
############  RESONANT BACKGROUND  ############
###############################################
###############################################


def makeResBackgroundShapesMVVConditional(name,filename,template,addCut="1"):
    inCR = ("CR" in name)

    cut='*'.join([cuts['CR' if inCR else 'common'],cuts['allL'],cuts['allP'],cuts['allC'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=outDir+filename+"_"+name+"_detectorResponse.root"
    cmd='vvMake2DDetectorParam.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt" -b "100,150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000" {rwwj} {ntuples}'.format(rootFile=resFile,samples=template,cut=cut,rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
    os.system(cmd)

    for c in categories:
        cut='*'.join([cuts['CR' if inCR else 'common'],cuts['allL'],cuts['allP'],addCut,cuts['acceptanceMJJ'],cuts['acceptanceGENMVV']])

        rootFile=outDir+filename+"_"+name+"_"+c+"_COND2D.root"
        cmd='vvMake2DTemplateWithKernels.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_gen_partialMass,lnujj_l2_softDrop_mass" -u "(1+0.0004*lnujj_l2_gen_pt),(1+0.000001*lnujj_l2_gen_pt*lnujj_l2_gen_pt)" -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ} -r {res} -l {limitTailFit2D} {rwwj} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV['allC'],minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,limitTailFit2D=limitTailFit2D['allC'],rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
        os.system(cmd)

        ## store gen distributions, just for control plots:
        rootFile=outDir+filename+"_GEN.root"
        cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}" -o "{rootFile}" -v "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}" {rwwj} {ntuples}'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV['allC'],bins=binsMJJ[c],MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=1,name=name+"_"+c,data=0,rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
        os.system(cmd)


def makeBackgroundShapesMJJFits(name,filename,template,addCut="1"):
    inCR = ("CR" in name)

    for l in leptons:
        for p in purities:
            for c in categories:
                expo=0
                if p=='LP':
                    expo=1
                cut='*'.join([cuts['CR' if inCR else 'common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceGENMJJ'],cuts['acceptanceMVV']])
                rootFile=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                cmd='vvMakeTopMJJMergedShapes.py -s "{template}" -c "{cut}" -o "{rootFile}"  -v "lnujj_l2_softDrop_mass"  -b {binsMJJ} -x {minMJJ} -X {maxMJJ} -e {expo}  {ntuples}'.format(template=template,cut=cut,rootFile=rootFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,expo=expo,ntuples=ntuples)
                os.system(cmd)


def mergeBackgroundShapesRes(name,filename):
    for l in leptons:
        for p in purities:
            for c in categories:
                inputy=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                inputx=outDir+filename+"_"+name+"_"+c+"_COND2D.root"
                rootFile=outDir+filename+"_"+name+"_2D_"+l+"_"+p+"_"+c+".root"
                cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -s "MVVScale:MVVScale,Diag:Diag" -S "scale:scaleY,res:resY,f:fractionY" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
                os.system(cmd)






###############################################
###############################################
##############  NORMALIZATIONS  ###############
###############################################
###############################################


def makeNormalizations(name,filename,template,data=0,addCut='1',factor=1):
    inCR = ("CR" in name)

    for l in leptons:
        for p in purities:
            for c in categories:

                if name=='res':
                    f=factor*renormRes[l][p][c]
                else:
                    f=factor

                cut="*".join([cuts['CR' if inCR else 'common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptance']])

                ## alternative cut strings, for the control plots of templates:
                if name=='nonRes_wgtMVV_inclLC':
                    cut="*".join([cuts['CR' if inCR else 'common'],cuts['allL'],cuts[p],cuts['allC'],addCut,cuts['acceptanceMJJ'],cuts['acceptanceGENMVV'],'(1.0+'+str(renormNonResMvvSlope[p][c])+'*lnujj_gen_partialMass)'])
                elif name=='nonRes_CR_inclLC':
                    cut="*".join([cuts['CR' if inCR else 'common'],cuts['allL'],cuts[p],cuts['allC'],addCut,cuts['acceptanceMJJ'],cuts['acceptanceGENMVV']])
                elif name=='nonRes_wgtMJJ'or name=='nonRes_CR_wgtMJJ':
                    cut="*".join([cuts['CR' if inCR else 'common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceMVV'],'(1+0.17*exp(-0.5*(TMath::Log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)+0.44)^2))'])
                elif name=='res_inclLPC' or name=='res_CR_inclLPC':
                    cut="*".join([cuts['CR' if inCR else 'common'],cuts['allL'],cuts['allP'],cuts['allC'],addCut,cuts['acceptanceMJJ'],cuts['acceptanceGENMVV']])

                rootFile=outDir+filename+"_"+l+"_"+p+"_"+c+".root"
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}" -o "{rootFile}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}" {rwwj} {ntuples}'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV[c],bins=binsMJJ[c],MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=f,name=name,data=data,rwwj=('' if inCR else '-W '+renormWJets3Yrs),ntuples=ntuples)
                os.system(cmd)






###############################################
###############################################
####################  RUN  ####################
###############################################
###############################################



## Normalizations
if DONORMMC:
    makeNormalizations("nonRes","LNuJJ_norm",nonResTemplate,0,cuts['nonres'])
    makeNormalizations("res","LNuJJ_norm",resTemplate,0,cuts['res'])
    ## The next 3 are just for control plots:
    makeNormalizations("nonRes_wgtMVV_inclLC","LNuJJ_norm",nonResTemplate,0,cuts['nonres'])
    makeNormalizations("nonRes_wgtMJJ","LNuJJ_norm",nonResTemplate,0,cuts['nonres'])
    makeNormalizations("res_inclLPC","LNuJJ_norm",resTemplate,0,cuts['res'])
if DONORMDATA:
    makeNormalizations("data","LNuJJ_norm",dataTemplate,1)
    makeNormalizations("data_2016","LNuJJ_norm",data2016Template,1)
    makeNormalizations("data_2017","LNuJJ_norm",data2017Template,1)
    makeNormalizations("data_2018","LNuJJ_norm",data2018Template,1)
if DONORMMCASDATA:
    makeNormalizations("MCasData","LNuJJ_norm",allMCTemplate,0)

if DONORMMCCR:
    makeNormalizations("nonRes_CR","LNuJJ_norm_CR",nonResTemplate,0,cuts['nonres'])
    makeNormalizations("res_CR","LNuJJ_norm_CR",resTemplate,0,cuts['res'])
    ## The next 3 are just for control plots:
    makeNormalizations("nonRes_CR_inclLC","LNuJJ_norm_CR",nonResTemplate,0,cuts['nonres'])
    makeNormalizations("nonRes_CR_wgtMJJ","LNuJJ_norm_CR",nonResTemplate,0,cuts['nonres'])
    makeNormalizations("res_CR_inclLPC","LNuJJ_norm_CR",resTemplate,0,cuts['res'])
if DONORMDATACR:
    makeNormalizations("data_CR","LNuJJ_norm_CR",dataTemplate,1)
    makeNormalizations("data_CR_2016","LNuJJ_norm_CR",data2016Template,1)
    makeNormalizations("data_CR_2017","LNuJJ_norm_CR",data2017Template,1)
    makeNormalizations("data_CR_2018","LNuJJ_norm_CR",data2018Template,1)


## Signal templates
if DOSIGNALSHAPES:
    if DOXWW: makeSignalShapesMJJ("LNuJJ_XWW",WWTemplate)
    if DOXWZ: makeSignalShapesMJJ("LNuJJ_XWZ",WZTemplate)
    if DOXWH: makeSignalShapesMJJ("LNuJJ_XWH",WHTemplate)
    if DOVBFXWW: makeSignalShapesMJJ("LNuJJ_VBFXWW",VBFWWTemplate)

    if DOXWW: makeSignalShapesMVV("LNuJJ_XWW",WWTemplate)
    if DOXWZ: makeSignalShapesMVV("LNuJJ_XWZ",WZTemplate)
    if DOXWH: makeSignalShapesMVV("LNuJJ_XWH",WHTemplate)
    if DOVBFXWW: makeSignalShapesMVV("LNuJJ_VBFXWW",VBFWWTemplate)

if DOSIGNALYIELDS:
    if DOXWW: makeSignalYields("LNuJJ_XWW",WWTemplate,BRWW,tau21SF,bbWgtWW)
    if DOXWZ: makeSignalYields("LNuJJ_XWZ",WZTemplate,BRWZ,tau21SF,bbWgtWZ)
    if DOXWH: makeSignalYields("LNuJJ_XWH",WHTemplate,BRWH,tau21SF,bbWgtWH)
    if DOVBFXWW: makeSignalYields("LNuJJ_VBFXWW",VBFWWTemplate,BRVBFWW,tau21SF,bbWgtWW)

if DOSIGNALCTPL:
    #for mx in [600,800,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]:
    for mx in [1000,2000,3000,4000]:
        if DOXWW: makeNormalizations("XWW"+str(mx).zfill(4),"LNuJJ_norm",WWTemplate+"_"+str(mx),0,'1',BRWW)
        #if mx!=4000:
        if DOXWZ: makeNormalizations("XWZ"+str(mx).zfill(4),"LNuJJ_norm",WZTemplate+"_"+str(mx),0,'1',BRWZ)
        #if mx!=1200:
        if DOXWH: makeNormalizations("XWH"+str(mx).zfill(4),"LNuJJ_norm",WHTemplate+"_"+str(mx),0,'1',BRWH)

    if DOXWW: makeNormalizations("XWWall","LNuJJ_norm",WWTemplate,0,'1',BRWW)
    if DOXWZ: makeNormalizations("XWZall","LNuJJ_norm",WZTemplate,0,'1',BRWZ)
    if DOXWH: makeNormalizations("XWHall","LNuJJ_norm",WHTemplate,0,'1',BRWH)


## Resonant background templates (W+V/t)
if DORESONANT:
    makeResBackgroundShapesMVVConditional("res","LNuJJ",resTemplate,cuts['res'])
    makeBackgroundShapesMJJFits("res","LNuJJ",resTemplate,cuts['res'])
    mergeBackgroundShapesRes("res","LNuJJ")

if DORESONANTCR:
    makeResBackgroundShapesMVVConditional("res_CR","LNuJJ",resTemplate,cuts['res'])
    makeBackgroundShapesMJJFits("res_CR","LNuJJ",resTemplate,cuts['res'])
    mergeBackgroundShapesRes("res_CR","LNuJJ")


## Non-resonant background templates (W+jets)
if DONONRESONANT:
    makeBackgroundShapesMJJSpline("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])
    makeBackgroundShapesMVVConditional("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])
    mergeBackgroundShapes("nonRes","LNuJJ")

if DONONRESONANTCR:
    makeBackgroundShapesMJJSpline("nonRes_CR","LNuJJ",nonResTemplate,cuts['nonres'])
    makeBackgroundShapesMVVConditional("nonRes_CR","LNuJJ",nonResTemplate,cuts['nonres'])
    mergeBackgroundShapes("nonRes_CR","LNuJJ")
