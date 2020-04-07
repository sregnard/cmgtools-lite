import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '


for category in ['nob','b']:
    if category=='vbf':
        pur=['NP']
    else:
        pur=['HP','LP']
    for purity in pur:
        for lepton in ['e','mu']:
            card=DataCardMaker(lepton,purity,'13TeV',35900,category)
            cat='_'.join([category,lepton,purity,'13TeV'])
            cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '

            #WW signal-MVV
            card.addMVVSignalParametricShape("XWW","MLNuJ","LNuJJ_XWW_MVV_"+lepton+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
            card.addParametricYieldWithUncertainty("XWW",0,"LNuJJ_XWW_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
#            card.addMVVSignalParametricShape("XWZ","MLNuJ","LNuJJ_XWZ_MVV_"+lepton+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
#            card.addParametricYieldWithUncertainty("XWZ",0,"LNuJJ_XWZ_"+lepton+"_"+purity+"_"+category+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)


            rootFile="LNuJJ_"+lepton+"_"+purity+"_"+category+".root"
            qcdTag ="_".join([lepton,purity,category])

            card.addHistoShapeFromFile("nonRes",["MLNuJ"],rootFile,"nonRes",["shape_nonRes:shape_nonRes"+qcdTag],False,0)        
#            card.addHistoShapeFromFile("nonRes",["MLNuJ"],rootFile,"nonRes",[],False,0)        
            card.addFixedYieldFromFile("nonRes",1,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","nonRes")



            card.addHistoShapeFromFile("resW",["MLNuJ"],rootFile,"resW",["shape_resW:shape_resW"+qcdTag],False,0)        
 #           card.addHistoShapeFromFile("resW",["MLNuJ"],rootFile,"resW",[],False,0)        
            card.addFixedYieldFromFile("resW",1,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","resW")

            card.importBinnedData(rootFile,"data",["MLNuJ"])

            #luminosity
            card.addSystematic("CMS_lumi","lnN",{'XWW':1.026,'XWZ':1.026})

            #kPDF uncertainty for the signal
            card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01})

            #lepton efficiency
            card.addSystematic("CMS_eff_"+lepton,"lnN",{'XWW':1.1,'XWZ':1.1})

            #W+jets cross section in acceptance-dominated by pruned mass
            card.addSystematic("CMS_VV_LNuJ_nonRes_norm_"+lepton+"_"+purity+"_"+category,"lnN",{'nonRes':1.3})
            card.addSystematic("CMS_VV_LNuJ_resW_norm_"+lepton+"_"+purity+"_"+category,"lnN",{'resW':1.20})
            #tau21 
            if purity=='HP':
                card.addSystematic("CMS_VV_LNuJ_tau21_eff","lnN",{'XWW':1+0.14,'XWZ':1+0.14})

            if purity=='LP':
                card.addSystematic("CMS_VV_LNuJ_tau21_eff","lnN",{'XWW':1-0.33,'XWZ':1-0.33})
            card.addSystematic("CMS_btag_fake","lnN",{'XWW':1+0.02,'XWZ':1+0.02})


            card.addSystematic("shape_nonRes"+qcdTag,"param",[0.0,0.333])
            card.addSystematic("shape_resW"+qcdTag,"param",[0.0,0.333])

               
            #pruned mass scale    
            card.addSystematic("CMS_scale_j","param",[0.0,0.02])
            card.addSystematic("CMS_res_j","param",[0.0,0.05])
            card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
            card.makeCard()

#make combined cards



print cmd
            
