#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

from fonctions import checkFastvsFull

def initDataSets(self):
    print "initDataSets"

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
    if self.tasks_counter == len(self.tasks_list) - 1:
        txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter) + ") Next : " 
    else:
        txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter + 1) + ") Next : " + self.tasks_list[self.tasks_counter+1]
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

    return
    
    
    