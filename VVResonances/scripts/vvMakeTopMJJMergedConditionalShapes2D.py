#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
import copy



parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT file",default='')
parser.add_option("-d","--debugoutput",dest="debugoutput",help="Output debug plots",default='')
parser.add_option("-O","--outDir",dest="outDir",help="Output directory",default='')
parser.add_option("-v","--varx",dest="varx",help="variablex",default='lnujj_LV_mass')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins in x",default=168)
parser.add_option("-x","--minx",dest="minx",type=float,help="minimum x",default=800.)
parser.add_option("-X","--maxx",dest="maxx",type=float, help="maximum x",default=5000.)
parser.add_option("-V","--vary",dest="vary",help="variabley",default='lnujj_l2_softDrop_mass')
parser.add_option("-B","--binsy",dest="binsy",type=int,help="bins in y (for the template)",default=90)
parser.add_option("-E","--binsxfit",dest="binsxfit",type=int,help="bins in x (for the fit)",default=168)
parser.add_option("-F","--binsyfit",dest="binsyfit",type=int,help="bins in y (for the fit)",default=90)
parser.add_option("-y","--miny",dest="miny",type=float,help="minimum y",default=30.)
parser.add_option("-Y","--maxy",dest="maxy",type=float, help="maximum y",default=210.)
parser.add_option("-l","--lumi",dest="lumi",type=float, help="lumi",default="35000")
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="")
parser.add_option("-e","--doExp",dest="doExp",action="store_true",help="DoExp",default=False)

(options,args) = parser.parse_args()
    


samples={}
sampleTypes=options.samples.split(',')
dataPlotters=[]

for filename in os.listdir(args[0]):
    for sampleType in sampleTypes:
        if filename.find(sampleType)!=-1:
            fnameParts=filename.split('.')
            fname=fnameParts[0]
            ext=fnameParts[1]
            if ext.find("root") ==-1:
                continue
            dataPlotters.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            dataPlotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
            dataPlotters[-1].addCorrectionFactor('xsec','tree')
            dataPlotters[-1].addCorrectionFactor('genWeight','tree')
            dataPlotters[-1].addCorrectionFactor('puWeight','tree')
            dataPlotters[-1].addCorrectionFactor('lnujj_sf','tree')
            dataPlotters[-1].addCorrectionFactor('truth_genTop_weight','tree')
    
data=MergedPlotter(dataPlotters)

h = data.drawTH2(options.vary+":"+options.varx,options.cut,str(options.lumi),options.binsxfit,options.minx,options.maxx,options.binsyfit,options.miny,options.maxy) 



fitter=Fitter(['MVV','MJJ'])
fitter.w.var("MVV").setVal((options.maxx-options.minx)/2.0)
fitter.w.var("MVV").setMax(options.maxx)
fitter.w.var("MVV").setMin(options.minx)
fitter.w.var("MJJ").setVal((options.maxy-options.miny)/2.0)
fitter.w.var("MJJ").setMax(options.maxy)
fitter.w.var("MJJ").setMin(options.miny)

scaleSysts= {'Scale':"0.0094"}
resSysts  = {'Res':"0.2"}
fracSysts = {'TopPt0':"0.2",
             'TopPt1':"25000.0/MVV^2"} 
fitter.jetDoublePeakExpCond('model',['MVV','MJJ'],scaleSysts,resSysts,fracSysts)

if options.doExp==0:
    fitter.w.var("g").setVal(1.0)
    fitter.w.var("g").setConstant(1)
    fitter.w.var("slope").setVal(0.0)
    fitter.w.var("slope").setConstant(1)

if options.fixPars!="":
    fixedPars =options.fixPars.split(',')
    for par in fixedPars:
        parVal = par.split(':')
        fitter.w.var(parVal[0]).setVal(float(parVal[1]))
        fitter.w.var(parVal[0]).setConstant(1)

histo=copy.deepcopy(h)
fitter.importBinnedData(histo,['MVV','MJJ'],'data')   
#fitter.w.Print()



fitter.fit('model','data',[ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(fitter.w.var("MVV"))),ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(0)])
fitter.fit('model','data',[ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(fitter.w.var("MVV"))),ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(1)]) ## this one computes correct asymmetric error bars




## store the result, for nominal and alternative shapes
F=ROOT.TFile(options.output+".root","RECREATE")
F.cd()

##nominal
template = fitter.w.pdf("model").createHistogram("histo", fitter.w.var("MVV"), ROOT.RooFit.Binning(options.binsx,options.minx,options.maxx), ROOT.RooFit.YVar(fitter.w.var("MJJ"),ROOT.RooFit.Binning(options.binsy,options.miny,options.maxy)) ) 
template.Write("histo")

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
allSysts = merge_dicts(scaleSysts,resSysts,fracSysts)

for syst,factor in allSysts.iteritems():

    ##up
    fitter.w.var(syst).setVal(+3.)
    name = "histo_"+syst+"Up"
    template = fitter.w.pdf("model").createHistogram(name, fitter.w.var("MVV"), ROOT.RooFit.Binning(options.binsx,options.minx,options.maxx), ROOT.RooFit.YVar(fitter.w.var("MJJ"),ROOT.RooFit.Binning(options.binsy,options.miny,options.maxy)) ) 
    template.Write(name)
    fitter.w.var(syst).setVal(0.)

    ##down
    fitter.w.var(syst).setVal(-3.)
    name = "histo_"+syst+"Down"
    template = fitter.w.pdf("model").createHistogram(name, fitter.w.var("MVV"), ROOT.RooFit.Binning(options.binsx,options.minx,options.maxx), ROOT.RooFit.YVar(fitter.w.var("MJJ"),ROOT.RooFit.Binning(options.binsy,options.miny,options.maxy)) ) 
    template.Write(name)
    fitter.w.var(syst).setVal(0.)

F.Close()



## also store a version with fine binning
FDebug=ROOT.TFile(options.output+"_debug.root","RECREATE")
FDebug.cd()
##nominal
templateDebug = fitter.w.pdf("model").createHistogram("histo", fitter.w.var("MVV"), ROOT.RooFit.Binning(options.binsxfit,options.minx,options.maxx), ROOT.RooFit.YVar(fitter.w.var("MJJ"),ROOT.RooFit.Binning(options.binsyfit,options.miny,options.maxy)) ) 
templateDebug.Write("histo")
for syst,factor in allSysts.iteritems():
    ##up
    fitter.w.var(syst).setVal(+3.)
    name = "histo_"+syst+"Up"
    templateDebug = fitter.w.pdf("model").createHistogram(name, fitter.w.var("MVV"), ROOT.RooFit.Binning(options.binsxfit,options.minx,options.maxx), ROOT.RooFit.YVar(fitter.w.var("MJJ"),ROOT.RooFit.Binning(options.binsyfit,options.miny,options.maxy)) ) 
    templateDebug.Write(name)
    fitter.w.var(syst).setVal(0.)
    ##down
    fitter.w.var(syst).setVal(-3.)
    name = "histo_"+syst+"Down"
    templateDebug = fitter.w.pdf("model").createHistogram(name, fitter.w.var("MVV"), ROOT.RooFit.Binning(options.binsxfit,options.minx,options.maxx), ROOT.RooFit.YVar(fitter.w.var("MJJ"),ROOT.RooFit.Binning(options.binsyfit,options.miny,options.maxy)) ) 
    templateDebug.Write(name)
    fitter.w.var(syst).setVal(0.)
FDebug.Close()



## plot the parameter functions
funcs = fitter.w.allFunctions()
#fitter.w.Print()
#funcs.Print()
iter = funcs.createIterator()
func = iter.Next()
while func :
    #print func.GetName()
    fitter.plotCoef(func.GetName(),"MVV",options.outDir+"debug2DfitCoef_"+options.debugoutput+"_"+func.GetName()+".png","m_{WV} (GeV)",[ROOT.RooFit.LineColor(ROOT.kGreen+1)])
    func = iter.Next()



## plot the MC and template in MVV slices
axis=ROOT.TAxis(9,array('d',[800,900,1000,1250,1500,2000,2500,3000,3500,4000]))

histoProjMVV_=histo.Clone().ProjectionX('_px',1,histo.GetYaxis().GetNbins())
histoProjMVV=histoProjMVV_.Rebin(9,'hnew',array('d',[800,900,1000,1250,1500,2000,2500,3000,3500,4000]))
dataprojMVVrdh = ROOT.RooDataHist("dataprojMVVrdh","dataprojMVVrdh",ROOT.RooArgList(fitter.w.var("MVV")),histoProjMVV)
dataprojMVV = ROOT.RooHistPdf("dataprojMVV","dataprojMVV",ROOT.RooArgSet(fitter.w.var("MVV")),dataprojMVVrdh)
getattr(fitter.w,'import')(dataprojMVV,ROOT.RooFit.Rename('dataprojMVV'))
fitter.w.factory("PROD::modelUncond(model|MVV,dataprojMVV)")
#fitter.w.Print()

for i in range(1,axis.GetNbins()+1):

    fitter.w.var("MVV").setRange("slice_"+str(i),axis.GetBinLowEdge(i),axis.GetBinUpEdge(i))

    chi=fitter.projection("model","data","MJJ",options.outDir+"debug2Dfit_"+options.debugoutput+"_"+str(i)+"_cond.png","m_{jet} (GeV)",[ROOT.RooFit.CutRange("slice_"+str(i))],[ROOT.RooFit.ProjectionRange("slice_"+str(i)),ROOT.RooFit.LineColor(ROOT.kRed)])

    chi=fitter.projection("modelUncond","data","MJJ",options.outDir+"debug2Dfit_"+options.debugoutput+"_"+str(i)+".png","m_{jet} (GeV)",[ROOT.RooFit.CutRange("slice_"+str(i))],[ROOT.RooFit.ProjectionRange("slice_"+str(i))])


