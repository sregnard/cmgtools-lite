import ROOT
import os, sys
from DoubleBscalefactors import *
from DoubleBefficiencies import *

#import optparse
#parser = optparse.OptionParser()
#parser.add_option("-y","--year",dest="year",type=int,default=2016,help="2016 or 2017 or 2018")
#(options,args) = parser.parse_args()
#
#if options.year not in [2016,2017,2018]:
#    parser.error("year must be 2016, 2017, or 2018")
#YEAR=options.year

DODATA= 1
DOMC  =1

###############################################
###############################################
#################  PARAMETERS  ################
###############################################
###############################################



ntuples='ntuples'


tau21SF={ ## Run2 values
    'HP' : '1',
    'LP' : '1',
    'allP' : '1',
    'NP' : '1',
    'fullP' : '1',
    }

bbSFWW_2016 = DoubleBsf_M2_B_80X
bbSFWZ_2016 = DoubleBsf_M2_B_80X
bbSFWH_2016 = DoubleBsf_M2_S_80X
#bbSFupWW_2016 = DoubleBsf_M2_B_80X_up
#bbSFupWZ_2016 = DoubleBsf_M2_B_80X_up
#bbSFupWH_2016 = DoubleBsf_M2_S_80X_up
#bbSFdnWW_2016 = DoubleBsf_M2_B_80X_dn
#bbSFdnWZ_2016 = DoubleBsf_M2_B_80X_dn
#bbSFdnWH_2016 = DoubleBsf_M2_S_80X_dn
bbEffWW_2016 = EffMC_M2_XWW_2016
bbEffWZ_2016 = EffMC_M2_XWZ_2016
bbEffWH_2016 = EffMC_M2_XWH_2016
bbSFWW_2017 = DoubleBsf_M2_B_94X
bbSFWZ_2017 = DoubleBsf_M2_B_94X
bbSFWH_2017 = DoubleBsf_M2_S_94X
#bbSFupWW_2017 = DoubleBsf_M2_B_94X_up
#bbSFupWZ_2017 = DoubleBsf_M2_B_94X_up
#bbSFupWH_2017 = DoubleBsf_M2_S_94X_up
#bbSFdnWW_2017 = DoubleBsf_M2_B_94X_dn
#bbSFdnWZ_2017 = DoubleBsf_M2_B_94X_dn
#bbSFdnWH_2017 = DoubleBsf_M2_S_94X_dn
bbEffWW_2017 = EffMC_M2_XWW_2017
bbEffWZ_2017 = EffMC_M2_XWZ_2017
bbEffWH_2017 = EffMC_M2_XWH_2017
bbSFWW_2018 = DoubleBsf_M2_B_102X
bbSFWZ_2018 = DoubleBsf_M2_B_102X
bbSFWH_2018 = DoubleBsf_M2_S_102X
#bbSFupWW_2018 = DoubleBsf_M2_B_102X_up
#bbSFupWZ_2018 = DoubleBsf_M2_B_102X_up
#bbSFupWH_2018 = DoubleBsf_M2_S_102X_up
#bbSFdnWW_2018 = DoubleBsf_M2_B_102X_dn
#bbSFdnWZ_2018 = DoubleBsf_M2_B_102X_dn
#bbSFdnWH_2018 = DoubleBsf_M2_S_102X_dn
bbEffWW_2018 = EffMC_M2_XWW_2018
bbEffWZ_2018 = EffMC_M2_XWZ_2018
bbEffWH_2018 = EffMC_M2_XWH_2018
bbWgtWW={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWW_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2016[ptcut])+')/(1-'+str(bbEffWW_2016[ptcut])+'))') for ptcut,sf in bbSFWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2017[ptcut])+')/(1-'+str(bbEffWW_2017[ptcut])+'))') for ptcut,sf in bbSFWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2018[ptcut])+')/(1-'+str(bbEffWW_2018[ptcut])+'))') for ptcut,sf in bbSFWW_2018))+'))',
    'vbf' : '1',
    'allC': '1',
    }
bbWgtWZ={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWZ_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2016[ptcut])+')/(1-'+str(bbEffWZ_2016[ptcut])+'))') for ptcut,sf in bbSFWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2017[ptcut])+')/(1-'+str(bbEffWZ_2017[ptcut])+'))') for ptcut,sf in bbSFWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2018[ptcut])+')/(1-'+str(bbEffWZ_2018[ptcut])+'))') for ptcut,sf in bbSFWZ_2018))+'))',
    'vbf' : '1',
    'allC': '1',
    }
bbWgtWH={
    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFWH_2018))+'))',
    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2016[ptcut])+')/(1-'+str(bbEffWH_2016[ptcut])+'))') for ptcut,sf in bbSFWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2017[ptcut])+')/(1-'+str(bbEffWH_2017[ptcut])+'))') for ptcut,sf in bbSFWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2018[ptcut])+')/(1-'+str(bbEffWH_2018[ptcut])+'))') for ptcut,sf in bbSFWH_2018))+'))',
    'vbf' : '1', 
    'allC': '1',
    }
#bbWgtWW_up={
#    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWW_2018))+'))',
#    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2016[ptcut])+')/(1-'+str(bbEffWW_2016[ptcut])+'))') for ptcut,sf in bbSFupWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2017[ptcut])+')/(1-'+str(bbEffWW_2017[ptcut])+'))') for ptcut,sf in bbSFupWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2018[ptcut])+')/(1-'+str(bbEffWW_2018[ptcut])+'))') for ptcut,sf in bbSFupWW_2018))+'))',
#    'vbf': '1',
#    'allC': '1',
#    }
#bbWgtWZ_up={
#    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWZ_2018))+'))',
#    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2016[ptcut])+')/(1-'+str(bbEffWZ_2016[ptcut])+'))') for ptcut,sf in bbSFupWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2017[ptcut])+')/(1-'+str(bbEffWZ_2017[ptcut])+'))') for ptcut,sf in bbSFupWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2018[ptcut])+')/(1-'+str(bbEffWZ_2018[ptcut])+'))') for ptcut,sf in bbSFupWZ_2018))+'))',
#    'vbf': '1',
#    'allC': '1',
#    }
#bbWgtWH_up={
#    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFupWH_2018))+'))',
#    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2016[ptcut])+')/(1-'+str(bbEffWH_2016[ptcut])+'))') for ptcut,sf in bbSFupWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2017[ptcut])+')/(1-'+str(bbEffWH_2017[ptcut])+'))') for ptcut,sf in bbSFupWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2018[ptcut])+')/(1-'+str(bbEffWH_2018[ptcut])+'))') for ptcut,sf in bbSFupWH_2018))+'))',
#    'vbf': '1',
#    'allC': '1',
#    }
#bbWgtWW_dn={
#    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWW_2018))+'))',
#    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2016[ptcut])+')/(1-'+str(bbEffWW_2016[ptcut])+'))') for ptcut,sf in bbSFdnWW_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2017[ptcut])+')/(1-'+str(bbEffWW_2017[ptcut])+'))') for ptcut,sf in bbSFdnWW_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWW_2018[ptcut])+')/(1-'+str(bbEffWW_2018[ptcut])+'))') for ptcut,sf in bbSFdnWW_2018))+'))',
#    'vbf': '1',
#    'allC': '1',
#    }
#bbWgtWZ_dn={
#    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWZ_2018))+'))',
#    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2016[ptcut])+')/(1-'+str(bbEffWZ_2016[ptcut])+'))') for ptcut,sf in bbSFdnWZ_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2017[ptcut])+')/(1-'+str(bbEffWZ_2017[ptcut])+'))') for ptcut,sf in bbSFdnWZ_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWZ_2018[ptcut])+')/(1-'+str(bbEffWZ_2018[ptcut])+'))') for ptcut,sf in bbSFdnWZ_2018))+'))',
#    'vbf': '1',
#    'allC': '1',
#    }
#bbWgtWH_dn={
#    'bb'   : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*'+str(sf)) for ptcut,sf in bbSFdnWH_2018))+'))',
#    'nobb' : '((year==2016)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2016[ptcut])+')/(1-'+str(bbEffWH_2016[ptcut])+'))') for ptcut,sf in bbSFdnWH_2016))+')  +  (year==2017)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2017[ptcut])+')/(1-'+str(bbEffWH_2017[ptcut])+'))') for ptcut,sf in bbSFdnWH_2017))+')  +  (year==2018)*('+('+'.join((ptcut.replace('pt','lnujj_l2_pt')+'*((1-'+str(sf)+'*'+str(bbEffWH_2018[ptcut])+')/(1-'+str(bbEffWH_2018[ptcut])+'))') for ptcut,sf in bbSFdnWH_2018))+'))',
#    'vbf': '1',
#    'allC': '1',
#    }
#print bbWgtWW['bb']
#print bbWgtWW['nobb']


lumi16=35920
lumi17=41530
lumi18=59740
lumiTotal=lumi16+lumi17+lumi18
lumiWeight2016="("+str(lumi16)+"/"+str(lumiTotal)+")"
lumiWeight2017="("+str(lumi17)+"/"+str(lumiTotal)+")"
lumiWeight2018="("+str(lumi18)+"/"+str(lumiTotal)+")"


cuts={}

cuts['common'] = '1'
#cuts['common'] = cuts['common'] + '*(HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET||HLT_PHOTON)' ## FIXME: HLT flags are temporarily handled via pcuts
cuts['common'] = cuts['common'] + '*((run>500) + (run<500)*lnujj_sfWV)'
cuts['common'] = cuts['common'] + '*(lnujj_nOtherLeptons==0&&nlljj==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>0)'
cuts['common'] = cuts['common'] + '*(Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&(Flag_eeBadScFilter*(run>500)+(run<500))&&(Flag_BadMuonFilter*(year==2016)+Flag_BadPFMuonFilter*(year!=2016)))'

## exclude 2018 events where the selected electron is in the problematic HEM15/16 region:
cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&abs(lnujj_l1_l_pdgId)==11&&(-1.55<lnujj_l1_l_phi)&&(lnujj_l1_l_phi<-0.9)&&(-2.5<lnujj_l1_l_eta)&&(lnujj_l1_l_eta<-1.479)))'
## exclude 2018 events where the selected V jet is in the problematic HEM15/16 region:
cuts['common'] = cuts['common'] + '*(!(year==2018&&run>=319077&&(-1.55<lnujj_l2_phi)&&(lnujj_l2_phi<-0.9)&&(-2.5<lnujj_l2_eta)&&(lnujj_l2_eta<-1.479)))'
## new cut on pT/M:
cuts['common'] = cuts['common'] + '*(lnujj_l1_pt/lnujj_LV_mass>0.4&&lnujj_l2_pt/lnujj_LV_mass>0.4)'
## lumi-based reweighting for MC:
cuts['common'] = cuts['common'] + '*( (run>500) + (run<500)*((year==2016)*'+lumiWeight2016+'+(year==2017)*'+lumiWeight2017+'+(year==2018)*'+lumiWeight2018+') )'

cuts['nob'] = '(lnujj_nMediumBTags==0)'
cuts['b'] = '(lnujj_nMediumBTags>0)'
cuts['CR'] = cuts['common'] + '*' + cuts['b'] + '*lnujj_btagWeight'
cuts['common'] = cuts['common'] + '*' + cuts['nob'] + '*lnujj_btagWeight'

cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['allL'] = '(abs(lnujj_l1_l_pdgId)==11||abs(lnujj_l1_l_pdgId)==13)'
leptons=['allL'] #['e','mu']
leptonsMerged=['allL']

Vtagger='(lnujj_l2_tau2/lnujj_l2_tau1-(-0.08)*log(lnujj_l2_softDrop_mass*lnujj_l2_softDrop_mass/lnujj_l2_pt))'
thrHP='0.50'
thrLP='0.80'
cuts['HP'] = '('+Vtagger+'<'+thrHP+')'
cuts['LP'] = '('+thrHP+'<='+Vtagger+'&&'+Vtagger+'<'+thrLP+')'
cuts['allP'] = '('+cuts['HP']+'||'+cuts['LP']+')'
cuts['NP'] = '('+thrLP+'<='+Vtagger+')'
cuts['fullP'] = '('+cuts['HP']+'||'+cuts['LP']+'||'+cuts['NP']+')'
purities=['HP','LP','NP'] #,'allP','fullP']
puritiesMerged=['allP']

bbtag='(lnujj_l2_btagBOOSTED>0.8)'
cuts['bb'] = bbtag+'*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'
cuts['nobb'] = '(!'+bbtag+')'+'*(!(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500))'
cuts['allC'] = '1'
cuts['vbf'] = '(lnujj_nJets>=2&&lnujj_vbfDEta>4.0&&lnujj_vbfMass>500)'
categories=['allC'] #['bb','nobb','vbf']
categoriesMerged=['allC']


#cuts['resW']  ='(lnujj_l2_mergedVTruth==1&&!(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'
#cuts['resTop']='(lnujj_l2_mergedVTruth==1&&(lnujj_l2_nearestBDRTruth<0.8&&lnujj_l2_gen_b_pt/(lnujj_l2_gen_qq_pt+lnujj_l2_gen_b_pt)>0.1&&lnujj_l2_gen_softDrop_mass>100))'
cuts['res']   ='(lnujj_l2_mergedVTruth==1)'
cuts['nonres']='(lnujj_l2_mergedVTruth==0)'



## get resonant yield from CR:
renormRes = {
'mu': {
        'HP':{'nobb':0.96,'bb':0.96,'vbf':0.96},
        'LP':{'nobb':0.88,'bb':0.79,'vbf':0.88},
      },
'e': {
        'HP':{'nobb':0.96,'bb':0.96,'vbf':0.96},
        'LP':{'nobb':0.88,'bb':0.81,'vbf':0.88},
      },
}

## get non-resonant MVV slope from CR (also hardcoded in vvMake2DTemplateWithKernels.py):
renormNonResMvvSlope = {
    'HP':{'nobb':-2.1e-4, 'bb':-2.65e-4,'vbf':-2.1e-4 },
    'LP':{'nobb':-2.57e-4,'bb':-2.61e-4,'vbf':-2.57e-4},
}

ptbin={}
ptbin['Low']="(lnujj_LV_mass>600&&lnujj_LV_mass<800)"
ptbin['Mid']="(lnujj_LV_mass>800&&lnujj_LV_mass<1000)"
ptbin['High']="(lnujj_LV_mass>1000&&lnujj_LV_mass<1500)"


allMCTemplate={}

allMCTemplate['Run2'] = "ntuples2016/TT_pow_pythia,ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2016/WWToLNuQQ,ntuples2017/WWToLNuQQ,ntuples2018/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2017/WZTo1L1Nu2Q,ntuples2018/WZTo1L1Nu2Q,ntuples2016/ZZTo2L2Q,ntuples2017/ZZTo2L2Q,ntuples2018/ZZTo2L2Q,ntuples2016/T_tW,ntuples2017/T_tW,ntuples2018/T_tW,ntuples2016/TBar_tW,ntuples2017/TBar_tW,ntuples2018/TBar_tW,ntuples2016/WJetsToLNu_HT,ntuples2017/WJetsToLNu_HT,ntuples2018/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT,ntuples2017/DYJetsToLL_M50_HT,ntuples2018/DYJetsToLL_M50_HT"

allMCTemplate['2016'] = "ntuples2016/TT_pow_pythia,ntuples2016/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2016/ZZTo2L2Q,ntuples2016/T_tW,ntuples2016/TBar_tW,ntuples2016/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT"

#allMCTemplate['2016'] = "ntuples2016/TT_pow_herwig,ntuples2016/WWToLNuQQ,ntuples2016/WZTo1L1Nu2Q,ntuples2016/ZZTo2L2Q,ntuples2016/T_tW,ntuples2016/TBar_tW,ntuples2016/WJetsToLNu_HT,ntuples2016/DYJetsToLL_M50_HT"


allMCTemplate['2017'] = "ntuples2017/TTHad_pow,ntuples2017/TTLep_pow,ntuples2017/TTSemi_pow,ntuples2017/WWToLNuQQ,ntuples2017/WZTo1L1Nu2Q,ntuples2017/ZZTo2L2Q,ntuples2017/T_tW,ntuples2017/TBar_tW,ntuples2017/WJetsToLNu_HT,ntuples2017/DYJetsToLL_M50_HT"

allMCTemplate['2018'] = "ntuples2018/TTHad_pow,ntuples2018/TTLep_pow,ntuples2018/TTSemi_pow,ntuples2018/WWToLNuQQ,ntuples2018/WZTo1L1Nu2Q,ntuples2018/ZZTo2L2Q,ntuples2018/T_tW,ntuples2018/TBar_tW,ntuples2018/WJetsToLNu_HT,ntuples2018/DYJetsToLL_M50_HT"





dataTemplate={}


dataTemplate['2016'] = "ntuples2016/SingleElectron,ntuples2016/SingleMuon,ntuples2016/MET,ntuples2016/SinglePhoton"
dataTemplate['2017'] = "ntuples2017/SingleElectron,ntuples2017/SingleMuon,ntuples2017/MET"
dataTemplate['2018'] = "ntuples2018/EGamma,ntuples2018/SingleMuon,ntuples2018/MET"
dataTemplate['Run2'] = dataTemplate['2016'] + "," + dataTemplate['2017'] + "," + dataTemplate['2018']




minMJJ=20.0
maxMJJ=145.0

binsMJJ={}
binsMJJ['allC']=35 #95

cuts['acceptance']= "(lnujj_LV_mass>600&&lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ)


###############################################
###############################################
##############  MC              ###############
###############################################
###############################################

def makeBackgroundShapesMJJFits(name,outDir,filename,template,addCut="1"):
    inCR = ("CR" in name)

    for l in leptons:
        for p in purities:
            for c in categories:
                cut='*'.join([cuts['CR' if inCR else 'common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptance']])
                rootFile=outDir+filename+"_"+name+"_MJJ_"+l+"_"+p+"_"+c+".root"
                cmd='vvMakeTopShapesSF.py -s "{template}" -c "{cut}" -o "{rootFile}"  -v "lnujj_l2_softDrop_mass"  -b {binsMJJ} -x {minMJJ} -X {maxMJJ}  -l {lumi} {ntuples}'.format(template=template,cut=cut,rootFile=rootFile,binsMJJ=binsMJJ[c],minMJJ=minMJJ,maxMJJ=maxMJJ,ntuples=ntuples,lumi=lumiTotal)
                os.system(cmd)



def makeNormalizations(name,outDir,filename,template,data=0,addCut='1',factor=1):
    inCR = ("CR" in name)

    for l in leptons:
        for p in purities:
            for c in categories:
                cut="*".join([cuts['CR' if inCR else 'common'],cuts[l],cuts[p],cuts[c],addCut,cuts['acceptance']])
                rootFile=outDir+filename+"_"+l+"_"+p+"_"+c+".root"
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}" -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -b "{bins}" -m "{mini}" -M "{maxi}" -f {factor} -n "{name}" {ntuples}'.format(samples=template,cut=cut,rootFile=rootFile,bins=binsMJJ[c],mini=minMJJ,maxi=maxMJJ,factor=factor,name=name,data=data,ntuples=ntuples)
                os.system(cmd)






###############################################
###############################################
####################  RUN  ####################
###############################################
###############################################




#for year in ['2016','2017','2018','Run2']:
#    odir='Inputs_'+year+'/'
#    os.system('mkdir -p '+odir)
#    if DODATA:
#        makeNormalizations("dataCR",odir,"LNuJJ_norm",dataTemplate[year],1)
#    if DOMC:    
#        makeBackgroundShapesMJJFits("resCR",odir,"LNuJJ",allMCTemplate[year])


#do pt dependence

for year in ['Run2']:
#    for bin in ['Low','Mid','High']:
    for bin in ['High']:
        odir='Inputs_'+bin+'/'
        os.system('mkdir -p '+odir)
        if DODATA:
            makeNormalizations("dataCR",odir,"LNuJJ_norm",dataTemplate[year],1,ptbin[bin])
        if DOMC:    
            makeBackgroundShapesMJJFits("resCR",odir,"LNuJJ",allMCTemplate[year],ptbin[bin])
