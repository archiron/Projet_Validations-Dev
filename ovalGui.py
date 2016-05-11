#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files
from fonctions import list_search_0, list_search_1, list_search, explode_item, sub_releases
from fonctions import list_simplify, create_file_list, create_commonfile_list, cmd_working_dirs_creation
from getChoice import *
#from getPublish import *
		
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Validations gui v0.0.1')

        self.cmsenv = env()
        self.texte = self.cmsenv.cmsAll()
        self.choix_calcul = 'Full'   # default
        self.choice_rel = ""
        self.choice_ref = ""
        self.coll_list = []
        self.files_list = []
        self.my_choice_rel = "" # release to work on
        self.my_choice_ref = "" # reference for comparison
        self.working_dir_base = os.getcwd()
        self.working_dir_rel = os.getcwd()
        self.working_dir_ref = os.getcwd()
        
        self.releasesList_0 = list_search_0(self) # list of releases in https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/
        self.my_choice_rel_0 = "" # 
        self.my_choice_rel_1 = "" # 
        self.my_choice_ref_0 = "" # 
        self.my_choice_ref_1 = "" # 
        self.rel_list_0 = []
        self.ref_list_0 = []
        self.profondeur_rel = 0
        self.profondeur_ref = 0
						
		# creation du grpe Calcul
        self.QGBox1 = QGroupBox("Calcul")
        self.QGBox1.setMaximumHeight(150)
        self.QGBox1.setMaximumWidth(100)
        self.radio11 = QRadioButton("FULL") # par defaut
        self.radio12 = QRadioButton("PU")
        self.radio13 = QRadioButton("FAST")
        self.radio11.setChecked(True)
        self.connect(self.radio11, SIGNAL("clicked()"), self.radio11Clicked) 
        self.connect(self.radio12, SIGNAL("clicked()"), self.radio12Clicked) 
        self.connect(self.radio13, SIGNAL("clicked()"), self.radio13Clicked) 
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.radio11)
        vbox1.addWidget(self.radio12)
        vbox1.addWidget(self.radio13)
        vbox1.addStretch(1)
        self.QGBox1.setLayout(vbox1)
        				
		# creation du grpe liste des collections
        self.QGBox31 = QGroupBox("Data Sets")
        self.QGBox32 = QGroupBox("Data Sets")
        self.QGBox31.setMaximumHeight(150)
        self.QGBox32.setMaximumHeight(150)
        self.QGBox31.setVisible(True)
        self.QGBox32.setVisible(False)
        self.check31 = QCheckBox("Pt10Startup_UP15")
        self.check32 = QCheckBox("Pt35Startup_UP15")
        self.check33 = QCheckBox("Pt1000Startup_UP15")
        self.check34 = QCheckBox("QcdPt80120Startup_13") # ex QcdPt80Pt120Startup_13
        self.check35 = QCheckBox("TTbarStartup_13")
        self.check36 = QCheckBox("ZEEStartup_13")
        self.check37 = QCheckBox("TTbarStartup_13")
        self.check38 = QCheckBox("ZEEStartup_13")
        self.check31.setChecked(True)
        self.check32.setChecked(True)
        self.check33.setChecked(True)
        self.check34.setChecked(True)
        self.check35.setChecked(True)
        self.check36.setChecked(True)
        self.check37.setChecked(True)
        self.check38.setChecked(True)
        qform31 = QFormLayout() # new
        qform31.addRow(self.check31, self.check32) # new
        qform31.addRow(self.check33, self.check34) # new
        qform31.addRow(self.check35, self.check36) # new
        self.QGBox31.setLayout(qform31) # new
        qform32 = QFormLayout() # new
        qform32.addRow(self.check37, self.check38) # new
        self.QGBox32.setLayout(qform32) # new
        
		# creation du grpe All/None
        self.QGBoxAllNone = QGroupBox("All / None")
        self.QGBoxAllNone.setMaximumHeight(150)
        self.QGBoxAllNone.setMinimumHeight(150)
        self.checkAllNone1 = QRadioButton("All")
        self.checkAllNone2 = QRadioButton("None")
        self.checkAllNone1.setChecked(True)
        self.connect(self.checkAllNone1, SIGNAL("clicked()"), self.checkAllNone1Clicked)
        self.connect(self.checkAllNone2, SIGNAL("clicked()"), self.checkAllNone2Clicked)
        vboxAllNone = QVBoxLayout()
        vboxAllNone.addWidget(self.checkAllNone1)
        vboxAllNone.addWidget(self.checkAllNone2)
        vboxAllNone.addStretch(1)
        self.QGBoxAllNone.setLayout(vboxAllNone)
                				
		# creation des texEdit pour release/reference
        self.QGBox6 = QGroupBox("release")
        self.QGBox6.setMaximumHeight(150)
        self.QGBox6.setMinimumHeight(150)
        self.QGBox6.setMinimumWidth(250)
        
        self.labelCombo1 = QLabel(self.trUtf8("Release"), self)
        self.listeReference1 = QComboBox()
        self.listeReference1.setSizeAdjustPolicy(self.listeReference1.AdjustToContents)
        self.connect(self.listeReference1, SIGNAL("currentIndexChanged(int)"), self.listeReferencehighlighted1)
        self.listeReference1.addItem("Release")
        self.listeReference1.addItem("Init")
        for elems in self.releasesList_0:
            self.listeReference1.addItem(elems)
        self.labelCombo2 = QLabel(self.trUtf8("Reference"), self)
        self.listeReference2 = QComboBox()
        self.listeReference2.setSizeAdjustPolicy(self.listeReference2.AdjustToContents)
        self.connect(self.listeReference2, SIGNAL("currentIndexChanged(int)"), self.listeReferencehighlighted2)
        self.listeReference2.addItem("Reference")
        self.listeReference2.addItem("Init")
        for elems in self.releasesList_0:
            self.listeReference2.addItem(elems)

        hbox63 = QHBoxLayout()
        hbox63.addWidget(self.labelCombo1)
        hbox63.addWidget(self.listeReference1)
        hbox64 = QHBoxLayout()
        hbox64.addWidget(self.labelCombo2)
        hbox64.addWidget(self.listeReference2)

        vbox6 = QVBoxLayout()
        vbox6.addLayout(hbox63)
        vbox6.addLayout(hbox64)
        vbox6.addStretch(1)
        self.QGBox6.setLayout(vbox6)

        #Layout intermédiaire : création et peuplement des gpes radios
        self.layoutH_radio = QHBoxLayout()
        self.layoutH_radio.addWidget(self.QGBox1)
        self.layoutH_radio.addWidget(self.QGBox31)
        self.layoutH_radio.addWidget(self.QGBox32)
        self.layoutH_radio.addWidget(self.QGBoxAllNone)
        self.layoutH_radio.addStretch(1)
        self.layoutH_radio.addWidget(self.QGBox6)

        # Création du bouton Get choice !, ayant pour parent la "fenetre"
        self.bouton3 = QPushButton(self.trUtf8("Get choice !"),self)
        self.bouton3.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.bouton3.setIcon(QIcon("../images/smile.png"))
        self.connect(self.bouton3, SIGNAL("clicked()"), self.liste4) 

        # Création du bouton quitter, ayant pour parent la "fenetre"
        self.boutonQ = QPushButton(self.trUtf8("Quitter ?"),self)
        self.boutonQ.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.boutonQ.setIcon(QIcon("../images/smile.png"))
        self.connect(self.boutonQ, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        
        #Layout intermédiaire : boutons
        self.layoutH_boutons = QHBoxLayout()
        self.layoutH_boutons.addWidget(self.bouton3)
        self.layoutH_boutons.addStretch(1)
        self.layoutH_boutons.addWidget(self.boutonQ)

		# creation du label resumé
        self.labelResume = QLabel(self.trUtf8(self.texte), self)
		# creation du grpe Folders paths
        self.QGBox8 = QGroupBox("Folders paths")
        vbox8 = QVBoxLayout()
        vbox8.addWidget(self.labelResume)
        self.QGBox8.setLayout(vbox8)

        #Layout intermédiaire : ComboBox + labelcombo
        self.layoutV_combobox = QVBoxLayout()
        self.layoutV_combobox.addWidget(self.QGBox8)
        
        # creation des onglets
        self.onglets = QTabWidget()
        self.generalTab = QWidget()
        self.generalTab.setMinimumHeight(170)
        self.onglets.insertTab(0, self.generalTab, "General")
        #Set Layout for Tabs Pages
        self.generalTab.setLayout(self.layoutV_combobox)   

        #Layout principal : création et peuplement
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.layoutH_radio)
        self.layout_general.addWidget(self.onglets)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)

    def liste4(self):
#        cmd_working_dirs_creation(self) # create rel/ref directories - to be done later
#        print "liste 4 Get Choice"
        
        if not os.path.exists(self.working_dir_rel):
            os.chdir(self.working_dir_base) # going to base folder
            print "liste 4 - Creation of (%s) folder" % str(self.lineedit1.text()[6:])
            os.makedirs(str(self.lineedit1.text()[6:]))

        os.chdir(self.working_dir_rel)   # Change current working directory
        if not os.path.exists(self.working_dir_ref):
            print "liste 4 - Creation of (%s) folder" % str(self.lineedit3.text()[6:])
            os.makedirs(str(self.lineedit3.text()[6:]))
#        list_search(self) # va chercher tous les fichiers
        to_transmit = [str("lineedit1"), str("lineedit3"), self.rel_list_0, self.ref_list_0] # [str(self.lineedit1.text()), str(self.lineedit3.text()), self.rel_list, self.ref_list] # temporaly removed
        self.getChoice_update(to_transmit)
              
    def getChoice_update(self, to_transmit):
        from operator import itemgetter
        """Lance la deuxième fenêtre"""
        self.getChoice = GetChoice()
        print "\ngetChoice_update - to_transmit : ", to_transmit
        
        self.rel_list_mod = []
        self.ref_list_mod = []
        self.rel_list_mod2 = []
        self.ref_list_mod2 = []
    
        # en cas de signal "fermeturegetChoice()" reçu de self.getChoice => exécutera clienchoice 
        self.connect(self.getChoice, SIGNAL("fermeturegetChoice(PyQt_PyObject)"), self.clientchoice) 
        # la deuxième fenêtre sera 'modale' (la première fenêtre sera inactive)
        self.getChoice.setWindowModality(QtCore.Qt.ApplicationModal)
        # appel de la deuxième fenêtre
        self.getChoice.show()

    def clientchoice(self, x):
        """affiche le résultat x transmis par le signal à l'arrêt de la deuxième fenêtre"""
        print "recuperation = ", x, "\n" # to be removed
        self.my_choice_rel_0 = x[0]
        self.my_choice_ref_0 = x[1]
        self.my_choice_rel_1 = x[2]
        self.my_choice_ref_1 = x[3]
        tmp = self.trUtf8(self.texte) 
        tmp += "<br /><strong>Release : </strong>"
        if ( self.my_choice_rel_0 ) :
            print "clientchoice : self.my_choice_rel_0 : %s " % self.my_choice_rel_0
            tmp += self.my_choice_rel_0 # 
            tmp += ' - ' + self.my_choice_rel1 # 
#            tmp += ' - ' + str(self.my_choice_rel[2]) # to not write self.my_choice_rel[3]
        tmp += "<br /><strong>Reference : </strong>"
        if ( self.my_choice_ref_0 ) :
            print "clientchoice : self.my_choice_ref_0 : %s " % self.my_choice_ref_0
            tmp += str(self.my_choice_ref_0) # 
            tmp += ' - ' + self.my_choice_ref1 # 
#            tmp += ' - ' + str(self.my_choice_ref[2]) # to not write self.my_choice_ref[3]
        self.labelResume.setText(tmp)
        QtCore.QCoreApplication.processEvents()
#        self.bouton5.setEnabled(False) # to be seen later
#        if ( self.my_choice_rel ) :
#            if ( self.my_choice_ref ) :
#                self.bouton5.setEnabled(True)

    def buttons_relClicked(self):
        i = 0
        k = 0
        for items in self.rel_list_mod2:
            j = 0
            items = (items[0], items[1], items[2])
            for items2 in items:
                if ( j == 1 ):
                    if self.buttons_rel[i].isChecked():
                        self.my_choice_rel = self.rel_list_mod2[k]
                        self.choice_rel = self.rel_list_mod2[k]
                j += 1
                i += 1
            k += 1
        QtCore.QCoreApplication.processEvents()

    def buttons_refClicked(self):
        i = 0
        k = 0
        for items in self.ref_list_mod2:
            j = 0
            items = (items[0], items[1], items[2])
            for items2 in items:
                if ( j == 1 ):
                    if self.buttons_ref[i].isChecked():
                        self.my_choice_ref = self.ref_list_mod2[k]
                        self.choice_ref = self.ref_list_mod2[k]
                j += 1
                i += 1
            k += 1
        QtCore.QCoreApplication.processEvents()
                                
    def radio11Clicked(self):
        if self.radio11.isChecked():
            self.QGBox31.setVisible(True)
            self.QGBox32.setVisible(False)
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()

    def radio12Clicked(self):
        if self.radio12.isChecked():
            self.QGBox31.setVisible(False)
            self.QGBox32.setVisible(True)
            self.choix_calcul = 'PileUp'
        QtCore.QCoreApplication.processEvents()
        
    def radio13Clicked(self):
        if self.radio13.isChecked():
            self.QGBox31.setVisible(False)
            self.QGBox32.setVisible(True)
            self.choix_calcul = 'Fast'
        QtCore.QCoreApplication.processEvents()
                        
    def checkAllNone1Clicked(self):
        if self.checkAllNone1.isChecked():
#            print "All"
            self.check31.setChecked(True)
            self.check32.setChecked(True)
            self.check33.setChecked(True)
            self.check34.setChecked(True)
            self.check35.setChecked(True)
            self.check36.setChecked(True)
            self.check37.setChecked(True)
            self.check38.setChecked(True)
        QtCore.QCoreApplication.processEvents() 

    def checkAllNone2Clicked(self):
        if self.checkAllNone2.isChecked():
#            print "None"
            self.check31.setChecked(False)
            self.check32.setChecked(False)
            self.check33.setChecked(False)
            self.check34.setChecked(False)
            self.check35.setChecked(False)
            self.check36.setChecked(False)
            self.check37.setChecked(False)
            self.check38.setChecked(False)
        QtCore.QCoreApplication.processEvents() 

    def listeReferencehighlighted1(self):
        print "coucou 1 - index", self.listeReference1.currentText(), '-', self.listeReference1.currentIndex()
        print "coucou 1 - profondeur", self.profondeur_rel
        self.my_choice_rel_1 = self.listeReference1.currentText()
        index_rel = self.listeReference1.currentIndex()
        if self.listeReference1.currentIndex() > 1:
            print "coucou 1b", self.listeReference1.currentText()
            temp = list_search_1(self.my_choice_rel_1)
            if ( len(temp) == 0 ): # we do not have to go here since it's tested on list_search_0
                print "Warning : no sub releases nor files inside !"
                BoiteMessage = QMessageBox()
                BoiteMessage.setText("Warning : no sub releases nor files inside !")
                BoiteMessage.setWindowTitle("WARNING !")
                BoiteMessage.exec_()
            else:
                print "sub releases - len : ", len(temp)
                # tester si self.profondeur = 1. oui: on choisit la sous release, non: on reaffiche la liste
                if ( self.profondeur_rel == 1 ):
                    print "profondeur 1 : ", self.listeReference1.currentText()
                    self.my_choice_rel_1 = self.listeReference1.currentText()
                    self.listeReference1.setCurrentIndex(index_rel)
                else:
                    self.profondeur_rel = 1 # 
                    self.rel_list_0 = sub_releases(temp)
                    tmp1 = sorted(list(set(self.rel_list_0)))
                    self.rel_list_0 = tmp1
                    i = 0
                    self.listeReference1.clear()
                    self.listeReference1.addItem("Release")
                    self.listeReference1.addItem("Init")
                    for items in self.rel_list_0:
#                        print "%d : %s" % (i+1, items)
                        self.listeReference1.addItem(items)
                        i += 1
        if self.listeReference1.currentIndex() == 1:
            print "coucou 1b - Init"
            self.listeReference1.clear()
            self.listeReference1.addItem("Release")
            self.listeReference1.addItem("Init")
            self.profondeur_rel = 0 # remet la profondeur a 0
            for elems in self.releasesList_0:
                self.listeReference1.addItem(elems)

    def listeReferencehighlighted2(self):
        print "coucou 2 - index", self.listeReference2.currentText()
        print "coucou 2 - profondeur", self.profondeur_ref
        self.my_choice_ref_1 = self.listeReference2.currentText()
        index_ref = self.listeReference2.currentIndex()
        if self.listeReference2.currentIndex() > 1:
            print "coucou 2b", self.listeReference2.currentText()
            temp = list_search_1(self.my_choice_ref_1)
            if ( len(temp) == 0 ): # we do not have to go here since it's tested on list_search_0
                print "Warning : no sub releases nor files inside !"
                BoiteMessage = QMessageBox()
                BoiteMessage.setText("Warning : no sub releases nor files inside !")
                BoiteMessage.setWindowTitle("WARNING !")
                BoiteMessage.exec_()
            else:
                print "sub releases - len : ", len(temp)
                # tester si self.profondeur = 2. oui: on choisit la sous release, non: on reaffiche la liste
                if ( self.profondeur_ref == 1 ):
                    print "profondeur 1 : ", self.listeReference2.currentText()
                    self.my_choice_ref_1 = self.listeReference2.currentText()
                    self.listeReference2.setCurrentIndex(index_ref)
                else:
                    self.profondeur_ref = 1 # 
                    self.ref_list_0 = sub_releases(temp)
                    tmp2 = sorted(list(set(self.ref_list_0)))
                    self.ref_list_0 = tmp2
                    i = 0
                    self.listeReference2.clear()
                    self.listeReference2.addItem("Reference")
                    self.listeReference2.addItem("Init")
                    for items in self.ref_list_0:
#                       print "%d : %s" % (i+1, items)
                        self.listeReference2.addItem(items)
                        i += 1
        if self.listeReference2.currentIndex() == 1:
            print "coucou 2 - Init"
            self.listeReference2.clear()
            self.listeReference2.addItem("Reference")
            self.listeReference2.addItem("Init")
            self.profondeur_ref = 0
            for elems in self.releasesList_0:
                self.listeReference2.addItem(elems)

