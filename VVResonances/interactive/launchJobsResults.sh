#!/bin/bash

for signal in GbuToWW RadToWW ZprToWW WprToWZ WprToWH VBFGbuToWW VBFRadToWW VBFZprToWW VBFWprToWZ
#for signal in GbuToWW
#for signal in WprToWH
#for signal in VBFZprToWW #ZprToWW

do

    cd Dc_${signal}/

    #for card in e_HP_bb_LDy e_HP_bb_HDy e_HP_nobb_LDy e_HP_nobb_HDy e_HP_vbf_LDy e_HP_vbf_HDy e_LP_bb_LDy e_LP_bb_HDy e_LP_nobb_LDy e_LP_nobb_HDy e_LP_vbf_LDy e_LP_vbf_HDy mu_HP_bb_LDy mu_HP_bb_HDy mu_HP_nobb_LDy mu_HP_nobb_HDy mu_HP_vbf_LDy mu_HP_vbf_HDy mu_LP_bb_LDy mu_LP_bb_HDy mu_LP_nobb_LDy mu_LP_nobb_HDy mu_LP_vbf_LDy mu_LP_vbf_HDy full
    #for card in e_HP_bb_LDy e_HP_bb_HDy e_HP_nobb_LDy e_HP_nobb_HDy e_HP_vbf_LDy e_HP_vbf_HDy e_LP_bb_LDy e_LP_bb_HDy e_LP_nobb_LDy e_LP_nobb_HDy e_LP_vbf_LDy e_LP_vbf_HDy mu_HP_bb_LDy mu_HP_bb_HDy mu_HP_nobb_LDy mu_HP_nobb_HDy mu_HP_vbf_LDy mu_HP_vbf_HDy mu_LP_bb_LDy mu_LP_bb_HDy mu_LP_nobb_LDy mu_LP_nobb_HDy mu_LP_vbf_LDy mu_LP_vbf_HDy
    #for card in 2016 2017 2018 full
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
	#python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 50 -m 1000 -M 4500 -q condor -o "-M AsymptoticLimits --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" ../../combined_$card.root
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 4500 -q condor -o "-M AsymptoticLimits --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" ../../combined_$card.root
	#python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 4500 -q condor -o "-M AsymptoticLimits --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" -t 2880 ../../combined_$card.root
	cd ..
	#'

	:'
	mkdir Jobs_pvalue_obs
	cd Jobs_pvalue_obs
	#python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 10 -m 1000 -M 4500 -q condor -o "-M Significance" ../../combined_$card.root
        python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 50 -m 1000 -M 4500 -q condor -o "-M Significance" ../../combined_$card.root
        cd ..
	#'

	:'
	mkdir Jobs_BiasTestNoInjectedSignal_1000
	cd Jobs_BiasTestNoInjectedSignal_1000
	for n in `seq 1 10`
	do
	    python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 100 -m 1000 -M 4500 -q condor -t 2880 -o "-M FitDiagnostics -t 100 -s -1 --rMin=-1000 --rMax=1000" ../../combined_$card.root
	done
	cd ..
	#'

	:'
	mkdir Jobs_BiasTestInject2sigma_1000
	cd Jobs_BiasTestInject2sigma_1000
	for n in `seq 1 10`
	do
	    python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 500 -m 1000 -M 4500 --injectSignal ${signal}2sigma -q condor -t 2880 -o "-M FitDiagnostics -t 100 -s -1 --rMin=-1000 --rMax=1000" ../../combined_$card.root
	done
	cd ..
	#'
	:'
	mkdir Jobs_BiasTestInject5sigma_1000
	cd Jobs_BiasTestInject5sigma_1000
	for n in `seq 1 10`
	do
	    python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 500 -m 1000 -M 4500 --injectSignal ${signal}5sigma -q condor -t 2880 -o "-M FitDiagnostics -t 100 -s -1 --rMin=-1000 --rMax=1000" ../../combined_$card.root
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

	## tests of Asymptotic vs toys
	:'
	mkdir Jobs_Limits_Asymptotic
	cd Jobs_Limits_Asymptotic
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 3500 -m 1000 -M 4500 -q condor -o "-M AsymptoticLimits --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" ../../combined_$card.root
	cd ..
	#'
	:'
	mkdir Jobs_Limits_fullCLs_observed
	cd Jobs_Limits_fullCLs_observed
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 3500 -m 1000 -M 4500 -q condor -t 10000 -o "-M HybridNew --LHCmode LHC-limits --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" ../../combined_$card.root
	cd ..
	#'
	:'
	mkdir Jobs_Limits_fullCLs_expected0p5
	cd Jobs_Limits_fullCLs_expected0p5
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitLimits.py -s 3500 -m 1000 -M 4500 -q condor -t 10000 -o "-M HybridNew --LHCmode LHC-limits --expectedFromGrid=0.5 --rAbsAcc=0.00001 --rMin=1e-6 --rMax=0.01" ../../combined_$card.root
	cd ..
	#'

	cd ..
	
    done
    
    cd ..
    
done
