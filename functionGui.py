#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

def initDataSets(self):
#    print "initDataSets"

    self.QLW_dataset.clear()
    for it in self.DataSetTable: # list of DataSets
        item = QListWidgetItem("%s" % it)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        item.setCheckState(QtCore.Qt.Checked)
        self.QLW_dataset.addItem(item)
    return
    
def clearDataSets(self):
    self.QLW_rel1.clear()
    self.QLW_rel2.clear()
    self.QTable_rel.clearContents()
    self.QTable_ref.clearContents()
    return

def clearDataSetsLists(self):
    self.QTable_rel.clearContents()
    self.QTable_ref.clearContents()
    return

def clearReleasesList(self):
    self.releasesList_rel_5 = []
    self.releasesList_ref_5 = []
    return
    
def writeLabelCombo3(self):
#    print "LabelCombo3 = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
#    print "LabelCombo3 : %s" % self.tasks_list[self.tasks_counter]
    if self.tasks_counter >= self.tasks_counterMax:
        txt = "(" + str(self.tasks_counter) + "/" + str(self.tasks_counter) + ") Next : " 
    else:
        txt = "(" + str(self.tasks_counter) + "/" + str(self.tasks_counter + 1) + ") Next : " + self.tasks_list[self.tasks_counter+1]
    self.labelCombo3.setText(self.trUtf8(txt))
    return

def fillQLW_rel1(self):
    self.QLW_rel1.clear()
    for it in self.releasesList_0:
        item = QListWidgetItem("%s" % it)
        self.QLW_rel1.addItem(item)
    return
    
def fillQLW_rel2_rel(self):
    self.QLW_rel2.clear()
    for it in self.rel_list_0:
        item = QListWidgetItem("%s" % it)
        self.QLW_rel2.addItem(item)
    return
    
def fillQLW_rel2_ref(self):
    self.QLW_rel2.clear()
    for it in self.ref_list_0:
        item = QListWidgetItem("%s" % it)
        self.QLW_rel2.addItem(item)
    return

def disableRadioButtons(self):
    self.radio11.setEnabled(False)
    self.radio12.setEnabled(False)
    self.radio13.setEnabled(False)
    self.checkSpecTarget1.setEnabled(False)
    self.checkSpecTarget2.setEnabled(False)
    self.checkSpecTarget3.setEnabled(False)
    self.checkSpecTarget4.setEnabled(False)
    self.checkSpecReference1.setEnabled(False)
    self.checkSpecReference2.setEnabled(False)
    self.checkSpecReference3.setEnabled(False)
    self.checkSpecReference4.setEnabled(False)
    self.checkAllNone1.setEnabled(False)
    self.checkAllNone2.setEnabled(False)
    self.checkDataSets1.setEnabled(False)
    self.checkDataSets2.setEnabled(False)

    return

def enableRadioButtons(self):
    self.radio11.setEnabled(True)
    self.radio12.setEnabled(True)
    self.radio13.setEnabled(True)
    self.checkSpecTarget1.setEnabled(True)
    self.checkSpecTarget2.setEnabled(True)
    self.checkSpecTarget3.setEnabled(True)
    self.checkSpecTarget4.setEnabled(True)
    self.checkSpecReference1.setEnabled(True)
    self.checkSpecReference2.setEnabled(True)
    self.checkSpecReference3.setEnabled(True)
    self.checkSpecReference4.setEnabled(True)
    self.checkAllNone1.setEnabled(True)
    self.checkAllNone2.setEnabled(True)
    self.checkDataSets1.setEnabled(True)
    self.checkDataSets2.setEnabled(True)

    return

def disableStdDevButtons(self):
    self.checkStdDev1.setEnabled(False)
    self.checkStdDev2.setEnabled(False)

    return

def enableStdDevButtons(self):
    self.checkStdDev1.setEnabled(True)
    self.checkStdDev2.setEnabled(True)

    return
    
def disableLocationButtons(self): 
    self.checkLocation1.setEnabled(False)
    self.checkLocation2.setEnabled(False)

    return

def enableLocationButtons(self):
    self.checkLocation1.setEnabled(True)
    self.checkLocation2.setEnabled(True)

    return

def comparisonRules(self): # to define which reference buttons are checked or not
    if ( self.checkSpecTarget1.isChecked() ): # RECO
        self.checkSpecReference1.setChecked(True) 
        self.checkSpecReference1.setEnabled(True)
        self.checkSpecReference2.setEnabled(False)
        self.checkSpecReference3.setEnabled(False)
        if ( self.radio13.isChecked() ): # Fast vs Full
            self.checkSpecReference4.setEnabled(False)
        else:
            self.checkSpecReference4.setEnabled(True)
    elif ( self.checkSpecTarget2.isChecked() ): # PU25
        self.checkSpecReference2.setChecked(True) 
        self.checkSpecReference1.setEnabled(False)
        self.checkSpecReference2.setEnabled(True)
        self.checkSpecReference3.setEnabled(False)
        self.checkSpecReference4.setEnabled(False)
    elif ( self.checkSpecTarget3.isChecked() ): # PUpmx25
        self.checkSpecReference2.setChecked(True) # default = PU25
        self.checkSpecReference1.setEnabled(False)
        if ( self.radio13.isChecked() ): # Fast vs Full
            self.checkSpecReference2.setEnabled(False) # PUpmx25
            self.checkSpecReference3.setChecked(True) # when Fast vs Full, only pmx vs pmx is allowed
        else:
            self.checkSpecReference2.setEnabled(True) # PUpmx25
        self.checkSpecReference3.setEnabled(True) # PU25
        self.checkSpecReference4.setEnabled(False)
    elif ( self.checkSpecTarget4.isChecked() ): # miniAOD
        self.checkSpecReference4.setChecked(True) 
        self.checkSpecReference1.setEnabled(False)
        self.checkSpecReference2.setEnabled(False)
        self.checkSpecReference3.setEnabled(False)
        self.checkSpecReference4.setEnabled(True)
    return
