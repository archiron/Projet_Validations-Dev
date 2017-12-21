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
    self.QTable_FastvsFull.clearContents()
    return

def clearReleasesList(self):
    self.releasesList_rel_5 = []
    self.releasesList_ref_5 = []
    self.releasesList_FvsF_5 = []
    return
    
def writeLabelCombo3(self):
    if self.tasks_counter == len(self.tasks_list) - 1:
        txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter) + ") Next : " 
    else:
        txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter + 1) + ") Next : " + self.tasks_list[self.tasks_counter+1]
    self.labelCombo3.setText(self.trUtf8(txt))
    return

def changeFastvsFullSize(self):
    print "self.tasks_counter = %d" % self.tasks_counter
    if ( self.tasks_counter == 2 and checkFastvsFull(self) ):
        print "self.checkFastvsFull = %s" % self.checkFastvsFull
        self.setFixedSize(1500, 700)
        self.QGBox_FastvsFull_0.setVisible(True)
    else:
        self.setFixedSize(1200, 700)
        self.QGBox_FastvsFull_0.setVisible(False)
    return
