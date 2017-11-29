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
parser.add_option("-u","--doUncBand",dest="doUncBand",type=int,default=0,help="do uncertainty band")
parser.add_option("-v","--var",dest="variable",default='',help="mjj or mvv")
parser.add_option("-p","--pur",dest="purity",default='',help="HP or LP")
parser.add_option("-l","--lep",dest="lepton",default='',help="e or mu")
(options,args) = parser.parse_args()



def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  #os.system("rm "+name+".eps") ## don't uncomment this for jobs

def cmsLabel(canvas):
  #cmslabel_not(canvas,'2016',11)
  #cmslabel_prelim(canvas,'2016',11)
  cmslabel_final(canvas,'2016',11)




directory='PlotsPostFit_'+options.signalType
os.system("mkdir -p "+directory)

s = options.signalType

doMjj = options.variable=='' or options.variable=='mjj'
doMvv = options.variable=='' or options.variable=='mvv'


if doMjj:
  
    plotter=RooPlotter(options.inputFile)    
  
    if s=='XWW':
        plotter.fix("MH",1350)
    elif s=='XWZ':
        plotter.fix("MH",1410)
    if options.fixR is not None:
        plotter.fix("r",options.fixR)

    plotter.prefit()

    if s=='XWW':
        plotter.addContribution("XWW",True,"X #rightarrow WW",3,1,ROOT.kOrange+10,0,ROOT.kWhite)
    elif s=='XWZ':
        plotter.addContribution("XWZ",True,"X #rightarrow WZ",3,1,ROOT.kMagenta,0,ROOT.kWhite)
    plotter.addContribution("resW",False,"W+V/t",1,1,ROOT.TColor.GetColor("#0F5500"),1001,ROOT.TColor.GetColor("#60B037")) #4CB319"))
    plotter.addContribution("nonRes",False,"W+jets",1,1,ROOT.TColor.GetColor("#0041AA"),1001,ROOT.TColor.GetColor("#A5D2FF"),"_opt")


if doMvv:

    plotter2=RooPlotter(options.inputFile)    

    if s=='XWW':
        plotter2.fix("MH",1350)
    elif s=='XWZ':
        plotter2.fix("MH",1410)
    if options.fixR is not None:
        plotter2.fix("r",options.fixR)

    plotter2.prefit()

    if s=='XWW':
        plotter2.addContribution("XWW",True,"X #rightarrow WW",3,1,ROOT.kOrange+10,0,ROOT.kWhite)
    elif s=='XWZ':
        plotter2.addContribution("XWZ",True,"X #rightarrow WZ",3,1,ROOT.kMagenta,0,ROOT.kWhite)
    plotter2.addContribution("nonRes",False,"W+jets",1,1,ROOT.TColor.GetColor("#0041AA"),1001,ROOT.TColor.GetColor("#A5D2FF"),"_opt")
    plotter2.addContribution("resW",False,"W+V/t",1,1,ROOT.TColor.GetColor("#0F5500"),1001,ROOT.TColor.GetColor("#60B037")) #4CB319"))




prt = options.purity
lep = options.lepton


for c in ['nob']:
#for c in ['Wplus','Wminus']:
    if c=='vbf':
        pur=['NP']
    else:
        pur=['HP','LP']
    for p in pur:
        for l in ['e','mu']:
            #continue

            label="W #rightarrow "+(("e","#mu")[l=='mu'])+"#nu, "+p
            
            if prt!='' and prt!=p: continue 
            if lep!='' and lep!=l: continue

            if doMvv:
                pass

                #''' ## for paper
                plotter2.drawBinned("MLNuJ","m_{WV} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,1,"")
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/postFitMVV_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''

                '''
                plotter2.drawBinned("MLNuJ","m_{WV} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,10000],options.doUncBand,c!='vbf',"")
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/postFitMVVBlind_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''

                '''
                plotter2.drawBinned("MLNuJ","m_{WV} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,0,"MJ:sig:66:86")
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/postFitMVVW_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                
                plotter2.frame.GetXaxis().SetRangeUser(1000.,2000.)
                plotter2.frame.GetYaxis().SetRangeUser(0.,1.1*(plotter2.frame.getHist("datapoints").GetY()[9]+plotter2.frame.getHist("datapoints").GetEYhigh()[9]))
                plotter2.frame2.GetXaxis().SetRangeUser(1000.,2000.)
                plotter2.line.SetX1(1000.)
                plotter2.line.SetX2(2000.)
                saveCanvas(plotter2.canvas,directory+"/postFitMVVWZoom_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''

                '''
                plotter2.drawBinned("MLNuJ","m_{WV} (GeV)",label+", 2D fit",c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,1,"MJ:sig:64:106")
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/postFitMVV_MJ64to106_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''

                '''
                plotter2.drawBinned("MLNuJ","m_{WV} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,1,"MJ:low:30:64")
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/postFitMVVLo_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''

                '''
                plotter2.drawBinned("MLNuJ","m_{WV} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,1,"MJ:high:106:210")
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/postFitMVVHi_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''

                ''' ## Plots in MLNuJ intervals (AN Fig. 65)
                plotter.drawBinned("MJ","m_{jet} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,0,"MLNuJ:bin1:800:1000",420.)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/postFitMJJ_MVVa0800to1000_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                
                plotter.drawBinned("MJ","m_{jet} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,0,"MLNuJ:bin1:1000:1200",162.)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/postFitMJJ_MVVb1000to1200_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                
                plotter.drawBinned("MJ","m_{jet} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,0,"MLNuJ:bin1:1200:1800",110.)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/postFitMJJ_MVVc1200to1800_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                
                plotter.drawBinned("MJ","m_{jet} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,0,"MLNuJ:bin1:1800:5000",31.)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/postFitMJJ_MVVd1800to5000_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''  

            if doMjj:
                pass

                #''' ## for paper
                plotter.drawBinned("MJ","m_{jet} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[0,0],options.doUncBand,0,"")
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/postFitMJJ_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''

                '''
                plotter.drawBinned("MJ","m_{jet} (GeV)",label,c+"_"+l+"_"+p+"_13TeV",[64,106],options.doUncBand,0,"")
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/postFitMJJBlind_"+s+"_"+c+"_"+l+"_"+p+"_13TeV")
                #'''





#for l in ['mu','e']:
#    for p in ['both']:
#        for c in ['vbf']:
#            plotter.drawProjection("MJ","m_{jet} [GeV]",c+"_"+l+"_"+p+"_13TeV",1,0)
#            saveCanvas(plotter.canvas,directory+"/postfitMJJ"+c+"_"+l+"_"+p)
#            plotter.drawProjection("MLNuJ","m_{WV} [GeV]",c+"_"+l+"_"+p+"_13TeV",1,0)
#            saveCanvas(plotter.canvas,directory+"/postfitMVV"+c+"_"+l+"_"+p)



#plotter=RooPlotter("LNuJJ_topPreFit_HP.root")    
#plotter.prefit()
#plotter.addContribution("topRes",True,"t#bar{t}",1,1,ROOT.kRed,0,ROOT.kWhite)
#plotter.addContribution("topNonRes",False,"non-resonant t#bar{t}",1,1,ROOT.kBlack,1001,ROOT.kGreen-5)
#plotter.drawStack("MJ","m_{jet} [GeV]","top_mu_HP_13TeV","top_mu_HP_13TeV")







