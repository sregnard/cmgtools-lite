import ROOT
import os




cuts={}


cuts['common'] = '((HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*(run>500) + (run<500)*lnujj_sf)*(Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0&&Flag_badChargedHadronFilter&&Flag_badMuonFilter)'


cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.55)'
cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1>0.55&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'


cuts['nob'] = '(lnujj_nMediumBTags==0&&lnujj_l2_softDrop_mass>65&&lnujj_l2_softDrop_mass<85)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags==0&&lnujj_l2_softDrop_mass>85&&lnujj_l2_softDrop_mass<105)*lnujj_btagWeight'

cuts['resW']='(lnujj_l2_mergedVTruth==1)'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'


leptons=['mu','e']
purities=['HP','LP']
categories=['nob','b']


WWTemplate="BulkGravToWWToWlepWhad_narrow"
BRWW=2.*0.327*0.6760


VBFWWTemplate="VBF_RadionToWW_narrow"
BRVBFWW=1.0

WZTemplate="WprimeToWZToWlepZhad_narrow"
BRWZ=0.327*0.6991

WHTemplate="WprimeToWhToWlephbb"
#BRWH=0.59*0.327
BRWH=0.327

dataTemplate="SingleMuon,SingleElectron,MET"
resWTemplate="TT_pow,WWTo1L1Nu2Q"
resWMJJTemplate="TT_pow,WWTo1L1Nu2Q"
resZTemplate="WZTo1L1Nu2Q"
nonResTemplate="WJetsToLNu_HT,TT_pow,DYJetsToLL_M50_HT,QCD_HT"



minMVV=800.0
maxMVV=2000.0
binsMVV=24


cuts['acceptance']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)

def makeSignalShapesMVV(filename,template):
    for l in leptons:
        cut='*'.join([cuts['common'],cuts[l],cuts['nob']])
        rootFile=filename+"_MVV_"+l+".root"
        cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_LV_mass"  samples'.format(template=template,cut=cut,rootFile=rootFile)
        os.system(cmd)
        jsonFile=filename+"_MVV_"+l+".json"
        print 'Making JSON'
        cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol1,ALPHA1:pol2,N1:pol0,ALPHA2:pol2,N2:pol0" -m 800 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        os.system(cmd)

def makeSignalYields(filename,template,branchingFraction,sfP = {'HP':1.0,'LP':1.0}):
    for region in categories:
        if region=='vbf':
            pur=['NP']
        else:
            pur=['HP','LP']
            
        for purity in pur:
            for lepton in leptons:
                cut = "*".join([cuts[lepton],cuts[purity],cuts['common'],cuts[region],cuts['acceptance'],str(sfP[purity])])
                #Signal yields
                yieldFile=filename+"_"+lepton+"_"+purity+"_"+region+"_yield"
                cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "lnujj_LV_mass" -m {minMVV} -M {maxMVV} -f "pol5" -b {BR} -x 950 samples'.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,BR=branchingFraction)
                os.system(cmd)



def makeNormalizations(name,filename,template,data=0,addCut='',factor=1):
    for region in categories:
        if region=='vbf':
            pur=['NP']
        else:
            pur=['HP','LP']
        for purity in pur:
            for lepton in leptons:
                rootFile=filename+"_"+lepton+"_"+purity+"_"+region+".root"
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region],cuts['acceptance']])
                else:
                    cut='*'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region],addCut,cuts['acceptance']])
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -b "{BINS}" -m "{MINI}" -M "{MAXI}" -f {factor} -n "{name}"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,MINI=minMVV,MAXI=maxMVV,factor=factor,name=name,data=data)
                os.system(cmd)
def makeUpDown(name,filename,template,data=0,addCut='',factor=1):
    for region in categories:
        if region=='vbf':
            pur=['NP']
        else:
            pur=['HP','LP']
        for purity in pur:
            for lepton in leptons:
                rootFile=filename+"_"+lepton+"_"+purity+"_"+region+".root"
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region]])
                else:
                    cut='*'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region],addCut])
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass*1.2" -b "{BINS}" -m "{MINI}" -M "{MAXI}" -f {factor} -n "{name}_shape_{name}Up"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,MINI=minMVV,MAXI=maxMVV,factor=factor,name=name,data=data)
                os.system(cmd)
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass*0.8" -b "{BINS}" -m "{MINI}" -M "{MAXI}" -f {factor} -n "{name}_shape_{name}Down"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,MINI=minMVV,MAXI=maxMVV,factor=factor,name=name,data=data)
                os.system(cmd)



#makeSignalShapesMVV("LNuJJ_XWW",WWTemplate)
#makeSignalShapesMVV("LNuJJ_XWZ",WZTemplate)

#makeSignalYields("LNuJJ_XWW",WWTemplate,BRWW,{'HP':1.03,'LP':0.95})
#makeSignalYields("LNuJJ_XWZ",WZTemplate,BRWZ,{'HP':1.03,'LP':0.95})



#makeNormalizations("nonRes","LNuJJ",nonResTemplate,0,cuts['nonres'],1.0)
#makeNormalizations("resW","LNuJJ",resWTemplate,0,cuts['resW'])
#makeNormalizations("data","LNuJJ",dataTemplate,1)

makeUpDown("nonRes","LNuJJ",nonResTemplate,0,cuts['nonres'],1.0)
makeUpDown("resW","LNuJJ",resWTemplate,0,cuts['resW'])
