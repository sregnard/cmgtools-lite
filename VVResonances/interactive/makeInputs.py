import ROOT
import os, sys

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",type=int,default=2016,help="2016 or 2017 or 2018")
(options,args) = parser.parse_args()



DONORM        = 1
DOSIGNAL      = 1
DORESONANT    = 1
DONONRESONANT = 1



###############################################
###############################################
#################  PARAMETERS  ################
###############################################
###############################################


if options.year not in [2016,2017,2018]:
    parser.error("year must be 2016, 2017, or 2018")
YEAR=options.year

outDir='Inputs_'+str(YEAR)+'/'
os.system('mkdir -p '+outDir)

ntuples='ntuples'+str(YEAR)
bbtagger=''
if YEAR==2016: 
    bbtagger='lnujj_l2_btagBOOSTED_recalc'
elif (YEAR==2017 or YEAR==2018): 
    bbtagger='lnujj_l2_btagBOOSTED'



USETAU21DDT = 0
MERGELEPNONRES = 0
MERGEPURNONRES = 0
MERGECATNONRES = 0



cuts={}

cuts['common'] = ''
if YEAR==2016:
    cuts['common'] = '((HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*(run>500) + (run<500)*lnujj_sf)*(Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0&&Flag_badChargedHadronFilter&&Flag_badMuonFilter)'
elif YEAR==2017 or YEAR==2018:
    cuts['common'] = '(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*lnujj_sfWV*(lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0)'

## new cut on pT/M:
cuts['common'] = cuts['common'] + '*(lnujj_l1_pt/lnujj_LV_mass>0.4&&lnujj_l2_pt/lnujj_LV_mass>0.4)'

cuts['nob'] = '(lnujj_nMediumBTags==0)' #*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)' #*lnujj_btagWeight'
## b-tag veto is now the default; put the btag weight only here:
cuts['common'] = cuts['common'] + '*' + cuts['nob'] + '*lnujj_btagWeight'

cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['allL'] = '(abs(lnujj_l1_l_pdgId)==11||abs(lnujj_l1_l_pdgId)==13)'
leptons=['e','mu']
leptonsMerged=['allL']

## tighter HP/LP cuts than in the 2016 analysis:
cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.45)'
cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1>0.45&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'
cuts['allP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.75)'
if USETAU21DDT:
    cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1-(-0.06845)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)<0.6)'
    cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1-(-0.06845)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)>0.6&&lnujj_l2_tau2/lnujj_l2_tau1-(-0.06845)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)<0.9)'
    cuts['allP'] = '(lnujj_l2_tau2/lnujj_l2_tau1-(-0.06845)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt)<0.9)'
purities=['HP','LP']
puritiesMerged=['allP']

cuts['bb'] = '('+bbtagger+'>0.3)'
cuts['nobb'] = '('+bbtagger+'<0.3)'
cuts['allC'] = '1'
categories=['bb','nobb']
categoriesMerged=['allC']

cuts['resW']='(lnujj_l2_mergedVTruth==1)'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'




WWTemplate="BulkGravToWWToWlepWhad_narrow"
BRWW=2.*0.327*0.6760

WZTemplate="WprimeToWZToWlepZhad_narrow"
BRWZ=0.327*0.6991

WHTemplate="WprimeToWhToWlephbb_narrow"
BRWH=0.327*0.59

dataTemplate=""
resWTemplate=""
nonResTemplate=""
if YEAR==2016:
    dataTemplate="SingleMuon,SingleElectron,MET"
    resWTemplate="TT_pow,WWTo1L1Nu2Q"
    nonResTemplate="WJetsToLNu_HT,TT_pow,DYJetsToLL_M50_HT"
elif YEAR==2017:
    dataTemplate="SingleMuon,SingleElectron,MET"
    resWTemplate="TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ"
    nonResTemplate="WJetsToLNu_HT,TTHad_pow,TTLep_pow,TTSemi_pow,DYJetsToLL_M50_HT"
elif YEAR==2018:
    dataTemplate="SingleMuon,EGamma,MET"
    resWTemplate="TTHad_pow,TTLep_pow,TTSemi_pow,WWToLNuQQ"
    nonResTemplate="WJetsToLNu_HT,TTHad_pow,TTLep_pow,TTSemi_pow,DYJetsToLL_M50_HT"



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

minMXSigParam = 999 #601
maxMXSigParam = 5000

limitTailFit2D = 1600

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
                cmd='vvMakeSignalMJJShapes.py -s "{template}" -c "{cut}" -o "{rootFile}" -d "{debugFile}" -V "lnujj_l2_softDrop_mass" -m {minMJJ} -M {maxMJJ} -e {doExp} {force} {ntuples}'.format(template=template,cut=cut,rootFile=rootFile,debugFile=debugFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=int(doExp),force=("-f "+force) if force!="" else "",ntuples=ntuples)
                os.system(cmd)
                
                jsonFile=outDir+filename+"_MJJ_"+p+"_"+c+".json"
                debugFile=outDir+"debugSignalShape_"+filename+"_MJJ_"+p+"_"+c+".root"
                print 'Making JSON ', jsonFile
                if p=='HP' or p=='NP':
                    cmd='vvMakeJSON.py -o "{jsonFile}" -d "{debugFile}" -g "mean:pol4,sigma:pol4,alpha:pol0,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m {minMX} -M {maxMX} {rootFile}'.format(jsonFile=jsonFile,debugFile=debugFile,minMX=minMXSigParam,maxMX=maxMXSigParam,rootFile=rootFile)
                else:
                    cmd='vvMakeJSON.py -o "{jsonFile}" -d "{debugFile}" -g "mean:pol4,sigma:pol1,alpha:pol0,n:pol0,alpha2:pol0,n2:pol0,slope:pol4,f:laur4" -m {minMX} -M {maxMX} {rootFile}'.format(jsonFile=jsonFile,debugFile=debugFile,minMX=minMXSigParam,maxMX=maxMXSigParam,rootFile=rootFile)
                os.system(cmd)


def makeSignalShapesMVV(filename,template):
    for l in leptonsMerged:
        for p in purities:
            for c in categories:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],cuts['acceptanceMJJ']])

                rootFile=outDir+filename+"_MVV_"+p+"_"+c+".root"
                debugFile=outDir+"debugVV_"+filename+"_MVV_"+p+"_"+c
                cmd='vvMakeSignalMVVShapes.py -s "{template}" -m {minMX} -M {maxMX} -c "{cut}" -o "{rootFile}" -d "{debugFile}" -v "lnujj_LV_mass" -b {binsMVV} -x {minMVV} -X {maxMVV} {ntuples}'.format(template=template,minMX=minMXSigParam,maxMX=maxMXSigParam,cut=cut,rootFile=rootFile,debugFile=debugFile,binsMVV=1000,minMVV=0,maxMVV=8000,ntuples=ntuples)
                os.system(cmd)
                
                jsonFile=outDir+filename+"_MVV_"+p+"_"+c+".json"
                debugFile=outDir+"debugSignalShape_"+filename+"_MVV_"+p+"_"+c+".root"
                print 'Making JSON ', jsonFile
                cmd='vvMakeJSON.py -o "{jsonFile}" -d "{debugFile}" -g "MEAN:pol1,SIGMA:pol1,ALPHA1:pol2,N1:pol0,ALPHA2:pol2,N2:pol0" -m {minMX} -M {maxMX} {rootFile}'.format(jsonFile=jsonFile,debugFile=debugFile,minMX=minMXSigParam,maxMX=maxMXSigParam,rootFile=rootFile)
                os.system(cmd)


def makeSignalYields(filename,template,branchingFraction,sfP = {'HP':1.0,'LP':1.0}):
    for l in leptons:
        for p in purities:
            for c in categories:
                cut = "*".join([cuts['common'],cuts[l],cuts[p],cuts[c],cuts['acceptance'],str(sfP[p])])

                yieldFile=outDir+filename+"_"+l+"_"+p+"_"+c+"_yield"
                debugFile=outDir+"debugSignalYield_"+filename+"_"+l+"_"+p+"_"+c
                cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -d "{debugFile}" -V "lnujj_LV_mass" -m {minMVV} -M {maxMVV} -f "pol5" -b {BR} -x {minMX} {ntuples}'.format(template=template,cut=cut,output=yieldFile,debugFile=debugFile,minMVV=minMVV,maxMVV=maxMVV,BR=branchingFraction,minMX=minMXSigParam,ntuples=ntuples)
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
                cmd='vvMake2DTemplateWithKernels.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass" -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ} -r {res} -l {limitTailFit2D} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,limitTailFit2D=limitTailFit2D,ntuples=ntuples)
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
                cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_l2_gen_softDrop_mass" -b {binsMJJ} -x {minMJJ} -X {maxMJJ} -r {res} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,ntuples=ntuples)
                os.system(cmd)


def makeBackgroundShapesMJJSpline(name,filename,template,addCut="1"):
    for l in (leptons,leptonsMerged)[MERGELEPNONRES]:
        for p in (purities,puritiesMerged)[MERGEPURNONRES]:
            for c in (categories,categoriesMerged)[MERGECATNONRES]:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceMVV']])
                rootFile=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake1DTemplateSpline.py -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_l2_softDrop_mass" -b {binsMJJ} -x {minMJJ} -X {maxMJJ} -f {fspline} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,fspline=fspline[c],ntuples=ntuples)
                os.system(cmd)


def mergeBackgroundShapes(name,filename):
    for l in (leptons,leptonsMerged)[MERGELEPNONRES]:
        for p in (purities,puritiesMerged)[MERGEPURNONRES]:
            for c in (categories,categoriesMerged)[MERGECATNONRES]:
                inputy=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                inputx=outDir+filename+"_"+name+"_COND2D_"+l+"_"+p+"_"+c+".root"            
                rootFile=outDir+filename+"_"+name+"_2D_"+l+"_"+p+"_"+c+".root"            
                #cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -s "Scale:ScaleX,PT:PTX,OPT:OPTX,PT2:PTX2,Res:ResX,TOP:TOPX" -S "PT:PTY,OPT:OPTY" -C "PT:PTBoth" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
                cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -s "Scale:ScaleX,PT:PTX,OPT:OPTX,PT2:PTX2,TOP:TOPX" -S "PT:PTY,OPT:OPTY" -C "PT:PTBoth" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
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

    for l in leptons:
        for p in purities:
            for c in categories:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptanceGENMVV']])

                rootFile=outDir+filename+"_"+name+"_MVV_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake1DTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{samples}" -c "{cut}" -v "lnujj_gen_partialMass" -b {binsMVV} -x {minMVV} -X {maxMVV} -r {res} {ntuples}'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,ntuples=ntuples)
                os.system(cmd)


def makeResTopMJJShapes2D(name,filename,template,addCut="1"):
    for l in leptonsMerged:
        for p in purities:
            for c in categories:
                cut='*'.join([cuts['common'],cuts[l],cuts[p],cuts[c],addCut])

                tplFile=outDir+filename+"_"+name+"_MJJGivenMVV_"+p+"_"+c
                debugName=name+"_MJJ_"+p+"_"+c

                cmd='vvMakeTopMJJMergedConditionalShapes2D.py -s "{template}" -c "{cut}" -o "{rootFile}" -O "{outDir}" -d "{debugName}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass" -b {binsMVV} -x {minMVV} -X {maxMVV} -B {binsMJJ} -y {minMJJ} -Y {maxMJJ} -E {binsMVVFit} -F {binsMJJFit} {e} {ntuples}'.format(template=template,cut=cut,rootFile=tplFile,outDir=outDir,debugName=debugName,binsMVV=binsMVV[c],minMVV=minMVV,maxMVV=maxMVV,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,binsMVVFit=168,binsMJJFit=90,e="-e",ntuples=ntuples) 

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
if DONORM:
    makeNormalizations("nonRes","LNuJJ",nonResTemplate,0,cuts['nonres'])
    makeNormalizations("resW","LNuJJ",resWTemplate,0,cuts['resW'])
    makeNormalizations("data","LNuJJ",dataTemplate,1)


## Signal templates
if DOSIGNAL:
    makeSignalShapesMJJ("LNuJJ_XWW",WWTemplate)
    makeSignalShapesMJJ("LNuJJ_XWZ",WZTemplate)
    makeSignalShapesMJJ("LNuJJ_XWH",WHTemplate)
    
    makeSignalShapesMVV("LNuJJ_XWW",WWTemplate)
    makeSignalShapesMVV("LNuJJ_XWZ",WZTemplate)
    makeSignalShapesMVV("LNuJJ_XWH",WHTemplate)

    makeSignalYields("LNuJJ_XWW",WWTemplate,BRWW,{'HP':1.03,'LP':0.95})
    makeSignalYields("LNuJJ_XWZ",WZTemplate,BRWZ,{'HP':1.03,'LP':0.95})
    makeSignalYields("LNuJJ_XWH",WHTemplate,BRWH,{'HP':1.03,'LP':0.95})

    #''' ##for control plots
    for mx in [600,800,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]:
        makeNormalizations("XWW"+str(mx).zfill(4),"LNuJJ",WWTemplate+"_"+str(mx),0,'1',BRWW)
        if mx!=4000: makeNormalizations("XWZ"+str(mx).zfill(4),"LNuJJ",WZTemplate+"_"+str(mx),0,'1',BRWZ)
        if mx!=1200: makeNormalizations("XWH"+str(mx).zfill(4),"LNuJJ",WHTemplate+"_"+str(mx),0,'1',BRWH)

    makeNormalizations("XWWall","LNuJJ",WWTemplate,0,'1',BRWW)
    makeNormalizations("XWZall","LNuJJ",WZTemplate,0,'1',BRWZ)
    makeNormalizations("XWHall","LNuJJ",WHTemplate,0,'1',BRWH)
    #'''


## Resonant background templates (W+V/t)
if DORESONANT:
    makeBackgroundShapesMVV("resW","LNuJJ",resWTemplate,cuts['resW'])
    makeResTopMJJShapes2D("resW","LNuJJ",resWMJJTemplate,cuts['resW'])


## Non-resonant background templates (W+jets)
if DONONRESONANT:

    ##makeBackgroundShapesMJJKernel("nonRes","LNuJJ",nonResTemplate,cuts['nonres']) ##replaced by following line
    makeBackgroundShapesMJJSpline("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])

    makeBackgroundShapesMVVConditional("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])

    mergeBackgroundShapes("nonRes","LNuJJ")

    ##makeBackgroundShapesMVV("nonRes","LNuJJ",nonResTemplate,cuts['nonres']) ##check




