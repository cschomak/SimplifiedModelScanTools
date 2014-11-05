#!/bin/bash

REGIONS="$(< Regions.txt)" #names from names.txt file
BINS="$(< Bins.txt)" #names from names.txt file
MASSES="$(< masses.txt)" #names from names.txt file 
for REGION in $REGIONS; do
	echo $REGION
	for BIN in $BINS; do
		echo $BIN
		for MASS in $MASSES; do
			echo $MASS
			python produceSystematicsSignal8TeV.py $REGION $BIN $MASS
		done
	done
done
