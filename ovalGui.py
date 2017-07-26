#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from Variables import *
from ovalOptionsGp import initGpOptions
from ovalChoiceGp import initGpChoice
from getEnv import env
#from fonctions import cmd_folder_creation, get_collection_list, get_validationType1, clean_files, copy_files  
from fonctions import list_search_1, list_search_3 # list_search_0, , list_search_2, list_search, explode_item
#from fonctions import list_simplify, create_file_list, create_commonfile_list, cmd_working_dirs_creation 
from fonctions import sub_releases, sub_releases2, print_arrays, list_search_5 #, list_search_4
from fonctions import checkFastvsFull
from Datasets_default import DataSetsFilter
from Paths_default import *
from functionGui import clearDataSets, clearDataSetsLists, writeLabelCombo3, changeFastvsFullSize
		
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Validations gui v0.1.8.0') # introducing the use of QTableWidget instead of QListWidget.
        
        # From top to bottom, there is 4 parts :
        # PART 1 : GroupBoxes for validation choice
        # PART 2 : Resume label for actions listing
        # PART 3 : GroupBoxes for Tag selection
        # BOTTOM PART : buttons
        # FINAL PART : keeping all previous part into one

        initVariables(self)
						
        ## PART 1 - Options Grp ##
        initGpOptions(self)
        
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
        self.bouton_Next.clicked.connect(self.Next_Choice) # 
        self.bouton_Previous = QPushButton("Previous", self)
        self.bouton_Previous.clicked.connect(self.Previous_Choice) # 
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
        initGpChoice(self)

        ## FINAL PART ##
        #Layout principal : création et peuplement
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.layoutH_radio)
        self.layout_general.addLayout(self.layoutH_resume)
        self.layout_general.addLayout(self.layout_Search)
        self.layout_general.addLayout(self.layout_Lists)
        self.layout_general.addLayout(self.layout_Selected)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)

    def radio11Clicked(self):
        if self.radio11.isChecked():
            changeFastvsFullSize(self)
            self.validationType1 = 'Full'
            self.checkDataSets2Clicked()
#            print "self.validationType1 :", self.validationType1
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()

    def radio12Clicked(self):
        if self.radio12.isChecked():
            changeFastvsFullSize(self)
            self.validationType1 = 'Fast'
            self.checkDataSets2Clicked()
#            print "self.validationType1 :", self.validationType1
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
        
    def radio21Clicked(self):
        if self.radio21.isChecked():
            changeFastvsFullSize(self)
            self.validationType2 = 'RECO'
            self.checkDataSets2Clicked()
            self.checkSpecificGlobal1.setEnabled(False) #default
            print "self.validationType2 :", self.validationType2
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()

    def radio22Clicked(self):
        if self.radio22.isChecked():
            changeFastvsFullSize(self)
            self.validationType2 = 'PU'
            self.checkDataSets2Clicked()
            self.checkSpecificGlobal1.setEnabled(False) #default
            print "self.validationType2 :", self.validationType2
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
        
    def radio23Clicked(self):
        if self.radio23.isChecked():
            changeFastvsFullSize(self)
            self.validationType2 = 'pmx'
            self.checkDataSets2Clicked()
            self.checkSpecificGlobal1.setEnabled(True)
            print "self.validationType2 :", self.validationType2
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
                        
    def radio24Clicked(self):
        if self.radio24.isChecked():
            changeFastvsFullSize(self)
            self.validationType2 = 'miniAOD'
            self.checkDataSets2Clicked()
            self.checkSpecificGlobal1.setEnabled(False) #default
            print "self.validationType2 :", self.validationType2
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
                        
    def checkAllNone1Clicked(self):
        if self.checkAllNone1.isChecked():
#            print "All"
            self.menu.clear()
            self.ag = QActionGroup(self, exclusive=False)
            for item in self.DataSetTable:
                a = self.ag.addAction(QAction(item, self, checkable=True, checked=True))
                self.menu.addAction(a)
                self.connect(a, SIGNAL('triggered()'), self.QGBoxListsUpdate)
            self.QGBoxListsUpdate() # needed ?
        QtCore.QCoreApplication.processEvents() 

    def checkAllNone2Clicked(self):
        if self.checkAllNone2.isChecked():
#            print "None"
            self.menu.clear()
            self.ag = QActionGroup(self, exclusive=False)
            for item in self.DataSetTable:
                a = self.ag.addAction(QAction(item, self, checkable=True, checked=False))
                self.menu.addAction(a)
                self.connect(a, SIGNAL('triggered()'), self.QGBoxListsUpdate)
            self.QGBoxListsUpdate() # needed ?
        QtCore.QCoreApplication.processEvents() 

    def checkSpecificGlobal1Clicked(self):
        if self.checkSpecificGlobal1.isChecked():
            self.validationType3 = 'specific'
#            print "Specific"
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents() 

    def checkSpecificGlobal2Clicked(self):
        if self.checkSpecificGlobal2.isChecked():
            self.validationType3 = 'global'
#            print "Global"
            self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents() 

    def checkDataSets2Clicked(self):
        self.checkAllNone1.setChecked(True) # as all DataSets are checked, we need the radiobutton All to be checked
        reload(sys.modules['Datasets_default'])
        from Datasets_default import DataSetsFilter
        self.DataSetTable = DataSetsFilter(self)
        self.menu.clear()
        self.ag = QActionGroup(self, exclusive=False)
        for item in self.DataSetTable:
            a = self.ag.addAction(QAction(item, self, checkable=True, checked=True))
            self.menu.addAction(a)
            self.connect(a, SIGNAL('triggered()'), self.QGBoxListsUpdate)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents() 
    
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
            self.rel_list_1 = sub_releases2(str(self.my_choice_rel_1), self.releasesList_rel_2)
        resume_text = self.texte
        resume_text += "<br />Release   : " + self.my_choice_rel_1
        resume_text += "<br />Reference : " + self.my_choice_ref_1
        self.QText_Resume.setText(self.trUtf8(resume_text))
        
    def Previous_Choice(self):
        print "Previous_Choice tmp: "
        if self.tasks_counter == 0:
            print "no way !, self.tasks_counter = 0"
        else:
            self.tasks_counter -= 1
            self.checkTaskCounter()

    def Next_Choice(self):
        print "Next_Choice tmp: "
        if self.tasks_counter == self.tasks_counterMax:
            print "no way !, self.tasks_counter = %d" % self.tasks_counterMax
        else:
            self.tasks_counter += 1
            self.checkTaskCounter()

    def checkTaskCounter(self):
        if self.tasks_counter == 0:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            self.bouton_Previous.setEnabled(False)
            self.bouton_Next.setEnabled(True)
            clearDataSets(self)
            self.labelCombo1.setText("Release ") # label used for resuming the rel/ref.
            self.QGBox_rel0.setTitle("Release list")
            self.QGBox_rel0.setVisible(True)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(False)
            for it in self.releasesList_0:
                item = QListWidgetItem("%s" % it)
                self.QLW_rel1.addItem(item)
        elif self.tasks_counter == 1:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(True)
            clearDataSets(self)
            self.labelCombo2.setText("Reference ") # label used for resuming the rel/ref.
            self.QGBox_rel0.setTitle("Reference list")
            self.QGBox_rel0.setVisible(True)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(False)
            for it in self.releasesList_0:
                item = QListWidgetItem("%s" % it)
                self.QLW_rel1.addItem(item)
        elif self.tasks_counter == 2:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            changeFastvsFullSize(self)
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(True)
            self.QGBox_rel0.setTitle("Lists")
            self.QGBox_rel0.setVisible(False) 
            self.QGBox_Lists.setVisible(True)
            self.QGBox_Selected.setVisible(False)
            self.QGBoxListsUpdate()
            self.selectedRelDatasets = ""
            self.selectedRefDatasets = ""
            self.selectedRelGlobalTag = ""
            self.selectedRefGlobalTag = ""
            self.selectedFvsFDatasets = ""
            self.selectedFvsFGlobalTag = ""
            # what to do if len(self.QLW_rel(f)_datasets) = 0? -> solved before arriving here !
        elif self.tasks_counter == 3:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(False)
            self.QGBox_rel0.setTitle("Selected")
            self.QGBox_rel0.setVisible(False)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(True)
            self.QGBoxListsUpdate()
            
            print BaseURL(self) # temporaire
            print_arrays(self) # temporaire
            
            selectedText = "<strong>Selected :</strong>"
            selectedText += "<table>"
            if ( checkFastvsFull(self) ): # FastvsFast
                selectedText += "<br /><br /><strong>Fast vs Fast : </strong>"
            selectedText += "<tr>"
            if (self.selectedRelDatasets == self.selectedRefDatasets):
                selectedText += "<td colspan=\"4\"><br /><strong><font color = \"green\">Datasets : " + self.selectedRelDatasets + "</font></strong><br /></td>"
            else: # need to extract common terms in blue and others in black (red?)
                selectedText += "<td colspan=\"4\"><br /><strong>Datasets : " + self.selectedRelDatasets + "</strong><br /></td>"
            selectedText += "</tr><tr><td><strong>GlobalTags : </td>" 
            selectedText += "<td>" + self.my_choice_rel_1 + "<br />" + self.selectedRelGlobalTag + "</td>" 
            selectedText += "<td>  </td>"
            selectedText += "<td>" + self.my_choice_ref_1 + "<br />" + self.selectedRefGlobalTag + "</strong></td>"           
            selectedText += "</tr>"
            
            if ( checkFastvsFull(self) ): # FastvsFull
                selectedText += "<br /><br /><strong>Fast vs Full : </strong>"
                selectedText += "<tr>"
                if (self.selectedRelDatasets == self.selectedFvsFDatasets):
                    selectedText += "<td colspan=\"4\"><br /><strong><font color = \"green\">Datasets : " + self.selectedRelDatasets + "</font></strong><br /></td>"
                else:
                    selectedText += "<td colspan=\"4\"><br /><strong>Selected Fast vs Full Datasets : " + self.selectedRelDatasets + "</strong><br /></td>"
                selectedText += "</tr><tr><td><strong>GlobalTags : </td>"
                selectedText += "<td>" + self.my_choice_rel_1 + "<br />" + self.selectedRelGlobalTag  + "</td>" 
                selectedText += "<td>  </td>"
                selectedText += "<td>" + self.my_choice_rel_1 + "<br />" + self.selectedFvsFGlobalTag + "</strong></td>"
                selectedText += "</tr>"
            selectedText += "</table>"
            self.labelResumeSelected.setText(self.trUtf8(selectedText))
            print "self.selectedRelDatasets : %s " % self.selectedRelDatasets # temporaire
            print "self.selectedRefDatasets : %s " % self.selectedRefDatasets # temporaire
            print "self.selectedRelGlobalTag : %s " % self.selectedRelGlobalTag # temporaire
            print "self.selectedRefGlobalTag : %s " % self.selectedRefGlobalTag # temporaire
            if ( checkFastvsFull(self) ): # FastvsFull
                print "self.selectedFvsFDatasets : %s " % self.selectedFvsFDatasets # temporaire
                print "self.selectedFvsFGlobalTag : %s " % self.selectedFvsFGlobalTag # temporaire
           
        else:
            "Hello Houston, we have a pbm !!"
        writeLabelCombo3(self)
        self.bouton_Previous.setText(self.trUtf8(self.tasks_list[self.tasks_counter-1]))
    
    def QGBoxListsUpdate(self):
        print "menu clicked !"
        print "*-*-**--*-*-*-*-*-* DataSets"
        if (self.my_choice_rel_0 != ''): # print the list of the releases
            for index in xrange(self.QLW_rel1.count()):
                print "self.QLW_rel1.item(%d) : %s" % ( index, self.QLW_rel1.item(index).text() )
        if (self.my_choice_ref_1 != ''): # this implies that all others my_choice_ref(l) have been chossen
            self.selectedDataSets = []
            print "self.validationType1 :", self.validationType1
            print "self.validationType2 :", self.validationType2
            print "self.validationType3 :", self.validationType3
            tt = self.ag.actions()
            self.allMenuListDatasetsChecked = False # default
            for it in tt:
                print "self.ag.actions()", it.text()
                if it.isChecked():
                    print "%s is checked" % it.text()
                    self.selectedDataSets.append(str(it.text()))
                    self.allMenuListDatasetsChecked = True # we need only one Dataset selected
                else:
                    print "%s is unchecked" % it.text()
            print "////// selectedDataSets : ", self.selectedDataSets
            print "////// allMenuListDatasetsChecked : ", self.allMenuListDatasetsChecked

            #if (self.checkAllNone1.isChecked() and self.allMenuListDatasetsChecked): # ALL and at least one selected
            if (self.allMenuListDatasetsChecked):
                (self.releasesList_rel_3, self.releasesList_rel_3b, self.releasesList_ref_3, self.releasesList_ref_3b) = list_search_5(self)
                # perhaps we can rewrite later as list_search_5(self) instead of (...) = list_search_5(self) 
                # as all the self.releasesList_re[l|f]_3[b] can be wrote in the list_search_5 function directly.

                #doing dataset display
                if ( self.releasesList_rel_3 == self.releasesList_ref_3 ):
                    print "HHHHHH : equal"
                else:
                    print "HHHHHH : NO EQUALITY"
                # to do : test between dataset extracted for release vs reference (green reference) after selection
                
                tempDataset = self.selectedDataSets
                tempDataset.sort()
                datasetList = self.selectedDataSets[0]
                for it in range(1, len(tempDataset)):
                    datasetList += ', ' + self.selectedDataSets[it]
                print datasetList # TEMPORAIRE

                clearDataSetsLists(self)
                print "nb of datasets  : ", len(self.releasesList_rel_3) # TEMPORAIRE
                print "nb of globaltags : ", len(self.releasesList_rel_3b) # TEMPORAIRE
                self.QTable_rel.setRowCount( len(self.releasesList_rel_3) )
                i_count = 0
                for it in self.releasesList_rel_3:
                    item = QTableWidgetItem("%s" % it)
                    if ( it == datasetList ):
                        item.setTextColor(QColor("blue"))
                    else:
                        item.setTextColor(QColor("black"))
                    self.QTable_rel.setItem(i_count, 0, item)
                    i_count += 1
                i_count = 0
                for it in self.releasesList_rel_3b:
                    item = QTableWidgetItem("%s" % it)
                    self.QTable_rel.setItem(i_count, 1, item)
                    i_count += 1
                self.connect(self.QTable_rel, SIGNAL("cellClicked(int, int)"),self.ItemSelectedTable_rel)
                
                print "nb of datasets  : ", len(self.releasesList_ref_3) # TEMPORAIRE
                print "nb of globaltags : ", len(self.releasesList_ref_3b) # TEMPORAIRE
                self.QTable_ref.setRowCount( len(self.releasesList_ref_3) )
                i_count = 0
                for it in self.releasesList_ref_3:
                    item = QTableWidgetItem("%s" % it)
                    if ( it == datasetList ):
                        item.setTextColor(QColor("blue"))
                    else:
                        item.setTextColor(QColor("black"))
                    self.QTable_ref.setItem(i_count, 0, item)
                    i_count += 1
                i_count = 0
                for it in self.releasesList_ref_3b:
                    item = QTableWidgetItem("%s" % it)
                    self.QTable_ref.setItem(i_count, 1, item)
                    i_count += 1
                self.connect(self.QTable_ref, SIGNAL("cellClicked(int, int)"),self.ItemSelectedTable_ref)
                
                #for it in self.releasesList_ref_3:
                if ( checkFastvsFull(self) ): # FastvsFull
                    print "nb of datasets  : ", len(self.releasesList_rel_4) # TEMPORAIRE
                    print "nb of globaltags : ", len(self.releasesList_rel_4b) # TEMPORAIRE
                    self.QTable_FastvsFull.setRowCount( len(self.releasesList_rel_4) )
                    i_count = 0
                    for it in self.releasesList_rel_4:
                        item = QTableWidgetItem("%s" % it)
                        if ( it == datasetList ):
                            item.setTextColor(QColor("blue"))
                        else:
                            item.setTextColor(QColor("black"))
                        self.QTable_FastvsFull.setItem(i_count, 0, item)
                        i_count += 1
                    i_count = 0
                    for it in self.releasesList_rel_4b:
                        item = QTableWidgetItem("%s" % it)
                        self.QTable_FastvsFull.setItem(i_count, 1, item)
                        i_count += 1
                    self.connect(self.QTable_FastvsFull, SIGNAL("cellClicked(int, int)"),self.ItemSelectedTable_FastvsFull)
                    
            else: # NONE & none checked, or ALL & none checked
                print "len of selectedDataSets = %d" % len(self.selectedDataSets)
                clearDataSetsLists(self)

    def ItemSelectedClicked5(self):
        print "Datasets Rel"
        self.selectedFvsFDatasets = self.QLW_FastvsFull_dataset.currentItem().text()
        print "ItemRelClicked5 : self.selectedFvsFDatasets : %s " % self.selectedFvsFDatasets
        
    def ItemSelectedClicked6(self):
        print "Datasets Ref"
        self.selectedFvsFGlobalTag = self.QLW_FastvsFull_dataset_list.currentItem().text()
        print "ItemRefClicked46 : self.selectedFvsFGlobalTag : %s " % self.selectedFvsFGlobalTag
        
    def ItemSelectedTable_rel(self, nRow, nCol):
        print "(%d, %d)" % (nRow, nCol)
        if (nCol): # nCol=1, True
            print self.QTable_rel.item(nRow, nCol-1).text()
            self.QTable_rel.item(nRow, nCol-1).setSelected(True)
            print self.QTable_rel.item(nRow, nCol).text()
            self.selectedRelDatasets = self.QTable_rel.item(nRow, nCol-1).text()
            self.selectedRelGlobalTag = self.QTable_rel.item(nRow, nCol).text()
        else : # nCol=0, False
            print self.QTable_rel.item(nRow, nCol).text()
            print self.QTable_rel.item(nRow, nCol+1).text()
            self.QTable_rel.item(nRow, nCol+1).setSelected(True)
            self.selectedRelDatasets = self.QTable_rel.item(nRow, nCol).text()
            self.selectedRelGlobalTag = self.QTable_rel.item(nRow, nCol+1).text()
        print "ItemSelectedTable_rel : self.selectedRelDatasets : %s " % self.selectedRelDatasets
        print "ItemSelectedTable_rel : self.selectedRelGlobalTag : %s " % self.selectedRelGlobalTag

    def ItemSelectedTable_ref(self, nRow, nCol):
        print "(%d, %d)" % (nRow, nCol)
        if (nCol): # nCol=1, True
            print self.QTable_ref.item(nRow, nCol-1).text()
            self.QTable_ref.item(nRow, nCol-1).setSelected(True)
            print self.QTable_ref.item(nRow, nCol).text()
            self.selectedRefDatasets = self.QTable_ref.item(nRow, nCol-1).text()
            self.selectedRefGlobalTag = self.QTable_ref.item(nRow, nCol).text()
        else : # nCol=0, False
            print self.QTable_ref.item(nRow, nCol).text()
            print self.QTable_ref.item(nRow, nCol+1).text()
            self.QTable_ref.item(nRow, nCol+1).setSelected(True)
            self.selectedRefDatasets = self.QTable_ref.item(nRow, nCol).text()
            self.selectedRefGlobalTag = self.QTable_ref.item(nRow, nCol+1).text()
        print "ItemSelectedTable_ref : self.selectedRefDatasets : %s " % self.selectedRefDatasets
        print "ItemSelectedTable_ref : self.selectedRefGlobalTag : %s " % self.selectedRefGlobalTag

    def ItemSelectedTable_FastvsFull(self, nRow, nCol):
        print "(%d, %d)" % (nRow, nCol)
        if (nCol): # nCol=1, True
            print self.QTable_FastvsFull.item(nRow, nCol-1).text()
            self.QTable_FastvsFull.item(nRow, nCol-1).setSelected(True)
            print self.QTable_FastvsFull.item(nRow, nCol).text()
            self.selectedRefDatasets = self.QTable_FastvsFull.item(nRow, nCol-1).text()
            self.selectedRefGlobalTag = self.QTable_FastvsFull.item(nRow, nCol).text()
        else : # nCol=0, False
            print self.QTable_FastvsFull.item(nRow, nCol).text()
            print self.QTable_FastvsFull.item(nRow, nCol+1).text()
            self.QTable_FastvsFull.item(nRow, nCol+1).setSelected(True)
            self.selectedFvsFDatasets = self.QTable_FastvsFull.item(nRow, nCol).text()
            self.selectedFvsFGlobalTag = self.QTable_FastvsFull.item(nRow, nCol+1).text()
        print "ItemSelectedTable_FastvsFull : self.selectedFvsFDatasets : %s " % self.selectedFvsFDatasets
        print "ItemSelectedTable_FastvsFull : self.selectedFvsFGlobalTag : %s " % self.selectedFvsFGlobalTag

