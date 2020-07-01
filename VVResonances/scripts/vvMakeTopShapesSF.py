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
(options,args) = parser.parse_args()



def runFits(data,options):

    h = data.drawTH1(options.varx,options.cut,str(options.lumi),options.binsx,options.minx,options.maxx) 
    histo=copy.deepcopy(h)
    fitter=Fitter(['M'])
    fitter.w.var("M").setVal((options.maxx-options.minx)/2.0)
    fitter.w.var("M").setMax(options.maxx)
    fitter.w.var("M").setMin(options.minx)
    fitter.w.var("M").setBins(options.binsx)
    fitter.jetDoublePeakSF('model','M')
    fitter.importBinnedData(histo,['M'],'data')   
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(1)])
    fitter.projection("model","data","M",options.output+"_debug.png",'m_{SD}')
    scaleW = fitter.w.var('meanW').getVal()
    scaleTop = fitter.w.var('meanTop').getVal()
    sigmaW = fitter.w.var('sigmaW').getVal()
    sigmaTop = fitter.w.var('sigmaTop').getVal()
    slope  = fitter.w.var("slope").getVal()
    fT = fitter.w.var('fT').getVal()
    fE = fitter.w.var('fE').getVal()
    NW = fitter.w.var('NW').getVal()
    NBKG = fitter.w.var('NBKG').getVal()

    F=ROOT.TFile(options.output,"RECREATE")
    F.cd()

    #################################################################
    h = fitter.w.pdf("WPeak").createHistogram("M",options.binsx)
    h.Scale(NW/(options.lumi*h.Integral()))
    h.Write("W")

    fitter.w.var('meanW').setVal(scaleW*1.05)
    h = fitter.w.pdf("WPeak").createHistogram("M",options.binsx)
    h.Write("W_scaleUp")

    fitter.w.var('meanW').setVal(scaleW*0.95)
    h = fitter.w.pdf("WPeak").createHistogram("M",options.binsx)
    h.Write("W_scaleDown")

    fitter.w.var('meanW').setVal(scaleW)

    fitter.w.var('sigmaW').setVal(sigmaW*1.25)
    h = fitter.w.pdf("WPeak").createHistogram("M",options.binsx)
    h.Write("W_sigmaUp")

    fitter.w.var('sigmaW').setVal(sigmaW*0.75)
    h = fitter.w.pdf("WPeak").createHistogram("M",options.binsx)
    h.Write("W_sigmaDown")

    fitter.w.var('sigmaW').setVal(sigmaW)

    #################################################################


    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Scale(NBKG/(options.lumi*h.Integral()))
    h.Write("bkg")

    fitter.w.var('meanTop').setVal(scaleTop*1.15)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_scaleUp")

    fitter.w.var('meanTop').setVal(scaleTop*0.85)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_scaleDown")

    fitter.w.var('meanTop').setVal(scaleTop)

    fitter.w.var('sigmaTop').setVal(sigmaTop*1.25)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_sigmaUp")

    fitter.w.var('sigmaTop').setVal(sigmaTop*0.75)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_sigmaDown")

    fitter.w.var('sigmaTop').setVal(sigmaTop)


    fitter.w.var('slope').setVal(slope*1.5)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_slopeUp")

    fitter.w.var('slope').setVal(slope*0.5)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_slopeDown")
    
    fitter.w.var('slope').setVal(slope)

    fitter.w.var('fT').setVal(fT*1.3)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_fTUp")
    fitter.w.var('fT').setVal(fT*0.7)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_fTDown")
    
    fitter.w.var('fT').setVal(fT)

    fitter.w.var('fE').setVal(fE*1.3)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_fEUp")
    fitter.w.var('fE').setVal(fE*0.7)
    h = fitter.w.pdf("bkg").createHistogram("M",options.binsx)
    h.Write("bkg_fEDown")
    
    fitter.w.var('fE').setVal(fE)
    F.Close()



    
data=loadNtuples(options.samples,args[0])

runFits(data,options)
    
    
    



