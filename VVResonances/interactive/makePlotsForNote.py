import os
import ROOT
import numpy as np
from ROOT import gStyle,gROOT,gPad
from array import array
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from CMGTools.VVResonances.plotting.RooPlotter import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="Run2",help="2016 or 2017 or 2018 or Run2")
parser.add_option("-o","--outDir",dest="outDirPrefix",default='PlotsTemplates_',help="where to save the plots")
parser.add_option("-p","--plots",dest="plots",default='all',help="possible plots: all, signal, nonResTpl, nonResSys, CRNonResTpl, CRNonResSys, resTpl, resSys, CRResTpl, CRResSys, resW, resTop, scaleres")
parser.add_option("-d","--withDC",dest="withDC",type=int,default=1,help="include plots that require datacards")
parser.add_option("-D","--differentBinning",action="store_true",dest="differentBinning",help="use other binning for bb category",default=True)
(options,args) = parser.parse_args()

YEAR=options.year
inDir='Inputs_'+YEAR+'/'
outDir=options.outDirPrefix+YEAR+'/'


plots = options.plots
if 'all' in plots:
    plots = plots + ', signal, nonResTpl, nonResSys, CRNonResTpl, CRNonResSys, resTpl, resSys, CRResTpl, CRResSys, scaleres'


COMPYEARS=0
inDir16='Inputs_2016/'
inDir17='Inputs_2017/'
inDir18='Inputs_2018/'
inDirR2='Inputs_Run2/'

DOXWW=1
DOXWZ=1
DOXWH=1
DOVBFXWW=1

#signals = ['XWW','XWZ','XWH','VBFXWW']
signals = []
if DOXWW: signals.append('XWW')
if DOXWZ: signals.append('XWZ')
if DOXWH: signals.append('XWH')
if DOVBFXWW: signals.append('VBFXWW')

colorSignal = { 
    'XWW':    ROOT.kOrange+2,
    'XWZ':    ROOT.kViolet-8,
    'XWH':    ROOT.kTeal-6,
    'VBFXWW': ROOT.kBlue-7,
}
colorGradientSignal = {
    'XWW':    ["#8B4D00","#A15900","#B16200","#C36B01","#D97700","#ED8200","#FF8D00","#FF9410","#FF9B1F","#FFA22F","#FFAA40"],
    'XWZ':    ["#57008E","#62009F","#6E00B2","#7900C4","#8500D8","#9200ED","#9E00FF","#A410FF","#AB24FF","#B235FF","#B844FF"],
    'XWH':    ["#005036","#015F41","#016C4A","#007C55","#008B5F","#009E6C","#00AE77","#00BF83","#00D08E","#00E19A","#00F7A9"],
    'VBFXWW': ["#001950","#00226B","#002A86","#0033A0","#003EC3","#0047E1","#0051FF","#3072FF","#2268FF","#3072FF","#407DFF"],
}
markerSignal = { 
    'XWW':    20,
    'XWZ':    21,
    'XWH':    22,
    'VBFXWW': 20,
}
legendSignal = { 
    'XWW':    "X #rightarrow WW",
    'XWZ':    "X #rightarrow WZ",
    'XWH':    "X #rightarrow WH",
    'VBFXWW': "VBF X #rightarrow WW",
}

colorUp=ROOT.kRed
colorDn=ROOT.kAzure+1

leptons = ['mu','e']#['allL']#
purities = ['LP','HP']#['allP']#
categories = ['bb','nobb','vbf']   #['allC']#['bb','nobbHP','nobbLP']#

DcFolder = 'Dc_XWW'

minMJJ=20.0
maxMJJ=210.0

minMVV=600.0
maxMVV=5000.0

binsMJJ={}
binsMJJ['bb']=19
binsMJJ['nobb']=38
binsMJJ['nobbHP']=38
binsMJJ['nobbLP']=38
binsMJJ['nob']=95
binsMJJ['vbf']=19
binsMJJ['allC']=38#95
binsMVV={}
binsMVV['bb']=176#44
binsMVV['nobb']=176
binsMVV['nobbHP']=176
binsMVV['nobbLP']=176
binsMVV['nob']=176
binsMVV['vbf']=176
binsMVV['allC']=176

varMVV = {}
varMJJ = {}
for c in categories:
    varMVV[c] = "MLNuJ"
    varMJJ[c] = "MJ"
    if options.differentBinning and c in ['bb','vbf']:
        varMVV[c] = "MLNuJ_coarse"
        varMJJ[c] = "MJ_coarse"

minmx=700 #500
maxmx=8100



def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  #canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  #os.system("rm "+name+".eps")

def setColZGradient_Rainbow1():
    NRGBs = 5
    NCont = 255
    stops = [ 0.00, 0.34, 0.61, 0.84, 1.00 ]
    red   = [ 0.00, 0.00, 0.87, 1.00, 0.51 ]
    green = [ 0.00, 0.81, 1.00, 0.20, 0.00 ]
    blue  = [ 0.51, 1.00, 0.12, 0.00, 0.00 ]
    stopsArray = array('d', stops)
    redArray   = array('d', red)
    greenArray = array('d', green)
    blueArray  = array('d', blue)
    ROOT.TColor.CreateGradientColorTable(NRGBs, stopsArray, redArray, greenArray, blueArray, NCont)
    gStyle.SetNumberContours(NCont)

def setColZGradient_PosNeg():
    NRGBs = 4
    NCont = 255
    stops = [ 0.00, 0.20, 0.50, 1.00 ]
    red   = [ 243./256., 256./256., 1.00,   0./256. ]
    green = [ 113./256., 150./256., 1.00,   0./256. ]
    blue  = [   0./256.,   0./256., 1.00, 220./256. ]
    stopsArray = array('d', stops)
    redArray   = array('d', red)
    greenArray = array('d', green)
    blueArray  = array('d', blue)
    ROOT.TColor.CreateGradientColorTable(NRGBs, stopsArray, redArray, greenArray, blueArray, NCont)
    gStyle.SetNumberContours(NCont)

def normalizePerSlice(h, sliceInX=True):
    nbinsx = h.GetNbinsX()
    nbinsy = h.GetNbinsY()
    if sliceInX:
        for bx in range(nbinsx+2):
            sliceNorm = h.Integral(bx,bx,0,nbinsy+1)
            if sliceNorm!=0:
                for by in range(nbinsy+2):
                    h.SetBinContent(bx,by,h.GetBinContent(bx,by)/sliceNorm)
    else:
        for by in range(nbinsy+2):
            sliceNorm = h.Integral(0,nbinsx+1,by,by)
            if sliceNorm!=0:
                for bx in range(nbinsx+2):
                    h.SetBinContent(bx,by,h.GetBinContent(bx,by)/sliceNorm)
    axisToChange = h.GetXaxis() if sliceInX else h.GetYaxis() 
    axisToChange.SetTitle(axisToChange.GetTitle()+" (normalized per slice)")









def makeShapeUncertainties2D(filename,sample,syst):
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    setColZGradient_PosNeg()

    f=ROOT.TFile(filename)
    hN = f.Get("histo")
    if not f.GetListOfKeys().Contains("histo_"+syst+"Up"):
        print 'Warning in makeShapeUncertainties2D: did not find uncertainty', syst
        return
    hU = f.Get("histo_"+syst+"Up")
    hD = f.Get("histo_"+syst+"Down")
    hN.Scale(1./hN.Integral())
    hU.Scale(1./hU.Integral())
    hD.Scale(1./hD.Integral())
    hU.Divide(hN)
    hD.Divide(hN)

    c=ROOT.TCanvas("c")
    c.cd()
    hU.GetXaxis().SetTitle("m_{WV} (GeV)")
    hU.GetYaxis().SetTitle("m_{jet} (GeV)")
    hU.Draw("COLZ")
    c.Update()
    c.UseCurrentStyle()
    c.SetRightMargin(0.14)
    hU.GetZaxis().SetRangeUser(0.5,1.5)
    #hU.GetZaxis().SetRangeUser(0.95,1.05)
    pal=hU.GetListOfFunctions().FindObject("palette")
    pal.SetX1NDC(0.875)
    pal.SetX2NDC(0.90)
    saveCanvas(c,outDir+"/"+sample+"_"+syst+"_2DUp")

    c=ROOT.TCanvas("c")
    c.cd()
    hD.GetXaxis().SetTitle("m_{WV} (GeV)")
    hD.GetYaxis().SetTitle("m_{jet} (GeV)")
    hD.Draw("COLZ")
    c.Update()
    c.UseCurrentStyle()
    c.SetRightMargin(0.14)
    hD.GetZaxis().SetRangeUser(0.5,1.5)
    #hD.GetZaxis().SetRangeUser(0.95,1.05)
    pal=hD.GetListOfFunctions().FindObject("palette")
    pal.SetX1NDC(0.875)
    pal.SetX2NDC(0.90)
    saveCanvas(c,outDir+"/"+sample+"_"+syst+"_2DDown")

def makeShapeUncertaintiesProj2D(filename,sample,syst):
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

    f=ROOT.TFile(filename)
    hN = f.Get("histo")
    if not f.GetListOfKeys().Contains("histo_"+syst+"Up"):
        print 'Warning in makeShapeUncertaintiesProj2D: did not find uncertainty', syst
        return
    hU = f.Get("histo_"+syst+"Up")
    hD = f.Get("histo_"+syst+"Down")
    
    cX=ROOT.TCanvas("cX")
    cX.cd()
    padX1 = ROOT.TPad("padX1","",0.0,0.24,1.0,0.95,0)
    padX2 = ROOT.TPad("padX2","",0.0,0.0,1.0,0.24,0)
    padX1.SetTopMargin(0.)
    padX1.SetBottomMargin(0.028)
    padX1.SetLeftMargin(0.14)
    padX1.SetRightMargin(0.04)
    padX2.SetTopMargin(0.)
    padX2.SetBottomMargin(0.5)
    padX2.SetLeftMargin(0.14)
    padX2.SetRightMargin(0.04)
    padX1.Draw()
    padX2.Draw()
    padX1.cd()
    projXN=hN.Clone().ProjectionX("qqqX")
    projXN.Scale(1./projXN.Integral())
    projXN.SetLineWidth(3)
    projXN.SetLineColor(ROOT.kBlack)
    #projXN.GetYaxis().SetRangeUser(0,)
    projXN.GetXaxis().SetLabelOffset(3)
    projXN.Draw("HIST")
    projXU=hU.Clone().ProjectionX("qqqqX")
    projXU.Scale(1./projXU.Integral())
    projXU.SetLineWidth(3)
    projXU.SetLineColor(colorUp)
    projXU.GetXaxis().SetLabelOffset(3)
    projXU.Draw("HIST,SAME")
    projXD=hD.Clone().ProjectionX("qqqqqX")
    projXD.Scale(1./projXD.Integral())
    projXD.SetLineWidth(3)
    projXD.SetLineColor(colorDn)
    projXD.GetXaxis().SetLabelOffset(3)
    projXD.Draw("HIST,SAME")
    projXN.GetYaxis().SetRangeUser(0,1.1*max(projXN.GetMaximum(),projXU.GetMaximum(),projXD.GetMaximum()))
    lX=ROOT.TLegend(0.6,0.65,0.95,0.95)
    lX.SetHeader(syst+" parameter")
    lX.AddEntry(projXN,"nominal","l")
    lX.AddEntry(projXU,"up","l")
    lX.AddEntry(projXD,"down","l")
    lX.SetBorderSize(0)
    lX.SetFillStyle(0)
    lX.SetTextSize(0.05)
    lX.Draw()
    padX1.RedrawAxis()
    padX1.Update()
    padX2.cd()
    padX2.SetGridy()
    ratioXN=projXN.Clone()
    ratioXN.Divide(ratioXN)
    ratioXN.GetXaxis().SetLabelSize(0.16)
    ratioXN.GetYaxis().SetLabelSize(0.125)
    ratioXN.GetXaxis().SetLabelOffset(0.007)
    ratioXN.GetXaxis().SetTitleSize(0.21)
    ratioXN.GetYaxis().SetTitleSize(0.11)
    ratioXN.GetXaxis().SetTitleOffset(0.95)
    ratioXN.GetYaxis().SetTitleOffset(0.45)
    ratioXN.GetXaxis().SetTitle("m_{WV} (GeV)")
    ratioXN.GetYaxis().SetTitle("Ratio to nominal")
    ratioXN.GetYaxis().SetNdivisions(206)
    ratioXN.GetYaxis().SetRangeUser(0.51,1.49)
    ratioXN.Draw("HIST")
    ratioXU=projXU.Clone()
    ratioXU.Divide(projXN)
    ratioXU.Draw("HIST,SAME")
    ratioXD=projXD.Clone()
    ratioXD.Divide(projXN)
    ratioXD.Draw("HIST,SAME")
    padX2.RedrawAxis()
    padX2.Update()
    saveCanvas(cX,outDir+"/"+sample+"_"+syst+"_ProjX")

    cY=ROOT.TCanvas("cY")
    cY.cd()
    padY1 = ROOT.TPad("padY1","",0.0,0.24,1.0,0.95,0)
    padY2 = ROOT.TPad("padY2","",0.0,0.0,1.0,0.24,0)
    padY1.SetTopMargin(0.)
    padY1.SetBottomMargin(0.028)
    padY1.SetLeftMargin(0.14)
    padY1.SetRightMargin(0.04)
    padY2.SetTopMargin(0.)
    padY2.SetBottomMargin(0.5)
    padY2.SetLeftMargin(0.14)
    padY2.SetRightMargin(0.04)
    padY1.Draw()
    padY2.Draw()
    padY1.cd()
    projYN=hN.Clone().ProjectionY("qqqY")
    projYN.Scale(1./projYN.Integral())
    projYN.SetLineWidth(3)
    projYN.SetLineColor(ROOT.kBlack)
    projYN.GetXaxis().SetLabelOffset(3)
    projYN.Draw("HIST")
    projYU=hU.Clone().ProjectionY("qqqqY")
    projYU.Scale(1./projYU.Integral())
    projYU.SetLineWidth(3)
    projYU.SetLineColor(colorUp)
    projYU.GetXaxis().SetLabelOffset(3)
    projYU.Draw("HIST,SAME")
    projYD=hD.Clone().ProjectionY("qqqqqY")
    projYD.Scale(1./projYD.Integral())
    projYD.SetLineWidth(3)
    projYD.SetLineColor(colorDn)
    projYD.GetXaxis().SetLabelOffset(3)
    projYD.Draw("HIST,SAME")
    projYN.GetYaxis().SetRangeUser(0,1.1*max(projYN.GetMaximum(),projYU.GetMaximum(),projYD.GetMaximum()))
    lY=ROOT.TLegend(0.6,0.65,0.95,0.95)
    lY.SetHeader(syst+" parameter")
    lY.AddEntry(projYN,"nominal","l")
    lY.AddEntry(projYU,"up","l")
    lY.AddEntry(projYD,"down","l")
    lY.SetBorderSize(0)
    lY.SetFillStyle(0)
    lY.SetTextSize(0.05)
    lY.Draw()
    padY1.RedrawAxis()
    padY1.Update()
    padY2.cd()
    padY2.SetGridy()
    ratioYN=projYN.Clone()
    ratioYN.Divide(ratioYN)
    ratioYN.GetXaxis().SetLabelSize(0.16)
    ratioYN.GetYaxis().SetLabelSize(0.125)
    ratioYN.GetXaxis().SetLabelOffset(0.007)
    ratioYN.GetXaxis().SetTitleSize(0.21)
    ratioYN.GetYaxis().SetTitleSize(0.11)
    ratioYN.GetXaxis().SetTitleOffset(0.95)
    ratioYN.GetYaxis().SetTitleOffset(0.45)
    ratioYN.GetXaxis().SetTitle("m_{jet} (GeV)")
    ratioYN.GetYaxis().SetTitle("Ratio to nominal")
    ratioYN.GetYaxis().SetNdivisions(206)
    ratioYN.GetYaxis().SetRangeUser(0.51,1.49)
    ratioYN.Draw("HIST")
    ratioYU=projYU.Clone()
    ratioYU.Divide(projYN)
    ratioYU.Draw("HIST,SAME")
    ratioYD=projYD.Clone()
    ratioYD.Divide(projYN)
    ratioYD.Draw("HIST,SAME")
    padY2.RedrawAxis()
    padY2.Update()
    saveCanvas(cY,outDir+"/"+sample+"_"+syst+"_ProjY")

def makeShapeUncertainties1D(filename,sample,syst,axistitle):
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

    f=ROOT.TFile(filename)
    hN = f.Get("histo")
    if not f.GetListOfKeys().Contains("histo_"+syst+"Up"):
        print 'Warning in makeShapeUncertainties1D: did not find uncertainty', syst
        return
    hU = f.Get("histo_"+syst+"Up")
    hD = f.Get("histo_"+syst+"Down")
    
    c=ROOT.TCanvas("c")
    c.cd()
    pad1 = ROOT.TPad("pad1","",0.0,0.24,1.0,0.95,0)
    pad2 = ROOT.TPad("pad2","",0.0,0.0,1.0,0.24,0)
    pad1.SetTopMargin(0.)
    pad1.SetBottomMargin(0.028)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.04)
    pad2.SetTopMargin(0.)
    pad2.SetBottomMargin(0.5)
    pad2.SetLeftMargin(0.14)
    pad2.SetRightMargin(0.04)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    hN.Scale(1./hN.Integral())
    hN.SetStats(0)
    hN.SetLineWidth(3)
    hN.SetLineColor(ROOT.kBlack)
    hN.GetXaxis().SetLabelOffset(3)
    hN.Draw("HIST")
    hU.Scale(1./hU.Integral())
    hU.SetStats(0)
    hU.SetLineWidth(3)
    hU.SetLineColor(colorUp)
    hU.GetXaxis().SetLabelOffset(3)
    hU.Draw("HIST,SAME")
    hD.Scale(1./hD.Integral())
    hD.SetStats(0)
    hD.SetLineWidth(3)
    hD.SetLineColor(colorDn)
    hD.GetXaxis().SetLabelOffset(3)
    hD.Draw("HIST,SAME")
    hN.GetYaxis().SetRangeUser(0,1.1*max(hN.GetMaximum(),hU.GetMaximum(),hD.GetMaximum()))
    l=ROOT.TLegend(0.6,0.65,0.95,0.95)
    l.SetHeader(syst+" parameter")
    l.AddEntry(hN,"nominal","l")
    l.AddEntry(hU,"up","l")
    l.AddEntry(hD,"down","l")
    l.SetBorderSize(0)
    l.SetFillStyle(0)
    l.SetTextSize(0.05)
    l.Draw()
    pad1.RedrawAxis()
    pad1.Update()
    pad2.cd()
    pad2.SetGridy()
    ratioN=hN.Clone()
    ratioN.Divide(ratioN)
    ratioN.GetXaxis().SetLabelSize(0.16)
    ratioN.GetYaxis().SetLabelSize(0.125)
    ratioN.GetXaxis().SetLabelOffset(0.007)
    ratioN.GetXaxis().SetTitleSize(0.21)
    ratioN.GetYaxis().SetTitleSize(0.11)
    ratioN.GetXaxis().SetTitleOffset(0.95)
    ratioN.GetYaxis().SetTitleOffset(0.45)
    ratioN.GetXaxis().SetTitle(axistitle)
    ratioN.GetYaxis().SetTitle("Ratio to nominal")
    ratioN.GetYaxis().SetNdivisions(206)
    ratioN.GetYaxis().SetRangeUser(0.51,1.49)
    ratioN.Draw("HIST")
    ratioU=hU.Clone()
    ratioU.Divide(hN)
    ratioU.Draw("HIST,SAME")
    ratioD=hD.Clone()
    ratioD.Divide(hN)
    ratioD.Draw("HIST,SAME")
    pad2.RedrawAxis()
    pad2.Update()
    saveCanvas(c,outDir+"/"+sample+"_"+syst+"_")



    
def extractResTemplateFromDC(DCfilename,cat,outputname,c):
    f = ROOT.TFile(DCfilename)
    w = f.Get("w")
    pdf = w.pdf("shapeBkg_res_"+cat)
    h2 = pdf.createHistogram(varMVV[c]+","+varMJJ[c])
    h2.GetXaxis().SetTitle("m_{WV} (GeV)")
    h2.GetYaxis().SetTitle("m_{jet} (GeV)")
    h2.GetZaxis().SetTitle("")
    fOut = ROOT.TFile(outputname+".root","recreate")
    h2.Write("histo")
    fOut.Close()

def extractResWTemplateFromDC(DCfilename,cat,outputname,c):
    f = ROOT.TFile(DCfilename)
    w = f.Get("w")
    pdf = w.pdf("shapeBkg_resW_"+cat)
    h2 = pdf.createHistogram(varMVV[c]+","+varMJJ[c])
    h2.GetXaxis().SetTitle("m_{WV} (GeV)")
    h2.GetYaxis().SetTitle("m_{jet} (GeV)")
    h2.GetZaxis().SetTitle("")
    fOut = ROOT.TFile(outputname+".root","recreate")
    h2.Write("histo")
    fOut.Close()

def extractResTopTemplateFromDC(DCfilename,cat,outputname,c):
    f = ROOT.TFile(DCfilename)
    w = f.Get("w")
    pdf = w.pdf("shapeBkg_resTop_"+cat)
    h2 = pdf.createHistogram(varMVV[c]+","+varMJJ[c])
    h2.GetXaxis().SetTitle("m_{WV} (GeV)")
    h2.GetYaxis().SetTitle("m_{jet} (GeV)")
    h2.GetZaxis().SetTitle("")
    fOut = ROOT.TFile(outputname+".root","recreate")
    h2.Write("histo")
    fOut.Close()

def extractSignalTemplateFromDC(DCfilename,pdfname,signal,mx,outputname,c):
    f = ROOT.TFile(DCfilename)
    w = f.Get("w")
    w.var("MH").setVal(mx)
    w.var("MH").setConstant(1)
    pdf = w.pdf(pdfname)
    h2 = pdf.createHistogram(varMVV[c]+","+varMJJ[c])
    h2.GetXaxis().SetTitle("m_{WV} (GeV)")
    h2.GetYaxis().SetTitle("m_{jet} (GeV)")
    h2.GetZaxis().SetTitle("")
    fOut = ROOT.TFile(outputname+".root","update")
    h2.Write(signal+str(mx).zfill(4))
    fOut.Close()
    f.Close()

def extractSignalMjjPdfFromDC(DCfilename,pdfname,signal,mx,outputname,c):
    f = ROOT.TFile(DCfilename)
    w = f.Get("w")
    w.var("MH").setVal(mx)
    w.var("MH").setConstant(1)
    pdf = w.pdf(pdfname)
    h = pdf.createHistogram(varMJJ[c])
    h.GetXaxis().SetTitle("m_{jet} (GeV)")
    h.GetYaxis().SetTitle("")
    fOut = ROOT.TFile(outputname+".root","update")
    h.Write(signal+str(mx).zfill(4))
    fOut.Close()

def extractSignalVsMXTemplateFromDC(DCfilename,signal,cat,outputname,c):
    f = ROOT.TFile(DCfilename)
    w = f.Get("w")
    pdf = w.pdf(signal+"_"+cat)
    h2 = pdf.createHistogram("histo", w.var("MH"), ROOT.RooFit.Binning(binsMVV[c],minMVV,maxMVV), ROOT.RooFit.YVar(w.var(varMJJ[c]),ROOT.RooFit.Binning(binsMJJ[c],minMJJ,maxMJJ)))#, ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(w.var("MH"))))
    h2.GetXaxis().SetTitle("m_{X} (GeV)")
    h2.GetYaxis().SetTitle("m_{jet} (GeV)")
    h2.GetZaxis().SetTitle("")
    fOut = ROOT.TFile(outputname+".root","recreate")
    h2.Write("histo")
    fOut.Close()


def makeTemplate2D(filename,histoname,outputname,logz=True,normXSlice=False,xtitle="m_{WV} (GeV)"):
    if not os.path.isfile(filename):
        print "Error in makeTemplate2D: file "+filename+" does not exist."
        return
    f = ROOT.TFile(filename)
    h2 = f.Get(histoname)
    if not(h2):
        print "Error in makeTemplate2D, file "+filename+": histogram "+histoname+" does not exist."
        return
    if normXSlice: normalizePerSlice(h2)
    c = ROOT.TCanvas("c")
    c.cd()
    setColZGradient_Rainbow1()
    h2.Draw("COLZ")
    h2.GetXaxis().SetTitle(xtitle)
    h2.GetYaxis().SetTitle("m_{jet} (GeV)")
    if logz: h2.SetMinimum(max(1e-12,h2.GetMinimum())) #h2.GetMaximum()/(1e3 if histoname=='resW' else 2e7))
    #else: h2.SetMinimum(-0.005)
    c.Update()
    c.UseCurrentStyle()
    if logz: c.SetLogz()
    c.SetRightMargin(0.14)
    h2.GetXaxis().SetLabelSize(0.035)
    pal=h2.GetListOfFunctions().FindObject("palette")
    pal.SetX1NDC(0.875)
    pal.SetX2NDC(0.90)
    saveCanvas(c,outDir+"/"+outputname)
    c.Close()


def makeTemplateVsReco2D(filenameTpt,histonameTpt,filenameReco,histonameReco,outputname,rebinx=0,rebiny=0):
    if not os.path.isfile(filenameTpt):
        print "Error in makeTemplateVsReco2D: file "+filenameTpt+" does not exist."
        return
    if not os.path.isfile(filenameReco):
        print "Error in makeTemplateVsReco2D: file "+filenameReco+" does not exist."
        return
    fTpt = ROOT.TFile(filenameTpt)
    hTpt = fTpt.Get(histonameTpt)
    fReco = ROOT.TFile(filenameReco)
    hReco = fReco.Get(histonameReco)
    if rebinx!=0:
        print "Info in makeTemplateVsReco2D: rebinning x axis ("+str(rebinx)+")"
        hTpt.RebinX(rebinx)
        hReco.RebinX(rebinx)    
    if rebiny!=0:
        print "Info in makeTemplateVsReco2D: rebinning y axis ("+str(rebiny)+")"
        hTpt.RebinY(rebiny)
        hReco.RebinY(rebiny)
    hTpt.Scale(1./hTpt.Integral())
    hReco.Scale(1./hReco.Integral())
    c = ROOT.TCanvas("c")
    c.cd()
    setColZGradient_PosNeg()
    h=hReco.Clone()
    h.Reset()
    for i in range(1,h.GetNbinsX()+1):
        for j in range(1,h.GetNbinsY()+1):
            if hReco.GetBinContent(i,j)!=0:
                value = (hReco.GetBinContent(i,j)-hTpt.GetBinContent(i,j))/hReco.GetBinError(i,j)
                #print hReco.GetBinContent(i,j), hTpt.GetBinContent(i,j), hReco.GetBinError(i,j), value
                h.SetBinContent(i,j,value)
    h.Draw("COLZ")
    h.GetXaxis().SetTitle("m_{WV} (GeV)")
    h.GetYaxis().SetTitle("m_{jet} (GeV)")
    h.GetZaxis().SetTitle("(reco #minus template) / #sigma(reco)")
    h.SetMinimum(-10.)
    h.SetMaximum(10.)
    c.Update()
    c.UseCurrentStyle()
    c.SetRightMargin(0.14)
    h.GetXaxis().SetLabelSize(0.035)
    h.GetZaxis().SetTitleOffset(0.9)
    pal=h.GetListOfFunctions().FindObject("palette")
    pal.SetX1NDC(0.875)
    pal.SetX2NDC(0.90)
    saveCanvas(c,outDir+"/"+outputname)


def makeTemplate1D(filename,histoname,outputname,xaxistitle):
    f = ROOT.TFile(filename)
    h = f.Get(histoname)
    c=ROOT.TCanvas("c")
    c.cd()
    h.Draw("HIST")
    h.GetXaxis().SetTitle(xaxistitle)
    c.Update()
    c.UseCurrentStyle()
    h.SetStats(0)
    c.SetLogy()
    saveCanvas(c,outDir+"/"+outputname)

def makeTemplateVsReco1D(filenameTpt,histonameTpt,filenameReco,histonameReco,outputname,var,xaxistitle):
    fTpt = ROOT.TFile(filenameTpt)
    hTpt = fTpt.Get(histonameTpt)
    hTpt.Scale(1./hTpt.Integral())
    fReco = ROOT.TFile(filenameReco)
    hReco2D = fReco.Get(histonameReco)
    if var=="MVV":
        hReco = hReco2D.Clone().ProjectionX('_px')
    elif var=="MJJ":
        hReco = hReco2D.Clone().ProjectionY('_py')
    hReco.Scale(1./hReco.Integral())
    c=ROOT.TCanvas("c")
    c.cd()
    hTpt.Draw("HIST")
    hReco.Draw("p,same")
    c.Update()
    c.UseCurrentStyle()
    colorTpt=ROOT.kGray+1
    colorReco=ROOT.kGray+3
    hTpt.SetLineColor(colorTpt)
    hTpt.GetXaxis().SetTitle(xaxistitle)
    hReco.SetLineColor(colorReco)
    hReco.SetMarkerColor(colorReco)
    hReco.SetMarkerSize(0.3)
    hTpt.SetStats(0)
    if var=="MVV":
        c.SetLogy()
    lgd=ROOT.TLegend(0.45,0.91-2*0.042,0.9,0.91)
    lgd.SetBorderSize(0)
    lgd.SetFillStyle(0)
    lgd.SetTextFont(42)
    lgd.SetTextSize(0.036)
    lgd.AddEntry(hReco,"Reconstructed simulation","pe")
    lgd.AddEntry(hTpt,"Template","l")
    lgd.Draw()
    saveCanvas(c,outDir+"/"+outputname)

    
def compCategories(fileprefix,histoname,projection,lep,pur,cat,outputprefix,var,xaxistitle,logy=False,rebin=0):
    c1=ROOT.TCanvas("c")
    c1.cd()
    if logy:
        c1.SetLogy()

    nL=len(lep)
    nP=len(pur)
    nC=len(cat)
    f = np.zeros((nL,nP,nC),dtype=object)
    h2 = np.zeros((nL,nP,nC),dtype=object)
    h = np.zeros((nL,nP,nC),dtype=object)
    hmaxmax = 0.

    for l in range(nL):
        for p in range(nP):
            for c in range(nC):
                filename = fileprefix+"_"+lep[l]+"_"+pur[p]+"_"+cat[c]+".root" 
                if not os.path.isfile(filename):
                    print "Error in compCategories: file "+filename+" does not exist."
                    return
                f[l][p][c] = ROOT.TFile(filename)
                if projection:
                    h2[l][p][c] = f[l][p][c].Get(histoname)
                    if var=="MVV":
                        h[l][p][c] = h2[l][p][c].Clone().ProjectionX('_px_'+lep[l]+'_'+pur[p]+'_'+cat[c])
                    elif var=="MJJ":
                        h[l][p][c] = h2[l][p][c].Clone().ProjectionY('_py_'+lep[l]+'_'+pur[p]+'_'+cat[c])
                else:
                    h[l][p][c] = f[l][p][c].Get(histoname)
                if rebin!=0:
                    print "Info in compCategories: rebinning ("+str(rebin)+")"
                    h[l][p][c].Rebin(rebin)
                h[l][p][c].Scale(1./h[l][p][c].Integral())
                hmax = h[l][p][c].GetMaximum()
                if hmax>hmaxmax:
                    hmaxmax = hmax
    if not logy:
        h[0][0][0].SetMinimum(0)
    h[0][0][0].SetMaximum(hmaxmax*(2. if logy else 1.1))

    lepColor=[ROOT.kBlue,ROOT.kRed]
    purHue=[-9,+2]
    catStyle=[1,3,9]
    lgd=ROOT.TLegend(0.6,0.91-2*2*nC*0.042,0.9,0.91)
    lgd.SetBorderSize(0)
    lgd.SetFillStyle(0)
    lgd.SetTextFont(42)
    lgd.SetTextSize(0.036)

    for l in range(nL):
        for p in range(nP):
            for c in range(nC):
                h[l][p][c].GetXaxis().SetTitle(xaxistitle)
                h[l][p][c].GetYaxis().SetTitle("integral normalized to 1")
                h[l][p][c].UseCurrentStyle()
                h[l][p][c].SetStats(0)
                h[l][p][c].SetLineColor(lepColor[l]+purHue[p])
                h[l][p][c].SetLineStyle(catStyle[c])
                lgd.AddEntry(h[l][p][c],lep[l]+", "+pur[p]+", "+cat[c],"l")
                h[l][p][c].Draw("hist,same")

    lgd.Draw()
    saveCanvas(c1,outDir+"/"+outputprefix+"_"+var+("_log" if logy else ""))


def compYears(fileprefixes,legends,histoname,projection,lep,pur,cat,outputprefix,var,xaxistitle,logy=False,rebin=0):

    nL=len(lep)
    nP=len(pur)
    nC=len(cat)
    nF=len(fileprefixes)
    ca = np.zeros((nL,nP,nC),dtype=object)
    lgd = np.zeros((nL,nP,nC),dtype=object)
    f = np.zeros((nL,nP,nC,nF),dtype=object)
    h2 = np.zeros((nL,nP,nC,nF),dtype=object)
    h = np.zeros((nL,nP,nC,nF),dtype=object)

    for l in range(nL):
        for p in range(nP):
            for c in range(nC):

                ca[l][p][c]=ROOT.TCanvas("c_"+lep[l]+"_"+pur[p]+"_"+cat[c])
                ca[l][p][c].cd()
                if logy:
                    ca[l][p][c].SetLogy()

                for i in range(nF):
                    filename = fileprefixes[i]+"_"+lep[l]+"_"+pur[p]+"_"+cat[c]+".root" 
                    if not os.path.isfile(filename):
                        print "Error in compYears: file "+filename+" does not exist."
                        return
                    f[l][p][c][i] = ROOT.TFile(filename)
                    if projection:
                        h2[l][p][c][i] = f[l][p][c][i].Get(histoname)
                        if var=="MVV":
                            h[l][p][c][i] = h2[l][p][c][i].Clone().ProjectionX('_px_'+lep[l]+'_'+pur[p]+'_'+cat[c]+'_'+str(i))
                        elif var=="MJJ":
                            h[l][p][c][i] = h2[l][p][c][i].Clone().ProjectionY('_py_'+lep[l]+'_'+pur[p]+'_'+cat[c]+'_'+str(i))
                    else:
                        h[l][p][c][i] = f[l][p][c][i].Get(histoname)
                    if rebin!=0:
                        print "Info in compYears: rebinning ("+str(rebin)+")"
                        h[l][p][c][i].Rebin(rebin)
                    h[l][p][c][i].Scale(1./h[l][p][c][i].Integral())

                hmax = max([h[l][p][c][i].GetMaximum() for i in range(nF)])
                if not logy:
                    h[l][p][c][0].SetMinimum(0)
                h[l][p][c][0].SetMaximum(hmax*(2. if logy else 1.1))

                color=[ROOT.kBlue-7,ROOT.kGreen-3,ROOT.kOrange-5,ROOT.kBlack]
                lgd[l][p][c]=ROOT.TLegend(0.6,0.91-2*2*nC*0.042,0.9,0.91)
                lgd[l][p][c].SetBorderSize(0)
                lgd[l][p][c].SetFillStyle(0)
                lgd[l][p][c].SetTextFont(42)
                lgd[l][p][c].SetTextSize(0.036)

                for i in range(nF):
                    h[l][p][c][i].GetXaxis().SetTitle(xaxistitle)
                    h[l][p][c][i].GetYaxis().SetTitle("integral normalized to 1")
                    h[l][p][c][i].UseCurrentStyle()
                    h[l][p][c][i].SetStats(0)
                    h[l][p][c][i].SetLineColor(color[i])
                    lgd[l][p][c].AddEntry(h[l][p][c][i],lep[l]+", "+pur[p]+", "+cat[c]+", "+legends[i],"l")
                    h[l][p][c][i].Draw("hist,same")

                lgd[l][p][c].Draw()
                saveCanvas(ca[l][p][c],outDir+"/"+outputprefix+"_"+lep[l]+"_"+pur[p]+"_"+cat[c]+"_"+var+("_log" if logy else ""))


def makeSignalParamFromHisto(filename,outputname,var,signal,mxpoints):
    if not os.path.isfile(filename):
        print "Error in compMXpoints: file "+filename+" does not exist."
        return
    f = ROOT.TFile(filename)

    color=colorGradientSignal[signal]

    c1=ROOT.TCanvas("c")
    c1.cd()
    
    masses = mxpoints.split(",")
    nM = len(masses)
    h2 = np.zeros(nM,dtype=object)
    h = np.zeros(nM,dtype=object)
    hmaxmax = 0.
    for m in range(nM):
        if not f.GetListOfKeys().Contains(signal+masses[m]):
            print 'Warning in makeSignalParamFromHisto: did not find histo', signal+masses[m]
            continue
        h2[m] = f.Get(signal+masses[m])
        if var=="MVV":
            h[m] = h2[m].Clone().ProjectionX('_px_'+masses[m])
        elif var=="MJJ":
            h[m] = h2[m].Clone().ProjectionY('_py_'+masses[m])
        h[m].Scale(1./h[m].Integral())
        hmax = h[m].GetMaximum()
        if hmax>hmaxmax:
            hmaxmax = hmax
    h[0].SetMinimum(0)
    h[0].SetMaximum(1.1*hmaxmax)

    for m in range(nM):
        if not f.GetListOfKeys().Contains(signal+masses[m]):
            continue
        #h[m].GetXaxis().SetTitle(xaxistitle)
        h[m].GetYaxis().SetTitle("a.u.")
        h[m].UseCurrentStyle()
        h[m].SetStats(0)
        h[m].SetLineColor(ROOT.TColor.GetColor(color[m]))
        h[m].Draw("hist,same")

    saveCanvas(c1,outDir+"/"+outputname)



def makeSignalParamFromDC(DCfilename,pdfname,outputname,signal,mxpoints,var,xaxistitle):
    color=colorGradientSignal[signal]
    ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
    F=ROOT.TFile(DCfilename)
    w=F.Get('w')
    frame=w.var(var).frame()
    masses = mxpoints.split(",")
    for m in range(len(masses)):
        w.var("MH").setVal(int(masses[m]))
        w.pdf(pdfname).plotOn(frame,ROOT.RooFit.LineColor(ROOT.TColor.GetColor(color[m])))
    frame.GetXaxis().SetTitle(xaxistitle)
    frame.GetYaxis().SetTitle("a.u.")
    frame.GetYaxis().SetTitleOffset(1.35)
    frame.SetTitle('')
    c1=ROOT.TCanvas("c")
    c1.cd()
    frame.Draw()
    c1.Update()
    saveCanvas(c1,outDir+"/"+outputname)


 
def slopeVsMjet(fileprefix,graphname,lep,pur,cat,outputprefix):
    c1=ROOT.TCanvas("c")
    c1.cd()

    nP=len(pur)
    nC=len(cat)
    f = np.zeros((2,nP,nC),dtype=object)
    g = np.zeros((2,nP,nC),dtype=object)

    for l in range(2):
        for p in range(nP):
            for c in range(nC):
                filename = fileprefix+"_"+lep[l]+"_"+pur[p]+"_"+cat[c]+".root" 
                if not os.path.isfile(filename):
                    print "Error in slopeVsMjet: file "+filename+" does not exist."
                    return
                f[l][p][c] = ROOT.TFile(filename)
                g[l][p][c] = f[l][p][c].Get(graphname)

    lepColor=[ROOT.kBlue,ROOT.kRed]
    purHue=[-9,+2]
    catStyle=[1,3]
    lgd=ROOT.TLegend(0.6,0.91-2*2*nC*0.042,0.9,0.91)
    lgd.SetBorderSize(0)
    lgd.SetFillStyle(0)
    lgd.SetTextFont(42)
    lgd.SetTextSize(0.036)

    for l in range(2):
        for p in range(nP):
            for c in range(nC):
                g[l][p][c].GetXaxis().SetTitle("m_{jet} (GeV)")
                g[l][p][c].UseCurrentStyle()
                g[l][p][c].SetLineColor(lepColor[l]+purHue[p])
                g[l][p][c].SetLineStyle(catStyle[c])
                g[l][p][c].SetMarkerColor(lepColor[l]+purHue[p])
                g[l][p][c].SetMarkerStyle(1)
                g[l][p][c].Draw(("ALP","LPSAME")[l+p+c!=0])
                g[l][p][c].GetXaxis().SetRangeUser(minMJJ,maxMJJ)
                g[l][p][c].GetYaxis().SetRangeUser(-0.008,-0.002)
                lgd.AddEntry(g[l][p][c],lep[l]+", "+pur[p]+", "+cat[c],"l")

    lgd.Draw()
    saveCanvas(c1,outDir+"/"+outputprefix)


 

def makeSignalShapeParam(files,sigs,var,region,outputPrefix):

    n=len(sigs)
    f=[None]*n
    g=[None]*n
    func=[None]*n    
    for j in range(n):
        if not os.path.isfile(files[j]):
            print "Error in makeSignalYieldParam: file "+files[j]+" does not exist."
            return
        f[j] = ROOT.TFile(files[j])

    paramsMJJ = [
        ("mean",  "#mu (GeV)",    70,  130, ),
        ("sigma", "#sigma (GeV)", 0,   18,  ),
        ("alpha", "#alpha",       0,   3,   ),
        ("alpha2","#alpha2",      0,   12,   ),
        ("slope", "slope",        -0.1,0.05,),
        ("f",     "f",            0,   1.5, ),
        ]
    paramsMVV = [
        ("MEAN",  "#mu (GeV)",    700, 4500,),
        ("SIGMA", "#sigma (GeV)", 0,   400, ),
        ("ALPHA1","#alpha",       0,   3,   ),
        ("ALPHA2","#alpha2",      0,   3,   ),
        ("MEAN_0",  "#mu_{0} (GeV)",    700, 4500,),#
        ("MEAN_1",  "#mu_{1} (GeV)",    -1,  1,   ),#
        ("SIGMA_0", "#sigma_{0} (GeV)", 0,   400, ),#
        ("SIGMA_1", "#sigma_{1} (GeV)", -1,  1,   ),#
        ]
    params = []
    if var=='MJJ':
        params = paramsMJJ
    elif var=='MVV':
        params = paramsMVV

    for i in range(len(params)):
        name = params[i][0]
        if not f[0].GetListOfKeys().Contains(name):
            continue

        c=ROOT.TCanvas("c_"+name)
        c.cd()
        frame=c.DrawFrame(minmx,params[i][2],maxmx,params[i][3])
        frame.GetXaxis().SetTitle("m_{X} (GeV)")
        frame.GetYaxis().SetTitle(params[i][1])
        l=ROOT.TLegend(0.6,0.2,0.9,0.34)
        l.SetBorderSize(0)
        l.SetFillStyle(0)

        notfound=False
        for j in range(n):
            g[j]=f[j].Get(name)
            g[j].SetName(name+str(j))
            g[j].SetMarkerColor(colorSignal[sigs[j]])
            g[j].SetMarkerStyle(markerSignal[sigs[j]])
            g[j].SetMarkerSize(0.8)
            g[j].SetLineColor(colorSignal[sigs[j]])
            g[j].Draw("Psame")
            func[j]=f[j].Get(name+"_func")
            func[j].SetLineColor(colorSignal[sigs[j]])
            func[j].Draw("lsame")
            l.AddEntry(g[j],legendSignal[sigs[j]],"p")
            if name=="mean" and "XWW" in sigs[j]:
                N=g[j].GetN()
                Y=g[j].GetY()
                Y.SetSize(N); 
                Y=np.array(Y,copy=True)
                print region, sigs[j], np.mean(Y)

        l.Draw()
        cmslabel_sim(c,YEAR,11)
        saveCanvas(c,outDir+"/"+outputPrefix+var+"_"+region+"_"+name)


def makeSignalYieldParam(files,sigs,outputname):

    n=len(sigs)
    f=[None]*n
    g=[None]*n
    func=[None]*n    

    c=ROOT.TCanvas("c")
    c.cd()
    l=ROOT.TLegend(0.6,0.2,0.9,0.34)
    l.SetBorderSize(0)
    l.SetFillStyle(0)

    maxy=0.
    for j in range(n):

        if not os.path.isfile(files[j]):
            print "Error in makeSignalYieldParam: file "+files[j]+" does not exist."
            return
        f[j] = ROOT.TFile(files[j])

        g[j]=f[j].Get('yield')
        g[j].Draw(("A" if j==0 else "")+"Psame")
        g[j].UseCurrentStyle()
        g[j].SetMarkerColor(colorSignal[sigs[j]])
        g[j].SetMarkerStyle(markerSignal[sigs[j]])
        g[j].SetMarkerSize(0.8)
        g[j].GetXaxis().SetTitle("m_{X} (GeV)")
        g[j].GetYaxis().SetTitle("expected yield")

        func[j]=g[j].GetFunction("func")
        func[j].SetLineColor(colorSignal[sigs[j]])

        l.AddEntry(g[j],legendSignal[sigs[j]],"p")

        maxtemp=g[j].GetHistogram().GetMaximum()
        if maxtemp>maxy: maxy=maxtemp

    g[0].GetXaxis().SetRangeUser(minmx,maxmx)
    g[0].GetYaxis().SetRangeUser(0.,1.3*maxy)
    l.Draw()
    cmslabel_sim(c,YEAR,11)
    saveCanvas(c,outDir+'/'+outputname)


def makeSignalYieldParam_unc(fileNo,fileUp,fileDn,outputname,ratio=1):

    if not os.path.isfile(fileNo):
        print "Error in makeSignalYieldParam: file "+fileNo+" does not exist."
        return
    if not os.path.isfile(fileUp):
        print "Error in makeSignalYieldParam: file "+fileUp+" does not exist."
        return
    if not os.path.isfile(fileDn):
        print "Error in makeSignalYieldParam: file "+fileDn+" does not exist."
        return

    contribs = []
    contribs.append((fileNo, ROOT.kBlack, 20, "nominal",))
    contribs.append((fileUp, colorUp,     21, "bb tag SF up",))
    contribs.append((fileDn, colorDn,     22, "bb tag SF down",))
    n=len(contribs)

    f=[None]*n
    g=[None]*n
    func=[None]*n    
    for j in range(n):
        f[j] = ROOT.TFile(contribs[j][0])

    c=ROOT.TCanvas("c")
    c.cd()
    l=ROOT.TLegend(0.6,0.2,0.9,0.34)
    l.SetBorderSize(0)
    l.SetFillStyle(0)

    if ratio: ## just the ratio to nominal
        gNominal=f[0].Get('yield')
        N=gNominal.GetN()
        X=gNominal.GetX(); X.SetSize(N); X=array('d',X)
        Yn=gNominal.GetY(); Yn.SetSize(N); Yn=array('d',Yn)
        EXn=gNominal.GetEX(); EXn.SetSize(N); EXn=array('d',EXn)
        for j in range(n):
            gShifted=f[j].Get('yield')
            Ys=gShifted.GetY(); Ys.SetSize(N); Ys=array('d',Ys)
            EYs=gShifted.GetEY(); EYs.SetSize(N); EYs=array('d',EYs)
            Yr = array('d',[sh/no for sh,no in zip(Ys,Yn)])
            EYr = array('d',[sh/no for sh,no in zip(EYs,Yn)])
            g[j]=ROOT.TGraphErrors(N,X,Yr,EXn,EYr)
            g[j].Draw(("A" if j==0 else "")+"Psame")
            g[j].UseCurrentStyle()
            g[j].SetMarkerColor(contribs[j][1])
            g[j].SetMarkerStyle(contribs[j][2])
            g[j].SetMarkerSize(0.8)
            g[j].GetXaxis().SetTitle("m_{X} (GeV)")
            g[j].GetYaxis().SetTitle("ratio to nominal yield")
            l.AddEntry(g[j],contribs[j][3],"p")
            ## print the scale factors
            if j>0:
                print contribs[j][0], np.mean(np.frombuffer(Yr))

        g[0].GetXaxis().SetRangeUser(minmx,maxmx)
        g[0].GetYaxis().SetRangeUser(0.8,1.2)

    else: ## draw the 3 curves
        maxy=0.
        for j in range(n):
            g[j]=f[j].Get('yield')
            g[j].Draw(("A" if j==0 else "")+"Psame")
            g[j].UseCurrentStyle()
            g[j].SetMarkerColor(contribs[j][1])
            g[j].SetMarkerStyle(contribs[j][2])
            g[j].SetMarkerSize(0.8)
            g[j].GetXaxis().SetTitle("m_{X} (GeV)")
            g[j].GetYaxis().SetTitle("expected yield")
            func[j]=g[j].GetFunction("func")
            func[j].SetLineColor(contribs[j][1])
            l.AddEntry(g[j],contribs[j][3],"p")
            maxtemp=g[j].GetHistogram().GetMaximum()
            if maxtemp>maxy: maxy=maxtemp
        g[0].GetXaxis().SetRangeUser(minmx,maxmx)
        g[0].GetYaxis().SetRangeUser(0.,1.3*maxy)

    l.Draw()
    cmslabel_sim(c,YEAR,11)
    saveCanvas(c,outDir+'/'+outputname)



def makeResWTopMergedMJJShapeParam(fileResW,region,outputPrefix):

    peaks = [
        (ROOT.kOrange+2,  20, "merged W",),
        (ROOT.kGreen+1,   21, "merged top",),
        ]
    f = ROOT.TFile(fileResW)
    g=[None]*2
    func=[None]*2

    paramsPerPeak = [
        ("mean",  "meanW",  "meanTop",  "#mu (GeV)",    50,  250, ),
        ("sigma", "sigmaW", "sigmaTop", "#sigma (GeV)", 0,   50,  ),
        ("alpha", "alphaW", "alphaTop", "#alpha",       0,   5,   ),
        ("alpha2","alphaW2","alphaTop2","#alpha2",      0,   5,   ),
        ]
    paramsCommon = [
        ("n",     "n",            0,   10., ),
        ("f",     "f",            0,   1.5, ),
        ("f2",    "f2",           0,   1.5, ),
        ("slope", "slope",       -0.05,0.05,),
        ]

    for i in range(4):
        name = paramsPerPeak[i][0]
        c=ROOT.TCanvas("c_"+name)
        c.cd()
        frame=c.DrawFrame(minMVV,paramsPerPeak[i][4],maxMVV,paramsPerPeak[i][5])
        frame.GetXaxis().SetTitle("m_{WV} (GeV)")
        frame.GetYaxis().SetTitle(paramsPerPeak[i][3])
        l=ROOT.TLegend(0.6,0.75,0.9,0.85)
        l.SetBorderSize(0)
        l.SetFillStyle(0)
        for j in range(2):
            g[j]=f.Get(paramsPerPeak[i][1+j])
            g[j].SetName(name+str(j))
            g[j].SetMarkerColor(peaks[j][0])
            g[j].SetMarkerStyle(peaks[j][1])
            g[j].SetMarkerSize(0.8)
            g[j].SetLineColor(peaks[j][0])
            g[j].Draw("Psame")
            func[j]=f.Get(paramsPerPeak[i][1+j]+"_func")
            func[j].SetLineColor(peaks[j][0])
            func[j].Draw("lsame")
            l.AddEntry(g[j],peaks[j][2],"p")
        l.Draw()
        cmslabel_sim(c,YEAR,11)
        saveCanvas(c,outDir+"/"+outputPrefix+region+"_"+name)

    for i in range(4):
        name = paramsCommon[i][0]
        c=ROOT.TCanvas("c_"+name)
        c.cd()
        frame=c.DrawFrame(minMVV,paramsCommon[i][2],maxMVV,paramsCommon[i][3])
        frame.GetXaxis().SetTitle("m_{WV} (GeV)")
        frame.GetYaxis().SetTitle(paramsCommon[i][1])
        color=ROOT.kBlue+1
        gc=f.Get(paramsCommon[i][0])
        gc.SetName(name)
        gc.SetMarkerColor(color)
        gc.SetMarkerStyle(20)
        gc.SetMarkerSize(0.8)
        gc.SetLineColor(color)
        gc.Draw("Psame")
        funcc=f.Get(name+"_func")
        funcc.SetLineColor(color)
        funcc.Draw("lsame")
        cmslabel_sim(c,YEAR,11)
        saveCanvas(c,outDir+"/"+outputPrefix+region+"_"+name)



def makeResWResTopMJJShapeParam(fileResW,fileResTop,region,outputPrefix):

    peaks = [
        (ROOT.kOrange+2,  20, "W",),
        (ROOT.kGreen+1,   21, "top",),
        ]
    f = [ROOT.TFile(fileResW),ROOT.TFile(fileResTop)]
    g=[None]*2
    func=[None]*2

    paramsPerPeak = [
        ("mean",  "mean",   "#mu (GeV)",    50,  250, ),
        ("sigma", "sigma",  "#sigma (GeV)", 0,   50,  ),
        ("alpha", "alpha",  "#alpha",       0,   5,   ),
        ("alpha2","alpha2", "#alpha2",      0,   5,   ),
        ("n",     "n",      "n",            0,   10., ),
        ("n2",    "n2",     "n2",           0,   10., ),
        ]

    for i in range(6):
        name = paramsPerPeak[i][0]
        c=ROOT.TCanvas("c_"+name)
        c.cd()
        frame=c.DrawFrame(minMVV,paramsPerPeak[i][3],maxMVV,paramsPerPeak[i][4])
        frame.GetXaxis().SetTitle("m_{WV} (GeV)")
        frame.GetYaxis().SetTitle(paramsPerPeak[i][2])
        l=ROOT.TLegend(0.6,0.75,0.9,0.85)
        l.SetBorderSize(0)
        l.SetFillStyle(0)
        for j in range(2):
            g[j]=f[j].Get(paramsPerPeak[i][1])
            g[j].SetName(name+str(j))
            g[j].SetMarkerColor(peaks[j][0])
            g[j].SetMarkerStyle(peaks[j][1])
            g[j].SetMarkerSize(0.8)
            g[j].SetLineColor(peaks[j][0])
            g[j].Draw("Psame")
            func[j]=f[j].Get(paramsPerPeak[i][1]+"_func")
            func[j].SetLineColor(peaks[j][0])
            func[j].Draw("lsame")
            l.AddEntry(g[j],peaks[j][2],"p")
        l.Draw()
        cmslabel_sim(c,YEAR,11)
        saveCanvas(c,outDir+"/"+outputPrefix+region+"_"+name)



def makeGOF(filename,val):
    f=ROOT.TFile(filename)
    t=f.Get("limit")
    c=ROOT.TCanvas("c","c")
    c.cd()
    t.Draw("limit>>h")
    h=ROOT.gOutDir.Get("h")
    h.SetLineWidth(2)
    h.SetLineColor(ROOT.kBlack)
    h.SetFillColor(ROOT.kOrange+1)
    h.Draw()
    l=ROOT.TArrow(val,0.8*h.GetMaximum(),val,0)
    l.Draw()
    h.GetXaxis().SetTitle("G.O.F. estimator")
    h.GetYaxis().SetTitle("toys")
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    c.Update()
    c.SaveAs("GOF.root")   


def makeBias():

    import numpy
    def median(lst):
        return numpy.median(numpy.array(lst))

    def getBias(filename,rValue):
        f=ROOT.TFile(filename)
        tree=f.Get("tree_fit_sb")
        bias=[]
        for event in tree:
            if event.muErr==0.0:
                continue
            b = (event.mu-rValue)/event.muErr
            if abs(event.mu-rValue)/event.muErr>0.45:
                continue
            bias.append(b)
        return  median(bias)   

    def makePull(filename,rValue):
        f=ROOT.TFile(filename)
        tree=f.Get("tree_fit_sb")
        bias=[]
        h=ROOT.TH1F("pull","pull",10,-5,5)
        h.Sumw2()
        for event in tree:
            if event.muErr==0.0:
                continue
            b = (event.mu-rValue)/event.muErr
            h.Fill(b)        
        c=ROOT.TCanvas("pull","pull")
        c.cd()
        h.Draw()
        h.GetXaxis().SetTitle("pull")
        h.GetYaxis().SetTitle("toys")
        h.Fit("gaus")
        ROOT.gStyle.SetOptFit(111111)
        c.SaveAs("pull_"+filename)
        c.SaveAs(("pull_"+filename).replace("root","png"))
        c.SaveAs(("pull_"+filename).replace("root","pdf"))
        
    rValue={1000:{'r':0.04,'2r':0.08,'r_freq':0.04,'2r_freq':0.08},\
            1500:{'r':0.01,'2r':0.02,'r_freq':0.01,'2r_freq':0.02},\
            2000:{'r':5e-3,'2r':0.01,'r_freq':5e-3,'2r_freq':0.01},\
            2500:{'r':3e-3,'2r':6e-3,'r_freq':3e-3,'2r_freq':6e-3},\
            3000:{'r':2e-3,'2r':4e-3,'r_freq':2e-3,'2r_freq':4e-3},\
            4000:{'r':7e-4,'2r':1.4e-3,'r_freq':7e-4,'2r_freq':1.4e-3}}
   

    graphs={}
    for graphName in ['r','2r','r_freq','2r_freq']: 
        graphs[graphName] = ROOT.TGraph()
        graphs[graphName].SetName("graph_"+graphName)
        g = graphs[graphName]
        for i,mass in enumerate([1000,1500,2000,2500,3000,4000]):
            bias = getBias("biasTests_"+str(mass)+"_"+graphName+".root",rValue[mass][graphName])
            makePull("biasTests_"+str(mass)+"_"+graphName+".root",rValue[mass][graphName])
            g.SetPoint(i,mass,bias)
            
    c=ROOT.TCanvas("c")
    graphs['r'].Draw("ALP")
    graphs['r'].GetXaxis().SetTitle("injected mass (GeV)")
    graphs['r'].GetYaxis().SetTitle("median pull")
    
    graphs['r'].GetYaxis().SetRangeUser(-0.05,0.05)
    graphs['r'].SetLineColor(ROOT.kRed)
    graphs['r'].SetMarkerColor(ROOT.kRed)
    graphs['r'].SetLineWidth(3)
    graphs['r'].SetMarkerStyle(20)

    graphs['2r'].Draw("PLsame")
    graphs['2r'].SetLineColor(ROOT.kBlue)
    graphs['2r'].SetMarkerColor(ROOT.kBlue)
    graphs['2r'].SetLineWidth(3)
    graphs['2r'].SetMarkerStyle(20)


    l=ROOT.TLegend(0.5,0.55,0.9,0.85)
    l.AddEntry(graphs['r'],"r=excluded (pre-fit toys)","lp")
    l.AddEntry(graphs['2r'],"r=2excluded (pre-fit toys)","lp")
    l.AddEntry(graphs['r_freq'],"r=excluded (post-fit toys)","lp")
    l.AddEntry(graphs['2r_freq'],"r=2excluded (post-fit toys)","lp")
    l.Draw()
    l.SetBorderSize(0)
    graphs['r_freq'].Draw("PLsame")
    graphs['r_freq'].SetLineColor(ROOT.kRed)
    graphs['r_freq'].SetMarkerColor(ROOT.kRed)
    graphs['r_freq'].SetLineWidth(3)
    graphs['r_freq'].SetLineStyle(3)
    graphs['r_freq'].SetMarkerStyle(20)

    graphs['2r_freq'].Draw("PLsame")
    graphs['2r_freq'].SetLineColor(ROOT.kBlue)
    graphs['2r_freq'].SetMarkerColor(ROOT.kBlue)
    graphs['2r_freq'].SetLineWidth(3)
    graphs['2r_freq'].SetLineStyle(3)
    graphs['2r_freq'].SetMarkerStyle(20)

    c.SaveAs("plots16/biasTests.root")
    c.SaveAs("plots16/biasTests.pdf")



def makeKernelScaleResolution(filename,histoname,outputPrefix):
    #ROOT.gStyle.SetOptTitle(0)
    #ROOT.gStyle.SetOptStat(0)

    setTDRStyle()
    style=gROOT.GetStyle("tdrStyle").Clone()
    style.SetPadLeftMargin(0.14)
    style.SetPadRightMargin(0.04)
    style.cd() 

    f=ROOT.TFile(filename)
    histo=f.Get(histoname)
    suffix=""
    if "scalex" in histoname:
        histo.GetYaxis().SetTitle("m_{WV} scale")
        suffix="scale_MVV"
    if "scaley" in histoname:
        histo.GetYaxis().SetTitle("m_{jet} scale")
        suffix="scale_MJJ"
    if "resx" in histoname:
        histo.GetYaxis().SetTitle("m_{WV} resolution")
        suffix="resolution_MVV"
    if "resy" in histoname:
        histo.GetYaxis().SetTitle("m_{jet} resolution")
        suffix="resolution_MJJ"

    if histo.GetXaxis().GetTitle()=="":
        histo.GetXaxis().SetTitle("gen jet p_{T} (GeV)")
    histo.SetLineWidth(2)
    c=ROOT.TCanvas("c","c",500,500)
    histo.Draw()
    histo.GetXaxis().SetTitleOffset(1.15)
    histo.GetYaxis().SetTitleOffset(1.35)
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleSize(0.05)
    histo.GetXaxis().SetLabelSize(0.035)
    histo.GetYaxis().SetLabelSize(0.035)
    cmslabel_sim(c,YEAR,0)
    saveCanvas(c,outDir+"/detectorParam_"+outputPrefix+suffix)









os.system("mkdir -p "+outDir)

setTDRStyle()
style=gROOT.GetStyle("tdrStyle").Clone()
style.SetOptStat(0)
style.SetPadLeftMargin(0.14)
style.SetPadRightMargin(0.04)
style.SetCanvasDefH(500)
style.SetCanvasDefW(500)
style.SetTitleXOffset(1.15)
style.SetTitleYOffset(1.35)
style.SetTitleSize(0.05,"XYZ")
style.SetLabelSize(0.03,"Z")
style.cd()






if 'nonResTpl' in plots:
    #'''
    compCategories(inDir+"LNuJJ_nonRes_2D","histo",True,leptons,purities,categories,"compTemplate_nonRes","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_nonRes_2D","histo",True,leptons,purities,categories,"compTemplate_nonRes","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_nonRes_2D","histo",True,leptons,purities,categories,"compTemplate_nonRes","MJJ","m_{jet} (GeV)")
    compCategories(inDir+"LNuJJ_norm","nonRes",True,leptons,purities,categories,"compReco_nonRes","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_norm","nonRes",True,leptons,purities,categories,"compReco_nonRes","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_norm","nonRes",True,leptons,purities,categories,"compReco_nonRes","MJJ","m_{jet} (GeV)")

    if COMPYEARS:
        compYears([inDir16+"LNuJJ_nonRes_2D",inDir17+"LNuJJ_nonRes_2D",inDir18+"LNuJJ_nonRes_2D",inDirR2+"LNuJJ_nonRes_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_nonRes","MVV","m_{WV} (GeV)",False)
        compYears([inDir16+"LNuJJ_nonRes_2D",inDir17+"LNuJJ_nonRes_2D",inDir18+"LNuJJ_nonRes_2D",inDirR2+"LNuJJ_nonRes_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_nonRes","MVV","m_{WV} (GeV)",True)
        compYears([inDir16+"LNuJJ_nonRes_2D",inDir17+"LNuJJ_nonRes_2D",inDir18+"LNuJJ_nonRes_2D",inDirR2+"LNuJJ_nonRes_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_nonRes","MJJ","m_{jet} (GeV)")
    #'''
    #slopeVsMjet(inDir+"LNuJJ_nonRes_COND2D","gr_tailSlopeVsMjet_histo",leptons,purities,categories,"nonRes_tailSlopeVsMjet")

    #'''
    for c in categories:
        for p in purities:
            for l in leptons:
                #continue
                
                #'''
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B}".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c]))
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -r 0".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##without the ranges
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -d 1".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test coarse intermediary template
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -D 1".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test conditional template
                #'''

                #'''
                makeTemplate2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","histo","template_nonRes_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_nonRes_COND2D_"+l+"_"+p+"_"+c+".root","histo","templCond_nonRes_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_nonRes_COND2D_"+l+"_"+p+"_"+c+".root","histo_coarse","template_nonResCoarse_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_nonRes_COND2D_"+l+"_"+p+"_"+c+".root","histo_coarsesmoothed","template_nonResCoarseSmoothed_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_nonRes_"+p+"_"+c+"_COND2D.root","histo","templCond_nonRes_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_nonRes_"+p+"_"+c+"_COND2D.root","histo_coarse","template_nonResCoarse_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_nonRes_"+p+"_"+c+"_COND2D.root","histo_coarsesmoothed","template_nonResCoarseSmoothed_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root","nonRes","reco_nonRes_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_"+l+"_"+p+"_"+c+"_GEN.root","nonRes","gen_nonRes_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_GEN.root","nonRes_"+p+"_"+c,"gen_nonRes_"+l+"_"+p+"_"+c)
                makeTemplateVsReco2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root","nonRes","templateVsReco_nonRes_"+l+"_"+p+"_"+c) #,4,(5,0)[binsMJJ[c]==18])
                makeTemplateVsReco1D(inDir+"LNuJJ_nonRes_MJJ_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root","nonRes_wgtMJJ","templateVsReco1D_nonRes_MJ_"+l+"_"+p+"_"+c,"MJJ","m_{jet} (GeV)")
                #'''
                ##makeTemplateVsReco2D(inDir+"LNuJJ_nonRes_COND2D_"+l+"_"+p+"_"+c+".root","histo_coarse",inDir+"LNuJJ_"+l+"_"+p+"_"+c+".root","nonRes","templateVsReco_nonResCoarse_"+l+"_"+p+"_"+c)
                #makeTemplateVsReco1D(inDir+"LNuJJ_nonRes_MVV_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_"+l+"_"+p+"_"+c+".root","nonRes","templateVsReco1D_nonRes_MVV_"+l+"_"+p+"_"+c,"MVV","m_{WV} (GeV)")

if 'nonResSys' in plots:
    for c in categories:
        for p in purities:
            for l in leptons:
                #continue

                '''
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"PTX")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"OPTX")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"PTY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"OPTY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPTBoth")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPT2Both")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPTX")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPT2X")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"SDY")

                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"PTX")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"OPTX")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"PTY")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"OPTY")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPTBoth")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPT2Both")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPTX")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"GPT2X")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"SDY")
                #'''

                #'''
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"logWeight")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"MJJScale")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"SD")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"PTY")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"OPTY")

                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"logWeight")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"MJJScale")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"SD")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"PTY")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_2D_"+l+"_"+p+"_"+c+".root","systs_nonRes_"+l+"_"+p+"_"+c,"OPTY")
                #'''


if 'CRNonResTpl' in plots:
    #'''
    compCategories(inDir+"LNuJJ_nonRes_CR_2D","histo",True,leptons,purities,categories,"compTemplate_CRnonRes","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_nonRes_CR_2D","histo",True,leptons,purities,categories,"compTemplate_CRnonRes","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_nonRes_CR_2D","histo",True,leptons,purities,categories,"compTemplate_CRnonRes","MJJ","m_{jet} (GeV)")
    compCategories(inDir+"LNuJJ_norm_CR","nonRes_CR",True,leptons,purities,categories,"compReco_CRnonRes","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_norm_CR","nonRes_CR",True,leptons,purities,categories,"compReco_CRnonRes","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_norm_CR","nonRes_CR",True,leptons,purities,categories,"compReco_CRnonRes","MJJ","m_{jet} (GeV)")

    if COMPYEARS:
        compYears([inDir16+"LNuJJ_nonRes_CR_2D",inDir17+"LNuJJ_nonRes_CR_2D",inDir18+"LNuJJ_nonRes_CR_2D",inDirR2+"LNuJJ_nonRes_CR_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_CRnonRes","MVV","m_{WV} (GeV)",False)
        compYears([inDir16+"LNuJJ_nonRes_CR_2D",inDir17+"LNuJJ_nonRes_CR_2D",inDir18+"LNuJJ_nonRes_CR_2D",inDirR2+"LNuJJ_nonRes_CR_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_CRnonRes","MVV","m_{WV} (GeV)",True)
        compYears([inDir16+"LNuJJ_nonRes_CR_2D",inDir17+"LNuJJ_nonRes_CR_2D",inDir18+"LNuJJ_nonRes_CR_2D",inDirR2+"LNuJJ_nonRes_CR_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_CRnonRes","MJJ","m_{jet} (GeV)")
    #'''

    #'''
    for c in categories:
        for p in purities:
            for l in leptons:
                #continue
                
                #'''
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c]))
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R -r 0".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##without the ranges
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R -d 1".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test coarse intermediary template
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R -D 1".format(i=inDir, o=outDir, C='nonRes', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test conditional template
                #'''

                #'''
                makeTemplate2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","histo","template_CRnonRes_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_nonRes_CR_COND2D_"+l+"_"+p+"_"+c+".root","histo","templCond_CRnonRes_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_nonRes_CR_COND2D_"+l+"_"+p+"_"+c+".root","histo_coarse","template_CRnonResCoarse_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_nonRes_CR_COND2D_"+l+"_"+p+"_"+c+".root","histo_coarsesmoothed","template_CRnonResCoarseSmoothed_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_nonRes_CR_"+p+"_"+c+"_COND2D.root","histo","templCond_CRnonRes_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_nonRes_CR_"+p+"_"+c+"_COND2D.root","histo_coarse","template_CRnonResCoarse_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_nonRes_CR_"+p+"_"+c+"_COND2D.root","histo_coarsesmoothed","template_CRnonResCoarseSmoothed_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_norm_CR_"+l+"_"+p+"_"+c+".root","nonRes_CR","reco_CRnonRes_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_"+l+"_"+p+"_"+c+"_GEN.root","nonRes_CR","gen_CRnonRes_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_GEN.root","nonRes_CR_"+p+"_"+c,"gen_CRnonRes_"+l+"_"+p+"_"+c)
                makeTemplateVsReco2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_CR_"+l+"_"+p+"_"+c+".root","nonRes_CR","templateVsReco_CRnonRes_"+l+"_"+p+"_"+c) #,4,(5,0)[binsMJJ[c]==18])
                makeTemplateVsReco1D(inDir+"LNuJJ_nonRes_CR_MJJ_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_CR_"+l+"_"+p+"_"+c+".root","nonRes_CR_wgtMJJ","templateVsReco1D_CRnonRes_MJ_"+l+"_"+p+"_"+c,"MJJ","m_{jet} (GeV)")
                #'''

if 'CRNonResSys' in plots:
    for c in categories:
        for p in purities:
            for l in leptons:
                #continue

                '''
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"PTX")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"OPTX")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"PTY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"OPTY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPTBoth")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPT2Both")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPTX")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPT2X")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"SDY")

                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"PTX")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"OPTX")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"PTY")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"OPTY")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPTBoth")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPT2Both")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPTX")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"GPT2X")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"SDY")
                #'''

                #'''
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"logWeight")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"MJJScale")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"SD")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"PTY")
                #makeShapeUncertaintiesProj2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"OPTY")

                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"logWeight")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"MJJScale")
                makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"SD")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"PTY")
                #makeShapeUncertainties2D(inDir+"LNuJJ_nonRes_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRnonRes_"+l+"_"+p+"_"+c,"OPTY")
                #'''



if 'resTpl' in plots:

    #'''
    compCategories(inDir+"LNuJJ_res_2D","histo",True,leptons,purities,categories,"compTemplate_res","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_res_2D","histo",True,leptons,purities,categories,"compTemplate_res","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_res_2D","histo",True,leptons,purities,categories,"compTemplate_res","MJJ","m_{jet} (GeV)")
    compCategories(inDir+"LNuJJ_norm","res",True,leptons,purities,categories,"compReco_res","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_norm","res",True,leptons,purities,categories,"compReco_res","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_norm","res",True,leptons,purities,categories,"compReco_res","MJJ","m_{jet} (GeV)")

    if COMPYEARS:
        compYears([inDir16+"LNuJJ_res_2D",inDir17+"LNuJJ_res_2D",inDir18+"LNuJJ_res_2D",inDirR2+"LNuJJ_res_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_res","MVV","m_{WV} (GeV)",False)
        compYears([inDir16+"LNuJJ_res_2D",inDir17+"LNuJJ_res_2D",inDir18+"LNuJJ_res_2D",inDirR2+"LNuJJ_res_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_res","MVV","m_{WV} (GeV)",True)
        compYears([inDir16+"LNuJJ_res_2D",inDir17+"LNuJJ_res_2D",inDir18+"LNuJJ_res_2D",inDirR2+"LNuJJ_res_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_res","MJJ","m_{jet} (GeV)")
    #'''

    #'''
    for c in categories:
        for p in purities:
            for l in leptons:
                #continue
                
                #'''
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B}".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c]))
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -r 0".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##without the ranges
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -d 1".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test coarse intermediary template
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -D 1".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test conditional template
                #'''

                #'''
                makeTemplate2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","histo","template_res_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_res_"+c+"_COND2D.root","histo","templCond_res_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_res_"+c+"_COND2D.root","histo_coarse","template_resCoarse_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_res_"+c+"_COND2D.root","histo_coarsesmoothed","template_resCoarseSmoothed_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root","res","reco_res_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_"+l+"_"+p+"_"+c+"_GEN.root","res","gen_res_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_GEN.root","res_"+c,"gen_res_"+l+"_"+p+"_"+c)
                makeTemplateVsReco2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root","res","templateVsReco_res_"+l+"_"+p+"_"+c) 
                makeTemplateVsReco1D(inDir+"LNuJJ_res_MJJ_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root","res","templateVsReco1D_res_MJ_"+l+"_"+p+"_"+c,"MJJ","m_{jet} (GeV)")
                #'''

if 'resSys' in plots:

    for c in categories:
        for p in purities:
            for l in leptons:
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"scaleY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"resY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"fractionY")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"scaleY")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"resY")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_2D_"+l+"_"+p+"_"+c+".root","systs_res_"+l+"_"+p+"_"+c,"fractionY")


if 'CRResTpl' in plots:

    #'''
    compCategories(inDir+"LNuJJ_res_CR_2D","histo",True,leptons,purities,categories,"compTemplate_CRres","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_res_CR_2D","histo",True,leptons,purities,categories,"compTemplate_CRres","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_res_CR_2D","histo",True,leptons,purities,categories,"compTemplate_CRres","MJJ","m_{jet} (GeV)")
    compCategories(inDir+"LNuJJ_norm_CR","res_CR",True,leptons,purities,categories,"compReco_CRres","MVV","m_{WV} (GeV)",False)
    compCategories(inDir+"LNuJJ_norm_CR","res_CR",True,leptons,purities,categories,"compReco_CRres","MVV","m_{WV} (GeV)",True)
    compCategories(inDir+"LNuJJ_norm_CR","res_CR",True,leptons,purities,categories,"compReco_CRres","MJJ","m_{jet} (GeV)")

    if COMPYEARS:
        compYears([inDir16+"LNuJJ_res_CR_2D",inDir17+"LNuJJ_res_CR_2D",inDir18+"LNuJJ_res_CR_2D",inDirR2+"LNuJJ_res_CR_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_CRres","MVV","m_{WV} (GeV)",False)
        compYears([inDir16+"LNuJJ_res_CR_2D",inDir17+"LNuJJ_res_CR_2D",inDir18+"LNuJJ_res_CR_2D",inDirR2+"LNuJJ_res_CR_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_CRres","MVV","m_{WV} (GeV)",True)
        compYears([inDir16+"LNuJJ_res_CR_2D",inDir17+"LNuJJ_res_CR_2D",inDir18+"LNuJJ_res_CR_2D",inDirR2+"LNuJJ_res_CR_2D"],["2016","2017","2018","merged"],"histo",True,leptons,purities,categories,"compYears_CRres","MJJ","m_{jet} (GeV)")
    #'''

    #'''
    for c in categories:
        for p in purities:
            for l in leptons:
                #continue
                
                #'''
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c]))
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R -r 0".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##without the ranges
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R -d 1".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test coarse intermediary template
                os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -R -D 1".format(i=inDir, o=outDir, C='res', l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c])) ##to test conditional template
                #'''

                #'''
                makeTemplate2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","histo","template_CRres_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_res_CR_"+c+"_COND2D.root","histo","templCond_CRres_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_res_CR_"+c+"_COND2D.root","histo_coarse","template_CRresCoarse_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_res_CR_"+c+"_COND2D.root","histo_coarsesmoothed","template_CRresCoarseSmoothed_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_norm_CR_"+l+"_"+p+"_"+c+".root","res_CR","reco_CRres_"+l+"_"+p+"_"+c)
                #makeTemplate2D(inDir+"LNuJJ_"+l+"_"+p+"_"+c+"_GEN.root","res","gen_CRres_"+l+"_"+p+"_"+c)
                makeTemplate2D(inDir+"LNuJJ_GEN.root","res_"+c,"gen_CRres_"+l+"_"+p+"_"+c)
                makeTemplateVsReco2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_CR_"+l+"_"+p+"_"+c+".root","res_CR","templateVsReco_CRres_"+l+"_"+p+"_"+c) 
                makeTemplateVsReco1D(inDir+"LNuJJ_res_CR_MJJ_"+l+"_"+p+"_"+c+".root","histo",inDir+"LNuJJ_norm_CR_"+l+"_"+p+"_"+c+".root","res_CR","templateVsReco1D_CRres_MJ_"+l+"_"+p+"_"+c,"MJJ","m_{jet} (GeV)")
                #'''

if 'CRResSys' in plots:

    for c in categories:
        for p in purities:
            for l in leptons:
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"scaleY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"resY")
                makeShapeUncertaintiesProj2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"fractionY")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"MVVScale")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"Diag")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"scaleY")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"resY")
                makeShapeUncertainties2D(inDir+"LNuJJ_res_CR_2D_"+l+"_"+p+"_"+c+".root","systs_CRres_"+l+"_"+p+"_"+c,"fractionY")



if 'signal' in plots:

    for c in categories:#['nobb']:#
        for p in purities:#['HP']:#
            pass
            #'''
            makeSignalShapeParam([inDir+"debugSignalShape_LNuJJ_"+s+"_MJJ_"+p+"_"+c+".root" for s in signals],signals,'MJJ',p+"_"+c,"paramSignalShape_allSig_")
            makeSignalShapeParam([inDir+"debugSignalShape_LNuJJ_"+s+"_MVV_"+p+"_"+c+".root" for s in signals],signals,'MVV',p+"_"+c,"paramSignalShape_allSig_")
            #'''

            for l in leptons:#['e']:#
                pass
                #'''
                makeSignalYieldParam([inDir+"LNuJJ_"+s+"_"+l+"_"+p+"_"+c+"_yield.root" for s in signals],signals,"paramSignalYield_allSig_"+l+"_"+p+"_"+c)
                #'''

                for signal in signals:
                    print c, p, l, signal
                    if options.withDC:
                        pass

                        '''
                        for mx in [2000]: #[1000,2000,3000,4000]: #[1000,1400,2000,3000,4500]:
                            os.system("python $CMSSW_BASE/src/CMGTools/VVResonances/interactive/makePlotsTemplateVsReco.py -i {i} -o {o} -C {C} -l {l} -p {p} -c {c} -b {b} -B {B} -r 0 -s".format(i=inDir, o=outDir, C=signal+str(mx).zfill(4), l=l, p=p, c=c, b=binsMVV[c], B=binsMJJ[c]))
                        #'''
                        '''
                        os.system("rm "+inDir+"/LNuJJ_"+signal+"_2DFromDC_"+l+"_"+p+"_"+c+".root")
                        for mx in [1000,1500,2000,2500,3000,3500,4000,4500]:
                            print mx
                            extractSignalTemplateFromDC("Dc_"+signal+"/combined_"+YEAR+".root","shapeSig_"+signal+"_"+c+"_"+l+"_"+p+"_"+YEAR,signal,mx,inDir+"LNuJJ_"+signal+"_2DFromDC_"+l+"_"+p+"_"+c,c)
                            #extractSignalTemplateFromDC("Dc_"+signal+"/combined_"+YEAR+".root",signal+"_MVV_"+c+"_"+l+"_"+p+"_"+YEAR,signal,mx,inDir+"LNuJJ_"+signal+"_MVVGivenMJJFromDC_"+l+"_"+p+"_"+c,c)
                            #extractSignalMjjPdfFromDC("Dc_"+signal+"/combined_"+YEAR+".root",signal+"_MJJ_"+c+"_"+l+"_"+p+"_"+YEAR,signal,mx,inDir+"LNuJJ_"+signal+"_MJJFromDC_"+l+"_"+p+"_"+c,c) ## just for a check
                        #'''
                        '''
                        makeSignalParamFromHisto(inDir+"LNuJJ_"+signal+"_2DFromDC_"+l+"_"+p+"_"+c+".root","templateSignalVsMX_fromHisto_"+signal+"_MVV_"+l+"_"+p+"_"+c,"MVV",signal,"1000,1500,2000,2500,3000,3500,4000,4500")
                        makeSignalParamFromHisto(inDir+"LNuJJ_"+signal+"_2DFromDC_"+l+"_"+p+"_"+c+".root","templateSignalVsMX_fromHisto_"+signal+"_MJJ_"+l+"_"+p+"_"+c,"MJJ",signal,"1000,1500,2000,2500,3000,3500,4000,4500")
                        #'''
                        #'''
                        makeSignalParamFromDC("Dc_"+signal+"/combined_"+YEAR+".root",signal+"_MVV_"+c+"_"+l+"_"+p+"_"+YEAR,"templateSignalVsMX_fromDC_"+signal+"_MVV_"+l+"_"+p+"_"+c,signal,"1000,1500,2000,2500,3000,3500,4000,4500",varMVV[c],"m_{WV} (GeV)")
                        makeSignalParamFromDC("Dc_"+signal+"/combined_"+YEAR+".root",signal+"_MJJ_"+c+"_"+l+"_"+p+"_"+YEAR,"templateSignalVsMX_fromDC_"+signal+"_MJJ_"+l+"_"+p+"_"+c,signal,"1000,1500,2000,2500,3000,3500,4000,4500",varMJJ[c],"m_{jet} (GeV)")
                        #''' 
                        '''
                        for mx in [2000]:
                            makeTemplate2D(inDir+"LNuJJ_"+signal+"_2DFromDC_"+l+"_"+p+"_"+c+".root",signal+str(mx),"template_"+signal+str(mx)+"_"+l+"_"+p+"_"+c,False)
                            makeTemplate2D(inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root",signal+str(mx),"reco_"+signal+str(mx)+"_"+l+"_"+p+"_"+c,False)
                            #makeTemplate2D(inDir+"LNuJJ_"+signal+"_MVVGivenMJJFromDC_"+l+"_"+p+"_"+c+".root",signal+str(mx),"templCond_"+signal+str(mx)+"_"+l+"_"+p+"_"+c,False)
                            makeTemplateVsReco2D(inDir+"LNuJJ_"+signal+"_2DFromDC_"+l+"_"+p+"_"+c+".root",signal+str(mx),inDir+"LNuJJ_norm_"+l+"_"+p+"_"+c+".root",signal+str(mx),"templateVsReco_"+signal+str(mx)+"_"+l+"_"+p+"_"+c)
                        #'''
    '''
    for signal in signals:
        #continue
        if options.withDC:
            compCategories(inDir+"LNuJJ_"+signal+"_2DFromDC",signal+"2000",True,leptons,purities,categories,"compTemplate_"+signal+"2000","MVV","m_{WV} (GeV)",False)
            compCategories(inDir+"LNuJJ_"+signal+"_2DFromDC",signal+"2000",True,leptons,purities,categories,"compTemplate_"+signal+"2000","MJJ","m_{jet} (GeV)")
        compCategories(inDir+"LNuJJ_norm",signal+"2000",True,leptons,purities,categories,"compReco_"+signal+"2000","MVV","m_{WV} (GeV)",False)
        compCategories(inDir+"LNuJJ_norm",signal+"2000",True,leptons,purities,categories,"compReco_"+signal+"2000","MJJ","m_{jet} (GeV)")
    #'''



if 'bbtagunc' in plots:
    for c in categories:#['nobb']:#
        for p in purities:#['HP']:#
            for l in leptons:#['e']:#
                makeSignalYieldParam_unc(inDir+"LNuJJ_XWW_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWW_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWW_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalYieldbbSFunc_XWW_"+l+"_"+p+"_"+c,0)
                makeSignalYieldParam_unc(inDir+"LNuJJ_XWZ_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWZ_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWZ_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalYieldbbSFunc_XWZ_"+l+"_"+p+"_"+c,0)
                makeSignalYieldParam_unc(inDir+"LNuJJ_XWH_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWH_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWH_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalYieldbbSFunc_XWH_"+l+"_"+p+"_"+c,0)
                makeSignalYieldParam_unc(inDir+"LNuJJ_VBFXWW_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_VBFXWW_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_VBFXWW_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalYield_VBFXWW_bbSFunc_"+l+"_"+p+"_"+c,0)
                makeSignalYieldParam_unc(inDir+"LNuJJ_XWW_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWW_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWW_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalbbSFunc_XWW_"+l+"_"+p+"_"+c,1)
                makeSignalYieldParam_unc(inDir+"LNuJJ_XWZ_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWZ_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWZ_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalbbSFunc_XWZ_"+l+"_"+p+"_"+c,1)
                makeSignalYieldParam_unc(inDir+"LNuJJ_XWH_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWH_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_XWH_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalbbSFunc_XWH_"+l+"_"+p+"_"+c,1)
                makeSignalYieldParam_unc(inDir+"LNuJJ_VBFXWW_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_VBFXWW_bbSFup_"+l+"_"+p+"_"+c+"_yield.root",inDir+"LNuJJ_VBFXWW_bbSFdn_"+l+"_"+p+"_"+c+"_yield.root","paramSignalbbSFunc_VBFXWW_"+l+"_"+p+"_"+c,1)



if 'scaleres' in plots:
    makeKernelScaleResolution(inDir+"LNuJJ_nonRes_detectorResponse.root","scalexHisto","nonRes_")
    makeKernelScaleResolution(inDir+"LNuJJ_nonRes_detectorResponse.root","scaleyHisto","nonRes_")
    makeKernelScaleResolution(inDir+"LNuJJ_nonRes_detectorResponse.root","resxHisto","nonRes_")
    makeKernelScaleResolution(inDir+"LNuJJ_nonRes_detectorResponse.root","resyHisto","nonRes_")

    #makeKernelScaleResolution(inDir+"LNuJJ_resW_detectorResponse.root","scalexHisto","resW_")
    #makeKernelScaleResolution(inDir+"LNuJJ_resW_detectorResponse.root","scaleyHisto","resW_")
    #makeKernelScaleResolution(inDir+"LNuJJ_resW_detectorResponse.root","resxHisto","resW_")
    #makeKernelScaleResolution(inDir+"LNuJJ_resW_detectorResponse.root","resyHisto","resW_")

    makeKernelScaleResolution(inDir+"LNuJJ_res_detectorResponse.root","scalexHisto","res_")
    makeKernelScaleResolution(inDir+"LNuJJ_res_detectorResponse.root","scaleyHisto","res_")
    makeKernelScaleResolution(inDir+"LNuJJ_res_detectorResponse.root","resxHisto","res_")
    makeKernelScaleResolution(inDir+"LNuJJ_res_detectorResponse.root","resyHisto","res_")

