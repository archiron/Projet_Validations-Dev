#!/bin/bash

now=$(date +"%Y_%m_%d")
echo $now
echo $CMSSW_VERSION
RELEASE='CMSSW_10_0_0_pre1'
echo "RELEASE : $RELEASE"
BASEDIR=$(pwd)
echo "pwd = $BASEDIR"

if $CMSSW_VERSION
then
    echo "no CMSSW VERSION"
    /cvmfs/cms.cern.ch/common/scramv1 project CMSSW $RELEASE
    cd $RELEASE/src
    echo "pwd =" $(pwd)
    source /afs/cern.ch/cms/cmsset_default.sh
    eval `scramv1 runtime -sh`
    echo "CMSSW VERSION : $CMSSW_VERSION"
    echo "appel Projet_Validations-Dev"
    python ~/lbin/Projet_Validations-Dev/main.py
    echo "fin appel Projet_Validations-Dev"
    cd ../..
    echo "pwd =" $(pwd)
    rm -Rf $RELEASE
else
    echo "CMSSW VERSION : $CMSSW_VERSION"
    python ~/lbin/Projet_CheckRootFiles/main.py
fi
