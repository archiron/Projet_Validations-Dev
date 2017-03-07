#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files
from fonctions import list_search_0, list_search_2, list_search_3, list_search, explode_item
from fonctions import list_simplify, create_file_list, create_commonfile_list, cmd_working_dirs_creation
from functionGui import initDataSets
from getChoice import *
from Datasets_default import DataSetsFilter
from Paths_default import *
#from getPublish import *
		
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Validations gui v0.1.3')

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
        self.releasesList_rel_1 = []
        self.releasesList_ref_1 = []
        self.my_choice_rel_0 = "" # 
        self.my_choice_rel_1 = "" # 
        self.my_choice_ref_0 = "" # 
        self.my_choice_ref_1 = "" # 
        self.rel_list_0 = []
        self.ref_list_0 = []
        self.rel_list_1 = []
        self.ref_list_1 = []
        self.rel_list_2 = []
        self.ref_list_2 = []
        self.profondeur_rel = 0
        self.profondeur_ref = 0
        self.tasks_list = ['Release', 'Reference', 'DataSets', 'Lists']
        self.tasks_counter = 0
        self.selectedDataSets = []
						
        ## PART 1 ##
		# creation du grpe Calcul
        self.QGBox1 = QGroupBox("Calcul")
        self.QGBox1.setMaximumHeight(120)
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
        				
		# creation du grpe liste des collections new version
        self.QGBoxDataSets = QGroupBox("DataSets")
        self.QGBoxDataSets.setMaximumHeight(120)
        self.QGBoxDataSets.setMinimumHeight(120)
        self.checkDataSets1 = QPushButton("List")
        self.checkDataSets2 = QPushButton("Reload")
        self.connect(self.checkDataSets2, SIGNAL("clicked()"), self.checkDataSets2Clicked)
        self.menu = QMenu()
        self.DataSetTable = DataSetsFilter(self)
        for it in self.DataSetTable:
            self.menu.addAction(it)
        self.checkDataSets1.setMenu(self.menu)
        self.selectedDataSets = self.DataSetTable # default, all datasets selected
#        print self.selectedDataSets
        vboxDataSets = QVBoxLayout()
        vboxDataSets.addWidget(self.checkDataSets1)
        vboxDataSets.addWidget(self.checkDataSets2)
        vboxDataSets.addStretch(1)
        self.QGBoxDataSets.setLayout(vboxDataSets)
        
		# creation du grpe All/None
        self.QGBoxAllNone = QGroupBox("All / None")
        self.QGBoxAllNone.setMaximumHeight(120)
        self.QGBoxAllNone.setMinimumHeight(120)
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
        self.QGBoxRelRef = QGroupBox("release")
        self.QGBoxRelRef.setMaximumHeight(120)
        self.QGBoxRelRef.setMinimumHeight(120)
        self.QGBoxRelRef.setMinimumWidth(250)
        
        self.labelCombo1 = QLabel(self.trUtf8("Release"), self)
        self.labelCombo2 = QLabel(self.trUtf8("Reference"), self)

        vbox6 = QVBoxLayout()
        vbox6.addWidget(self.labelCombo1) 
        vbox6.addWidget(self.labelCombo2) 
        vbox6.addStretch(1)
        self.QGBoxRelRef.setLayout(vbox6)

        #Layout intermédiaire : création et peuplement des gpes radios
        self.layoutH_radio = QHBoxLayout()
        self.layoutH_radio.addWidget(self.QGBox1)
        self.layoutH_radio.addWidget(self.QGBoxAllNone)
        self.layoutH_radio.addWidget(self.QGBoxDataSets)
        self.layoutH_radio.addStretch(1)
        self.layoutH_radio.addWidget(self.QGBoxRelRef)

        ## PART 2 ##
        # Resume
        self.QText_Resume = QTextEdit()
        self.QText_Resume.setMinimumHeight(170)
        self.QText_Resume.setMaximumHeight(170)
        self.QText_Resume.setReadOnly(True)
        self.QText_Resume.setText(self.trUtf8(self.texte))
        vbox8 = QVBoxLayout()
        vbox8.addWidget(self.QText_Resume)
		# creation du grpe Folders paths
        self.QGBoxResume = QGroupBox("Resume")
        self.QGBoxResume.setMinimumHeight(250)
        self.QGBoxResume.setMaximumHeight(250)
        self.QGBoxResume.setLayout(vbox8)
        self.layoutH_resume = QHBoxLayout()
        self.layoutH_resume.addWidget(self.QGBoxResume)
        
        ## BOTTOM PART ##
        # créer un bouton
        self.bouton_Next = QPushButton("Next", self)
        self.bouton_Next.clicked.connect(self.Next_Choice)
        self.bouton_Previous = QPushButton("Previous", self)
        self.bouton_Previous.clicked.connect(self.Previous_Choice)
        self.bouton_Previous.setEnabled(False) #default
        self.bouton_Previous.setText(self.trUtf8(self.tasks_list[0]))
        
        #label button creation
        txt = "(" + str(self.tasks_counter) + ",1) Next : " + self.tasks_list[1]
        self.labelCombo3 = QLabel(self.trUtf8(txt), self)

        # Création du bouton quitter, ayant pour parent la "fenetre"
        self.boutonQ = QPushButton(self.trUtf8("Quitter ?"),self)
        self.boutonQ.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.boutonQ.setIcon(QIcon("../images/smile.png"))
        self.connect(self.boutonQ, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        
        #Layout intermédiaire : boutons
        self.layoutH_boutons = QHBoxLayout()
        self.layoutH_boutons.addWidget(self.bouton_Previous)
        self.layoutH_boutons.addWidget(self.bouton_Next)
        self.layoutH_boutons.addWidget(self.labelCombo3)
        self.layoutH_boutons.addStretch(1)
        self.layoutH_boutons.addWidget(self.boutonQ)

        ## PART 3 ##
        # release/reference
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

        # DataSets
        self.QGBox_Lists= QGroupBox("Lists") # default
        self.QGBox_Lists.setMinimumHeight(250)
        self.QGBox_Lists.setMaximumHeight(250)
        self.QHL_Lists = QHBoxLayout(self.QGBox_Lists) 
        
        self.QGBox_rel = QGroupBox("Release")
        self.QGBox_rel.setMinimumWidth(250)
        self.QGBox_rel.setMaximumWidth(250)
        self.vbox_rel4 = QVBoxLayout()
        self.QLW_rel_dataset = QListWidget()
        item = QListWidgetItem("%s" % "")
        self.QLW_rel_dataset.addItem(item)
#        self.connect(self.QLW_rel_dataset, SIGNAL("itemSelectionChanged()"),self.ItemRelRefClicked3)
        self.vbox_rel4.addWidget(self.QLW_rel_dataset) 
        self.QGBox_rel.setLayout(self.vbox_rel4)
        
        self.QGBox_ref = QGroupBox("Reference")
        self.QGBox_ref.setMinimumWidth(250)
        self.QGBox_ref.setMaximumWidth(250)
        self.vbox_ref4 = QVBoxLayout()
        self.QLW_ref_dataset = QListWidget()
        item = QListWidgetItem("%s" % "")
        self.QLW_ref_dataset.addItem(item)
#        self.connect(self.QLW_ref_dataset, SIGNAL("itemSelectionChanged()"),self.ItemRelRefClicked3)
        self.vbox_ref4.addWidget(self.QLW_ref_dataset) 
        self.QGBox_ref.setLayout(self.vbox_ref4)
        
        self.QHL_Lists.addWidget(self.QGBox_rel)
        self.QHL_Lists.addWidget(self.QGBox_ref)
        self.layout_Lists = QVBoxLayout()
        self.layout_Lists.addWidget(self.QGBox_Lists)
        self.QGBox_Lists.setVisible(False)

        # DataSets
        self.QGBox_DataSets = QGroupBox("DataSets")
        self.QGBox_DataSets.setMinimumWidth(250)
        self.QGBox_DataSets.setMaximumWidth(250)
        #self.QHL_DataSets = QHBoxLayout(self.QGBox_DataSets) 
        self.vbox_ds = QVBoxLayout()
        self.QLW_dataset = QListWidget()
        initDataSets(self)
#        for it in self.selectedDataSets:
#            print "== step 0 ==", it
#            item = QListWidgetItem("%s" % it)
#            self.QLW_dataset.addItem(item)
        self.vbox_ds.addWidget(self.QLW_dataset) 
        self.QGBox_DataSets.setLayout(self.vbox_ds)
        self.layout_DataSets = QVBoxLayout()
        self.layout_DataSets.addWidget(self.QGBox_DataSets)
        self.layout_DataSets.setAlignment(QtCore.Qt.AlignHCenter)
        self.QGBox_DataSets.setVisible(False)

        ## FINAL PART ##
        #Layout principal : création et peuplement
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.layoutH_radio)
        self.layout_general.addLayout(self.layoutH_resume)
        self.layout_general.addLayout(self.layout_Search)
        self.layout_general.addLayout(self.layout_Lists)
        self.layout_general.addLayout(self.layout_DataSets)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)

    def radio11Clicked(self):
        if self.radio11.isChecked():
            self.choix_calcul = 'Full'
        QtCore.QCoreApplication.processEvents()

    def radio12Clicked(self):
        if self.radio12.isChecked():
            self.choix_calcul = 'PileUp'
        QtCore.QCoreApplication.processEvents()
        
    def radio13Clicked(self):
        if self.radio13.isChecked():
            self.choix_calcul = 'Fast'
        QtCore.QCoreApplication.processEvents()
                        
    def checkAllNone1Clicked(self):
        if self.checkAllNone1.isChecked():
#            print "All"
            initDataSets(self)
#            self.QLW_dataset.clear()
#            for item in self.DataSetTable:
#                item1 = QListWidgetItem("%s" % item)
#                item1.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
#                item1.setCheckState(QtCore.Qt.Checked)
#                self.QLW_dataset.addItem(item1)
        QtCore.QCoreApplication.processEvents() 

    def checkAllNone2Clicked(self):
        if self.checkAllNone2.isChecked():
#            print "None"
            self.QLW_dataset.clear() # clear all datasets
        QtCore.QCoreApplication.processEvents() 

    def checkDataSets2Clicked(self):
        reload(sys.modules['Datasets_default'])
        from Datasets_default import DataSetsFilter
        self.DataSetTable = DataSetsFilter(self)
        self.menu.clear()
        for it in self.DataSetTable:
            self.menu.addAction(it)
        initDataSets(self)
#        self.QLW_dataset.clear()
#        for it in self.DataSetTable: # list of DataSets
#            item = QListWidgetItem("%s" % it)
#            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
#            item.setCheckState(QtCore.Qt.Checked)
#            self.QLW_dataset.addItem(item)
    
    def ItemRelRefClicked1(self):
        self.QGBox_rel2.setTitle(self.QLW_rel1.currentItem().text())        
        self.QLW_rel2.clear()
        if self.QGBox_rel0.title() == "Reference list":
            print "reference"
            self.my_choice_ref_0 = self.QLW_rel1.currentItem().text()
            print "ItemRefClicked1 : self.my_choice_ref_0 : %s " % self.my_choice_ref_0
            self.releasesList_ref_1 = list_search_1(self.my_choice_ref_0)
            self.ref_list_0 = sub_releases(self.releasesList_ref_1) #list_search_1(self.my_choice_ref_0))
            for it in self.ref_list_0:
                item = QListWidgetItem("%s" % it)
                self.QLW_rel2.addItem(item)
        else:
            print "release"
            self.my_choice_rel_0 = self.QLW_rel1.currentItem().text()
            print "ItemRelRefClicked1 : self.my_choice_rel_0 : %s " % self.my_choice_rel_0
            self.releasesList_rel_1 = list_search_1(self.my_choice_rel_0)
            self.rel_list_0 = sub_releases(self.releasesList_rel_1) #list_search_1(self.my_choice_rel_0))
            # tester si =0 
            for it in self.rel_list_0:
                item = QListWidgetItem("%s" % it)
                self.QLW_rel2.addItem(item)
        
    def ItemRelRefClicked2(self):
        rel_text = self.QLW_rel2.currentItem().text() + " DataSets"
        if self.QGBox_rel0.title() == "Reference list":
            print "reference"
            self.my_choice_ref_1 = self.QLW_rel2.currentItem().text()
            print "ItemRefClicked2 : self.my_choice_ref_1 : %s " % self.my_choice_ref_1
            tmp = "Reference : " + self.my_choice_ref_1
            self.labelCombo2.setText(tmp)
            self.releasesList_ref_2 = list_search_3(self.releasesList_ref_1, str(self.my_choice_ref_1))
            self.ref_list_1 = sub_releases2(str(self.my_choice_ref_1), self.releasesList_ref_2)
        else:
            print "release"
            self.my_choice_rel_1 = self.QLW_rel2.currentItem().text()
            print "ItemRelRefClicked2 : self.my_choice_rel_1 : %s " % self.my_choice_rel_1
            tmp = "Release : " + self.my_choice_rel_1
            self.labelCombo1.setText(tmp)
            self.releasesList_rel_2 = list_search_3(self.releasesList_rel_1, str(self.my_choice_rel_1))
            #### TEMP
 #           with open("releasesList_rel_2.txt", "w+") as f:
 #               f.write(self.my_choice_rel_1 + "\n")
 #               for line in self.releasesList_rel_2:
 #                   f.write(line + "\n") # write the line
 #               f.close()
            #### TEMP
            self.rel_list_1 = sub_releases2(str(self.my_choice_rel_1), self.releasesList_rel_2)
        resume_text = self.texte
        resume_text += "<br />Release   : " + self.my_choice_rel_1
        resume_text += "<br />Reference : " + self.my_choice_ref_1
        self.QText_Resume.setText(self.trUtf8(resume_text))
        
    def ItemRelRefClicked3(self): # to be used later
        #self.QGBox_rel4.setTitle(self.QLW_rel3.currentItem().text())
        #self.my_choice_rel_1 = self.QLW_rel2.currentItem().text()
        print "ItemRelRefClicked3 : self.my_choice_rel_1 : %s " % self.QLW_rel3.currentItem().text()
        
    def Next_Choice(self):
        print "Next_Choice: "
        if self.tasks_counter + 1 > len(self.tasks_list) - 1:
            print "no way : %i" % self.tasks_counter
            self.bouton_Next.setEnabled(False)
        else:
            self.tasks_counter += 1
            if self.tasks_counter == len(self.tasks_list) - 1:
                self.bouton_Next.setEnabled(False)
                txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter) + ") Next : " 
                self.labelCombo3.setText(self.trUtf8(txt))
                self.bouton_Previous.setText(self.trUtf8(self.tasks_list[self.tasks_counter-1]))
                self.QGBox_Lists.setVisible(True)
                self.QGBox_DataSets.setVisible(False)
                self.QGBox_rel0.setVisible(False)
                self.selectedDataSets = []
                index = 0
                for it in self.DataSetTable:
                    item1 = QListWidgetItem (self.QLW_dataset.item(index) )
                    if item1.checkState() == 2:
                        self.selectedDataSets.append(it)
                    index += 1
                print "selectedDataSets : ", self.selectedDataSets

                self.rel_list_2 = list_search_2(self.rel_list_1, self.selectedDataSets)
                self.ref_list_2 = list_search_2(self.ref_list_1, self.selectedDataSets)
                self.QLW_rel_dataset.clear()
                for it in self.rel_list_2:
                    item = QListWidgetItem("%s" % it)
                    self.QLW_rel_dataset.addItem(item)
                self.QLW_ref_dataset.clear()
                for it in self.ref_list_2:
                    item = QListWidgetItem("%s" % it)
                    self.QLW_ref_dataset.addItem(item)
                
                # what to do if len(self.QLW_rel(f)_datasets) = 0?
                print BaseURL(self) # temporaire
                
            elif (self.tasks_counter == 2):
                print "*-*-**--*-*-*-*-*-*", self.tasks_list[2]
                self.bouton_Previous.setText(self.trUtf8(self.tasks_list[self.tasks_counter-1]))
                self.bouton_Next.setEnabled(True)
                txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter+1) + ") Next : "  + self.tasks_list[self.tasks_counter+1]
                self.labelCombo3.setText(self.trUtf8(txt))
                self.QGBox_Lists.setVisible(False)
                self.QGBox_rel0.setVisible(False)
                self.QGBox_DataSets.setVisible(True)
                initDataSets(self)
#                self.QLW_dataset.clear()
#                for it in self.DataSetTable: # list of DataSets
#                    print it, "******"
#                    item = QListWidgetItem("%s" % it)
#                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
#                    item.setCheckState(QtCore.Qt.Checked)
#                    self.QLW_dataset.addItem(item)
            else:
                self.bouton_Previous.setText(self.trUtf8(self.tasks_list[self.tasks_counter-1]))
                txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter+1) + ") Next : " + self.tasks_list[self.tasks_counter+1]
                self.labelCombo3.setText(self.trUtf8(txt))
                self.QGBox_Lists.setVisible(False)
                self.QGBox_rel0.setVisible(True)
                self.QGBox_DataSets.setVisible(False)

        if self.tasks_counter == 1:
            self.bouton_Previous.setEnabled(True)
            self.QGBox_rel0.setTitle("Reference list")
            self.QLW_rel1.clear()
            self.QLW_rel2.clear()
            self.QLW_rel_dataset.clear()
            self.QLW_ref_dataset.clear()
            self.labelCombo2.setText("Reference")
            for it in self.releasesList_0:
                item = QListWidgetItem("%s" % it)
                self.QLW_rel1.addItem(item)
        else :
            print self.tasks_list[self.tasks_counter]
        
    def Previous_Choice(self):
        print "Previous_Choice: "
        if self.tasks_counter - 1 < 0:
            print "no way : %i" % self.tasks_counter
            self.bouton_Previous.setEnabled(False)
        else:
            self.QGBox_Lists.setVisible(False)
            self.QGBox_DataSets.setVisible(False)
            self.QGBox_rel0.setVisible(True)
            self.tasks_counter -= 1
            if self.tasks_counter == 0:
                self.bouton_Previous.setEnabled(False)
                self.bouton_Previous.setText(self.trUtf8(self.tasks_list[0]))
            else:
                self.bouton_Previous.setText(self.trUtf8(self.tasks_list[self.tasks_counter-1]))
            txt = "(" + str(self.tasks_counter) + "," + str(self.tasks_counter+1) + ") Next : " + self.tasks_list[self.tasks_counter+1]
            self.labelCombo3.setText(self.trUtf8(txt))
        
        if self.tasks_counter == 0:
            self.bouton_Next.setEnabled(True)
            self.QGBox_rel0.setTitle("Release list")
            self.QLW_rel1.clear()
            self.QLW_rel2.clear()
            self.QLW_rel_dataset.clear()
            self.QLW_ref_dataset.clear()
            self.labelCombo1.setText("Release")
            for it in self.releasesList_0:
                item = QListWidgetItem("%s" % it)
                self.QLW_rel1.addItem(item)
        elif self.tasks_counter == 1:
            self.bouton_Next.setEnabled(True)
            self.QGBox_rel0.setTitle("Reference list")
            self.QLW_rel1.clear()
            self.QLW_rel2.clear()
            self.QLW_rel_dataset.clear()
            self.QLW_ref_dataset.clear()
            self.labelCombo2.setText("Reference")
            for it in self.releasesList_0:
                item = QListWidgetItem("%s" % it)
                self.QLW_rel1.addItem(item)
        elif self.tasks_counter == 2:
            self.bouton_Next.setEnabled(True)
            self.QGBox_rel0.setTitle("DataSets")
            self.QGBox_Lists.setVisible(False)
            self.QGBox_rel0.setVisible(False)
            self.QGBox_DataSets.setVisible(True)
        else :
            print self.tasks_list[self.tasks_counter]
