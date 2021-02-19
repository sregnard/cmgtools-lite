import os, sys
import ROOT

import optparse
parser = optparse.OptionParser()
parser.add_option("-t","--tag",dest="tag",default='',help="makeCard tag")
parser.add_option("-a","--allcomb",dest="allcomb",default=False,action="store_true",help="do combined DC for every category")
parser.add_option("-r","--region",dest="region",default='SR',help="signal region (SR) or control region (CR)")
(options,args) = parser.parse_args()


doAllComb='''
text2workspace.py datacard_e_HP_bb_LDy_{year}.txt -o combined_e_HP_bb_LDy_{year}.root
text2workspace.py datacard_e_LP_bb_LDy_{year}.txt -o combined_e_LP_bb_LDy_{year}.root
text2workspace.py datacard_mu_HP_bb_LDy_{year}.txt -o combined_mu_HP_bb_LDy_{year}.root
text2workspace.py datacard_mu_LP_bb_LDy_{year}.txt -o combined_mu_LP_bb_LDy_{year}.root
text2workspace.py datacard_e_HP_nobb_LDy_{year}.txt -o combined_e_HP_nobb_LDy_{year}.root
text2workspace.py datacard_e_LP_nobb_LDy_{year}.txt -o combined_e_LP_nobb_LDy_{year}.root
text2workspace.py datacard_mu_HP_nobb_LDy_{year}.txt -o combined_mu_HP_nobb_LDy_{year}.root
text2workspace.py datacard_mu_LP_nobb_LDy_{year}.txt -o combined_mu_LP_nobb_LDy_{year}.root
text2workspace.py datacard_e_HP_vbf_LDy_{year}.txt -o combined_e_HP_vbf_LDy_{year}.root
text2workspace.py datacard_e_LP_vbf_LDy_{year}.txt -o combined_e_LP_vbf_LDy_{year}.root
text2workspace.py datacard_mu_HP_vbf_LDy_{year}.txt -o combined_mu_HP_vbf_LDy_{year}.root
text2workspace.py datacard_mu_LP_vbf_LDy_{year}.txt -o combined_mu_LP_vbf_LDy_{year}.root

combineCards.py  e_HP_bb_LDy_{year}=datacard_e_HP_bb_LDy_{year}.txt  e_LP_bb_LDy_{year}=datacard_e_LP_bb_LDy_{year}.txt > combined_e_bb_LDy_{year}.txt
text2workspace.py combined_e_bb_LDy_{year}.txt -o combined_e_bb_LDy_{year}.root
combineCards.py  e_HP_nobb_LDy_{year}=datacard_e_HP_nobb_LDy_{year}.txt  e_LP_nobb_LDy_{year}=datacard_e_LP_nobb_LDy_{year}.txt > combined_e_nobb_LDy_{year}.txt
text2workspace.py combined_e_nobb_LDy_{year}.txt -o combined_e_nobb_LDy_{year}.root
combineCards.py  e_HP_vbf_LDy_{year}=datacard_e_HP_vbf_LDy_{year}.txt  e_LP_vbf_LDy_{year}=datacard_e_LP_vbf_LDy_{year}.txt > combined_e_vbf_LDy_{year}.txt
text2workspace.py combined_e_vbf_LDy_{year}.txt -o combined_e_vbf_LDy_{year}.root
combineCards.py  mu_HP_bb_LDy_{year}=datacard_mu_HP_bb_LDy_{year}.txt  mu_LP_bb_LDy_{year}=datacard_mu_LP_bb_LDy_{year}.txt > combined_mu_bb_LDy_{year}.txt
text2workspace.py combined_mu_bb_LDy_{year}.txt -o combined_mu_bb_LDy_{year}.root
combineCards.py  mu_HP_nobb_LDy_{year}=datacard_mu_HP_nobb_LDy_{year}.txt  mu_LP_nobb_LDy_{year}=datacard_mu_LP_nobb_LDy_{year}.txt > combined_mu_nobb_LDy_{year}.txt
text2workspace.py combined_mu_nobb_LDy_{year}.txt -o combined_mu_nobb_LDy_{year}.root
combineCards.py  mu_HP_vbf_LDy_{year}=datacard_mu_HP_vbf_LDy_{year}.txt  mu_LP_vbf_LDy_{year}=datacard_mu_LP_vbf_LDy_{year}.txt > combined_mu_vbf_LDy_{year}.txt
text2workspace.py combined_mu_vbf_LDy_{year}.txt -o combined_mu_vbf_LDy_{year}.root

combineCards.py  e_HP_bb_LDy_{year}=datacard_e_HP_bb_LDy_{year}.txt  mu_HP_bb_LDy_{year}=datacard_mu_HP_bb_LDy_{year}.txt > combined_HP_bb_LDy_{year}.txt
text2workspace.py combined_HP_bb_LDy_{year}.txt -o combined_HP_bb_LDy_{year}.root
combineCards.py  e_LP_bb_LDy_{year}=datacard_e_LP_bb_LDy_{year}.txt  mu_LP_bb_LDy_{year}=datacard_mu_LP_bb_LDy_{year}.txt > combined_LP_bb_LDy_{year}.txt
text2workspace.py combined_LP_bb_LDy_{year}.txt -o combined_LP_bb_LDy_{year}.root
combineCards.py  e_HP_nobb_LDy_{year}=datacard_e_HP_nobb_LDy_{year}.txt  mu_HP_nobb_LDy_{year}=datacard_mu_HP_nobb_LDy_{year}.txt > combined_HP_nobb_LDy_{year}.txt
text2workspace.py combined_HP_nobb_LDy_{year}.txt -o combined_HP_nobb_LDy_{year}.root
combineCards.py  e_LP_nobb_LDy_{year}=datacard_e_LP_nobb_LDy_{year}.txt  mu_LP_nobb_LDy_{year}=datacard_mu_LP_nobb_LDy_{year}.txt > combined_LP_nobb_LDy_{year}.txt
text2workspace.py combined_LP_nobb_LDy_{year}.txt -o combined_LP_nobb_LDy_{year}.root
combineCards.py  e_HP_vbf_LDy_{year}=datacard_e_HP_vbf_LDy_{year}.txt  mu_HP_vbf_LDy_{year}=datacard_mu_HP_vbf_LDy_{year}.txt > combined_HP_vbf_LDy_{year}.txt
text2workspace.py combined_HP_vbf_LDy_{year}.txt -o combined_HP_vbf_LDy_{year}.root
combineCards.py  e_LP_vbf_LDy_{year}=datacard_e_LP_vbf_LDy_{year}.txt  mu_LP_vbf_LDy_{year}=datacard_mu_LP_vbf_LDy_{year}.txt > combined_LP_vbf_LDy_{year}.txt
text2workspace.py combined_LP_vbf_LDy_{year}.txt -o combined_LP_vbf_LDy_{year}.root

combineCards.py  e_HP_bb_LDy_{year}=datacard_e_HP_bb_LDy_{year}.txt  e_HP_nobb_LDy_{year}=datacard_e_HP_nobb_LDy_{year}.txt  e_HP_vbf_LDy_{year}=datacard_e_HP_vbf_LDy_{year}.txt > combined_e_HP_LDy_{year}.txt
text2workspace.py combined_e_HP_LDy_{year}.txt -o combined_e_HP_LDy_{year}.root
combineCards.py  e_LP_bb_LDy_{year}=datacard_e_LP_bb_LDy_{year}.txt  e_LP_nobb_LDy_{year}=datacard_e_LP_nobb_LDy_{year}.txt  e_LP_vbf_LDy_{year}=datacard_e_LP_vbf_LDy_{year}.txt > combined_e_LP_LDy_{year}.txt
text2workspace.py combined_e_LP_LDy_{year}.txt -o combined_e_LP_LDy_{year}.root
combineCards.py  mu_HP_bb_LDy_{year}=datacard_mu_HP_bb_LDy_{year}.txt  mu_HP_nobb_LDy_{year}=datacard_mu_HP_nobb_LDy_{year}.txt  mu_HP_vbf_LDy_{year}=datacard_mu_HP_vbf_LDy_{year}.txt > combined_mu_HP_LDy_{year}.txt
text2workspace.py combined_mu_HP_LDy_{year}.txt -o combined_mu_HP_LDy_{year}.root
combineCards.py  mu_LP_bb_LDy_{year}=datacard_mu_LP_bb_LDy_{year}.txt  mu_LP_nobb_LDy_{year}=datacard_mu_LP_nobb_LDy_{year}.txt  mu_LP_vbf_LDy_{year}=datacard_mu_LP_vbf_LDy_{year}.txt > combined_mu_LP_LDy_{year}.txt
text2workspace.py combined_mu_LP_LDy_{year}.txt -o combined_mu_LP_LDy_{year}.root

combineCards.py  e_HP_bb_LDy_{year}=datacard_e_HP_bb_LDy_{year}.txt  mu_HP_bb_LDy_{year}=datacard_mu_HP_bb_LDy_{year}.txt  e_LP_bb_LDy_{year}=datacard_e_LP_bb_LDy_{year}.txt  mu_LP_bb_LDy_{year}=datacard_mu_LP_bb_LDy_{year}.txt > combined_bb_LDy_{year}.txt
text2workspace.py combined_bb_LDy_{year}.txt -o combined_bb_LDy_{year}.root
combineCards.py  e_HP_nobb_LDy_{year}=datacard_e_HP_nobb_LDy_{year}.txt  mu_HP_nobb_LDy_{year}=datacard_mu_HP_nobb_LDy_{year}.txt  e_LP_nobb_LDy_{year}=datacard_e_LP_nobb_LDy_{year}.txt  mu_LP_nobb_LDy_{year}=datacard_mu_LP_nobb_LDy_{year}.txt > combined_nobb_LDy_{year}.txt
text2workspace.py combined_nobb_LDy_{year}.txt -o combined_nobb_LDy_{year}.root
combineCards.py  e_HP_vbf_LDy_{year}=datacard_e_HP_vbf_LDy_{year}.txt  mu_HP_vbf_LDy_{year}=datacard_mu_HP_vbf_LDy_{year}.txt  e_LP_vbf_LDy_{year}=datacard_e_LP_vbf_LDy_{year}.txt  mu_LP_vbf_LDy_{year}=datacard_mu_LP_vbf_LDy_{year}.txt > combined_vbf_LDy_{year}.txt
text2workspace.py combined_vbf_LDy_{year}.txt -o combined_vbf_LDy_{year}.root

combineCards.py  e_HP_bb_LDy_{year}=datacard_e_HP_bb_LDy_{year}.txt  e_LP_bb_LDy_{year}=datacard_e_LP_bb_LDy_{year}.txt  e_HP_nobb_LDy_{year}=datacard_e_HP_nobb_LDy_{year}.txt  e_LP_nobb_LDy_{year}=datacard_e_LP_nobb_LDy_{year}.txt  e_HP_vbf_LDy_{year}=datacard_e_HP_vbf_LDy_{year}.txt  e_LP_vbf_LDy_{year}=datacard_e_LP_vbf_LDy_{year}.txt > combined_e_LDy_{year}.txt
text2workspace.py combined_e_LDy_{year}.txt -o combined_e_LDy_{year}.root
combineCards.py  mu_HP_bb_LDy_{year}=datacard_mu_HP_bb_LDy_{year}.txt  mu_LP_bb_LDy_{year}=datacard_mu_LP_bb_LDy_{year}.txt  mu_HP_nobb_LDy_{year}=datacard_mu_HP_nobb_LDy_{year}.txt  mu_LP_nobb_LDy_{year}=datacard_mu_LP_nobb_LDy_{year}.txt  mu_HP_vbf_LDy_{year}=datacard_mu_HP_vbf_LDy_{year}.txt  mu_LP_vbf_LDy_{year}=datacard_mu_LP_vbf_LDy_{year}.txt > combined_mu_LDy_{year}.txt
text2workspace.py combined_mu_LDy_{year}.txt -o combined_mu_LDy_{year}.root

combineCards.py  e_HP_bb_LDy_{year}=datacard_e_HP_bb_LDy_{year}.txt  mu_HP_bb_LDy_{year}=datacard_mu_HP_bb_LDy_{year}.txt  e_HP_nobb_LDy_{year}=datacard_e_HP_nobb_LDy_{year}.txt  mu_HP_nobb_LDy_{year}=datacard_mu_HP_nobb_LDy_{year}.txt  e_HP_vbf_LDy_{year}=datacard_e_HP_vbf_LDy_{year}.txt  mu_HP_vbf_LDy_{year}=datacard_mu_HP_vbf_LDy_{year}.txt > combined_HP_LDy_{year}.txt
text2workspace.py combined_HP_LDy_{year}.txt -o combined_HP_LDy_{year}.root
combineCards.py  e_LP_bb_LDy_{year}=datacard_e_LP_bb_LDy_{year}.txt  mu_LP_bb_LDy_{year}=datacard_mu_LP_bb_LDy_{year}.txt  e_LP_nobb_LDy_{year}=datacard_e_LP_nobb_LDy_{year}.txt  mu_LP_nobb_LDy_{year}=datacard_mu_LP_nobb_LDy_{year}.txt  e_LP_vbf_LDy_{year}=datacard_e_LP_vbf_LDy_{year}.txt  mu_LP_vbf_LDy_{year}=datacard_mu_LP_vbf_LDy_{year}.txt > combined_LP_LDy_{year}.txt
text2workspace.py combined_LP_LDy_{year}.txt -o combined_LP_LDy_{year}.root
'''


for signal in [
#        'GbuToWW',
#        'RadToWW',
#        'ZprToWW',
#        'WprToWZ',
#        'WprToWH',
#        'VBFGbuToWW',
#        'VBFRadToWW',
        'VBFZprToWW',
#        'VBFWprToWZ',
##        'VBFWprToWH',
]:

    dcFolder = 'Dc'+(('_'+options.region) if options.region!="SR" else '')+'_'+signal+'/'
    os.system('mkdir -p '+dcFolder)

    for year in ['2016','2017','2018']:

        doCards = 'python ../makeCard{tag}.py -y {year} -s {signal} -r {region} 2>&1 | tee log_makeCard{tag}_{year}_{region}_{signal}.txt'.format(tag=options.tag,year=year,signal=signal,region=options.region)
        os.system(doCards)
    
        if options.allcomb:
            os.system(doAllComb.format(year=year))

        os.system('combineCards.py   e_HP_bb_LDy_{year}=datacard_e_HP_bb_LDy_{year}.txt  mu_HP_bb_LDy_{year}=datacard_mu_HP_bb_LDy_{year}.txt  e_LP_bb_LDy_{year}=datacard_e_LP_bb_LDy_{year}.txt  mu_LP_bb_LDy_{year}=datacard_mu_LP_bb_LDy_{year}.txt  e_HP_nobb_LDy_{year}=datacard_e_HP_nobb_LDy_{year}.txt  mu_HP_nobb_LDy_{year}=datacard_mu_HP_nobb_LDy_{year}.txt  e_LP_nobb_LDy_{year}=datacard_e_LP_nobb_LDy_{year}.txt  mu_LP_nobb_LDy_{year}=datacard_mu_LP_nobb_LDy_{year}.txt  e_HP_vbf_LDy_{year}=datacard_e_HP_vbf_LDy_{year}.txt  mu_HP_vbf_LDy_{year}=datacard_mu_HP_vbf_LDy_{year}.txt  e_LP_vbf_LDy_{year}=datacard_e_LP_vbf_LDy_{year}.txt  mu_LP_vbf_LDy_{year}=datacard_mu_LP_vbf_LDy_{year}.txt    e_HP_bb_HDy_{year}=datacard_e_HP_bb_HDy_{year}.txt  mu_HP_bb_HDy_{year}=datacard_mu_HP_bb_HDy_{year}.txt  e_LP_bb_HDy_{year}=datacard_e_LP_bb_HDy_{year}.txt  mu_LP_bb_HDy_{year}=datacard_mu_LP_bb_HDy_{year}.txt  e_HP_nobb_HDy_{year}=datacard_e_HP_nobb_HDy_{year}.txt  mu_HP_nobb_HDy_{year}=datacard_mu_HP_nobb_HDy_{year}.txt  e_LP_nobb_HDy_{year}=datacard_e_LP_nobb_HDy_{year}.txt  mu_LP_nobb_HDy_{year}=datacard_mu_LP_nobb_HDy_{year}.txt  e_HP_vbf_HDy_{year}=datacard_e_HP_vbf_HDy_{year}.txt  mu_HP_vbf_HDy_{year}=datacard_mu_HP_vbf_HDy_{year}.txt  e_LP_vbf_HDy_{year}=datacard_e_LP_vbf_HDy_{year}.txt  mu_LP_vbf_HDy_{year}=datacard_mu_LP_vbf_HDy_{year}.txt   > combined_{year}.txt'.format(year=year))
        os.system('text2workspace.py combined_{year}.txt -o combined_{year}.root'.format(year=year))


    os.system('combineCards.py    e_HP_bb_LDy_2016=datacard_e_HP_bb_LDy_2016.txt  mu_HP_bb_LDy_2016=datacard_mu_HP_bb_LDy_2016.txt  e_LP_bb_LDy_2016=datacard_e_LP_bb_LDy_2016.txt  mu_LP_bb_LDy_2016=datacard_mu_LP_bb_LDy_2016.txt  e_HP_nobb_LDy_2016=datacard_e_HP_nobb_LDy_2016.txt  mu_HP_nobb_LDy_2016=datacard_mu_HP_nobb_LDy_2016.txt  e_LP_nobb_LDy_2016=datacard_e_LP_nobb_LDy_2016.txt  mu_LP_nobb_LDy_2016=datacard_mu_LP_nobb_LDy_2016.txt  e_HP_vbf_LDy_2016=datacard_e_HP_vbf_LDy_2016.txt  mu_HP_vbf_LDy_2016=datacard_mu_HP_vbf_LDy_2016.txt  e_LP_vbf_LDy_2016=datacard_e_LP_vbf_LDy_2016.txt  mu_LP_vbf_LDy_2016=datacard_mu_LP_vbf_LDy_2016.txt    e_HP_bb_HDy_2016=datacard_e_HP_bb_HDy_2016.txt  mu_HP_bb_HDy_2016=datacard_mu_HP_bb_HDy_2016.txt  e_LP_bb_HDy_2016=datacard_e_LP_bb_HDy_2016.txt  mu_LP_bb_HDy_2016=datacard_mu_LP_bb_HDy_2016.txt  e_HP_nobb_HDy_2016=datacard_e_HP_nobb_HDy_2016.txt  mu_HP_nobb_HDy_2016=datacard_mu_HP_nobb_HDy_2016.txt  e_LP_nobb_HDy_2016=datacard_e_LP_nobb_HDy_2016.txt  mu_LP_nobb_HDy_2016=datacard_mu_LP_nobb_HDy_2016.txt  e_HP_vbf_HDy_2016=datacard_e_HP_vbf_HDy_2016.txt  mu_HP_vbf_HDy_2016=datacard_mu_HP_vbf_HDy_2016.txt  e_LP_vbf_HDy_2016=datacard_e_LP_vbf_HDy_2016.txt  mu_LP_vbf_HDy_2016=datacard_mu_LP_vbf_HDy_2016.txt   e_HP_bb_LDy_2017=datacard_e_HP_bb_LDy_2017.txt  mu_HP_bb_LDy_2017=datacard_mu_HP_bb_LDy_2017.txt  e_LP_bb_LDy_2017=datacard_e_LP_bb_LDy_2017.txt  mu_LP_bb_LDy_2017=datacard_mu_LP_bb_LDy_2017.txt  e_HP_nobb_LDy_2017=datacard_e_HP_nobb_LDy_2017.txt  mu_HP_nobb_LDy_2017=datacard_mu_HP_nobb_LDy_2017.txt  e_LP_nobb_LDy_2017=datacard_e_LP_nobb_LDy_2017.txt  mu_LP_nobb_LDy_2017=datacard_mu_LP_nobb_LDy_2017.txt  e_HP_vbf_LDy_2017=datacard_e_HP_vbf_LDy_2017.txt  mu_HP_vbf_LDy_2017=datacard_mu_HP_vbf_LDy_2017.txt  e_LP_vbf_LDy_2017=datacard_e_LP_vbf_LDy_2017.txt  mu_LP_vbf_LDy_2017=datacard_mu_LP_vbf_LDy_2017.txt    e_HP_bb_HDy_2017=datacard_e_HP_bb_HDy_2017.txt  mu_HP_bb_HDy_2017=datacard_mu_HP_bb_HDy_2017.txt  e_LP_bb_HDy_2017=datacard_e_LP_bb_HDy_2017.txt  mu_LP_bb_HDy_2017=datacard_mu_LP_bb_HDy_2017.txt  e_HP_nobb_HDy_2017=datacard_e_HP_nobb_HDy_2017.txt  mu_HP_nobb_HDy_2017=datacard_mu_HP_nobb_HDy_2017.txt  e_LP_nobb_HDy_2017=datacard_e_LP_nobb_HDy_2017.txt  mu_LP_nobb_HDy_2017=datacard_mu_LP_nobb_HDy_2017.txt  e_HP_vbf_HDy_2017=datacard_e_HP_vbf_HDy_2017.txt  mu_HP_vbf_HDy_2017=datacard_mu_HP_vbf_HDy_2017.txt  e_LP_vbf_HDy_2017=datacard_e_LP_vbf_HDy_2017.txt  mu_LP_vbf_HDy_2017=datacard_mu_LP_vbf_HDy_2017.txt   e_HP_bb_LDy_2018=datacard_e_HP_bb_LDy_2018.txt  mu_HP_bb_LDy_2018=datacard_mu_HP_bb_LDy_2018.txt  e_LP_bb_LDy_2018=datacard_e_LP_bb_LDy_2018.txt  mu_LP_bb_LDy_2018=datacard_mu_LP_bb_LDy_2018.txt  e_HP_nobb_LDy_2018=datacard_e_HP_nobb_LDy_2018.txt  mu_HP_nobb_LDy_2018=datacard_mu_HP_nobb_LDy_2018.txt  e_LP_nobb_LDy_2018=datacard_e_LP_nobb_LDy_2018.txt  mu_LP_nobb_LDy_2018=datacard_mu_LP_nobb_LDy_2018.txt  e_HP_vbf_LDy_2018=datacard_e_HP_vbf_LDy_2018.txt  mu_HP_vbf_LDy_2018=datacard_mu_HP_vbf_LDy_2018.txt  e_LP_vbf_LDy_2018=datacard_e_LP_vbf_LDy_2018.txt  mu_LP_vbf_LDy_2018=datacard_mu_LP_vbf_LDy_2018.txt    e_HP_bb_HDy_2018=datacard_e_HP_bb_HDy_2018.txt  mu_HP_bb_HDy_2018=datacard_mu_HP_bb_HDy_2018.txt  e_LP_bb_HDy_2018=datacard_e_LP_bb_HDy_2018.txt  mu_LP_bb_HDy_2018=datacard_mu_LP_bb_HDy_2018.txt  e_HP_nobb_HDy_2018=datacard_e_HP_nobb_HDy_2018.txt  mu_HP_nobb_HDy_2018=datacard_mu_HP_nobb_HDy_2018.txt  e_LP_nobb_HDy_2018=datacard_e_LP_nobb_HDy_2018.txt  mu_LP_nobb_HDy_2018=datacard_mu_LP_nobb_HDy_2018.txt  e_HP_vbf_HDy_2018=datacard_e_HP_vbf_HDy_2018.txt  mu_HP_vbf_HDy_2018=datacard_mu_HP_vbf_HDy_2018.txt  e_LP_vbf_HDy_2018=datacard_e_LP_vbf_HDy_2018.txt  mu_LP_vbf_HDy_2018=datacard_mu_LP_vbf_HDy_2018.txt   > combined.txt')

    os.system('text2workspace.py combined.txt -o combined.root')

    os.system('cp combined.root combined_full.root')
    os.system('cp combined.root combined_Run2.root')

    os.system('\mv datacard* '+dcFolder)
    os.system('\mv comb* '+dcFolder)
    os.system('\mv log_makeCard* '+dcFolder)
