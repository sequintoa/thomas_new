#!/bin/bash

topDirName=/array/hdd/maheshbk/tools/thomas_wip/data
#topDirName=$1

# if wmn processing then tag = 1, for csfn tag = 2
contrastTag=1

if [ $contrastTag -eq 1 ]; then
    fdirString=wmn
    fnameString=wmn_bc.nii.gz
fi 

if [ $contrastTag -eq 2 ]; then
    fnameString=csfn.nii.gz
fi

for dirName in $topDirName/* ; do
    fname=$dirName/$fnameString

    if [ -f "$fname" ]; then
        echo "Running thomas in $fname: "
        newDirName=$dirName
	cd $newDirName
        thomas_csh_big $fnameString r
    else 
        echo "$fname does not exist"
    fi
done

$THOMASDIR/runUncropLabelsInDir.sh $topDirName
