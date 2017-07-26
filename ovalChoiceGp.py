#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

def initGpRelRef(self):
    print "initGpRelRef"

    self.QGBox_rel0 = QGroupBox("Release list") # default
    self.QGBox_rel0.setMinimumHeight(250)
    self.QGBox_rel0.setMaximumHeight(250)
    self.QHL_rel = QHBoxLayout(self.QGBox_rel0)
        
    self.QGBox_rel1 = QGroupBox("List")
    self.QGBox_rel1.setMinimumWidth(180)
    self.QGBox_rel1.setMaximumWidth(180)
    self.vbox_rel1 = QVBoxLayout()
    self.QLW_rel1 = QListWidget()
    for it in self.releasesList_0:
        item = QListWidgetItem("%s" % it)
        self.QLW_rel1.addItem(item)
    self.connect(self.QLW_rel1, SIGNAL("itemSelectionChanged()"),self.ItemRelRefClicked1)
    self.vbox_rel1.addWidget(self.QLW_rel1)        
    self.QGBox_rel1.setLayout(self.vbox_rel1)
    self.QHL_rel.addWidget(self.QGBox_rel1)
        
    self.QGBox_rel2 = QGroupBox("Release")
    self.QGBox_rel2.setMinimumWidth(200)
    self.QGBox_rel2.setMaximumWidth(200)
    self.vbox_rel2 = QVBoxLayout()
    self.QLW_rel2 = QListWidget()
    item = QListWidgetItem("%s" % "")
    self.QLW_rel2.addItem(item)
    self.connect(self.QLW_rel2, SIGNAL("itemSelectionChanged()"),self.ItemRelRefClicked2)
    self.vbox_rel2.addWidget(self.QLW_rel2)        
    self.QGBox_rel2.setLayout(self.vbox_rel2)
    self.QHL_rel.addWidget(self.QGBox_rel2)
        
    self.layout_Search = QVBoxLayout()
    self.layout_Search.addWidget(self.QGBox_rel0)

    return

def initGpLists(self):
    print "initGpLists"

    self.QGBox_Lists = QGroupBox("Lists") # default
    self.QGBox_Lists.setMinimumHeight(250)
    self.QGBox_Lists.setMaximumHeight(250)
    self.QGBox_Lists.setVisible(False)
    self.QHL_Lists = QHBoxLayout(self.QGBox_Lists) 
        
    self.QGBox_rel_0 = QGroupBox("Release")
    self.QGBox_rel_0.setMinimumWidth(450)
    self.vbox_rel4_0 = QVBoxLayout()
    self.QTable_rel = QTableWidget()
    self.QTable_rel.setColumnCount(2)
    self.QTable_rel.setHorizontalHeaderLabels(self.listHeader)
    self.QTable_rel.setColumnWidth(0, 150)
    self.QTable_rel.setColumnWidth(1, 380)
    self.vbox_rel4_0.addWidget(self.QTable_rel)
    self.QGBox_rel_0.setLayout(self.vbox_rel4_0)
    
    self.QGBox_ref_0 = QGroupBox("Reference")
    self.QGBox_ref_0.setMinimumWidth(450)
    self.vbox_ref4_0 = QVBoxLayout()
    self.QTable_ref = QTableWidget()
    self.QTable_ref.setColumnCount(2)
    self.QTable_ref.setHorizontalHeaderLabels(self.listHeader)
    self.QTable_ref.setColumnWidth(0, 150)
    self.QTable_ref.setColumnWidth(1, 380)
    self.vbox_ref4_0.addWidget(self.QTable_ref)
    self.QGBox_ref_0.setLayout(self.vbox_ref4_0)
    
    self.QGBox_FastvsFull_0 = QGroupBox("FastvsFull Reference")
    self.QGBox_FastvsFull_0.setMinimumWidth(450)
    self.vbox_FastvsFull_0 = QVBoxLayout()
    self.QTable_FastvsFull = QTableWidget()
    self.QTable_FastvsFull.setColumnCount(2)
    self.QTable_FastvsFull.setHorizontalHeaderLabels(self.listHeader)
    self.QTable_FastvsFull.setColumnWidth(0, 150)
    self.QTable_FastvsFull.setColumnWidth(1, 380)
    self.vbox_FastvsFull_0.addWidget(self.QTable_FastvsFull)
    self.QGBox_FastvsFull_0.setLayout(self.vbox_FastvsFull_0)
    self.QGBox_FastvsFull_0.setVisible(False)
    
    self.QHL_Lists.addWidget(self.QGBox_rel_0)
    self.QHL_Lists.addWidget(self.QGBox_ref_0)
    self.QHL_Lists.addWidget(self.QGBox_FastvsFull_0)
    
    self.layout_Lists = QVBoxLayout()
    self.layout_Lists.addWidget(self.QGBox_Lists)

    return

def initGpSelected(self):
    print "initGpSelected"

    self.QGBox_Selected = QGroupBox("Selected")
    self.QGBox_Selected.setMinimumHeight(250)
    self.QGBox_Selected.setMaximumHeight(250)
    self.QGBox_Selected.setVisible(False)       
    
    self.labelResumeSelected = QLabel(self.trUtf8("<strong>Selected :</strong>"), self)   # label used for resuming the rel/ref.
    vboxSelected = QVBoxLayout()
    vboxSelected.addWidget(self.labelResumeSelected)
    self.QGBox_Selected.setLayout(vboxSelected)

    self.layout_Selected = QVBoxLayout()
    self.layout_Selected.addWidget(self.QGBox_Selected)

    return

def initGpChoice(self):
    # release/reference
    initGpRelRef(self)
    
    # Datasets Lists
    initGpLists(self)
    
    # Selected DataSets
    initGpSelected(self)
    
    return
    
