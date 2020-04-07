import ROOT
import json
import time

class Fitter(object):
    def __init__(self,poi = ['x']):
        self.cache=ROOT.TFile("cache.root","RECREATE")
        #self.cache=ROOT.TFile("cache_"+str(time.time())+".root","RECREATE")
        self.cache.cd()

        self.w=ROOT.RooWorkspace("w","w")
        self.dimensions = len(poi)
        self.poi=poi
        for v in poi:
            self.w.factory(v+"[1,161]")


    def factory(self,expr):
        self.w.factory(expr)

    def function(self,name,function,dependents):
        self.w.factory("expr::"+name+"('"+function+"',"+','.join(dependents)+")")


    def bernstein(self,name = 'model',poi='x',order=1):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        cList = ROOT.RooArgList()
        for i in range(0,order):
            self.w.factory("c_"+str(i)+"[0,100]")
            cList.add(self.w.var("c_"+str(i)))
        bernsteinPDF = ROOT.RooBernsteinFast(order)(name,name,self.w.var(poi),cList)
        getattr(self.w,'import')(bernsteinPDF,ROOT.RooFit.Rename(name))


    def mjjSignalBinned(self,name = 'model',poi='x',filename="mjjSignal.root",boson="W"):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        
        cList = ROOT.RooArgList()
        self.w.factory("c_0[-1,1]")
        self.w.factory("c_1[-1,1]")
        cList.add(self.w.var("c_0"))
        cList.add(self.w.var("c_1"))
        f=ROOT.TFile(filename)
        V = f.Get(boson)
        V_sup = f.Get(boson+"_jetMassScaleUp")
        V_sdwn = f.Get(boson+"_jetMassScaleDown")
        V_rup = f.Get(boson+"_jetMassResUp")
        V_rdwn = f.Get(boson+"_jetMassResDown")
        
        VH=ROOT.RooDataHist(boson+"H",boson+"H",ROOT.RooArgList(self.w.var(poi)),V)
        V_supH=ROOT.RooDataHist(boson+"supH",boson+"H",ROOT.RooArgList(self.w.var(poi)),V_sup)
        V_sdwnH=ROOT.RooDataHist(boson+"sdwnH",boson+"H",ROOT.RooArgList(self.w.var(poi)),V_sdwn)
        V_rupH=ROOT.RooDataHist(boson+"rupH",boson+"H",ROOT.RooArgList(self.w.var(poi)),V_rup)
        V_rdwnH=ROOT.RooDataHist(boson+"rdwnH",boson+"H",ROOT.RooArgList(self.w.var(poi)),V_rdwn)

        VPdf=ROOT.RooHistPdf(boson+"Pdf",boson+"P",ROOT.RooArgSet(self.w.var(poi)),VH)
        V_supPdf=ROOT.RooHistPdf(boson+"supPdf",boson+"P",ROOT.RooArgSet(self.w.var(poi)),V_supH)
        V_sdwnPdf=ROOT.RooHistPdf(boson+"sdwnPdf",boson+"P",ROOT.RooArgSet(self.w.var(poi)),V_sdwnH)
        V_rupPdf=ROOT.RooHistPdf(boson+"rupPdf",boson+"P",ROOT.RooArgSet(self.w.var(poi)),V_rupH)
        V_rdwnPdf=ROOT.RooHistPdf(boson+"rdwnPdf",boson+"P",ROOT.RooArgSet(self.w.var(poi)),V_rdwnH)
        
        pdfList=ROOT.RooArgList(VPdf,V_supPdf,V_sdwnPdf,V_rupPdf,V_rdwnPdf)                  

        bernsteinPDF = ROOT.FastVerticalInterpHistPdf(name,name,self.w.var(poi),pdfList,cList)
        getattr(self.w,'import')(bernsteinPDF,ROOT.RooFit.Rename(name))


    def gaussianSum(self,name,poi,dataset,variable):
        self.w.factory('scale[1.0,0.1,2]')
        self.w.factory('sigma[30,1,1e+4]')
        self.w.factory('sigma2[0]')
        gaussianSum=ROOT.RooGaussianSumPdf(name,name,self.w.var(poi), self.w.var('scale'),self.w.var('sigma'),self.w.var('sigma2'),dataset,variable)
        getattr(self.w,'import')(gaussianSum,ROOT.RooFit.Rename(name))


    def mjjParamErfExp(self,name,jsonFile):
        self.w.factory("MH[2000]")
        self.w.var("MH").setConstant(1)
        varToReplace='x'

        f=open(jsonFile)
        info=json.load(f)

        self.w.factory("expr::{name}('({param})',x)".format(name='mean',param=info['mean']).replace("MH",varToReplace))
        self.w.factory("expr::{name}('({param})',x)".format(name='sigma',param=info['sigma']).replace("MH",varToReplace))
        self.w.factory("expr::{name}('MH*0+{param}',x)".format(name='alpha',param=info['alpha']).replace("MH",varToReplace))
        self.w.factory("expr::{name}('MH*0+{param}',x)".format(name='n',param=info['n']).replace("MH",varToReplace))
        vvMass = ROOT.RooCBShape(name+'Peak','peak',self.w.var('y'),self.w.function('mean'),self.w.function('sigma'),self.w.function('alpha'),self.w.function('n'))
        getattr(self.w,'import')(vvMass,ROOT.RooFit.Rename(name+'Peak'))


        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name='slope',param=info['slope']).replace("MH",varToReplace))
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name='f',param=info['f']).replace("MH",varToReplace))
        self.w.factory("RooExponential::{name}({var},{SLOPE})".format(name=name+'Expo',var='y',SLOPE='slope').replace("MH",varToReplace))
        self.w.factory("SUM::{name}1({f}*{PDF1},{PDF2})".format(name=name,f='f',PDF1=name+"Peak",PDF2=name+'Expo'))
        f.close()
        self.erfexp(name+'2','y')
        self.w.factory("SUM::{name}(c_3[0.5,0,1]*{name}1,{name}2)".format(name=name))
        





    def expoN(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[-0.005,-0.1,0]")
        self.w.factory("c_1[-5000,-100000,0]")       
        expoNPDF = ROOT.RooExpNPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"))
        getattr(self.w,'import')(expoNPDF,ROOT.RooFit.Rename(name))







    def expoTail(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[1,0,10000]")
        self.w.factory("c_1[0,-1,10000]")       
        expoNPDF = ROOT.RooExpTailPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"))
        getattr(self.w,'import')(expoNPDF,ROOT.RooFit.Rename(name))


    def fancy(self,name = 'model',poi='x',histo=None):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[0,-200,200]")
        self.w.factory("c_1[10,0,10000]")       
        fancy = ROOT.DynamicBinnedSmearingPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),histo)
        getattr(self.w,'import')(fancy,ROOT.RooFit.Rename(name))



    def bernsteinPlusGaus(self,name = 'model',poi='x',order=1):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("RooGaussian::"+name+"G(x,c_0[-10,-15,15],c_1[3,0,10])")


        cList = ROOT.RooArgList()
        for i in range(3,order):
            self.w.factory("c_"+str(i)+"[0.1,0,100]")
            cList.add(self.w.var("c_"+str(i)))
        bernsteinPDF = ROOT.RooBernsteinFast(order)(name+"B",name,self.w.var(poi),cList)
        getattr(self.w,'import')(bernsteinPDF,ROOT.RooFit.Rename(name+"B"))

        self.w.factory("SUM::"+name+"(c_2[0.5,0,1]*"+name+"G,"+name+"B)")



    def expo(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("RooExponential::"+name+"("+poi+",c_0[-1,-1000,0])")


    def gaus(self,name = 'model',poi='x'):
        self.w.factory("RooGaussian::"+name+"("+poi+",c_0[50,0,10000],c_1[30,0,10000])")


    def pow(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[-1,-200,200]")
        power=ROOT.RooPower(name,name,self.w.var(poi),self.w.var("c_0"))
        getattr(self.w,'import')(power,ROOT.RooFit.Rename(name))


    def roopow(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[-1,-20000,20000]")
        power=ROOT.RooPowPdf(name,name,self.w.var(poi),self.w.var("c_0"))
        getattr(self.w,'import')(power,ROOT.RooFit.Rename(name))





    def twoPow(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[-1,-200,200]")
        self.w.factory("c_1[-0.1,-200,200]")
        self.w.factory("c_2[0,1]")

        power=ROOT.RooPower(name+'1',name,self.w.var(poi),self.w.var("c_0"))
        getattr(self.w,'import')(power,ROOT.RooFit.Rename(name+'1'))
        power=ROOT.RooPower(name+'2',name,self.w.var(poi),self.w.var("c_1"))
        getattr(self.w,'import')(power,ROOT.RooFit.Rename(name+'2'))
        self.w.factory("SUM::"+name+"(c_2*"+name+"1,"+name+"2)")
        


    def bifur(self,name = 'model',poi='x'):
        self.w.factory("RooBifurGauss::"+name+"("+poi+",c_0[0,3000],c_1[0,10000],c_2[0,10000])")


    def erfexp(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[-0.01,-1,0]")
        self.w.factory("c_1[45,5,240]")
        self.w.factory("c_2[50,10,10000]")
        erfexp = ROOT.RooErfExpPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))


    def erfexpinv(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[-0.1,-1000,0]")
        self.w.factory("c_1[40,0,100]")
        self.w.factory("c_2[-10,-100000,-0.1]")
        erfexp = ROOT.RooErfExpPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))


    def erfexpCB(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.erfexp(name+'NonRes',poi)
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("mean[80,75,85]")
        self.w.factory("sigma[10,10,30]")
        self.w.factory("alpha1[1]")
        self.w.factory("n1[10,1,100]")
        self.w.factory("alpha2[1]")
        self.w.factory("n2[10,1,100]")

        peak = ROOT.RooDoubleCB(name+'S','modelS',self.w.var('x'),self.w.var('mean'),self.w.var('sigma'),self.w.var('alpha1'),self.w.var('n1'),self.w.var('alpha2'),self.w.var('n2'))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name+'S'))
        self.w.factory("SUM::{name}(fR[0.2,0,1]*{name}NonRes,{name}S)".format(name=name))


    def erfexpTimesCB(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.erfexp(name+'NonRes',poi)
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("mean[80,75,85]")
        self.w.factory("sigma[10,10,30]")
        self.w.factory("alpha1[1]")
        self.w.factory("n1[10,1,100]")
        self.w.factory("alpha2[1]")
        self.w.factory("n2[10,1,100]")

        peak = ROOT.RooDoubleCB(name+'S','modelS',self.w.var('x'),self.w.var('mean'),self.w.var('sigma'),self.w.var('alpha1'),self.w.var('n1'),self.w.var('alpha2'),self.w.var('n2'))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name+'S'))
        self.w.factory("PROD::{name}({name}NonRes,{name}S)".format(name=name))



    def erfexp2Gaus(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[0,-1000,1000]")
        self.w.factory("c_1[20,-30000,30000]")
        self.w.factory("c_2[-10,-1000000,100000]")
        erfexp = ROOT.RooErfExpPdf(name+"Erf",name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))
        self.w.factory("RooGaussian::gaus1("+poi+",mean1[80,60,100],sigma1[10,0,200])")
        self.w.factory("RooGaussian::gaus2("+poi+",mean2[0,200],sigma2[0,200])")
        self.w.factory("SUM::gaus(f[0,1]*gaus1,gaus2)")
        self.w.factory("PROD::"+name+"(gaus,"+name+"Erf)")



    def twoErfexp(self,name = 'model',poi='x'):      
        self.w.factory("c_0[0,-5,5]")
        self.w.factory("c_1[50,0,300]")
        self.w.factory("c_2[20,0,1000]")
        self.w.factory("c_3[0,-5,5]")

        erfexp1 = ROOT.RooErfExpPdf(name+'1',name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp1,ROOT.RooFit.Rename(name))
        erfexp2 = ROOT.RooErfExpPdf(name+'2',name,self.w.var(poi),self.w.var("c_3"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp2,ROOT.RooFit.Rename(name))
        self.w.factory("SUM::"+name+"(c_4[0.5,0,1]*"+name+"1,"+name+"2)")


    def twoExp(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("RooExponential::"+name+"E1("+poi+",c_0[-1,-15,15])")
        self.w.factory("RooExponential::"+name+"E2("+poi+",c_1[0,-15,15])")
        self.w.factory("SUM::"+name+"(c_2[0.5,0,1]*"+name+"E1,"+name+"E2)")

    def twoGaus(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("RooGaussian::"+name+"G1("+poi+",c_0[-200,200],c_1[0,200])")
        self.w.factory("RooGaussian::"+name+"G2("+poi+",c_2[-200,200],c_3[0,200])")
        self.w.factory("SUM::"+name+"(c_4[0.5,0,1]*"+name+"E1,"+name+"E2)")


    def doubleCB(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[0.1,-1000,2000]")
        self.w.factory("c_1[5,0,4000]")
        self.w.factory("c_2[2,1,20]")
        self.w.factory("c_3[2,0,20]")
        self.w.factory("c_4[2,1,20]")
        self.w.factory("c_5[2,0,20]")

        doubleCB = ROOT.RooDoubleCB(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"),self.w.var("c_3"),self.w.var("c_4"),self.w.var("c_5"))
        getattr(self.w,'import')(doubleCB,ROOT.RooFit.Rename(name))



    def upperCB(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[0.0]")
        self.w.factory("c_1[5,0,100]")
        self.w.factory("c_2[1]")
        self.w.factory("c_3[5]")
        self.w.factory("c_4[2,0.1,5]")
        self.w.factory("c_5[5]")

        doubleCB = ROOT.RooDoubleCB(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"),self.w.var("c_3"),self.w.var("c_4"),self.w.var("c_5"))
        getattr(self.w,'import')(doubleCB,ROOT.RooFit.Rename(name))



    def inversePol(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[-1e+90,1e+90]")
        self.w.factory("c_1[-1e+90,1e+90]")
        self.w.factory("c_2[-1e+90,1e+90]")
        self.w.factory("c_3[-1e+90,1e+90]")


        softDrop = ROOT.RooInversePolPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"),self.w.var("c_3"))
        getattr(self.w,'import')(softDrop,ROOT.RooFit.Rename(name))



    def jetResonanceNOEXP2D(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("mean0[80,50,300]")
        self.w.factory("mean1[0,-1,1]")
        self.w.factory("expr::mean('mean0+mean1*M',mean0,mean1,M)")
        self.w.factory("sigma0[10,0,100]")
        self.w.factory("sigma1[0,-0.1,0.1]")
        self.w.factory("sigma2[0]")
        self.w.factory("expr::sigma('sigma0+sigma1*M+sigma2*M*M',sigma0,sigma1,sigma2,M)")
        self.w.factory("alpha[3,0.5,5]")
        self.w.factory("n[6]")
        self.w.factory("alpha2[1.5,0.5,5]")
        self.w.factory("n2[6]")

        peak = ROOT.RooDoubleCB(name,'modelS',self.w.var(poi),self.w.function('mean'),self.w.function('sigma'),self.w.var('alpha'),self.w.var('n'),self.w.var("alpha2"),self.w.var("n2"))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name))

    def jetResonance(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("mean[80,50,200]")
        self.w.factory("sigma[10,2,40]")
        self.w.factory("alpha[3,0.5,10]")
        self.w.factory("n[2]")
        self.w.factory("alpha2[3,0.5,10]")
        self.w.factory("n2[2]")

        peak = ROOT.RooDoubleCB(name+'S','modelS',self.w.var(poi),self.w.var('mean'),self.w.var('sigma'),self.w.var('alpha'),self.w.var('n'),self.w.var("alpha2"),self.w.var("n2"))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name+'S'))
        self.w.factory("RooExponential::"+name+"B("+poi+",slope[-1,-10,0])")       
        self.w.factory("SUM::"+name+"(f[0.8,0,1]*"+name+"S,"+name+"B)")

    def jetResonanceNOEXP(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("mean[80,50,200]")
        self.w.factory("sigma[10,3,40]")
        self.w.factory("alpha[1,0.5,10]")
        self.w.factory("n[2]")
        self.w.factory("alpha2[1,0.5,10]")
        self.w.factory("n2[2]")
        self.w.factory("slope[0.0]")
        self.w.factory("f[0.0]")

        peak = ROOT.RooDoubleCB(name,'modelS',self.w.var(poi),self.w.var('mean'),self.w.var('sigma'),self.w.var('alpha'),self.w.var('n'),self.w.var("alpha2"),self.w.var("n2"))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name))

    def jetResonance2(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("mean[174,50,300]")
        self.w.factory("sigma[15,5,30]")
        self.w.factory("alpha[1,0.2,3]")
        self.w.factory("n[6]")
        self.w.factory("alpha2[1]")
        self.w.factory("n2[6]")

        peak = ROOT.RooDoubleCB(name,'modelS',self.w.var(poi),self.w.var('mean'),self.w.var('sigma'),self.w.var('alpha'),self.w.var('n'),self.w.var("alpha2"),self.w.var("n2"))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name+'S'))



    def jetDoublePeak(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        
        self.w.factory("meanW[80,75,85]")
        self.w.factory("sigmaW[10,7.5,20]")
        self.w.factory("alphaW[1,0.1,10]")
        self.w.factory("alphaW2[1,0.1,10]")
        self.w.factory("n1[5,1,20]")
        self.w.factory("n2[5,1,20]")

        self.w.factory("meanTop[160,140,190]")
        self.w.factory("sigmaTop[30,12,100]")
        self.w.factory("alphaTop[3,0.1,10]")
        self.w.factory("alphaTop2[3,0.1,10]")
        self.w.factory("n3[5,1,20]")
        self.w.factory("n4[5,1,20]")

        peak = ROOT.RooDoubleCB('WPeak','modelS',self.w.var(poi),self.w.var('meanW'),self.w.var('sigmaW'),self.w.var('alphaW'),self.w.var('n1'),self.w.var("alphaW2"),self.w.var("n2"))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename('WPeak'))
        peak2 = ROOT.RooDoubleCB('TopPeak','modelS',self.w.var(poi),self.w.var('meanTop'),self.w.var('sigmaTop'),self.w.var('alphaTop'),self.w.var('n3'),self.w.var("alphaTop2"),self.w.var("n4"))
        getattr(self.w,'import')(peak2,ROOT.RooFit.Rename('TopPeak'))
        self.w.factory("SUM::"+name+"(f[0.5,0,1]*WPeak,TopPeak)")


    def jetDoublePeakExp(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.jetDoublePeak('modelS',poi)
        self.w.factory("RooExponential::modelB("+poi+",slope[0,-3,3])")
        self.w.factory("SUM::"+name+"(f2[0.5,0,1]*modelS,modelB)")


    def jetDoublePeakExpCond(self,name,poi,scale={},resolution={},fraction={}):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
               
        scaleStr='0'
        resolutionStr='0'
        fractionStr='0'
        scaleSysts=[]
        resolutionSysts=[]
        fractionSysts=[]
        for syst,factor in scale.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            scaleStr=scaleStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            scaleSysts.append(syst)
            self.w.var(syst).setVal(0.0)
            self.w.var(syst).setConstant(1)
        for syst,factor in resolution.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            resolutionStr=resolutionStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            resolutionSysts.append(syst)
            self.w.var(syst).setVal(0.0)
            self.w.var(syst).setConstant(1)
        for syst,factor in fraction.iteritems():
            self.w.factory(syst+"[0,-50,50]")
            fractionStr=fractionStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            fractionSysts.append(syst)
            self.w.var(syst).setVal(0.0)
            self.w.var(syst).setConstant(1)

        self.w.factory("meanW0[80,75,85]")
        self.w.factory("expr::meanW('(meanW0+0*{x})*(1+{vv_syst})',meanW0,{x},{vv_systs})".format(x=poi[0],vv_syst=scaleStr,vv_systs=','.join(scaleSysts)))
        self.w.factory("sigmaW0[12,7.5,20]")
        self.w.factory("expr::sigmaW('(sigmaW0+0*{x})*(1+{vv_syst})',sigmaW0,{x},{vv_systs})".format(x=poi[0],vv_syst=resolutionStr,vv_systs=','.join(resolutionSysts)))
        self.w.factory("alphaW0[1,0.1,10]")
        self.w.factory("expr::alphaW('(alphaW0+0*{x})',alphaW0,{x})".format(x=poi[0]))
        self.w.factory("alpha2W0[1,0.1,10]")
        self.w.factory("expr::alpha2W('(alpha2W0+0*{x})',alpha2W0,{x})".format(x=poi[0]))
        self.w.factory("n[5]")

        self.w.factory("meanTop0[160,100,250]")
        self.w.factory("meanTop1[0,-500000,500000]")
        self.w.factory("meanTop2[0,-300000000,300000000]")
        self.w.factory("expr::meanTop('(meanTop0+meanTop1/{x}+meanTop2/({x}*{x}))*(1+{vv_syst})',meanTop0,meanTop1,meanTop2,{x},{vv_systs})".format(x=poi[0],vv_syst=scaleStr,vv_systs=','.join(scaleSysts)))
        self.w.factory("sigmaTop0[25,2,100]")
        self.w.factory("expr::sigmaTop('(sigmaTop0+0*{x})*(1+{vv_syst})',sigmaTop0,{x},{vv_systs})".format(x=poi[0],vv_syst=resolutionStr,vv_systs=','.join(resolutionSysts)))
        self.w.factory("alphaTop0[1,0.1,10]")
        self.w.factory("expr::alphaTop('(alphaTop0+0*{x})',alphaTop0,{x})".format(x=poi[0]))
        self.w.factory("alpha2Top0[1,0.1,10]")
        self.w.factory("expr::alpha2Top('(alpha2Top0+0*{x})',alpha2Top0,{x})".format(x=poi[0]))

        peak = ROOT.RooDoubleCB('WPeak','modelS',self.w.var(poi[1]),self.w.function('meanW'),self.w.function('sigmaW'),self.w.function('alphaW'),self.w.var('n'),self.w.function("alpha2W"),self.w.var("n"))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename('WPeak'))
        peak2 = ROOT.RooDoubleCB('TopPeak','modelS',self.w.var(poi[1]),self.w.function('meanTop'),self.w.function('sigmaTop'),self.w.function('alphaTop'),self.w.var('n'),self.w.function("alpha2Top"),self.w.var("n"))
        getattr(self.w,'import')(peak2,ROOT.RooFit.Rename('TopPeak'))

        self.w.factory("f0[0.6,0,1]")
        self.w.factory("f2[200000,0,300000000]")
        self.w.factory("expr::f('(f0+f2/({x}*{x}))+({vv_syst})*min((f0+f2/({x}*{x})),(1-(f0+f2/({x}*{x}))))',f0,f2,{x},{vv_systs})".format(x=poi[0],vv_syst=fractionStr,vv_systs=','.join(fractionSysts)))

        self.w.factory("SUM::modelS(f*WPeak,TopPeak)")
        self.w.factory("RooExponential::modelB("+poi[1]+",slope[0,-5,5])")
        self.w.factory("SUM::"+name+"(g[0.99,0,1]*modelS,modelB)")


    def jetPeakCond(self,name,poi,p,scale={},resolution={}):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        scaleStr='0'
        resolutionStr='0'
        scaleSysts=[]
        resolutionSysts=[]
        for syst,factor in scale.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            scaleStr=scaleStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            scaleSysts.append(syst)
            self.w.var(syst).setVal(0.0)
            self.w.var(syst).setConstant(1)
        for syst,factor in resolution.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            resolutionStr=resolutionStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            resolutionSysts.append(syst)
            self.w.var(syst).setVal(0.0)
            self.w.var(syst).setConstant(1)

        self.w.factory("n[5]")
        if p=="W":
            self.w.factory("mean"+p+"0[85,60,100]")
        elif p=="Top":
            self.w.factory("mean"+p+"0[170,140,200]")
        else:
            print "peak", p, "not supported" 
        self.w.factory("mean"+p+"1[0,-500000,500000]")
        self.w.factory("mean"+p+"2[0,-300000000,300000000]")
        self.w.factory(("expr::mean"+p+"('(mean"+p+"0+mean"+p+"1/{x}+mean"+p+"2/({x}*{x}))*(1+{vv_syst})',mean"+p+"0,mean"+p+"1,mean"+p+"2,{x},{vv_systs})").format(x=poi[0],vv_syst=scaleStr,vv_systs=','.join(scaleSysts)))
        if p=="W":
            self.w.factory("sigma"+p+"0[8,2,50]")
        elif p=="Top":
            self.w.factory("sigma"+p+"0[15,2,50]")
        else:
            print "peak", p, "not supported" 
        self.w.factory(("expr::sigma"+p+"('(sigma"+p+"0+0*{x})*(1+{vv_syst})',sigma"+p+"0,{x},{vv_systs})").format(x=poi[0],vv_syst=resolutionStr,vv_systs=','.join(resolutionSysts)))
        self.w.factory("alpha"+p+"0[1.5,0.1,10]")
        self.w.factory(("expr::alpha"+p+"('(alpha"+p+"0+0*{x})',alpha"+p+"0,{x})").format(x=poi[0]))
        self.w.factory("alpha2"+p+"0[1.5,0.1,10]")
        self.w.factory(("expr::alpha2"+p+"('(alpha2"+p+"0+0*{x})',alpha2"+p+"0,{x})").format(x=poi[0]))

        peak = ROOT.RooDoubleCB(name,p+'Peak',self.w.var(poi[1]),self.w.function('mean'+p),self.w.function('sigma'+p),self.w.function('alpha'+p),self.w.var('n'),self.w.function('alpha2'+p),self.w.var('n'))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name))



    def jetResonanceCB2(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("mean[80,50,100]")
        self.w.factory("sigma[10,0,100]")
        self.w.factory("alpha[3,0.5,6]")
        self.w.factory("n[6]")
        self.w.factory("alpha2[3,0.5,6]")
        self.w.factory("n2[6]")

        peak = ROOT.RooDoubleCB(name+'S','modelS',self.w.var(poi),self.w.var('mean'),self.w.var('sigma'),self.w.var('alpha'),self.w.var('n'),self.w.var("alpha2"),self.w.var("n2"))
        getattr(self.w,'import')(peak,ROOT.RooFit.Rename(name+'S'))
        self.w.factory("RooExponential::"+name+"B("+poi+",slope[-1,-10,0])")       
        self.w.factory("SUM::"+name+"(f[0.8,0,1]*"+name+"S,"+name+"B)")




    def signalResonance(self,name = 'model',poi="MVV",singleSided=False):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("MH[1000]")
        self.w.factory("MEAN[400,13000]")
        self.w.factory("SIGMA[100,1,5000]")
        self.w.factory("ALPHA1[1,0.5,3]")
        self.w.factory("N1[5]")
        if singleSided:
            self.w.factory("ALPHA2[1000000.0]")
            self.w.factory("N2[0]")
        else:
            self.w.factory("ALPHA2[1,0.5,3]")
            self.w.factory("N2[5]")
        peak_vv = ROOT.RooDoubleCB(name,'modelS',self.w.var(poi),self.w.var('MEAN'),self.w.function('SIGMA'),self.w.var('ALPHA1'),self.w.var('N1'),self.w.var('ALPHA2'),self.w.var('N2'))
        getattr(self.w,'import')(peak_vv,ROOT.RooFit.Rename(name))


    def signal2D(self,name,poi):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("MH[1000]")
        self.w.factory("MEAN[400,8000]")
        self.w.factory("SIGMA[100,0,1000]")
        self.w.factory("ALPHA1[1,0.5,5]")
        self.w.factory("N1[5]")
        self.w.factory("ALPHA2[1,0.5,5]")
        self.w.factory("N2[5]")

        peak_vv = ROOT.RooDoubleCB(name+"MVV",'modelMVV',self.w.var(poi[0]),self.w.var('MEAN'),self.w.function('SIGMA'),self.w.var('ALPHA1'),self.w.var('N1'),self.w.var("ALPHA2"),self.w.var("N2"))
        getattr(self.w,'import')(peak_vv,ROOT.RooFit.Rename(name+"MVV"))

        self.w.factory("mean[80,40,300]")
        self.w.factory("sigma[10,1,30]")
        self.w.factory("alpha[0.5,5]")
        self.w.factory("n[6]")

        peak_jj = ROOT.RooCBShape(name+"MJJ1",'modelMJJ',self.w.var(poi[1]),self.w.var('mean'),self.w.function('sigma'),self.w.var('alpha'),self.w.var('n'))
        getattr(self.w,'import')(peak_jj,ROOT.RooFit.Rename(name+"MJJ1"))
        self.w.factory("RooExponential::"+name+'MJJ2('+poi[1]+',slope[-1,-2,2])')
        self.w.factory("SUM::"+name+'MJJ(f[0.9,0,1]*'+name+'MJJ1,'+name+'MJJ2)')
        self.w.factory("PROD::"+name+"("+name+"MJJ,"+name+"MVV)")



    def signalMJJ(self,name,poi):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[80,40,300]")
        self.w.factory("c_1[10,1,30]")
        self.w.factory("c_2[0.5,5]")
        self.w.factory("c_3[6]")
        peak_jj = ROOT.RooCBShape(name+"MJJ1",'modelMJJ',self.w.var(poi),self.w.var('c_0'),self.w.function('c_1'),self.w.var('c_2'),self.w.var('c_3'))
        getattr(self.w,'import')(peak_jj,ROOT.RooFit.Rename(name+"MJJ1"))
        self.w.factory("RooExponential::"+name+'MJJ2('+poi+',c_4[-1,-2,2])')
        self.w.factory("SUM::"+name+'(c_5[0.9,0,1]*'+name+'MJJ1,'+name+'MJJ2)')


    def signalMJJCB(self,name,poi):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[80,40,300]")
        self.w.factory("c_1[10,1,30]")
        self.w.factory("c_2[0.5,5]")
        self.w.factory("c_3[6]")
        self.w.factory("c_4[0.5,5]")
        self.w.factory("c_5[6]")
        peak_jj = ROOT.RooDoubleCB(name,'modelMJJ',self.w.var(poi),self.w.var('c_0'),self.w.function('c_1'),self.w.var('c_2'),self.w.var('c_3'),self.w.var("c_4"),self.w.var("c_5"))
        getattr(self.w,'import')(peak_jj,ROOT.RooFit.Rename(name))


    def signalMJJCBBoth(self,name,poi):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[80,70,90]")
        self.w.factory("c_1[10,1,30]")
        self.w.factory("c_2[0.5,5]")
        self.w.factory("c_3[6]")
        self.w.factory("c_4[0.5,5]")
        self.w.factory("c_5[6]")
        self.w.factory("c_6[170,150,190]")
        self.w.factory("c_7[30,1,100]")
        self.w.factory("c_8[0.5,5]")
        self.w.factory("c_9[6]")
        self.w.factory("c_10[0.5,5]")
        self.w.factory("c_11[6]")
        self.w.factory("c_12[0.5,0,1]")


        peak_jj = ROOT.RooDoubleCB(name+"W",'modelMJJ',self.w.var(poi),self.w.var('c_0'),self.w.function('c_1'),self.w.var('c_2'),self.w.var('c_3'),self.w.var("c_4"),self.w.var("c_5"))
        peak_jj2 = ROOT.RooDoubleCB(name+"top",'modelMJJ',self.w.var(poi),self.w.var('c_6'),self.w.function('c_7'),self.w.var('c_8'),self.w.var('c_9'),self.w.var("c_10"),self.w.var("c_11"))
        getattr(self.w,'import')(peak_jj,ROOT.RooFit.Rename(name+"W"))
        getattr(self.w,'import')(peak_jj2,ROOT.RooFit.Rename(name+"top"))
        self.w.factory("SUM::{name}(c_12*{name}W,{name}top)".format(name=name))





    def signalMJJPara(self,name,poi):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("mean0[80,50,100]")
        self.w.factory("mean1[0,-0.005,0.005]")
        self.w.factory("mean2[0,-2e-5,2e-5]")
        self.w.factory("mean3[0]")
        self.w.factory("mean4[0]")

        self.w.factory("expr::mean('(mean0+mean1*{x}+mean2*{x}*{x}+mean3*{x}*{x}*{x}+mean4*{x}*{x}*{x}*{x})',mean0,mean1,mean2,mean3,mean4,{x})".format(x=poi[1]))

        self.w.factory("sigma0[10,0,20]")
        self.w.factory("sigma1[0,-0.002,0.002]")
        self.w.factory("sigma2[0,-2e-5,2e-5]")
        self.w.factory("sigma3[0]")
        self.w.factory("sigma4[0]")
        self.w.factory("expr::sigma('(sigma0+sigma1*{x}+sigma2*{x}*{x}+sigma3*{x}*{x}*{x}+sigma4*{x}*{x}*{x}*{x})',sigma0,sigma1,sigma2,sigma3,sigma4,{x})".format(x=poi[1]))

        self.w.factory("alpha10[3,0.5,10]")
        self.w.factory("alpha11[0.0,-0.002,0.002]")
        self.w.factory("alpha12[0.0,-5e-5,5e-5]")
        self.w.factory("alpha13[0.0]")
        self.w.factory("alpha14[0.0]")
        self.w.factory("expr::alpha1('(alpha10+alpha11*{x}+alpha12*{x}*{x}+alpha13*{x}*{x}*{x}+alpha14*{x}*{x}*{x}*{x})',alpha10,alpha11,alpha12,alpha13,alpha14,{x})".format(x=poi[1]))
        self.w.factory("alpha20[3,0.5,10]")
        self.w.factory("alpha21[0.0,-0.002,0.002]")
        self.w.factory("alpha22[0.0,-2e-5,2e-5]")
        self.w.factory("alpha23[0.0]")
        self.w.factory("alpha24[0.0]")
        self.w.factory("expr::alpha2('(alpha20+alpha21*{x}+alpha22*{x}*{x}+alpha23*{x}*{x}*{x}+alpha24*{x}*{x}*{x}*{x})',alpha20,alpha21,alpha22,alpha23,alpha24,{x})".format(x=poi[1]))

        self.w.factory("n1[6]")
        self.w.factory("n2[6]")


        self.w.factory("slope0[0.0,-1,1]")
        self.w.factory("slope1[0,-0.0005,0.0005]")
        self.w.factory("slope2[0,-2e-5,23-5]")
        self.w.factory("slope3[0]")
        self.w.factory("slope4[0]")
        self.w.factory("expr::slope('(slope0+slope1*{x}+slope2*{x}*{x}+slope3*{x}*{x}*{x}+slope4*{x}*{x}*{x}*{x})',slope0,slope1,slope2,slope3,slope4,{x})".format(x=poi[1]))

        self.w.factory("f0[0.8,0,1]")
        self.w.factory("f1[0,-0.0003,0.0003]")
        self.w.factory("f2[0,-2e-5,2e-5]")
        self.w.factory("f3[0]")
        self.w.factory("f4[0]")
        self.w.factory("expr::f('(f0+f1*{x}+f2*{x}*{x}+f3*{x}*{x}*{x}+f4*{x}*{x}*{x}*{x})',f0,f1,f2,f3,f4,{x})".format(x=poi[1]))


#        peak_jj = ROOT.RooDoubleCB(name+"MJJ1",'modelMJJ',self.w.var(poi[0]),self.w.function('mean'),self.w.function('sigma'),self.w.function('alpha1'),self.w.var('n1'),self.w.function('alpha2'),self.w.var('n2'))
        peak_jj = ROOT.RooDoubleCB(name,'modelMJJ',self.w.var(poi[0]),self.w.function('mean'),self.w.function('sigma'),self.w.function('alpha1'),self.w.var('n1'),self.w.function('alpha2'),self.w.var('n2'))
        getattr(self.w,'import')(peak_jj,ROOT.RooFit.Rename(name+"MJJ1"))
#        self.w.factory("RooExponential::"+name+'MJJ2('+poi[0]+',slope)')
#        self.w.factory("SUM::"+name+'(f*'+name+'MJJ1,'+name+'MJJ2)')


    def doublePol(self,name = 'model',poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[0,-1,1]")
        self.w.factory("c_1[0,-100,100]")
        self.w.factory("c_2[0,-1000,1000]")
        self.w.factory("c_3[0]")

        softDrop = ROOT.RooDoublePolPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"),self.w.var("c_3"))
        getattr(self.w,'import')(softDrop,ROOT.RooFit.Rename(name))



    def softDrop2D(self):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("M[1000,20000]")
        self.w.factory("m[3,203]")


        self.w.factory("scale_a[50,0,100]")
        self.w.factory("scale_b[-1250,-10000,0]")
        self.w.factory("expr::scale('scale_a+scale_b*M/13000.0',scale_a,scale_b,M)")

        self.w.factory("offset[160,0,2000]")

        self.w.factory("alpha[0.005,0,10]")

        self.w.factory("beta_f[2.5,0,100]")
        self.w.factory("expr::beta('-alpha+beta_f*M/13000.0',alpha,beta_f,M)")


        self.w.factory("gamma[0.1,0,1]")


        softDrop = ROOT.RooFatJetFallingPdf("modelJJ","",self.w.var("m"),self.w.function("scale"),self.w.var("offset"),self.w.var("alpha"),self.w.function("beta"),self.w.var("gamma"))
        getattr(self.w,'import')(softDrop,ROOT.RooFit.Rename("modelJJ"))

        self.w.factory("p0[1,0,100]")
        self.w.factory("p1[2,0,100]")
        self.w.factory("p2[0]")

        qcd = ROOT.RooQCDPdf("modelQ","",self.w.var("M"),self.w.var("p0"),self.w.var("p1"),self.w.var("p2"))
        getattr(self.w,'import')(qcd,ROOT.RooFit.Rename("modelQ"))

        self.w.factory("PROD::model(modelJJ|M,modelQ)")



    def bifurTimesQCD(self):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("M[1000,200000]")
        self.w.factory("m[25,165]")



        self.w.factory("alpha_0[-35.661,-40,-30]")
        self.w.factory("alpha_1[15.882,10,35]")
        self.w.factory("expr::alpha('alpha_0+alpha_1*log(M)',alpha_0,alpha_1,M)")

        self.w.factory("beta_0[19.5,0,35]")
        self.w.factory("beta_1[0.0101766,0,0.05]")
        self.w.factory("expr::beta('beta_0+beta_1*M',beta_0,beta_1,M)")       

        self.w.factory("gamma[62.6,40,80]")

        self.w.factory("RooBifurGauss::modelJJ(m,alpha,beta,gamma)")


        self.w.factory("p0[33,0,100]")
        self.w.factory("p1[0.5,0,10]")
        self.w.factory("p2[0.001,0,10]")

        qcd = ROOT.RooQCDPdf("modelQ","",self.w.var("M"),self.w.var("p0"),self.w.var("p1"),self.w.var("p2"))
        getattr(self.w,'import')(qcd,ROOT.RooFit.Rename("modelQ"))
        self.w.factory("PROD::model(modelJJ|M,modelQ)")

    def expoTimesQCD(self):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("M[1000,200000]")
        self.w.factory("m[25,165]")



        self.w.factory("alpha_0[-35.661,-40,-30]")
        self.w.factory("alpha_1[15.882,10,35]")
        self.w.factory("expr::alpha('alpha_0+alpha_1*(M)',alpha_0,alpha_1,M)")

        self.w.factory("RooExponential::modelJJ(m,alpha)")


        self.w.factory("p0[33,0,100]")
        self.w.factory("p1[0.5,0,10]")
        self.w.factory("p2[0.001,0,10]")

        qcd = ROOT.RooQCDPdf("modelQ","",self.w.var("M"),self.w.var("p0"),self.w.var("p1"),self.w.var("p2"))
        getattr(self.w,'import')(qcd,ROOT.RooFit.Rename("modelQ"))
        self.w.factory("PROD::model(modelJJ|M,modelQ)")




    def backgroundFast(self):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("M[1000,20000]")
        self.w.factory("m[25,175]")



        self.w.factory("alpha_0[7,0,100]")
        self.w.factory("alpha_1[0,-0.1,0.1]")
        self.w.factory("expr::alpha('alpha_0+alpha_1*M',alpha_0,alpha_1,M)")

        self.w.factory("beta_0[6,0,100]")
        self.w.factory("beta_1[0,-0.1,0.1]")
        self.w.factory("expr::beta('beta_0+beta_1*M',beta_0,beta_1,M)")       

        self.w.factory("gamma_0[1,0,100]")
        self.w.factory("gamma_1[0,-0.1,0.1]")
        self.w.factory("expr::gamma('gamma_0+gamma_1*M',gamma_0,gamma_1,M)")       
        self.w.factory("delta[1.4,0,1000]")


        cList = ROOT.RooArgList()
        cList.add(self.w.function("alpha"))
        cList.add(self.w.function("beta"))
        cList.add(self.w.function("gamma"))
        cList.add(self.w.var("delta"))


        softDrop = ROOT.RooBernsteinFast(4)("modelJJ","modelJJ",self.w.var('m'),cList)
        getattr(self.w,'import')(softDrop,ROOT.RooFit.Rename("modelJJ"))
        self.w.factory("p0[20,0,100]")
        self.w.factory("p1[0.5,0,100]")
        self.w.factory("p2[0.0001,0,10]")

        qcd = ROOT.RooQCDPdf("modelQ","",self.w.var("M"),self.w.var("p0"),self.w.var("p1"),self.w.var("p2"))
        getattr(self.w,'import')(qcd,ROOT.RooFit.Rename("modelQ"))

        self.w.factory("PROD::model(modelJJ|M,modelQ)")


    def qcd(self,name='model',poi='MVV',logTerm=True):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

        self.w.factory("c_0[20,0,100]")
        self.w.factory("c_1[0.5,0,100]")
        if logTerm:
            self.w.factory("c_2[0.0001,0,10]")
        else:    
            self.w.factory("c_2[0]")

        qcd = ROOT.RooQCDPdf(name,"",self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(qcd,ROOT.RooFit.Rename("model"))


    def qcdINT(self,poi='x'):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("p0[0,100]")
        self.w.factory("p1[0,100]")
        qcd = ROOT.RooDiBosonQCDPdf(13)("model","",self.w.var(poi),self.w.var("p0"),self.w.var("p1"))
        getattr(self.w,'import')(qcd,ROOT.RooFit.Rename("model"))



    def erfpowPlusGaus(self,name = 'model',poi='x'):      
        self.w.factory("RooGaussian:modelG(x,c_0[0.0001,-5000,40],c_1[20,0,100])")
        self.w.factory("c_2[-2,-20,0]")
        self.w.factory("expr::xdisp('x-c_2',x,c_2)")
        self.w.factory("c_3[-1,-20,0]")
        self.w.factory("c_4[30,-1000,1000]")
        self.w.factory("c_5[11,-10000,10000]")      


        erfexp = ROOT.RooErfPowPdf(name+"F",name,self.w.function('xdisp'),self.w.var("c_3"),self.w.var("c_4"),self.w.var("c_5"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))
        self.w.factory("SUM::"+name+"(c_6[0.5,0.,1]*modelG,modelF)")



    def erfpow(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[-4.6,-9.0,0.0]")
        self.w.factory("c_1[600,500,20000]")
        self.w.factory("c_2[500,100,10000]")      
        erfexp = ROOT.RooErfPowPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))


    def tsallis(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[-4.6,-9.0,0.0]")
        self.w.factory("c_1[600,500,20000]")
        self.w.factory("c_2[500,100,10000]")      
        erfexp = ROOT.RooErfPowPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))


    def erfpowinv(self,name = 'model',poi='x'):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c_0[-4.6,-9.0,0.0]")
        self.w.factory("c_1[40,50,200]")
        self.w.factory("c_2[-5,-1000,-0.1]")      
        erfexp = ROOT.RooErfPowPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))



    def erfpowParam(self,name = 'model',poi=['x','X']):      
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        self.w.factory("c0[-4.6,-9.0,0.0]")
        self.w.factory("c1_0[1000,500,20000]")
        self.w.factory("c1_1[-1,-500,500]")
        self.w.factory("c1_2[0,-5,5]")
        self.w.factory("c1_3[0,-0.01,0.01]")
        self.w.factory("expr::c1('c1_0+c1_1*{x}+c1_2*{x}*{x}+c1_3*{x}*{x}*{x}',c1_0,c1_1,c1_2,c1_3,{x})".format(x=poi[1]))

        self.w.factory("c2_0[1000,500,20000]")
        self.w.factory("c2_1[-1,-500,500]")
        self.w.factory("c2_2[0,-1,1]")
        self.w.factory("expr::c2('c2_0+c2_1*{x}+c2_2*{x}*{x}',c2_0,c2_1,c2_2,{x})".format(x=poi[1]))

        erfexp = ROOT.RooErfPowPdf(name,name,self.w.var(poi[0]),self.w.var("c0"),self.w.function("c1"),self.w.function("c2"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))



    def erfpow2(self,name = 'model',poi='x'):      
        self.w.factory("c_0[10,0,200]")
        self.w.factory("c_1[10,-200,200]")
        self.w.factory("c_2[800,400,10000]")
        self.w.factory("c_3[1000,-10000,10000]")      
        erfexp = ROOT.RooErfPow2Pdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"),self.w.var("c_3"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))

    def erfpowexp(self,name = 'model',poi='x'):      
        self.w.factory("c_0[0,-20,0]")
        self.w.factory("c_1[0,-20,0]")
        self.w.factory("c_2[800,-10000,10000]")
        self.w.factory("c_3[1000,-10000,10000]")      
        erfexp = ROOT.RooErfPowExpPdf(name,name,self.w.var(poi),self.w.var("c_0"),self.w.var("c_1"),self.w.var("c_2"),self.w.var("c_3"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))



    def erfpowPlusGausLOG(self,name = 'model',poi='x'):      
        self.w.factory("RooGaussian:modelG(x,c_0[0.0001,-5000,40],c_1[20,0,100])")
        self.w.factory("c_2[0,-20,20]")
        self.w.factory("expr::xdisp('x-c_2',x,c_2)")
        self.w.factory("c_3[2,0,20]")
        self.w.factory("c_4[30,-100,100]")
        self.w.factory("c_5[11,-1000,1000]")      


        erfexp = ROOT.RooErfPowPdf(name+"F",name,self.w.function('xdisp'),self.w.var("c_3"),self.w.var("c_4"),self.w.var("c_5"))
        getattr(self.w,'import')(erfexp,ROOT.RooFit.Rename(name))
        self.w.factory("SUM::"+name+"(c_6[0.5,0,1]*modelG,modelF)")




        
    def importBinnedData(self,histogram,poi = ["x"],name = "data"):
        cList = ROOT.RooArgList()
        for i,p in enumerate(poi):
            cList.add(self.w.var(p))
            if i==0:
                axis=histogram.GetXaxis()
            elif i==1:
                axis=histogram.GetYaxis()
            elif i==2:
                axis=histogram.GetZaxis()
            else:
                print 'Asking for more than 3 D . ROOT doesnt support that, use unbinned data instead'
                return
            mini=axis.GetXmin()
            maxi=axis.GetXmax()
            bins=axis.GetNbins()
            self.w.var(p).setMin(mini)
            self.w.var(p).setMax(maxi)
            self.w.var(p).setBins(bins)
        dataHist=ROOT.RooDataHist(name,name,cList,histogram)
        getattr(self.w,'import')(dataHist,ROOT.RooFit.Rename(name))



    def importUnbinnedData(self,tree,name,variables,poi,accept):
        cList = ROOT.RooArgSet()
        for i,p in enumerate(poi):
            cList.add(self.w.var(p))
        
        data=ROOT.RooDataSet(name,name,cList)

        for event in tree:
            if not accept(event):
                continue
            for i,p in enumerate(poi):
                val =  getattr(event,variables[i])
                cList.find(p).setVal(val[0])

            data.add(cList)


        getattr(self.w,'import')(data,ROOT.RooFit.Rename(name))
            



    def fit(self,model = "model",data="data",options=[]):
        if len(options)==0:
            self.w.pdf(model).fitTo(self.w.data("data"))
        if len(options)==1:
            self.w.pdf(model).fitTo(self.w.data("data"),options[0])
        if len(options)==2:
            self.w.pdf(model).fitTo(self.w.data("data"),options[0],options[1])
        if len(options)==3:
            self.w.pdf(model).fitTo(self.w.data("data"),options[0],options[1],options[2])
        if len(options)==4:
            self.w.pdf(model).fitTo(self.w.data("data"),options[0],options[1],options[2],options[3])


    def fetch(self,var):
        return (self.w.var(var).getVal(), self.w.var(var).getError())

    def projection(self,model = "model",data="data",poi="x",filename="fit.root",xtitle='x',plotOptionData=[],plotOptionModel=[]):
        self.frame=self.w.var(poi).frame()
        if data!="":
            if len(plotOptionData)==0:
                self.w.data(data).plotOn(self.frame)
            if len(plotOptionData)==1:
                self.w.data(data).plotOn(self.frame,plotOptionData[0])
            if len(plotOptionData)==2:
                self.w.data(data).plotOn(self.frame,plotOptionData[0],plotOptionData[1])
        if len(plotOptionModel)==0:
            self.w.pdf(model).plotOn(self.frame)
        if len(plotOptionModel)==1:
            self.w.pdf(model).plotOn(self.frame,plotOptionModel[0])
        if len(plotOptionModel)==2:
            self.w.pdf(model).plotOn(self.frame,plotOptionModel[0],plotOptionModel[1])
        if len(plotOptionModel)==3:
            self.w.pdf(model).plotOn(self.frame,plotOptionModel[0],plotOptionModel[1],plotOptionModel[2])
        self.c=ROOT.TCanvas("c","c")
        self.c.cd()
        self.frame.Draw()
        self.frame.GetYaxis().SetTitle('')
        self.frame.GetXaxis().SetTitle(xtitle)
        self.frame.SetTitle('')
        self.c.Draw()
        self.c.SaveAs(filename)
        pullDist = self.frame.pullHist()
        return self.frame.chiSquare()


    def projectionCond(self,model = "model",data="data",poi="y",otherpoi="x",filename="fit.root"):
        
        self.frame=self.w.var(poi).frame()
        self.w.data(data).plotOn(self.frame)
        self.w.pdf(model).plotOn(self.frame,ROOT.RooFit.ProjWData(ROOT.RooArgSet(self.w.var(otherpoi)),self.w.data(data)))
        self.c=ROOT.TCanvas("c","c")
        self.c.cd()
        self.frame.Draw()
        self.c.SaveAs(filename)
        return self.frame.chiSquare()
        
        

    def plotCoef(self,funcname,poi,filename="coef.root",xtitle='x',plotOption=[]):
        self.frame=self.w.var(poi).frame()
        if len(plotOption)==0:
            self.w.function(funcname).plotOn(self.frame)
        if len(plotOption)==1:
            self.w.function(funcname).plotOn(self.frame,plotOption[0])
        if len(plotOption)==2:
            self.w.function(funcname).plotOn(self.frame,plotOption[0],plotOption[1])
        self.c=ROOT.TCanvas("c","c")
        self.c.cd()
        self.frame.Draw()
        self.frame.GetYaxis().SetTitle(funcname)
        self.frame.GetXaxis().SetTitle(xtitle)
        self.frame.SetMinimum(0.)
        self.frame.SetTitle('')
        self.c.Draw()
        self.c.SaveAs(filename)

