import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="Run2",help="2016 or 2017 or 2018 or Run2")
parser.add_option("-s","--signalType",dest="signalType",default='GbuToWW',help="signal type")
parser.add_option("-b","--differentBinning",action="store_true",dest="differentBinning",help="use other binning for bb category",default=True)
parser.add_option("-r","--region",dest="region",default='SR',help="signal region (SR) or control region (CR)")
(options,args) = parser.parse_args()


YEAR=options.year
inputDir='Inputs_Run2/'
intlumi=0.
if YEAR=="2016":
  intlumi = 35920
elif YEAR=="2017":
  intlumi = 41530
elif YEAR=="2018":
  intlumi = 59740
elif YEAR=="Run2":
  intlumi=35920+41530+59740

HPunc = 0.03
LPunc = 0.03

inCR = options.region=="CR"
sfx_rgn = "_CR" if inCR else ""

sfx_year = "_"+YEAR if YEAR!="Run2" else ""

sig=options.signalType
if sig not in ['GbuToWW','RadToWW','ZprToWW','WprToWZ','WprToWH','VBFGbuToWW','VBFRadToWW','VBFZprToWW','VBFWprToWZ']:
    sys.exit('Error: unrecognized signal')




for lepton in ['e','mu']:
    for purity in ['HP','LP']:
        for category in ['bb','nobb','vbf']:

            card=DataCardMaker(lepton,purity,YEAR,intlumi,category)
            cat='_'.join([category,lepton,purity,YEAR])
            cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '


            varMVV = "MLNuJ"
            varMJJ = "MJ"
            if options.differentBinning and category in ['bb','vbf']:
                varMVV = "MLNuJ_coarse"
                varMJJ = "MJ_coarse"


            PCtag = "_".join([purity,category])
            PYtag = "_".join([purity,YEAR])
            LPCtag = "_".join([lepton,purity,category])
            PCYtag = "_".join([purity,category,YEAR])
            LPCYtag = "_".join([lepton,purity,category,YEAR])

            ## Signal
            card.addMVVSignalParametricShape(sig+"_MVV",varMVV,inputDir+"LNuJJ_"+sig+"_MVV_"+PCtag+".json",{'CMS_scale_j_'+YEAR:1,'CMS_scale_MET_'+YEAR:1.0,'CMS_scale_'+lepton+'_'+YEAR:1.0},{'CMS_res_j_'+YEAR:1.0,'CMS_res_MET_'+YEAR:1.0})
            if purity=='LP':
                card.addMJJSignalParametricShape(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+PCtag+".json",{'CMS_scale_prunedj_WPeak_'+PYtag:'0.05'},{'CMS_res_prunedj_WPeak_'+PYtag:'0.25'})
            else:
                card.addMJJSignalParametricShapeNOEXP(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+PCtag+".json",{'CMS_scale_prunedj_WPeak_'+PYtag:'0.05'},{'CMS_res_prunedj_WPeak_'+PYtag:'0.25'})
            card.product(sig,sig+"_MJJ",sig+"_MVV")

            if purity=='HP':
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+LPCtag+"_yield.json",1,'CMS_Vtag_PtDependence_'+YEAR,'(4.95e-5*(MH-650))',1.)
            else:
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+LPCtag+"_yield.json",1,'CMS_Vtag_PtDependence_'+YEAR,'(-3.54e-5*(MH-650))',1.)


            ## Non-resonant bkgd
            rootFile=inputDir+"LNuJJ_nonRes"+sfx_rgn+"_2D_"+LPCtag+".root"
            card.addHistoShapeFromFile("nonRes",[varMVV,varMJJ],rootFile,"histo",['MVVScale:CMS_VV_LNuJ_nonRes_MVVScale_'+LPCYtag,'Diag:CMS_VV_LNuJ_nonRes_Diag_'+LPCYtag,'logWeight:CMS_VV_LNuJ_nonRes_logWeight_'+LPCYtag,'MJJScale:CMS_VV_LNuJ_nonRes_MJJScale_'+LPCYtag],False,0)

            card.addFixedYieldFromFile("nonRes",1,inputDir+"LNuJJ_norm"+sfx_rgn+"_"+LPCtag+".root","nonRes"+sfx_rgn)


            ##resonant bkgd
            rootFile=inputDir+"LNuJJ_res"+sfx_rgn+"_2D_"+LPCtag+".root"
            card.addHistoShapeFromFile("res",[varMVV,varMJJ],rootFile,"histo",['MVVScale:CMS_VV_LNuJ_res_MVVScale_'+LPCYtag,'Diag:CMS_VV_LNuJ_res_Diag_'+LPCYtag,'scaleWY:CMS_scale_prunedj_WPeak_'+PYtag,'resWY:CMS_res_prunedj_WPeak_'+PYtag,'scaleTopY:CMS_scale_prunedj_TopPeak_'+PYtag,'resTopY:CMS_res_prunedj_TopPeak_'+PYtag,'fractionY:CMS_VV_LNuJ_res_fractionY_'+LPCYtag],False,0)

            card.addFixedYieldFromFile("res",1,inputDir+"LNuJJ_norm"+sfx_rgn+"_"+LPCtag+".root","res"+sfx_rgn)

            #DATA
            card.importBinnedData(inputDir+"LNuJJ_norm"+sfx_rgn+"_"+LPCtag+".root","data"+sfx_rgn+sfx_year,[varMVV,varMJJ])


            ## SYSTEMATICS

            ## luminosity
            card.addSystematic("CMS_lumi_"+YEAR,"lnN",{'XWW':1.018,'XWZ':1.018,'XWH':1.018,'VBFXWW':1.018})

            ## PDF
            card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01,'XWH':1.01,'VBFXWW':1.01})

            ## pileup reweighting (from shifting the min-bias cross section)
            card.addSystematic("CMS_puWeight_"+YEAR,"lnN",{'XWW':1.015,'XWZ':1.015,'XWH':1.015,'VBFXWW':1.015})

            ## lepton efficiency
            card.addSystematic("CMS_eff_"+lepton+"_"+YEAR,"lnN",{'XWW':1.05,'XWZ':1.05,'XWH':1.05,'VBFXWW':1.05})

            ## efficiency of the pt/m cut
            card.addSystematic("CMS_eff_ptom_"+YEAR,"lnN",{'XWW':1.025,'XWZ':1.025,'XWH':1.025,'VBFXWW':1.05})

            ## b tagging fake rate
            card.addSystematic("CMS_btag_fake_"+YEAR,"lnN",{'XWW':1+0.02,'XWZ':1+0.02,'XWH':1+0.02,'VBFXWW':1+0.02})

            ## V tagging
            if purity=='HP':
                card.addSystematic("CMS_VV_LNuJ_Vtag_eff_"+YEAR,"lnN",{'XWW':1+HPunc,'XWZ':1+HPunc,'XWH':1+HPunc,'VBFXWW':1+HPunc})
            if purity=='LP':
                card.addSystematic("CMS_VV_LNuJ_Vtag_eff_"+YEAR,"lnN",{'XWW':1-LPunc,'XWZ':1-LPunc,'XWH':1-LPunc,'VBFXWW':1-LPunc})

            ## bb tagging
            if category=='bb':
                card.addSystematic("CMS_VV_LNuJ_bbtag_eff_"+YEAR,"lnN",{'XWW':1+0.09,'XWZ':1+0.09,'XWH':1+0.06,'VBFXWW':1+0.09})
            if category=='nobb':
                card.addSystematic("CMS_VV_LNuJ_bbtag_eff_"+YEAR,"lnN",{'XWW':1-0.004,'XWZ':1-0.015,'XWH':1-0.02,'VBFXWW':1-0.004})

            ## background normalization

#            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+lepton+"_"+purity+"_"+category+"_"+YEAR,"lnN",{'nonRes':1.25})

            card.addSystematic("CMS_VV_LNuJ_bkg_norm_"+lepton+"_"+YEAR,"lnN",{'nonRes':1.05,'res':1.05})
            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+purity+"_"+category+"_"+YEAR,"lnN",{'nonRes':1.25})

#            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+purity+"_"+YEAR,"lnN",{'nonRes':1.15})
#            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+category+"_"+YEAR,"lnN",{'nonRes':1.15})


#            card.addSystematic("CMS_VV_LNuJ_res_norm_"+lepton+"_"+purity+"_"+category+"_"+YEAR,"lnN",{'res':1.25})
            card.addSystematic("CMS_VV_LNuJ_res_norm_"+purity+"_"+category+"_"+YEAR,"lnN",{'res':1.25})
#            card.addSystematic("CMS_VV_LNuJ_res_norm_"+lepton+"_"+YEAR,"lnN",{'res':1.05})
#            card.addSystematic("CMS_VV_LNuJ_res_norm_"+purity+"_"+YEAR,"lnN",{'res':1.15})
#            card.addSystematic("CMS_VV_LNuJ_res_norm_"+category+"_"+YEAR,"lnN",{'res':1.15})

            ## shapes
            card.addSystematic("CMS_scale_j_"+YEAR,"param",[0.0,0.02])
            card.addSystematic("CMS_res_j_"+YEAR,"param",[0.0,0.05])
            card.addSystematic("CMS_scale_MET_"+YEAR,"param",[0.0,0.02])
            card.addSystematic("CMS_res_MET_"+YEAR,"param",[0.0,0.01])
            if lepton=='e':
                card.addSystematic("CMS_scale_e_"+YEAR,"param",[0.0,0.005])
            elif lepton=='mu':
                card.addSystematic("CMS_scale_mu_"+YEAR,"param",[0.0,0.003])

            card.addSystematic("CMS_VV_LNuJ_nonRes_MVVScale_"+LPCYtag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_Diag_"+LPCYtag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_logWeight_"+LPCYtag,"param",[0.0,0.333])
#            card.addSystematic("CMS_VV_LNuJ_nonRes_SD_"+LPCYtag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_MJJScale_"+LPCYtag,"param",[0.0,0.333])
#            card.addSystematic("CMS_VV_LNuJ_nonRes_OPTY_"+LPCYtag,"param",[0.0,0.333])


            card.addSystematic("CMS_VV_LNuJ_res_MVVScale_"+LPCYtag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_res_Diag_"+LPCYtag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_res_fractionY_"+LPCYtag,"param",[0.0,0.333])

            card.addSystematic("CMS_scale_prunedj_WPeak_"+PYtag,"param",[-0.22,0.2]) ## central value: -1.1%, uncertainty: +-1%
            card.addSystematic("CMS_res_prunedj_WPeak_"+PYtag,"param",[0.32,0.32]) ## central value: +8%, uncertainty: +-8%
            card.addSystematic("CMS_scale_prunedj_TopPeak_"+PYtag,"param",[0.0,0.2]) ## central value not rescaled, uncertainty: +-1%
            card.addSystematic("CMS_res_prunedj_TopPeak_"+PYtag,"param",[0.0,0.32]) ## central value not rescaled, uncertainty: +-8%
            card.makeCard()


##make combined cards
print cmd
