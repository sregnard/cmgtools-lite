import ROOT
import copy
from ROOT import gStyle,gROOT,gPad
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *


def convertToPoisson(h):
    graph = ROOT.TGraphAsymmErrors()
    q = (1-0.6827)/2.

    for i in range(1,h.GetNbinsX()+1):
        x=h.GetXaxis().GetBinCenter(i)
        xLow =h.GetXaxis().GetBinLowEdge(i) 
        xHigh =h.GetXaxis().GetBinUpEdge(i) 
        y=h.GetBinContent(i)
        yLow=0
        yHigh=0
        if y !=0.0:
            yLow = y-ROOT.Math.chisquared_quantile_c(1-q,2*y)/2.
            yHigh = ROOT.Math.chisquared_quantile_c(q,2*(y+1))/2.-y
            graph.SetPoint(i-1,x,y)
            graph.SetPointEYlow(i-1,yLow)
            graph.SetPointEYhigh(i-1,yHigh)
            graph.SetPointEXlow(i-1,0.0)
            graph.SetPointEXhigh(i-1,0.0)


    graph.SetMarkerStyle(20)
    graph.SetLineWidth(2)
    graph.SetMarkerSize(1.)
    graph.SetMarkerColor(ROOT.kBlack)
    
    return graph    

class RooPlotter(object):

    def __init__(self,filename):
        self.fCACHE = ROOT.TFile("cache.root","RECREATE")
        self.fIN=ROOT.TFile(filename)
        self.w=self.fIN.Get("w")
        self.contributions=[]
        self.fitResult=None
        
    def fix(self,var,val):
        self.w.var(var).setVal(val)
        self.w.var(var).setConstant(1)


    def load_toys(self,filename,numberOfToys):
        f=ROOT.TFile(filename)
        for toy in range(1,numberOfToys+1):
            dataset = f.Get("toys/toy_"+str(toy))
            getattr(self.w,'import')(dataset,ROOT.RooFit.Rename('toy_'+str(toy)))




    def prefit(self,model="s",minos=0,weighted=False,verbose=0,data="data_obs"):
        self.fitResult = self.w.pdf("model_"+model).fitTo(self.w.data(data),ROOT.RooFit.NumCPU(8),ROOT.RooFit.SumW2Error(weighted),ROOT.RooFit.Minos(minos),ROOT.RooFit.Verbose(verbose),ROOT.RooFit.Save(1))

        
    def addContribution(self,contrib,signal,description,linewidth,lineStyle,lineColor,fillStyle,fillColor,suffix=""):
        self.contributions.append({'name':contrib,'signal':signal,'description':description,'linewidth':linewidth,'linestyle':lineStyle,'linecolor':lineColor,'fillstyle':fillStyle,'fillcolor':fillColor,'suffix':suffix}) 


    def draw(self,var,varDesc,cat,blinded=[],doUncBand = False,log=False,data="data_obs"):
        self.canvas=ROOT.TCanvas("c")
        self.canvas.cd()
        varMax=self.w.var(var).getMax()
        varMin=self.w.var(var).getMin()
        varBins=self.w.var(var).getBins()
        #make frame
        self.frame=self.w.var(var).frame()

        if log:
            self.frame.GetYaxis().SetRangeUser(1e-2,1e+5)

        dataset=self.w.data(data).reduce("CMS_channel==CMS_channel::"+cat)
        dataset.plotOn(self.frame,ROOT.RooFit.Name("datapoints"),ROOT.RooFit.Invisible())
        visError=False

        #make special binning for fats drawing


        #OK now stack for each curve add all the others
        for i in range(0,len(self.contributions)):
            data = self.contributions[i]
            print 'Plotting ',data['name']
            names=[]
            hasSignal=False
            for j in range(i,len(self.contributions)):
                if self.contributions[j]['signal']:
                    names.append('shapeSig_'+self.contributions[j]['name']+"_"+cat+self.contributions[j]['suffix'])
                    hasSignal=True
                else:
                    names.append('shapeBkg_'+self.contributions[j]['name']+"_"+cat+self.contributions[j]['suffix'])


            if (not visError) and (self.fitResult != None) and (not hasSignal) and doUncBand:
                self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(",".join(names)),ROOT.RooFit.Name('bkgError'),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected),ROOT.RooFit.VisualizeError(self.fitResult))

                visError=True
                errorCurve=self.frame.getCurve('bkgError')
                errorCurve.SetLineColor(ROOT.kBlack)
                errorCurve.SetLineWidth(1)
                errorCurve.SetLineStyle(1)
                errorCurve.SetFillColor(ROOT.kBlack)
                errorCurve.SetFillStyle(3003)



            self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(",".join(names)),ROOT.RooFit.Name(data['name']),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected))

            curve=self.frame.getCurve(data['name'])
            curve.SetLineColor(data['linecolor'])
            curve.SetLineWidth(data['linewidth'])
            curve.SetLineStyle(data['linestyle'])
            curve.SetFillColor(data['fillcolor'])
            curve.SetFillStyle(data['fillstyle'])

        
        self.frame.SetXTitle(varDesc)
        self.frame.SetYTitle("Events")

        #legend
        self.legend = ROOT.TLegend(0.62,0.6,0.92,0.90,"","brNDC")
	self.legend.SetBorderSize(0)
	self.legend.SetLineColor(1)
	self.legend.SetLineStyle(1)
	self.legend.SetLineWidth(1)
	self.legend.SetFillColor(0)
	self.legend.SetFillStyle(0)
	self.legend.SetTextFont(42)

        for c in self.contributions:
            name=c['name']
            desc=c['description']
            curve=self.frame.getCurve(name)
            self.legend.AddEntry(curve,desc,"f")
           
            

        self.frame.SetTitle("")    
        self.frame.SetLabelSize(0.04,"X")    
        self.frame.SetLabelSize(0.04,"Y")    
        self.frame.SetTitleSize(0.05,"X")    
        self.frame.SetTitleSize(0.05,"Y")    
        self.frame.SetTitleOffset(0.90,"X")    
        self.frame.SetTitleOffset(0.93,"Y")    

        self.frame.Draw()       
        for c in self.contributions:
            name=c['name']
            curve=self.frame.getCurve(name)
            curve.Draw("Fsame")
            curve.Draw("Lsame")
            
        if visError:
            curve=self.frame.getCurve('bkgError')
            curve.Draw("Fsame")



        hist=self.frame.getHist("datapoints")

        if len(blinded)==0:
            hist.Draw("Psame")
        elif len(blinded)==2:    
            x=ROOT.Double(0.0)
            y=ROOT.Double(0.0)
            graph = hist.Clone()
            graph.SetName('tmpGRAPH')
            while hist.GetN()>0:
                hist.RemovePoint(0)
            N=0
            for i in range(0,graph.GetN()):
                graph.GetPoint(i,x,y)
                if x>blinded[0] and x< blinded[1]:
                    continue
                hist.SetPoint(N,x,y)
                hist.SetPointError(N,graph.GetErrorXlow(i),graph.GetErrorXhigh(i),graph.GetErrorYlow(i),graph.GetErrorYhigh(i))
                N=N+1
            hist.Draw("Psame")
        self.legend.Draw()    
        if log:
            self.canvas.SetLogy(1)
        self.canvas.RedrawAxis()
        self.canvas.Update()



    def fetch2DHistogram(self,var1,var2,cat,component,signal,suffix = "",data="data_obs"):
        prefix = "Bkg"
        if signal:
            prefix = "Sig"

        histogram = self.w.pdf("shape"+prefix+"_"+component+"_"+cat+suffix).createHistogram(component+"_"+cat,self.w.var(var1),ROOT.RooFit.YVar(self.w.var(var2)),ROOT.RooFit.IntrinsicBinning())

        #Now get norm
        frame=self.w.var(var1).frame()
        cutStr="CMS_channel==CMS_channel::"+cat
        dataset=self.w.data(data).reduce(cutStr)
        dataset.plotOn(frame,ROOT.RooFit.Name("datapoints"),ROOT.RooFit.Invisible())
        name = "shape"+prefix+"_"+component+"_"+cat+suffix
        self.w.pdf("model_s").getPdf(cat).plotOn(frame,ROOT.RooFit.Components(name),ROOT.RooFit.Name("tmp"),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected))
        curve=frame.getCurve("tmp")
        binArray = self.w.var(var1).getBinning().array()
        nBins = self.w.var(var1).getBinning().numBins()
        histo = ROOT.TH1D("tmp","histo",nBins,binArray)           
        for j in range(1,histo.GetNbinsX()+1):
            x=histo.GetXaxis().GetBinCenter(j)
            histo.SetBinContent(j,curve.Eval(x))
        histogram.Scale(histo.Integral()/histogram.Integral())
        return histogram
        
        

    def moneyPlot(self,var1,var2,varDesc,categories,log=False,rebin=0,drawSignal=True,data="data_obs"):
        histo={}
        histoW={}
        histoSB={}
        histoWeighted={}
        varMax=self.w.var(var1).getMax()
        varMin=self.w.var(var1).getMin()
        varBins=self.w.var(var1).getBins()

        for c in categories:
            histo[c]={}
            histoW[c]=None
            histoSB[c]=None
            histoSBTest=None
            #first create 2D histograms and fill the S and S+B histograms in each category

            for i in range(0,len(self.contributions)):
                data = self.contributions[i]
                histo[c][data['name']] = self.fetch2DHistogram(var1,var2,c,data['name'],data['signal'],data['suffix'])
                proje = histo[c][data['name']].ProjectionY('proje')
                if data['signal']:
                    if histoW[c]==None:
                        histoW[c] = histo[c][data['name']].ProjectionY('weight_'+c)
                    else:    
                        histoW[c].Add(proje)

                    if histoSB[c]==None:
                        histoSB[c] = histo[c][data['name']].ProjectionY('weightDenom_'+c)
                    else:   
                        histoSB[c].Add(proje)

                    if histoSBTest==None:
                        histoSBTest = histo[c][data['name']].ProjectionY('weightDenomT')
                    else:   
                        histoSBTest.Add(proje)

                else:
                    if histoSB[c]==None:
                        histoSB[c] = histo[c][data['name']].ProjectionY('weightDenom_'+c)
                    else:   
                        histoSB[c].Add(proje)
                    if histoSBTest==None:
                        histoSBTest = histo[c][data['name']].ProjectionY('weightDenomT')
                    else:   
                        histoSBTest.Add(proje)


        for c in categories:
            histoW[c].Divide(histoSB[c])
#            histoW[c].Divide(histoSBTest)
#            histoW[c].Scale(1.0/histoW[c].Integral())
#        sumW=0    
#        for c in categories:
#            sumW+=histoW[c].Integral()
#        for c in categories:
#            histoW[c].Scale(1.0/sumW)


        #Now reloop and reweigh the histograms creating 1D histograms 
        finalSignalHisto = None    
        finalBkgHisto = None    

        self.stack = ROOT.THStack("stack","")
        for comp in reversed(self.contributions):
            for cat in categories:
                histogram =histo[cat][comp['name']]
                for i in range(1,histogram.GetNbinsX()+1):
                    for j in range(1,histogram.GetNbinsY()+1):
                        d = histogram.GetBinContent(i,j)
                        weight = histoW[cat].GetBinContent(j)
                        histogram.SetBinContent(i,j,d*weight)
                proje = histogram.ProjectionX()
                if rebin:
                    proje.Rebin(rebin)
                if not (comp['name'] in histoWeighted.keys()):
                    histoWeighted[comp['name']] =histogram.ProjectionX(comp['name'])
                    if rebin:
                        histoWeighted[comp['name']].Rebin(rebin)
                    histoWeighted[comp['name']].GetXaxis().SetTitle(varDesc)
                else:
                    histoWeighted[comp['name']].Add(proje)

                if comp['signal']:
                    if finalSignalHisto==None:
                        finalSignalHisto=histogram.ProjectionX("finalSignalHisto") 
                        if rebin:
                            finalSignalHisto.Rebin(rebin)
                        finalSignalHisto.SetLineColor(comp['linecolor'])
                        finalSignalHisto.SetLineWidth(comp['linewidth'])
                        finalSignalHisto.SetLineStyle(comp['linestyle'])
                        finalSignalHisto.SetFillColor(comp['fillcolor'])
                        finalSignalHisto.SetFillStyle(comp['fillstyle'])
                    else:
                        finalSignalHisto.Add(proje)

                else:        
                    if finalBkgHisto==None:
                        finalBkgHisto=histogram.ProjectionX("finalBkgHisto") 
                        if rebin:
                            histogram.ProjectionX("finalBkgHisto").Rebin(rebin) 

                    else:
                        finalBkgHisto.Add(proje)

    
#            histoWeighted[comp['name']].Scale(1.0/sumW)
            #apply colors
            histoWeighted[comp['name']].SetLineColor(comp['linecolor'])
            histoWeighted[comp['name']].SetLineWidth(comp['linewidth'])
            histoWeighted[comp['name']].SetLineStyle(comp['linestyle'])
            histoWeighted[comp['name']].SetFillColor(comp['fillcolor'])
            histoWeighted[comp['name']].SetFillStyle(comp['fillstyle'])
            if comp['signal'] and not drawSignal:
                continue
            else:
                self.stack.Add(histoWeighted[comp['name']])


    
        #Now reweigh the data
        dataH = ROOT.TH1D("data","data",self.w.var(var1).getBins(),self.w.var(var1).getMin(),self.w.var(var1).getMax())
        dataH.SetLineColor(ROOT.kBlack)
        dataH.Sumw2()
        for i in range(0,self.w.data(data).numEntries()):
            line=self.w.data(data).get(i)
            weight = self.w.data(data).weight()
            x = line.find(var1).getVal()
            y = line.find(var2).getVal()
            cat = line.find("CMS_channel").getLabel()
            if not (cat in categories):
                continue
            weight=weight*histoW[cat].GetBinContent(histoW[cat].GetXaxis().FindBin(y))
            dataH.Fill(x,weight)

        if rebin:
            dataH.Rebin(rebin)
        #Draw!
        self.canvas=ROOT.TCanvas("c","",700,750)
        self.canvas.cd()
        self.pad1 = ROOT.TPad("pad1","",0.0,0.2,1.0,1.0,0)
        self.pad2 = ROOT.TPad("pad2","",0.0,0.0,1.0,0.2,0)
        self.pad1.Draw()
        self.pad2.Draw()
        self.pad1.cd()
        self.frame=self.w.var(var1).frame()
        self.frame.SetXTitle(varDesc)
        self.frame.SetYTitle("S/(S+B) weighted events")
        dataH.SetMarkerStyle(20)
        dataH.SetLineWidth(2)

        self.frame.Draw("AH")
        self.stack.Draw("A,HIST,SAME")
        self.data=dataH
        self.data.Draw("Psame")
        self.pad1.SetBottomMargin(0.012)
        self.pad1.SetLeftMargin(0.13)

        if log:
            self.frame.GetYaxis().SetRangeUser(0.00001,1e+6)
            self.pad1.SetLogy(1)
        else:
            self.frame.GetYaxis().SetRangeUser(0.0,self.data.GetMaximum()*1.3)
        self.pad1.RedrawAxis()
        self.pad1.Update()



        self.legend = ROOT.TLegend(0.58,0.6,0.92,0.90,"","brNDC")
	self.legend.SetBorderSize(0)
	self.legend.SetLineColor(1)
	self.legend.SetLineStyle(1)
	self.legend.SetLineWidth(1)
	self.legend.SetFillColor(0)
	self.legend.SetFillStyle(0)
	self.legend.SetTextFont(42)
        
	self.legend.AddEntry(self.data,"Data","P")
        

        for c in self.contributions:
            hist=histoWeighted[c['name']]
            desc=c['description']
            self.legend.AddEntry(hist,desc,"LF")



        self.legend.Draw()    
            
        self.pad2.cd()
        #mke the ratio data/MC
        self.frame2=self.w.var(var1).frame()
        self.frame2.SetTitle("")    
        self.frame2.SetLabelSize(0.15,"X")    
        self.frame2.SetLabelSize(0.15,"Y")    
        self.frame2.SetTitleSize(0.18,"X")    
        self.frame2.SetTitleSize(0.18,"Y")   
        self.frame2.SetTitleOffset(0.90,"X")    
        self.frame2.SetTitleOffset(0.3,"Y")    

        self.frame2.Draw()
        self.frame2.SetXTitle(varDesc)
        
        self.dataMinusB = self.data.Clone()
        self.dataMinusB.SetName("dataMinusB")
        self.signalHisto = finalSignalHisto
        for  i in range(1,self.dataMinusB.GetNbinsX()+1):
            d = self.dataMinusB.GetBinContent(i)
#            de = self.dataMinusB.GetBinError(i)
            b = finalBkgHisto.GetBinContent(i)
            self.dataMinusB.SetBinContent(i,d-b)
        self.signalHisto.Draw("HIST,SAME")
        self.dataMinusB.Draw("Psame")
        self.line=ROOT.TLine(varMin,0.0,varMax,0.0)
        self.line.SetLineWidth(2)
        self.line.Draw()


        self.pad2.SetTopMargin(0.04)
        self.pad2.SetBottomMargin(0.5)
        self.pad2.SetLeftMargin(0.13)
        self.pad2.RedrawAxis()
        self.pad2.Update()








    def moneyPlotSimple(self,var1,var2,varDesc,categories,SOB=False,log=False,rebin=0,drawSignal=True):

        nBinsVar1 = self.w.var(var1).getBins()
        nBinsVar2 = self.w.var(var2).getBins()
        ncat = len(categories)
        nWeights = nBinsVar2 * ncat

        var1Max=self.w.var(var1).getMax()
        var1Min=self.w.var(var1).getMin()
        var2Max=self.w.var(var2).getMax()
        var2Min=self.w.var(var2).getMin()

        histo={}
        histoW={}
        histoSB={}
        histoWeighted={}


        for c in categories:
            histo[c]={}
            histoW[c]=None
            histoSB[c]=None
            histoSBTest=None
            ## first create 2D histograms and fill the S and S+B histograms in each category

            for i in range(0,len(self.contributions)):
                data = self.contributions[i]
                histo[c][data['name']] = self.fetch2DHistogram(var1,var2,c,data['name'],data['signal'],data['suffix'])
                proje = histo[c][data['name']].ProjectionY('proje')
                if data['signal']:
                    if histoW[c]==None:
                        histoW[c] = histo[c][data['name']].ProjectionY('weight_'+c)
                    else:    
                        histoW[c].Add(proje)

                    if not SOB: ## means if SOSPB
                        if histoSB[c]==None:
                            histoSB[c] = histo[c][data['name']].ProjectionY('weightDenom_'+c)
                        else:   
                            histoSB[c].Add(proje)

                        if histoSBTest==None:
                            histoSBTest = histo[c][data['name']].ProjectionY('weightDenomT')
                        else:   
                            histoSBTest.Add(proje)

                else:
                    if histoSB[c]==None:
                        histoSB[c] = histo[c][data['name']].ProjectionY('weightDenom_'+c)
                    else:   
                        histoSB[c].Add(proje)
                    if histoSBTest==None:
                        histoSBTest = histo[c][data['name']].ProjectionY('weightDenomT')
                    else:   
                        histoSBTest.Add(proje)

        #print 'number of bins*categories for weights:', nWeights
        sumS=0
        sumSB=0
        sumW=0
        sumWnew=0

        for c in categories:
            #print 'expected in cat', c, ': sig', histoW[c].Integral(), 'bkg', histoSB[c].Integral()
            sumS+=histoW[c].Integral()
            sumSB+=histoSB[c].Integral()
            histoW[c].Divide(histoSB[c])
            sumW+=histoW[c].Integral()

        for c in categories:
            histoW[c].Scale(nWeights/sumW) ## Divide by the mean weight to get proper normalization
            sumWnew+=histoW[c].Integral()

        #print 'initial expected sig integral', sumS
        #if SOB:
        #    print 'initial expected bkg integral', sumSB
        #else:
        #    print 'initial expected sig+bkg integral', sumSB
        #print 'sum of weights (before normalizing them)', sumW
        #print 'sum of weights (after normalizing them) ', sumWnew

        ## Now reloop and reweigh the histograms creating 1D histograms 
        finalSignalHisto = None    
        finalBkgHisto = None    

        self.stack = ROOT.THStack("stack","")
        for comp in reversed(self.contributions):
            for cat in categories:
                histogram =histo[cat][comp['name']]
                for i in range(1,histogram.GetNbinsX()+1):
                    for j in range(1,histogram.GetNbinsY()+1):
                        d = histogram.GetBinContent(i,j)
                        weight = histoW[cat].GetBinContent(j)
                        histogram.SetBinContent(i,j,d*weight)
                proje = histogram.ProjectionX()
                if rebin:
                    proje.Rebin(rebin)
                if not (comp['name'] in histoWeighted.keys()):
                    histoWeighted[comp['name']] =histogram.ProjectionX(comp['name'])
                    if rebin:
                        histoWeighted[comp['name']].Rebin(rebin)
                    histoWeighted[comp['name']].GetXaxis().SetTitle(varDesc)
                else:
                    histoWeighted[comp['name']].Add(proje)

                if comp['signal']:
                    if finalSignalHisto==None:
                        finalSignalHisto=histogram.ProjectionX("finalSignalHisto") 
                        if rebin:
                            finalSignalHisto.Rebin(rebin)
                        finalSignalHisto.SetLineColor(comp['linecolor'])
                        finalSignalHisto.SetLineWidth(comp['linewidth'])
                        finalSignalHisto.SetLineStyle(comp['linestyle'])
                        finalSignalHisto.SetFillColor(comp['fillcolor'])
                        finalSignalHisto.SetFillStyle(comp['fillstyle'])
                    else:
                        finalSignalHisto.Add(proje)

                else:        
                    if finalBkgHisto==None:
                        finalBkgHisto=histogram.ProjectionX("finalBkgHisto") 
                        if rebin:
                            finalBkgHisto.Rebin(rebin)
                    else:
                        finalBkgHisto.Add(proje)

            #apply colors
            histoWeighted[comp['name']].SetLineColor(comp['linecolor'])
            histoWeighted[comp['name']].SetLineWidth(comp['linewidth'])
            histoWeighted[comp['name']].SetLineStyle(comp['linestyle'])
            histoWeighted[comp['name']].SetFillColor(comp['fillcolor'])
            histoWeighted[comp['name']].SetFillStyle(comp['fillstyle'])
            if comp['signal'] and not drawSignal:
                continue
            else:
                self.stack.Add(histoWeighted[comp['name']])

        #print 'finalSignalHisto.Integral()', finalSignalHisto.Integral()
        #print 'finalBkgHisto.Integral()', finalBkgHisto.Integral()

    
        ## Now reweigh the data
        dataH = ROOT.TH1D("data","data",nBinsVar1,var1Min,var1Max)
        dataH.SetLineColor(ROOT.kBlack)
        dataH.Sumw2()

        sumdatawoldtot=0
        sumdatawnewtot=0
        sumdatawold={}
        sumdatawnew={}
        for cat in categories:
            sumdatawold[cat]=0
            sumdatawnew[cat]=0
        for i in range(0,self.w.data(data).numEntries()): ## Loop over data bins (in 2D * 4 cat)
            line=self.w.data(data).get(i)
            x = line.find(var1).getVal()
            y = line.find(var2).getVal()
            cat = line.find("CMS_channel").getLabel()
            if not (cat in categories):
                print 'ERROR, cat', cat, 'not found'
                continue

            N=int(self.w.data(data).weight())
            sumdatawoldtot+=N
            sumdatawold[cat]+=N
            for e in range(N): ## Fill one event at a time, to get Sumw2 error bars
                weight=histoW[cat].GetBinContent(histoW[cat].GetXaxis().FindBin(y))
                dataH.Fill(x,weight)
                sumdatawnewtot+=weight
                sumdatawnew[cat]+=weight

        if rebin:
            dataH.Rebin(rebin)
        
        self.gData = ROOT.TGraphAsymmErrors(dataH)

        #print 'number of data events', sumdatawoldtot
        #print 'sum of data weights (before, after)'
        #for cat in categories:
        #    print '  ', cat, sumdatawold[cat], sumdatawnew[cat]
        #print '  total', sumdatawoldtot, sumdatawnewtot
        #print 'dataH.Integral() after reweighting', dataH.Integral()


        ## Draw

        setTDRStyle()
        style=gROOT.GetStyle("tdrStyle").Clone()
        style.SetPadLeftMargin(0.14)
        style.SetPadRightMargin(0.04)
        style.SetErrorX(0)
        style.cd()
        ROOT.TGaxis.SetMaxDigits(4)

        ZOOMX = True

        self.canvas=ROOT.TCanvas("c","c",500,500)
        self.canvas.cd()

        self.pad1 = ROOT.TPad("pad1","",0.0,0.24,1.0,1.0,0)
        self.pad2 = ROOT.TPad("pad2","",0.0,0.0,1.0,0.24,0)

        self.pad1.SetTopMargin(0.066)
        self.pad1.SetBottomMargin(0.026)
        self.pad1.SetLeftMargin(0.14)
        self.pad1.SetRightMargin(0.04)
        self.pad2.SetTopMargin(0.)
        self.pad2.SetBottomMargin(0.5)
        self.pad2.SetLeftMargin(0.14)
        self.pad2.SetRightMargin(0.04)

        if log: self.pad1.SetLogy(1)
        self.pad1.Draw()
        self.pad2.Draw()
        self.pad1.cd()

        self.frame=self.w.var(var1).frame()
        self.frame.SetTitle("")    
        self.frame.SetXTitle(varDesc)
        if SOB:        
            self.frame.SetYTitle("S/B weighted events / "+str(int(dataH.GetBinWidth(1)))+" GeV")
        else:
            self.frame.SetYTitle("S/(S+B) weighted events / "+str(int(dataH.GetBinWidth(1)))+" GeV")
        self.frame.SetLabelSize(0.04,"X")    
        self.frame.SetLabelSize(0.055,"Y")
        self.frame.SetTitleSize(0.05,"X")    
        self.frame.SetTitleSize(0.058,"Y")    
        self.frame.SetTitleOffset(3,"X")    
        self.frame.SetLabelOffset(3,"X")    
        self.frame.SetTitleOffset(1.05,"Y")
        self.frame.Draw("AH")
        if ZOOMX:
            self.frame.GetXaxis().SetRangeUser(800,4500)

        self.bkgHisto = finalBkgHisto.Clone()
        self.bkgHisto.SetName("BKGHISTOTOTAL")
        self.bkgHisto.SetLineWidth(1)
        self.bkgHisto.SetLineColor(ROOT.TColor.GetColor("#084B55"))
        self.bkgHisto.SetFillColor(ROOT.TColor.GetColor("#82C19B"))
        self.bkgHisto.Draw("A,HIST,SAME")

        dataH.SetMarkerStyle(20)
        dataH.SetMarkerSize(0.5)
        dataH.SetLineWidth(2)
        self.data=dataH
        for i in range(self.gData.GetN()):
            self.gData.SetPointEXlow(i,0.)
            self.gData.SetPointEXhigh(i,0.)
        self.gData.SetMarkerStyle(20)
        self.gData.SetMarkerSize(0.5)
        self.gData.Draw("E0,P,same")

        if log:
            self.frame.GetYaxis().SetRangeUser(0.00001,1e+6)
            self.pad1.SetLogy(1)
        else:
            #self.frame.GetYaxis().SetRangeUser(0.0,self.data.GetMaximum()*1.3)
            self.frame.GetYaxis().SetRangeUser(0.0,52000.)
        self.pad1.RedrawAxis()
        self.pad1.Update()


        self.legend = ROOT.TLegend(0.58,0.58,0.92,0.85,"","brNDC")
	self.legend.SetBorderSize(0)
	self.legend.SetLineColor(1)
	self.legend.SetLineStyle(1)
	self.legend.SetLineWidth(1)
	self.legend.SetFillColor(0)
	self.legend.SetFillStyle(0)
	self.legend.SetTextFont(42)
	self.legend.SetTextSize(0.06)
	self.legend.SetHeader("2D fit")
	self.legend.AddEntry(self.data,"Data","P")
	self.legend.AddEntry(self.bkgHisto,"Background","F")
        self.legend.Draw()    


        
        ## pad for data/MC ratio
        whichratio = "DMB" ## data minus bkg
        #whichratio = "DMBOE" ## data minus bkg over error
        #whichratio = "DOB" ## data over bkg

        self.pad2.cd()
        self.pad2.SetGridy()

        self.frame2=self.w.var(var1).frame()
        self.frame2.SetTitle("")    
        self.frame2.SetLabelSize(0.16,"X")    
        self.frame2.SetLabelSize(0.12,"Y")    
        self.frame2.SetTitleSize(0.21,"X")    
        self.frame2.SetTitleSize(0.15,"Y")   
        self.frame2.SetTitleOffset(0.95,"X")    
        self.frame2.SetTitleOffset(0.41,"Y")    
        self.frame2.Draw()
        self.frame2.SetXTitle(varDesc)
        if whichratio=="DMB":
            self.frame2.GetYaxis().SetTitle("Data#minusBkg.")    
        elif whichratio=="DMBOE":
            self.frame2.GetYaxis().SetTitle("#frac{Data#minusBkg.}{#sigma_{Data}}")    
        elif whichratio=="DOB":
            self.frame2.GetYaxis().SetTitle("Data/Bkg.")
        self.frame2.GetYaxis().SetNdivisions(206)
        
        self.gDataMinusB = ROOT.TGraphAsymmErrors()
        for i in range(dataH.GetNbinsX()):
            x = self.gData.GetX()[i]
            d = self.gData.GetY()[i]
            b = finalBkgHisto.GetBinContent(i+1)
            el = self.gData.GetEYlow()[i]
            eh = self.gData.GetEYhigh()[i]
            if whichratio=="DMB": 
                self.gDataMinusB.SetPoint(i, x, d-b)
                self.gDataMinusB.SetPointEYlow (i, el)
                self.gDataMinusB.SetPointEYhigh(i, eh)      
            elif whichratio=="DMBOE":
                if eh!=0:
                    self.gDataMinusB.SetPoint(i, x, (d-b)/eh)
                    self.gDataMinusB.SetPointEYlow (i, el/eh)
                    self.gDataMinusB.SetPointEYhigh(i, eh/eh)
            elif whichratio=="DOB":
                self.gDataMinusB.SetPoint(i, x, d/b)
                self.gDataMinusB.SetPointEYlow (i, el/b)
                self.gDataMinusB.SetPointEYhigh(i, eh/b)
        self.gDataMinusB.SetMarkerStyle(20)
        self.gDataMinusB.SetMarkerSize(0.5)

        self.line=ROOT.TLine(var1Min,0.0,var1Max,0.0)
        self.line.SetLineWidth(1)
        self.line.SetLineColor(14)

        if whichratio=="DMB":
            self.frame2.GetYaxis().SetRangeUser(-1300,1300)
        elif whichratio=="DMBOE":
            self.frame2.GetYaxis().SetRangeUser(-2.9,2.9)
        elif whichratio=="DOB":
            self.frame2.GetYaxis().SetRangeUser(0.,1.95)
            self.line.SetY1(1.)
            self.line.SetY2(1.)

        self.line.Draw()
        self.gDataMinusB.Draw("E0,P,same")

        if ZOOMX:
            self.frame2.GetXaxis().SetRangeUser(800,4500)
            self.line.SetX1(800)
            self.line.SetX2(4500)

        self.pad2.RedrawAxis()
        self.pad2.Update()












    
    def drawBinned(self,var,varDesc,label,cat,blinded=[],doUncBand=False,log=False,rebin=0,rangeStr="",minX=0.,maxX=10000.,maxY=-1.,unstackSignal=False,scaleSignal=-1.,sigLabel="",data="data_obs"):

        setTDRStyle()
        style=gROOT.GetStyle("tdrStyle").Clone()
        style.SetPadLeftMargin(0.14)
        style.SetPadRightMargin(0.04)
        #style.SetGridColor(15)
        style.SetErrorX(0)
        style.cd()
        uncColor=ROOT.kOrange+9 #14
        uncStyle=3154

        self.canvas=ROOT.TCanvas("c","",500,500)
        self.canvas.cd()
        self.pad1 = ROOT.TPad("pad1","",0.0,0.24,1.0,0.95,0)
        self.pad2 = ROOT.TPad("pad2","",0.0,0.0,1.0,0.24,0)

        self.pad1.SetTopMargin(0.)
        self.pad1.SetBottomMargin(0.028)
        self.pad1.SetLeftMargin(0.14)
        self.pad1.SetRightMargin(0.04)
        self.pad2.SetTopMargin(0.)
        self.pad2.SetBottomMargin(0.5)
        self.pad2.SetLeftMargin(0.14)
        self.pad2.SetRightMargin(0.04)

        if log: self.pad1.SetLogy(1)
        self.pad1.Draw()
        self.pad2.Draw()
        self.pad1.cd()
        style.cd()
                
        varMax=self.w.var(var).getMax()
        varMin=self.w.var(var).getMin()
        varNBins=self.w.var(var).getBins()
        newNBins=int(varNBins / (1. if not rebin else rebin))
        print varMin, varMax, varNBins, newNBins ## debug

        ## make the frame
        self.frame=self.w.var(var).frame()
        cutStr="CMS_channel==CMS_channel::"+cat
        dataset=self.w.data(data).reduce(cutStr)
        
        projRange=[]
        if rangeStr!="":
            ranges=rangeStr.split(',')
            for r in ranges:
                rdata=r.split(':')
                self.w.var(rdata[0]).setRange(rdata[1],float(rdata[2]),float(rdata[3]))
                projRange.append(rdata[1])
                dataset=dataset.reduce("{var}>{mini}&&{var}<{maxi}".format(var=rdata[0],mini=rdata[2],maxi=rdata[3]))
        
        #dataset.plotOn(self.frame,ROOT.RooFit.Name("datapoints"),ROOT.RooFit.Invisible(),ROOT.RooFit.Binning(newNBins))
        dataset.plotOn(self.frame,ROOT.RooFit.Name("datapoints"),ROOT.RooFit.Invisible(),ROOT.RooFit.Binning(newNBins),ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
        ##---- debug
        #for i in range(dataset.numEntries()):
        #    line = dataset.get(i)
        #    x = line.find("MLNuJ").getVal()
        #    y = line.find("MJ").getVal()
        #    cat = line.find("CMS_channel").getLabel()
        #    wgt = dataset.weight()
        #    print x, cat, wgt
        ##----

        visError=False
        
        self.histoSum = ROOT.TH1D("histoSum","histo",newNBins,varMin,varMax)
        self.bkgUncRatio = ROOT.TH1D(self.histoSum)
        self.hSig = ROOT.TH1D(self.histoSum)
        backgrounds=[]
        hasSignal=False
        
        ## retrieve each curve and add all backgrounds
        for i in range(0,len(self.contributions)):
            data = self.contributions[i]
            print 'Plotting ',data['name']

            if self.contributions[i]['signal']:
                name=('shapeSig_'+self.contributions[i]['name']+"_"+cat+self.contributions[i]['suffix'])
                hasSignal=True
            else:
                name=('shapeBkg_'+self.contributions[i]['name']+"_"+cat+self.contributions[i]['suffix'])
                backgrounds.append(name)            
            
            if rangeStr=="":    
                self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(name),ROOT.RooFit.Name(data['name']),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected),ROOT.RooFit.Binning(newNBins))
            else:
                self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(name),ROOT.RooFit.Name(data['name']),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected),ROOT.RooFit.Binning(newNBins),ROOT.RooFit.ProjectionRange(','.join(projRange)))
                
            curve=self.frame.getCurve(data['name'])
            histo = ROOT.TH1D("histo_"+name,"histo",newNBins,varMin,varMax)
            histo.SetLineColor(data['linecolor'])
            histo.SetLineWidth(data['linewidth'])
            histo.SetLineStyle(data['linestyle'])
            histo.SetFillColor(data['fillcolor'])
            histo.SetFillStyle(data['fillstyle'])
            for j in range(1,histo.GetNbinsX()+1):
                x=histo.GetXaxis().GetBinCenter(j)
                histo.SetBinContent(j,curve.Eval(x))
            if not data['signal']:    
                self.histoSum.Add(histo)
            self.contributions[i]['histo']=histo    

        ## create uncertainty band
        if (not visError) and (self.fitResult != None) and doUncBand:
            if rangeStr=="":
                self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(",".join(backgrounds)),ROOT.RooFit.Name('bkgError'),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected),ROOT.RooFit.Binning(newNBins),ROOT.RooFit.VisualizeError(self.fitResult))
            else:
                self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(",".join(backgrounds)),ROOT.RooFit.Name('bkgError'),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected),ROOT.RooFit.Binning(newNBins),ROOT.RooFit.VisualizeError(self.fitResult),ROOT.RooFit.ProjectionRange(','.join(projRange)))
            errorCurve=self.frame.getCurve('bkgError')
            visError=True

            for i in range(1,self.histoSum.GetNbinsX()+1):
                x=self.histoSum.GetXaxis().GetBinCenter(i)
                bkg=self.histoSum.GetBinContent(i)
                self.histoSum.SetBinError(i,errorCurve.Eval(x)-self.histoSum.GetBinContent(i))
                self.bkgUncRatio.SetBinContent(i,1.0)
                self.bkgUncRatio.SetBinError(i,self.histoSum.GetBinError(i)/bkg)

            self.histoSum.SetFillColor(uncColor)
            self.histoSum.SetFillStyle(uncStyle)
            self.histoSum.SetMarkerSize(0)
            self.histoSum.SetLineColor(0)#uncColor)

            self.bkgUncRatio.SetFillColor(uncColor)
            self.bkgUncRatio.SetFillStyle(uncStyle)
            self.bkgUncRatio.SetMarkerSize(0)
            self.bkgUncRatio.SetLineColor(uncColor)


        ## build stack and legend
        self.stack = ROOT.THStack("stack","")

        printSigLabel = sigLabel!=""
        self.legend = ROOT.TLegend(0.57,0.79-0.065*(visError+len(self.contributions)+printSigLabel),0.92,0.95,"","brNDC")
	self.legend.SetBorderSize(0)
	self.legend.SetLineColor(1)
	self.legend.SetLineStyle(1)
	self.legend.SetLineWidth(1)
	self.legend.SetFillColor(0)
	self.legend.SetFillStyle(0)
	self.legend.SetTextFont(42)
	self.legend.SetTextSize(0.055)

        self.legend.SetHeader(label)
        self.legend.AddEntry(self.frame.getHist("datapoints"),"Data","EP")

        for i in range(len(self.contributions)-1,-1,-1):
            c=self.contributions[i]
            hist=c['histo']
            if c['signal']:
                if scaleSignal>0:
                    hist.Scale(scaleSignal)
                self.hSig=hist
            if not(unstackSignal and c['signal']):
                self.stack.Add(hist)
        for c in self.contributions:
            if not(unstackSignal and c['signal']):
                self.legend.AddEntry(c['histo'],c['description'],"F")
                if c['signal'] and printSigLabel:
                    self.legend.AddEntry(None,sigLabel,"")
        if visError:
            self.legend.AddEntry(self.histoSum,"Bkg. shape unc.","F")            
        for c in self.contributions:
            if unstackSignal and c['signal']:
                self.legend.AddEntry(c['histo'],c['description'],"F")
                if printSigLabel:
                    self.legend.AddEntry(None,sigLabel,"")

        self.frame.SetTitle("")    
        self.frame.SetXTitle(varDesc)
        self.frame.SetYTitle("Events")
        self.frame.SetLabelSize(0.04,"X")    
        self.frame.SetLabelSize(0.06,"Y")    
        self.frame.SetTitleSize(0.05,"X")    
        self.frame.SetTitleSize(0.07,"Y")    
        self.frame.SetTitleOffset(3,"X")    
        self.frame.SetLabelOffset(3,"X")    
        self.frame.SetTitleOffset(0.9,"Y")    

        self.frame.Draw("AH")

        self.stack.Draw("A,HIST,SAME")

        if unstackSignal:
            self.hSig.SetLineWidth(2)
            self.hSig.Draw("HIST,SAME")

            
        binWidth=(varMax-varMin)/newNBins
        self.frame.SetYTitle("Events / "+str(int(binWidth))+" GeV")

        ## axis range customization
        self.frame.GetXaxis().SetRangeUser(minX,maxX)
        if var.startswith("MLNuJ"):
            if log and maxY>0:
                self.frame.GetYaxis().SetRangeUser(0.3,maxY)
        if var.startswith("MJ"):
            if not log and maxY>0:
                self.frame.GetYaxis().SetRangeUser(0.,maxY)

        if visError:
            self.histoSum.Draw("E2,same")

        hist=self.frame.getHist("datapoints")
        hist.SetMarkerStyle(20)
        hist.SetMarkerSize(0.5)
        if var.startswith("MLNuJ"):
            hist.SetMarkerSize(0.4)
        #hist.SetLineWidth(2)
        if len(blinded)==0:
            hist.Draw("Psame")
        elif len(blinded)==2:    
            x=ROOT.Double(0.0)
            y=ROOT.Double(0.0)
            graph = hist.Clone()
            graph.SetName('tmpGRAPH')
            while hist.GetN()>0:
                hist.RemovePoint(0)
            N=0
            for i in range(0,graph.GetN()):
                graph.GetPoint(i,x,y)
                if x>blinded[0] and x< blinded[1]:
                    continue
                hist.SetPoint(N,x,y)
                #hist.SetPointError(N,graph.GetErrorXlow(i),graph.GetErrorXhigh(i),graph.GetErrorYlow(i),graph.GetErrorYhigh(i))
                hist.SetPointError(N,0,0,graph.GetErrorYlow(i),graph.GetErrorYhigh(i))
                N=N+1
            hist.Draw("Psame")

        self.legend.Draw()

        self.pad1.RedrawAxis()
        self.pad1.Update()




        ## pad for data/MC ratio

        self.pad2.cd()
        #self.pad2.SetGridy()

        self.frame2=self.w.var(var).frame()
        self.frame2.SetTitle("")    
        self.frame2.SetLabelSize(0.16,"X")    
        self.frame2.SetLabelSize(0.125,"Y")    
        #self.frame2.SetLabelOffset(0.01,"X")    
        self.frame2.SetTitleSize(0.21,"X")    
        self.frame2.SetTitleSize(0.17,"Y")   
        self.frame2.SetTitleOffset(0.95,"X")    
        self.frame2.SetTitleOffset(0.35,"Y")    

        self.frame2.Draw()
        self.frame2.SetXTitle(varDesc)
        self.frame2.SetYTitle("Data/Bkg." if hasSignal else "Data/fit")
        self.frame2.GetYaxis().SetNdivisions(206)

        self.ratioGraph = ROOT.TGraphAsymmErrors(hist)
        x=ROOT.Double(0.)
        y=ROOT.Double(0.)
        chisq=0
        for i in range(0,hist.GetN()):
            hist.GetPoint(i,x,y)
            bkgBin=self.histoSum.GetXaxis().FindBin(x)
            bkg=self.histoSum.GetBinContent(bkgBin)
            #if y==0.0: continue
            chisq = chisq + (y-bkg)*(y-bkg)/bkg
            self.ratioGraph.SetPoint(i,x,y/bkg)
            self.ratioGraph.SetPointError(i,0,0,hist.GetErrorYlow(i)/bkg,hist.GetErrorYhigh(i)/bkg)
        #print 'chisquare=', chisq

        self.hSigRatio = self.hSig.Clone()
        self.hSigRatio.SetName(self.hSig.GetName()+"_ratio")
        drawSigRatio = hasSignal and not unstackSignal
        if drawSigRatio:
            self.hSigRatio.Add(self.histoSum)
            self.hSigRatio.Divide(self.histoSum)

        self.line=ROOT.TLine(varMin,1.0,varMax,1)
        self.line.SetLineWidth(2 if drawSigRatio else 1)
        self.line.SetLineColor(14)

        ## axis range customization
        self.frame2.GetXaxis().SetRangeUser(minX,maxX)
        if var.startswith("MLNuJ"):
            self.line.SetX1(minX)
            self.line.SetX2(maxX)
        self.frame2.GetYaxis().SetRangeUser(0.5,1.5)

        ## draw everything
        if drawSigRatio:
            self.hSigRatio.Draw("hist,same")
        if visError:
            self.bkgUncRatio.Draw("E2,same")
        self.line.Draw()
        self.ratioGraph.Draw("0Psame")

        self.pad2.RedrawAxis()
        self.pad2.Update()











    
    def drawOverlay(self,var,varDesc,label,cat,blinded=[],log=False,rebin=0,rangeStr="",minX=0.,maxX=10000.,maxY=-1.,data="data_obs"):

        setTDRStyle()
        style=gROOT.GetStyle("tdrStyle").Clone()
        style.SetPadLeftMargin(0.14)
        style.SetPadRightMargin(0.04)
        #style.SetGridColor(15)
        style.SetErrorX(0)
        style.cd()

        self.canvas=ROOT.TCanvas("c","",500,500)
        self.canvas.cd()
        style.cd()
                
        varMax=self.w.var(var).getMax()
        varMin=self.w.var(var).getMin()
        varNBins=self.w.var(var).getBins()
        newNBins=int(varNBins / (1. if not rebin else rebin))
        print varMin, varMax, varNBins, newNBins ## debug

        ## make the frame
        self.frame=self.w.var(var).frame()
        cutStr="CMS_channel==CMS_channel::"+cat
        dataset=self.w.data(data).reduce(cutStr)
        
        projRange=[]
        if rangeStr!="":
            ranges=rangeStr.split(',')
            for r in ranges:
                rdata=r.split(':')
                self.w.var(rdata[0]).setRange(rdata[1],float(rdata[2]),float(rdata[3]))
                projRange.append(rdata[1])
                dataset=dataset.reduce("{var}>{mini}&&{var}<{maxi}".format(var=rdata[0],mini=rdata[2],maxi=rdata[3]))
        
        #dataset.plotOn(self.frame,ROOT.RooFit.Name("datapoints"),ROOT.RooFit.Invisible(),ROOT.RooFit.Binning(newNBins))
        dataset.plotOn(self.frame,ROOT.RooFit.Name("datapoints"),ROOT.RooFit.Invisible(),ROOT.RooFit.Binning(newNBins),ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
        ##---- debug
        #for i in range(dataset.numEntries()):
        #    line = dataset.get(i)
        #    x = line.find("MLNuJ").getVal()
        #    y = line.find("MJ").getVal()
        #    cat = line.find("CMS_channel").getLabel()
        #    wgt = dataset.weight()
        #    print x, cat, wgt
        ##----
        
        ## retrieve each curve and add all backgrounds
        for i in range(0,len(self.contributions)):
            data = self.contributions[i]
            print 'Plotting ',data['name']

            if self.contributions[i]['signal']:
                name=('shapeSig_'+self.contributions[i]['name']+"_"+cat+self.contributions[i]['suffix'])
            else:
                name=('shapeBkg_'+self.contributions[i]['name']+"_"+cat+self.contributions[i]['suffix'])
            
            if rangeStr=="":    
                self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(name),ROOT.RooFit.Name(data['name']),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected),ROOT.RooFit.Binning(newNBins))
            else:
                self.w.pdf("model_s").getPdf(cat).plotOn(self.frame,ROOT.RooFit.Components(name),ROOT.RooFit.Name(data['name']),ROOT.RooFit.Invisible(),ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected),ROOT.RooFit.Binning(newNBins),ROOT.RooFit.ProjectionRange(','.join(projRange)))
                
            curve=self.frame.getCurve(data['name'])
            histo = ROOT.TH1D("histo_"+name,"histo",newNBins,varMin,varMax)
            histo.SetLineColor(data['linecolor'] if self.contributions[i]['signal'] else data['fillcolor'])
            histo.SetLineWidth(3)
            histo.SetFillStyle(0)
            for j in range(1,histo.GetNbinsX()+1):
                x=histo.GetXaxis().GetBinCenter(j)
                histo.SetBinContent(j,curve.Eval(x))
            self.contributions[i]['histo']=histo    


        self.legend = ROOT.TLegend(0.57,0.79-0.065*len(self.contributions),0.92,0.95,"","brNDC")
	self.legend.SetBorderSize(0)
	self.legend.SetLineColor(1)
	self.legend.SetLineStyle(1)
	self.legend.SetLineWidth(1)
	self.legend.SetFillColor(0)
	self.legend.SetFillStyle(0)
	self.legend.SetTextFont(42)
	self.legend.SetTextSize(0.055)
        self.legend.SetHeader(label)

        self.frame.SetTitle("")    
        self.frame.SetXTitle(varDesc)
        self.frame.SetYTitle("Events")
        self.frame.SetLabelSize(0.04,"X")    
        self.frame.SetLabelSize(0.06,"Y")    
        self.frame.SetTitleSize(0.05,"X")    
        self.frame.SetTitleSize(0.07,"Y")    
        self.frame.SetTitleOffset(3,"X")    
        self.frame.SetLabelOffset(3,"X")    
        self.frame.SetTitleOffset(0.9,"Y")    
        self.frame.Draw("AH")

        for i in range(len(self.contributions)-1,-1,-1):
            c=self.contributions[i]
            c['histo'].Draw("HIST,SAME")
            self.legend.AddEntry(c['histo'],c['description'],"F")
            
        binWidth=(varMax-varMin)/newNBins
        self.frame.SetYTitle("Events / "+str(int(binWidth))+" GeV")

        ## axis range customization
        self.frame.GetXaxis().SetRangeUser(minX,maxX)
        if var.startswith("MLNuJ"):
            if log and maxY>0:
                self.frame.GetYaxis().SetRangeUser(0.3,maxY)
        if var.startswith("MJ"):
            if not log and maxY>0:
                self.frame.GetYaxis().SetRangeUser(0.,maxY)

        self.legend.Draw()

        self.canvas.RedrawAxis()
        self.canvas.Update()



