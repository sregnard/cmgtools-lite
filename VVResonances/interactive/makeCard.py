import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",type=int,default=2016,help="2016 or 2017 or 2018")
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
  intlumi = 59970


sig=options.signalType
if sig not in ['XWW','XWZ','XWH']:
    sys.exit('Error: unrecognized signal')


categories = []
if options.categories == 'old':
    categories = ['nob']
elif options.categories == 'bb':
    categories = ['bb','nobb']
#elif options.categories == 'charge':
#    categories = ['Wplus','Wminus']



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
                card.addMJJSignalParametricShape(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+purity+"_"+category+".json",{'CMS_scale_prunedj_'+YEAR:1},{'CMS_res_prunedj_'+YEAR:1.0})
            else:
                card.addMJJSignalParametricShapeNOEXP(sig+"_MJJ",varMJJ,inputDir+"LNuJJ_"+sig+"_MJJ_"+purity+"_"+category+".json",{'CMS_scale_prunedj_'+YEAR:1},{'CMS_res_prunedj_'+YEAR:1.0})
            card.product(sig,sig+"_MJJ",sig+"_MVV")

            if purity=='HP':
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence'+YEAR,'log(MH/600)',0.041)
            else:
                card.addParametricYieldWithUncertainty(sig,0,inputDir+"LNuJJ_"+sig+"_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence'+YEAR,'((0.054/0.041)*(-log(MH/600)))',0.041)


            ## Non-resonant bkgd
            nonResTag ="_".join([lepton,purity,category,YEAR])
            rootFile=inputDir+"LNuJJ_nonRes_2D_"+lepton+"_"+purity+"_"+category+".root"
#            card.addHistoShapeFromFile("nonRes",[varMVV,varMJJ],rootFile,"histo",['OPTX:CMS_VV_LNuJ_nonRes_OPTX_'+nonResTag,'PTX:CMS_VV_LNuJ_nonRes_PTX_'+nonResTag,'PTX2:CMS_VV_LNuJ_nonRes_PTX2_'+nonResTag,'PTY:CMS_VV_LNuJ_nonRes_PTY_'+nonResTag,'OPTY:CMS_VV_LNuJ_nonRes_OPTY_'+nonResTag],False,0)
            card.addHistoShapeFromFile("nonRes",[varMVV,varMJJ],rootFile,"histo",['PTX:CMS_VV_LNuJ_nonRes_PTX_'+nonResTag,'OPTX:CMS_VV_LNuJ_nonRes_OPTX_'+nonResTag,'OPTY:CMS_VV_LNuJ_nonRes_OPTY_'+nonResTag,'PTY:CMS_VV_LNuJ_nonRes_PTY_'+nonResTag],False,0)
            
            card.addFixedYieldFromFile("nonRes",1,inputDir+"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","nonRes")


            ## Resonant bkgd
            resWTag ="_".join([lepton,purity,category,YEAR])

            rootFile=inputDir+"LNuJJ_resW_MJJGivenMVV_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("mjjRes",[varMVV,varMJJ],rootFile,"histo",['Scale:CMS_scale_prunedj_'+YEAR,'Res:CMS_res_prunedj_'+YEAR,'TopPt0:CMS_VV_topPt_0_'+resWTag,'TopPt1:CMS_VV_topPt_1_'+resWTag],True,0)

            rootFile=inputDir+"LNuJJ_resW_MVV_"+lepton+"_"+purity+"_"+category+".root"
            card.addHistoShapeFromFile("resW_MVV",[varMVV],rootFile,"histo",['PT:CMS_VV_LNuJ_resW_PT_'+resWTag,'OPT:CMS_VV_LNuJ_resW_OPT_'+resWTag],False,0)

            card.conditionalProduct("resW","mjjRes",varMVV,"resW_MVV")
            card.addFixedYieldFromFile("resW",2,inputDir+"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","resW")


            ## DATA
            card.importBinnedData(inputDir+"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","data",[varMVV,varMJJ])



            ## SYSTEMATICS

            #luminosity
            card.addSystematic("CMS_lumi_"+YEAR,"lnN",{'XWW':1.026,'XWZ':1.026,'XWH':1.026})

            #kPDF uncertainty for the signal
            card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01,'XWH':1.01})

            #lepton efficiency
            card.addSystematic("CMS_eff_"+lepton+"_"+YEAR,"lnN",{'XWW':1.1,'XWZ':1.1,'XWH':1.1})

            #bkgd normalization
            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+nonResTag,"lnN",{'nonRes':1.5})
            card.addSystematic("CMS_VV_LNuJ_resW_norm_"+resWTag,"lnN",{'resW':1.20})

            #tau21 
            if purity=='HP':
                card.addSystematic("CMS_VV_LNuJ_tau21_eff_"+YEAR,"lnN",{'XWW':1+0.14,'XWZ':1+0.14,'XWH':1+0.14})
            if purity=='LP':
                card.addSystematic("CMS_VV_LNuJ_tau21_eff_"+YEAR,"lnN",{'XWW':1-0.33,'XWZ':1-0.33,'XWH':1-0.33})

            card.addSystematic("CMS_btag_fake_"+YEAR,"lnN",{'XWW':1+0.02,'XWZ':1+0.02,'XWH':1+0.02})


            card.addSystematic("CMS_scale_j_"+YEAR,"param",[0.0,0.02])
            card.addSystematic("CMS_res_j_"+YEAR,"param",[0.0,0.05])
            card.addSystematic("CMS_scale_prunedj_"+YEAR,"param",[0.0,0.333])
            card.addSystematic("CMS_res_prunedj_"+YEAR,"param",[0.0,0.333])
            card.addSystematic("CMS_scale_MET_"+YEAR,"param",[0.0,0.02])
            card.addSystematic("CMS_res_MET_"+YEAR,"param",[0.0,0.01])
            if lepton=='e':
                card.addSystematic("CMS_scale_e_"+YEAR,"param",[0.0,0.005])
            elif lepton=='mu':
                card.addSystematic("CMS_scale_mu_"+YEAR,"param",[0.0,0.003])

            card.addSystematic("CMS_VV_LNuJ_nonRes_PTX_"+nonResTag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_OPTX_"+nonResTag,"param",[0.0,0.333])
#            card.addSystematic("CMS_VV_LNuJ_nonRes_ScaleY_"+nonResTag,"param",[0.0,333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_PTY_"+nonResTag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_nonRes_OPTY_"+nonResTag,"param",[0.0,0.6])

            card.addSystematic("CMS_VV_LNuJ_resW_PT_"+resWTag,"param",[0.0,0.333])
            card.addSystematic("CMS_VV_LNuJ_resW_OPT_"+resWTag,"param",[0.0,0.333])
            card.addSystematic('CMS_VV_topPt_0_'+resWTag,"param",[0.0,0.333])
            card.addSystematic('CMS_VV_topPt_1_'+resWTag,"param",[0.0,0.333])


            card.makeCard()


##make combined cards
print cmd
            
