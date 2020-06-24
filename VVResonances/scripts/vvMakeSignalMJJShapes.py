#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
from loadNtuples import *

parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-m","--minMX",dest="minMX",type=float,help="minimum MX",default=900)
parser.add_option("-M","--maxMX",dest="maxMX",type=float,help="maximum MX",default=4600)
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output file",default='')
parser.add_option("-d","--debugFile",dest="debugFile",help="Output debug plots",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-x","--min",dest="mini",type=float,help="min MJJ",default=30)
parser.add_option("-X","--max",dest="maxi",type=float,help="max MJJ",default=210)
parser.add_option("-e","--exp",dest="doExp",type=int,help="useExponential",default=1)
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="")

(options,args) = parser.parse_args()


## color of control plots
color = 0
if 'XWW' in options.output: color = ROOT.kOrange+2
elif 'XWZ' in options.output: color = ROOT.kViolet-8
elif 'XWH' in options.output: color = ROOT.kTeal-6

## Define output dictionary
graphs={
    'mean':ROOT.TGraphErrors(),
    'sigma':ROOT.TGraphErrors(),
    'alpha':ROOT.TGraphErrors(),
    'n':ROOT.TGraphErrors(),
    'f':ROOT.TGraphErrors(),
    'slope':ROOT.TGraphErrors(),
    'alpha2':ROOT.TGraphErrors(),
    'n2':ROOT.TGraphErrors()
    }


## Load the samples for all signal mass values
plotter = loadSignalNtuples(options.samples,args[0],options.minMX,options.maxMX)


## Sort the masses and run the fits
N=0
for mass in sorted(plotter.keys()):
    print 'fitting',str(mass)

    ## Get the histo from MC
    histo = plotter[mass].drawTH1(options.mvv,options.cut,"1",int((options.maxi-options.mini)/4),options.mini,options.maxi)

    ## Set up the fitter 
    fitter=Fitter(['x'])
    if options.doExp==1:
        fitter.jetResonance('model','x')
    else:
        fitter.jetResonanceNOEXP('model','x')
    if options.fixPars!="":
        fixedPars =options.fixPars.split(',')
        for par in fixedPars:
            parVal = par.split(':')
            fitter.w.var(parVal[0]).setVal(float(parVal[1]))
            fitter.w.var(parVal[0]).setConstant(1)
    #fitter.w.var("MH").setVal(mass)
    fitter.importBinnedData(histo,['x'],'data')

    ## fit
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])

    ## control plot
    fitter.projection("model","data","x",options.debugFile+"_"+str(int(mass)).zfill(4)+".png",options.mvv,[],[ROOT.RooFit.LineColor(color)])
    fitter.projection("model","data","x",options.debugFile+"_"+str(int(mass)).zfill(4)+".root",options.mvv,[],[ROOT.RooFit.LineColor(color)])

    ## Save parameters vs MX  
    for var,graph in graphs.iteritems():
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1


## Store all graphs       
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()
            
