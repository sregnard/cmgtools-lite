#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
import copy
from loadNtuples import *


parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT",default='')
parser.add_option("-v","--varx",dest="varx",help="variablex",default='lnujj_LV_mass')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins in x",default=1000)
parser.add_option("-x","--minx",dest="minx",type=float,help="minimum x",default=600)
parser.add_option("-X","--maxx",dest="maxx",type=float, help="maximum x",default=5000)
parser.add_option("-l","--lumi",dest="lumi",type=float, help="lumi",default="35000")
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="")
parser.add_option("-e","--doExp",dest="doExp",type=int,help="DoExp",default=0)
(options,args) = parser.parse_args()



def runFits(data,options):

    h = data.drawTH1(options.varx,options.cut,str(options.lumi),options.binsx,options.minx,options.maxx) 
    histo=copy.deepcopy(h)
    fitter=Fitter(['M'])
    fitter.w.var("M").setVal((options.maxx-options.minx)/2.0)
    fitter.w.var("M").setMax(options.maxx)
    fitter.w.var("M").setMin(options.minx)
    fitter.w.var("M").setBins(options.binsx)
    fitter.jetDoublePeakExp('model','M')
    if options.doExp==0:
        fitter.w.var("f2").setVal(1.0)
        fitter.w.var("f2").setConstant(1)
        fitter.w.var("slope").setVal(0.0)
        fitter.w.var("slope").setConstant(1)
        
    if options.fixPars!="":
            fixedPars =options.fixPars.split(',')
            for par in fixedPars:
                parVal = par.split(':')
                fitter.w.var(parVal[0]).setVal(float(parVal[1]))
                fitter.w.var(parVal[0]).setConstant(1)

    fitter.importBinnedData(histo,['M'],'data')   
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(1)])
    chi=fitter.projection("model","data","M",options.output+"_debug.png","m_{j} (GeV)")

    
    scaleW = fitter.w.var('meanW').getVal()
    scaleTop = fitter.w.var('meanTop').getVal()
    sigmaW = fitter.w.var('sigmaW').getVal()
    sigmaTop = fitter.w.var('sigmaTop').getVal()
    fraction = fitter.w.var('f').getVal()


    F=ROOT.TFile(options.output,"RECREATE")
    F.cd()

    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo")

    '''
    fitter.w.var('meanW').setVal(scaleW*1.05)
    fitter.w.var('meanTop').setVal(scaleTop*1.05)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_scaleUp")

    fitter.w.var('meanW').setVal(scaleW*0.95)
    fitter.w.var('meanTop').setVal(scaleTop*0.95)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_scaleDown")
    #'''

    fitter.w.var('meanW').setVal(scaleW*1.05)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_scaleWUp")

    fitter.w.var('meanW').setVal(scaleW*0.95)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_scaleWDown")

    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop*1.05)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_scaleTopUp")

    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop*0.95)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_scaleTopDown")

    '''
    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW*1.25)
    fitter.w.var('sigmaTop').setVal(sigmaTop*1.25)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_resUp")
    
    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW*0.75)
    fitter.w.var('sigmaTop').setVal(sigmaTop*0.75)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_resDown")
    #'''

    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW*1.25)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_resWUp")
    
    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW*0.75)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_resWDown")

    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop*1.25)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_resTopUp")
    
    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop*0.75)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_resTopDown")

    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    fitter.w.var('f').setVal(fraction*1.40)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_fUp")

    fitter.w.var('meanW').setVal(scaleW)
    fitter.w.var('meanTop').setVal(scaleTop)
    fitter.w.var('sigmaW').setVal(sigmaW)
    fitter.w.var('sigmaTop').setVal(sigmaTop)
    fitter.w.var('f').setVal(fraction*0.60)
    h = fitter.w.pdf("model").createHistogram("M",options.binsx)
    h.Write("histo_fDown")


    F.Close()



    
data=loadNtuples(options.samples,args[0])

runFits(data,options)
    
    
    



