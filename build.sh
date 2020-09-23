#!/bin/sh
# coding: utf-8

Split=$1
Protogenie=~/dev/ppa-data-splitter/env/bin/protogenie
LASLA_CONVERTER=~/dev/lasla-converter/cli.py
Python=python3

# Step 0: From APN to TSV
$Python $LASLA_CONVERTER convert LASLA-SOURCE-APN LASLA-CONVERTED-TSV --apn

# Step 1 : Protogenie

mkdir OUTPUT/step-01
$Protogenie build step-01/protogenie-config.xml --output OUTPUT/step-01/ --clear --verbose $1
if [ $Split != "--no-split" ]; 
	then $Protogenie concat step-01/protogenie-config.xml OUTPUT/step-01/;
fi

# Step 2: Tenses
$Python step-02/decomposed-tense.py 

# Step 3: Numeric + Clitics
$Python step-03/GlueClitics.py