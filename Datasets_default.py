#! /usr/bin/env python
#-*-coding: utf-8 -*-

# A new presentation/use is made in order to use very precisely the DataSets.
# You can add a DataSet inside a given function and look what happened for only the considerated Datatsets.
# This seems more efficient than use "hard coding" and complex search function for the separate cases.

# new way to load datasets items into the menu. datasets are presented as [name, True/False] with True/False the default choice to be checked or not.

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
    ["SingleElectronPt10", 1], 
    ["SingleElectronPt10_UP15", 1], 
    ["SingleElectronPt35", 1],
    ["SingleElectronPt35_UP15", 0],
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
