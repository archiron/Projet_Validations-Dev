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

    self.QGBox_Lists= QGroupBox("Lists") # default
    self.QGBox_Lists.setMinimumHeight(250)
    self.QGBox_Lists.setMaximumHeight(250)
    self.QGBox_Lists.setVisible(False)
    self.QHL_Lists = QHBoxLayout(self.QGBox_Lists) 
        
    self.QGBox_rel = QGroupBox("Release")
    self.QGBox_rel.setMinimumWidth(180)
    self.QGBox_rel.setMaximumWidth(180)
    self.vbox_rel4 = QVBoxLayout()
    self.QLW_rel_dataset = QListWidget()
    item = QListWidgetItem("%s" % "")
    self.QLW_rel_dataset.addItem(item)
    self.vbox_rel4.addWidget(self.QLW_rel_dataset) 
    self.QGBox_rel.setLayout(self.vbox_rel4)
        
    self.QGBox_rel_list = QGroupBox("Release List")
    self.QGBox_rel_list.setMinimumWidth(270)
    self.QGBox_rel_list.setMaximumWidth(270)
    self.vbox_rel_list = QVBoxLayout()
    self.QLW_rel_dataset_list = QListWidget()
    item = QListWidgetItem("%s" % "")
    self.QLW_rel_dataset_list.addItem(item)
    self.vbox_rel_list.addWidget(self.QLW_rel_dataset_list) 
    self.QGBox_rel_list.setLayout(self.vbox_rel_list)
        
    self.QGBox_ref = QGroupBox("Reference")
    self.QGBox_ref.setMinimumWidth(180)
    self.QGBox_ref.setMaximumWidth(180)
    self.vbox_ref4 = QVBoxLayout()
    self.QLW_ref_dataset = QListWidget()
    item = QListWidgetItem("%s" % "")
    self.QLW_ref_dataset.addItem(item)
    self.vbox_ref4.addWidget(self.QLW_ref_dataset) 
    self.QGBox_ref.setLayout(self.vbox_ref4)
        
    self.QGBox_ref_list = QGroupBox("Reference List")
    self.QGBox_ref_list.setMinimumWidth(270)
    self.QGBox_ref_list.setMaximumWidth(270)
    self.vbox_ref_list = QVBoxLayout()
    self.QLW_ref_dataset_list = QListWidget()
    item = QListWidgetItem("%s" % "")
    self.QLW_ref_dataset_list.addItem(item)
    self.vbox_ref_list.addWidget(self.QLW_ref_dataset_list) 
    self.QGBox_ref_list.setLayout(self.vbox_ref_list)
        
    self.QGBox_FastvsFull = QGroupBox("FastvsFull Reference")
    self.QGBox_FastvsFull.setMinimumWidth(180)
    self.QGBox_FastvsFull.setMaximumWidth(180)
    self.vbox_FastvsFull = QVBoxLayout()
    self.QLW_FastvsFull_dataset = QListWidget()
    item = QListWidgetItem("%s" % "")
    self.QLW_FastvsFull_dataset.addItem(item)
    self.vbox_FastvsFull.addWidget(self.QLW_FastvsFull_dataset) 
    self.QGBox_FastvsFull.setLayout(self.vbox_FastvsFull)
        
    self.QGBox_FastvsFull_list = QGroupBox("FastvsFull Reference List")
    self.QGBox_FastvsFull_list.setMinimumWidth(270)
    self.QGBox_FastvsFull_list.setMaximumWidth(270)
    self.vbox_FastvsFull_list = QVBoxLayout()
    self.QLW_FastvsFull_dataset_list = QListWidget()
    item = QListWidgetItem("%s" % "")
    self.QLW_FastvsFull_dataset_list.addItem(item)
    self.vbox_FastvsFull_list.addWidget(self.QLW_FastvsFull_dataset_list) 
    self.QGBox_FastvsFull_list.setLayout(self.vbox_FastvsFull_list)
    self.QGBox_FastvsFull.setVisible(False)
    self.QGBox_FastvsFull_list.setVisible(False)
        
    self.QHL_Lists.addWidget(self.QGBox_rel)
    self.QHL_Lists.addWidget(self.QGBox_rel_list)
    self.QHL_Lists.addWidget(self.QGBox_ref)
    self.QHL_Lists.addWidget(self.QGBox_ref_list)
    self.QHL_Lists.addWidget(self.QGBox_FastvsFull)
    self.QHL_Lists.addWidget(self.QGBox_FastvsFull_list)
    
    self.layout_Lists = QVBoxLayout()
    self.layout_Lists.addWidget(self.QGBox_Lists)

    return

def initGpSelected(self):
    print "initGpSelected"

    self.QGBox_Selected = QGroupBox("Selected")
    self.QGBox_Selected.setMinimumHeight(250)
    self.QGBox_Selected.setMaximumHeight(250)
    self.QGBox_Selected.setVisible(False)       
    
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
    
