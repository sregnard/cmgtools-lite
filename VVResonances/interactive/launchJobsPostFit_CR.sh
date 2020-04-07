#!/bin/bash

for signal in XWH #XWW XWZ XWH

do

    cd Dc_CR_${signal}/

    for year in Run2 # 2016 2017 2018

    do

        if [ $# -ne 0 ] && [ ${year} != "$1" ]
        then continue
        fi

	mkdir Jobs_prepostfit_${year}
	cd Jobs_prepostfit_${year}

        #:'  ## pre-fit
	mkdir Jobs_PreFit
	cd Jobs_PreFit
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitPostFit.py ../../combined.root -o "-y ${year} --region CR -f 0"
	cd ..
	#'

        #:'  ## post-fit, background only
	mkdir Jobs_PostFit_Bonly
	cd Jobs_PostFit_Bonly
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitPostFit.py ../../combined.root -o "-y ${year} --region CR -r 0"
	cd ..
	#'

        cd ..

    done

    cd ..

done
