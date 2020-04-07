import ROOT
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *
import os
from array import array

def efficiency1D(plotter,var,bins,denom,num):    
    h1 = plotter.drawTH1Binned(var,denom,"1",bins)
    h2 = plotter.drawTH1Binned(var,denom+"*"+num,"1",bins)
    
#    graph=ROOT.TGraphAsymmErrors()
#    graph.Divide(h2,h1)
    h2.Divide(h1)
    return h2


def efficiency2D(plotter,var,binsx,binsy,denom,num):
    h1 = plotter.drawTH2Binned(var,denom,"1",binsx,binsy)
    h2 = plotter.drawTH2Binned(var,denom+"*"+num,"1",binsx,binsy)
    h2.Divide(h1)
    return h2


def makeEff():
    f=ROOT.TFile("trigger.root","RECREATE")
    f.cd()
    g=efficiency1D(VJets,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['e'],'HLT_ELE']),'HLT_MET120')
    g.Write("MET_ELE_MC")
    g=efficiency1D(data,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['e'],'HLT_ELE']),'HLT_MET120')
    g.Write("MET_ELE_DATA")
    g=efficiency1D(VJets,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['mu'],'HLT_MU']),'HLT_MET120')
    g.Write("MET_MU_MC")
    g=efficiency1D(data,"lnujj_l1_met_pt",[50,80,100,150,200,250,300,500,1000],"*".join([cuts['common'],cuts['mu'],'HLT_MU']),'HLT_MET120')
    g.Write("MET_MU_DATA")


    g=efficiency2D(VJets,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['e'],'HLT_MET120']),'HLT_ELE')
    g.Write("ELE_MC")
    g=efficiency2D(data,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['e'],'HLT_MET120']),'HLT_ELE')
    g.Write("ELE_DATA")

    g=efficiency2D(VJets,"lnujj_l1_l_eta:lnujj_l1_l_pt",[30,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['mu'],'HLT_MET120']),'HLT_MU')
    g.Write("MU_MC")
    g=efficiency2D(data,"lnujj_l1_l_eta:lnujj_l1_l_pt",[50,50,70,80,100,120,150,200,250,300,500,1000],[-2.5,-1.7,-0.9,0.9,1.7,2.5],"*".join([cuts['common'],cuts['mu'],'HLT_MET120']),'HLT_MU')
    g.Write("MU_DATA")
    
    f.Close()





def getPlotters(samples,isData=False,corr="1"):
    sampleTypes=samples.split(',')
    plotters=[]
    for filename in os.listdir('samples'):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                print 'Adding file',fname
                plotters.append(TreePlotter('samples/'+fname+'.root','tree'))
                if not isData:
                    plotters[-1].setupFromFile('samples/'+fname+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor('lnujj_sf','tree')
                    plotters[-1].addCorrectionFactor('truth_genTop_weight','tree')
                    plotters[-1].addCorrectionFactor(corr,'flat')
                    
    return  plotters


def compare(p1,p2,var,cut1,cut2,bins,mini,maxi,title,unit,leg1,leg2):
    canvas = ROOT.TCanvas("canvas","")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    canvas.cd()
    legend = ROOT.TLegend(0.62,0.2,0.92,0.4,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)


    h1=p1.drawTH1(var,cut1,"1",bins,mini,maxi,title,unit)
    h2=p2.drawTH1(var,cut2,"1",bins,mini,maxi,title,unit)
    h1.DrawNormalized("HIST")
    h2.DrawNormalized("SAME")
    legend.AddEntry(h1,leg1,"LF")
    legend.AddEntry(h2,leg2,"P")
    legend.Draw()

    pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
#    text = pt.AddText(0.01,0.3,"CMS Preliminary 2016")
#    text = pt.AddText(0.25,0.3,"#sqrt{s} = 13 TeV")
    pt.Draw()   


    return canvas,h1,h2,legend,pt


cuts={}

cuts['common'] = '(((HLT_MU)&&(abs(lnujj_l1_l_pdgId)==13))||((HLT_ELE)&&abs(lnujj_l1_l_pdgId)==11))*(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>600&&Flag_badChargedHadronFilter&&Flag_badMuonFilter&&Flag_globalTightHalo2016Filter)'


cuts['mu'] = '(abs(ljj_l1_l1_pdgId)==13)'
cuts['e'] = '(abs(lljj_l1_l1_pdgId)==11)'
cuts['HP'] = '(lljj_l2_tau2/lljj_l2_tau1<0.55)'
cuts['LP'] = '(lljj_l2_tau2/lljj_l2_tau1>0.55&&lljj_l2_tau2/lljj_l2_tau1<0.75)'


#change the CMS_lumi variables (see CMS_lumi.py)
lumi_13TeV = "35.9 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=4
iPos = 11



#zjPlotters=[]
BKGPlotters = getPlotters('DYJetsToLL_M50_HT,WJetsToLNu_HT,TT_pow,T_tWch,TBar_tWch',False)
BKG = MergedPlotter(BKGPlotters)


VVPlotters = getPlotters('WZTo2L2Q,WZTo1L1Nu2Q',False)
VV=MergedPlotter(VVPlotters)

DATAPlotters = getPlotters('SingleMuon_,SingleElectron_',True)
data=MergedPlotter(DATAPlotters)

SigPlotters = getPlotters('WprimeToWZToWhadZlep_narrow_1400',False)
sig = MergedPlotter(SigPlotters)


#Fill properties
BKG.setFillProperties(1001,ROOT.kAzure-9)
VV.setFillProperties(1001,ROOT.kSpring-5)

#Stack for lnu+J
lljjStack = StackPlotter()
lljjStack.addPlotter(BKG,"Bkg","V+Jets","background")
lljjStack.addPlotter(VV,"VV","VV","background")
lljjStack.addPlotter(sig,"sig","X #rightarrow WZ","signal")
lljjStack.addPlotter(data,"data_obs","Data","data")




