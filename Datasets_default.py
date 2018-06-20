#! /usr/bin/env python
#-*-coding: utf-8 -*-

# A new presentation/use is made in order to use very precisely the DataSets.
# You can add a DataSet inside a given function and look what happened for only the considered Datatsets.
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
    ["SingleElectronPt10_UP15", 0], 
    ["SingleElectronPt35", 1],
    ["SingleElectronPt35_UP15", 0], # 0 : not displayed
    ["SingleElectronPt1000", 1],
    ["QCD_Pt_80_120_13", 1],
    ["TTbar_13", 0],
    ["ZEE_13", 0],
    ]
    return table

def DataSetsFilter_FastRECO(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastFullRECO(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FullPU25(self):
    print "Full"
    table=[
    ["TTbar_13", 0],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastPU25(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastFullPU25(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FullPUpmx25(self):
    print "Full"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastPUpmx25(self):
    print "Fast"
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastFullPUpmx25(self):
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

def DataSetsFilter_FastFullminiAOD(self):
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
    
    return extraction #, extractionDisplay
    
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

def checkCalculValidation(self, fileName, side):
#Full, RECO    : (not PU) and (not Fast)
#Full, PU25    : PU25 and (not Fast)
#Full, PUpmx25 : PUpmx25 and (not Fast) for rel, PU and (not Fast) for ref
#Full, miniAOD : idem Full, RECO

#Fast, RECO    : Fast and (not PU nor pmx)
#Fast, PU25    : PU25 and Fast
#Fast, PUpmx25 : PUpmx25 and Fast for rel, PU and Fast for ref
#Fast, miniAOD : idem Fast, RECO
    
    checkCalculValidation = True
    check_PU25 = False
    check_pmx25 = False
    check_Fast = False
    
    if self.radio11.isChecked(): # Full vs Full
        testFull = True
        testFast = False
    if self.radio12.isChecked(): # Full vs Full
        testFull = False
        testFast = True
    if self.radio13.isChecked(): # Fast vs Full
        if ( side == "rel" ): # Fast
            testFull = False
            testFast = True
        elif ( side == "ref" ): # Fast
            testFull =  True
            testFast =False
        else:
            print "BIG PBM !!"
    
    if ( re.search("PU25", fileName) ):
        check_PU25 = True
    if ( re.search("PUpmx25", fileName) ):
        check_pmx25 = True
    if ( re.search("Fast", fileName) ):
        check_Fast = True
    
    if self.checkSpecTarget1.isChecked(): # RECO or miniAOD
        if check_PU25 or check_pmx25:
            checkCalculValidation = False
        else:
            if testFast: # Fast
                if check_Fast:
                    checkCalculValidation = True
                else:
                    checkCalculValidation = False
            else: # Full
                if check_Fast:
                    checkCalculValidation = False
                else:
                    checkCalculValidation = True
    elif self.checkSpecTarget2.isChecked(): # PU25ns
        if check_PU25:
            if testFast: # Fast, PU25ns
                if check_Fast:
                    checkCalculValidation = True
                else:
                    checkCalculValidation = False
            else: # Full, PU25ns
                if check_Fast:
                    checkCalculValidation = False
                else:
                    checkCalculValidation = True
        else:
            checkCalculValidation = False
    elif self.checkSpecTarget3.isChecked(): # PUpmx25ns
        if check_pmx25:
            if testFast: # Fast, PUpmx25ns
                if check_Fast:
                    checkCalculValidation = True
                else:
                    checkCalculValidation = False
            else: # Full, PUpmx25ns
                if check_Fast:
                    checkCalculValidation = False
                else:
                    checkCalculValidation = True
        elif check_PU25:
            if testFast: # Fast, PU25ns
                if check_Fast:
                    checkCalculValidation = True
                else:
                    checkCalculValidation = False
            else: # Full, PU25ns
                if check_Fast:
                    checkCalculValidation = False
                else:
                    checkCalculValidation = True
        else:
            checkCalculValidation = False
    #else: # miniAOD or pbm
    
    return checkCalculValidation

def testForDataSetsFile(self, dataSetsName): # perhaps t_ref is not useful
    # also get the tree path part (tp_rel, tp_ref) for root files :
    # ElectronMcSignalValidator
    # ElectronMcSignalValidatorMiniAOD
    # ElectronMcSignalValidatorPt1000
    # ElectronMcFakeValidator

    print "testForDataSetsFile : ", dataSetsName
    
    t_rel = self.working_dir_base + '/' + 'ElectronMcSignalHistos.txt'
    t_ref = t_rel
    tp_rel = 'ElectronMcSignalValidator'
    tp_ref = tp_rel
    if ( re.search('Pt1000', dataSetsName) ):
        t_rel = self.working_dir_base + '/' + 'ElectronMcSignalHistosPt1000.txt'
        t_ref = t_rel
        tp_rel = 'ElectronMcSignalValidatorPt1000'
        tp_ref = tp_rel
    elif ( re.search('QCD', dataSetsName) ):
        t_rel = self.working_dir_base + '/' + 'ElectronMcFakeHistos.txt'
        t_ref = t_rel
        tp_rel = 'ElectronMcFakeValidator'
        tp_ref = tp_rel
    else: # general
        if self.checkSpecTarget1.isChecked(): # RECO
            #print "testForDataSetsFile : RECO"
            if self.checkSpecReference4.isChecked(): # RECO vs miniAOD
                #print "testForDataSetsFile : RECO vs miniAOD"
                #t_rel = self.working_dir_base + '/' + 'ElectronMcSignalHistos.txt'
                t_rel = self.working_dir_base + '/' + 'ElectronMcSignalHistosMiniAOD.txt' # we have only miniAOD histos to compare.
                t_ref = self.working_dir_base + '/' + 'ElectronMcSignalHistosMiniAOD.txt'
                tp_rel = 'ElectronMcSignalValidator'
                tp_ref = 'ElectronMcSignalValidatorMiniAOD'
            else: # RECO vs RECO
                #print "testForDataSetsFile : RECO vs RECO"
                t_rel = self.working_dir_base + '/' + 'ElectronMcSignalHistos.txt'
                t_ref = t_rel
                tp_rel = 'ElectronMcSignalValidator'
                tp_ref = 'ElectronMcSignalValidator'
        elif self.checkSpecTarget4.isChecked(): # miniAOD vs miniAOD
            #print "testForDataSetsFile : miniAOD vs miniAOD"
            t_rel = self.working_dir_base + '/' + 'ElectronMcSignalHistosMiniAOD.txt'
            t_ref = t_rel
            tp_rel = 'ElectronMcSignalValidatorMiniAOD'
            tp_ref = tp_rel
            print("testForDataSetsFile : tp_rel %s") % tp_rel
    #print "testForDataSetsFile end OK "
    return [t_rel, t_ref, tp_rel, tp_ref]

