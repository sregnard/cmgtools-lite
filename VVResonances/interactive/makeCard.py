import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",type=int,default=2016,help="2016 or 2017 or 2018 or Run2")
parser.add_option("-s","--signalType",dest="signalType",default='XWW',help="XWW or XWZ or XWH")
parser.add_option("-c","--cat",dest="categories",default='bb',help="categorization scheme")
parser.add_option("-b","--differentBinning",action="store_true",dest="differentBinning",help="use other binning for bb category",default=False)
(options,args) = parser.parse_args()


YEAR=str(options.year)
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


            ## Signal
            card.addMVVSignalParametricShape(sig+"_MVV",varMVV,inputDir+"LNuJJ_"+sig+"_MVV_"+purity+"_"+category+".json",{'CMS_scale_j_'+YEAR:1,'CMS_scale_MET_'+YEAR:1.0,'CMS_scale_'+lepton+'_'+YEAR:1.0},{'CMS_res_j_'+YEAR:1.0,'CMS_res_MET_'+YEAR:1.0})
            if purity=='LP':
                card.addMJJSignalParametricShape(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+purity+"_"+category+".json",{'CMS_scale_prunedj_'+YEAR:0.0094},{'CMS_res_prunedj_'+YEAR:0.2}) 
            else:
                card.addMJJSignalParametricShapeNOEXP(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+purity+"_"+category+".json",{'CMS_scale_prunedj_'+YEAR:0.0094},{'CMS_res_prunedj_'+YEAR:0.2})
            card.product(sig,sig+"_MJJ",sig+"_MVV")

            if purity=='HP':
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence'+YEAR,'log(MH/600)',0.041)
            else:
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence'+YEAR,'((0.054/0.041)*(-log(MH/600)))',0.041)


            ## Non-resonant bkgd
            nonResTag ="_".join([lepton,purity,category,YEAR])
            rootFile=inputDir+"LNuJJ_nonRes_2D_"+lepton+"_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("nonRes",[varMVV,varMJJ],rootFile,"histo",['GPTX:CMS_VV_LNuJ_nonRes_GPT_'+nonResTag,'GPT2X:CMS_VV_LNuJ_nonRes_GPT2_'+nonResTag,'SDY:CMS_VV_LNuJ_nonRes_SD_'+nonResTag],False,0)
            
            card.addFixedYieldFromFile("nonRes",1,inputDir+"LNuJJ_norm_"+lepton+"_"+purity+"_"+category+".root","nonRes")


            ## Resonant bkgd
            resWTag ="_".join([lepton,purity,category,YEAR])

            rootFile=inputDir+"LNuJJ_resW_MJJGivenMVV_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("mjjRes",[varMVV,varMJJ],rootFile,"histo",['Scale:CMS_scale_prunedj_'+YEAR,'Res:CMS_res_prunedj_'+YEAR,'TopPt0:CMS_VV_topPt_0_'+resWTag,'TopPt1:CMS_VV_topPt_1_'+resWTag],True,0)

            rootFile=inputDir+"LNuJJ_resW_MVV_"+lepton+"_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("resW_MVV",[varMVV],rootFile,"histo",['GPT:CMS_VV_LNuJ_resW_GPT_'+resWTag,'GPT2:CMS_VV_LNuJ_resW_GPT2_'+resWTag],False,0)

            card.conditionalProduct("resW","mjjRes",varMVV,"resW_MVV")
            card.addFixedYieldFromFile("resW",2,inputDir+"LNuJJ_norm_"+lepton+"_"+purity+"_"+category+".root","resW")


            ## DATA
            card.importBinnedData(inputDir+"LNuJJ_norm_"+lepton+"_"+purity+"_"+category+".root","data",[varMVV,varMJJ])



            ## SYSTEMATICS

            #luminosity
            card.addSystematic("CMS_lumi_"+YEAR,"lnN",{'XWW':1.026,'XWZ':1.026,'XWH':1.026})

            #kPDF uncertainty for the signal
            card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01,'XWH':1.01})

            #lepton efficiency
            card.addSystematic("CMS_eff_"+lepton+"_"+YEAR,"lnN",{'XWW':1.1,'XWZ':1.1,'XWH':1.1})

            #bkgd normalization
            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+nonResTag,"lnN",{'nonRes':1.5})
            card.addSystematic("CMS_VV_LNuJ_resW_norm_"+resWTag,"lnN",{'resW':1.5})

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
            card.addSystematic("CMS_scale_prunedj_"+YEAR,"param",[0.0,1.0]) ## /!\ A magnitude of 0.0094 is hardcoded above for the signal, and in the template maker for resW
            card.addSystematic("CMS_res_prunedj_"+YEAR,"param",[0.0,1.0]) ## /!\ A magnitude of 0.2 is hardcoded above for the signal, and in the template maker for resW
            card.addSystematic("CMS_scale_MET_"+YEAR,"param",[0.0,0.02])
            card.addSystematic("CMS_res_MET_"+YEAR,"param",[0.0,0.01])
            if lepton=='e':
                card.addSystematic("CMS_scale_e_"+YEAR,"param",[0.0,0.005])
            elif lepton=='mu':
                card.addSystematic("CMS_scale_mu_"+YEAR,"param",[0.0,0.003])

            card.addSystematic("CMS_VV_LNuJ_nonRes_GPT_"+nonResTag,"param",[0.0,1.0])
            card.addSystematic("CMS_VV_LNuJ_nonRes_GPT2_"+nonResTag,"param",[0.0,1.0])
            card.addSystematic("CMS_VV_LNuJ_nonRes_SD_"+nonResTag,"param",[0.0,0.5])

            card.addSystematic("CMS_VV_LNuJ_resW_GPT_"+resWTag,"param",[0.0,1.0])
            card.addSystematic("CMS_VV_LNuJ_resW_GPT2_"+resWTag,"param",[0.0,1.0])
            card.addSystematic('CMS_VV_topPt_0_'+resWTag,"param",[0.0,1.0]) ## /!\ A magnitude of 0.2 is hardcoded in the template maker
            card.addSystematic('CMS_VV_topPt_1_'+resWTag,"param",[0.0,1.0]) ## /!\ A magnitude of 25000.0/MVV^2 is hardcoded in the template maker


            card.makeCard()


##make combined cards
print cmd
            
