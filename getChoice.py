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
        				
        #Layout intermédiaire : création et peuplement des gpes radios
        self.layoutH_radio = QHBoxLayout()
        self.layoutH_radio.addWidget(self.QGBox0)
        self.layoutH_radio.addStretch(1)

## PART 2
        # créer un bouton
        self.bouton_OK = QPushButton("OK", self)
        self.bouton_OK.clicked.connect(self.ok_Choice)
        self.bouton_Next = QPushButton("Next", self)
        self.bouton_Next.clicked.connect(self.Next_Choice)
        self.bouton_Previous = QPushButton("Previous", self)
        self.bouton_Previous.clicked.connect(self.Previous_Choice)
        self.bouton_Previous.setEnabled(False) #default
        
        hbox_button = QHBoxLayout()
        hbox_button.addWidget(self.bouton_Previous)
        hbox_button.addWidget(self.bouton_Next)
        hbox_button.addStretch(1)
        hbox_button.addWidget(self.bouton_OK)
        # positionner les widgets dans la fenêtre
        posit = QVBoxLayout()
        posit.addLayout(self.layoutH_radio)
        posit.addLayout(vbox_H0)
        posit.addLayout(hbox_button)

        self.setLayout(posit)
 
    def ok_Choice(self):
        tptp = [str(self.my_choice_rel_0), str(self.my_choice_ref_0),str(self.my_choice_rel_1), str(self.my_choice_ref_1)]
        self.emit(SIGNAL("fermeturegetChoice(PyQt_PyObject)"), tptp) 
        # fermer la fenêtre
        self.close()
 
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
                        
