#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import copy
import json
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
ROOT.gSystem.Load("libCMGToolsVVResonances")

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--var",dest="var",help="variable for x",default='')
parser.add_option("-u","--uncweight",dest="uncweight",help="weights for upward shape variation, split by comma",default='')
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
(options,args) = parser.parse_args()





random=ROOT.TRandom3(101082)


sampleTypes=options.samples.split(',')
dataPlotters=[]
dataPlottersNW=[]

filelist = []
if args[0]=='ntuples':
    filelist = [g for flist in [[(path+'/'+f) for f in os.listdir(args[0]+'/'+path)] for path in os.listdir(args[0])] for g in flist]
else:
    filelist = os.listdir(args[0])

for filename in filelist:
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
            dataPlotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
            ##dataPlotters[-1].addCorrectionFactor('lnujj_sf','branch')
            ##dataPlotters[-1].addCorrectionFactor('lnujj_btagWeight','branch')
            dataPlotters[-1].filename=fname

            dataPlottersNW.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            dataPlottersNW[-1].addCorrectionFactor('genWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor('puWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor('truth_genTop_weight','branch')
            ##dataPlottersNW[-1].addCorrectionFactor('lnujj_sf','branch')
            ##dataPlottersNW[-1].addCorrectionFactor('lnujj_btagWeight','branch')
            dataPlottersNW[-1].filename=fname

data=MergedPlotter(dataPlotters)








## Make histograms for uncertainty weights
uncWeights=options.uncweight.split(',')
uncw1=uncWeights[0]
hGenPtUp=ROOT.TH1F("hGenPtUp","hGenPtUp",5000,0,5000)
hGenPtDn=ROOT.TH1F("hGenPtDn","hGenPtDn",5000,0,5000)
fGenPtUp=ROOT.TF1("fGenPtUp",uncw1.replace("lnujj_l2_gen_pt","x"),0,5000)
fGenPtDn=ROOT.TF1("fGenPtDn",'1/'+uncw1.replace("lnujj_l2_gen_pt","x"),0,5000)
for i in range(5000):
    hGenPtUp.Fill(i+0.5,fGenPtUp.Eval(i+0.5))
    hGenPtDn.Fill(i+0.5,fGenPtDn.Eval(i+0.5))





histograms=[
]

#ok lets populate!


fitter=Fitter(['M'])
fitter.w.var("M").setVal((options.maxx-options.minx)/2.0)
fitter.w.var("M").setMax(options.maxx)
fitter.w.var("M").setMin(options.minx)
fitter.factory("GM[15,215]")
fitter.factory("weight[0,1e+32]")

   
#datasetPDF=data.makeDataSet('lnujj_l2_gen_softDrop_mass,'+options.var,options.cut,-1)
histoPDF=data.drawTH1('lnujj_l2_gen_softDrop_mass',options.cut,"1",options.binsx*4,options.minx,options.maxx)




fitter.w.var("GM").setMin(histoPDF.GetXaxis().GetXmin())
fitter.w.var("GM").setMax(histoPDF.GetXaxis().GetXmax())
fitter.w.var("GM").setBins(histoPDF.GetXaxis().GetNbins())


cList = ROOT.RooArgSet(fitter.w.var("GM"),fitter.w.var("weight"))


fcache=ROOT.TFile("cache.root","RECREATE")
dataset=ROOT.RooDataSet("datasetPDF","",cList,"weight")
for i in range(1,histoPDF.GetNbinsX()+1):
    x = histoPDF.GetXaxis().GetBinCenter(i)
    w = histoPDF.GetBinContent(i)
    cList.setRealValue("GM",x)
    cList.setRealValue("weight",w)
    dataset.add(cList,w)


fitter=Fitter(['M'])
fitter.w.var("M").setVal((options.maxx-options.minx)/2.0)
fitter.w.var("M").setMax(options.maxx)
fitter.w.var("M").setMin(options.minx)

fitter.gaussianSum("model","M",dataset,"GM")

histo=data.drawTH1(options.var,options.cut,"1",options.binsx*4,options.minx,options.maxx)
fitter.importBinnedData(histo,"M")
fitter.fit()
scale=fitter.w.var("scale").getVal()
sigma=fitter.w.var("sigma").getVal()
fitter.projection("model","data","M",options.output+"_debug.png")

h=fitter.w.pdf("model").createHistogram("M",options.binsx)
h.SetName("histo")
histograms.append(h)

#scaleUp
fitter.w.var("scale").setVal(scale*1.15)
h=fitter.w.pdf("model").createHistogram("M",options.binsx)
h.SetName("histo_scaleUp")
histograms.append(h)

#scaleDn
fitter.w.var("scale").setVal(scale*0.85)
h=fitter.w.pdf("model").createHistogram("M",options.binsx)
h.SetName("histo_scaleDown")
histograms.append(h)

fitter.w.var("scale").setVal(scale)
fitter.w.var("sigma").setVal(sigma*1.25)
h=fitter.w.pdf("model").createHistogram("M",options.binsx)
h.SetName("histo_resUp")
histograms.append(h)


fitter.w.var("sigma").setVal(sigma*0.75)
h=fitter.w.pdf("model").createHistogram("M",options.binsx)
h.SetName("histo_resDown")
histograms.append(h)

fitter.w.var("scale").setVal(scale)
fitter.w.var("sigma").setVal(sigma)






    


 


#    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)


    #gen pt up (linear)
#    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_mass',scale,res,histogram_gpt_up,histTMP,histTMP,histTMP,histTMP,'lnujj_l2_gen_pt',hGenPtUp)
#    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_mass',scale,res,histogram_gpt_up,histTMP,histTMP,histTMP,histTMP,'lnujj_l2_gen_pt',hGenPtDn)

#    histTMP.Delete()

f=ROOT.TFile(options.output,"RECREATE")
f.cd()

histoPDF.Write("histoPDF")

finalHistograms={}
for hist in histograms:
    hist.Write(hist.GetName()+"_raw")
    hist.Write(hist.GetName())
    finalHistograms[hist.GetName()]=hist



#histogram_res_down=mirror(finalHistograms['histo_ResUp'],finalHistograms['histo'],"histo_ResDown")
#histogram_res_down.Write()


#scaleUp.Write("scaleUp")
#scaleDown.Write("scaleDown")
#ptUp.Write("weightPTUp")
#ptDown.Write("weightPTDown")
#resUp.Write("resUp")
#resDown.Write("resDown")
#ptUp.Write("ptUp")
#ptDown.Write("ptDown")
#wptUp.Write("wptUp")
#wptDown.Write("wptDown")

#quarkGluonUp.Write("qgUp")
#quarkGluonDown.Write("qgDwn")

hGenPtUp.Write("hGenPtUp")
hGenPtDn.Write("hGenPtDn")


f.Close()




