#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_folder_creation, get_choix_calcul, clean_files, copy_files, cmd_fetch, explode_item
from fonctions import list_search_0, list_search_1, list_search, explode_item, sub_releases
from fonctions import list_simplify
		
#############################################################################
class GetChoice(QWidget):
 
    def __init__(self, parent=None):
        super(GetChoice, self).__init__(parent)
        self.setWindowTitle("Releases choice")
        self.cmsenv = env()
        self.releasesList_0 = list_search_0(self) # list of releases in https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/
 
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
        item = QListWidgetItem("%s" % "toto")
        self.QLW_rel2.addItem(item)
        self.connect(self.QLW_rel2, SIGNAL("itemSelectionChanged()"),self.ItemRelClicked2)
        self.vbox_rel2.addWidget(self.QLW_rel2)        
        self.QGBox_rel2.setLayout(self.vbox_rel2)
        self.QHL_rel.addWidget(self.QGBox_rel2)
        
        self.QGBox_rel3 = QGroupBox("Tiens")
        self.QGBox_rel3.setMinimumWidth(200)
        self.QHL_rel.addWidget(self.QGBox_rel3)
        self.QGBox_rel4 = QGroupBox("Bof")
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
        item = QListWidgetItem("%s" % "toto")
        self.QLW_ref2.addItem(item)
        self.connect(self.QLW_ref2, SIGNAL("itemSelectionChanged()"),self.ItemRefClicked2)
        self.vbox_ref2.addWidget(self.QLW_ref2)        
        self.QGBox_ref2.setLayout(self.vbox_ref2)
        self.QHL_ref.addWidget(self.QGBox_ref2)
        
        self.QGBox_ref3 = QGroupBox("Tiens")
        self.QGBox_ref3.setMinimumWidth(200)
        self.QHL_ref.addWidget(self.QGBox_ref3)
        self.QGBox_ref4 = QGroupBox("Bof")
        self.QGBox_ref4.setMinimumWidth(200)
        self.QHL_ref.addWidget(self.QGBox_ref4)
        self.QGBox_ref0.setLayout(self.QHL_ref)

        vbox_H0 = QVBoxLayout()
        vbox_H0.addWidget(self.QGBox_rel0)
        vbox_H0.addWidget(self.QGBox_ref0)

        # créer un bouton
        self.bouton = QPushButton("Cancel", self)
        self.bouton.clicked.connect(self.ok_Choice)
        hbox_button = QHBoxLayout()
        hbox_button.addStretch(1)
        hbox_button.addWidget(self.bouton)
        # positionner les widgets dans la fenêtre
        posit = QVBoxLayout()
        posit.addLayout(vbox_H0)
        posit.addLayout(hbox_button)

        self.setLayout(posit)
 
    def ok_Choice(self):
        # emettra un signal "fermeturegetChoice()" avec l'argument cité
        print "ok_Choice: self.my_choice_rel_0 : %s " % self.my_choice_rel_0
        print "ok_Choice: self.my_choice_ref_0 : %s " % self.my_choice_ref_0
        print "ok_Choice: self.my_choice_rel_1 : %s " % self.my_choice_rel_1
        print "ok_Choice: self.my_choice_ref_1 : %s " % self.my_choice_ref_1
        tptp = [str(self.my_choice_rel_0), str(self.my_choice_ref_0),str(self.my_choice_rel_1), str(self.my_choice_ref_1)]
        self.emit(SIGNAL("fermeturegetChoice(PyQt_PyObject)"), tptp) 
        # fermer la fenêtre
        self.close()
 
    def ItemRelClicked1(self):
#        QMessageBox.information(None,"Hello!","You Clicked: \n" + self.QLW_rel1.currentItem().text())
        self.QGBox_rel2.setTitle(self.QLW_rel1.currentItem().text())
        self.my_choice_rel_0 = self.QLW_rel1.currentItem().text()
        print "ItemRelClicked1 : self.my_choice_rel_0 : %s " % self.my_choice_rel_0
        temp = sub_releases(list_search_1(self.my_choice_rel_0))
        for it in temp:
            item = QListWidgetItem("%s" % it)
            self.QLW_rel2.addItem(item)
        
    def ItemRefClicked1(self):
#        QMessageBox.information(None,"Hello!","You Clicked: \n" + self.QLW_rel1.currentItem().text())
        self.QGBox_ref2.setTitle(self.QLW_ref1.currentItem().text())
        self.my_choice_ref_0 = self.QLW_ref1.currentItem().text()
        print "ItemRefClicked1 : self.my_choice_ref_0 : %s " % self.my_choice_ref_0
        temp = sub_releases(list_search_1(self.my_choice_ref_0))
        for it in temp:
            item = QListWidgetItem("%s" % it)
            self.QLW_ref2.addItem(item)

    def ItemRelClicked2(self):
        self.QGBox_rel3.setTitle(self.QLW_rel2.currentItem().text())
        self.my_choice_rel_1 = self.QLW_rel2.currentItem().text()
        print "ItemRelClicked2 : self.my_choice_rel_1 : %s " % self.my_choice_rel_1
        
    def ItemRefClicked2(self):
        self.QGBox_ref3.setTitle(self.QLW_ref2.currentItem().text())
        self.my_choice_ref_1 = self.QLW_ref2.currentItem().text()
        print "ItemRefClicked2 : self.my_choice_ref_1 : %s " % self.my_choice_ref_1

