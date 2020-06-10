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
from loadSamples import *

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--var",dest="var",help="variable for x",default='')
parser.add_option("-V","--varalt",dest="varalt",help="alternative variables for shape variation: up,down",default='')
parser.add_option("-u","--uncweight",dest="uncweight",help="weights for upward shape variation, split by comma",default='')
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-f","--factor",dest="factor",type=int,help="factor to reduce stats",default=1)
(options,args) = parser.parse_args()


def amplify(histo,histoNominal,factor=10):
    histo.Scale(histo.Integral())
    histoNominal.Scale(histoNominal.Integral())
    for i  in range(1,histo.GetNbinsX()+1):
        c=histo.GetBinContent(i)
        g=histoNominal.GetBinContent(i)
        newC = g+ (c-g)*factor
        histo.SetBinContent(i,newC)
        


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
        factor = 1+alpha*pow(x,power) 
        newHistoU.SetBinContent(i,nominal*factor)
        newHistoD.SetBinContent(i,nominal/factor)
    return newHistoU,newHistoD    


def expandHisto(histo,histogram):
    graph=ROOT.TGraph(histo)
    for j in range(1,histogram.GetNbinsX()+1):
        x=histogram.GetXaxis().GetBinCenter(j)
        histogram.SetBinContent(j,graph.Eval(x,0,"S"))




random=ROOT.TRandom3(101082)


data=loadSamples(options.samples,args[0])


uncWeights=options.uncweight.split(',')
uncw1=uncWeights[0]
uncw2=uncWeights[1]

cut=options.cut
var=options.var
altVariables=options.varalt.split(',')
varup=altVariables[0]
vardown=altVariables[1]

histogram=ROOT.TH1F("histo","histo",options.binsx,options.minx,options.maxx)
histogram.Sumw2()
histogram_gpt_up=ROOT.TH1F("histo_logWeightUp","histo",options.binsx,options.minx,options.maxx)
histogram_gpt_up.Sumw2()
histogram_gpt_down=ROOT.TH1F("histo_logWeightDown","histo",options.binsx,options.minx,options.maxx)
histogram_gpt_down.Sumw2()
histogram_gpt2_up=ROOT.TH1F("histo_MJJScaleUp","histo",options.binsx,options.minx,options.maxx)
histogram_gpt2_up.Sumw2()
histogram_gpt2_down=ROOT.TH1F("histo_MJJScaleDown","histo",options.binsx,options.minx,options.maxx)
histogram_gpt2_down.Sumw2()
histogram_sd_up=ROOT.TH1F("histo_SDUp","histo",options.binsx,options.minx,options.maxx)
histogram_sd_up.Sumw2()
histogram_sd_down=ROOT.TH1F("histo_SDDown","histo",options.binsx,options.minx,options.maxx)
histogram_sd_down.Sumw2()

newNbins=options.binsx/options.factor 
newBinWidth=(options.maxx-options.minx)/newNbins
histoCoarse=data.drawTH1(var,cut,"1",newNbins+1,options.minx,options.maxx+newBinWidth)
expandHisto(histoCoarse,histogram)
histoCoarse_gpt_up=data.drawTH1(var,cut+'*(1+'+uncw1+')',"1",newNbins+1,options.minx,options.maxx+newBinWidth)
expandHisto(histoCoarse_gpt_up,histogram_gpt_up)
histoCoarse_gpt_down=data.drawTH1(var,cut+'*(1.0/(1+'+uncw1+'))',"1",newNbins+1,options.minx,options.maxx+newBinWidth)
expandHisto(histoCoarse_gpt_down,histogram_gpt_down)
histoCoarse_gpt2_up=data.drawTH1(var,cut+'*(1+'+uncw2+')',"1",newNbins+1,options.minx,options.maxx+newBinWidth)
expandHisto(histoCoarse_gpt2_up,histogram_gpt2_up)
histoCoarse_gpt2_down=data.drawTH1(var,cut+'*(1.0/(1+'+uncw2+'))',"1",newNbins+1,options.minx,options.maxx+newBinWidth)
expandHisto(histoCoarse_gpt2_down,histogram_gpt2_down)
histoCoarse_sd_up=data.drawTH1(varup,cut.replace(var,varup),"1",newNbins+1,options.minx,options.maxx+newBinWidth)
expandHisto(histoCoarse_sd_up,histogram_sd_up)
#histoCoarse_sd_down=data.drawTH1(vardown,cut.replace(var,vardown),"1",newNbins+1,options.minx,options.maxx+newBinWidth)
#expandHisto(histoCoarse_sd_down,histogram_sd_down)

#amplify(histogram_sd_down,histogram)

histogram_sd_down=mirror(histogram_sd_up,histogram,"histo_SDDown")


f=ROOT.TFile(options.output,"RECREATE")
f.cd()
histoCoarse.Write("histo_coarse")


histogram.Write()
histogram_gpt_up.Write()
histogram_gpt_down.Write()
histogram_gpt2_up.Write()
histogram_gpt2_down.Write()
histogram_sd_up.Write()
histogram_sd_down.Write()




alpha=1.5/210
histogram_pt_down,histogram_pt_up=unequalScale(histogram,"histo_PT",alpha)
histogram_pt_down.Write()
histogram_pt_up.Write()
alpha=1.5*30
histogram_opt_down,histogram_opt_up=unequalScale(histogram,"histo_OPT",alpha,-1)
histogram_opt_down.Write()
histogram_opt_up.Write()
f.Close()
