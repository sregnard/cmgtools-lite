import os, sys
import ROOT

import optparse
parser = optparse.OptionParser()
parser.add_option("-t","--tag",dest="tag",default='',help="makeCard tag")
parser.add_option("-a","--allcomb",dest="allcomb",default=False,action="store_true",help="do combined DC for every category")
parser.add_option("-r","--region",dest="region",default='SR',help="signal region (SR) or control region (CR)")
(options,args) = parser.parse_args()


doAllComb='''
text2workspace.py datacard_e_HP_bb_LDy_Run2.txt -o combined_e_HP_bb_LDy.root
text2workspace.py datacard_e_LP_bb_LDy_Run2.txt -o combined_e_LP_bb_LDy.root
text2workspace.py datacard_mu_HP_bb_LDy_Run2.txt -o combined_mu_HP_bb_LDy.root
text2workspace.py datacard_mu_LP_bb_LDy_Run2.txt -o combined_mu_LP_bb_LDy.root
text2workspace.py datacard_e_HP_nobb_LDy_Run2.txt -o combined_e_HP_nobb_LDy.root
text2workspace.py datacard_e_LP_nobb_LDy_Run2.txt -o combined_e_LP_nobb_LDy.root
text2workspace.py datacard_mu_HP_nobb_LDy_Run2.txt -o combined_mu_HP_nobb_LDy.root
text2workspace.py datacard_mu_LP_nobb_LDy_Run2.txt -o combined_mu_LP_nobb_LDy.root
text2workspace.py datacard_e_HP_vbf_LDy_Run2.txt -o combined_e_HP_vbf_LDy.root
text2workspace.py datacard_e_LP_vbf_LDy_Run2.txt -o combined_e_LP_vbf_LDy.root
text2workspace.py datacard_mu_HP_vbf_LDy_Run2.txt -o combined_mu_HP_vbf_LDy.root
text2workspace.py datacard_mu_LP_vbf_LDy_Run2.txt -o combined_mu_LP_vbf_LDy.root

combineCards.py  e_HP_bb_LDy_Run2=datacard_e_HP_bb_LDy_Run2.txt  e_LP_bb_LDy_Run2=datacard_e_LP_bb_LDy_Run2.txt > combined_e_bb_LDy.txt
text2workspace.py combined_e_bb_LDy.txt -o combined_e_bb_LDy.root
combineCards.py  e_HP_nobb_LDy_Run2=datacard_e_HP_nobb_LDy_Run2.txt  e_LP_nobb_LDy_Run2=datacard_e_LP_nobb_LDy_Run2.txt > combined_e_nobb_LDy.txt
text2workspace.py combined_e_nobb_LDy.txt -o combined_e_nobb_LDy.root
combineCards.py  e_HP_vbf_LDy_Run2=datacard_e_HP_vbf_LDy_Run2.txt  e_LP_vbf_LDy_Run2=datacard_e_LP_vbf_LDy_Run2.txt > combined_e_vbf_LDy.txt
text2workspace.py combined_e_vbf_LDy.txt -o combined_e_vbf_LDy.root
combineCards.py  mu_HP_bb_LDy_Run2=datacard_mu_HP_bb_LDy_Run2.txt  mu_LP_bb_LDy_Run2=datacard_mu_LP_bb_LDy_Run2.txt > combined_mu_bb_LDy.txt
text2workspace.py combined_mu_bb_LDy.txt -o combined_mu_bb_LDy.root
combineCards.py  mu_HP_nobb_LDy_Run2=datacard_mu_HP_nobb_LDy_Run2.txt  mu_LP_nobb_LDy_Run2=datacard_mu_LP_nobb_LDy_Run2.txt > combined_mu_nobb_LDy.txt
text2workspace.py combined_mu_nobb_LDy.txt -o combined_mu_nobb_LDy.root
combineCards.py  mu_HP_vbf_LDy_Run2=datacard_mu_HP_vbf_LDy_Run2.txt  mu_LP_vbf_LDy_Run2=datacard_mu_LP_vbf_LDy_Run2.txt > combined_mu_vbf_LDy.txt
text2workspace.py combined_mu_vbf_LDy.txt -o combined_mu_vbf_LDy.root

combineCards.py  e_HP_bb_LDy_Run2=datacard_e_HP_bb_LDy_Run2.txt  mu_HP_bb_LDy_Run2=datacard_mu_HP_bb_LDy_Run2.txt > combined_HP_bb_LDy.txt
text2workspace.py combined_HP_bb_LDy.txt -o combined_HP_bb_LDy.root
combineCards.py  e_LP_bb_LDy_Run2=datacard_e_LP_bb_LDy_Run2.txt  mu_LP_bb_LDy_Run2=datacard_mu_LP_bb_LDy_Run2.txt > combined_LP_bb_LDy.txt
text2workspace.py combined_LP_bb_LDy.txt -o combined_LP_bb_LDy.root
combineCards.py  e_HP_nobb_LDy_Run2=datacard_e_HP_nobb_LDy_Run2.txt  mu_HP_nobb_LDy_Run2=datacard_mu_HP_nobb_LDy_Run2.txt > combined_HP_nobb_LDy.txt
text2workspace.py combined_HP_nobb_LDy.txt -o combined_HP_nobb_LDy.root
combineCards.py  e_LP_nobb_LDy_Run2=datacard_e_LP_nobb_LDy_Run2.txt  mu_LP_nobb_LDy_Run2=datacard_mu_LP_nobb_LDy_Run2.txt > combined_LP_nobb_LDy.txt
text2workspace.py combined_LP_nobb_LDy.txt -o combined_LP_nobb_LDy.root
combineCards.py  e_HP_vbf_LDy_Run2=datacard_e_HP_vbf_LDy_Run2.txt  mu_HP_vbf_LDy_Run2=datacard_mu_HP_vbf_LDy_Run2.txt > combined_HP_vbf_LDy.txt
text2workspace.py combined_HP_vbf_LDy.txt -o combined_HP_vbf_LDy.root
combineCards.py  e_LP_vbf_LDy_Run2=datacard_e_LP_vbf_LDy_Run2.txt  mu_LP_vbf_LDy_Run2=datacard_mu_LP_vbf_LDy_Run2.txt > combined_LP_vbf_LDy.txt
text2workspace.py combined_LP_vbf_LDy.txt -o combined_LP_vbf_LDy.root

combineCards.py  e_HP_bb_LDy_Run2=datacard_e_HP_bb_LDy_Run2.txt  e_HP_nobb_LDy_Run2=datacard_e_HP_nobb_LDy_Run2.txt  e_HP_vbf_LDy_Run2=datacard_e_HP_vbf_LDy_Run2.txt > combined_e_HP_LDy.txt
text2workspace.py combined_e_HP_LDy.txt -o combined_e_HP_LDy.root
combineCards.py  e_LP_bb_LDy_Run2=datacard_e_LP_bb_LDy_Run2.txt  e_LP_nobb_LDy_Run2=datacard_e_LP_nobb_LDy_Run2.txt  e_LP_vbf_LDy_Run2=datacard_e_LP_vbf_LDy_Run2.txt > combined_e_LP_LDy.txt
text2workspace.py combined_e_LP_LDy.txt -o combined_e_LP_LDy.root
combineCards.py  mu_HP_bb_LDy_Run2=datacard_mu_HP_bb_LDy_Run2.txt  mu_HP_nobb_LDy_Run2=datacard_mu_HP_nobb_LDy_Run2.txt  mu_HP_vbf_LDy_Run2=datacard_mu_HP_vbf_LDy_Run2.txt > combined_mu_HP_LDy.txt
text2workspace.py combined_mu_HP_LDy.txt -o combined_mu_HP_LDy.root
combineCards.py  mu_LP_bb_LDy_Run2=datacard_mu_LP_bb_LDy_Run2.txt  mu_LP_nobb_LDy_Run2=datacard_mu_LP_nobb_LDy_Run2.txt  mu_LP_vbf_LDy_Run2=datacard_mu_LP_vbf_LDy_Run2.txt > combined_mu_LP_LDy.txt
text2workspace.py combined_mu_LP_LDy.txt -o combined_mu_LP_LDy.root

combineCards.py  e_HP_bb_LDy_Run2=datacard_e_HP_bb_LDy_Run2.txt  mu_HP_bb_LDy_Run2=datacard_mu_HP_bb_LDy_Run2.txt  e_LP_bb_LDy_Run2=datacard_e_LP_bb_LDy_Run2.txt  mu_LP_bb_LDy_Run2=datacard_mu_LP_bb_LDy_Run2.txt > combined_bb_LDy.txt
text2workspace.py combined_bb_LDy.txt -o combined_bb_LDy.root
combineCards.py  e_HP_nobb_LDy_Run2=datacard_e_HP_nobb_LDy_Run2.txt  mu_HP_nobb_LDy_Run2=datacard_mu_HP_nobb_LDy_Run2.txt  e_LP_nobb_LDy_Run2=datacard_e_LP_nobb_LDy_Run2.txt  mu_LP_nobb_LDy_Run2=datacard_mu_LP_nobb_LDy_Run2.txt > combined_nobb_LDy.txt
text2workspace.py combined_nobb_LDy.txt -o combined_nobb_LDy.root
combineCards.py  e_HP_vbf_LDy_Run2=datacard_e_HP_vbf_LDy_Run2.txt  mu_HP_vbf_LDy_Run2=datacard_mu_HP_vbf_LDy_Run2.txt  e_LP_vbf_LDy_Run2=datacard_e_LP_vbf_LDy_Run2.txt  mu_LP_vbf_LDy_Run2=datacard_mu_LP_vbf_LDy_Run2.txt > combined_vbf_LDy.txt
text2workspace.py combined_vbf_LDy.txt -o combined_vbf_LDy.root

combineCards.py  e_HP_bb_LDy_Run2=datacard_e_HP_bb_LDy_Run2.txt  e_LP_bb_LDy_Run2=datacard_e_LP_bb_LDy_Run2.txt  e_HP_nobb_LDy_Run2=datacard_e_HP_nobb_LDy_Run2.txt  e_LP_nobb_LDy_Run2=datacard_e_LP_nobb_LDy_Run2.txt  e_HP_vbf_LDy_Run2=datacard_e_HP_vbf_LDy_Run2.txt  e_LP_vbf_LDy_Run2=datacard_e_LP_vbf_LDy_Run2.txt > combined_e_LDy.txt
text2workspace.py combined_e_LDy.txt -o combined_e_LDy.root
combineCards.py  mu_HP_bb_LDy_Run2=datacard_mu_HP_bb_LDy_Run2.txt  mu_LP_bb_LDy_Run2=datacard_mu_LP_bb_LDy_Run2.txt  mu_HP_nobb_LDy_Run2=datacard_mu_HP_nobb_LDy_Run2.txt  mu_LP_nobb_LDy_Run2=datacard_mu_LP_nobb_LDy_Run2.txt  mu_HP_vbf_LDy_Run2=datacard_mu_HP_vbf_LDy_Run2.txt  mu_LP_vbf_LDy_Run2=datacard_mu_LP_vbf_LDy_Run2.txt > combined_mu_LDy.txt
text2workspace.py combined_mu_LDy.txt -o combined_mu_LDy.root

combineCards.py  e_HP_bb_LDy_Run2=datacard_e_HP_bb_LDy_Run2.txt  mu_HP_bb_LDy_Run2=datacard_mu_HP_bb_LDy_Run2.txt  e_HP_nobb_LDy_Run2=datacard_e_HP_nobb_LDy_Run2.txt  mu_HP_nobb_LDy_Run2=datacard_mu_HP_nobb_LDy_Run2.txt  e_HP_vbf_LDy_Run2=datacard_e_HP_vbf_LDy_Run2.txt  mu_HP_vbf_LDy_Run2=datacard_mu_HP_vbf_LDy_Run2.txt > combined_HP_LDy.txt
text2workspace.py combined_HP_LDy.txt -o combined_HP_LDy.root
combineCards.py  e_LP_bb_LDy_Run2=datacard_e_LP_bb_LDy_Run2.txt  mu_LP_bb_LDy_Run2=datacard_mu_LP_bb_LDy_Run2.txt  e_LP_nobb_LDy_Run2=datacard_e_LP_nobb_LDy_Run2.txt  mu_LP_nobb_LDy_Run2=datacard_mu_LP_nobb_LDy_Run2.txt  e_LP_vbf_LDy_Run2=datacard_e_LP_vbf_LDy_Run2.txt  mu_LP_vbf_LDy_Run2=datacard_mu_LP_vbf_LDy_Run2.txt > combined_LP_LDy.txt
text2workspace.py combined_LP_LDy.txt -o combined_LP_LDy.root
'''


for signal in [
        'GbuToWW',
        'RadToWW',
        'ZprToWW',
        'WprToWZ',
        'WprToWH',
        'VBFGbuToWW',
        'VBFRadToWW',
        'VBFZprToWW',
        'VBFWprToWZ',
#        'VBFWprToWH',
]:

    dcFolder = 'Dc'+(('_'+options.region) if options.region!="SR" else '')+'_'+signal+'/'
    os.system('mkdir -p '+dcFolder)

    doCards = 'python ../makeCard{tag}.py -y Run2 -s {signal} -r {region} 2>&1 | tee log_makeCard{tag}_{region}_{signal}.txt'.format(tag=options.tag,signal=signal,region=options.region)
    os.system(doCards)

    if options.allcomb:
        os.system(doAllComb)

    os.system('combineCards.py   e_HP_bb_LDy_Run2=datacard_e_HP_bb_LDy_Run2.txt  mu_HP_bb_LDy_Run2=datacard_mu_HP_bb_LDy_Run2.txt  e_LP_bb_LDy_Run2=datacard_e_LP_bb_LDy_Run2.txt  mu_LP_bb_LDy_Run2=datacard_mu_LP_bb_LDy_Run2.txt  e_HP_nobb_LDy_Run2=datacard_e_HP_nobb_LDy_Run2.txt  mu_HP_nobb_LDy_Run2=datacard_mu_HP_nobb_LDy_Run2.txt  e_LP_nobb_LDy_Run2=datacard_e_LP_nobb_LDy_Run2.txt  mu_LP_nobb_LDy_Run2=datacard_mu_LP_nobb_LDy_Run2.txt  e_HP_vbf_LDy_Run2=datacard_e_HP_vbf_LDy_Run2.txt  mu_HP_vbf_LDy_Run2=datacard_mu_HP_vbf_LDy_Run2.txt  e_LP_vbf_LDy_Run2=datacard_e_LP_vbf_LDy_Run2.txt  mu_LP_vbf_LDy_Run2=datacard_mu_LP_vbf_LDy_Run2.txt    e_HP_bb_HDy_Run2=datacard_e_HP_bb_HDy_Run2.txt  mu_HP_bb_HDy_Run2=datacard_mu_HP_bb_HDy_Run2.txt  e_LP_bb_HDy_Run2=datacard_e_LP_bb_HDy_Run2.txt  mu_LP_bb_HDy_Run2=datacard_mu_LP_bb_HDy_Run2.txt  e_HP_nobb_HDy_Run2=datacard_e_HP_nobb_HDy_Run2.txt  mu_HP_nobb_HDy_Run2=datacard_mu_HP_nobb_HDy_Run2.txt  e_LP_nobb_HDy_Run2=datacard_e_LP_nobb_HDy_Run2.txt  mu_LP_nobb_HDy_Run2=datacard_mu_LP_nobb_HDy_Run2.txt  e_HP_vbf_HDy_Run2=datacard_e_HP_vbf_HDy_Run2.txt  mu_HP_vbf_HDy_Run2=datacard_mu_HP_vbf_HDy_Run2.txt  e_LP_vbf_HDy_Run2=datacard_e_LP_vbf_HDy_Run2.txt  mu_LP_vbf_HDy_Run2=datacard_mu_LP_vbf_HDy_Run2.txt   > combined.txt')
    os.system('text2workspace.py combined.txt -o combined.root')

    os.system('cp combined.root combined_full.root')
    os.system('mv combined.root combined_Run2.root')

    os.system('\mv datacard* '+dcFolder)
    os.system('\mv comb* '+dcFolder)
    os.system('\mv log_makeCard* '+dcFolder)
