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
parser.add_option("-r","--res",dest="res",help="res",default='')
parser.add_option("-H","--resHisto",dest="resHisto",help="res",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--var",dest="var",help="variable for x",default='')
parser.add_option("-u","--uncweight",dest="uncweight",help="weights for upward shape variation, split by comma",default='')
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
(options,args) = parser.parse_args()



def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        up=histo.GetBinContent(i)/intUp
        nominal=histoNominal.GetBinContent(i)/intNominal
        newHisto.SetBinContent(i,nominal*nominal/up)
    return newHisto        


def smoothTail(hist):

    bin_1200=hist.GetXaxis().FindBin(1200)
    if bin_1200>=hist.GetNbinsX()+1:
        return

    if hist.Integral()==0:
        print "Well we have  0 integrl for the hist ",hist.GetName()
        return

    expo=ROOT.TF1("func","{Y}*exp([0]*(x-{X}))".format(X=hist.GetBinCenter(bin_1200),Y=hist.GetBinContent(bin_1200)),0,8000)

    for j in range(1,hist.GetNbinsX()+1):
        if hist.GetBinContent(j)/hist.Integral()<0.0005:
            hist.SetBinError(j,1.8)

    hist.Fit(expo,"","",1200,8000)
    for j in range(1,hist.GetNbinsX()+1):
        x=hist.GetXaxis().GetBinCenter(j)
        if x>1200:
            hist.SetBinContent(j,expo.Eval(x))





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


fcorr=ROOT.TFile(options.res)

scale=fcorr.Get("scale"+options.resHisto+"Histo")
res=fcorr.Get("res"+options.resHisto+"Histo")


###Make res up and down
resUp = ROOT.TH1F(res)
resUp.SetName("resUp")
for i in range(1,res.GetNbinsX()+1):
    resUp.SetBinContent(i,res.GetBinContent(i)+0.3)



scaleUp = ROOT.TH1F(scale)
scaleUp.SetName("scaleUp")
scaleDown = ROOT.TH1F(scale)
scaleDown.SetName("scaleDown")
for i in range(1,res.GetNbinsX()+1):
    if options.resHisto=="x":
        scaleUp.SetBinContent(i,scale.GetBinContent(i)+0.1)
        scaleDown.SetBinContent(i,scale.GetBinContent(i)-0.1)
    else:
        scaleUp.SetBinContent(i,scale.GetBinContent(i)+0.3)
        scaleDown.SetBinContent(i,scale.GetBinContent(i)-0.3)




## Make histograms for uncertainty weights
uncWeights=options.uncweight.split(',')
uncw1=uncWeights[0]
uncw2=uncWeights[1]
hGenPtUp=ROOT.TH1F("hGenPtUp","hGenPtUp",5000,0,5000)
hGenPtDn=ROOT.TH1F("hGenPtDn","hGenPtDn",5000,0,5000)
hGenPt2Up=ROOT.TH1F("hGenPt2Up","hGenPt2Up",5000,0,5000)
hGenPt2Dn=ROOT.TH1F("hGenPt2Dn","hGenPt2Dn",5000,0,5000)
fGenPtUp=ROOT.TF1("fGenPtUp",uncw1.replace("lnujj_l2_gen_pt","x"),0,5000)
fGenPtDn=ROOT.TF1("fGenPtDn",'1/'+uncw1.replace("lnujj_l2_gen_pt","x"),0,5000)
fGenPt2Up=ROOT.TF1("fGenPt2Up",uncw2.replace("lnujj_l2_gen_pt","x"),0,5000)
fGenPt2Dn=ROOT.TF1("fGenPt2Dn",'1/'+uncw2.replace("lnujj_l2_gen_pt","x"),0,5000)
for i in range(5000):
    hGenPtUp.Fill(i+0.5,fGenPtUp.Eval(i+0.5))
    hGenPtDn.Fill(i+0.5,fGenPtDn.Eval(i+0.5))
    hGenPt2Up.Fill(i+0.5,fGenPt2Up.Eval(i+0.5))
    hGenPt2Dn.Fill(i+0.5,fGenPt2Dn.Eval(i+0.5))


histogram=ROOT.TH1F("histo","histo",options.binsx,options.minx,options.maxx)
histogram.Sumw2()
histogram_gpt_up=ROOT.TH1F("histo_GPTUp","histo",options.binsx,options.minx,options.maxx)
histogram_gpt_down=ROOT.TH1F("histo_GPTDown","histo",options.binsx,options.minx,options.maxx)
histogram_gpt2_up=ROOT.TH1F("histo_GPT2Up","histo",options.binsx,options.minx,options.maxx)
histogram_gpt2_down=ROOT.TH1F("histo_GPT2Down","histo",options.binsx,options.minx,options.maxx)

'''
histogram_res_up=ROOT.TH1F("histo_ResUp","histo",options.binsx,options.minx,options.maxx)
histogram_res_up.Sumw2()

histogram_scale_up=ROOT.TH1F("histo_ScaleUp","histo",options.binsx,options.minx,options.maxx)
histogram_scale_up.Sumw2()
histogram_scale_down=ROOT.TH1F("histo_ScaleDown","histo",options.binsx,options.minx,options.maxx)
histogram_scale_down.Sumw2()

histogram_top_up=ROOT.TH1F("histo_TOPUp","histo",options.binsx,options.minx,options.maxx)
histogram_top_up.Sumw2()
histogram_top_down=ROOT.TH1F("histo_TOPDown","histo",options.binsx,options.minx,options.maxx)
histogram_top_down.Sumw2()
#'''

#histogram_pt_up=ROOT.TH1F("histo_PTUp","histo",options.binsx,options.minx,options.maxx)
#histogram_pt_up.Sumw2()
#histogram_pt_down=ROOT.TH1F("histo_PTDown","histo",options.binsx,options.minx,options.maxx)
#histogram_pt_down.Sumw2()

histograms=[
    histogram,
    histogram_gpt_up,
    histogram_gpt_down,
    histogram_gpt2_up,
    histogram_gpt2_down,
#    histogram_res_up,
#    histogram_scale_up,
#    histogram_scale_down,
#    histogram_top_up,
#    histogram_top_down,
#    histogram_pt_up,
#    histogram_pt_down,
]

#ok lets populate!




for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):
    histI=plotter.drawTH1(options.var,options.cut,"1",1,0,1000000000)
    norm=histI.Integral()

    #nominal
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    if options.var != 'lnujj_gen_partialMass':
        dataset=plotter.makeDataSet('lnujj_l1_pt,lnujj_gen_partialMass,lnujj_l2_gen_pt,'+options.var,options.cut,-1)
    else:
        dataset=plotter.makeDataSet('lnujj_l1_pt,lnujj_l2_gen_pt,'+options.var,options.cut,-1)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP);
    if histTMP.Integral()>0:
    #    histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram.Add(histTMP)
    histTMP.Delete()

    #'''
    #gen pt up (linear)
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,'lnujj_l2_gen_pt',hGenPtUp)
    if histTMP.Integral()>0:
        histogram_gpt_up.Add(histTMP)
    histTMP.Delete()

    #gen pt down (linear)
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,'lnujj_l2_gen_pt',hGenPtDn)
    if histTMP.Integral()>0:
        histogram_gpt_down.Add(histTMP)
    histTMP.Delete()

    #gen pt up (quadratic)
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,'lnujj_l2_gen_pt',hGenPt2Up)
    if histTMP.Integral()>0:
        histogram_gpt2_up.Add(histTMP)
    histTMP.Delete()

    #gen pt down (quadratic)
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,'lnujj_l2_gen_pt',hGenPt2Dn)
    if histTMP.Integral()>0:
        histogram_gpt2_down.Add(histTMP)
    histTMP.Delete()
    #'''

    '''
        if "TT" in plotterNW.filename:
            histogram_top_up.Add(histTMP,2.0)
            histogram_top_down.Add(histTMP,0.5)
        else:
            histogram_top_up.Add(histTMP,1.0)
            histogram_top_down.Add(histTMP,1.0)


    #res Up
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,resUp,histTMP);
    if histTMP.Integral()>0:
        histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_res_up.Add(histTMP)
    histTMP.Delete()



    #scale Up
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scaleUp,res,histTMP);
    if histTMP.Integral()>0:
        histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_scale_up.Add(histTMP)
    histTMP.Delete()


    #scale Down
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scaleDown,res,histTMP);
    if histTMP.Integral()>0:
        histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_scale_down.Add(histTMP)
    histTMP.Delete()

    #pt Up
#    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
#    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,options.var,ptUp);
#    if histTMP.Integral()>0:
#        histTMP.Scale(histI.Integral()/histTMP.Integral())
#        histogram_pt_up.Add(histTMP)
#    histTMP.Delete()

    #pt Down
#    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
#    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,options.var,ptDown);
#    if histTMP.Integral()>0:
#        histTMP.Scale(histI.Integral()/histTMP.Integral())
#        histogram_pt_down.Add(histTMP)
#    histTMP.Delete()
     #'''

f=ROOT.TFile(options.output,"RECREATE")
f.cd()

finalHistograms={}
for hist in histograms:
    hist.Write(hist.GetName()+"_raw")
    smoothTail(hist)
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
hGenPt2Up.Write("hGenPt2Up")
hGenPt2Dn.Write("hGenPt2Dn")

f.Close()




