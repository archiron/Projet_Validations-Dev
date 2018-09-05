#!/bin/bash

if [ ! $1 ]
then
    echo "use is :  . /eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/validationDev.sh CMSSW_X_Y_Z[_preU]"
    echo "You must use a valid CMSSW release version"
    source scramv1 list
else
    now=$(date +"%Y_%m_%d")
    echo $now
    echo "SCRAM_ARCH : $SCRAM_ARCH"
    RELEASE=$1
    echo "RELEASE : $RELEASE"
    BASEDIR=$(pwd)
    echo "pwd = $BASEDIR"
    /cvmfs/cms.cern.ch/common/scramv1 project CMSSW $RELEASE
    cd $RELEASE/src
    echo "pwd =" $(pwd)
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    eval `scramv1 runtime -sh`
    echo "CMSSW VERSION : $CMSSW_VERSION"

    logic="1"
    while [ $logic = "1" ]
    do
        echo "appel Projet_Validations-PortableDev"
        python /eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/Projet_Validations-PortableDev/main.py
        echo "fin appel Projet_Validations-PortableDev"
        echo "pwd =" $(pwd)
        read -p "(R)eload GUI, Quit (K)eeping folder, Quit (D)eleting folder ? " choice
        echo $choice
        if [ $choice == "R" ] || [ $choice == "r" ]
        then 
            python /eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/Projet_Validations-PortableDev/main.py
            echo "Reload GUI"
        elif [ $choice == "K" ] || [ $choice == "k" ]
        then
            echo "Quit Keeping folder"
            cd ../..
            logic="0"
        elif [ $choice == "D" ] || [ $choice == "d" ] || [ $choice == "q" ]
        then
            echo "Quit Deleting folder"
            cd ../..
            rm -Rf $RELEASE
            logic="0"
        else
            echo "no choice, Keeping folder"
        fi
    done
fi

echo "Fin."
