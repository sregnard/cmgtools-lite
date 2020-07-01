import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

import optparse
parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default="Run2",help="2016 or 2017 or 2018 or Run2")
(options,args) = parser.parse_args()


YEAR=options.year
inputDir='Inputs_'+YEAR+'/'
intlumi=35920+41530+59740
inCR = True
sfx_rgn = "CR" if inCR else ""
sfx_year = "_"+YEAR if YEAR!="Run2" else ""


for lepton in ['allL']: #['e','mu']:
    for purity in ['HP','LP','NP']:
        for category in ['allC']: #['bb','nobb']:

            card=DataCardMaker(lepton,purity,YEAR,intlumi,category)
            cat='_'.join([category,lepton,purity,YEAR])
            cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '


            varMJJ = "MJ"


            PCtag = "_".join([purity,category])
            PYtag = "_".join([purity,YEAR])
            LPCtag = "_".join([lepton,purity,category])
            PCYtag = "_".join([purity,category,YEAR])
            LPCYtag = "_".join([lepton,purity,category,YEAR])


            rootFile=inputDir+"LNuJJ_res"+sfx_rgn+"_MJJ_"+LPCtag+".root"
            print(rootFile)
            card.addHistoShapeFromFile("W",[varMJJ],rootFile,"W",['scale:scale','sigma:sigma'],False,0)            
#            card.addFixedYieldFromFile("W",0,rootFile,"res"+sfx_rgn)
            card.addVTagSFCustomYield("W",0,
                                      inputDir+"LNuJJ_res"+sfx_rgn+"_MJJ_"+lepton+"_HP_"+category+".root",
                                      inputDir+"LNuJJ_res"+sfx_rgn+"_MJJ_"+lepton+"_LP_"+category+".root",
                                      inputDir+"LNuJJ_res"+sfx_rgn+"_MJJ_"+lepton+"_NP_"+category+".root",
                                      purity)
            ## Non-resonant bkgd
            card.addHistoShapeFromFile("bkg",[varMJJ],rootFile,"bkg",['scale:bkgShape0_'+LPCYtag,'sigma:bkgShape1_'+LPCYtag,'slope:bkgShape2_'+LPCYtag,'fT:bkgShape3_'+LPCYtag,'fE:bkgShape4_'+LPCYtag],False,0)            
            card.addFixedYieldFromFile("bkg",1,rootFile,"bkg")

            #DATA
            card.importBinnedData(inputDir+"LNuJJ_norm_"+LPCtag+".root","data"+sfx_rgn,[varMJJ])
            ## SYSTEMATICS
            card.addSystematic("bkgNorm_"+LPCtag,"lnN",{'bkg':1.20})

            card.addSystematic('scale',"param",[0.0,0.333])
            card.addSystematic('sigma',"param",[0.0,0.333])
            
            card.addSystematic('bkgShape0_'+LPCYtag,"param",[0.0,0.333])
            card.addSystematic('bkgShape1_'+LPCYtag,"param",[0.0,0.333])
            card.addSystematic('bkgShape2_'+LPCYtag,"param",[0.0,0.333])
            card.addSystematic('bkgShape3_'+LPCYtag,"param",[0.0,0.333])
            card.addSystematic('bkgShape4_'+LPCYtag,"param",[0.0,0.333])
            card.makeCard()


##make combined cards
print cmd
            
