#! /usr/bin/env python
#-*-coding: utf-8 -*-

# A new presentation/use is made in order to use very precisely the DataSets.
# You can add a DataSet inside a given function and look what happened for only the considered Datatsets.
# This seems more efficient than use "hard coding" and complex search function for the separate cases.

# new way to load datasets items into the menu. datasets are presented as [name, True/False] with True/False the default choice to be checked or not.

import re
from Paths_default import *

def DataSetsFilter(self):
    import sys
    fieldname = self.validationType1
    if ( self.validationType3 == 'miniAOD' ):
        fieldname = fieldname + self.validationType3
    else:
        fieldname = fieldname + self.validationType2
    table=getattr(sys.modules[__name__], "DataSetsFilter_%s" % fieldname)(self)
    
    return table

def DataSetsFilter_FullRECO(self):
    table=[
    ["SingleElectronPt10", 1], # 1 : displayed
    ["SingleElectronPt10_UP15", 0], 
    ["SingleElectronPt35", 1],
    ["SingleElectronPt35_UP15", 0], # 0 : not displayed
    ["SingleElectronPt1000", 1],
    ["QCD_Pt_80_120_13", 1],
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastRECO(self):
    table=[
    ["TTbar_13", 0],
    ["ZEE_13", 0],
    ["TTbar_13_UP17", 1],
    ["ZEE_13_UP17", 1],
    ]
    return table

def DataSetsFilter_FastFullRECO(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ["TTbar_13_UP17", 1],
    ["ZEE_13_UP17", 1],
    ]
    return table

def DataSetsFilter_FullPU25(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastPU25(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastFullPU25(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FullPUpmx25(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastPUpmx25(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastFullPUpmx25(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FullminiAOD(self):
    table=[
    ["SingleElectronPt10", 1],
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastminiAOD(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def DataSetsFilter_FastFullminiAOD(self):
    table=[
    ["TTbar_13", 1],
    ["ZEE_13", 1],
    ]
    return table

def extractDatasets(self):
    extraction = ""
    extractionDisplay = ""
    # display of the datasets strings
    self.wp.write("datasets release   : %s\n" % self.selectedRelDatasets)
    self.wp.write("datasets reference : %s\n" % self.selectedRefDatasets)
    self.textReport += "datasets release   : " + self.selectedRelDatasets + "<br>"
    self.textReport += "datasets reference : " + self.selectedRefDatasets + "<br>"
    # cutting self.selectedRelDatasets
    cuttedRelease = str(self.selectedRelDatasets).split(',')
    #print "cuttedRelease : ", cuttedRelease
    self.wp.write("cuttedRelease : %s\n" % cuttedRelease)
    self.textReport += "cuttedRelease   : " + str(cuttedRelease) + "<br>"
    # searching in self.selectedRefDatasets
    for elem in cuttedRelease:
        elem2 = elem.replace("_UP17", "") # TEMP for _UP17 & Fast vs Full
        if re.search(elem2, self.selectedRefDatasets): # TEMP for _UP17 & Fast vs Full
            extraction += ', ' + elem
            extractionDisplay += ', ' + "<font color = \"blue\">" + elem + "</font>"
        else:
            extractionDisplay += ', ' + elem

    extraction = extraction[2:]
    extractionDisplay = extractionDisplay[2:]
    
    return extraction 

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
    # folder location for those files : HistosConfigFiles/
    # ElectronMcSignalValidator
    # ElectronMcSignalValidatorMiniAOD
    # ElectronMcSignalValidatorPt1000
    # ElectronMcFakeValidator
    
    '''
    in order to use the GUI without the CMSSW env (i.e. without the cmsrel, and the need of the Validation/RecoEgamma/test folder)
    you have to use the following line below.
    '''
    #tmp_path = '/afs/cern.ch/user/a/archiron/lbin/Projet_Validations-PortableDev/HistosConfigFiles/'
    tmp_path = '/eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/Projet_Validations-PortableDev/HistosConfigFiles/'
    '''
    in order to use the GUI with the CMSSW env (i.e. with the Validation/RecoEgamma/test folder)
    you have to use the following line below with self.working_dir_base.
    '''
    #tmp_path = self.working_dir_base + '/'

    t_rel = tmp_path + 'ElectronMcSignalHistos.txt'
    t_ref = t_rel
    tp_rel = 'ElectronMcSignalValidator'
    tp_ref = tp_rel
    if ( re.search('Pt1000', dataSetsName) ):
        t_rel = tmp_path + 'ElectronMcSignalHistosPt1000.txt'
        t_ref = t_rel
        tp_rel = 'ElectronMcSignalValidatorPt1000'
        tp_ref = tp_rel
    elif ( re.search('QCD', dataSetsName) ):
        t_rel = tmp_path + 'ElectronMcFakeHistos.txt'
        t_ref = t_rel
        tp_rel = 'ElectronMcFakeValidator'
        tp_ref = tp_rel
    else: # general
        if self.checkSpecTarget1.isChecked(): # RECO
            if self.checkSpecReference4.isChecked(): # RECO vs miniAOD
                t_rel = tmp_path + 'ElectronMcSignalHistosMiniAOD.txt' # we have only miniAOD histos to compare.
                t_ref = tmp_path + 'ElectronMcSignalHistosMiniAOD.txt'
                tp_rel = 'ElectronMcSignalValidator'
                tp_ref = 'ElectronMcSignalValidatorMiniAOD'
            else: # RECO vs RECO
                t_rel = tmp_path + 'ElectronMcSignalHistos.txt'
                t_ref = t_rel
                tp_rel = 'ElectronMcSignalValidator'
                tp_ref = 'ElectronMcSignalValidator'
        elif self.checkSpecTarget4.isChecked(): # miniAOD vs miniAOD
            t_rel = tmp_path + 'ElectronMcSignalHistosMiniAOD.txt'
            t_ref = t_rel
            tp_rel = 'ElectronMcSignalValidatorMiniAOD'
            tp_ref = tp_rel
    return [t_rel, t_ref, tp_rel, tp_ref]

