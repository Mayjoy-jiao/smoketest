#!/bin/bash

i=1 
while [ $i -lt 10000 ]
do
       python runAll.py	
       i=$(expr $i + 1)
done
