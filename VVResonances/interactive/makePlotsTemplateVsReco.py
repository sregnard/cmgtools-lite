import os
import ROOT
from array import array
from ROOT import gStyle,gROOT,gPad
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-i","--inDir",dest="inDir",default='.',help="directory containing inputs")
parser.add_option("-o","--outDir",dest="outDir",default='PlotsCheckTemplates',help="where to save the plots")
parser.add_option("-C","--contrib",dest="contrib",default='nonRes',help="nonRes or resW")
parser.add_option("-s","--signal",dest="signal",default=False,action="store_true",help="signal template")
parser.add_option("-b","--binmvv",dest="mvvbinning",type=int,default=168,help="168 or 42")
parser.add_option("-B","--binmjet",dest="mjetbinning",type=int,default=90,help="90 or 18")
parser.add_option("-c","--cat",dest="category",default='nob',help="category") ## fix the category because the binning depends on it
parser.add_option("-r","--inranges",dest="inranges",type=int,default=1,help="also in intervals of the other variable")
parser.add_option("-f","--final",dest="final",type=int,default=0,help="print CMS label")
parser.add_option("-d","--coarse",dest="coarse",type=int,default=0,help="debug coarse template")
(options,args) = parser.parse_args()


leptons = ['mu','e']
purities = ['LP','HP']

ININTERVALS = options.inranges
DOMVV = 1
RATIOPLOT = 1

def saveCanvas(canvas,name):
    canvas.SaveAs(name+".root")
    canvas.SaveAs(name+".C")
    canvas.SaveAs(name+".pdf")
    #canvas.SaveAs(name+".png")
    canvas.SaveAs(name+".eps")
    os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
    os.system("rm "+name+".eps")



tag = ''

recoColor = ROOT.kGray+3
tptColor = ROOT.kGray+1
if options.signal:
    if 'XWW' in options.contrib: tptColor = ROOT.kOrange+2
    if 'XWZ' in options.contrib: tptColor = ROOT.kViolet-8
    if 'XWH' in options.contrib: tptColor = ROOT.kTeal-6
templates = [
  { 'name':'new_mjspline', 'source':options.inDir,             'lstyle':1, 'lcolor':tptColor       , 'label':"Template", },
]
n = len(templates)
RATIOPLOT = RATIOPLOT and n==1

ir = {}
ir['nonRes'] = {
    'nIntervalsMVV': 3,
    'nIntervalsMJ' : 3,
    'binColorTpt' : [ROOT.kGray+1, ROOT.TColor.GetColor("#88A8E0"), ROOT.TColor.GetColor("#E68F6F"), ROOT.TColor.GetColor("#9CD663")],
    'binColorReco': [ROOT.kGray+3, ROOT.kBlue+2, ROOT.kRed+2, ROOT.kGreen+3 ],
    'rangeLoMVVCoarseTpt' : [-1,1,5,9], ## MJ in [30,70], [70,110], [110,210]  
    'rangeUpMVVCoarseTpt' : [-1,4,8,14],
    'rangeLoMVVCoarseReco': ([-1,1,5,9] if options.mjetbinning == 18
                             else [-1,1,21,41]), 
    'rangeUpMVVCoarseReco': ([-1,4,8,18] if options.mjetbinning == 18
                             else [-1,20,40,90]),
    'rangeLoMVV': ([-1,1,5,9] if options.mjetbinning == 18 ## MJ in [30,70], [70,110], [110,210]
                   else [-1,1,18,39]), ## MJ in [30,64], [64,106], [106,210]
    'rangeUpMVV': ([-1,4,8,18] if options.mjetbinning == 18
                   else [-1,17,38,90]),
    'rangeLoMJ': ([-1,1,3,9] if options.mvvbinning == 42 ## MVV in [800,1000], [1000,1600], [1600,5000]
                  else [-1,1,9,33]), ## MVV in [800,1000], [1000,1600], [1600,5000]
    'rangeUpMJ': ([-1,2,8,42] if options.mvvbinning == 42
                  else [-1,8,32,168]),
    'rangeLabelMVV': (['full m_{jet} range', '30 #leq m_{jet} < 70 GeV', '70 #leq m_{jet} < 110 GeV', '110 #leq m_{jet} < 210 GeV'] if options.mjetbinning == 18 or options.coarse
                      else ['full m_{jet} range', '30 #leq m_{jet} < 64 GeV', '64 #leq m_{jet} < 106 GeV', '106 #leq m_{jet} < 210 GeV']),
    'rangeLabelMJ' : ['full m_{WV} range', '0.8 #leq m_{WV} < 1.0 TeV', '1.0 #leq m_{WV} < 1.6 TeV', '1.6 #leq m_{WV} < 5.0 TeV'],
    'multMVV': [1., 1., 1e-1, 1e-2],
    'multMJ' : [1., 1., 1., 4.],
    'multLabelMVV': ['', '', ' (#times 0.1)', ' (#times 0.01)'],
    'multLabelMJ' : ['', '', '', ' (#times 4)'],
}
ir['resW'] = {
    'nIntervalsMVV': 5,
    'nIntervalsMJ' : 3,
    'binColorTpt' : [ROOT.kGray+1, ROOT.TColor.GetColor("#88A8E0"), ROOT.TColor.GetColor("#E68F6F"), ROOT.TColor.GetColor("#9CD663"), ROOT.kOrange-9, ROOT.kMagenta-9],
    'binColorReco': [ROOT.kGray+3, ROOT.kBlue+2, ROOT.kRed+2, ROOT.kGreen+3, ROOT.kOrange+2, ROOT.kMagenta+2 ],
    'rangeLoMVV': ([-1,1,5,8,13,17] if options.mjetbinning == 18 ## MJ in [30,70], [70,100], [100,150], [150,190], [190,210]
                   else [-1,1,19,33,61,78]), ## MJ in [30,66], [66,94], [94,150], [150,184], [184,210]
    'rangeUpMVV': ([-1,4,7,12,16,18] if options.mjetbinning == 18
                   else [-1,18,32,60,77,90]),
    'rangeLoMJ': ([-1,1,3,9] if options.mvvbinning == 42 ## MVV in [800,1000], [1000,1600], [1600,5000]
                  else [-1,1,9,33]), ## MVV in [800,1000], [1000,1600], [1600,5000]
    'rangeUpMJ': ([-1,2,8,42] if options.mvvbinning == 42
                  else [-1,8,32,168]),
    'rangeLabelMVV': (['full m_{jet} range', '30 #leq m_{jet} < 70 GeV', '70 #leq m_{jet} < 100 GeV', '100 #leq m_{jet} < 150 GeV', '150 #leq m_{jet} < 190 GeV', '190 #leq m_{jet} < 210 GeV'] if options.mjetbinning == 18
                      else ['full m_{jet} range', '30 #leq m_{jet} < 66 GeV', '66 #leq m_{jet} < 94 GeV', '94 #leq m_{jet} < 150 GeV', '150 #leq m_{jet} < 184 GeV', '184 #leq m_{jet} < 210 GeV']),
    'rangeLabelMJ' : ['full m_{WV} range', '0.8 #leq m_{WV} < 1.0 TeV', '1.0 #leq m_{WV} < 1.6 TeV', '1.6 #leq m_{WV} < 5.0 TeV'],
    'multMVV': [1., 1., 1., 1., 1e-2, 1e-2],
    'multMJ' : [1., 1., 1., 4.],
    'multLabelMVV': ['', '', '', '', ' (#times 0.01)', ' (#times 0.01)'],
    'multLabelMJ' : ['', '', '', ' (#times 4)'],
}



def refillEvtPerAxisUnit(h1):
    for i in range(1,h1.GetNbinsX()+1):
        h1.SetBinContent(i,h1.GetBinContent(i)/h1.GetBinWidth(i))
        h1.SetBinError(i,h1.GetBinError(i)/h1.GetBinWidth(i))
    return h1

def refillEvtPerBin(h2Coarse):
    for i in range(1,h2Coarse.GetNbinsX()+1):
        for j in range(1,h2Coarse.GetNbinsY()+1):
            h2Coarse.SetBinContent(i,j,h2Coarse.GetBinContent(i,j)*h2Coarse.GetYaxis().GetBinWidth(j))
            h2Coarse.SetBinError(i,j,h2Coarse.GetBinError(i,j)*h2Coarse.GetYaxis().GetBinWidth(j))
    return h2Coarse



def compareTemplatesVsReco(contrib,l,p,c,var,varDesc,label):

    cat=l+"_"+p+"_"+c

    nintervals = ir[contrib]['nIntervalsMVV' if var=="MVV" else 'nIntervalsMJ'] if ININTERVALS else 0

    c=ROOT.TCanvas("c","c",500,500)
    c.cd()

    if RATIOPLOT:
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

    LOGY = var=="MVV" and (contrib=='nonRes' or contrib=='resW')
    if LOGY:
        (pad1 if RATIOPLOT else c).SetLogy()

    fRecoName = options.inDir+"/LNuJJ_"+cat+".root"
    if not os.path.isfile(fRecoName):
        print "Error in compareTemplatesVsReco: file "+fRecoName+" does not exist."
        return
    fReco = ROOT.TFile(fRecoName)
    h2_Reco = fReco.Get(contrib)
    hReco = [None]*(1+nintervals)

    fTpt = []
    h2_Tpt = []
    hTpt = []
    if contrib=='nonRes':
        fTptName = "LNuJJ_nonRes_COND2D_"+cat+".root" if options.coarse else "LNuJJ_nonRes_2D_"+cat+".root"
    elif contrib=='resW':
        fTptName = "LNuJJ_resW_2DFromDC_"+cat+".root"
    elif options.signal:
        fTptName = "LNuJJ_"+(''.join([i for i in contrib if not i.isdigit()]))+"_2DFromDC_"+cat+".root"
    for i in range(n):
        fTptPath = templates[i]['source']+"/"+fTptName
        if not os.path.isfile(fTptPath):
            print "Error in compareTemplatesVsReco: file "+fTptPath+" does not exist."
            return
        fTpt.append(ROOT.TFile(fTptPath))
        h2_Tpt.append(fTpt[i].Get(contrib if options.signal else "histo_coarse" if options.coarse else "histo"))
        if options.coarse:
            refillEvtPerBin(h2_Tpt[i])
        hTpt.append([None]*(1+nintervals))

    if var=="MVV":

        hReco[0] = h2_Reco.Clone().ProjectionX('_px')
        if ININTERVALS:
            for r in range(1,1+nintervals):
                hReco[r] = h2_Reco.Clone().ProjectionX('_px_'+str(r),ir[contrib]['rangeLoMVVCoarseReco' if options.coarse else 'rangeLoMVV'][r],ir[contrib]['rangeUpMVVCoarseReco' if options.coarse else 'rangeUpMVV'][r])
                hReco[r].Scale(ir[contrib]['multMVV'][r])

        for i in range(n):
            hTpt[i][0] = h2_Tpt[i].Clone().ProjectionX(str(i)+'_px')
            if ININTERVALS:
                for r in range(1,1+nintervals):
                    hTpt[i][r] = h2_Tpt[i].Clone().ProjectionX(str(i)+'_px_'+str(r),ir[contrib]['rangeLoMVVCoarseTpt' if options.coarse else 'rangeLoMVV'][r],ir[contrib]['rangeUpMVVCoarseTpt' if options.coarse else 'rangeUpMVV'][r])
                    hTpt[i][r].Scale(ir[contrib]['multMVV'][r])

    elif var=="MJ":

        hReco[0] = h2_Reco.Clone().ProjectionY('_py')
        if options.coarse:
            hReco[0] = hReco[0].Rebin(14,hReco[0].GetName()+"_rebinned",array('d',[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,140.,150.,160.,180.,210.]))
            refillEvtPerAxisUnit(hReco[0])
        if ININTERVALS:
            for r in range(1,1+nintervals):
                hReco[r] = h2_Reco.Clone().ProjectionY('_py_'+str(r),ir[contrib]['rangeLoMJ'][r],ir[contrib]['rangeUpMJ'][r])
                if options.coarse:
                    hReco[r] = hReco[r].Rebin(14,hReco[r].GetName()+"_rebinned",array('d',[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,140.,150.,160.,180.,210.]))
                    refillEvtPerAxisUnit(hReco[r])
                hReco[r].Scale(ir[contrib]['multMJ'][r])

        for i in range(n):
            hTpt[i][0] = h2_Tpt[i].Clone().ProjectionY(str(i)+'_py')
            if options.coarse:
                refillEvtPerAxisUnit(hTpt[i][0])
            if ININTERVALS:
                for r in range(1,1+nintervals):
                    hTpt[i][r] = h2_Tpt[i].Clone().ProjectionY(str(i)+'_py_'+str(r),ir[contrib]['rangeLoMJ'][r],ir[contrib]['rangeUpMJ'][r])
                    if options.coarse:
                        refillEvtPerAxisUnit(hTpt[i][r])
                    hTpt[i][r].Scale(ir[contrib]['multMJ'][r])

    hTpt[0][0].GetXaxis().SetTitleSize(0.05)
    hTpt[0][0].GetYaxis().SetTitleSize(0.07 if RATIOPLOT else 0.05)
    hTpt[0][0].GetXaxis().SetLabelSize(0.04 if RATIOPLOT else 0.037)
    hTpt[0][0].GetYaxis().SetLabelSize(0.045 if RATIOPLOT else 0.035)
    hTpt[0][0].GetXaxis().SetTitleOffset(1.1)
    if RATIOPLOT: hTpt[0][0].GetXaxis().SetLabelOffset(3)
    hTpt[0][0].GetYaxis().SetTitleOffset(0.9 if RATIOPLOT else 1.35)
    hTpt[0][0].GetXaxis().SetTitle(varDesc)
    hTpt[0][0].GetYaxis().SetTitle("arbitrary scale")#"a.u.")

    intHReco = hReco[0].Integral()
    intHTpt = [None]*n
    for i in range(n):
        intHTpt[i] = hTpt[i][0].Integral()

    for r in range(1+nintervals):
        for i in range(n):
            hTpt[i][r].SetLineColor(ir[contrib]['binColorTpt'][r] if ININTERVALS else templates[i]['lcolor'])
            hTpt[i][r].SetLineWidth(2 if var=="MJ" else 1)
            hTpt[i][r].SetLineStyle(templates[i]['lstyle'] if ININTERVALS else 1)
            hTpt[i][r].SetFillStyle(0)
            hTpt[i][r].Scale(1/intHTpt[i])
            hTpt[i][r].Draw("hist,same")

        hReco[r].SetLineColor(ir[contrib]['binColorReco'][r] if ININTERVALS else recoColor)
        hReco[r].SetMarkerColor(ir[contrib]['binColorReco'][r] if ININTERVALS else recoColor)
        hReco[r].SetMarkerSize(0.6 if var=="MJ" else 0.3)
        hReco[r].Scale(1/intHReco)
        hReco[r].Draw("p,same")

    lgd=ROOT.TLegend(0.38 if var=="MVV" else 0.45, ((0.91,0.95)[RATIOPLOT])-(1+n+nintervals*ININTERVALS)*((0.042,0.052)[RATIOPLOT]),0.9,(0.91,0.95)[RATIOPLOT])
    lgd.SetBorderSize(0)
    lgd.SetFillStyle(0)
    lgd.SetTextFont(42)
    lgd.SetTextSize((0.036,0.05)[RATIOPLOT])
    lgd.AddEntry(hReco[0],"Reconstructed simulation","pe")
    if n==1:
        lgd.AddEntry(hTpt[0][0],"Template","l")
    else:
        for i in range(n):
            lgd.AddEntry(hTpt[i][0],templates[i]['label'],"l")
    if ININTERVALS:
        for r in range(1,1+nintervals):
            rangeLabel = ir[contrib]['rangeLabelMVV'][r] if var=="MVV" else ir[contrib]['rangeLabelMJ'][r]
            multLabel = ir[contrib]['multLabelMVV'][r] if var=="MVV" else ir[contrib]['multLabelMJ'][r]
            lgd.AddEntry(hTpt[0][r],rangeLabel+multLabel,"l")

    hmax = hReco[0].GetMaximum()
    ymax = (1.3,10.)[LOGY] * hmax
    ymin = (0.,1.5e-9)[LOGY]
    hTpt[0][0].GetYaxis().SetRangeUser(ymin,ymax)

    (pad1 if RATIOPLOT else c).Update()
    lgd.Draw()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextAlign(13) 
    latex.SetTextSize((0.036,0.05)[RATIOPLOT]) 
    latex.DrawLatex(0.18,(0.90,0.93)[RATIOPLOT],label)

    if RATIOPLOT:
        pad1.RedrawAxis()
        pad1.Update()

        pad2.cd()
        pad2.SetGridy()

        hLine = hTpt[0][0].Clone()
        hLine.Divide(hLine)
        hLine.SetLineWidth(1)
        hLine.SetLineColor(14)
        hLine.GetXaxis().SetLabelSize(0.16)
        hLine.GetYaxis().SetLabelSize(0.125)
        hLine.GetXaxis().SetLabelOffset(0.007)
        hLine.GetXaxis().SetTitleSize(0.21)    
        hLine.GetYaxis().SetTitleSize(0.17)   
        hLine.GetXaxis().SetTitleOffset(0.95)    
        hLine.GetYaxis().SetTitleOffset(0.35)    
        hLine.GetXaxis().SetTitle(varDesc)
        hLine.GetYaxis().SetTitle("Reco./templ.")
        hLine.GetYaxis().SetNdivisions(206)
        hLine.GetYaxis().SetRangeUser(0.,1.95)
        hLine.Draw("hist")

        hRatio = [None]*(1+nintervals)
        for r in range(1+nintervals):
            hRatio[r] = hReco[r].Clone()
            for i in range(1,hRatio[r].GetNbinsX()):
                hRatio[r].SetBinContent(i,hRatio[r].GetBinContent(i)/hTpt[0][r].GetBinContent(i) if hTpt[0][r].GetBinContent(i) else 0.)
                hRatio[r].SetBinError(i,hRatio[r].GetBinError(i)/hTpt[0][r].GetBinContent(i) if hTpt[0][r].GetBinContent(i) else 0.)
            #hRatio[r].Divide(hTpt[0][r])
            hRatio[r].SetMarkerSize(0.4 if var=="MJ" else 0.3)
            hRatio[r].Draw("0Psame")

        pad2.RedrawAxis()
        pad2.Update()

    if options.final:
        CMSPlotLabel("CMS","Simulation Supplementary",{'':{'lumi':'','energy':'13 TeV'}})(c,'',0)

    saveCanvas(c,options.outDir+"/"+'templateVsReco'+tag+'_'+contrib+("Coarse" if options.coarse else "")+'_'+var+'_'+cat)




os.system("mkdir -p "+options.outDir)



setTDRStyle()
style=gROOT.GetStyle("tdrStyle").Clone()
style.SetPadLeftMargin(0.14)
style.SetPadRightMargin(0.04)
style.cd()


for l in leptons:
    for p in purities:
        #for c in categories:

        #if not (p=='HP' and l=='mu'): continue
          
        label=(("electron","muon")[l=='mu'])+", "+p

        compareTemplatesVsReco(options.contrib,l,p,options.category,'MJ',"m_{jet} (GeV)",label)
        
        if DOMVV:
            compareTemplatesVsReco(options.contrib,l,p,options.category,'MVV',"m_{WV} (GeV)",label)
