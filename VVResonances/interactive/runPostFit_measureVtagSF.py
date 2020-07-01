import os, math
import ROOT
from ROOT import gStyle,gROOT,gPad
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from CMGTools.VVResonances.plotting.RooPlotter import *
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="Run2",help="2016 or 2017 or 2018 or Run2")
parser.add_option("-i","--input",dest="inputFile",default='',help="input root datacard")
parser.add_option("-f","--fit",dest="fit",type=int,default=1,help="perform the fit")
parser.add_option("-r","--fixR",dest="fixR",type=float,help="fix r in the fit")
parser.add_option("-v","--var",dest="variable",default='',help="restrict mjj or mvv")
parser.add_option("-p","--pur",dest="purity",default='',help="restrict to some purity")
parser.add_option("-C","--CMSlabel",dest="CMSlabel",type=int,default=0,help="0:None 1:CMS 2:CMS Preliminary 3:CMS Supplementary")
(options,args) = parser.parse_args()

minMJJ=20.0
maxMJJ=145.0


YmaxMJJ = -1 #paper: 650
YmaxMVV = -1 #paper: 2e+4

UNSTACKSIG = 0
OPTINRESW = 1 #to be activated when resW uses FastVerticalInterpHistPdf2D
VERBOSE = 0

def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")
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



s = "W"
YEAR=options.year
if options.inputFile=='':
  inputDir="Dc"+("_CR" if options.region=="CR" else "")+"_"+(s if s!="" else "XWW")+"/"
  inputDC=inputDir+"combined_"+YEAR+".root"
else:
  inputDC=options.inputFile
prefix = ('PreFit_','PostFit_')[options.fit]+"_"
directory='Plots_' + prefix + (s if s!="" else "Bonly") + '_' + YEAR
os.system("mkdir -p "+directory)

sigSF = -1.
sigStr = ""
sigLgd = ""
sigColor = 0
sigLabel = ""

sigLgd += "W"
sigColor = ROOT.kRed-3
plotter=RooPlotter(inputDC)    
if options.fixR is not None:
  plotter.fix("r",options.fixR)
if options.fit:
  plotter.prefit(verbose=VERBOSE)
    
if s!="":
  plotter.addContribution("W",True,sigLgd,2,1,sigColor,0,ROOT.kWhite)
  plotter.addContribution("bkg",False,"Background",1,1,ROOT.TColor.GetColor("#0041AA"),1001,ROOT.TColor.GetColor("#A5D2FF"))

l = 'allL'
pur = options.purity
c = 'allC'


purities = ['HP','LP','NP'] #['LP','HP']

for p in purities:

  varMJJ = "MJ"
  label=p+", "+YEAR

  if pur!='' and pur!=p: continue 
  plotter.drawBinned(varMJJ,"m_{jet} (GeV)",label,c+"_"+l+"_"+p+"_"+YEAR,[0,0],False,0,0,"",minMJJ,maxMJJ,YmaxMJJ,0,sigSF,sigLabel)
#  cmsLabel(plotter.canvas)
  
  saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJ_"+sigStr+"_"+c+"_"+l+"_"+p+"_"+YEAR)







