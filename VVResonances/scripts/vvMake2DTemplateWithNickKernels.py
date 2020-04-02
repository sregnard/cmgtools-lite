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
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--vars",dest="vars",help="variable for x",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="conditional bins split by comma",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-y","--miny",dest="miny",type=float,help="bins",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-N","--kdeFactor",dest="kdeFactor",type=int,help="KDE factor to make more bins",default=100)


DEBUG=0


def conditional(hist):
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)

(options,args) = parser.parse_args()

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
            dataPlotters[-1].filename = fname
data=MergedPlotter(dataPlotters)
variables=options.vars.split(',')

histI=data.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
norm=histI.Integral()


histograms={}
histograms['nominal'] = {'scalex':1.0,'scaley':1.0,'weight':'1'}
histograms['scalex_Up'] = {'scalex':1.2,'scaley':1.0,'weight':'1'}
histograms['scalex_Down'] = {'scalex':0.8,'scaley':1.0,'weight':'1'}
histograms['ptSpectrum_Up'] = {'scalex':1.0,'scaley':1.0,'weight':'(1.1*lnujj_l2_gen_pt)'}
histograms['ptSpectrum_Down'] = {'scalex':1.0,'scaley':1.0,'weight':'(0.8*lnujj_l2_gen_pt)'}

f=ROOT.TFile(options.output,"RECREATE")
f.cd()

for histo,info in histograms.iteritems():
    histSource =data.drawTH2(str(info['scaley'])+'*'+variables[1]+':'+str(info['scalex'])+'*'+variables[0],'('+options.cut+'*'+info['weight']+')',"1",int(options.binsx*options.kdeFactor),options.minx*0.8,options.maxx*1.5,int(options.binsy*options.kdeFactor),options.miny*0.8,options.maxy*1.5)
    vectorx = ROOT.vector('double')()
    vectory = ROOT.vector('double')()
    weight  = ROOT.vector('double')()

    for i in range(1,histSource.GetNbinsX()+1):
        for j in range(1,histSource.GetNbinsY()+1):
            bin=histSource.GetBin(i,j)
            content = histSource.GetBinContent(bin)
            if content==0.0:
                continue;
            vectorx.push_back(histSource.GetXaxis().GetBinCenter(i))
            vectory.push_back(histSource.GetYaxis().GetBinCenter(j))
            weight.push_back(content)


    kde=ROOT.KDEProducer2D(vectorx,vectory,weight, 1.0,options.binsx*options.kdeFactor,options.minx*0.8,options.maxx*1.5,5,1.0,options.binsy*options.kdeFactor,options.miny*0.5,options.maxy*1.5,5.0)        
    histogram = kde.getAPDF("h_"+histo,"h_"+histo,options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    histogram.Scale(histI.Integral()/histogram.Integral())
    histSource.Write("seedingHistogram_"+histo)
    histogram.Write()
    conditional(histogram)
    histogram.Scale(histI.Integral()/histogram.Integral())
    histogram.Write("cond_"+histogram.GetName())
f.Close()









