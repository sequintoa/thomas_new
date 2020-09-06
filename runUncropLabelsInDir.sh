#!/bin/bash

topDirName=$1

## Array of nuclei strings
declare -a nucleiArr=("1-THALAMUS" "2-AV" "4-VA" "5-VLa" "6-VLP" "7-VPL" "8-Pul" "9-LGN" "10-MGN" "11-CM" "12-MD-Pf" "13-Hb" "14-MTT")

thomasOutDirL=/left
thomasOutDirR=/right

for dirName in $topDirName/* ; do
    segDirL="${dirName}/${thomasOutDirL}/"
    segDirR="${dirName}/${thomasOutDirR}/"
    
    if [ -d "${segDirL}" ]; then
        echo "Running uncrop in $segDirL: "

        outDirL="${dirName}/uncrop_left/"
        mkdir -p ${outDirL}

	## now loop through the above array
	for i in "${nucleiArr[@]}"
	do
	   #echo "Loop index:" "$i"
	   inpFname="${segDirL}${i}.nii.gz"
	   #echo "Processing" "$inpFname"
	   outFname="${outDirL}${i}.nii.gz"
	   uncrop.py ${inpFname} ${outFname} "${segDirL}mask_inp.nii.gz"
	done
        inpFname="${segDirL}thomas.nii.gz"
        #echo "Processing" "$inpFname"
        outFname="${outDirL}thomas.nii.gz"
        uncrop.py ${inpFname} ${outFname} "${segDirL}mask_inp.nii.gz"
    else 
        echo "$segDirL does not exist"
    fi

    if [ -d "${segDirR}" ]; then
        echo "Running uncrop in $segDirR: "

        outDirR="${dirName}/uncrop_right/"
        mkdir -p ${outDirR}

	## now loop through the above array
	for i in "${nucleiArr[@]}"
	do
	   #echo "Loop index:" "$i"
	   inpFname="${segDirR}${i}.nii.gz"
	   #echo "Processing" "$inpFname"
	   outFname="${outDirR}${i}.nii.gz"
	   uncrop.py ${inpFname} ${outFname} "${segDirR}mask_inp.nii.gz"
	done
        inpFname="${segDirR}thomas.nii.gz"
        #echo "Processing" "$inpFname"
        outFname="${outDirR}thomas.nii.gz"
        uncrop.py ${inpFname} ${outFname} "${segDirR}mask_inp.nii.gz"
    else 
        echo "$segDirR does not exist"
    fi
done

