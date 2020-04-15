#!/usr/bin/env python

import os
import ROOT
from ROOT import gStyle,gROOT,gPad
import math
import numpy as np
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-i","--input",dest="input",default='',help="input ROOT file")
parser.add_option("-o","--output",dest="output",default='biasPlot',help="output plot name")
parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=1000.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=4500.0)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=-4.5)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=4.5)
parser.add_option("-t","--titleX",dest="titleX",default='m_{X} (GeV)',help="title of x axis")
parser.add_option("-T","--titleY",dest="titleY",default='measured x-sec. / uncertainty',help="title of y axis")
parser.add_option("-l","--log",dest="log",type=int,help="use log scale",default=0)
(options,args) = parser.parse_args()


withObs = 0



def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  os.system("rm "+name+".eps")



setTDRStyle()
style=gROOT.GetStyle("tdrStyle").Clone()
style.SetPadLeftMargin(0.14)
style.SetPadRightMargin(0.04)
style.SetGridColor(14)
style.cd()

f = ROOT.TFile(options.input)
limit = f.Get("limit")
#f.Close()
data = {}

for event in limit:
    if float(event.mh)<options.minX or float(event.mh)>options.maxX:
        continue

    if not (event.mh in data.keys()):
        data[event.mh]={}

    if withObs and event.iToy==0:
        data[event.mh]['obs']=event.limit/event.limitErr


lineExp = ROOT.TGraph()
lineExp.SetName("limit_exp")
band68 = ROOT.TGraphAsymmErrors()
band68.SetName("band68")
band95 = ROOT.TGraphAsymmErrors()
band95.SetName("band95")
line_plus1 = ROOT.TGraph()
line_plus1.SetName("line_plus1")
line_plus2 = ROOT.TGraph()
line_plus2.SetName("line_plus2")
line_minus1 = ROOT.TGraph()
line_minus1.SetName("line_minus1")
line_minus2 = ROOT.TGraph()
line_minus2.SetName("line_minus2")
lineObs = ROOT.TGraph()
lineObs.SetName("limit_obs")
lineZero = ROOT.TGraph()
lineZero.SetName("zero")


N=0
h = ROOT.TH1D("tmpTH1","",300000,-100,100)
for mass,info in data.iteritems():

    h.Reset()

    limit.Draw("limit/limitErr>>tmpTH1","mh=="+str(mass)+"&&quantileExpected==-1&&limitErr!=0&&limitErr<100")

    prob=np.array([0.025,0.16,0.5,0.84,0.975])
    q=np.array([0.,0.,0.,0.,0.])
    nq=h.GetQuantiles(5,q,prob)

    M2sigma=q[0]
    M1sigma=q[1]
    median=q[2]
    P1sigma=q[3]
    P2sigma=q[4]

    print mass, q, info

    lineExp.SetPoint(N,mass,median)
    band68.SetPoint(N,mass,median)
    band95.SetPoint(N,mass,median)
    band68.SetPointError(N,0.0,0.0,median-M1sigma,P1sigma-median)
    band95.SetPointError(N,0.0,0.0,median-M2sigma,P2sigma-median)
    line_plus1.SetPoint(N,mass,P1sigma)
    line_plus2.SetPoint(N,mass,P2sigma)
    line_minus1.SetPoint(N,mass,M1sigma)
    line_minus2.SetPoint(N,mass,M2sigma)
    if withObs:
        lineObs.SetPoint(N,mass,info['obs'])
    lineZero.SetPoint(N,mass,0.)

    N=N+1

lineExp.Sort()
band68.Sort()
band95.Sort()
line_plus1.Sort()
line_plus2.Sort()
line_minus1.Sort()
line_minus2.Sort()
if withObs:
    lineObs.Sort()
lineZero.Sort()

color1=ROOT.kBlue-9 #ROOT.kGreen+1
color2=ROOT.kBlue-10 #ROOT.kOrange
band68.SetFillColor(color1)
band68.SetLineColor(0)
band95.SetFillColor(color2)
band95.SetLineColor(0)
line_plus1.SetLineWidth(1)
line_plus1.SetLineColor(color1)
line_plus2.SetLineWidth(1)
line_plus2.SetLineColor(color2)
line_minus1.SetLineWidth(1)
line_minus1.SetLineColor(color1)
line_minus2.SetLineWidth(1)
line_minus2.SetLineColor(color2)
lineExp.SetLineWidth(2)
lineExp.SetLineColor(ROOT.kBlue)
lineExp.SetLineStyle(7)
lineExp.SetMarkerStyle(0)
if withObs:
    lineObs.SetLineWidth(2)
    lineObs.SetLineColor(ROOT.kBlack)
    lineObs.SetMarkerSize(0.6)
    lineObs.SetMarkerStyle(20)
    lineObs.SetMarkerColor(ROOT.kBlack)
lineZero.SetLineWidth(2)
lineZero.SetLineColor(ROOT.kBlack)
lineZero.SetMarkerStyle(0)


c=ROOT.TCanvas("c","c",500,500)
c.cd()
c.UseCurrentStyle()

frame=c.DrawFrame(options.minX,options.minY,options.maxX,options.maxY)
frame.GetXaxis().SetTitle(options.titleX)
frame.GetYaxis().SetTitle(options.titleY)
frame.GetXaxis().SetTitleOffset(1.15)
frame.GetYaxis().SetTitleOffset(1.35)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetNdivisions(10)
frame.Draw()
c.Draw()
c.SetLogy(options.log)

band95.Draw("3same")
band68.Draw("3same")
#band68.Draw("XLsame")
#line_plus1.Draw("Lsame")
#line_plus2.Draw("Lsame")
#line_minus1.Draw("Lsame")
#line_minus2.Draw("Lsame")

c.Update()
c.RedrawAxis("g")

lineExp.Draw("Lsame")
if withObs:
    lineObs.Draw("PLsame")
lineZero.Draw("Lsame")

gPad.Update()

lgd = ROOT.TLegend(0.7,0.75,1.,0.9)
lgd.SetFillStyle(0)
lgd.SetBorderSize(0)
lgd.SetTextFont(42)
lgd.SetTextSize(0.04)
if withObs:
    lgd.AddEntry(lineObs,"Data","lp")
lgd.AddEntry(lineExp,"Median","l")
lgd.AddEntry(band68,"68%","f")
lgd.AddEntry(band95,"95%","f")
lgd.Draw()

c.Update()
c.RedrawAxis()

saveCanvas(c,options.output)
