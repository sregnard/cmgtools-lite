#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-d","--debugFile",dest="debugFile",help="Output debug plots",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("-e","--exp",dest="doExp",type=int,help="useExponential",default=1)
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="")

(options,args) = parser.parse_args()
#define output dictionary

samples={}
graphs={'mean':ROOT.TGraphErrors(),'sigma':ROOT.TGraphErrors(),'alpha':ROOT.TGraphErrors(),'n':ROOT.TGraphErrors(),'f':ROOT.TGraphErrors(),'slope':ROOT.TGraphErrors(),'alpha2':ROOT.TGraphErrors(),'n2':ROOT.TGraphErrors()}

for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        

    mass = float(fname.split('_')[-1])

        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 


#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):

    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
#    plotter.setupFromFile(args[0]+'/'+samples[mass]+'.pck')
    plotter.addCorrectionFactor('genWeight','tree')
#    plotter.addCorrectionFactor('xsec','tree')
    plotter.addCorrectionFactor('puWeight','tree')
       
        
    fitter=Fitter(['x'])
    if options.doExp==1:
        fitter.jetResonance('model','x')
#        fitter.w.var("alpha").setVal(1.41)
#        fitter.w.var("alpha").setConstant(1)
    else:
        fitter.jetResonanceNOEXP('model','x')
#        fitter.w.var("alpha").setVal(0.50)
#        fitter.w.var("alpha").setConstant(1)


    if options.fixPars!="":
        fixedPars =options.fixPars.split(',')
        for par in fixedPars:
            parVal = par.split(':')
            fitter.w.var(parVal[0]).setVal(float(parVal[1]))
            fitter.w.var(parVal[0]).setConstant(1)


#    fitter.w.var("MH").setVal(mass)
    histo = plotter.drawTH1(options.mvv,options.cut,"1",int((options.maxi-options.mini)/4),options.mini,options.maxi)

    fitter.importBinnedData(histo,['x'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])

    optModel = []
    if 'XWW' in options.output: optModel = [ROOT.RooFit.LineColor(ROOT.kOrange+2)]
    if 'XWZ' in options.output: optModel = [ROOT.RooFit.LineColor(ROOT.kViolet-8)]
    if 'XWH' in options.output: optModel = [ROOT.RooFit.LineColor(ROOT.kTeal-6)]
    fitter.projection("model","data","x",options.debugFile+"_"+str(int(mass)).zfill(4)+".png",options.mvv,[],optModel)
    fitter.projection("model","data","x",options.debugFile+"_"+str(int(mass)).zfill(4)+".root",options.mvv,[],optModel)

    for var,graph in graphs.iteritems():
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1
        
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()
            
