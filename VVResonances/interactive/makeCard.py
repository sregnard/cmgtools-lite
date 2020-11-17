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

HPunc = 0.04
LPunc = 0.04
bbuncWW = 0.09
bbuncWZ = 0.09
bbuncWH = 0.06
nobbuncWW = 0.004
nobbuncWZ = 0.015
nobbuncWH = 0.025

inCR = options.region=="CR"
sfx_rgn = "_CR" if inCR else ""

sfx_year = "_"+YEAR if YEAR!="Run2" else ""

sig=options.signalType
if sig not in ['GbuToWW','RadToWW','ZprToWW','WprToWZ','WprToWH','VBFGbuToWW','VBFRadToWW','VBFZprToWW','VBFWprToWZ','VBFWprToWH']:
    sys.exit('Error: unrecognized signal')




for lepton in ['e','mu']:
    for purity in ['HP','LP']:
        for category in ['bb','nobb','vbf']:
            for dy in ['LDy','HDy']:

                card=DataCardMaker(lepton,purity,YEAR,intlumi,category+"_"+dy)
                cat='_'.join([lepton,purity,category,dy,YEAR])
                cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '


                varMVV = "MLNuJ"
                varMJJ = "MJ"
                if options.differentBinning and category in ['bb','vbf']:
                    varMVV = "MLNuJ_coarse"
                    varMJJ = "MJ_coarse"


                PCEtag = "_".join([purity,category,dy])
                LPCEtag = "_".join([lepton,purity,category,dy])
                LYtag = "_".join([lepton,YEAR])
                PYtag = "_".join([purity,YEAR])
                PCEYtag = "_".join([purity,category,dy,YEAR])
                LPCEYtag = "_".join([lepton,purity,category,dy,YEAR])

                ## Signal
                card.addMVVSignalParametricShape(sig+"_MVV",varMVV,inputDir+"LNuJJ_"+sig+"_MVV_"+PCEtag+".json",{'CMS_scale_j_'+YEAR:1,'CMS_scale_MET_'+YEAR:1.0,'CMS_scale_'+LYtag:1.0},{'CMS_res_j_'+YEAR:1.0,'CMS_res_MET_'+YEAR:1.0})
                if purity=='LP':
                    card.addMJJSignalParametricShape(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+PCEtag+".json",{'CMS_scale_prunedj_WPeak_'+PYtag:'0.05'},{'CMS_res_prunedj_WPeak_'+PYtag:'0.25'})
                else:
                    card.addMJJSignalParametricShapeNOEXP(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+PCEtag+".json",{'CMS_scale_prunedj_WPeak_'+PYtag:'0.05'},{'CMS_res_prunedj_WPeak_'+PYtag:'0.25'})
                card.product(sig,sig+"_MJJ",sig+"_MVV")

                if purity=='HP':
                    card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+LPCEtag+"_yield.json",1,'CMS_Vtag_PtDependence_'+YEAR,'(4.95e-5*(MH-650))',1.)
                else:
                    card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+LPCEtag+"_yield.json",1,'CMS_Vtag_PtDependence_'+YEAR,'(-3.54e-5*(MH-650))',1.)


                ## Non-resonant bkgd
                rootFile=inputDir+"LNuJJ_nonRes"+sfx_rgn+"_2D_"+LPCEtag+".root"
                card.addHistoShapeFromFile("nonRes",[varMVV,varMJJ],rootFile,"histo",['MVVScale:CMS_VV_LNuJ_nonRes_MVVScale_'+LPCEYtag,'Diag:CMS_VV_LNuJ_nonRes_Diag_'+LPCEYtag,'logWeight:CMS_VV_LNuJ_nonRes_logWeight_'+LPCEYtag,'MJJScale:CMS_VV_LNuJ_nonRes_MJJScale_'+LPCEYtag],False,0)

                card.addFixedYieldFromFile("nonRes",1,inputDir+"LNuJJ_norm"+sfx_rgn+"_"+LPCEtag+".root","nonRes"+sfx_rgn)


                ## Resonant bkgd
                rootFile=inputDir+"LNuJJ_res"+sfx_rgn+"_2D_"+LPCEtag+".root"
                card.addHistoShapeFromFile("res",[varMVV,varMJJ],rootFile,"histo",['MVVScale:CMS_VV_LNuJ_res_MVVScale_'+LPCEYtag,'Diag:CMS_VV_LNuJ_res_Diag_'+LPCEYtag,'scaleWY:CMS_scale_prunedj_WPeak_'+PYtag,'resWY:CMS_res_prunedj_WPeak_'+PYtag,'scaleTopY:CMS_scale_prunedj_TopPeak_'+PYtag,'resTopY:CMS_res_prunedj_TopPeak_'+PYtag,'fractionY:CMS_VV_LNuJ_res_fractionY_'+LPCEYtag],False,0)

                card.addFixedYieldFromFile("res",1,inputDir+"LNuJJ_norm"+sfx_rgn+"_"+LPCEtag+".root","res"+sfx_rgn)

                ## DATA
                card.importBinnedData(inputDir+"LNuJJ_norm"+sfx_rgn+"_"+LPCEtag+".root","data"+sfx_rgn+sfx_year,[varMVV,varMJJ])


                ## SYSTEMATICS

                ## luminosity
                card.addSystematic("CMS_lumi_"+YEAR,"lnN",{'GbuToWW':1.018,'RadToWW':1.018,'ZprToWW':1.018,'WprToWZ':1.018,'WprToWH':1.018,'VBFGbuToWW':1.018,'VBFRadToWW':1.018,'VBFZprToWW':1.018,'VBFWprToWZ':1.018,'VBFWprToWH':1.018})

                ## PDF
                card.addSystematic("CMS_pdf","lnN",{'GbuToWW':1.01,'RadToWW':1.01,'ZprToWW':1.01,'WprToWZ':1.01,'WprToWH':1.01,'VBFGbuToWW':1.01,'VBFRadToWW':1.01,'VBFZprToWW':1.01,'VBFWprToWZ':1.01,'VBFWprToWH':1.01})

                ## pileup reweighting (from shifting the min-bias cross section)
                card.addSystematic("CMS_puWeight_"+YEAR,"lnN",{'GbuToWW':1.015,'RadToWW':1.015,'ZprToWW':1.015,'WprToWZ':1.015,'WprToWH':1.015,'VBFGbuToWW':1.015,'VBFRadToWW':1.015,'VBFZprToWW':1.015,'VBFWprToWZ':1.015,'VBFWprToWH':1.015})

                ## lepton efficiency
                card.addSystematic("CMS_eff_"+LYtag,"lnN",{'GbuToWW':1.05,'RadToWW':1.05,'ZprToWW':1.05,'WprToWZ':1.05,'WprToWH':1.05,'VBFGbuToWW':1.05,'VBFRadToWW':1.05,'VBFZprToWW':1.05,'VBFWprToWZ':1.05,'VBFWprToWH':1.05})

                ## b tagging fake rate
                card.addSystematic("CMS_btag_fake_"+YEAR,"lnN",{'GbuToWW':1.02,'RadToWW':1.02,'ZprToWW':1.02,'WprToWZ':1.02,'WprToWH':1.02,'VBFGbuToWW':1.02,'VBFRadToWW':1.02,'VBFZprToWW':1.02,'VBFWprToWZ':1.02,'VBFWprToWH':1.02})

                ## V tagging
                if purity=='HP':
                    card.addSystematic("CMS_VV_LNuJ_Vtag_eff_"+YEAR,"lnN",{'GbuToWW':1+HPunc,'RadToWW':1+HPunc,'ZprToWW':1+HPunc,'WprToWZ':1+HPunc,'WprToWH':1+HPunc,'VBFGbuToWW':1+HPunc,'VBFRadToWW':1+HPunc,'VBFZprToWW':1+HPunc,'VBFWprToWZ':1+HPunc,'VBFWprToWH':1+HPunc})
                if purity=='LP':
                    card.addSystematic("CMS_VV_LNuJ_Vtag_eff_"+YEAR,"lnN",{'GbuToWW':1-LPunc,'RadToWW':1-LPunc,'ZprToWW':1-LPunc,'WprToWZ':1-LPunc,'WprToWH':1-LPunc,'VBFGbuToWW':1-LPunc,'VBFRadToWW':1-LPunc,'VBFZprToWW':1-LPunc,'VBFWprToWZ':1-LPunc,'VBFWprToWH':1-LPunc})

                ## bb tagging
                if category=='bb':
                    card.addSystematic("CMS_VV_LNuJ_bbtag_eff_"+YEAR,"lnN",{'GbuToWW':1+bbuncWW,'RadToWW':1+bbuncWW,'ZprToWW':1+bbuncWW,'WprToWZ':1+bbuncWZ,'WprToWH':1+bbuncWH,'VBFGbuToWW':1+bbuncWW,'VBFRadToWW':1+bbuncWW,'VBFZprToWW':1+bbuncWW,'VBFWprToWZ':1+bbuncWZ,'VBFWprToWH':1+bbuncWH})
                if category=='nobb':
                    card.addSystematic("CMS_VV_LNuJ_bbtag_eff_"+YEAR,"lnN",{'GbuToWW':1-nobbuncWW,'RadToWW':1-nobbuncWW,'ZprToWW':1-nobbuncWW,'WprToWZ':1-nobbuncWZ,'WprToWH':1-nobbuncWH,'VBFGbuToWW':1-nobbuncWW,'VBFRadToWW':1-nobbuncWW,'VBFZprToWW':1-nobbuncWW,'VBFWprToWZ':1-nobbuncWZ,'VBFWprToWH':1-nobbuncWH})

                ## Dy tagging
                if dy=='LDy':
                    card.addSystematic("CMS_VV_Dy_"+YEAR,"lnN",{'GbuToWW':0.985,'RadToWW':0.965,'ZprToWW':0.965,'WprToWZ':0.98,'WprToWH':0.98,'VBFGbuToWW':0.95,'VBFRadToWW':0.965,'VBFZprToWW':0.945,'VBFWprToWZ':0.945,'VBFWprToWH':0.945})
                if dy=='HDy':
                    card.addSystematic("CMS_VV_Dy_"+YEAR,"lnN",{'GbuToWW':1.04 ,'RadToWW':1.04 ,'ZprToWW':1.04 ,'WprToWZ':1.04,'WprToWH':1.04,'VBFGbuToWW':1.06,'VBFRadToWW':1.04 ,'VBFZprToWW':1.02 ,'VBFWprToWZ':1.02 ,'VBFWprToWH':1.02 })

                ## background normalization
                #card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+LPCEYtag,"lnN",{'nonRes':1.25})
                #card.addSystematic("CMS_VV_LNuJ_res_norm_"+LPCEYtag,"lnN",{'res':1.25})
                card.addSystematic("CMS_VV_LNuJ_bkg_norm_"+LYtag,"lnN",{'nonRes':1.05,'res':1.05})
                card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+PCEYtag,"lnN",{'nonRes':1.25})
                card.addSystematic("CMS_VV_LNuJ_res_norm_"+PCEYtag,"lnN",{'res':1.25})

                ## shapes
                card.addSystematic("CMS_scale_j_"+YEAR,"param",[0.0,0.02])
                card.addSystematic("CMS_res_j_"+YEAR,"param",[0.0,0.05])
                card.addSystematic("CMS_scale_MET_"+YEAR,"param",[0.0,0.02])
                card.addSystematic("CMS_res_MET_"+YEAR,"param",[0.0,0.01])
                if lepton=='e':
                    card.addSystematic("CMS_scale_e_"+YEAR,"param",[0.0,0.005])
                elif lepton=='mu':
                    card.addSystematic("CMS_scale_mu_"+YEAR,"param",[0.0,0.003])

                card.addSystematic("CMS_VV_LNuJ_nonRes_MVVScale_"+LPCEYtag,"param",[0.0,0.333])
                card.addSystematic("CMS_VV_LNuJ_nonRes_Diag_"+LPCEYtag,"param",[0.0,0.333])
                card.addSystematic("CMS_VV_LNuJ_nonRes_logWeight_"+LPCEYtag,"param",[0.0,0.333])
                #card.addSystematic("CMS_VV_LNuJ_nonRes_SD_"+LPCEYtag,"param",[0.0,0.333])
                card.addSystematic("CMS_VV_LNuJ_nonRes_MJJScale_"+LPCEYtag,"param",[0.0,0.333])
                #card.addSystematic("CMS_VV_LNuJ_nonRes_OPTY_"+LPCEYtag,"param",[0.0,0.333])


                card.addSystematic("CMS_VV_LNuJ_res_MVVScale_"+LPCEYtag,"param",[0.0,0.333])
                card.addSystematic("CMS_VV_LNuJ_res_Diag_"+LPCEYtag,"param",[0.0,0.333])
                card.addSystematic("CMS_VV_LNuJ_res_fractionY_"+LPCEYtag,"param",[0.0,0.333])

                card.addSystematic("CMS_scale_prunedj_WPeak_"+PYtag,"param",[-0.22,0.2]) ## central value: -1.1%, uncertainty: +-1%
                card.addSystematic("CMS_res_prunedj_WPeak_"+PYtag,"param",[0.32,0.32]) ## central value: +8%, uncertainty: +-8%
                card.addSystematic("CMS_scale_prunedj_TopPeak_"+PYtag,"param",[0.0,0.2]) ## central value not rescaled, uncertainty: +-1%
                card.addSystematic("CMS_res_prunedj_TopPeak_"+PYtag,"param",[0.0,0.32]) ## central value not rescaled, uncertainty: +-8%
                card.makeCard()


##make combined cards
print cmd
