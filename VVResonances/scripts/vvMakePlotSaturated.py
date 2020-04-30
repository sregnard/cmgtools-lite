#!/usr/bin/env python

import os
import ROOT
from ROOT import gStyle,gROOT,gPad
import math
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *


import optparse
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",default='saturated',help="name of output file")
parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=10500)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=18500)
(options,args) = parser.parse_args()


def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  #canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  os.system("rm "+name+".eps")




setTDRStyle()
style=gROOT.GetStyle("tdrStyle").Clone()
style.SetPadLeftMargin(0.14)
style.SetPadRightMargin(0.04)
#style.SetGridColor(16)
style.cd()


f0 = ROOT.TFile(args[0])
exp = f0.Get("limit")
h0 = ROOT.TH1F("h0","",30,options.minX,options.maxX)
exp.Draw("limit>>h0")

f1 = ROOT.TFile(args[1])
obs = f1.Get("limit")
h1 = ROOT.TH1F("h1","",30,options.minX,options.maxX)
obs.Draw("limit>>h1")
ob = f1.limit.limit



c=ROOT.TCanvas("c","c",500,500)
c.cd()
c.UseCurrentStyle()

h0.SetNdivisions(205)

h0.SetLineColor(ROOT.kAzure-9)
h0.SetFillColor(ROOT.kAzure-9)
#h1.SetFillColor(ROOT.kRed)


h0.Draw("HIST")
#h1.Draw("HIST,SAME")


arr = ROOT.TArrow(ob,30.,ob,0.)
arr.SetLineWidth(5)
arr.SetLineColor(ROOT.kRed+1)
arr.Draw()




saveCanvas(c,options.output)

