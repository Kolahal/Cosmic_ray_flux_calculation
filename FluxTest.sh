#!/bin/bash

tempfile=$(mktemp test.XXXXX.$1.$2.f90)

cp main-simple.f90 $tempfile

#echo 'tempfile name '$tempfile

#echo 'altitude: '$4

perl -pi -e "s/ip=1 /ip=$3 /g" ${tempfile}
perl -pi -e "s/e=1000.0 /e=$4 /g" ${tempfile}
perl -pi -e "s/glat=30 /glat=$5 /g" ${tempfile}
perl -pi -e "s/Alti=12.0 /Alti=$6 /g" ${tempfile}

gfortran $tempfile subroutines.f90 -o a.${1}.${2}.out

str=$(./a.${1}.${2}.out | grep 'Integrated')

echo $str | awk '{print $NF}' > flux_${1}_${2}.txt
test_var=$(echo $str | awk '{print $NF}')

#echo 'bash:- '$4'     '$5'     '$6'     '$test_var

#export test_var
#echo '---> '${test_var}

#echo '...........................'
rm $tempfile
rm a.${1}.${2}.out
