@#! /usr/bin/env python
#-*-coding: utf-8 -*-

# A new presentation/use is made in order to use very precisely the DataSets.
# You can add a DataSet inside a given function and look what happened for only the considerated Datatsets.
# This seems more efficient than use "hard coding" and complex search function for the separate cases.

# new way to load datasets items into the menu. datasets are presented as [name, True/False] with True/False the default choice to be checked or not.

import re
from getEnv import env
from Paths_default import *

def DataSetsFilter(self):
    import sys
    fieldname=self.validationType1
    fieldname = fieldname + self.validationType2
    print("fieldname=%s") % fieldname
    table=getattr(sys.modules[__name__], "DataSetsFilter_%s" % fieldname)(self)
    
    return table

def DataSetsFilter_FullRECO(self):
    print "Full"
    table=[
    ["SingleElectronPt10", 1], # 1 : displayed
    ["SingleElectronPt10_UP15", 1], 
    ["SingleElectronPt35", 1],
    ["SingleElectronPt35_UP15", 0], # 0 : not displayed
    ["SingleElectronPt1000", 1],
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastRECO(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FullPU(self):
    print "Full"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastPU(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_Fullpmx(self):
    print "Full"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_Fastpmx(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FullminiAOD(self):
    print "Full"
    table=[
    ["SingleElectronPt10", 1],
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastminiAOD(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def extractDatasets(self):
    extraction = ""
    extractionDisplay = ""
    # display of the datasets strings
    print "datasets release   : ", self.selectedRelDatasets
    print "datasets reference : ", self.selectedRefDatasets
    # cutting self.selectedRelDatasets
    cuttedRelease = str(self.selectedRelDatasets).split(',')
    print "cuttedRelease : ", cuttedRelease
    # searching in self.selectedRefDatasets
    for elem in cuttedRelease:
        print elem
        if re.search(elem, self.selectedRefDatasets):
            print "OK"
            extraction += ', ' + elem
            extractionDisplay += ', ' + "<font color = \"blue\">" + elem + "</font>"
        else:
            print "KO"
            extractionDisplay += ', ' + elem

    extraction = extraction[2:]
    extractionDisplay = extractionDisplay[2:]
    
    return extraction, extractionDisplay
    
def extractDatasetsFastvsFull(self): # do not verify if checkFastvsFull(self) !! MUST be called inside a if(checkFastvsFull(self)): !!
    extractionFastvsFull = ""
    extractionFastvsFullDisplay = ""
    # display of the datasets strings
    print "datasets release   : ", self.selectedRelDatasets
    print "datasets reference : ", self.selectedFvsFDatasets
    # cutting self.selectedRelDatasets
    cuttedRelease = str(self.selectedRelDatasets).split(',')
    print "cuttedRelease : ", cuttedRelease
    # searching in self.selectedFvsFDatasets
    for elem in cuttedRelease:
        print elem
        if re.search(elem, self.selectedFvsFDatasets):
            print "OK"
            extractionFastvsFull += ', ' + elem
            extractionFastvsFullDisplay += ', ' + "<font color = \"blue\">" + elem + "</font>"
        else:
            print "KO"
            extractionFastvsFullDisplay += ', ' + elem
    
    extractionFastvsFull = extractionFastvsFull[2:]
    extractionFastvsFullDisplay = extractionFastvsFullDisplay[2:]
    
    return extractionFastvsFull, extractionFastvsFullDisplay

def checkCalculValidation(self, fileName):
#Full, RECO    : (not PU) and (not Fast)
#Full, PU      : PU and (not Fast)
#Full, pmx     : pmx and (not Fast) for rel, PU and (not Fast) for ref
#Full, miniAOD : idem Full, RECO

#Fast, RECO    : Fast and (not PU nor pmx)
#Fast, PU      : PU and Fast
#Fast, pmx     : pmx and Fast for rel, PU and Fast for ref
#Fast, miniAOD : idem Fast, RECO
    
    checkCalculValidation = True
    check_PU = False
    check_pmx = False
    check_Fast = False
    if ( re.search("PU", fileName) ):
        check_PU = True
    if ( re.search("pmx", fileName) ):
        check_pmx = True
    if ( re.search("Fast", fileName) ):
        check_Fast = True
    
    if ( self.radio11.isChecked() and self.radio21.isChecked() ): #Full, RECO
#        print ">>>>>>>> Full, RECO"
        if ( re.search("PU", fileName) or re.search("Fast", fileName) ):
#            print ">>>> PU, Fast : " + fileName
            checkCalculValidation = False
    
    if ( self.radio11.isChecked() and self.radio22.isChecked() ): #Full, PU
        print ">>>>>>>> Full, PU"
    return checkCalculValidation

