import os, sys
import ROOT

import optparse
parser = optparse.OptionParser()
parser.add_option("-t","--tag",dest="tag",default='',help="makeCard tag")
parser.add_option("-a","--allcomb",dest="allcomb",default=False,action="store_true",help="do combined DC for every category")
parser.add_option("-r","--region",dest="region",default='SR',help="signal region (SR) or control region (CR)")
(options,args) = parser.parse_args()


doAllComb='''
text2workspace.py datacard_bb_e_HP_{year}.txt -o combined_bb_e_HP_{year}.root
text2workspace.py datacard_bb_e_LP_{year}.txt -o combined_bb_e_LP_{year}.root
text2workspace.py datacard_bb_mu_HP_{year}.txt -o combined_bb_mu_HP_{year}.root
text2workspace.py datacard_bb_mu_LP_{year}.txt -o combined_bb_mu_LP_{year}.root
text2workspace.py datacard_nobb_e_HP_{year}.txt -o combined_nobb_e_HP_{year}.root
text2workspace.py datacard_nobb_e_LP_{year}.txt -o combined_nobb_e_LP_{year}.root
text2workspace.py datacard_nobb_mu_HP_{year}.txt -o combined_nobb_mu_HP_{year}.root
text2workspace.py datacard_nobb_mu_LP_{year}.txt -o combined_nobb_mu_LP_{year}.root
text2workspace.py datacard_vbf_e_HP_{year}.txt -o combined_vbf_e_HP_{year}.root
text2workspace.py datacard_vbf_e_LP_{year}.txt -o combined_vbf_e_LP_{year}.root
text2workspace.py datacard_vbf_mu_HP_{year}.txt -o combined_vbf_mu_HP_{year}.root
text2workspace.py datacard_vbf_mu_LP_{year}.txt -o combined_vbf_mu_LP_{year}.root

combineCards.py  bb_e_HP_{year}=datacard_bb_e_HP_{year}.txt  bb_e_LP_{year}=datacard_bb_e_LP_{year}.txt > combined_bb_e_{year}.txt
text2workspace.py combined_bb_e_{year}.txt -o combined_bb_e_{year}.root
combineCards.py  nobb_e_HP_{year}=datacard_nobb_e_HP_{year}.txt  nobb_e_LP_{year}=datacard_nobb_e_LP_{year}.txt > combined_nobb_e_{year}.txt
text2workspace.py combined_nobb_e_{year}.txt -o combined_nobb_e_{year}.root
combineCards.py  vbf_e_HP_{year}=datacard_vbf_e_HP_{year}.txt  vbf_e_LP_{year}=datacard_vbf_e_LP_{year}.txt > combined_vbf_e_{year}.txt
text2workspace.py combined_vbf_e_{year}.txt -o combined_vbf_e_{year}.root
combineCards.py  bb_mu_HP_{year}=datacard_bb_mu_HP_{year}.txt  bb_mu_LP_{year}=datacard_bb_mu_LP_{year}.txt > combined_bb_mu_{year}.txt
text2workspace.py combined_bb_mu_{year}.txt -o combined_bb_mu_{year}.root
combineCards.py  nobb_mu_HP_{year}=datacard_nobb_mu_HP_{year}.txt  nobb_mu_LP_{year}=datacard_nobb_mu_LP_{year}.txt > combined_nobb_mu_{year}.txt
text2workspace.py combined_nobb_mu_{year}.txt -o combined_nobb_mu_{year}.root
combineCards.py  vbf_mu_HP_{year}=datacard_vbf_mu_HP_{year}.txt  vbf_mu_LP_{year}=datacard_vbf_mu_LP_{year}.txt > combined_vbf_mu_{year}.txt
text2workspace.py combined_vbf_mu_{year}.txt -o combined_vbf_mu_{year}.root

combineCards.py  bb_e_HP_{year}=datacard_bb_e_HP_{year}.txt  bb_mu_HP_{year}=datacard_bb_mu_HP_{year}.txt > combined_bb_HP_{year}.txt
text2workspace.py combined_bb_HP_{year}.txt -o combined_bb_HP_{year}.root
combineCards.py  bb_e_LP_{year}=datacard_bb_e_LP_{year}.txt  bb_mu_LP_{year}=datacard_bb_mu_LP_{year}.txt > combined_bb_LP_{year}.txt
text2workspace.py combined_bb_LP_{year}.txt -o combined_bb_LP_{year}.root
combineCards.py  nobb_e_HP_{year}=datacard_nobb_e_HP_{year}.txt  nobb_mu_HP_{year}=datacard_nobb_mu_HP_{year}.txt > combined_nobb_HP_{year}.txt
text2workspace.py combined_nobb_HP_{year}.txt -o combined_nobb_HP_{year}.root
combineCards.py  nobb_e_LP_{year}=datacard_nobb_e_LP_{year}.txt  nobb_mu_LP_{year}=datacard_nobb_mu_LP_{year}.txt > combined_nobb_LP_{year}.txt
text2workspace.py combined_nobb_LP_{year}.txt -o combined_nobb_LP_{year}.root
combineCards.py  vbf_e_HP_{year}=datacard_vbf_e_HP_{year}.txt  vbf_mu_HP_{year}=datacard_vbf_mu_HP_{year}.txt > combined_vbf_HP_{year}.txt
text2workspace.py combined_vbf_HP_{year}.txt -o combined_vbf_HP_{year}.root
combineCards.py  vbf_e_LP_{year}=datacard_vbf_e_LP_{year}.txt  vbf_mu_LP_{year}=datacard_vbf_mu_LP_{year}.txt > combined_vbf_LP_{year}.txt
text2workspace.py combined_vbf_LP_{year}.txt -o combined_vbf_LP_{year}.root

combineCards.py  bb_e_HP_{year}=datacard_bb_e_HP_{year}.txt  nobb_e_HP_{year}=datacard_nobb_e_HP_{year}.txt  vbf_e_HP_{year}=datacard_vbf_e_HP_{year}.txt > combined_e_HP_{year}.txt
text2workspace.py combined_e_HP_{year}.txt -o combined_e_HP_{year}.root
combineCards.py  bb_e_LP_{year}=datacard_bb_e_LP_{year}.txt  nobb_e_LP_{year}=datacard_nobb_e_LP_{year}.txt  vbf_e_LP_{year}=datacard_vbf_e_LP_{year}.txt > combined_e_LP_{year}.txt
text2workspace.py combined_e_LP_{year}.txt -o combined_e_LP_{year}.root
combineCards.py  bb_mu_HP_{year}=datacard_bb_mu_HP_{year}.txt  nobb_mu_HP_{year}=datacard_nobb_mu_HP_{year}.txt  vbf_mu_HP_{year}=datacard_vbf_mu_HP_{year}.txt > combined_mu_HP_{year}.txt
text2workspace.py combined_mu_HP_{year}.txt -o combined_mu_HP_{year}.root
combineCards.py  bb_mu_LP_{year}=datacard_bb_mu_LP_{year}.txt  nobb_mu_LP_{year}=datacard_nobb_mu_LP_{year}.txt  vbf_mu_LP_{year}=datacard_vbf_mu_LP_{year}.txt > combined_mu_LP_{year}.txt
text2workspace.py combined_mu_LP_{year}.txt -o combined_mu_LP_{year}.root

combineCards.py  bb_e_HP_{year}=datacard_bb_e_HP_{year}.txt  bb_mu_HP_{year}=datacard_bb_mu_HP_{year}.txt  bb_e_LP_{year}=datacard_bb_e_LP_{year}.txt  bb_mu_LP_{year}=datacard_bb_mu_LP_{year}.txt > combined_bb_{year}.txt
text2workspace.py combined_bb_{year}.txt -o combined_bb_{year}.root
combineCards.py  nobb_e_HP_{year}=datacard_nobb_e_HP_{year}.txt  nobb_mu_HP_{year}=datacard_nobb_mu_HP_{year}.txt  nobb_e_LP_{year}=datacard_nobb_e_LP_{year}.txt  nobb_mu_LP_{year}=datacard_nobb_mu_LP_{year}.txt > combined_nobb_{year}.txt
text2workspace.py combined_nobb_{year}.txt -o combined_nobb_{year}.root
combineCards.py  vbf_e_HP_{year}=datacard_vbf_e_HP_{year}.txt  vbf_mu_HP_{year}=datacard_vbf_mu_HP_{year}.txt  vbf_e_LP_{year}=datacard_vbf_e_LP_{year}.txt  vbf_mu_LP_{year}=datacard_vbf_mu_LP_{year}.txt > combined_vbf_{year}.txt
text2workspace.py combined_vbf_{year}.txt -o combined_vbf_{year}.root

combineCards.py  bb_e_HP_{year}=datacard_bb_e_HP_{year}.txt  bb_e_LP_{year}=datacard_bb_e_LP_{year}.txt  nobb_e_HP_{year}=datacard_nobb_e_HP_{year}.txt  nobb_e_LP_{year}=datacard_nobb_e_LP_{year}.txt  vbf_e_HP_{year}=datacard_vbf_e_HP_{year}.txt  vbf_e_LP_{year}=datacard_vbf_e_LP_{year}.txt > combined_e_{year}.txt
text2workspace.py combined_e_{year}.txt -o combined_e_{year}.root
combineCards.py  bb_mu_HP_{year}=datacard_bb_mu_HP_{year}.txt  bb_mu_LP_{year}=datacard_bb_mu_LP_{year}.txt  nobb_mu_HP_{year}=datacard_nobb_mu_HP_{year}.txt  nobb_mu_LP_{year}=datacard_nobb_mu_LP_{year}.txt  vbf_mu_HP_{year}=datacard_vbf_mu_HP_{year}.txt  vbf_mu_LP_{year}=datacard_vbf_mu_LP_{year}.txt > combined_mu_{year}.txt
text2workspace.py combined_mu_{year}.txt -o combined_mu_{year}.root

combineCards.py  bb_e_HP_{year}=datacard_bb_e_HP_{year}.txt  bb_mu_HP_{year}=datacard_bb_mu_HP_{year}.txt  nobb_e_HP_{year}=datacard_nobb_e_HP_{year}.txt  nobb_mu_HP_{year}=datacard_nobb_mu_HP_{year}.txt  vbf_e_HP_{year}=datacard_vbf_e_HP_{year}.txt  vbf_mu_HP_{year}=datacard_vbf_mu_HP_{year}.txt > combined_HP_{year}.txt
text2workspace.py combined_HP_{year}.txt -o combined_HP_{year}.root
combineCards.py  bb_e_LP_{year}=datacard_bb_e_LP_{year}.txt  bb_mu_LP_{year}=datacard_bb_mu_LP_{year}.txt  nobb_e_LP_{year}=datacard_nobb_e_LP_{year}.txt  nobb_mu_LP_{year}=datacard_nobb_mu_LP_{year}.txt  vbf_e_LP_{year}=datacard_vbf_e_LP_{year}.txt  vbf_mu_LP_{year}=datacard_vbf_mu_LP_{year}.txt > combined_LP_{year}.txt
text2workspace.py combined_LP_{year}.txt -o combined_LP_{year}.root
'''


for signal in ['XWW','XWZ','XWH','VBFXWW']:

    dcFolder = 'Dc'+(('_'+options.region) if options.region!="SR" else '')+'_'+signal+'/'
    os.system('mkdir -p '+dcFolder)

    for year in ['2016','2017','2018']:

        doCards = 'python ../makeCard{tag}.py -y {year} -s {signal} -r {region} 2>&1 | tee log_makeCard{tag}_{year}_{region}_{signal}.txt'.format(tag=options.tag,year=year,signal=signal,region=options.region)
        os.system(doCards)
    
        if options.allcomb:
            os.system(doAllComb.format(year=year))

        os.system('combineCards.py  bb_e_HP_{year}=datacard_bb_e_HP_{year}.txt  bb_mu_HP_{year}=datacard_bb_mu_HP_{year}.txt  bb_e_LP_{year}=datacard_bb_e_LP_{year}.txt  bb_mu_LP_{year}=datacard_bb_mu_LP_{year}.txt  nobb_e_HP_{year}=datacard_nobb_e_HP_{year}.txt  nobb_mu_HP_{year}=datacard_nobb_mu_HP_{year}.txt  nobb_e_LP_{year}=datacard_nobb_e_LP_{year}.txt  nobb_mu_LP_{year}=datacard_nobb_mu_LP_{year}.txt  vbf_e_HP_{year}=datacard_vbf_e_HP_{year}.txt  vbf_mu_HP_{year}=datacard_vbf_mu_HP_{year}.txt  vbf_e_LP_{year}=datacard_vbf_e_LP_{year}.txt  vbf_mu_LP_{year}=datacard_vbf_mu_LP_{year}.txt > combined_{year}.txt'.format(year=year))
        os.system('text2workspace.py combined_{year}.txt -o combined_{year}.root'.format(year=year))


    os.system('combineCards.py    bb_e_HP_2016=datacard_bb_e_HP_2016.txt  bb_mu_HP_2016=datacard_bb_mu_HP_2016.txt  bb_e_LP_2016=datacard_bb_e_LP_2016.txt  bb_mu_LP_2016=datacard_bb_mu_LP_2016.txt  nobb_e_HP_2016=datacard_nobb_e_HP_2016.txt  nobb_mu_HP_2016=datacard_nobb_mu_HP_2016.txt  nobb_e_LP_2016=datacard_nobb_e_LP_2016.txt  nobb_mu_LP_2016=datacard_nobb_mu_LP_2016.txt  vbf_e_HP_2016=datacard_vbf_e_HP_2016.txt  vbf_mu_HP_2016=datacard_vbf_mu_HP_2016.txt  vbf_e_LP_2016=datacard_vbf_e_LP_2016.txt  vbf_mu_LP_2016=datacard_vbf_mu_LP_2016.txt      bb_e_HP_2017=datacard_bb_e_HP_2017.txt  bb_mu_HP_2017=datacard_bb_mu_HP_2017.txt  bb_e_LP_2017=datacard_bb_e_LP_2017.txt  bb_mu_LP_2017=datacard_bb_mu_LP_2017.txt  nobb_e_HP_2017=datacard_nobb_e_HP_2017.txt  nobb_mu_HP_2017=datacard_nobb_mu_HP_2017.txt  nobb_e_LP_2017=datacard_nobb_e_LP_2017.txt  nobb_mu_LP_2017=datacard_nobb_mu_LP_2017.txt  vbf_e_HP_2017=datacard_vbf_e_HP_2017.txt  vbf_mu_HP_2017=datacard_vbf_mu_HP_2017.txt  vbf_e_LP_2017=datacard_vbf_e_LP_2017.txt  vbf_mu_LP_2017=datacard_vbf_mu_LP_2017.txt      bb_e_HP_2018=datacard_bb_e_HP_2018.txt  bb_mu_HP_2018=datacard_bb_mu_HP_2018.txt  bb_e_LP_2018=datacard_bb_e_LP_2018.txt  bb_mu_LP_2018=datacard_bb_mu_LP_2018.txt  nobb_e_HP_2018=datacard_nobb_e_HP_2018.txt  nobb_mu_HP_2018=datacard_nobb_mu_HP_2018.txt  nobb_e_LP_2018=datacard_nobb_e_LP_2018.txt  nobb_mu_LP_2018=datacard_nobb_mu_LP_2018.txt  vbf_e_HP_2018=datacard_vbf_e_HP_2018.txt  vbf_mu_HP_2018=datacard_vbf_mu_HP_2018.txt  vbf_e_LP_2018=datacard_vbf_e_LP_2018.txt  vbf_mu_LP_2018=datacard_vbf_mu_LP_2018.txt    > combined.txt')

    os.system('text2workspace.py combined.txt -o combined.root')

    os.system('cp combined.root combined_full.root')
    os.system('cp combined.root combined_Run2.root')

    os.system('\mv datacard* '+dcFolder)
    os.system('\mv comb* '+dcFolder)
    os.system('\mv log_makeCard* '+dcFolder)
