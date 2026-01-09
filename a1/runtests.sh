#!/bin/bash

for iter in `seq 10`
do 
	echo Test $iter | tee -a  REPORT1.txt

	for i in `seq 10`
	do 
		./Test$iter.py >> REPORT1.txt
		sleep 3
	done

	echo >> REPORT1.TXT
done 

