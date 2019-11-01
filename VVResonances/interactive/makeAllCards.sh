#!/bin/bash

for signal in XWW XWZ XWH
do

    for year in 2016 2017 2018
    do

	if [ $# -ne 0 ] && [ ${year} != "$1" ]
	then continue
	fi

	python ../makeCard.py -y ${year} -s ${signal} -c bb -b 2>&1 | tee log_makeCard_${year}_${signal}.txt


	: '
	text2workspace.py datacard_bb_e_HP_${year}.txt -o combined_bb_e_HP_${year}.root
	text2workspace.py datacard_bb_e_LP_${year}.txt -o combined_bb_e_LP_${year}.root
	text2workspace.py datacard_bb_mu_HP_${year}.txt -o combined_bb_mu_HP_${year}.root
	text2workspace.py datacard_bb_mu_LP_${year}.txt -o combined_bb_mu_LP_${year}.root
	text2workspace.py datacard_nobb_e_HP_${year}.txt -o combined_nobb_e_HP_${year}.root
	text2workspace.py datacard_nobb_e_LP_${year}.txt -o combined_nobb_e_LP_${year}.root
	text2workspace.py datacard_nobb_mu_HP_${year}.txt -o combined_nobb_mu_HP_${year}.root
	text2workspace.py datacard_nobb_mu_LP_${year}.txt -o combined_nobb_mu_LP_${year}.root
	
	combineCards.py  bb_e_HP_${year}=datacard_bb_e_HP_${year}.txt  bb_e_LP_${year}=datacard_bb_e_LP_${year}.txt > combined_bb_e_${year}.txt
	text2workspace.py combined_bb_e_${year}.txt -o combined_bb_e_${year}.root
	combineCards.py  nobb_e_HP_${year}=datacard_nobb_e_HP_${year}.txt  nobb_e_LP_${year}=datacard_nobb_e_LP_${year}.txt > combined_nobb_e_${year}.txt
	text2workspace.py combined_nobb_e_${year}.txt -o combined_nobb_e_${year}.root
	combineCards.py  bb_mu_HP_${year}=datacard_bb_mu_HP_${year}.txt  bb_mu_LP_${year}=datacard_bb_mu_LP_${year}.txt > combined_bb_mu_${year}.txt
	text2workspace.py combined_bb_mu_${year}.txt -o combined_bb_mu_${year}.root
	combineCards.py  nobb_mu_HP_${year}=datacard_nobb_mu_HP_${year}.txt  nobb_mu_LP_${year}=datacard_nobb_mu_LP_${year}.txt > combined_nobb_mu_${year}.txt
	text2workspace.py combined_nobb_mu_${year}.txt -o combined_nobb_mu_${year}.root
	
	combineCards.py  bb_e_HP_${year}=datacard_bb_e_HP_${year}.txt  bb_mu_HP_${year}=datacard_bb_mu_HP_${year}.txt > combined_bb_HP_${year}.txt
	text2workspace.py combined_bb_HP_${year}.txt -o combined_bb_HP_${year}.root
	combineCards.py  bb_e_LP_${year}=datacard_bb_e_LP_${year}.txt  bb_mu_LP_${year}=datacard_bb_mu_LP_${year}.txt > combined_bb_LP_${year}.txt
	text2workspace.py combined_bb_LP_${year}.txt -o combined_bb_LP_${year}.root
	combineCards.py  nobb_e_HP_${year}=datacard_nobb_e_HP_${year}.txt  nobb_mu_HP_${year}=datacard_nobb_mu_HP_${year}.txt > combined_nobb_HP_${year}.txt
	text2workspace.py combined_nobb_HP_${year}.txt -o combined_nobb_HP_${year}.root
	combineCards.py  nobb_e_LP_${year}=datacard_nobb_e_LP_${year}.txt  nobb_mu_LP_${year}=datacard_nobb_mu_LP_${year}.txt > combined_nobb_LP_${year}.txt
	text2workspace.py combined_nobb_LP_${year}.txt -o combined_nobb_LP_${year}.root
	
	combineCards.py  bb_e_HP_${year}=datacard_bb_e_HP_${year}.txt  nobb_e_HP_${year}=datacard_nobb_e_HP_${year}.txt > combined_e_HP_${year}.txt
	text2workspace.py combined_e_HP_${year}.txt -o combined_e_HP_${year}.root
	combineCards.py  bb_e_LP_${year}=datacard_bb_e_LP_${year}.txt  nobb_e_LP_${year}=datacard_nobb_e_LP_${year}.txt > combined_e_LP_${year}.txt
	text2workspace.py combined_e_LP_${year}.txt -o combined_e_LP_${year}.root
	combineCards.py  bb_mu_HP_${year}=datacard_bb_mu_HP_${year}.txt  nobb_mu_HP_${year}=datacard_nobb_mu_HP_${year}.txt > combined_mu_HP_${year}.txt
	text2workspace.py combined_mu_HP_${year}.txt -o combined_mu_HP_${year}.root
	combineCards.py  bb_mu_LP_${year}=datacard_bb_mu_LP_${year}.txt  nobb_mu_LP_${year}=datacard_nobb_mu_LP_${year}.txt > combined_mu_LP_${year}.txt
	text2workspace.py combined_mu_LP_${year}.txt -o combined_mu_LP_${year}.root
	
	combineCards.py  bb_e_HP_${year}=datacard_bb_e_HP_${year}.txt  bb_mu_HP_${year}=datacard_bb_mu_HP_${year}.txt  bb_e_LP_${year}=datacard_bb_e_LP_${year}.txt  bb_mu_LP_${year}=datacard_bb_mu_LP_${year}.txt > combined_bb_${year}.txt
	text2workspace.py combined_bb_${year}.txt -o combined_bb_${year}.root
	combineCards.py  nobb_e_HP_${year}=datacard_nobb_e_HP_${year}.txt  nobb_mu_HP_${year}=datacard_nobb_mu_HP_${year}.txt  nobb_e_LP_${year}=datacard_nobb_e_LP_${year}.txt  nobb_mu_LP_${year}=datacard_nobb_mu_LP_${year}.txt > combined_nobb_${year}.txt
	text2workspace.py combined_nobb_${year}.txt -o combined_nobb_${year}.root
	
	combineCards.py  bb_e_HP_${year}=datacard_bb_e_HP_${year}.txt  bb_e_LP_${year}=datacard_bb_e_LP_${year}.txt  nobb_e_HP_${year}=datacard_nobb_e_HP_${year}.txt  nobb_e_LP_${year}=datacard_nobb_e_LP_${year}.txt > combined_e_${year}.txt
	text2workspace.py combined_e_${year}.txt -o combined_e_${year}.root
	combineCards.py  bb_mu_HP_${year}=datacard_bb_mu_HP_${year}.txt  bb_mu_LP_${year}=datacard_bb_mu_LP_${year}.txt  nobb_mu_HP_${year}=datacard_nobb_mu_HP_${year}.txt  nobb_mu_LP_${year}=datacard_nobb_mu_LP_${year}.txt > combined_mu_${year}.txt
	text2workspace.py combined_mu_${year}.txt -o combined_mu_${year}.root
	
	combineCards.py  bb_e_HP_${year}=datacard_bb_e_HP_${year}.txt  bb_mu_HP_${year}=datacard_bb_mu_HP_${year}.txt  nobb_e_HP_${year}=datacard_nobb_e_HP_${year}.txt  nobb_mu_HP_${year}=datacard_nobb_mu_HP_${year}.txt > combined_HP_${year}.txt
	text2workspace.py combined_HP_${year}.txt -o combined_HP_${year}.root
	combineCards.py  bb_e_LP_${year}=datacard_bb_e_LP_${year}.txt  bb_mu_LP_${year}=datacard_bb_mu_LP_${year}.txt  nobb_e_LP_${year}=datacard_nobb_e_LP_${year}.txt  nobb_mu_LP_${year}=datacard_nobb_mu_LP_${year}.txt > combined_LP_${year}.txt
	text2workspace.py combined_LP_${year}.txt -o combined_LP_${year}.root
	#'

	combineCards.py  bb_e_HP_${year}=datacard_bb_e_HP_${year}.txt  bb_mu_HP_${year}=datacard_bb_mu_HP_${year}.txt  bb_e_LP_${year}=datacard_bb_e_LP_${year}.txt  bb_mu_LP_${year}=datacard_bb_mu_LP_${year}.txt  nobb_e_HP_${year}=datacard_nobb_e_HP_${year}.txt  nobb_mu_HP_${year}=datacard_nobb_mu_HP_${year}.txt  nobb_e_LP_${year}=datacard_nobb_e_LP_${year}.txt  nobb_mu_LP_${year}=datacard_nobb_mu_LP_${year}.txt > combined_${year}.txt
	text2workspace.py combined_${year}.txt -o combined_${year}.root
	
    done

    if [ $# -eq 0 ] 
    then
	combineCards.py    bb_e_HP_2016=datacard_bb_e_HP_2016.txt  bb_mu_HP_2016=datacard_bb_mu_HP_2016.txt  bb_e_LP_2016=datacard_bb_e_LP_2016.txt  bb_mu_LP_2016=datacard_bb_mu_LP_2016.txt  nobb_e_HP_2016=datacard_nobb_e_HP_2016.txt  nobb_mu_HP_2016=datacard_nobb_mu_HP_2016.txt  nobb_e_LP_2016=datacard_nobb_e_LP_2016.txt  nobb_mu_LP_2016=datacard_nobb_mu_LP_2016.txt      bb_e_HP_2017=datacard_bb_e_HP_2017.txt  bb_mu_HP_2017=datacard_bb_mu_HP_2017.txt  bb_e_LP_2017=datacard_bb_e_LP_2017.txt  bb_mu_LP_2017=datacard_bb_mu_LP_2017.txt  nobb_e_HP_2017=datacard_nobb_e_HP_2017.txt  nobb_mu_HP_2017=datacard_nobb_mu_HP_2017.txt  nobb_e_LP_2017=datacard_nobb_e_LP_2017.txt  nobb_mu_LP_2017=datacard_nobb_mu_LP_2017.txt      bb_e_HP_2018=datacard_bb_e_HP_2018.txt  bb_mu_HP_2018=datacard_bb_mu_HP_2018.txt  bb_e_LP_2018=datacard_bb_e_LP_2018.txt  bb_mu_LP_2018=datacard_bb_mu_LP_2018.txt  nobb_e_HP_2018=datacard_nobb_e_HP_2018.txt  nobb_mu_HP_2018=datacard_nobb_mu_HP_2018.txt  nobb_e_LP_2018=datacard_nobb_e_LP_2018.txt  nobb_mu_LP_2018=datacard_nobb_mu_LP_2018.txt    > combined.txt

	text2workspace.py combined.txt -o combined.root

	cp combined.root combined_full.root
    fi
	
    mkdir -p Dc_${signal}/

    \mv datacard* Dc_${signal}/
    \mv comb* Dc_${signal}/
    \mv log_makeCard* Dc_${signal}/

done
