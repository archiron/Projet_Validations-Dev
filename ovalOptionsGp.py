#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

def initGpCalcul(self):
    print "initGpCalcul"

    self.QGBox1 = QGroupBox("Calcul")
    self.QGBox1.setMaximumHeight(120)
    self.QGBox1.setMaximumWidth(100)
    self.radio11 = QRadioButton("FULL") # par defaut
    self.radio12 = QRadioButton("FAST")
    self.radio11.setChecked(True)
    self.connect(self.radio11, SIGNAL("clicked()"), self.radio11Clicked) 
    self.connect(self.radio12, SIGNAL("clicked()"), self.radio12Clicked) 
    vbox1 = QVBoxLayout()
    vbox1.addWidget(self.radio11)
    vbox1.addWidget(self.radio12)
    vbox1.addStretch(1)
    self.QGBox1.setLayout(vbox1)
    return
    
def initGpValidation(self):
    print "initGpValidation"

    self.QGBox2 = QGroupBox("Validation")
    self.QGBox2.setMaximumHeight(120)
    self.QGBox2.setMaximumWidth(100)
    self.radio21 = QRadioButton("RECO") # par defaut
    self.radio22 = QRadioButton("PU")
    self.radio23 = QRadioButton("pmx")
    self.radio24 = QRadioButton("miniAOD")
    self.radio21.setChecked(True)
    self.connect(self.radio21, SIGNAL("clicked()"), self.radio21Clicked) 
    self.connect(self.radio22, SIGNAL("clicked()"), self.radio22Clicked) 
    self.connect(self.radio23, SIGNAL("clicked()"), self.radio23Clicked) 
    self.connect(self.radio24, SIGNAL("clicked()"), self.radio24Clicked) 
    vbox2 = QVBoxLayout()
    vbox2.addWidget(self.radio21)
    vbox2.addWidget(self.radio22)
    vbox2.addWidget(self.radio23)
    vbox2.addWidget(self.radio24)
    vbox2.addStretch(1)
    self.QGBox2.setLayout(vbox2)
    return
