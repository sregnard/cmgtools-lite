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
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-f","--factor",dest="factor",type=int,help="factor to reduce stats",default=1)

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

def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        nominal=histo.GetBinContent(i)
        factor = alpha*pow(x,power) 
        newHistoU.SetBinContent(i,nominal*factor)
        newHistoD.SetBinContent(i,nominal/factor)
    return newHistoU,newHistoD        


def expandHisto(histo,histogram):
    graph=ROOT.TGraph(histo)
    for j in range(1,histogram.GetNbinsX()+1):
        x=histogram.GetXaxis().GetBinCenter(j)
        histogram.SetBinContent(j,graph.Eval(x,0,"S"))




random=ROOT.TRandom3(101082)

sampleTypes=options.samples.split(',')
dataPlotters=[]
dataPlottersNW=[]

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
            dataPlotters[-1].addCorrectionFactor('lnujj_sf','branch')
            dataPlotters[-1].addCorrectionFactor('lnujj_btagWeight','branch')
            dataPlotters[-1].addCorrectionFactor('truth_genTop_weight','branch')

            dataPlotters[-1].filename=fname
data=MergedPlotter(dataPlotters)


histogram=ROOT.TH1F("histo","histo",options.binsx,options.minx,options.maxx)
histogram.Sumw2()

histoCoarse=data.drawTH1(options.var,options.cut,"1",options.binsx/options.factor,options.minx,options.maxx)
expandHisto(histoCoarse,histogram)



f=ROOT.TFile(options.output,"RECREATE")
f.cd()
histoCoarse.Write("histo_coarse")

histogram.Write()
alpha=2.0/150
histogram_pt_down,histogram_pt_up=unequalScale(histogram,"histo_PT",alpha)
histogram_pt_down.Write()
histogram_pt_up.Write()
alpha=1.5*20
histogram_opt_down,histogram_opt_up=unequalScale(histogram,"histo_OPT",alpha,-1)
histogram_opt_down.Write()
histogram_opt_up.Write()
f.Close()




