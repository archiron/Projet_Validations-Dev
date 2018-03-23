#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

#def initGpTextResume(self):
#    self.QText_Resume = QTextEdit()
#    self.QText_Resume.setMinimumHeight(170)
#    self.QText_Resume.setMaximumHeight(170)
#    self.QText_Resume.setReadOnly(True)
#    self.QText_Resume.setText(self.trUtf8(self.texte))
#    return

def initGpLabelResume(self):
    self.LabelResume = QLabel("")
    self.LabelResume.setText(self.trUtf8(self.texte))
    return

def initButtonResume(self):
    self.buttonResume = QPushButton(self.trUtf8("Get list of operations")) # par defaut
    self.buttonResume.setMinimumWidth(150)
    self.buttonResume.setMaximumWidth(150)
    self.connect(self.buttonResume, SIGNAL("clicked()"), self.showResume) #
    return

def initGpMiddle(self):
#    initGpTextResume(self)
    initGpLabelResume(self)
    
    initButtonResume(self)
    
	#creation du grpe Resume
    self.QGBoxResume = QGroupBox("Resume")
    self.QGBoxResume.setMinimumHeight(200)
    self.QGBoxResume.setMaximumHeight(200)
    vbox8 = QHBoxLayout()
#    vbox8.addWidget(self.QText_Resume)
    vbox8.addWidget(self.LabelResume)
    vbox8.addWidget(self.buttonResume)
    self.QGBoxResume.setLayout(vbox8)
	#creation du layout Resume
    self.layoutH_resume = QHBoxLayout()
    self.layoutH_resume.addWidget(self.QGBoxResume)

    return
    