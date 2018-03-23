#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

def initGpNextPrevious(self):
    print "initGpNextPrevious"
    
    # créer un bouton
    self.bouton_Next = QPushButton("Next", self)
    self.bouton_Next.clicked.connect(self.Next_Choice) # 
    self.bouton_Previous = QPushButton("Previous", self)
    self.bouton_Previous.clicked.connect(self.Previous_Choice) # 
    self.bouton_Previous.setEnabled(False) #default
    self.bouton_Previous.setText(self.trUtf8(self.tasks_list[0]))
    
         
    #label button creation
    txt = "(" + str(self.tasks_counter) + ",1) Next : " + self.tasks_list[1]
    self.labelCombo3 = QLabel(self.trUtf8(txt), self)

    return

def initQuit(self):
    print("initQuit")
        
    # Création du bouton quitter, ayant pour parent la "fenetre"
    self.bouton_Quit = QPushButton(self.trUtf8("Quitter ?"),self)
    self.bouton_Quit.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
    #self.bouton_Quit.setIcon(QIcon("../images/smile.png"))
    self.connect(self.bouton_Quit, SIGNAL("clicked()"), qApp, SLOT("quit()"))
    
    return

def initHelp(self):
    print("initHelp")
    
    # Création du bouton Help
    self.bouton_Help = QPushButton(self.trUtf8("Help"),self)
    self.connect(self.bouton_Help, SIGNAL("clicked()"), self.showHelp) # to be done
    return

def initAbout(self):
    print("initAbout")
    
    # Création du bouton About
    self.bouton_About = QPushButton(self.trUtf8("About"),self)
    self.bouton_About.setIcon(QIcon("GUI_00.png"))
    self.connect(self.bouton_About, SIGNAL("clicked()"), self.showAbout) #

    return

def initGpBottom(self):

    # Next/Previous
    initGpNextPrevious(self)
    
    # Help
    initHelp(self)
    
    # About
    initAbout(self)
    
    # Quit
    initQuit(self)
    
    #Layout intermédiaire : boutons
    self.layoutH_boutons = QHBoxLayout()
    self.layoutH_boutons.addWidget(self.bouton_Previous)
    self.layoutH_boutons.addWidget(self.bouton_Next)
    self.layoutH_boutons.addWidget(self.labelCombo3)
    self.layoutH_boutons.addStretch(1)
    self.layoutH_boutons.addWidget(self.bouton_About)
    self.layoutH_boutons.addWidget(self.bouton_Help)
    self.layoutH_boutons.addStretch(1)
    self.layoutH_boutons.addWidget(self.bouton_Quit)

    return


