#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_folder_creation, get_choix_calcul, clean_files, copy_files, cmd_fetch, explode_item
from fonctions import list_search_0, list_search_1, list_search, explode_item, sub_releases, sub_releases2
from fonctions import list_simplify
		
#############################################################################
class GetChoice(QWidget):
 
    def __init__(self, parent=None):
        super(GetChoice, self).__init__(parent)
        self.setWindowTitle("Releases choice")
        self.cmsenv = env()
        self.releasesList_0 = list_search_0(self) # list of releases in https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/
 
## PART 1
		# creation du grpe DataSets Type
        self.QGBox0 = QGroupBox("DataSets Type")
        self.QGBox0.setMaximumHeight(150)
        self.QGBox0.setMaximumWidth(100)
        self.radio01 = QRadioButton("Classical") # par defaut
        self.radio02 = QRadioButton("Others")
        self.radio03 = QRadioButton("All")
        self.radio01.setChecked(True)
        self.connect(self.radio01, SIGNAL("clicked()"), self.radio01Clicked) 
        self.connect(self.radio02, SIGNAL("clicked()"), self.radio02Clicked) 
        self.connect(self.radio03, SIGNAL("clicked()"), self.radio03Clicked) 
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.radio01)
        vbox1.addWidget(self.radio02)
        vbox1.addWidget(self.radio03)
        vbox1.addStretch(1)
        self.QGBox0.setLayout(vbox1)
        				
		# creation des texEdit pour release/reference
        self.QGBox6 = QGroupBox("release")
        self.QGBox6.setMaximumHeight(150)
        self.QGBox6.setMinimumHeight(150)
        self.QGBox6.setMinimumWidth(250)
        
        self.labelCombo1 = QLabel(self.trUtf8("Release"), self)
        self.labelCombo2 = QLabel(self.trUtf8("Reference"), self)

        vbox6 = QVBoxLayout()
        vbox6.addWidget(self.labelCombo1) 
        vbox6.addWidget(self.labelCombo2) 
        vbox6.addStretch(1)
        self.QGBox6.setLayout(vbox6)

        #Layout intermédiaire : création et peuplement des gpes radios
        self.layoutH_radio = QHBoxLayout()
        self.layoutH_radio.addWidget(self.QGBox0)
        self.layoutH_radio.addStretch(1)
        self.layoutH_radio.addWidget(self.QGBox6)

## PART 2
        # release
        self.QGBox_rel0 = QGroupBox("Release list")
        self.QGBox_rel0.setMinimumHeight(150)
        self.QHL_rel = QHBoxLayout(self.QGBox_rel0)
        self.QGBox_rel1 = QGroupBox("List")
        self.QGBox_rel1.setMinimumWidth(120)
        self.QGBox_rel1.setMaximumWidth(120)
        self.vbox_rel1 = QVBoxLayout()
        self.QLW_rel1 = QListWidget()
        for it in self.releasesList_0:
            item = QListWidgetItem("%s" % it)
            self.QLW_rel1.addItem(item)
        self.connect(self.QLW_rel1, SIGNAL("itemSelectionChanged()"),self.ItemRelClicked1)
        self.vbox_rel1.addWidget(self.QLW_rel1)        
        self.QGBox_rel1.setLayout(self.vbox_rel1)
        self.QHL_rel.addWidget(self.QGBox_rel1)
        
        self.QGBox_rel2 = QGroupBox("An Other List")
        self.QGBox_rel2.setMinimumWidth(200)
        self.QGBox_rel2.setMaximumWidth(200)
        self.vbox_rel2 = QVBoxLayout()
        self.QLW_rel2 = QListWidget()
        item = QListWidgetItem("%s" % "")
        self.QLW_rel2.addItem(item)
        self.connect(self.QLW_rel2, SIGNAL("itemSelectionChanged()"),self.ItemRelClicked2)
        self.vbox_rel2.addWidget(self.QLW_rel2)        
        self.QGBox_rel2.setLayout(self.vbox_rel2)
        self.QHL_rel.addWidget(self.QGBox_rel2)
        
        self.QGBox_rel3 = QGroupBox("Tiens")
        self.QGBox_rel3.setMinimumWidth(200)
        self.QGBox_rel3.setMaximumWidth(200)
        self.vbox_rel3 = QVBoxLayout()
        self.QLW_rel3 = QListWidget()
        item = QListWidgetItem("%s" % "")
        self.QLW_rel3.addItem(item)
        self.connect(self.QLW_rel3, SIGNAL("itemSelectionChanged()"),self.ItemRelClicked3)
        self.vbox_rel3.addWidget(self.QLW_rel3)        
        self.QGBox_rel3.setLayout(self.vbox_rel3)
        self.QHL_rel.addWidget(self.QGBox_rel3)
        
        self.QGBox_rel4 = QGroupBox("Data Sets")
        self.QGBox_rel4.setMinimumWidth(200)
        self.QHL_rel.addWidget(self.QGBox_rel4)
        self.QGBox_rel0.setLayout(self.QHL_rel)

        # reference
        self.QGBox_ref0 = QGroupBox("Reference list")
        self.QGBox_ref0.setMinimumHeight(150)
        self.QHL_ref = QHBoxLayout(self.QGBox_ref0)
        self.QGBox_ref1 = QGroupBox("List")
        self.QGBox_ref1.setMinimumWidth(120)
        self.QGBox_ref1.setMaximumWidth(120)
        self.vbox_ref1 = QVBoxLayout()
        self.QLW_ref1 = QListWidget()
        for it in self.releasesList_0:
            item = QListWidgetItem("%s" % it)
            self.QLW_ref1.addItem(item)
        self.connect(self.QLW_ref1, SIGNAL("itemSelectionChanged()"),self.ItemRefClicked1)
        self.vbox_ref1.addWidget(self.QLW_ref1)        
        self.QGBox_ref1.setLayout(self.vbox_ref1)
        self.QHL_ref.addWidget(self.QGBox_ref1)
        
        self.QGBox_ref2 = QGroupBox("An Other List")
        self.QGBox_ref2.setMinimumWidth(200)
        self.QGBox_ref2.setMaximumWidth(200)
        self.vbox_ref2 = QVBoxLayout()
        self.QLW_ref2 = QListWidget()
        item = QListWidgetItem("%s" % "")
        self.QLW_ref2.addItem(item)
        self.connect(self.QLW_ref2, SIGNAL("itemSelectionChanged()"),self.ItemRefClicked2)
        self.vbox_ref2.addWidget(self.QLW_ref2)        
        self.QGBox_ref2.setLayout(self.vbox_ref2)
        self.QHL_ref.addWidget(self.QGBox_ref2)
        
        self.QGBox_ref3 = QGroupBox("Tiens")
        self.QGBox_ref3.setMinimumWidth(200)
        self.QGBox_ref3.setMaximumWidth(200)
        self.vbox_ref3 = QVBoxLayout()
        self.QLW_ref3 = QListWidget()
        item = QListWidgetItem("%s" % "")
        self.QLW_ref3.addItem(item)
        self.connect(self.QLW_ref3, SIGNAL("itemSelectionChanged()"),self.ItemRefClicked3)
        self.vbox_ref3.addWidget(self.QLW_ref3)        
        self.QGBox_ref3.setLayout(self.vbox_ref3)
        self.QHL_ref.addWidget(self.QGBox_ref3)
        
        self.QGBox_ref4 = QGroupBox("Data Sets")
        self.QGBox_ref4.setMinimumWidth(200)
        self.QHL_ref.addWidget(self.QGBox_ref4)
        self.QGBox_ref0.setLayout(self.QHL_ref)

        vbox_H0 = QVBoxLayout()
        vbox_H0.addWidget(self.QGBox_rel0)
        vbox_H0.addWidget(self.QGBox_ref0)

        # créer un bouton
        self.bouton = QPushButton("OK", self)
        self.bouton.clicked.connect(self.ok_Choice)
        hbox_button = QHBoxLayout()
        hbox_button.addStretch(1)
        hbox_button.addWidget(self.bouton)
        # positionner les widgets dans la fenêtre
        posit = QVBoxLayout()
        posit.addLayout(self.layoutH_radio)
        posit.addLayout(vbox_H0)
        posit.addLayout(hbox_button)

        self.setLayout(posit)
 
    def ok_Choice(self):
        # emettra un signal "fermeturegetChoice()" avec l'argument cité
#        print "ok_Choice: self.my_choice_rel_0 : %s " % self.my_choice_rel_0
#        print "ok_Choice: self.my_choice_ref_0 : %s " % self.my_choice_ref_0
#        print "ok_Choice: self.my_choice_rel_1 : %s " % self.my_choice_rel_1
#        print "ok_Choice: self.my_choice_ref_1 : %s " % self.my_choice_ref_1
        tptp = [str(self.my_choice_rel_0), str(self.my_choice_ref_0),str(self.my_choice_rel_1), str(self.my_choice_ref_1)]
        self.emit(SIGNAL("fermeturegetChoice(PyQt_PyObject)"), tptp) 
        # fermer la fenêtre
        self.close()
 
    def ItemRelClicked1(self):
        self.QGBox_rel2.setTitle(self.QLW_rel1.currentItem().text())
        self.my_choice_rel_0 = self.QLW_rel1.currentItem().text()
        print "ItemRelClicked1 : self.my_choice_rel_0 : %s " % self.my_choice_rel_0
        self.rel_list_0 = sub_releases(list_search_1(self.my_choice_rel_0))
        # tester si =0
        self.QLW_rel2.clear()
        for it in self.rel_list_0:
            item = QListWidgetItem("%s" % it)
            self.QLW_rel2.addItem(item)
        
    def ItemRefClicked1(self):
        self.QGBox_ref2.setTitle(self.QLW_ref1.currentItem().text())
        self.my_choice_ref_0 = self.QLW_ref1.currentItem().text()
        print "ItemRefClicked1 : self.my_choice_ref_0 : %s " % self.my_choice_ref_0
        self.ref_list_0 = sub_releases(list_search_1(self.my_choice_ref_0))
        self.QLW_ref2.clear()
        for it in self.ref_list_0:
            item = QListWidgetItem("%s" % it)
            self.QLW_ref2.addItem(item)

    def ItemRelClicked2(self):
        self.QGBox_rel3.setTitle(self.QLW_rel2.currentItem().text())
        self.my_choice_rel_1 = self.QLW_rel2.currentItem().text()
        print "ItemRelClicked2 : self.my_choice_rel_1 : %s " % self.my_choice_rel_1
        tmp = "Release : " + self.my_choice_rel_1
        self.labelCombo1.setText(tmp)
        self.rel_list_1 = sub_releases2(str(self.my_choice_rel_1), list_search_1(self.my_choice_rel_1))
        self.QLW_rel3.clear()
        for it in self.rel_list_1:
            item = QListWidgetItem("%s" % it)
            self.QLW_rel3.addItem(item)
        
    def ItemRefClicked2(self):
        self.QGBox_ref3.setTitle(self.QLW_ref2.currentItem().text())
        self.my_choice_ref_1 = self.QLW_ref2.currentItem().text()
        print "ItemRefClicked2 : self.my_choice_ref_1 : %s " % self.my_choice_ref_1
        tmp = "Reference : " + self.my_choice_ref_1
        self.labelCombo2.setText(tmp)
        self.ref_list_1 = sub_releases2(str(self.my_choice_ref_1), list_search_1(self.my_choice_ref_1))
        self.QLW_ref3.clear()
        for it in self.ref_list_1:
            item = QListWidgetItem("%s" % it)
            self.QLW_ref3.addItem(item)

    def ItemRelClicked3(self):
        #self.QGBox_rel4.setTitle(self.QLW_rel3.currentItem().text())
        #self.my_choice_rel_1 = self.QLW_rel2.currentItem().text()
        print "ItemRelClicked3 : self.my_choice_rel_1 : %s " % self.QLW_rel3.currentItem().text()
        
    def ItemRefClicked3(self):
        #self.QGBox_ref4.setTitle(self.QLW_ref3.currentItem().text())
        #self.my_choice_ref_1 = self.QLW_ref2.currentItem().text()
        print "ItemRefClicked3 : self.my_choice_ref_1 : %s " % self.QLW_ref3.currentItem().text()

    def radio01Clicked(self):
        if self.radio01.isChecked():
            print self.radio01.text()
        QtCore.QCoreApplication.processEvents()

    def radio02Clicked(self):
        if self.radio02.isChecked():
            print self.radio02.text()
        QtCore.QCoreApplication.processEvents()
        
    def radio03Clicked(self):
        if self.radio03.isChecked():
            print self.radio03.text()
        QtCore.QCoreApplication.processEvents()
                        
