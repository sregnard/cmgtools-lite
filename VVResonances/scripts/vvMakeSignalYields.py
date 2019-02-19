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
parser.add_option("-m","--minMX",dest="minmx",type=float,help="minimum mx",default=0.)
parser.add_option("-M","--maxMX",dest="maxmx",type=float,help="maximum mx",default=0.)
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-d","--debugFile",dest="debugFile",help="Output debug plots",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-x","--minMVV",dest="min",type=float,help="min mVV",default=1)
parser.add_option("-X","--maxMVV",dest="max",type=float,help="max mVV",default=1)
parser.add_option("-f","--function",dest="function",help="interpolating function",default='')
parser.add_option("-b","--BR",dest="BR",type=float,help="branching ratio",default=1)

(options,args) = parser.parse_args()


yieldgraph=ROOT.TGraphErrors()


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
    if mass<options.minmx or mass>options.maxmx:
        continue
    samples[mass] = fname
    print 'found',filename,'mass',str(mass) 


## Sort the masses and get the yields
N=0
for mass in sorted(samples.keys()):
    print 'fitting',str(mass)

    ## Get the histo from MC
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
    plotter.setupFromFile(args[0]+'/'+samples[mass]+'.pck')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('xsec','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    histo = plotter.drawTH1(options.mvv,options.cut,"1",500,options.min,options.max)

    ## Get the yield and its uncertainty
    err=ROOT.Double(0)
    integral=histo.IntegralAndError(1,histo.GetNbinsX(),err) 
    print integral, err

    ## Add them to the graph
    yieldgraph.SetPoint(N,mass,integral*options.BR)
    yieldgraph.SetPointError(N,0.0,err*options.BR)

    N=N+1



## Run the fit and store the parameterization
func = ROOT.TF1("func",options.function,0,13000)
yieldgraph.Fit(func)

parameterization={'yield':returnString(func)}
f=open(options.output+".json","w")
json.dump(parameterization,f)
f.close()


## For control plots
f=ROOT.TFile(options.output+".root","RECREATE")
f.cd()
yieldgraph.Write("yield")
func.Write("yield_func")
f.Close()

c=ROOT.TCanvas("c")
c.cd()
yieldgraph.Draw("AP")
c.SaveAs(options.debugFile+".png")

#F=ROOT.TFile(options.output+".root",'RECREATE')
#F.cd()
#yieldgraph.Write("yield")
#F.Close()

