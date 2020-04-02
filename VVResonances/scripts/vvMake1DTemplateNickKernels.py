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
parser.add_option("-N","--kdeFactor",dest="kdeFactor",type=int,help="factor to reduce stats",default=1)
(options,args) = parser.parse_args()


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
            dataPlotters[-1].addCorrectionFactor('lnujj_sf','branch')
            dataPlotters[-1].addCorrectionFactor('lnujj_btagWeight','branch')
            dataPlotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
            dataPlotters[-1].filename=fname
data=MergedPlotter(dataPlotters)



histI=data.drawTH1(options.var,options.cut,"1",1,0,1000000000)
norm=histI.Integral()


histograms={}
histograms['nominal'] = {'scale':1.0,'weight':'1'}
histograms['scale_Up'] = {'scale':1.2,'weight':'1'}
histograms['scale_Down'] = {'scale':0.8,'weight':'1'}
histograms['ptSpectrum_Up'] = {'scale':1.0,'weight':'(1.2*lnujj_l2_gen_pt)'}
histograms['ptSpectrum_Down'] = {'scale':1.0,'weight':'(0.8*lnujj_l2_gen_pt)'}

f=ROOT.TFile(options.output,"RECREATE")
f.cd()

for histo,info in histograms.iteritems():
    histSource =data.drawTH1(str(info['scale'])+'*'+options.var,'('+options.cut+'*'+info['weight']+')',"1",int(options.binsx*options.kdeFactor),options.minx*0.8,options.maxx*1.5)
    vectorx = ROOT.vector('double')()
    weight  = ROOT.vector('double')()

    for i in range(1,histSource.GetNbinsX()+1):
        content = histSource.GetBinContent(i)
        if content==0.0:
            continue;
        vectorx.push_back(histSource.GetXaxis().GetBinCenter(i))
        weight.push_back(content)


    kde=ROOT.KDEProducer(vectorx,weight, 1.0,options.binsx*options.kdeFactor,options.minx*0.8,options.maxx*1.5,5)        
    histogram = kde.getAPDF("h_"+histo,"h_"+histo,options.binsx,options.minx,options.maxx)
    histogram.Scale(histI.Integral()/histogram.Integral())
    histSource.Write("seedingHistogram_"+histo)
    histogram.Write()
f.Close()





