import ROOT
import os, sys
from DoubleBscalefactors import *
from DoubleBefficiencies import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",type=int,default=2016,help="2016 or 2017 or 2018")
(options,args) = parser.parse_args()

if options.year not in [2016,2017,2018]:
    parser.error("year must be 2016, 2017, or 2018")
YEAR=options.year



DONORMMC       = 1
DONORMDATA     = 1
DOSIGNALSHAPES = 1
DOSIGNALYIELDS = 1
DOSIGNALCTPL   = 1
DORESONANT     = 1
DONONRESONANT  = 1

DOXWW = 1
DOXWZ = 1
DOXWH = 1

RENORMNONRES   = 1
REMOVE2018ELEHEM1516 = (options.year==2018 and 1)

MERGELEPNONRES = 0
MERGEPURNONRES = 0
MERGECATNONRES = 0



###############################################
###############################################
#################  PARAMETERS  ################
###############################################
###############################################


outDir='Inputs_'+str(YEAR)+'/'
os.system('mkdir -p '+outDir)

ntuples='ntuples'+str(YEAR)

ttbar=''
electronPD=''
tau21SF={'HP':1.,'LP':1.}
if YEAR==2016: 
    ttbar='TT_pow'
    electronPD='SingleElectron'
    renormNonRes=0.942220835364
    tau21SF['HP'] = 1.03 ##TBU with new WP
    tau21SF['LP'] = 0.95
    bbSFWW=DoubleBsf_M2_B_80X
    bbSFWZ=DoubleBsf_M2_B_80X
    bbSFWH=DoubleBsf_M2_S_80X
    bbEffWW=EffMC_M2_XWW_2016
    bbEffWZ=EffMC_M2_XWZ_2016
    bbEffWH=EffMC_M2_XWH_2016
elif YEAR==2017:
    ttbar='TTHad_pow,TTLep_pow,TTSemi_pow'
    electronPD='SingleElectron'
    renormNonRes=0.799382735674
    tau21SF['HP'] = 0.97
    tau21SF['LP'] = 1.14
    bbSFWW=DoubleBsf_M2_B_94X
    bbSFWZ=DoubleBsf_M2_B_94X
    bbSFWH=DoubleBsf_M2_S_94X
    bbEffWW=EffMC_M2_XWW_2017
    bbEffWZ=EffMC_M2_XWZ_2017
    bbEffWH=EffMC_M2_XWH_2017
elif YEAR==2018:
    ttbar='TTHad_pow,TTLep_pow,TTSemi_pow'
    electronPD='EGamma'
    renormNonRes=0.904081371649
    tau21SF['HP'] = 0.97 ##TBU (copied from 2017 for now)
    tau21SF['LP'] = 1.14
    bbSFWW=DoubleBsf_M2_B_102X
    bbSFWZ=DoubleBsf_M2_B_102X
    bbSFWH=DoubleBsf_M2_S_102X
    bbEffWW=EffMC_M2_XWW_2018
    bbEffWZ=EffMC_M2_XWZ_2018
    bbEffWH=EffMC_M2_XWH_2018

bbWgtWW={'bb':('('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWW))+')'), 'nobb':('('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW[ptcut])+')/(1-'+str(bbEffWW[ptcut])+'))') for ptcut,sf in bbSFWW))+')')}
bbWgtWZ={'bb':('('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ))+')'), 'nobb':('('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ[ptcut])+')/(1-'+str(bbEffWZ[ptcut])+'))') for ptcut,sf in bbSFWZ))+')')}
bbWgtWH={'bb':('('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH))+')'), 'nobb':('('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH[ptcut])+')/(1-'+str(bbEffWH[ptcut])+'))') for ptcut,sf in bbSFWH))+')')}
#print bbWgtWW['bb']
#print bbWgtWW['nobb']


cuts={}

cuts['common'] = '1'
cuts['common'] = cuts['common'] + '*(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*((run>500) + (run<500)*lnujj_sfWV)' ## changed from lnujj_sf to lnujj_sfWV for 2016 
cuts['common'] = cuts['common'] + '*(lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0)'
## Not just for 2016 now:
cuts['common'] = cuts['common'] + '*(Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&(Flag_eeBadScFilter*(run>500)+(run<500))&&Flag_badMuonFilter)'
if REMOVE2018ELEHEM1516:
    cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&abs(lnujj_l1_l_pdgId)==11&&(-1.55<lnujj_l1_l_phi)&&(lnujj_l1_l_phi<-0.9)&&(-2.5<lnujj_l1_l_eta)&&(lnujj_l1_l_eta<-1.479)))'
## new cut on pT/M:
cuts['common'] = cuts['common'] + '*(lnujj_l1_pt/lnujj_LV_mass>0.4&&lnujj_l2_pt/lnujj_LV_mass>0.4)'
## ensure orthogonality with VBF analysis:
cuts['common'] = cuts['common'] + '*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'


cuts['nob'] = '(lnujj_nMediumBTags==0)' #*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)' #*lnujj_btagWeight'
## b-tag veto is now the default; put the btag weight only here:
cuts['common'] = cuts['common'] + '*' + cuts['nob'] + '*lnujj_btagWeight'

cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['allL'] = '(abs(lnujj_l1_l_pdgId)==11||abs(lnujj_l1_l_pdgId)==13)'
leptons=['e','mu']
leptonsMerged=['allL']

Vtagger='(lnujj_l2_tau2/lnujj_l2_tau1)'
thrHP='0.35'
thrLP='0.75'
cuts['HP'] = '('+Vtagger+'<'+thrHP+')'
cuts['LP'] = '('+thrHP+'<='+Vtagger+'&&'+Vtagger+'<'+thrLP+')'
cuts['allP'] = '('+cuts['HP']+'||'+cuts['LP']+')'
purities=['HP','LP']
puritiesMerged=['allP']

bbtag='(lnujj_l2_btagBOOSTED>0.8)'
cuts['bb'] = bbtag
cuts['nobb'] = '(!'+bbtag+')'
cuts['allC'] = '1'
categories=['bb','nobb']
categoriesMerged=['allC']


cuts['resW']  ='(lnujj_l2_mergedVTruth==1&&lnujj_l2_gen_softDrop_mass<100)'
cuts['resTop']='(lnujj_l2_mergedVTruth==1&&lnujj_l2_gen_softDrop_mass>100)'

cuts['nonres']='(lnujj_l2_mergedVTruth==0)'




WWTemplate="BulkGravToWWToWlepWhad_narrow"
BRWW=2.*0.327*0.6760

WZTemplate="WprimeToWZToWlepZhad_narrow"
BRWZ=0.327*0.6991

WHTemplate="WprimeToWHToWlepHinc_narrow"
BRWH=0.327

#resWTemplate = ttbar+",WWToLNuQQ,WZTo1L1Nu2Q,T_tW,TBar_tW"
resWTemplate = ttbar+',WWToLNuQQ' #+",WZTo1L1Nu2Q,T_tW,TBar_tW"
resTopTemplate = resWTemplate
nonResTemplate = ttbar+",WJetsToLNu_HT,DYJetsToLL_M50_HT"
dataTemplate = electronPD+",SingleMuon,MET"



minMJJ=30.0
maxMJJ=210.0

minMVV=800.0
maxMVV=5000.0

binsMJJ={}
binsMJJ['bb']=18
binsMJJ['nobb']=45
binsMJJ['allC']=90
binsMVV={}
binsMVV['bb']=42
binsMVV['nobb']=168
binsMVV['allC']=168


fspline={}
fspline['bb']=2
fspline['nobb']=5
fspline['allC']=10

limitTailFit2D={}
limitTailFit2D['bb']=1200
limitTailFit2D['nobb']=1600
limitTailFit2D['allC']=1600


minMXSigShapeParam = 799
maxMXSigShapeParam = 8001
minMXSigYieldParam = 999
maxMXSigYieldParam = 4501


cuts['acceptance']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV}&&lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
cuts['acceptanceGEN']= "(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMJJ=25,maxMJJ=300,minMVV=700,maxMVV=10000)                
#cuts['acceptanceGEN']= "(lnujj_l2_gen_softDrop_mass>0&&lnujj_gen_partialMass>0)"

cuts['acceptanceGENMVV']= "(lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMVV=700,maxMVV=5000)
cuts['acceptanceGENMJJ']= "(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMJJ=minMJJ-5,maxMJJ=maxMJJ+5,minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceMVV']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceMJJ']= "(lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ)                



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


def makeSignalYields(filename,template,branchingFraction,sfP={'HP':1.0,'LP':1.0},sfC={'bb':'1','nobb':'1'}):
    for l in leptons:
        for p in purities:
            for c in categories:
                cut = "*".join([cuts['common'],cuts[l],cuts[p],cuts[c],cuts['acceptance'],str(sfP[p]),sfC[c]])

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
    cut='*'.join([cuts['common'],cuts['allL'],cuts['allP'],cuts['allC'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=outDir+filename+"_"+name+"_detectorResponse.root"            
    cmd='vvMake2DDetectorParam.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt" -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000" {ntuples}'.format(rootFile=resFile,samples=template,cut=cut,ntuples=ntuples)
    os.system(cmd)

    for l in (leptons,leptonsMerged)[MERGELEPNONRES]:
        for p in (purities,puritiesMerged)[MERGEPURNONRES]:
            for c in (categories,categoriesMerged)[MERGECATNONRES]:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceGEN']])

                rootFile=outDir+filename+"_"+name+"_COND2D_"+l+"_"+p+"_"+c+".root"
                cmd='vvMake2DTemplateWithKernels.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass" -u "(1+0.0004*lnujj_l2_gen_pt),(1+0.000001*lnujj_l2_gen_pt*lnujj_l2_gen_pt)" -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ} -r {res} -l {limitTailFit2D} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,limitTailFit2D=limitTailFit2D[c],ntuples=ntuples)
                os.system(cmd)

                ## store gen distributions, just for control plots
                rootFile=outDir+filename+"_"+l+"_"+p+"_"+c+"_GEN.root"
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}" -o "{rootFile}" -v "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}" {ntuples}'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV[c],bins=binsMJJ[c],MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=1,name=name,data=0,ntuples=ntuples)
                os.system(cmd)


def makeBackgroundShapesMJJKernel(name,filename,template,addCut="1"):
    cut='*'.join([cuts['common'],cuts['allL'],cuts['allP'],cuts['allC'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=outDir+filename+"_"+name+"_detectorResponse.root"            
    cmd='vvMake2DDetectorParam.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt" -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000" {ntuples}'.format(rootFile=resFile,samples=template,cut=cut,ntuples=ntuples)
    os.system(cmd)

    for l in (leptons,leptonsMerged)[MERGELEPNONRES]:
        for p in (purities,puritiesMerged)[MERGEPURNONRES]:
            for c in (categories,categoriesMerged)[MERGECATNONRES]:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceGENMJJ']])

                rootFile=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_l2_gen_softDrop_mass" -u "(1+0.0004*lnujj_l2_gen_pt),(1+0.000001*lnujj_l2_gen_pt*lnujj_l2_gen_pt)" -b {binsMJJ} -x {minMJJ} -X {maxMJJ} -r {res} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,ntuples=ntuples)
                os.system(cmd)


def makeBackgroundShapesMJJSpline(name,filename,template,addCut="1"):
    for l in (leptons,leptonsMerged)[MERGELEPNONRES]:
        for p in (purities,puritiesMerged)[MERGEPURNONRES]:
            for c in (categories,categoriesMerged)[MERGECATNONRES]:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceMVV']])
                rootFile=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake1DTemplateSpline.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_l2_softDrop_mass" -V "lnujj_l2_softDrop_mass_high,lnujj_l2_softDrop_mass_low" -u "(1+0.0004*lnujj_l2_gen_pt),(1+0.000001*lnujj_l2_gen_pt*lnujj_l2_gen_pt)" -b {binsMJJ} -x {minMJJ} -X {maxMJJ} -f {fspline} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,fspline=fspline[c],ntuples=ntuples)
                os.system(cmd)


def mergeBackgroundShapes(name,filename):
    for l in (leptons,leptonsMerged)[MERGELEPNONRES]:
        for p in (purities,puritiesMerged)[MERGEPURNONRES]:
            for c in (categories,categoriesMerged)[MERGECATNONRES]:
                inputy=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                inputx=outDir+filename+"_"+name+"_COND2D_"+l+"_"+p+"_"+c+".root"            
                rootFile=outDir+filename+"_"+name+"_2D_"+l+"_"+p+"_"+c+".root"            
                #cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -C "GPT:GPTBoth" -S "SD:SDY" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
                cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -s "GPT:GPTX,GPT2:GPT2X" -S "SD:SDY" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
                os.system(cmd)

            if MERGECATNONRES:
                for c in categories:
                    os.system('cp LNuJJ_nonRes_2D_'+l+'_'+p+'_allC.root LNuJJ_nonRes_2D_'+l+'_'+p+'_'+c+'.root')
        if MERGEPURNONRES:
            for p in purities:
                for c in categories:
                    os.system('cp LNuJJ_nonRes_2D_'+l+'_allP_'+c+'.root LNuJJ_nonRes_2D_'+l+'_'+p+'_'+c+'.root')
    if MERGELEPNONRES:
        for l in leptons:
            for p in purities:
                for c in categories:
                    os.system('cp LNuJJ_nonRes_2D_allL_'+p+'_'+c+'.root LNuJJ_nonRes_2D_'+l+'_'+p+'_'+c+'.root')




###############################################
###############################################
############  RESONANT BACKGROUND  ############
###############################################
###############################################


def makeBackgroundShapesMVV(name,filename,template,addCut="1"):
    cut='*'.join([cuts['common'],cuts['allL'],cuts['allP'],cuts['allC'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=outDir+filename+"_"+name+"_detectorResponse.root"            
    cmd='vvMake2DDetectorParam.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt" -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000" {ntuples}'.format(rootFile=resFile,samples=template,cut=cut,ntuples=ntuples)
    os.system(cmd)

    for l in leptonsMerged:#leptons:
        for p in puritiesMerged:#purities:
            for c in categoriesMerged:#categories:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceGENMVV']])
                rootFile=outDir+filename+"_"+name+"_MVV_"+l+"_"+p+"_"+c+".root"
                cmd='vvMake1DTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_gen_partialMass" -u "(1+0.0004*lnujj_l2_gen_pt),(1+0.000001*lnujj_l2_gen_pt*lnujj_l2_gen_pt)" -b {binsMVV} -x {minMVV} -X {maxMVV} -r {res} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,ntuples=ntuples)
                os.system(cmd)
    for l in leptons:
        for p in ['HP']:
            for c in ['nobb']:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceGENMVV']])
                rootFile=outDir+filename+"_"+name+"_MVV_"+l+"_"+p+"_"+c+".root"
                cmd='vvMake1DTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_gen_partialMass" -u "(1+0.0004*lnujj_l2_gen_pt),(1+0.000001*lnujj_l2_gen_pt*lnujj_l2_gen_pt)" -b {binsMVV} -x {minMVV} -X {maxMVV} -r {res} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,ntuples=ntuples)
                os.system(cmd)


def makeResMJJPeaksShapes2D(name,filename,template,peak,addCut="1"):
    for l in leptonsMerged:
        for p in puritiesMerged:#purities:
            for c in categoriesMerged:#categories:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut])
                tplFile=outDir+filename+"_"+name+"_MJJGivenMVV_"+p+"_"+c
                debugName=filename+"_"+name+"_MJJ_"+p+"_"+c
                cmd='vvMakeWTopMJJConditionalShapes2D.py -s "{template}" -c "{cut}" -o "{rootFile}" -O "{outDir}" -d "{debugName}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass" -b {binsMVV} -x {minMVV} -X {maxMVV} -B {binsMJJ} -y {minMJJ} -Y {maxMJJ} -E {binsMVVFit} -F {binsMJJFit} -p {peak} {ntuples}'.format(template=template,cut=cut,rootFile=tplFile,outDir=outDir,debugName=debugName,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,binsMVVFit=168,binsMJJFit=90,peak=peak,ntuples=ntuples)
                os.system(cmd)

        for p in ['HP']:
            for c in ['nobb']:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut])
                tplFile=outDir+filename+"_"+name+"_MJJGivenMVV_"+p+"_"+c
                debugName=filename+"_"+name+"_MJJ_"+p+"_"+c
                cmd='vvMakeWTopMJJConditionalShapes2D.py -s "{template}" -c "{cut}" -o "{rootFile}" -O "{outDir}" -d "{debugName}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass" -b {binsMVV} -x {minMVV} -X {maxMVV} -B {binsMJJ} -y {minMJJ} -Y {maxMJJ} -E {binsMVVFit} -F {binsMJJFit} -p {peak} {ntuples}'.format(template=template,cut=cut,rootFile=tplFile,outDir=outDir,debugName=debugName,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,binsMVVFit=168,binsMJJFit=90,peak=peak,ntuples=ntuples)
                os.system(cmd)




###############################################
###############################################
##############  NORMALIZATIONS  ###############
###############################################
###############################################


def makeNormalizations(name,filename,template,data=0,addCut='1',factor=1):
    for l in leptons:
        for p in purities:
            for c in categories:
                rootFile=outDir+filename+"_"+l+"_"+p+"_"+c+".root"
                cut="*".join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptance']])
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}" -o "{rootFile}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}" {ntuples}'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV[c],bins=binsMJJ[c],MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=factor,name=name,data=data,ntuples=ntuples)
                os.system(cmd)







###############################################
###############################################
####################  RUN  ####################
###############################################
###############################################



## Normalizations
if DONORMMC:
    makeNormalizations("nonRes","LNuJJ_norm",nonResTemplate,0,cuts['nonres'],(1.,renormNonRes)[RENORMNONRES])
    makeNormalizations("resW","LNuJJ_norm",resWTemplate,0,cuts['resW'])
    makeNormalizations("resTop","LNuJJ_norm",resTopTemplate,0,cuts['resTop'])
if DONORMDATA:
    makeNormalizations("data","LNuJJ_norm",dataTemplate,1)


## Signal templates
if DOSIGNALSHAPES:
    if DOXWW: makeSignalShapesMJJ("LNuJJ_XWW",WWTemplate)
    if DOXWZ: makeSignalShapesMJJ("LNuJJ_XWZ",WZTemplate)
    if DOXWH: makeSignalShapesMJJ("LNuJJ_XWH",WHTemplate)
    
    if DOXWW: makeSignalShapesMVV("LNuJJ_XWW",WWTemplate)
    if DOXWZ: makeSignalShapesMVV("LNuJJ_XWZ",WZTemplate)
    if DOXWH: makeSignalShapesMVV("LNuJJ_XWH",WHTemplate)

if DOSIGNALYIELDS:
    if DOXWW: makeSignalYields("LNuJJ_XWW",WWTemplate,BRWW,tau21SF,bbWgtWW)
    if DOXWZ: makeSignalYields("LNuJJ_XWZ",WZTemplate,BRWZ,tau21SF,bbWgtWZ)
    if DOXWH: makeSignalYields("LNuJJ_XWH",WHTemplate,BRWH,tau21SF,bbWgtWH)

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

    makeBackgroundShapesMVV("resW","LNuJJ",resWTemplate,cuts['resW'])
    makeResMJJPeaksShapes2D("resW","LNuJJ",resWTemplate,"W",cuts['resW'])

    makeBackgroundShapesMVV("resTop","LNuJJ",resTopTemplate,cuts['resTop'])
    makeResMJJPeaksShapes2D("resTop","LNuJJ",resTopTemplate,"Top",cuts['resTop'])

    os.system( '\cp -p '+outDir+'LNuJJ_resW_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resW_MVV_e_HP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resW_MVV_e_LP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resW_MVV_e_LP_nobb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resW_MVV_mu_HP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resW_MVV_mu_LP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resW_MVV_mu_LP_nobb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MJJGivenMVV_allP_allC.root '+outDir+'LNuJJ_resW_MJJGivenMVV_HP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MJJGivenMVV_allP_allC.root '+outDir+'LNuJJ_resW_MJJGivenMVV_LP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resW_MJJGivenMVV_allP_allC.root '+outDir+'LNuJJ_resW_MJJGivenMVV_LP_nobb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resTop_MVV_e_HP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resTop_MVV_e_LP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resTop_MVV_e_LP_nobb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resTop_MVV_mu_HP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resTop_MVV_mu_LP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MVV_allL_allP_allC.root '+outDir+'LNuJJ_resTop_MVV_mu_LP_nobb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MJJGivenMVV_allP_allC.root '+outDir+'LNuJJ_resTop_MJJGivenMVV_HP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MJJGivenMVV_allP_allC.root '+outDir+'LNuJJ_resTop_MJJGivenMVV_LP_bb.root; '
              +'\cp -p '+outDir+'LNuJJ_resTop_MJJGivenMVV_allP_allC.root '+outDir+'LNuJJ_resTop_MJJGivenMVV_LP_nobb.root; ')



## Non-resonant background templates (W+jets)
if DONONRESONANT:
    makeBackgroundShapesMJJSpline("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])
    makeBackgroundShapesMVVConditional("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])
    mergeBackgroundShapes("nonRes","LNuJJ")




