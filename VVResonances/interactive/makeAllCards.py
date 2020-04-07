import os, sys
import ROOT

import optparse
parser = optparse.OptionParser()
parser.add_option("-t","--tag",dest="tag",default='',help="makeCard tag")
parser.add_option("-a","--allcomb",dest="allcomb",default=False,action="store_true",help="do combined DC for every category")
parser.add_option("-r","--region",dest="region",default='SR',help="signal region (SR) or control region (CR)")
(options,args) = parser.parse_args()


doAllComb='''
text2workspace.py datacard_bb_e_HP_Run2.txt -o combined_bb_e_HP.root
text2workspace.py datacard_bb_e_LP_Run2.txt -o combined_bb_e_LP.root
text2workspace.py datacard_bb_mu_HP_Run2.txt -o combined_bb_mu_HP.root
text2workspace.py datacard_bb_mu_LP_Run2.txt -o combined_bb_mu_LP.root
text2workspace.py datacard_nobb_e_HP_Run2.txt -o combined_nobb_e_HP.root
text2workspace.py datacard_nobb_e_LP_Run2.txt -o combined_nobb_e_LP.root
text2workspace.py datacard_nobb_mu_HP_Run2.txt -o combined_nobb_mu_HP.root
text2workspace.py datacard_nobb_mu_LP_Run2.txt -o combined_nobb_mu_LP.root

combineCards.py  bb_e_HP_Run2=datacard_bb_e_HP_Run2.txt  bb_e_LP_Run2=datacard_bb_e_LP_Run2.txt > combined_bb_e.txt
text2workspace.py combined_bb_e.txt -o combined_bb_e.root
combineCards.py  nobb_e_HP_Run2=datacard_nobb_e_HP_Run2.txt  nobb_e_LP_Run2=datacard_nobb_e_LP_Run2.txt > combined_nobb_e.txt
text2workspace.py combined_nobb_e.txt -o combined_nobb_e.root
combineCards.py  bb_mu_HP_Run2=datacard_bb_mu_HP_Run2.txt  bb_mu_LP_Run2=datacard_bb_mu_LP_Run2.txt > combined_bb_mu.txt
text2workspace.py combined_bb_mu.txt -o combined_bb_mu.root
combineCards.py  nobb_mu_HP_Run2=datacard_nobb_mu_HP_Run2.txt  nobb_mu_LP_Run2=datacard_nobb_mu_LP_Run2.txt > combined_nobb_mu.txt
text2workspace.py combined_nobb_mu.txt -o combined_nobb_mu.root

combineCards.py  bb_e_HP_Run2=datacard_bb_e_HP_Run2.txt  bb_mu_HP_Run2=datacard_bb_mu_HP_Run2.txt > combined_bb_HP.txt
text2workspace.py combined_bb_HP.txt -o combined_bb_HP.root
combineCards.py  bb_e_LP_Run2=datacard_bb_e_LP_Run2.txt  bb_mu_LP_Run2=datacard_bb_mu_LP_Run2.txt > combined_bb_LP.txt
text2workspace.py combined_bb_LP.txt -o combined_bb_LP.root
combineCards.py  nobb_e_HP_Run2=datacard_nobb_e_HP_Run2.txt  nobb_mu_HP_Run2=datacard_nobb_mu_HP_Run2.txt > combined_nobb_HP.txt
text2workspace.py combined_nobb_HP.txt -o combined_nobb_HP.root
combineCards.py  nobb_e_LP_Run2=datacard_nobb_e_LP_Run2.txt  nobb_mu_LP_Run2=datacard_nobb_mu_LP_Run2.txt > combined_nobb_LP.txt
text2workspace.py combined_nobb_LP.txt -o combined_nobb_LP.root

combineCards.py  bb_e_HP_Run2=datacard_bb_e_HP_Run2.txt  nobb_e_HP_Run2=datacard_nobb_e_HP_Run2.txt > combined_e_HP.txt
text2workspace.py combined_e_HP.txt -o combined_e_HP.root
combineCards.py  bb_e_LP_Run2=datacard_bb_e_LP_Run2.txt  nobb_e_LP_Run2=datacard_nobb_e_LP_Run2.txt > combined_e_LP.txt
text2workspace.py combined_e_LP.txt -o combined_e_LP.root
combineCards.py  bb_mu_HP_Run2=datacard_bb_mu_HP_Run2.txt  nobb_mu_HP_Run2=datacard_nobb_mu_HP_Run2.txt > combined_mu_HP.txt
text2workspace.py combined_mu_HP.txt -o combined_mu_HP.root
combineCards.py  bb_mu_LP_Run2=datacard_bb_mu_LP_Run2.txt  nobb_mu_LP_Run2=datacard_nobb_mu_LP_Run2.txt > combined_mu_LP.txt
text2workspace.py combined_mu_LP.txt -o combined_mu_LP.root

combineCards.py  bb_e_HP_Run2=datacard_bb_e_HP_Run2.txt  bb_mu_HP_Run2=datacard_bb_mu_HP_Run2.txt  bb_e_LP_Run2=datacard_bb_e_LP_Run2.txt  bb_mu_LP_Run2=datacard_bb_mu_LP_Run2.txt > combined_bb.txt
text2workspace.py combined_bb.txt -o combined_bb.root
combineCards.py  nobb_e_HP_Run2=datacard_nobb_e_HP_Run2.txt  nobb_mu_HP_Run2=datacard_nobb_mu_HP_Run2.txt  nobb_e_LP_Run2=datacard_nobb_e_LP_Run2.txt  nobb_mu_LP_Run2=datacard_nobb_mu_LP_Run2.txt > combined_nobb.txt
text2workspace.py combined_nobb.txt -o combined_nobb.root

combineCards.py  bb_e_HP_Run2=datacard_bb_e_HP_Run2.txt  bb_e_LP_Run2=datacard_bb_e_LP_Run2.txt  nobb_e_HP_Run2=datacard_nobb_e_HP_Run2.txt  nobb_e_LP_Run2=datacard_nobb_e_LP_Run2.txt > combined_e.txt
text2workspace.py combined_e.txt -o combined_e.root
combineCards.py  bb_mu_HP_Run2=datacard_bb_mu_HP_Run2.txt  bb_mu_LP_Run2=datacard_bb_mu_LP_Run2.txt  nobb_mu_HP_Run2=datacard_nobb_mu_HP_Run2.txt  nobb_mu_LP_Run2=datacard_nobb_mu_LP_Run2.txt > combined_mu.txt
text2workspace.py combined_mu.txt -o combined_mu.root

combineCards.py  bb_e_HP_Run2=datacard_bb_e_HP_Run2.txt  bb_mu_HP_Run2=datacard_bb_mu_HP_Run2.txt  nobb_e_HP_Run2=datacard_nobb_e_HP_Run2.txt  nobb_mu_HP_Run2=datacard_nobb_mu_HP_Run2.txt > combined_HP.txt
text2workspace.py combined_HP.txt -o combined_HP.root
combineCards.py  bb_e_LP_Run2=datacard_bb_e_LP_Run2.txt  bb_mu_LP_Run2=datacard_bb_mu_LP_Run2.txt  nobb_e_LP_Run2=datacard_nobb_e_LP_Run2.txt  nobb_mu_LP_Run2=datacard_nobb_mu_LP_Run2.txt > combined_LP.txt
text2workspace.py combined_LP.txt -o combined_LP.root
'''


for signal in ['XWW','XWZ','XWH']:

    dcFolder = 'Dc'+(('_'+options.region) if options.region!="SR" else '')+'_'+signal+'/'
    os.system('mkdir -p '+dcFolder)

    #doCards = 'python ../makeCard_{tag}.py -y Run2 -s {signal} -r {region} 2>&1 | tee log_makeCard_{tag}_{region}_{signal}.txt'.format(tag=options.tag,signal=signal,region=options.region)
    doCards = 'python ../makeCard_V2.py -y Run2 -s {signal} -r {region} 2>&1 | tee log_makeCard_{region}_{signal}.txt'.format(signal=signal,region=options.region)
    os.system(doCards)
    
    if options.allcomb:
        os.system(doAllComb)

    os.system('combineCards.py  bb_e_HP_Run2=datacard_bb_e_HP_Run2.txt  bb_mu_HP_Run2=datacard_bb_mu_HP_Run2.txt  bb_e_LP_Run2=datacard_bb_e_LP_Run2.txt  bb_mu_LP_Run2=datacard_bb_mu_LP_Run2.txt  nobb_e_HP_Run2=datacard_nobb_e_HP_Run2.txt  nobb_mu_HP_Run2=datacard_nobb_mu_HP_Run2.txt  nobb_e_LP_Run2=datacard_nobb_e_LP_Run2.txt  nobb_mu_LP_Run2=datacard_nobb_mu_LP_Run2.txt > combined.txt')
    os.system('text2workspace.py combined.txt -o combined.root')
    
    os.system('cp combined.root combined_full.root')
    os.system('cp combined.root combined_Run2.root')
    
    os.system('\mv datacard* '+dcFolder)
    os.system('\mv comb* '+dcFolder)
    os.system('\mv log_makeCard* '+dcFolder)

