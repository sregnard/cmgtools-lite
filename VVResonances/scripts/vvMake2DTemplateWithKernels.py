#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import json
import copy
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
ROOT.gSystem.Load("libCMGToolsVVResonances")
from loadNtuples import *

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-r","--res",dest="res",help="res",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--vars",dest="vars",help="variable for x",default='')
parser.add_option("-u","--uncweight",dest="uncweight",help="weights for upward shape variation, split by comma",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="conditional bins split by comma",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-y","--miny",dest="miny",type=float,help="bins",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-l","--limit",dest="limit",type=float,help="lower limit of the high-mass smoothing range",default=2500)
parser.add_option("-t","--tails",dest="tails",type=int,help="method for tail smoothing: 1: all bins together (default); 2: do lowest 4 bins independently",default=1)
(options,args) = parser.parse_args()

DEBUG=0


def addToYSlice(h2,b,h1):
    for i in range(1,h2.GetNbinsX()+1):
        h2.Fill(h2.GetXaxis().GetBinLowEdge(i),h2.GetYaxis().GetBinLowEdge(b),h1.GetBinContent(i))
        #print 'addToYSlice', i, b, h1.GetBinContent(i), h2.GetBinContent(i,b)


def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        for j in range(1,histo.GetNbinsY()+1):
            up=histo.GetBinContent(i,j)/intUp
            nominal=histoNominal.GetBinContent(i,j)/intNominal
            newHisto.SetBinContent(i,j,nominal*nominal/up)
    return newHisto        


def expandHisto(histo,options):
    histogram=ROOT.TH2F(histo.GetName(),"histo",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    graph=ROOT.TGraph2D(histo)
    for i in range(1,histogram.GetNbinsX()+1):
        for j in range(1,histogram.GetNbinsY()+1):
            if histogram.GetYaxis().GetBinCenter(j)>histo.GetYaxis().GetBinCenter(1) and histogram.GetYaxis().GetBinCenter(j)<histo.GetYaxis().GetBinCenter(histo.GetNbinsY()): 
                histogram.SetBinContent(i,j,graph.Interpolate(histogram.GetXaxis().GetBinCenter(i),histogram.GetYaxis().GetBinCenter(j)))
            else:
                histogram.SetBinContent(i,j,histo.GetBinContent(histo.FindBin(histogram.GetXaxis().GetBinCenter(i),histogram.GetYaxis().GetBinCenter(j))))
    return histogram
        


def conditional(hist):
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)



def smoothTail(hist):
    hist.Scale(1.0/hist.Integral())

    bin_limit = hist.GetXaxis().FindBin(options.limit)

    histfit=hist.ProjectionX("q",1,hist.GetNbinsY())
    X=histfit.GetBinCenter(bin_limit)
    Y=histfit.GetBinContent(bin_limit)
    print 'X', X, 'Y', Y
    fun=ROOT.TF1("func","{Y}*(((x-[1])/({X}-[1]))^[0])".format(X=X,Y=Y),options.limit,options.maxx)
    fun.SetParameter(0,-10.)
    histfit.Fit(fun,"WL,R")

    for i in range(1,hist.GetNbinsX()+1):
        x=hist.GetXaxis().GetBinCenter(i)
        if x>options.limit:
            for j in range(1,hist.GetNbinsY()+1):
                hist.SetBinContent(i,j,fun.Eval(x)*hist.GetBinContent(bin_limit,j)/fun.Eval(histfit.GetBinCenter(bin_limit)))

def smoothTail_4LowestBinsIndep(hist):
    hist.Scale(1.0/hist.Integral())

    bin_limit = hist.GetXaxis().FindBin(options.limit)

    histfit=hist.ProjectionX("q",4,hist.GetNbinsY())
    X=histfit.GetBinCenter(bin_limit)
    Y=histfit.GetBinContent(bin_limit)
    print 'X', X, 'Y', Y
    fun=ROOT.TF1("func","{Y}*(((x-[1])/({X}-[1]))^[0])".format(X=X,Y=Y),options.limit,options.maxx)
    fun.SetParameter(0,-10.)
    histfit.Fit(fun,"WL,R")

    for i in range(1,hist.GetNbinsX()+1):
        x=hist.GetXaxis().GetBinCenter(i)
        if x>options.limit:
            for j in range(4,hist.GetNbinsY()+1):
                hist.SetBinContent(i,j,fun.Eval(x)*hist.GetBinContent(bin_limit,j)/fun.Eval(histfit.GetBinCenter(bin_limit)))

    for j in range(1,4):
        y=hist.GetYaxis().GetBinCenter(j)

        histfit=hist.ProjectionX("q_"+str(j),j,j)
        X=histfit.GetBinCenter(bin_limit)
        Y=histfit.GetBinContent(bin_limit)
        print 'X', X, 'Y', Y
        fun=ROOT.TF1("func","{Y}*(((x-[1])/({X}-[1]))^[0])".format(X=X,Y=Y),options.limit,options.maxx)
        fun.SetParameter(0,-10.)
        histfit.Fit(fun,"WL,R")

        for i in range(1,hist.GetNbinsX()+1):
            x=hist.GetXaxis().GetBinCenter(i)
            if x>options.limit:
                hist.SetBinContent(i,j,fun.Eval(x)*hist.GetBinContent(bin_limit,j)/fun.Eval(histfit.GetBinCenter(bin_limit)))








data=loadNtuples(options.samples,args[0])


fcorr=ROOT.TFile(options.res)
scale_x=fcorr.Get("scalexHisto")
#scale_y=fcorr.Get("scaleyHisto")
res_x=fcorr.Get("resxHisto")
#res_y=fcorr.Get("resyHisto")


variables=options.vars.split(',')


binsx=[]
for i in range(0,options.binsx+1):
    binsx.append(options.minx+i*(options.maxx-options.minx)/options.binsx)

binsy=[20.,25.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,140.,150.,160.,180.,210.]    


###Make res up and down
resUp = ROOT.TH1F(res_x)
resUp.SetName("resUp")
for i in range(1,res_x.GetNbinsX()+1):
    resUp.SetBinContent(i,res_x.GetBinContent(i)+0.3)


## Make histograms for uncertainty weights
#uncWeights=options.uncweight.split(',')
#uncw1=uncWeights[0]
#uncw2=uncWeights[1]
#hGenPtUp=ROOT.TH1F("hGenPtUp","hGenPtUp",5000,0,5000)
#hGenPtDn=ROOT.TH1F("hGenPtDn","hGenPtDn",5000,0,5000)
#hGenPt2Up=ROOT.TH1F("hGenPt2Up","hGenPt2Up",5000,0,5000)
#hGenPt2Dn=ROOT.TH1F("hGenPt2Dn","hGenPt2Dn",5000,0,5000)
#fGenPtUp=ROOT.TF1("fGenPtUp",uncw1.replace("lnujj_l2_gen_pt","x"),0,5000)
#fGenPtDn=ROOT.TF1("fGenPtDn",'1/'+uncw1.replace("lnujj_l2_gen_pt","x"),0,5000)
#fGenPt2Up=ROOT.TF1("fGenPt2Up",uncw2.replace("lnujj_l2_gen_pt","x"),0,5000)
#fGenPt2Dn=ROOT.TF1("fGenPt2Dn",'1/'+uncw2.replace("lnujj_l2_gen_pt","x"),0,5000)
#for i in range(5000):
#    hGenPtUp.Fill(i+0.5,fGenPtUp.Eval(i+0.5))
#    hGenPtDn.Fill(i+0.5,fGenPtDn.Eval(i+0.5))
#    hGenPt2Up.Fill(i+0.5,fGenPt2Up.Eval(i+0.5))
#    hGenPt2Dn.Fill(i+0.5,fGenPt2Dn.Eval(i+0.5))


histogram=ROOT.TH2F("histo","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_MVVScale_up=ROOT.TH2F("histo_MVVScaleUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_MVVScale_down=ROOT.TH2F("histo_MVVScaleDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_Diag_up=ROOT.TH2F("histo_DiagUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_Diag_down=ROOT.TH2F("histo_DiagDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

histograms=[
    histogram,
    histogram_MVVScale_up,
    histogram_MVVScale_down,
    histogram_Diag_up,
    histogram_Diag_down,
]




output=options.output
for plotter in data.plotters:

    dataset=plotter.makeDataSet('lnujj_l1_pt,lnujj_l2_gen_pt,'+variables[1]+','+variables[0],options.cut,-1)

    reweigh_p0=1.0
    reweigh_p1=0.0
    if "nonRes" in output and not("CR" in output):
        if "DEtaLo" in output:
            if "_HP_" in output:
                if "_bb_" in output:
                    reweigh_p0=-5.11351e-02; reweigh_p1=9.48416e+02
                elif "_nobb_" in output:
                    reweigh_p0=7.64206e-01; reweigh_p1=2.12583e+02
                elif "_vbf_" in output:
                    reweigh_p0=1.22312e+00; reweigh_p1=-1.30739e+02
            elif "_LP_" in output: 
                if "_bb_" in output:
                    reweigh_p0=3.23885e-01; reweigh_p1=5.97861e+02 
                elif "_nobb_" in output:
                    reweigh_p0=6.42083e-01; reweigh_p1=3.15756e+02
                elif "_vbf_" in output:
                    reweigh_p0=7.66046e-01; reweigh_p1=2.05378e+02
        elif "DEtaHi" in output:
            if "_HP_" in output:
                if "_bb_" in output:
                    reweigh_p0=1.42547e-01; reweigh_p1=8.25972e+02
                elif "_nobb_" in output:
                    reweigh_p0=9.33242e-01; reweigh_p1=6.24309e+01
                elif "_vbf_" in output:
                    reweigh_p0=1.78506e+00; reweigh_p1=-6.93369e+02
            elif "_LP_" in output: 
                if "_bb_" in output:
                    reweigh_p0=4.43246e-01; reweigh_p1=5.30202e+02
                elif "_nobb_" in output:
                    reweigh_p0=7.87605e-01; reweigh_p1=2.02196e+02
                elif "_vbf_" in output:
                    reweigh_p0=1.32359e+00; reweigh_p1=-3.03538e+02
        elif "allE" in output:
            if "_HP_" in output:
                if "_bb_" in output:
                    reweigh_p0=9.22987e-03; reweigh_p1=9.06804e+02
                elif "_nobb_" in output:
                    reweigh_p0=7.23583e-01; reweigh_p1=2.50664e+02
                elif "_vbf_" in output:
                    reweigh_p0=1.29390e+00; reweigh_p1=-1.90990e+02
            elif "_LP_" in output: 
                if "_bb_" in output:
                    reweigh_p0=4.92293e-01; reweigh_p1=4.56496e+02
                elif "_nobb_" in output:
                    reweigh_p0=6.15018e-01; reweigh_p1=3.43643e+02
                elif "_vbf_" in output:
                    reweigh_p0=8.32691e-01; reweigh_p1=1.46536e+02

    datamaker=ROOT.cmg.ConditionalGaussianSumTemplateMaker(dataset,variables[0],variables[1],'lnujj_l2_gen_pt',scale_x,res_x,histogram,histogram_MVVScale_up,histogram_MVVScale_down,histogram_Diag_up,histogram_Diag_down,reweigh_p0,reweigh_p1);


f=ROOT.TFile(options.output,"RECREATE")
f.cd()

finalHistograms={}
for hist in histograms:
    hist.Write(hist.GetName()+"_coarse")
    if options.tails==1:
        smoothTail(hist)
    elif options.tails==2:
        smoothTail_4LowestBinsIndep(hist)
    hist.Write(hist.GetName()+"_coarsesmoothed")
    conditional(hist)
    hist.Write(hist.GetName()+"_coarsesmoothedcond")
    expanded=expandHisto(hist,options)
    expanded.Write(hist.GetName()+"_expanded")
    conditional(expanded)
    expanded.Write()
    finalHistograms[hist.GetName()]=expanded



#hGenPtUp.Write("hGenPtUp")
#hGenPtDn.Write("hGenPtDn")
#hGenPt2Up.Write("hGenPt2Up")
#hGenPt2Dn.Write("hGenPt2Dn")

f.Close()




