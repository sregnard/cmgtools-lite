import os, math
import ROOT
from ROOT import gStyle,gROOT,gPad
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from CMGTools.VVResonances.plotting.RooPlotter import *
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import optparse
parser = optparse.OptionParser()
parser.add_option("-i","--input",dest="inputFile",default='',help="input root datacard")
parser.add_option("-f","--fit",dest="fit",type=int,default=1,help="perform the fit")
parser.add_option("-r","--fixR",dest="fixR",type=float,help="fix r in the fit")
parser.add_option("-s","--signalType",dest="signalType",default='XWW',help="XWW or XWZ or XWH")
parser.add_option("-m","--fixMX",dest="fixMX",type=float,help="fix signal mass")
(options,args) = parser.parse_args()

minMJJ=20.0
maxMJJ=210.0

minMVV=700.0
maxMVV=5000.0

YmaxMJJ = -1 ##2016 paper: 650
YmaxMVV = -1 ##2016 paper: 2e+4

labelMJJ = "m_{jet} (GeV)"
labelMVV = "m_{WV} (GeV)"

UNSTACKSIG = 1
OPTINRESW = 1 #to be activated when resW uses FastVerticalInterpHistPdf2D
VERBOSE = 0

def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  #canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  #os.system("rm "+name+".eps") ## don't uncomment this for jobs

def cmsLabel(canvas):
  if options.CMSlabel==0:
    cmslabel_not(canvas,YEAR,11)
  elif options.CMSlabel==1:
    cmslabel_final(canvas,YEAR,11)
  elif options.CMSlabel==2:
    cmslabel_prelim(canvas,YEAR,11)
  elif options.CMSlabel==3:
    cmslabel_suppl(canvas,YEAR,11)



s = options.signalType

if options.inputFile=='':
  inputDir="Dc"+("_CR" if options.region=="CR" else "")+"_"+(s if s!="" else "XWW")+"/"
  inputDC=inputDir+"combined_"+YEAR+".root"
else:
  inputDC=options.inputFile



sigSF = -1.
sigStr = ""
sigLgd = ""
sigColor = ROOT.kRed
sigLabel = ""


  
plotter=RooPlotter(inputDC)    
if options.fixMX is not None:
  plotter.fix("MH",options.fixMX)
if options.fixR is not None:
  plotter.fix("r",options.fixR)

if options.fit:
  data="data_obs"
  plotter.prefit(verbose=VERBOSE,data=data)

if s!="":
  plotter.addContribution(s,True,sigLgd,2,1,sigColor,0,ROOT.kWhite)
plotter.addContribution("res",False,"W+V/t",1,1,ROOT.TColor.GetColor("#0F5500"),1001,ROOT.TColor.GetColor("#60B037"),("","_opt")[OPTINRESW]) #4CB319"))
plotter.addContribution("nonRes",False,"W+jets",1,1,ROOT.TColor.GetColor("#0041AA"),1001,ROOT.TColor.GetColor("#A5D2FF"),"_opt")



def plot(var,cat,window,mini,maxi,log=0):
  plotter.drawBinned(var,var,cat,cat,[0,0],0,log,0,window,mini,maxi,-1)

#            subcat = '_'.join([l,p,c,d,YEAR])
