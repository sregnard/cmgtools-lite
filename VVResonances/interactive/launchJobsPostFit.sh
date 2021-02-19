#!/bin/bash

for signal in GbuToWW
#for signal in WprToWH
#for signal in VBFZprToWW
#for signal in GbuToWW RadToWW ZprToWW WprToWZ WprToWH VBFGbuToWW VBFRadToWW VBFZprToWW VBFWprToWZ

do

    cd Dc_${signal}/

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
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitPostFit.py ../../combined_full.root -o "-y ${year} -f 0"
	cd ..
	#'

        #:'  ## post-fit, background only
	mkdir Jobs_PostFit_Bonly
	cd Jobs_PostFit_Bonly
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitPostFit.py ../../combined_full.root -o "-y ${year} -r 0"
	cd ..
	#'

        :'  ## post-fit, signal+background (mX=1000)
	mkdir Jobs_PostFit_${signal}1000
	cd Jobs_PostFit_${signal}1000
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitPostFit.py ../../combined_full.root -o "-y ${year} -s ${signal} -m 1000"
	cd ..
	#'
        :'  ## post-fit, signal+background (mX=1500)
	mkdir Jobs_PostFit_${signal}1500
	cd Jobs_PostFit_${signal}1500
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitPostFit.py ../../combined_full.root -o "-y ${year} -s ${signal} -m 1500"
	cd ..
	#'

        :'  ## post-fit, background only, display shape uncertainties (very long)
	mkdir Jobs_PostFit_Bonly_ShapeUnc
	cd Jobs_PostFit_Bonly_ShapeUnc
	python $CMSSW_BASE/src/CMGTools/VVResonances/scripts/vvSubmitPostFit.py ../../combined_full.root -o "-y ${year} -r 0 -u 1"
	cd ..
	#'

        cd ..

    done

    cd ..

done
