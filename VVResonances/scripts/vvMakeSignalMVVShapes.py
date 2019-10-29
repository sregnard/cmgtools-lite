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
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
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
plotters={}
sampleTypes=options.samples.split(',')

filelist = []
if args[0]=='ntuples':
    filelist = [g for flist in [[(path+'/'+f) for f in os.listdir(args[0]+'/'+path)] for path in os.listdir(args[0])] for g in flist]
else:
    filelist = os.listdir(args[0])

for filename in filelist:
    for sampleType in sampleTypes:
        if not (filename.find(sampleType)!=-1):
            continue
        fnameParts=filename.split('.')
        fname=fnameParts[0]
        ext=fnameParts[1]
        if ext.find("root") ==-1:
            continue
        mass = float(fname.split('_')[-1])
        if mass<options.minMX or mass>options.maxMX:
            continue
        if not mass in plotters.keys():
            plotters[mass] = []
        plotters[mass].append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
        plotters[mass][-1].setupFromFile(args[0]+'/'+fname+'.pck')
        plotters[mass][-1].addCorrectionFactor('xsec','tree')
        plotters[mass][-1].addCorrectionFactor('genWeight','tree')
        plotters[mass][-1].addCorrectionFactor('puWeight','tree')
        plotters[mass][-1].filename=fname
        if options.scaleFactors!='':
            for s in scaleFactors:
                plotter[mass][-1].addCorrectionFactor(s,'tree')
        print 'found',filename,'mass',str(mass) 


## Sort the masses and run the fits
N=0
for mass in sorted(plotters.keys()):
    print 'fitting',str(mass)

    if len(plotters[mass]) != (1,3)[args[0]=='ntuples']:
        continue

    ## Get the histo from MC
    plotter=MergedPlotter(plotters[mass])
    histo = plotter.drawTH1(options.varx,options.cut,"1",options.binsxfit,options.minx,options.maxx)

    ## Set up the fitter
    fitter=Fitter(['MVV'])
    fitter.signalResonance('model','MVV')
    #fitter.w.var("MH").setVal(mass)
    fitter.importBinnedData(histo,['MVV'],'data')

    ## fit 
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    #fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1)])
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
            
