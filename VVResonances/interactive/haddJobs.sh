#!/bin/bash

for signal in XWW XWZ XWH
do 

    cd Dc_${signal}/

    #for card in e_HP e_LP mu_HP mu_LP e mu HP LP #full 
    for card in 2016 2017 full 

    do

	cd Jobs_${card}

	cd Jobs_Limits
	pwd
	hadd -f merged.higgsCombineTest.Asymptotic.root higgsCombineTest.Asymptotic.mH*.root
	cd ..

	#cd Jobs_pvalue_obs
	#pwd
	#hadd -f merged.higgsCombineTest.ProfileLikelihood.root higgsCombineTest.ProfileLikelihood.mH*.root
	#cd ..
	
	cd ..
	
    done
    
    cd ..
    
done