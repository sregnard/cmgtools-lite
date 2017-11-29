import os
import ROOT
from ROOT import gStyle,gROOT,gPad
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from CMGTools.VVResonances.plotting.RooPlotter import *
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import optparse
parser = optparse.OptionParser()
parser.add_option("-i","--input",dest="inputFile",default='combined.root',help="input root datacard")
parser.add_option("-r","--fixR",dest="fixR",type=float,help="fix r in the fit")
parser.add_option("-s","--signalType",dest="signalType",default='',help="XWW or XWZ")
parser.add_option("-R","--rForWeight",dest="rForWeight",type=float,help="fix r for the S/(S+B) reweighting")
parser.add_option("-u","--doUncBand",dest="doUncBand",type=int,default=0,help="do uncertainty band")
(options,args) = parser.parse_args()



def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  os.system("rm "+name+".eps")

def cmsLabel(canvas):
  #cmslabel_not(canvas,'2016',11)
  #cmslabel_prelim(canvas,'2016',11)
  cmslabel_final(canvas,'2016',11)



directory='PlotsPostFit_'+options.signalType
os.system("mkdir -p "+directory)

plotter=RooPlotter(options.inputFile)

s = options.signalType
if s=='XWW':
    plotter.fix("MH",2000)
elif s=='XWZ':
    plotter.fix("MH",2000)
if options.fixR is not None:
    plotter.fix("r",options.fixR)

plotter.prefit()

if options.rForWeight is not None:
    plotter.fix("r",options.rForWeight)


if s=='XWW':
    plotter.addContribution("XWW",True,"X #rightarrow WW",3,1,ROOT.kOrange+10,0,ROOT.kWhite)
elif s=='XWZ':
    plotter.addContribution("XWZ",True,"X #rightarrow WZ",3,1,ROOT.kMagenta,0,ROOT.kWhite)
plotter.addContribution("resW",False,"W+V/t",1,1,ROOT.TColor.GetColor("#0F5500"),1001,ROOT.TColor.GetColor("#60B037"))
plotter.addContribution("nonRes",False,"W+jets",1,1,ROOT.TColor.GetColor("#0041AA"),1001,ROOT.TColor.GetColor("#A5D2FF"),"_opt")





categories1 = [
  "nob_mu_HP_13TeV",
  "nob_mu_LP_13TeV",
  "nob_e_HP_13TeV",
  "nob_e_LP_13TeV",
]

SOB=False

plotter.moneyPlotSimple("MLNuJ","MJ","m_{WV} (GeV)",categories1,SOB,False,4)

cmsLabel(plotter.canvas)

outname = directory+"/SOSPB_"+s
if SOB:
    outname = directory+"/SOB_"+s

saveCanvas(plotter.canvas,outname)



