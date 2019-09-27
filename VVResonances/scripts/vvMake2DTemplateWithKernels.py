#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import json
import copy
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
ROOT.gSystem.Load("libCMGToolsVVResonances")
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-r","--res",dest="res",help="res",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--vars",dest="vars",help="variable for x",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="conditional bins split by comma",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-y","--miny",dest="miny",type=float,help="bins",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-l","--limit",dest="limit",type=float,help="lower limit of the high-mass smoothing range",default=2500)


DEBUG=0


def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        for j in range(1,histo.GetNbinsY()+1):
            up=histo.GetBinContent(i,j)/intUp
            nominal=histoNominal.GetBinContent(i,j)/intNominal
            newHisto.SetBinContent(i,j,nominal*nominal/up)
    return newHisto        


def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    maxFactor = max(pow(histo.GetXaxis().GetXmax(),power),pow(histo.GetXaxis().GetXmin(),power))
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        for j in range(1,histo.GetNbinsY()+1):
            nominal=histo.GetBinContent(i,j)
            factor = 1+alpha*pow(x,power) 
            newHistoU.SetBinContent(i,j,nominal*factor)
            newHistoD.SetBinContent(i,j,nominal/factor)
    if newHistoU.Integral()>0.0:        
        newHistoU.Scale(1.0/newHistoU.Integral())        
    if newHistoD.Integral()>0.0:        
        newHistoD.Scale(1.0/newHistoD.Integral())        
    return newHistoU,newHistoD        



def expandHisto(histo,options):
    histogram=ROOT.TH2F(histo.GetName(),"histo",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
    return histogram
        


def conditional(hist):
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)

def smoothTail(hist):
    hist.Scale(1.0/hist.Integral())

    bin_limit = hist.GetXaxis().FindBin(options.limit)

    histfit=hist.ProjectionX("q",1,hist.GetNbinsY())
    X=histfit.GetBinCenter(bin_limit)
    Y=histfit.GetBinContent(bin_limit)
    print 'X', X, 'Y', Y
    fun=ROOT.TF1("func","{Y}*(((x-[1])/({X}-[1]))^[0])".format(X=X,Y=Y),options.limit,options.maxx)
    fun.SetParameter(0,-10.)

    histfit.Fit(fun,"R")

    for i in range(1,hist.GetNbinsX()+1):
        x=hist.GetXaxis().GetBinCenter(i)
        if x>options.limit:
            for j in range(1,hist.GetNbinsY()+1):
                hist.SetBinContent(i,j,fun.Eval(x)*hist.GetBinContent(bin_limit,j)/fun.Eval(histfit.GetBinCenter(bin_limit)))
    



(options,args) = parser.parse_args()


random=ROOT.TRandom3(101082)


sampleTypes=options.samples.split(',')
dataPlotters=[]
dataPlottersNW=[]

for filename in os.listdir(args[0]):
    for sampleType in sampleTypes:
        if filename.find(sampleType)!=-1:
            fnameParts=filename.split('.')
            fname=fnameParts[0]
            ext=fnameParts[1]
            if ext.find("root") ==-1:
                continue
            dataPlotters.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            dataPlotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
            dataPlotters[-1].addCorrectionFactor('xsec','tree')
            dataPlotters[-1].addCorrectionFactor('genWeight','tree')
            dataPlotters[-1].addCorrectionFactor('puWeight','tree')
            dataPlotters[-1].addCorrectionFactor('lnujj_sf','branch')
            dataPlotters[-1].addCorrectionFactor('lnujj_btagWeight','branch')
            dataPlotters[-1].addCorrectionFactor('truth_genTop_weight','branch')
            dataPlotters[-1].filename = fname


            dataPlottersNW.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            dataPlottersNW[-1].addCorrectionFactor('puWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor('genWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor('lnujj_sf','branch')
            dataPlottersNW[-1].addCorrectionFactor('truth_genTop_weight','branch')
            dataPlottersNW[-1].addCorrectionFactor('lnujj_btagWeight','branch')
            dataPlottersNW[-1].filename = fname


#if options.data==2:
#    sigmas=[]
#    for d in dataPlotters:
#        sigmas.append(d.tree.GetMaximum("xsec")/d.weightinv)
#    sigmaW=max(sigmas)
#    for p in dataPlotters:
#        p.addCorrectionFactor(1.0/sigmaW,'flat')
data=MergedPlotter(dataPlotters)


fcorr=ROOT.TFile(options.res)
scale_x=fcorr.Get("scalexHisto")
scale_y=fcorr.Get("scaleyHisto")
res_x=fcorr.Get("resxHisto")
res_y=fcorr.Get("resyHisto")


variables=options.vars.split(',')


ptBins=[0,150,200,250,300,350,400,450,500,550,600,700,800,900,1000,1500,2000,5000]
binsx=[]
for i in range(0,options.binsx+1):
    binsx.append(options.minx+i*(options.maxx-options.minx)/options.binsx)

binsy=[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,140.,150.,160.,180.,210.]    


###Make res up and down
resUp = ROOT.TH1F(res_x)
resUp.SetName("resUp")
for i in range(1,res_x.GetNbinsX()+1):
    resUp.SetBinContent(i,res_x.GetBinContent(i)+0.3)


scaleUp = ROOT.TH1F(scale_x)
scaleUp.SetName("scaleUp")
scaleDown = ROOT.TH1F(scale_x)
scaleDown.SetName("scaleDown")
for i in range(1,scale_x.GetNbinsX()+1):
    scaleUp.SetBinContent(i,scale_x.GetBinContent(i)+0.09)
    scaleDown.SetBinContent(i,scale_x.GetBinContent(i)-0.09)






ptBins=[200,300,400,500,600,700,800,1000,1500,2000,3000,5000]

###Make pt spectrum
#print 'Making W Pt spectra for reweighting'
#wptNominal=data.drawTH1Binned("lnujj_l1_pt","lnujj_LV_mass>600",'1',ptBins)
#wptUp=data.drawTH1Binned("1.3*lnujj_l1_pt","lnujj_LV_mass>600",'1',ptBins)
#wptDown=data.drawTH1Binned("0.7*lnujj_l1_pt","lnujj_LV_mass>600&&(0.7*lnujj_l1_pt)>200",'1',ptBins)
#wptNominal.Scale(1.0/wptNominal.Integral())
#wptUp.Scale(1.0/wptUp.Integral())
#wptDown.Scale(1.0/wptDown.Integral())
#wptUp.Divide(wptNominal)
#wptDown.Divide(wptNominal)

#print 'Making  Pt spectra for reweighting'
#ptNominal=data.drawTH1Binned("lnujj_l2_gen_pt","lnujj_LV_mass>600",'1',ptBins)
#ptUp=data.drawTH1Binned("1.3*lnujj_l2_gen_pt","lnujj_LV_mass>600",'1',ptBins)
#ptDown=data.drawTH1Binned("0.7*lnujj_l2_gen_pt","lnujj_LV_mass>600&&(0.7*lnujj_l2_gen_pt)>100",'1',ptBins)
#ptNominal.Scale(1.0/ptNominal.Integral())
#ptUp.Scale(1.0/ptUp.Integral())
#ptDown.Scale(1.0/ptDown.Integral())
#ptUp.Divide(ptNominal)
#ptDown.Divide(ptNominal)



#print 'Making quark gluon spectra for reweighting'
#partonFlavour=data.drawTH1Binned("lnujj_l2_partonFlavour",options.cut,'1',[0.,20.,22])
#quarkGluonUp=data.drawTH1Binned("lnujj_l2_partonFlavour",options.cut,'1',[0.,20.,22])
#quarkGluonDown=data.drawTH1Binned("lnujj_l2_partonFlavour",options.cut,'1',[0.,20.,22])
#partonFlavour.Scale(1.0/partonFlavour.Integral())
#quarkGluonUp.Scale(1.0/quarkGluonUp.Integral())
#quarkGluonDown.Scale(1.0/quarkGluonDown.Integral())
#quarks=partonFlavour.GetBinContent(1)
#offset=1
#quarkGluonUp.SetBinContent(1,quarkGluonUp.GetBinContent(1)*(1+offset))
#quarkGluonUp.SetBinContent(2,1-quarkGluonUp.GetBinContent(1))
#offset=-1
#quarkGluonDown.SetBinContent(1,quarkGluonDown.GetBinContent(1)*(1+offset))
#quarkGluonDown.SetBinContent(2,1-quarkGluonDown.GetBinContent(1))
#quarkGluonUp.Divide(partonFlavour)
#quarkGluonDown.Divide(partonFlavour)
#
#print 'Making Tail spectra for reweighting'
#tailSyst=0.0012
#tailUp=ROOT.TH1F("tailUp","tailUp",100,400,10000)
#tailDown=ROOT.TH1F("tailDown","tailDown",100,400,10000)
#for i in range(1,tailUp.GetNbinsX()+1):
#    x=tailUp.GetXaxis().GetBinCenter(i)
#    if x<2500:
#        tailUp.SetBinContent(i,1.0)
#        tailDown.SetBinContent(i,1.0)
#    else:
#        tailUp.SetBinContent(i,exp(tailSyst*(x-2500)))
#        tailDown.SetBinContent(i,1/tailUp.GetBinContent(i))





histogram=ROOT.TH2F("histo","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_top_up=ROOT.TH2F("histo_TOPUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_top_down=ROOT.TH2F("histo_TOPDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

histogram_scale_up=ROOT.TH2F("histo_ScaleUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_scale_down=ROOT.TH2F("histo_ScaleDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

histogram_res_up=ROOT.TH2F("histo_ResUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
#histogram_res_down=ROOT.TH2F("histo_ResDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

#histogram_qg_up=ROOT.TH2F("histo_GluonUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
#histogram_qg_down=ROOT.TH2F("histo_GluonDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
#histogram_tail_up=ROOT.TH2F("histo_TailUp","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
#histogram_tail_down=ROOT.TH2F("histo_TailDown","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

#systs

histograms=[
    histogram,
#    histogram_pt_up,
#    histogram_pt_down,
    histogram_top_up,
    histogram_top_down,
    histogram_scale_up,
    histogram_scale_down,
#    histogram_scaleLog_up,
#    histogram_scaleLog_down,
    histogram_res_up,
#    histogram_res_down,
#    histogram_qg_up,
#    histogram_qg_down,
#    histogram_tail_up,
#    histogram_tail_down,
]

#ok lets populate!




for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):
    histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
    norm=histI.Integral()

    #nominal
    histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
    dataset=plotter.makeDataSet('lnujj_l1_pt,lnujj_l2_gen_pt,'+variables[1]+','+variables[0],options.cut,-1)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'lnujj_l2_gen_pt',scale_x,scale_y,res_x,res_y,histTMP);
    if histTMP.Integral()>0:
        #histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram.Add(histTMP)

        #TOP UP/DOWN
        if "TT" in plotterNW.filename:
            histogram_top_up.Add(histTMP,2.0)
            histogram_top_down.Add(histTMP,0.5)
        else:

            histogram_top_up.Add(histTMP)
            histogram_top_down.Add(histTMP)

    histTMP.Delete()




    #remove the factor you added:

    #resUp
    histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
    datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'lnujj_l2_gen_pt',scale_x,scale_y,resUp,res_y,histTMP);
    if histTMP.Integral()>0:
        #histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_res_up.Add(histTMP)
    histTMP.Delete()



    #scale up
    histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
    datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'lnujj_l2_gen_pt',scaleUp,scale_y,res_x,res_y,histTMP);
    if histTMP.Integral()>0:
        #histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_scale_up.Add(histTMP)
    histTMP.Delete()

    #scale down
    histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
    datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'lnujj_l2_gen_pt',scaleDown,scale_y,res_x,res_y,histTMP);
    if histTMP.Integral()>0:
        #histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_scale_down.Add(histTMP)
    histTMP.Delete()
    histI.Delete()





f=ROOT.TFile(options.output,"RECREATE")
f.cd()

finalHistograms={}
for hist in histograms:
    hist.Write(hist.GetName()+"_coarse")
    smoothTail(hist)
    hist.Write(hist.GetName()+"_coarsesmoothed")
    conditional(hist)
    hist.Write(hist.GetName()+"_coarsesmoothedcond")
    expanded=expandHisto(hist,options)
    expanded.Write(hist.GetName()+"_expanded")
    conditional(expanded)
    expanded.Write()
    finalHistograms[hist.GetName()]=expanded

histogram_pt_down,histogram_pt_up=unequalScale(finalHistograms['histo'],"histo_PT",1.5/5000)
conditional(histogram_pt_down)
histogram_pt_down.Write()
conditional(histogram_pt_up)
histogram_pt_up.Write()



h1,h2=unequalScale(finalHistograms['histo'],"histo_OPT",1.5*800,-1)
conditional(h1)
h1.Write()
conditional(h2)
h2.Write()

h1,h2=unequalScale(finalHistograms['histo'],"histo_PT2",5*5000*5000,2)
conditional(h1)
h1.Write()
conditional(h2)
h2.Write()


##special treatment for mirroring
''' ###FIXME: bug with empty bins
histogram_res_down=mirror(finalHistograms['histo_ResUp'],finalHistograms['histo'],"histo_ResDown")
conditional(histogram_res_down)
histogram_res_down.Write()
'''


#ptUp.Write("ptUp")
#ptDown.Write("ptDown")
#wptUp.Write("wptUp")
#wptDown.Write("wptDown")

scaleUp.Write("scaleUp")
scaleDown.Write("scaleDown")
#resUp.Write("resUp")

#resDown.Write("resDown")

#quarkGluonUp.Write("qgUp")
#quarkGluonDown.Write("qgDwn")
#tailUp.Write("tailUp")
#tailDown.Write("tailDown")

f.Close()




