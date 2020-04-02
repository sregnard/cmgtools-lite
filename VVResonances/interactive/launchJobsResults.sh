#!/bin/bash

for signal in XWW XWZ XWH

do

    cd Dc_${signal}/

    #for card in bb_e_HP bb_e_LP bb_mu_HP bb_mu_LP nobb_e_HP nobb_e_LP nobb_mu_HP nobb_mu_LP bb_e bb_mu nobb_e nobb_mu bb_HP bb_LP nobb_HP nobb_LP e_HP e_LP mu_HP mu_LP bb nobb e mu HP LP full  
    for card in 2016 2017 full 

    do

	mkdir Jobs_${card}
	cd Jobs_${card}

	mkdir Jobs_Limits
	cd Jobs_Limits
	#python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 50 -m 1000 -M 4500 -q condor -o '-M Asymptotic --rAbsAcc=0.00001' ../../combined_$card.root
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 4500 -q condor -o '-M Asymptotic --rAbsAcc=0.00001' ../../combined_$card.root
	cd ..
	
	#mkdir Jobs_pvalue_obs
	#cd Jobs_pvalue_obs
        #python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 10 -m 1000 -M 4500 -q condor -o '--signif --pvalue' ../../combined_$card.root
        #python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 50 -m 1000 -M 4500 -q condor -o '--signif --pvalue' ../../combined_$card.root
        #cd ..
	
	cd ..
	
    done
    
    cd ..
    
done
