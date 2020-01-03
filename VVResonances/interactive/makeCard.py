import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="2016",help="2016 or 2017 or 2018 or Run2")
parser.add_option("-s","--signalType",dest="signalType",default='XWW',help="XWW or XWZ or XWH")
parser.add_option("-c","--cat",dest="categories",default='bb',help="categorization scheme")
parser.add_option("-b","--differentBinning",action="store_true",dest="differentBinning",help="use other binning for bb category",default=False)
(options,args) = parser.parse_args()


YEAR=options.year
inputDir='Inputs_'+YEAR+'/'
intlumi=0.
if YEAR=="2016":
  intlumi = 35920
elif YEAR=="2017":
  intlumi = 41530
elif YEAR=="2018":
  intlumi = 59740
elif YEAR=="Run2":
  intlumi=35920+41530+59740

if YEAR=="2016": ## TBU with new WP
  HPunc = 0.14
  LPunc = 0.33
elif YEAR=="2017" or YEAR=="2018": ## TBU for 2018
  HPunc = 0.06
  LPunc = 0.29
elif YEAR=="Run2": ## TBU with an uncertainty for the 3 years together
  HPunc = 0.14
  LPunc = 0.33

## TBU
bbunc = 0.07
nobbunc = 0.07



sig=options.signalType
if sig not in ['XWW','XWZ','XWH']:
    sys.exit('Error: unrecognized signal')


categories = []
if options.categories == 'old':
    categories = ['nob']
elif options.categories == 'bb':
    categories = ['bb','nobb']



for category in categories:
    for purity in ['HP','LP']:
        for lepton in ['e','mu']:

            card=DataCardMaker(lepton,purity,YEAR,intlumi,category)
            cat='_'.join([category,lepton,purity,YEAR])
            cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '


            varMVV = "MLNuJ"
            varMJJ = "MJ"
            if options.differentBinning and category=='bb':
                varMVV = "MLNuJ_coarse"
                varMJJ = "MJ_coarse"


            PCYtag = "_".join([purity,category,YEAR])
            LPCYtag = "_".join([lepton,purity,category,YEAR])

            ## Signal
            card.addMVVSignalParametricShape(sig+"_MVV",varMVV,inputDir+"LNuJJ_"+sig+"_MVV_"+purity+"_"+category+".json",{'CMS_scale_j_'+YEAR:1,'CMS_scale_MET_'+YEAR:1.0,'CMS_scale_'+lepton+'_'+YEAR:1.0},{'CMS_res_j_'+YEAR:1.0,'CMS_res_MET_'+YEAR:1.0})
            if purity=='LP':
                card.addMJJSignalParametricShape(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+purity+"_"+category+".json",{'CMS_scale0_prunedj_WPeak_'+PCYtag:'3*0.01','CMS_scale1_prunedj_WPeak_'+PCYtag:'3*10.0/MH'},{'CMS_res0_prunedj_WPeak_'+PCYtag:'3*0.2','CMS_res1_prunedj_WPeak_'+PCYtag:'3*200.0/MH'})
            else:
                card.addMJJSignalParametricShapeNOEXP(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+purity+"_"+category+".json",{'CMS_scale0_prunedj_WPeak_'+PCYtag:'3*0.01','CMS_scale1_prunedj_WPeak_'+PCYtag:'3*10.0/MH'},{'CMS_res0_prunedj_WPeak_'+PCYtag:'3*0.2','CMS_res1_prunedj_WPeak_'+PCYtag:'3*200.0/MH'})
            card.product(sig,sig+"_MJJ",sig+"_MVV")

            if purity=='HP':
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence_'+YEAR,'log(MH/600)',0.041)
            else:
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence_'+YEAR,'((0.054/0.041)*(-log(MH/600)))',0.041)


            ## Non-resonant bkgd
            rootFile=inputDir+"LNuJJ_nonRes_2D_"+lepton+"_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("nonRes",[varMVV,varMJJ],rootFile,"histo",['GPTX:CMS_VV_LNuJ_nonRes_GPT_'+LPCYtag,'GPT2X:CMS_VV_LNuJ_nonRes_GPT2_'+LPCYtag,'SDY:CMS_VV_LNuJ_nonRes_SD_'+LPCYtag],False,0)
            
            card.addFixedYieldFromFile("nonRes",1,inputDir+"LNuJJ_norm_"+lepton+"_"+purity+"_"+category+".root","nonRes")


            ## Resonant W bkgd
            rootFile=inputDir+"LNuJJ_resW_MJJGivenMVV_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("resW_MJJ",[varMVV,varMJJ],rootFile,"histo",['Scale0:CMS_scale0_prunedj_WPeak_'+PCYtag,'Scale1:CMS_scale1_prunedj_WPeak_'+PCYtag,'Res0:CMS_res0_prunedj_WPeak_'+PCYtag,'Res1:CMS_res1_prunedj_WPeak_'+PCYtag],True,0)

            rootFile=inputDir+"LNuJJ_resW_MVV_"+lepton+"_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("resW_MVV",[varMVV],rootFile,"histo",['GPT:CMS_VV_LNuJ_resW_GPT_'+LPCYtag,'GPT2:CMS_VV_LNuJ_resW_GPT2_'+LPCYtag],False,0)

            card.conditionalProduct("resW","resW_MJJ",varMVV,"resW_MVV")
            card.addFixedYieldFromFile("resW",2,inputDir+"LNuJJ_norm_"+lepton+"_"+purity+"_"+category+".root","resW")


            ## Resonant Top bkgd
            rootFile=inputDir+"LNuJJ_resTop_MJJGivenMVV_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("resTop_MJJ",[varMVV,varMJJ],rootFile,"histo",['Scale0:CMS_scale0_prunedj_TopPeak_'+PCYtag,'Scale1:CMS_scale1_prunedj_TopPeak_'+PCYtag,'Res0:CMS_res0_prunedj_TopPeak_'+PCYtag,'Res1:CMS_res1_prunedj_TopPeak_'+PCYtag],True,0)

            rootFile=inputDir+"LNuJJ_resTop_MVV_"+lepton+"_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("resTop_MVV",[varMVV],rootFile,"histo",['GPT:CMS_VV_LNuJ_resTop_GPT_'+LPCYtag,'GPT2:CMS_VV_LNuJ_resTop_GPT2_'+LPCYtag],False,0)

            card.conditionalProduct("resTop","resTop_MJJ",varMVV,"resTop_MVV")
            card.addFixedYieldFromFile("resTop",2,inputDir+"LNuJJ_norm_"+lepton+"_"+purity+"_"+category+".root","resTop")


            ## DATA
            card.importBinnedData(inputDir+"LNuJJ_norm_"+lepton+"_"+purity+"_"+category+".root","data",[varMVV,varMJJ])



            ## SYSTEMATICS

            #luminosity
            card.addSystematic("CMS_lumi_"+YEAR,"lnN",{'XWW':1.026,'XWZ':1.026,'XWH':1.026})

            #kPDF uncertainty for the signal
            card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01,'XWH':1.01})

            #lepton efficiency
            card.addSystematic("CMS_eff_"+lepton+"_"+YEAR,"lnN",{'XWW':1.05,'XWZ':1.05,'XWH':1.05,'resW':1.05,'resTop':1.05})
            card.addSystematic("CMS_effWJets_"+lepton+"_"+YEAR,"lnN",{'nonRes':1.05})

            #bkgd normalization
            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+PCYtag,"lnN",{'nonRes':1.5})
            card.addSystematic("CMS_VV_LNuJ_resW_norm_"+PCYtag,"lnN",{'resW':1.5})
            card.addSystematic("CMS_VV_LNuJ_resTop_norm_"+PCYtag,"lnN",{'resTop':1.5})

            #V tagging
            if purity=='HP':
                card.addSystematic("CMS_VV_LNuJ_Vtag_eff_"+YEAR,"lnN",{'XWW':1+HPunc,'XWZ':1+HPunc,'XWH':1+HPunc})
            if purity=='LP':
                card.addSystematic("CMS_VV_LNuJ_Vtag_eff_"+YEAR,"lnN",{'XWW':1-LPunc,'XWZ':1-LPunc,'XWH':1-LPunc})

            #bb tagging 
            if category=='bb':
                card.addSystematic("CMS_VV_LNuJ_bbtag_eff_"+YEAR,"lnN",{'XWW':1+bbunc,'XWZ':1+bbunc,'XWH':1+bbunc})
            if category=='nobb':
                card.addSystematic("CMS_VV_LNuJ_bbtag_eff_"+YEAR,"lnN",{'XWW':1-nobbunc,'XWZ':1-nobbunc,'XWH':1-nobbunc})

            card.addSystematic("CMS_btag_fake_"+YEAR,"lnN",{'XWW':1+0.02,'XWZ':1+0.02,'XWH':1+0.02})


            #shapes
            card.addSystematic("CMS_scale_j_"+YEAR,"param",[0.0,0.02])
            card.addSystematic("CMS_res_j_"+YEAR,"param",[0.0,0.05])
            card.addSystematic("CMS_scale_MET_"+YEAR,"param",[0.0,0.02])
            card.addSystematic("CMS_res_MET_"+YEAR,"param",[0.0,0.01])
            if lepton=='e':
                card.addSystematic("CMS_scale_e_"+YEAR,"param",[0.0,0.005])
            elif lepton=='mu':
                card.addSystematic("CMS_scale_mu_"+YEAR,"param",[0.0,0.003])

            card.addSystematic("CMS_VV_LNuJ_nonRes_GPT_"+LPCYtag,"param",[0.0,1.0])#0.333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_GPT2_"+LPCYtag,"param",[0.0,1.0])#0.333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_SD_"+LPCYtag,"param",[0.0,0.5])

            card.addSystematic("CMS_VV_LNuJ_resW_GPT_"+LPCYtag,"param",[0.0,1.0])#0.333])
            card.addSystematic("CMS_VV_LNuJ_resW_GPT2_"+LPCYtag,"param",[0.0,1.0])#0.333])
            
            card.addSystematic("CMS_VV_LNuJ_resTop_GPT_"+LPCYtag,"param",[0.0,1.0])#0.333])
            card.addSystematic("CMS_VV_LNuJ_resTop_GPT2_"+LPCYtag,"param",[0.0,1.0])#0.333])

            card.addSystematic("CMS_scale0_prunedj_WPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker for the bkgd, and above for the signal
            card.addSystematic("CMS_res0_prunedj_WPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker the bkgd, and above for the signal
            card.addSystematic("CMS_scale1_prunedj_WPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker the bkgd, and above for the signal
            card.addSystematic("CMS_res1_prunedj_WPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker the bkgd, and above for the signal
            card.addSystematic("CMS_scale0_prunedj_TopPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker
            card.addSystematic("CMS_res0_prunedj_TopPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker
            card.addSystematic("CMS_scale1_prunedj_TopPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker
            card.addSystematic("CMS_res1_prunedj_TopPeak_"+PCYtag,"param",[0.0,0.333]) ## /!\ Magnitude hardcoded in the template maker

            card.makeCard()


##make combined cards
print cmd
            
