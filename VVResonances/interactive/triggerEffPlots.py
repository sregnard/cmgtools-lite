import os
import ROOT
import math
import numpy as np
from array import array
from ROOT import gROOT, gStyle
from tdrstyle import *
from CMS_lumi import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="Run2",help="2016 or 2017 or 2018 or Run2")
parser.add_option("-C","--CMSlabel",dest="CMSlabel",type=int,default=0,help="0:None 1:CMS 2:CMS Preliminary 3:CMS Supplementary")
(options,args) = parser.parse_args()

YEAR=options.year
if YEAR not in ["2016","2017","2018"]:
    parser.error("year must be 2016, 2017, or 2018")


outputDir = 'TriggerEffPlots'#+YEAR+'/'
os.system("mkdir -p "+outputDir)

fIn = ROOT.TFile('trigger_eff_'+YEAR+'.root','READ')


setTDRStyle()
#'''
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.13)
ROOT.gStyle.SetPadLeftMargin(0.16)
ROOT.gStyle.SetPadRightMargin(0.02)
ROOT.gStyle.SetPalette(57)
#'''

def saveCanvas(dirName,canvas,tag=""):
    name = dirName + "/" + canvas.GetName()
    if tag!="":
        name += "_" + tag
    canvas.SaveAs(name+".root")
    #canvas.SaveAs(name+".C")
    canvas.SaveAs(name+".pdf")
    canvas.SaveAs(name+".png")
    #canvas.SaveAs(name+".eps")
    #os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png") ## not installed 
    #os.system("rm "+name+".eps")

def cmsLabel(canvas):
  if options.CMSlabel==0:
    cmslabel_not(canvas,YEAR,11)
  elif options.CMSlabel==1:
    cmslabel_final(canvas,YEAR,11)
  elif options.CMSlabel==2:
    cmslabel_prelim(canvas,YEAR,11)
  elif options.CMSlabel==3:
    cmslabel_suppl(canvas,YEAR,11)

def setColZGradient_PosNeg():
    NRGBs = 4
    NCont = 40 #255
    stops = [ 0.00, 0.20, 0.50, 1.00 ]
    red   = [ 243./256., 256./256., 1.00,   0./256. ]
    green = [ 113./256., 150./256., 1.00,   0./256. ]
    blue  = [   0./256.,   0./256., 1.00, 220./256. ]
    stopsArray = array('d', stops)
    redArray   = array('d', red)
    greenArray = array('d', green)
    blueArray  = array('d', blue)
    ROOT.TColor.CreateGradientColorTable(NRGBs, stopsArray, redArray, greenArray, blueArray, NCont)
    ROOT.gStyle.SetNumberContours(NCont)

def setColZGradient_PosNeg_deep():
    NRGBs = 5
    NCont = 40 #255
    stops = [ 0.00, 0.20, 0.40, 0.6666, 1.00 ]
    red   = [ 144./256., 243./256., 256./256., 1.00,   0./256. ]
    green = [  65./256., 113./256., 150./256., 1.00,   0./256. ]
    blue  = [   0./256.,   0./256.,   0./256., 1.00, 220./256. ]
    stopsArray = array('d', stops)
    redArray   = array('d', red)
    greenArray = array('d', green)
    blueArray  = array('d', blue)
    ROOT.TColor.CreateGradientColorTable(NRGBs, stopsArray, redArray, greenArray, blueArray, NCont)
    ROOT.gStyle.SetNumberContours(NCont)




h1n = [
    ("TriggerEff_MET_eleChannel_", "MET_ELE_MC", "MET_ELE_DATA", 0.7,  1.19  ),
    ("TriggerEff_MET_muChannel_",  "MET_MU_MC",  "MET_MU_DATA",  0.94, 1.019 ),
]

n1 = 2
h1m = np.zeros((n1), dtype=object)
h1d = np.zeros((n1), dtype=object)
h1r = np.zeros((n1), dtype=object)
c1 = np.zeros((n1), dtype=object)

for i in range(n1):

    canvasname = h1n[i][0]+YEAR
    c1[i] = ROOT.TCanvas(canvasname,canvasname,500,500)
    c1[i].cd()
    p1a = ROOT.TPad("p1a","",0.0,0.24,1.0,0.95,0)
    p1b = ROOT.TPad("p1b","",0.0,0.0,1.0,0.24,0)
    p1a.SetTopMargin(0.)
    p1a.SetBottomMargin(0.028)
    p1a.SetLeftMargin(0.14)
    p1a.SetRightMargin(0.04)
    p1b.SetTopMargin(0.)
    p1b.SetBottomMargin(0.5)
    p1b.SetLeftMargin(0.14)
    p1b.SetRightMargin(0.04)
    p1a.Draw()
    p1b.Draw()
    
    p1a.cd()
    h1m[i] = fIn.Get(h1n[i][1])
    h1d[i] = fIn.Get(h1n[i][2])
    h1m[i].GetYaxis().SetRangeUser(0.,1.1)
    h1m[i].GetXaxis().SetTitle('E_{T}^{miss}')
    h1m[i].GetYaxis().SetTitle('Efficiency')
    h1m[i].GetXaxis().SetLabelSize(0.04)
    h1m[i].GetYaxis().SetLabelSize(0.06)
    h1m[i].GetXaxis().SetTitleSize(0.05)
    h1m[i].GetYaxis().SetTitleSize(0.07)
    h1m[i].GetXaxis().SetTitleOffset(3)
    h1m[i].GetXaxis().SetLabelOffset(3)
    h1m[i].GetYaxis().SetTitleOffset(0.9)
    h1m[i].SetLineColor(ROOT.kRed)
    h1m[i].SetMarkerColor(ROOT.kRed)
    h1m[i].Draw()
    h1d[i].Draw("same")

    p1b.cd()
    h1r[i] = h1d[i].Clone()
    h1r[i].Divide(h1m[i])
    h1r[i].GetYaxis().SetRangeUser(h1n[i][3],h1n[i][4])
    h1r[i].GetXaxis().SetTitle('E_{T}^{miss}')
    h1r[i].GetYaxis().SetTitle('data/MC')
    h1r[i].GetXaxis().SetLabelSize(0.16)
    h1r[i].GetYaxis().SetLabelSize(0.125)
    h1r[i].GetXaxis().SetTitleSize(0.21)
    h1r[i].GetYaxis().SetTitleSize(0.17)
    h1r[i].GetXaxis().SetTitleOffset(0.95)
    h1r[i].GetYaxis().SetTitleOffset(0.35)
    line=ROOT.TLine(50.,1.,1000.,1.)
    line.SetLineWidth(1)
    line.SetLineColor(14)
    h1r[i].Draw()
    line.Draw()
    h1r[i].Draw("same")
    p1b.RedrawAxis()
    p1b.Update()
    
    saveCanvas(outputDir,c1[i])
    cmsLabel(c1[i])



    
ROOT.gStyle.SetPadRightMargin(0.16)

h2n = [
    ("ELE_MC", "ELE_DATA", "ELE", "electron" ),
    ("MU_MC",  "MU_DATA",  "MU",  "muon"     ),
    ]
n2=2

h2m = np.zeros((n2), dtype=object)
h2d = np.zeros((n2), dtype=object)
h2r = np.zeros((n2), dtype=object)
c2m = np.zeros((n2), dtype=object)
c2d = np.zeros((n2), dtype=object)
c2r = np.zeros((n2), dtype=object)

for i in range(n2):

    canvasname = 'TriggerEff_'+h2n[i][0]+'_'+YEAR
    c2m[i] = ROOT.TCanvas(canvasname,canvasname,500,500)
    c2m[i].SetLogx()
    h2m[i] = fIn.Get(h2n[i][0])
    h2m[i].GetXaxis().SetRangeUser(50.,1000.)
    h2m[i].GetZaxis().SetRangeUser(0.,1.)
    h2m[i].GetXaxis().SetTitle(h2n[i][3]+' p_{T}')
    h2m[i].GetYaxis().SetTitle(h2n[i][3]+' #eta')
    h2m[i].GetZaxis().SetTitle('Efficiency in data')
    h2m[i].Draw('colz')
    saveCanvas(outputDir,c2m[i])
    cmsLabel(c2m[i])

    canvasname = 'TriggerEff_'+h2n[i][1]+'_'+YEAR
    c2d[i] = ROOT.TCanvas(canvasname,canvasname,500,500)
    c2d[i].SetLogx()
    h2d[i] = fIn.Get(h2n[i][1])
    h2d[i].GetXaxis().SetRangeUser(50.,1000.)
    h2d[i].GetZaxis().SetRangeUser(0.,1.)
    h2d[i].GetXaxis().SetTitle(h2n[i][3]+' p_{T}')
    h2d[i].GetYaxis().SetTitle(h2n[i][3]+' #eta')
    h2d[i].GetZaxis().SetTitle('Efficiency in MC')
    h2d[i].Draw('colz')
    saveCanvas(outputDir,c2d[i])
    cmsLabel(c2d[i])

    
#setColZGradient_PosNeg()
setColZGradient_PosNeg_deep()

for i in range(n2):

    canvasname = 'TriggerSF_'+h2n[i][2]+'_'+YEAR
    c2r[i] = ROOT.TCanvas(canvasname,canvasname,500,500)
    c2r[i].SetLogx()
    h2r[i] = h2d[i].Clone()
    h2r[i].Divide(h2m[i])
    h2r[i].GetXaxis().SetRangeUser(50.,1000.)
    h2r[i].GetXaxis().SetTitle(h2n[i][3]+' p_{T}')
    h2r[i].GetYaxis().SetTitle(h2n[i][3]+' #eta')
    h2r[i].GetZaxis().SetTitle('data/MC scale factor')
    h2r[i].GetZaxis().SetRangeUser(0.63,1.2)
    ROOT.gStyle.SetPaintTextFormat(".3f")
    h2r[i].Draw('colz,text45,error')
    saveCanvas(outputDir,c2r[i])
    cmsLabel(c2r[i])
    
