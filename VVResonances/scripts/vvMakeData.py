#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from math import log
import os, sys, re, optparse,pickle,shutil,json
from loadNtuples import *


parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT",default='')
parser.add_option("-v","--vars",dest="vars",help="variables seprataed by comma",default='')
parser.add_option("-b","--bins",dest="bins",help="bins per dimension separated by comma",default='')
parser.add_option("-m","--min",dest="mins",help="minimum separated by comma",default='')
parser.add_option("-M","--max",dest="maxes",help="maximum separated by comma",default='')
parser.add_option("-d","--isData",dest="data",type=int,help="isData",default=1)
parser.add_option("-f","--factor",dest="factor",type=float,help="factor",default=1.0)
parser.add_option("-n","--name",dest="name",help="name",default="histo")
#parser.add_option("-z","--zeroNegative",dest="zeroNegative",type=int,help="zero bvins with negative weights",default=0)



(options,args) = parser.parse_args()
#define output dictionary


data=loadNtuples(options.samples,args[0],options.data)


pvars=options.vars.split(',')
pmins=options.mins.split(',')
pmaxes=options.maxes.split(',')
pbins=options.bins.split(',')

if len(pvars)==1:
    histo=data.drawTH1(pvars[0],options.cut,"1",int(pbins[0]),float(pmins[0]),float(pmaxes[0]))
#    if options.zeroNegative:
#        for i in range(0,int(pbins[0])+2):
#            if histo.GetBinContent(i)<0:
#                histo.SetBinContent(i,0.0)


if len(pvars)==2:
    histo=data.drawTH2(pvars[1]+":"+pvars[0],options.cut,"1",int(pbins[0]),float(pmins[0]),float(pmaxes[0]),int(pbins[1]),float(pmins[1]),float(pmaxes[1]))
#    if options.zeroNegative:
#        for i in range(0,int(pbins[0])+2):
#            for j in range(0,int(pbins[1])+2):
#                bin=histo.GetBin(i,j)
#                if histo.GetBinContent(bin)<0:
#                    histo.SetBinContent(bin,0.0)


if len(pvars)==3:
    histo=data.drawTH3(pvars[2]+":"+pvars[1]+":"+pvars[0],options.cut,"1",int(pbins[0]),float(pmins[0]),float(pmaxes[0]),int(pbins[1]),float(pmins[1]),float(pmaxes[1]),int(pbins[2]),float(pmins[2]),float(pmaxes[2]))
#    if options.zeroNegative:
#        for i in range(0,int(pbins[0])+2):
#            for j in range(0,int(pbins[1])+2):
#                for k in range(0,int(pbins[2])+1):
#                    bin=histo.GetBin(i,j,k)
#                    if histo.GetBinContent(bin)<0:
#                        histo.SetBinContent(bin,0.0)


#PROTECTION



histo.Scale(options.factor)
F=ROOT.TFile(options.output,"UPDATE")
F.cd()
histo.Write(options.name)
F.Close()



