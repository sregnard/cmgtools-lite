import os, sys
import ROOT

import optparse
parser = optparse.OptionParser()
#parser.add_option("-t","--tag",dest="tag",default='',help="makeCard tag")
parser.add_option("-r","--region",dest="region",default='CR',help="signal region (SR) or control region (CR)")
(options,args) = parser.parse_args()


for signal in ['XWW']: #['XWW','XWZ','XWH']:

    for year in ['2016','2017','2018','Run2']:

        dcFolder = 'Dc'+(('_'+options.region) if options.region!="SR" else '')+'_'+signal+'_'+year+'/'
        os.system('mkdir -p '+dcFolder)

        #doCards = 'python ../makeCard_measureVtagSF_{tag}.py -y {year}  -s {signal} -r {region} 2>&1 | tee log_makeCard_{tag}_{year}_{region}_{signal}.txt'.format(tag=options.tag,year=year,signal=signal,region=options.region)
        doCards = 'python ../makeCard_measureVtagSF.py -y {year} -s {signal} -r {region} 2>&1 | tee log_makeCard_{year}_{region}_{signal}.txt'.format(year=year,signal=signal,region=options.region)
        os.system(doCards)
    
        os.system('combineCards.py  allC_allL_HP_{year}=datacard_allC_allL_HP_{year}.txt  allC_allL_LP_{year}=datacard_allC_allL_LP_{year}.txt  > combined_{year}.txt'.format(year=year))
        os.system('text2workspace.py combined_{year}.txt -o combined_{year}.root'.format(year=year))
    
        #os.system('cp combined.root combined_full.root')
        #os.system('cp combined.root combined_Run2.root')
    
        os.system('\mv datacard* '+dcFolder)
        os.system('\mv comb* '+dcFolder)
        os.system('\mv log_makeCard* '+dcFolder)

