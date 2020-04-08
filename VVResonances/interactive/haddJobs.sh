#!/bin/bash

for signal in XWW XWZ XWH

do 

    if [ $# -ne 0 ] && [ ${signal} != "$1" ]
    then continue
    fi

    cd Dc_${signal}/

    #for card in bb_e_HP bb_e_LP bb_mu_HP bb_mu_LP nobb_e_HP nobb_e_LP nobb_mu_HP nobb_mu_LP bb_e bb_mu nobb_e nobb_mu bb_HP bb_LP nobb_HP nobb_LP e_HP e_LP mu_HP mu_LP bb nobb e mu HP LP full 
    #for card in 2016 2017 2018
    for card in full 

    do

	cd Jobs_results_${card}

	#: '
	cd Jobs_Limits
	pwd
	hadd -f merged.higgsCombineTest.Asymptotic.root higgsCombineTest.Asymptotic.mH*.root
	cd ..
	#'

        : '  
	cd Jobs_pvalue_obs
	pwd
	hadd -f merged.higgsCombineTest.ProfileLikelihood.root higgsCombineTest.ProfileLikelihood.mH*.root
	cd ..
        #'

        : '  
	cd Jobs_SanityCheck_1000
	pwd
	hadd -f merged.higgsCombineTest.MaxLikelihoodFit.root higgsCombineTest.MaxLikelihoodFit.mH*.root
	cd ..
        #'

        : '  
	cd Jobs_Saturated
	pwd
	hadd -f merged.higgsCombineTest.GoodnessOfFit.root higgsCombineTest.GoodnessOfFit.mH*.root
	cd ..
	cd Jobs_Saturated_toys
	pwd
	hadd -f merged.higgsCombineTest.GoodnessOfFit.root higgsCombineTest.GoodnessOfFit.mH*.root
	cd ..
	hadd -f mergedSaturated.root Jobs_Saturated/higgsCombineTest.GoodnessOfFit.mH*.root Jobs_Saturated_toys/higgsCombineTest.GoodnessOfFit.mH*.root
        #'

	cd ..
	
    done
    
    cd ..
    
done
