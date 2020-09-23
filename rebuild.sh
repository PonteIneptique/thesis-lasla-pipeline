#!/bin/bash

ALREADY_GENERATED = $1

for file in ./*.xml;
 do
  if [ $file != $ALREADY_GENERATED ]; 
  	then protogenie rebuild $file memory_protogenie_classic.csv --output ${file%.xml}/ && protogenie concat $file ${file%.xml};
  fi
 done
