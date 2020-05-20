#!/usr/bin/env python

import os
import ROOT
from ROOT import gStyle,gROOT,gPad
import math
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *

import optparse
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",default='limitPlot',help="output plot name")
parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=1000.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=4500.0)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=0.0001)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=2.5)
parser.add_option("-t","--titleX",dest="titleX",default='m_{X} (GeV)',help="title of x axis")
parser.add_option("-T","--titleY",dest="titleY",default='#sigma #times #bf{#it{#Beta}} (pb)',help="title of y axis")
parser.add_option("-b","--blind",dest="blind",type=int,help="don't draw the observed",default=1)
parser.add_option("-l","--log",dest="log",type=int,help="use log scale",default=1)
parser.add_option("-c","--curves",dest="curves",default='',help="which curves to draw")
parser.add_option("-r","--ratio",action="store_true",dest="ratioToNominal",help="ratio to 1st expected limit curve",default=False)
parser.add_option("-m","--markers",action="store_true",dest="drawMarkers",help="draw markers",default=False)
parser.add_option("-H","--lheader",dest="legendHeader",type=int,help="put legend header",default=1)
parser.add_option("-s","--signal",dest="signal",default='',help="which signal theoretical cross section to draw if any: XWW, XWZ or XWH")
(options,args) = parser.parse_args()


def saveCanvas(canvas,name):
  canvas.SaveAs(name+".root")
  canvas.SaveAs(name+".C")
  canvas.SaveAs(name+".pdf")
  #canvas.SaveAs(name+".png")
  canvas.SaveAs(name+".eps")
  os.system("convert -density 150 -quality 100 "+name+".eps "+name+".png")
  os.system("rm "+name+".eps")




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






curveset = {}

nameSuffix,           lgdSuffix,                   color,          width, lstyle,blind, filepath           = range(7)

curveset['percateg']  = { 'lgdL':0.35, 'lgdD':0.55, 'grid':0, 'curves': [
    ( "bb_e_HP",      "bb, e, HP",                 ROOT.kOrange+7, 3,     9,     1,     "path/file.root", ),
    ( "bb_e_LP",      "bb, e, LP",                 ROOT.kOrange+7, 3,     7,     1,     "path/file.root", ),
    ( "bb_mu_HP",     "bb, #mu, HP",               ROOT.kPink-2,   3,     9,     1,     "path/file.root", ),
    ( "bb_mu_LP",     "bb, #mu, LP",               ROOT.kPink-2,   3,     7,     1,     "path/file.root", ),
    ( "nobb_e_HP",    "nobb, e, HP",               ROOT.kYellow+2, 3,     9,     1,     "path/file.root", ),
    ( "nobb_e_LP",    "nobb, e, LP",               ROOT.kYellow+2, 3,     7,     1,     "path/file.root", ),
    ( "nobb_mu_HP",   "nobb, #mu, HP",             ROOT.kGreen+2,  3,     9,     1,     "path/file.root", ),
    ( "nobb_mu_LP",   "nobb, #mu, LP",             ROOT.kGreen+2,  3,     7,     1,     "path/file.root", ),
    ( "vbf_e_HP",     "vbf, e, HP",                ROOT.kViolet+5, 3,     9,     1,     "path/file.root", ),
    ( "vbf_e_LP",     "vbf, e, LP",                ROOT.kViolet+5, 3,     7,     1,     "path/file.root", ),
    ( "vbf_mu_HP",    "vbf, #mu, HP",              ROOT.kAzure-3,  3,     9,     1,     "path/file.root", ),
    ( "vbf_mu_LP",    "vbf, #mu, LP",              ROOT.kAzure-3,  3,     7,     1,     "path/file.root", ),
    ( "combined",     "combined",                  ROOT.kBlack,    3,     1,     1,     "path/file.root", ),
]}

curveset['peryear']  = { 'lgdL':0.35, 'lgdD':0.6, 'grid':0, 'curves': [
    ( "old2016",      "B2G-16-029 (2016)",         ROOT.kBlue-7,   4,     3,     1,     "path/file.root", ),
    ( "2016",         "2016",                      ROOT.kBlue-7,   4,     7,     1,     "path/file.root", ),
    ( "2017",         "2017",                      ROOT.kGreen-3,  4,     7,     1,     "path/file.root", ),
    ( "2018",         "2018",                      ROOT.kOrange-5, 4,     7,     1,     "path/file.root", ),
    ( "Run2",         "full Run 2",                ROOT.kBlack,    4,     7,     1,     "path/file.root", ),
]}





plot = curveset[options.curves]
curves = plot['curves']
ncurves = len(curves)
sig = options.signal

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
frame.GetXaxis().SetTitle(options.titleX)
frame.GetYaxis().SetTitle(options.titleY)
frame.GetXaxis().SetTitleOffset(1.15)
frame.GetYaxis().SetTitleOffset(1.35)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleSize(0.05)
if not options.ratioToNominal: frame.GetYaxis().SetNdivisions(10)
frame.Draw()
c.Draw()
c.SetLogy(options.log)
if plot['grid']:
  c.SetGrid()


lgdshift = (0.,0.05)[sig!=""]
lgd = ROOT.TLegend(plot['lgdL'],plot['lgdD']-lgdshift,0.95,0.9-lgdshift)
lgd.SetFillStyle(0)
lgd.SetBorderSize(0)
lgd.SetTextFont(42)
lgd.SetTextSize(0.036)
if options.legendHeader: lgd.SetHeader("95% CL median expected upper limits")
compactLegend = True
exponly = True
for i in range(ncurves):
    if not curves[i][blind]:
        exponly = False
        break

f = [None]*ncurves
limit = [None]*ncurves
data = [None]*ncurves
bandExp = [None]*ncurves
bandObs = [None]*ncurves

for i in range(ncurves):
    #if i==1: continue

    obsbl = options.blind==1 and curves[i][blind]

    f[i] = ROOT.TFile(curves[i][filepath])
    limit[i] = f[i].Get("limit")
    data[i] = {}

    for event in limit[i]:
        if float(event.mh)<options.minX or float(event.mh)>options.maxX:
            continue
    
        if not (event.mh in data[i].keys()):
            data[i][event.mh]={}

        if event.quantileExpected<0:            
            data[i][event.mh]['obs']=event.limit
        if event.quantileExpected>0.02 and event.quantileExpected<0.03:            
            data[i][event.mh]['-2sigma']=event.limit
        if event.quantileExpected>0.15 and event.quantileExpected<0.17:            
            data[i][event.mh]['-1sigma']=event.limit
        if event.quantileExpected>0.49 and event.quantileExpected<0.51:            
            data[i][event.mh]['exp']=event.limit
        if event.quantileExpected>0.83 and event.quantileExpected<0.85:            
            data[i][event.mh]['+1sigma']=event.limit
        if event.quantileExpected>0.974 and event.quantileExpected<0.976:            
            data[i][event.mh]['+2sigma']=event.limit

    bandExp[i] = ROOT.TGraph()
    bandExp[i].SetName("limit_exp_"+curves[i][nameSuffix])

    bandObs[i] = ROOT.TGraph()
    bandObs[i].SetName("limit_obs_"+curves[i][nameSuffix])

    N=0
    for mass,info in data[i].iteritems():
        print 'Setting mass',mass,info

        if not ('exp' in info.keys() and '+1sigma' in info.keys() and '+2sigma' in info.keys() and '-1sigma' in info.keys() and '-2sigma' in info.keys() and 'obs' in info.keys()):
            print 'Incomplete file'
            continue

        if not obsbl:
            bandObs[i].SetPoint(N,mass,info['obs'])
 
        ## Manually excluding points where the fit failed
        #if options.curves=="" and (curves[i][nameSuffix] in [""]) and mass in []:
        #  continue

        bandExp[i].SetPoint(N,mass,info['exp'])
        if options.ratioToNominal:
            bandExp[i].SetPoint(N,mass,info['exp']/data[0][mass]['exp'])

        N=N+1

    bandExp[i].Sort()
    if not obsbl:
        bandObs[i].Sort()

    bandExp[i].SetLineWidth(curves[i][width])
    bandExp[i].SetLineColor(curves[i][color])
    bandExp[i].SetLineStyle(curves[i][lstyle])
    bandExp[i].SetMarkerStyle(0)

    if not obsbl:
        bandObs[i].SetLineWidth(curves[i][width])
        bandObs[i].SetLineColor(curves[i][color])
        bandObs[i].SetMarkerSize(0.5) #0.7)
        #bandObs[i].SetMarkerStyle(0)#20)
        bandObs[i].SetMarkerColor(curves[i][color])

    bandExp[i].Draw("Lsame")
    if not obsbl:
        if options.drawMarkers:
            bandObs[i].Draw("PLsame")
        else:
            bandObs[i].Draw("Lsame")

    if exponly:
        lgd.AddEntry(bandExp[i],curves[i][lgdSuffix],"l")
    elif not compactLegend:
        lgd.AddEntry(bandExp[i],"expected, "+curves[i][lgdSuffix],"l")
        if not obsbl:
            lgd.AddEntry(bandObs[i],"observed, "+curves[i][lgdSuffix],"lp")
    else:
        if not obsbl:
            lgd.AddEntry(bandObs[i],curves[i][lgdSuffix],"lp")
        if i == len(curves)-1:
            lgd.AddEntry(bandExp[i],"expected","l")

    f[i].Close()

c.Update()
c.RedrawAxis()

lgd.Draw()

if sig!="":
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
    lgdTh = ROOT.TLegend(0.35,0.87,0.92,0.92)
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
for i in range(ncurves):
    #if i==1: continue
    bandExp[i].Write()
    bandObs[i].Write()
fout.Close()
#'''


