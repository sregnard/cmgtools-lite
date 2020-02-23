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
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
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

#    fTemp=ROOT.TFile("checkFitTails.root","RECREATE")
#    fTemp.cd()
#    histfit.Write()
#    fTemp.Close()

    for i in range(1,hist.GetNbinsX()+1):
        x=hist.GetXaxis().GetBinCenter(i)
        if x>options.limit:
            for j in range(1,hist.GetNbinsY()+1):
                hist.SetBinContent(i,j,fun.Eval(x)*hist.GetBinContent(bin_limit,j)/fun.Eval(histfit.GetBinCenter(bin_limit)))





random=ROOT.TRandom3(101082)


sampleTypes=options.samples.split(',')
dataPlotters=[]

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
            #dataPlotters[-1].addCorrectionFactor(options.uncweight,'branch')
            dataPlotters[-1].filename = fname


data=MergedPlotter(dataPlotters)


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


histogram=ROOT.TH2F("histo","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_gpt_up=ROOT.TH2F("histo_GPTUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_gpt_down=ROOT.TH2F("histo_GPTDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_gpt2_up=ROOT.TH2F("histo_GPT2Up","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_gpt2_down=ROOT.TH2F("histo_GPT2Down","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

histograms=[
    histogram,
    histogram_gpt_up,
    histogram_gpt_down,
    histogram_gpt2_up,
    histogram_gpt2_down,
]





for plotter in dataPlotters:

    for b in range(1,histogram.GetNbinsY()+1):

        bincut = options.cut+"*("+str(histogram.GetYaxis().GetBinLowEdge(b))+"<"+variables[1]+")*("+variables[1]+"<"+str(histogram.GetYaxis().GetBinUpEdge(b))+")"

        dataset=plotter.makeDataSet('lnujj_l1_pt,lnujj_l2_gen_pt,'+variables[1]+','+variables[0],bincut,-1)

        ##nominal
        histTMP=ROOT.TH1F("histoTMP","histo",len(binsx)-1,array('f',binsx))
        datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,variables[0],'lnujj_l2_gen_pt',scale_x,res_x,histTMP)
        if histTMP.Integral()>0:
            addToYSlice(histogram,b,histTMP)
            #print histTMP.Integral(), histogram.Integral()
        histTMP.Delete()

        #'''
        ##gen pt up (linear)
        histTMP=ROOT.TH1F("histoTMP","histo",len(binsx)-1,array('f',binsx))
        datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,variables[0],'lnujj_l2_gen_pt',scale_x,res_x,histTMP,'lnujj_l2_gen_pt',hGenPtUp)
        if histTMP.Integral()>0:
            addToYSlice(histogram_gpt_up,b,histTMP)
        histTMP.Delete()

        ##gen pt down (linear)
        histTMP=ROOT.TH1F("histoTMP","histo",len(binsx)-1,array('f',binsx))
        datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,variables[0],'lnujj_l2_gen_pt',scale_x,res_x,histTMP,'lnujj_l2_gen_pt',hGenPtDn)
        if histTMP.Integral()>0:
            addToYSlice(histogram_gpt_down,b,histTMP)
        histTMP.Delete()

        ##gen pt up (quadratic)
        histTMP=ROOT.TH1F("histoTMP","histo",len(binsx)-1,array('f',binsx))
        datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,variables[0],'lnujj_l2_gen_pt',scale_x,res_x,histTMP,'lnujj_l2_gen_pt',hGenPt2Up)
        if histTMP.Integral()>0:
            addToYSlice(histogram_gpt2_up,b,histTMP)
        histTMP.Delete()

        ##gen pt down (quadratic)
        histTMP=ROOT.TH1F("histoTMP","histo",len(binsx)-1,array('f',binsx))
        datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,variables[0],'lnujj_l2_gen_pt',scale_x,res_x,histTMP,'lnujj_l2_gen_pt',hGenPt2Dn)
        if histTMP.Integral()>0:
            addToYSlice(histogram_gpt2_down,b,histTMP)
        histTMP.Delete()
        #'''



f=ROOT.TFile(options.output,"RECREATE")
f.cd()

finalHistograms={}
for hist in histograms:
    hist.Write(hist.GetName()+"_coarse")
    smoothTail(hist)
    hist.Write(hist.GetName()+"_coarsesmoothed")
    conditional(hist)
    hist.Write(hist.GetName()+"_coarsesmoothedcond")
    expanded=expandHisto(hist,options)
    expanded.Write(hist.GetName()+"_expanded")
    conditional(expanded)
    expanded.Write()
    finalHistograms[hist.GetName()]=expanded



hGenPtUp.Write("hGenPtUp")
hGenPtDn.Write("hGenPtDn")
hGenPt2Up.Write("hGenPt2Up")
hGenPt2Dn.Write("hGenPt2Dn")

f.Close()




