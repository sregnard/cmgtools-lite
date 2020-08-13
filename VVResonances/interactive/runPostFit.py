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
parser.add_option("-s","--signalType",dest="signalType",default='',help="XWW or XWZ or XWH")
parser.add_option("-m","--fixMX",dest="fixMX",type=float,help="fix signal mass")
parser.add_option("-R","--dispR",dest="dispR",type=float,help="displayed signal cross section times BR")
parser.add_option("-u","--doUncBand",dest="doUncBand",type=int,default=0,help="do uncertainty band")
parser.add_option("-v","--var",dest="variable",default='',help="restrict mjj or mvv")
parser.add_option("-l","--lep",dest="lepton",default='',help="restrict to some lepton")
parser.add_option("-p","--pur",dest="purity",default='',help="restrict to some purity")
parser.add_option("-c","--cat",dest="category",default='',help="restrict to some category")
parser.add_option("-e","--eta",dest="deltaeta",default='',help="restrict to some deltaeta")
parser.add_option("-C","--CMSlabel",dest="CMSlabel",type=int,default=0,help="0:None 1:CMS 2:CMS Preliminary 3:CMS Supplementary")
parser.add_option("-b","--differentBinning",dest="differentBinning",type=int,default=1,help="use other binning for bb category")
parser.add_option("-S","--splitWTopPeaks",dest="splitWTopPeaks",type=int,default=0,help="separate W and top peak bkgd")
parser.add_option("-Z","--region",dest="region",default='SR',help="signal region (SR) or control region (CR)")
parser.add_option("-T","--toysFile",dest="toysFile",default='none',help="Toy MC file to import toys")
parser.add_option("-N","--nToys",dest="nToys",type=int, default=0,help="Number of Toys to import")
parser.add_option("-t","--fitToy",dest="fitToy",type=int, default=-1,help="Toy to use , -1 is real data ")
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
YEAR=options.year
if options.inputFile=='':
  inputDir="Dc"+("_CR" if options.region=="CR" else "")+"_"+(s if s!="" else "XWW")+"/"
  inputDC=inputDir+"combined_"+YEAR+".root"
else:
  inputDC=options.inputFile

prefix = ('PreFit_','PostFit_')[options.fit] + options.region + "_"
directory='Plots_' + prefix + (s if s!="" else "Bonly") + '_' + YEAR
os.system("mkdir -p "+directory)

sigSF = -1.
sigStr = ""
sigLgd = ""
sigColor = 0
sigLabel = ""
if s!="":
    sigSF = -1. if options.dispR is None else options.dispR/options.fixR
    sigStr = s + ("" if options.fixMX is None else str(int((options.fixMX))))
    mx = "" if options.fixMX is None else '{:,g}'.format(options.fixMX/1000)
    sx = "" if options.dispR is None else '{:,g}'.format(options.dispR)
    if s=="XWW":
        sigLgd += "G_{Bulk}" + ("" if options.fixMX is None else "#scale[0.9]{("+mx+" TeV)}") + "#rightarrowWW" 
        sigColor = ROOT.kRed-3
    elif s=="XWZ":
        sigLgd += "W'" + ("" if options.fixMX is None else "#scale[0.9]{("+mx+" TeV)}") + "#rightarrowWZ"
        sigColor = ROOT.kViolet-5
    elif s=="XWH":
        sigLgd += "W'" + ("" if options.fixMX is None else "#scale[0.9]{("+mx+" TeV)}") + "#rightarrowWH"
        sigColor = ROOT.kViolet+6
    sigLabel = "" if options.dispR is None else "#scale[0.9]{(#sigma #times BR = "+sx+" pb)}" 

doMjj = options.variable=='' or options.variable=='mjj'
doMvv = options.variable=='' or options.variable=='mvv'


if doMjj:
  
    plotter=RooPlotter(inputDC)    
    if options.nToys>0:
      plotter.load_toys(options.toysFile,options.nToys)


    if options.fixMX is not None:
        plotter.fix("MH",options.fixMX)
    if options.fixR is not None:
        plotter.fix("r",options.fixR)

    if options.fit:
      if options.fitToy<0:
        data="data_obs"
      else:
        data="toy_"+str(options.fitToy)
      plotter.prefit(verbose=VERBOSE,data=data)

    if s!="":
        plotter.addContribution(s,True,sigLgd,2,1,sigColor,0,ROOT.kWhite)
    if options.splitWTopPeaks:
        plotter.addContribution("resW",False,"W peak",1,1,ROOT.TColor.GetColor("#00551B"),1001,ROOT.TColor.GetColor("#37B04D"),("","_opt")[OPTINRESW]) #4CB319"))
        plotter.addContribution("resTop",False,"top peak",1,1,ROOT.TColor.GetColor("#707A23"),1001,ROOT.TColor.GetColor("#C3D631"),("","_opt")[OPTINRESW]) #4CB319"))
    else:
        plotter.addContribution("res",False,"W+V/t",1,1,ROOT.TColor.GetColor("#0F5500"),1001,ROOT.TColor.GetColor("#60B037"),("","_opt")[OPTINRESW]) #4CB319"))
    plotter.addContribution("nonRes",False,"W+jets",1,1,ROOT.TColor.GetColor("#0041AA"),1001,ROOT.TColor.GetColor("#A5D2FF"),"_opt")


if doMvv:

    plotter2=RooPlotter(inputDC)
    if options.nToys>0:
      plotter2.load_toys(options.toysFile,options.nToys)

    if options.fixMX is not None:
        plotter2.fix("MH",options.fixMX)
    if options.fixR is not None:
        plotter2.fix("r",options.fixR)

    if options.fit:
      if options.fitToy<0:
        data="data_obs"
      else:
        data="toy_"+str(options.fitToy)
      plotter2.prefit(verbose=VERBOSE,data=data)


    if s!="":
        plotter2.addContribution(s,True,sigLgd,2,1,sigColor,0,ROOT.kWhite)
    plotter2.addContribution("nonRes",False,"W+jets",1,1,ROOT.TColor.GetColor("#0041AA"),1001,ROOT.TColor.GetColor("#A5D2FF"),"_opt")
    if options.splitWTopPeaks:
        plotter2.addContribution("resW",False,"W peak",1,1,ROOT.TColor.GetColor("#00551B"),1001,ROOT.TColor.GetColor("#37B04D"),("","_opt")[OPTINRESW]) #4CB319"))
        plotter2.addContribution("resTop",False,"top peak",1,1,ROOT.TColor.GetColor("#707A23"),1001,ROOT.TColor.GetColor("#C3D631"),("","_opt")[OPTINRESW]) #4CB319"))
    else:
        plotter2.addContribution("res",False,"W+V/t",1,1,ROOT.TColor.GetColor("#0F5500"),1001,ROOT.TColor.GetColor("#60B037"),("","_opt")[OPTINRESW]) #4CB319"))



lep = options.lepton
pur = options.purity
cat = options.category
eta = options.deltaeta

leptons = ['mu','e']
purities = ['LP','HP']
categories = ['bb','nobb','vbf']
deltaetas = ['DEtaLo','DEtaHi']


dataset="data_obs"
if options.fitToy>0:
  dataset="toy_"+str(options.fitToy)


for l in leptons:
    for p in purities:
        for c in categories:
          for e in deltaetas:
            #continue

            varMVV = "MLNuJ"
            varMJJ = "MJ"
            if options.differentBinning and c in ['bb','vbf']:
                varMVV = "MLNuJ_coarse"
                varMJJ = "MJ_coarse"

            subcat = '_'.join([l,p,c,e,YEAR])

            ##label="W #rightarrow "+(("e","#mu")[l=='mu'])+"#nu, "+p
            ##label="W#rightarrow"+(("e","#mu")[l=='mu'])+"#nu, "+(("low-purity","high-purity")[p=='HP'])
            ##label=(("electron","muon")[l=='mu'])+", "+(("low-purity","high-purity")[p=='HP'])
            #label="#bf{"+(("electron","muon")[l=='mu'])+", "+(("low-purity","high-purity")[p=='HP'])+"}"
            label=(("e","#mu")[l=='mu'])+", "+p+", "+c#+", "+YEAR

            if lep!='' and lep!=l: continue
            if pur!='' and pur!=p: continue 
            if cat!='' and cat!=c: continue
            if eta!='' and eta!=e: continue 

            if doMvv:
                pass

                #''' ## just low-mjet and high-mjet sidebands
                plotter2.drawBinned(varMVV,labelMVV,label,subcat,[0,0],options.doUncBand,1,0,varMJJ+":low:20:70",minMVV,maxMVV,YmaxMVV,False,-1,"",dataset)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_LowMJJ_"+sigStr+"_"+subcat)

                plotter2.drawBinned(varMVV,labelMVV,label,subcat,[0,0],options.doUncBand,1,0,varMJJ+":high:150:210",minMVV,maxMVV,YmaxMVV,False,-1,"",dataset)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_HighMJJ_"+sigStr+"_"+subcat)
                #'''

                ''' ## fully blind, full mjet range
                plotter2.drawBinned(varMVV,labelMVV,label,subcat,[0,10000],options.doUncBand,1,0,"",minMVV,maxMVV,YmaxMVV,False,-1,"",dataset)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVVBlind_"+sigStr+"_"+subcat)
                #'''

                ''' ## unblinded (for the paper)
                plotter2.drawBinned(varMVV,labelMVV,label,subcat,[0,0],options.doUncBand,1,0,"",minMVV,maxMVV,YmaxMVV,UNSTACKSIG,sigSF,sigLabel,dataset)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_"+sigStr+"_"+subcat)
                #'''
                ''' ## same but linear scale
                plotter2.drawBinned(varMVV,labelMVV,label,subcat,[0,0],options.doUncBand,0,0,"",minMVV,maxMVV,YmaxMVV,UNSTACKSIG,sigSF,sigLabel,dataset)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVVlinear_"+sigStr+"_"+subcat)
                #'''

                ''' ## unblinded (for tests with toys)
                plotter2.drawBinned(varMVV,labelMVV,label,subcat,[0,0],options.doUncBand,1,0,"",minMVV,maxMVV,YmaxMVV,False,-1,"",dataset)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_"+sigStr+"_"+subcat)
                #'''

                ''' ## unblinded, zoom on W mass region
                #plotter2.drawBinned(varMVV,labelMVV,label,subcat,[0,0],options.doUncBand,0,0,varMJJ+":sig:66:86",minMVV,maxMVV,YmaxMVV)
                #cmsLabel(plotter2.canvas)
                #saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVVW_"+sigStr+"_"+subcat)
                
                plotter2.frame.GetXaxis().SetRangeUser(1000.,2000.)
                plotter2.frame.GetYaxis().SetRangeUser(0.,1.1*(plotter2.frame.getHist("datapoints").GetY()[9]+plotter2.frame.getHist("datapoints").GetEYhigh()[9]))
                plotter2.frame2.GetXaxis().SetRangeUser(1000.,2000.)
                plotter2.line.SetX1(1000.)
                plotter2.line.SetX2(2000.)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVVWZoom_"+sigStr+"_"+subcat)
                #'''

                ''' ## unblinded, in MJJ slices
                plotter2.drawBinned(varMVV,labelMVV,"#splitline{"+label+"}{20 #leq m_{jet} < 70 GeV}",subcat,[0,0],options.doUncBand,1,0,varMJJ+":bin1:20:70",minMVV,maxMVV,YmaxMVV)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_MJJ020to070_"+sigStr+"_"+subcat)

                plotter2.drawBinned(varMVV,labelMVV,"#splitline{"+label+"}{70 #leq m_{jet} < 110 GeV}",subcat,[0,0],options.doUncBand,1,0,varMJJ+":bin2:70:110",minMVV,maxMVV,YmaxMVV)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_MJJ070to110_"+sigStr+"_"+subcat)

                plotter2.drawBinned(varMVV,labelMVV,"#splitline{"+label+"}{110 #leq m_{jet} < 150 GeV}",subcat,[0,0],options.doUncBand,1,0,varMJJ+":bin3:110:150",minMVV,maxMVV,YmaxMVV)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_MJJ110to150_"+sigStr+"_"+subcat)

                plotter2.drawBinned(varMVV,labelMVV,"#splitline{"+label+"}{150 #leq m_{jet} < 210 GeV}",subcat,[0,0],options.doUncBand,1,0,varMJJ+":bin4:150:210",minMVV,maxMVV,YmaxMVV)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_MJJ150to210_"+sigStr+"_"+subcat)
                #'''

                ''' ## debug 1
                plotter2.drawBinned(varMVV,labelMVV,"#splitline{"+label+"}{70 #leq m_{jet} < 100 GeV}",subcat,[0,0],options.doUncBand,1,0,varMJJ+":sig:70:100",minMVV,maxMVV,YmaxMVV)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/debug"+prefix+"MVV_MJ70to110_"+sigStr+"_"+subcat)

                plotter2.drawOverlay(varMVV,labelMVV,"#splitline{"+label+"}{70 #leq m_{jet} < 100 GeV}",subcat,[0,0],0,0,varMJJ+":sig:70:100",minMVV,maxMVV,YmaxMVV)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/debugOverlay_"+prefix+"MVV_MJ70to110_"+sigStr+"_"+subcat)
                #'''

                ''' ## debug 2
                plotter2.drawBinned(varMVV,labelMVV,"#splitline{"+label+"}{100 #leq m_{jet} < 140 GeV}",subcat,[0,0],options.doUncBand,1,0,varMJJ+":bindebug:100:140",minMVV,maxMVV,YmaxMVV)
                cmsLabel(plotter2.canvas)
                saveCanvas(plotter2.canvas,directory+"/"+prefix+"MVV_MJJ100to140_"+sigStr+"_"+subcat)
                #'''

            if doMjj:
                pass

                #''' ## blind
                plotter.drawBinned(varMJJ,labelMJJ,label,subcat,[70,150],options.doUncBand,0,0,"",minMJJ,maxMJJ,YmaxMJJ,False,-1,"",dataset)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJBlind_"+sigStr+"_"+subcat)
                #'''

                ''' ## unblinded (for tests with toys)
                plotter.drawBinned(varMJJ,labelMJJ,label,subcat,[0,0],options.doUncBand,0,0,"",minMJJ,maxMJJ,YmaxMJJ,False,-1,"",dataset)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJ_"+sigStr+"_"+subcat)
                #'''

                ''' ## unblinded (for the paper)
                plotter.drawBinned(varMJJ,labelMJJ,label,subcat,[0,0],options.doUncBand,0,0,"",minMJJ,maxMJJ,YmaxMJJ,UNSTACKSIG,sigSF,sigLabel,dataset)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJ_"+sigStr+"_"+subcat)
                #'''

                ''' ## blind, in MVV slices
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{0.6 #leq m_{WV} < 1 TeV}",subcat,[70,150],options.doUncBand,0,0,varMVV+":bin1:600:1000",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJBlind_MVV0600to1000_"+sigStr+"_"+subcat)
                
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{1 #leq m_{WV} < 1.5 TeV}",subcat,[70,150],options.doUncBand,0,0,varMVV+":bin2:1000:1500",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJBlind_MVV1000to1500_"+sigStr+"_"+subcat)

                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{1.5 #leq m_{WV} < 5 TeV}",subcat,[70,150],options.doUncBand,0,2,varMVV+":bin3:1500:5000",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJBlind_MVV1500to5000_"+sigStr+"_"+subcat)
                #'''

                ''' ## unblinded, in MVV slices
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{0.6 #leq m_{WV} < 1 TeV}",subcat,[0,0],options.doUncBand,0,0,varMVV+":bin1:600:1000",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJ_MVV0600to1000_"+sigStr+"_"+subcat)
                
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{1 #leq m_{WV} < 1.5 TeV}",subcat,[0,0],options.doUncBand,0,0,varMVV+":bin2:1000:1500",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJ_MVV1000to1500_"+sigStr+"_"+subcat)

                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{1.5 #leq m_{WV} < 5 TeV}",subcat,[0,0],options.doUncBand,0,2,varMVV+":bin3:1500:5000",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJ_MVV1500to5000_"+sigStr+"_"+subcat)
                #'''

                ''' ## debug 1
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{1 #leq m_{WV} < 1.5 TeV}",subcat,[0,0],options.doUncBand,0,0,varMVV+":bin1:1000:1500",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/debug"+prefix+"MJJ_MVV1000to1500_"+sigStr+"_"+subcat)
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{1.5 #leq m_{WV} < 2 TeV}",subcat,[0,0],options.doUncBand,0,0,varMVV+":bin1:1500:2000",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/debug"+prefix+"MJJ_MVV1500to2000_"+sigStr+"_"+subcat)
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{2 #leq m_{WV} < 3 TeV}",subcat,[0,0],options.doUncBand,0,0,varMVV+":bin1:2000:3000",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/debug"+prefix+"MJJ_MVV2000to3000_"+sigStr+"_"+subcat)

                plotter.drawOverlay(varMJJ,labelMJJ,"#splitline{"+label+"}{1.5 #leq m_{WV} < 2 TeV}",subcat,[0,0],0,0,varMVV+":bin1:1500:2000",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/debugOverlay_"+prefix+"MJJ_MVV1500to2000_"+sigStr+"_"+subcat)
                #'''

                ''' ## debug 2
                plotter.drawBinned(varMJJ,labelMJJ,"#splitline{"+label+"}{0.8 #leq m_{WV} < 1.2 TeV}",subcat,[0,0],options.doUncBand,0,0,varMVV+":bindebug:800:1200",minMJJ,maxMJJ,YmaxMJJ)
                cmsLabel(plotter.canvas)
                saveCanvas(plotter.canvas,directory+"/"+prefix+"MJJ_MVV0800to1200_"+sigStr+"_"+subcat)
                #'''








