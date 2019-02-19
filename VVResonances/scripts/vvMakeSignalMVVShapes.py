#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json

parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-m","--minMX",dest="minMX",type=float,help="minimum MX",default=900)
parser.add_option("-M","--maxMX",dest="maxMX",type=float,help="maximum MX",default=4600)
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output file",default='')
parser.add_option("-d","--debugFile",dest="debugFile",help="Output debug plots",default='')
parser.add_option("-v","--varx",dest="varx",help="variablex",default='lnujj_LV_mass')
parser.add_option("-x","--minx",dest="minx",type=float,help="minimum x",default=800.)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="maximum x",default=5000.)
parser.add_option("-b","--binsxfit",dest="binsxfit",type=int,help="bins in x (for the fit)",default=168)
parser.add_option("-f","--scaleFactors",dest="scaleFactors",help="Additional scale factors separated by comma",default='')

(options,args) = parser.parse_args()


## color of control plots
color = 0
if 'XWW' in options.output: color = ROOT.kOrange+2
elif 'XWZ' in options.output: color = ROOT.kViolet-8
elif 'XWH' in options.output: color = ROOT.kTeal-6

## Define output dictionary
graphs={
    'MEAN':ROOT.TGraphErrors(),
    'SIGMA':ROOT.TGraphErrors(),
    'ALPHA1':ROOT.TGraphErrors(),
    'N1':ROOT.TGraphErrors(),
    'ALPHA2':ROOT.TGraphErrors(),
    'N2':ROOT.TGraphErrors()
    }

scaleFactors=options.scaleFactors.split(',')


## Find the samples for all signal mass values
samples={}
for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
    mass = float(fname.split('_')[-1])
    if mass<options.minMX or mass>options.maxMX:
        continue
    samples[mass] = fname
    print 'found',filename,'mass',str(mass) 


## Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):
    print 'fitting',str(mass)

    ## Get the histo from MC
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    if options.scaleFactors!='':
        for s in scaleFactors:
            plotter.addCorrectionFactor(s,'tree')
    histo = plotter.drawTH1(options.varx,options.cut,"1",options.binsxfit,options.minx,options.maxx)

    ## Set up the fitter
    fitter=Fitter(['MVV'])
    fitter.signalResonance('model','MVV')
    #fitter.w.var("MH").setVal(mass)
    fitter.importBinnedData(histo,['MVV'],'data')

    ## fit 
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])

    ## control plot
    fitter.projection("model","data","MVV",options.debugFile+"_"+str(int(mass)).zfill(4)+".root",options.varx,[],[ROOT.RooFit.LineColor(color)])
    fitter.projection("model","data","MVV",options.debugFile+"_"+str(int(mass)).zfill(4)+".png",options.varx,[],[ROOT.RooFit.LineColor(color)])

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
            
