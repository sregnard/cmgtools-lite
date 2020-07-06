#!/bin/bash

for signal in GbuToWW RadToWW ZprToWW WprToWZ WprToWH VBFGbuToWW VBFRadToWW VBFZprToWW VBFWprToWZ

do

    cd Dc_${signal}/

    #for card in bb_e_HP bb_e_LP bb_mu_HP bb_mu_LP nobb_e_HP nobb_e_LP nobb_mu_HP nobb_mu_LP vbf_e_HP vbf_e_LP vbf_mu_HP vbf_mu_LP bb_e bb_mu nobb_e nobb_mu vbf_e vbf_mu bb_HP bb_LP nobb_HP nobb_LP vbf_HP vbf_LP e_HP e_LP mu_HP mu_LP bb nobb vbf e mu HP LP full
    #for card in bb_e_HP bb_e_LP bb_mu_HP bb_mu_LP nobb_e_HP nobb_e_LP nobb_mu_HP nobb_mu_LP vbf_e_HP vbf_e_LP vbf_mu_HP vbf_mu_LP
    #for card in 2016 2017 2018
    for card in full 

    do

        if [ $# -ne 0 ] && [ ${card} != "$1" ]
        then continue
        fi

	mkdir -p Jobs_results_${card}
	cd Jobs_results_${card}

	#:'
	mkdir Jobs_Limits
	cd Jobs_Limits
	#python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 50 -m 1000 -M 4500 -q condor -o "-M Asymptotic --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" ../../combined_$card.root
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 4500 -q condor -o "-M Asymptotic --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" ../../combined_$card.root
	cd ..
	#'

	:'
	mkdir Jobs_pvalue_obs
	cd Jobs_pvalue_obs
	#python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 10 -m 1000 -M 4500 -q condor -o "--signif --pvalue" ../../combined_$card.root
        python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 50 -m 1000 -M 4500 -q condor -o "--signif --pvalue" ../../combined_$card.root
        cd ..
	#'

	:'
	mkdir Jobs_BiasTestNoInjectedSignal_1000
	cd Jobs_BiasTestNoInjectedSignal_1000
	for n in `seq 1 10`
	do
	    python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 4500 -q condor -t 2880 -o "-M MaxLikelihoodFit -t 100 -s -1 --rMin=-1000 --rMax=1000" ../../combined_$card.root
	done
	cd ..
	#'

	#:'
	mkdir Jobs_BiasTestInject2sigma_1000
	cd Jobs_BiasTestInject2sigma_1000
	for n in `seq 1 10`
	do
	    python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 500 -m 1000 -M 4500 --injectSignal ${signal}2sigma -q condor -t 2880 -o "-M MaxLikelihoodFit -t 100 -s -1 --rMin=-1000 --rMax=1000" ../../combined_$card.root
	done
	cd ..
	#'
	#:'
	mkdir Jobs_BiasTestInject5sigma_1000
	cd Jobs_BiasTestInject5sigma_1000
	for n in `seq 1 10`
	do
	    python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 500 -m 1000 -M 4500 --injectSignal ${signal}5sigma -q condor -t 2880 -o "-M MaxLikelihoodFit -t 100 -s -1 --rMin=-1000 --rMax=1000" ../../combined_$card.root
	done
	cd ..
	#'

	:'
	mkdir Jobs_Saturated
	cd Jobs_Saturated
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 1000 -q condor -o "-M GoodnessOfFit --algorithm saturated" ../../combined_$card.root
	cd ..
	mkdir Jobs_Saturated_toys
	cd Jobs_Saturated_toys
	for n in `seq 1 100`
        do
	    python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 1000 -q condor -o "-M GoodnessOfFit --algorithm saturated -t 10 -s -1" ../../combined_$card.root
	done
	cd ..
	#'

	cd ..
	
    done
    
    cd ..
    
done
