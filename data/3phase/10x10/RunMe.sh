#!/bin/bash

CDDIR=$PWD
MAINDIR=/Users/olgawodo/MINE/PROJECTS/GraSPI/graspi

# paths to GraSPI and external tools used to pre or post process data
GRASPI=$MAINDIR/src/graspi

# file to analyze 

FILENAME=data_10_10

# run GraSPI analysis 

$GRASPI -a ${FILENAME}.txt -n 3 > ${FILENAME}-a.log 2>&1

