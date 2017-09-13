import ROOT
import os




cuts={}


cuts['common'] = '((HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)*(run>500) + (run<500)*lnujj_sf)*(Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0&&Flag_badChargedHadronFilter&&Flag_badMuonFilter)'


cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.55)'
cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1>0.55&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'


cuts['nob'] = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'

cuts['resW']='(lnujj_l2_mergedVTruth==1)'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'


leptons=['e','mu']
purities=['HP']
categories=['nob']


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
nonResTemplate="WJetsToLNu_HT,TT_pow,DYJetsToLL_M50_HT"



minMJJ=30.0
maxMJJ=210.0

minMVV=800.0
maxMVV=5000.0

binsMJJ=90
binsMVV=168


cuts['acceptance']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV}&&lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
cuts['acceptanceGEN']= "(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMJJ=25,maxMJJ=300,minMVV=700,maxMVV=10000)                
#cuts['acceptanceGEN']= "(lnujj_l2_gen_softDrop_mass>0&&lnujj_gen_partialMass>0)"

cuts['acceptanceGENMVV']= "(lnujj_gen_partialMass>{minMVV}&&lnujj_gen_partialMass<{maxMVV})".format(minMVV=700,maxMVV=5000)
cuts['acceptanceGENMJJ']= "(lnujj_l2_gen_softDrop_mass>{minMJJ}&&lnujj_l2_gen_softDrop_mass<{maxMJJ}&&lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV})".format(minMJJ=minMJJ-5,maxMJJ=maxMJJ+5,minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceMJJ']= "(lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ)                


def makeSignalShapesMVV(filename,template):
    for l in leptons:
        cut='*'.join([cuts['common'],cuts[l],cuts['acceptanceMJJ']])
        rootFile=filename+"_MVV_"+l+".root"
        cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_LV_mass"  samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
        os.system(cmd)
        jsonFile=filename+"_MVV_"+l+".json"
        print 'Making JSON'
        cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol1,ALPHA1:pol2,N1:pol0,ALPHA2:pol2,N2:pol0" -m 800 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        os.system(cmd)


def makeSignalShapesMJJ(filename,template):
    for p in purities:
        cut='*'.join([cuts['common'],cuts[p]])
        rootFile=filename+"_MJJ_"+p+".root"
        doExp=1
        if p=='HP' or p=='NP':
            doExp=0
        cmd='vvMakeSignalMJJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_l2_softDrop_mass" -m {minMJJ} -M {maxMJJ} -e {doExp} -f "alpha:1.347" samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=doExp)
        os.system(cmd)
        jsonFile=filename+"_MJJ_"+p+".json"

        if p=='HP' or p=='NP':
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        else:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol3,sigma:pol1,alpha:pol0,n:pol0,slope:pol1,f:laur4,alpha2:pol0,n2:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)

        os.system(cmd)



def makeHiggsShapesMJJ(filename,template):
    for p in purities:
        cut='*'.join([cuts['common'],cuts[p]])
        rootFile=filename+"_MJJ_"+p+".root"
        doExp=1
        if p=='HP' or p=='NP':
            doExp=0
        cmd='vvMakeSignalMJJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_l2_softDrop_mass" -m {minMJJ} -M {maxMJJ} -e {doExp} -f "" samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=doExp)
        os.system(cmd)
        jsonFile=filename+"_MJJ_"+p+".json"

        if p=='HP' or p=='NP':
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        else:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol3,sigma:pol1,alpha:pol0,n:pol0,slope:pol1,f:laur4,alpha2:pol0,n2:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)

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




def makeBackgroundShapesMVVConditional(name,filename,template,addCut=""):
    #first parameterize detector response
    cut='*'.join([cuts['common'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=filename+"_"+name+"_detectorResponse.root"            
    cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_LV_mass,lnujj_l2_softDrop_mass"  -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt"  -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   samples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name)
    os.system(cmd)


    for c in categories:
        if c=='vbf':
            pur=['NP']
            catcut=cuts['dijet']
        else:
            pur=['HP','LP']
            catcut=cuts[c]

        for p in pur:
            for l in leptons:
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],catcut,cuts[l],cuts['acceptanceGEN']])
                else:
                    cut='*'.join([cuts['common'],cuts[p],catcut,cuts[l],addCut,cuts['acceptanceGEN']])
                rootFile=filename+"_"+name+"_COND2D_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake2DTemplateWithKernels.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass"  -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ}  -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
                os.system(cmd)



def makeBackgroundShapesMJJKernel(name,filename,template,addCut=""):
    #first parameterize detector response
    cut='*'.join([cuts['common'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=filename+"_"+name+"_detectorResponse.root"            
    cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_LV_mass,lnujj_l2_softDrop_mass"  -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt"  -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   samples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name)
    os.system(cmd)

    for c in categories:
        if c=='vbf':
            pur=['NP']
#            c='dijet'
        else:
            pur=['HP','LP']
        for p in pur:
            for l in leptons:
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],cuts[l],cuts['acceptanceGENMJJ']])
                else:
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],addCut,cuts[l],cuts['acceptanceGENMJJ']])
                rootFile=filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_l2_gen_softDrop_mass"  -b {binsMJJ}  -x {minMJJ} -X {maxMJJ} -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
                os.system(cmd)


def makeBackgroundShapesMJJSpline(name,filename,template,addCut=""):
    for c in categories:
        if c=='vbf':
            pur=['NP']
#            c='dijet'
        else:
            pur=['HP','LP']
        for p in pur:
            for l in leptons:
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],cuts[l],cuts['acceptance']])
                else:
                    cut='*'.join([cuts['common'],cuts[p],cuts[c],addCut,cuts[l],cuts['acceptance']])
                rootFile=filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake1DTemplateSpline.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_l2_softDrop_mass"  -b {binsMJJ}  -x {minMJJ} -X {maxMJJ} -f 6 samples'.format(rootFile=rootFile,samples=template,cut=cut,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
                os.system(cmd)


def mergeBackgroundShapes(name,filename):
    #first parameterize detector response
    for c in categories:
        if c=='vbf':
            pur=['NP']
        else:
            pur=['HP','LP']
        for p in pur:
            for l in leptons:
                inputy=filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"            
                inputx=filename+"_"+name+"_COND2D_"+l+"_"+p+"_"+c+".root"            
                rootFile=filename+"_"+name+"_2D_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMergeHistosToPDF2D.py -i "{inputx}" -I "{inputy}" -o "{rootFile}" -s "Scale:ScaleX,PT:PTX,OPT:OPTX,PT2:PTX2,Res:ResX,TOP:TOPX" -S "PT:PTY,OPT:OPTY" -C "PT:PTBoth" '.format(rootFile=rootFile,inputx=inputx,inputy=inputy)
                os.system(cmd)

                os.system(cmd)


def makeBackgroundShapesMVV(name,filename,template,addCut=""):
    #first parameterize detector response


    cut='*'.join([cuts['common'],'lnujj_l2_gen_softDrop_mass>10&&lnujj_gen_partialMass>0',addCut])
    resFile=filename+"_"+name+"_detectorResponse.root"            
    cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_LV_mass,lnujj_l2_softDrop_mass"  -g "lnujj_gen_partialMass,lnujj_l2_gen_softDrop_mass,lnujj_l2_gen_pt"  -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   samples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name)
    os.system(cmd)

    for l in leptons:
        for c in categories:
            if c=='vbf':
                pur=['NP']
#                cutcat=cuts['dijet']
                cutcat=cuts['dijet']
            else:
                pur=['HP','LP']
                cutcat=cuts[c]

            for p in pur:
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[l],cuts[p],cutcat,cuts['acceptanceGENMVV']])
                else:
                    cut='*'.join([cuts['common'],cuts[l],cuts[p],cutcat,addCut,cuts['acceptanceGENMVV']])
                rootFile=filename+"_"+name+"_MVV_"+l+"_"+p+"_"+c+".root"            
                cmd='vvMake1DTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "lnujj_gen_partialMass"  -b {binsMVV}  -x {minMVV} -X {maxMVV} -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV)
                os.system(cmd)



def makeResWMJJShapes(name,filename,template,addCut=""):
    for p in purities:
        if p=='HP' or p=='NP':
            doExp=0    
        else:
            doExp=1    

        if addCut=='':
            cut='*'.join([cuts['common'],cuts[p],cuts['inc']])
        else:
            cut='*'.join([cuts['common'],cuts[p],cuts['inc'],addCut])
                       
        mjjFile=filename+"_MJJ_"+name+"_"+p
        jsonFile=filename+"_XWW_MJJ_"+p+".json"
        cmd='vvMakeTopMJJConditionalShapesFromTruth.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -V "lnujj_LV_mass"  -b 20  -x {minMJJ} -X {maxMJJ} -e {doExp} -j {jsonFile} samples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=doExp,jsonFile=jsonFile)
        os.system(cmd)
#        print 'NOT RUNNING FIT'
        jsonFile=filename+"_MJJ_"+name+"_"+p+".json"
        if doExp==0:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol1,sigma:llog,alpha:pol3,n:pol0,alpha2:pol0,n2:pol0" -m 500 -M 2500  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')
        else:
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol1,sigma:llog,alpha:pol3,n:pol0,alpha2:pol0,n2:pol0,slope:pol0,f:pol0" -m 500 -M 2500  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')

        os.system(cmd)




def makeResTopMJJShapes(name,filename,template,addCut=""):
    for p in purities:
        if addCut=='':
            cut='*'.join([cuts['common'],cuts[p]])
        else:
            cut='*'.join([cuts['common'],cuts[p],addCut])

        mjjFile=filename+"_MJJ_"+name+"_"+p
        jsonFile=filename+"_MJJ_"+name+"_"+p+".json"

        if p in ['HP','NP']:    
            cmd='vvMakeTopMJJMergedConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -V "lnujj_LV_mass"  -b 60  -x {minMJJ} -X {maxMJJ} -f "meanW:81.9752,sigmaW:9.10,sigmaTop:15.075,alphaW:1.3,alphaW2:1.17,alphaTop:0.622,alphaTop2:1.58" samples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=230)
            os.system(cmd)
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "meanW:pol0,sigmaW:pol0,meanTop:laur3,sigmaTop:pol0,alphaW:pol0,alphaTop:pol0,alphaW2:pol2,alphaTop2:pol0,n:pol0,f:laur5,f2:pol0,slope:pol0" -m 500 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')
            os.system(cmd)

        else:
            cmd='vvMakeTopMJJMergedConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -V "lnujj_LV_mass"  -b 60  -x {minMJJ} -X {maxMJJ} -f "meanW:77.045,sigmaW:8.6,sigmaTop:18.49,alphaTop2:1.069,alphaW2:0.768,alphaTop:0.524,slope:-0.0196,f2:0.952" -e 1 samples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=230)
            os.system(cmd)
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "meanW:pol0,sigmaW:pol0,meanTop:laur3,sigmaTop:pol0,alphaW:laur2,alphaTop:pol0,alphaW2:pol2,alphaTop2:pol0,n:pol0,f:laur5,f2:pol0,slope:pol0" -m 500 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=mjjFile+'.root')
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
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJJ,MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=factor,name=name,data=data)
                os.system(cmd)




#makeSignalShapesMVV("LNuJJ_XWW",WWTemplate)
#makeSignalShapesMVV("LNuJJ_XWZ",WZTemplate)
#makeSignalShapesMVV("LNuJJ_XWH",WHTemplate)


#makeSignalShapesMJJ("LNuJJ_XWW",WWTemplate)
#makeSignalShapesMJJ("LNuJJ_XWZ",WZTemplate)
#makeHiggsShapesMJJ("LNuJJ_XWH",WHTemplate)


#makeSignalYields("LNuJJ_XWW",WWTemplate,BRWW,{'HP':1.03,'LP':0.95})
#makeSignalYields("LNuJJ_XWZ",WZTemplate,BRWZ,{'HP':1.03,'LP':0.95})
#makeSignalYields("LNuJJ_XWH",WHTemplate,BRWH,{'HP':1.03,'LP':0.95})

###makeSignalYields("LNuJJ_VBFXWW",VBFWWTemplate,BRVBFWW)





#makeResTopMJJShapes("resW","LNuJJ",resWMJJTemplate,cuts['resW'])
#makeBackgroundShapesMVV("resW","LNuJJ",resWTemplate,cuts['resW'])

#print 'OK GOING FOR THE 2D ONES'

makeBackgroundShapesMJJSpline("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])
#makeBackgroundShapesMVVConditional("nonRes","LNuJJ",nonResTemplate,cuts['nonres'])
#mergeBackgroundShapes("nonRes","LNuJJ")






#makeNormalizations("nonRes","LNuJJ",nonResTemplate,0,cuts['nonres'],1.0)
#makeNormalizations("resW","LNuJJ",resWTemplate,0,cuts['resW'])
#makeNormalizations("data","LNuJJ",dataTemplate,1)
