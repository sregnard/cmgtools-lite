#!/usr/bin/env python

import os
import ROOT
from ROOT import gStyle,gROOT,gPad
import math
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-i","--input",dest="input",default='',help="input ROOT file")
parser.add_option("-o","--output",dest="output",default='limitPlot',help="output plot name")
parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=1000.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=4500.0)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=0.00004)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=2.)
#parser.add_option("-t","--titleX",dest="titleX",default='m_{X} (GeV)',help="title of x axis")
#parser.add_option("-T","--titleY",dest="titleY",default='#sigma #times #bf{#it{#Beta}} (pb)',help="title of y axis")
parser.add_option("-b","--blind",dest="blind",type=int,help="don't draw the observed",default=1)
parser.add_option("-l","--log",dest="log",type=int,help="use log scale",default=1)
parser.add_option("-C","--CMSlabel",dest="CMSlabel",type=int,default=0,help="0:None 1:CMS 2:CMS Preliminary 3:CMS Supplementary")
parser.add_option("-p","--period",dest="period",default='Run2',help="run period, to set the luminosity: 2016, 2017, 2018, or Run2")
parser.add_option("-s","--signal",dest="signal",default='generic',help="which signal: XWW, XWZ, XWH, or VBFXWW")
(options,args) = parser.parse_args()


def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  os.system("rm "+name+".eps")

def cmsLabel(canvas,period):
  if options.CMSlabel==0:
    cmslabel_not(canvas,period,11)
  elif options.CMSlabel==1:
    cmslabel_final(canvas,period,11)
  elif options.CMSlabel==2:
    cmslabel_prelim(canvas,period,11)
  elif options.CMSlabel==3:
    cmslabel_suppl(canvas,period,11)




drawTheo = 1

sigxsec = {}
sigxsec['XWW']  = { 
    'theo':[
#    (mG(GeV),25*XS(pb),WW,full(%)(from xsec file, not to be taken),PDF,Scale),
    ( 1000, 25 * 0.0056657071801246945 , 0.24760630932823052, 29.660917045836598, (0.10565+0.14237)/2., (0.0978498+0.124306)/2. ),
    ( 1500, 25 * 0.0005727231501579456 , 0.22005013790397887, 43.337397245335346, (0.165529+0.192089)/2. , (0.134482+0.143518)/2. ),
    ( 1800, 25 * 0.00018315617607742797, 0.21371662932013388, 52.52437529376242 , 0.218125, 0.151284 ),
    ( 2000, 25 * 0.00009062263600103764, 0.21103043636291363, 59.42154491428172 , 0.247751, 0.158533 ),
    ( 2500, 25 * 0.00001868308774736877, 0.20696480536908055, 78.00923022309604 , 0.339052, 0.174824 ),
    ( 3000, 25 * 4.412202866735033e-6  , 0.20478514049527263, 100.51611811048016, 0.450011, 0.189223 ),
    ( 3500, 25 * 1.1518090410508347e-6 , 0.20348064946832398, 127.5113328296744 , 0.589637, 0.202864 ),
    ( 4500, 25 * 8.933087336020322e-8  , 0.2020619221283911 , 198.910055050015  , 1., 0.227372 ),
    ], 
    'lgdTheo':"G_{Bulk}#rightarrowWW, #tilde{k} = 0.5" 
}
sigxsec['XWZ']  = { 
    'theo':[
#        (M0,BRZW,BRWH,CX0(pb),CX+(pb),CX-(pb),PDF,Scale),
        (1000.,0.460359,0.507973,0.509804,0.687047,0.299486, 0.0419527, 0.0400242 ),
        #(1100.,0.464974,0.49948,0.37177,0.512156,0.214767),
        (1200.,0.467605,0.493896,0.271104,0.381432,0.153962, 0.0437757, 0.0502532 ),
        #(1300.,0.469214,0.489978,0.198844,0.285322,0.110992),
        (1400.,0.470248,0.487101,0.146961,0.214856,0.0806679, 0.0460551, 0.058957 ),
        #(1500.,0.470938,0.484915,0.109482,0.162942,0.0591312),
        (1600.,0.471413,0.48321,0.0822156,0.124438,0.0437098, 0.0483122, 0.0666744 ),
        #(1700.,0.471749,0.481851,0.0622015,0.0956578,0.0325698),
        (1800.,0.471991,0.480747,0.0473673,0.0739789,0.0244536, 0.0509453, 0.0739624 ),
        #(1900.,0.472168,0.479838,0.036303,0.0575243,0.0184817),
        (2000.,0.472301,0.479079,0.0279823,0.0449418,0.0140562, 0.0543189, 0.0807293 ),
        #(2100.,0.472401,0.478438,0.02168,0.035265,0.0107528),
        #(2200.,0.472477,0.477892,0.0168765,0.0277791,0.0082689),
        #(2300.,0.472536,0.477422,0.0131933,0.021956,0.00638847),
        #(2400.,0.472582,0.477015,0.0103538,0.0174056,0.00495788),
        (2500.,0.472619,0.476659,0.00815289,0.013834,0.00387631, 0.0655156, 0.0967945 ),
        #(2600.,0.472647,0.476347,0.00644032,0.01102,0.00302043),
        #(2700.,0.47267,0.476071,0.0051021,0.00879738,0.00236942),
        #(2800.,0.472688,0.475827,0.00405245,0.00703223,0.00186407),
        #(2900.,0.472703,0.475608,0.00323048,0.00562985,0.00147046),
        (3000.,0.472715,0.475412,0.00257265,0.00451288,0.00116241, 0.0846863, 0.11186 ),
        #(3100.,0.472724,0.475236,0.00205583,0.00362067,0.000921187),
        #(3200.,0.472732,0.475077,0.00164562,0.00290702,0.000731461),
        #(3300.,0.472738,0.474933,0.00131918,0.0023356,0.000581736),
        #(3400.,0.472743,0.474802,0.00105885,0.00187714,0.000463361),
        (3500.,0.472748,0.474682,0.000850838,0.00150893,0.000369561, 0.118175, 0.125904 ),
        #(3600.,0.472751,0.474573,0.000684318,0.00121305,0.000295015),
        #(3700.,0.472754,0.474473,0.000550813,0.000975141,0.000235716),
        #(3800.,0.472756,0.474381,0.000443641,0.000783596,0.000188334),
        #(3900.,0.472758,0.474296,0.000357546,0.000629536,0.000150705),
        (4000.,0.472759,0.474217,0.000288261,0.000505512,0.000120638, 0.18496, 0.137632 ),
        (4500.,1.,1.,0.,0.000105,0., 0.307965, 0.145058 ),
    ], 
    'lgdTheo':"W'#rightarrowWZ, HVT model B",
}
sigxsec['XWH']  = { 
    'theo':sigxsec['XWZ']['theo'],
    'lgdTheo':"W'#rightarrowWH, HVT model B",
}


plots = {}
plots['generic']  = { 
    'lgdL':0.47, 'lgdR':0.92, 'lgdD':0.64, 'lgdU':0.88, 
    'blind':0, 'grid':0,
    'titleX':"m_{X} (GeV)",
    'titleY':"#sigma #times #bf{#it{#Beta}} (pb)",
    'thl':0,
}
plots['XWW']  = { 
    'lgdL':0.47, 'lgdR':0.92, 'lgdD':0.64, 'lgdU':0.88, 
    'blind':0, 'grid':0,
    'titleX':"m_{G_{Bulk}} (GeV)",
    'titleY':"#sigma #times #bf{#it{#Beta}}(G_{Bulk}#rightarrowWW) (pb)",
    'thl':1,
}
plots['XWZ']  = { 
    'lgdL':0.47, 'lgdR':0.92, 'lgdD':0.64, 'lgdU':0.88, 
    'blind':0, 'grid':0,
    'titleX':"m_{W'} (GeV)",
    'titleY':"#sigma #times #bf{#it{#Beta}}(W'#rightarrowWZ) (pb)",
    'thl':1,
}
plots['XWH']  = { 
    'lgdL':0.47, 'lgdR':0.92, 'lgdD':0.64, 'lgdU':0.88, 
    'blind':0, 'grid':0,
    'titleX':"m_{W'} (GeV)",
    'titleY':"#sigma #times #bf{#it{#Beta}}(W'#rightarrowWH) (pb)",
    'thl':1,
}
plots['VBFXWW']  = { 
    'lgdL':0.47, 'lgdR':0.92, 'lgdD':0.64, 'lgdU':0.88, 
    'blind':0, 'grid':0,
    'titleX':"m_{radion} (GeV)",
    'titleY':"#sigma #times #bf{#it{#Beta}}(VBF radion#rightarrowWW) (pb)",
    'thl':0,
}


sig = options.signal
plot = plots[sig]
drawTheo = drawTheo and plot['thl']
blind = options.blind==1 or plot['blind']

setTDRStyle()
style=gROOT.GetStyle("tdrStyle").Clone()
style.SetPadLeftMargin(0.14)
style.SetPadRightMargin(0.04)
style.SetGridColor(14)
style.cd()

c=ROOT.TCanvas("c","c",500,500)
c.cd()
c.UseCurrentStyle()

frame=c.DrawFrame(options.minX,options.minY,options.maxX,options.maxY)
frame.GetXaxis().SetTitle(plot['titleX'])#options.titleX)
frame.GetYaxis().SetTitle(plot['titleY'])#options.titleY)
frame.GetXaxis().SetTitleOffset(1.15)
frame.GetYaxis().SetTitleOffset(1.35)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetNdivisions(10)
frame.Draw()
c.Draw()
c.SetLogy(options.log)
if plot['grid']:
  c.SetGrid()

cmsLabel(c,options.period)

f = ROOT.TFile(options.input)
limit = f.Get("limit")
#f.Close()
data = {}

for event in limit:
    if float(event.mh)<options.minX or float(event.mh)>options.maxX:
        continue
    
    if not (event.mh in data.keys()):
        data[event.mh]={}

    if event.quantileExpected<0:            
        data[event.mh]['obs']=event.limit
    if event.quantileExpected>0.02 and event.quantileExpected<0.03:            
        data[event.mh]['-2sigma']=event.limit
    if event.quantileExpected>0.15 and event.quantileExpected<0.17:            
        data[event.mh]['-1sigma']=event.limit
    if event.quantileExpected>0.49 and event.quantileExpected<0.51:            
        data[event.mh]['exp']=event.limit
    if event.quantileExpected>0.83 and event.quantileExpected<0.85:            
        data[event.mh]['+1sigma']=event.limit
    if event.quantileExpected>0.974 and event.quantileExpected<0.976:            
        data[event.mh]['+2sigma']=event.limit

lineExp = ROOT.TGraph()
lineExp.SetName("limit_exp")
band68 = ROOT.TGraphAsymmErrors()
band68.SetName("band68")
band95 = ROOT.TGraphAsymmErrors()
band95.SetName("band95")
lineObs = ROOT.TGraph()
lineObs.SetName("limit_obs")
line_plus1 = ROOT.TGraph()
line_plus1.SetName("line_plus1")
line_plus2 = ROOT.TGraph()
line_plus2.SetName("line_plus2")
line_minus1 = ROOT.TGraph()
line_minus1.SetName("line_minus1")
line_minus2 = ROOT.TGraph()
line_minus2.SetName("line_minus2")

N=0
for mass,info in data.iteritems():
    print mass, info

    if not ('exp' in info.keys() and '+1sigma' in info.keys() and '+2sigma' in info.keys() and '-1sigma' in info.keys() and '-2sigma' in info.keys() and 'obs' in info.keys()):
        print 'Incomplete file'
        continue

    if mass%50!=0: continue

    lineExp.SetPoint(N,mass,info['exp'])
    band68.SetPoint(N,mass,info['exp'])
    band95.SetPoint(N,mass,info['exp'])
    band68.SetPointError(N,0.0,0.0,info['exp']-info['-1sigma'],info['+1sigma']-info['exp'])
    band95.SetPointError(N,0.0,0.0,info['exp']-info['-2sigma'],info['+2sigma']-info['exp'])
    line_plus1.SetPoint(N,mass,info['+1sigma'])
    line_plus2.SetPoint(N,mass,info['+2sigma'])
    line_minus1.SetPoint(N,mass,info['-1sigma'])
    line_minus2.SetPoint(N,mass,info['-2sigma'])
    if not blind:
        lineObs.SetPoint(N,mass,info['obs'])

    N=N+1

lineExp.Sort()
band68.Sort()
band95.Sort()
if not blind:
    lineObs.Sort()
line_plus1.Sort()    
line_plus2.Sort()    
line_minus1.Sort()    
line_minus2.Sort()    

band68.SetFillColor(ROOT.kGreen+1)
#band68.SetLineWidth(3)
#band68.SetLineColor(ROOT.kBlue)
#band68.SetLineStyle(7)
#band68.SetMarkerStyle(0)
band95.SetFillColor(ROOT.kOrange)
line_plus1.SetLineWidth(1)
line_plus1.SetLineColor(ROOT.kGreen+1)    
line_plus2.SetLineWidth(1)
line_plus2.SetLineColor(ROOT.kOrange-2)
line_minus1.SetLineWidth(1)
line_minus1.SetLineColor(ROOT.kGreen+1)
line_minus2.SetLineWidth(1)
line_minus2.SetLineColor(ROOT.kOrange-2)
lineExp.SetLineWidth(2)
lineExp.SetLineColor(ROOT.kBlue)
lineExp.SetLineStyle(7)
lineExp.SetMarkerStyle(0)
if not blind:
    lineObs.SetLineWidth(2)
    lineObs.SetLineColor(ROOT.kBlack)
    lineObs.SetMarkerSize(0.6)
    lineObs.SetMarkerStyle(20)
    lineObs.SetMarkerColor(ROOT.kBlack)

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
if not blind:
    lineObs.Draw("PLsame")

gPad.Update()
#p=ROOT.TPad("p","p",0.,0.,1.,1.); p.SetFillStyle(0); p.Draw(); p.cd()
#box = ROOT.TBox(plot['lgdL'],plot['lgdD']-0.01-drawTheo*0.06-(not blind)*0.06,plot['lgdR'],plot['lgdU']+0.01+drawTheo*0.02)
#box.SetFillColor(ROOT.kWhite)
#box.Draw()
lgd = ROOT.TLegend(plot['lgdL'],plot['lgdD']-drawTheo*0.06-(not blind)*0.06,plot['lgdR'],plot['lgdU']-drawTheo*0.06)
lgd.SetFillStyle(0)
lgd.SetBorderSize(0)
lgd.SetTextFont(42)
lgd.SetTextSize(0.036)
lgd.SetHeader("95% CL upper limits")
if not blind:
    lgd.AddEntry(lineObs,"Observed","lp")
lgd.AddEntry(lineExp,"Median expected","l")
lgd.AddEntry(band68,"68% expected","f")
lgd.AddEntry(band95,"95% expected","f")
lgd.Draw()

if drawTheo:
    c.cd()
    bandTh = ROOT.TGraphAsymmErrors()
    bandTh.SetName("bandTh")
    M=0
    if sig=="XWW":
        for mass,xsec,brww,full,pdf,scale in sigxsec[sig]['theo']:
            xsecbr=xsec*brww
            print 'Mass',mass,' xsec_theo',xsec,' BR',brww,' Product',xsecbr
            bandTh.SetPoint(M,mass,xsecbr)
            absunc=xsecbr*math.sqrt(pdf*pdf+scale*scale)
            bandTh.SetPointError(M,0.0,0.0,absunc,absunc)
            M=M+1
    elif sig=="XWZ":
        for mass,brwz,brwh,xsec0,xsecplus,xsecminus,pdf,scale in sigxsec[sig]['theo']:
            xsecbr=(xsecplus+xsecminus)*brwz
            print 'Mass',mass,' xsec_theo',(xsecplus+xsecminus),' BR',brwz,' Product',xsecbr
            bandTh.SetPoint(M,mass,xsecbr)
            absunc=xsecbr*math.sqrt(pdf*pdf+scale*scale)
            bandTh.SetPointError(M,0.0,0.0,absunc,absunc)
            M=M+1
    elif sig=="XWH":
        for mass,brwz,brwh,xsec0,xsecplus,xsecminus,pdf,scale in sigxsec[sig]['theo']:
            xsecbr=(xsecplus+xsecminus)*brwh
            print 'Mass',mass,' xsec_theo',(xsecplus+xsecminus),' BR',brwh,' Product',xsecbr
            bandTh.SetPoint(M,mass,xsecbr)
            absunc=xsecbr*math.sqrt(pdf*pdf+scale*scale)
            bandTh.SetPointError(M,0.0,0.0,absunc,absunc)
            M=M+1
    bandTh.Sort()
    bandTh.SetFillColor(ROOT.kRed)
    bandTh.SetFillStyle(3013)
    bandTh.SetLineWidth(3)
    bandTh.SetLineColor(ROOT.kRed)
    bandTh.SetMarkerStyle(0)
    bandTh.Draw("3Lsame")
    lgdTh = ROOT.TLegend(plot['lgdL'],plot['lgdU']-0.02,plot['lgdR'],plot['lgdU']+0.02)
    lgdTh.SetFillStyle(0)
    lgdTh.SetBorderSize(0)
    lgdTh.SetTextFont(42)
    lgdTh.SetTextSize(0.036)
    lgdTh.AddEntry(bandTh,sigxsec[sig]['lgdTheo'],"fl")
    lgdTh.Draw()

c.Update()
c.RedrawAxis()

saveCanvas(c,options.output)

'''
fout=ROOT.TFile(options.output+".root","RECREATE")
fout.cd()
c.Write()
lineExp.Write()
band68.Write()
band95.Write()
lineObs.Write()
line_plus1.Write()    
line_plus2.Write()    
line_minus1.Write()    
line_minus2.Write()    
fout.Close()
#'''

