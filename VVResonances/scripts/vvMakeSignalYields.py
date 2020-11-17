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

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    


parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-m","--minMX",dest="minMX",type=float,help="minimum MX",default=0.)
parser.add_option("-M","--maxMX",dest="maxMX",type=float,help="maximum MX",default=0.)
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-d","--debugFile",dest="debugFile",help="Output debug plots",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-x","--minMVV",dest="min",type=float,help="min mVV",default=1)
parser.add_option("-X","--maxMVV",dest="max",type=float,help="max mVV",default=1)
parser.add_option("-f","--function",dest="function",help="interpolating function",default='')
parser.add_option("-b","--BR",dest="BR",help="branching ratio",default='1.0')

(options,args) = parser.parse_args()


yieldgraph=ROOT.TGraphErrors()


## Load the samples for all signal mass values
plotter = loadSignalNtuples(options.samples,args[0],options.minMX,options.maxMX)


## Sort the masses and get the yields
N=0
for mass in sorted(plotter.keys()):
    print 'integrating',str(mass)

    ## Get the histo from MC
    histo = plotter[mass].drawTH1(options.mvv,options.cut+"*("+options.BR+")","1",500,options.min,options.max)

    ## Get the yield and its uncertainty
    err=ROOT.Double(0)
    integral=histo.IntegralAndError(1,histo.GetNbinsX(),err) 
    print integral, err

    ## Add them to the graph
    yieldgraph.SetPoint(N,mass,integral)
    yieldgraph.SetPointError(N,0.0,err)

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

