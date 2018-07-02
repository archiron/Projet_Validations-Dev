#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from Variables import *
from guiOptionsGp import initGpOptions
from guiChoiceGp import initGpChoice
from guiBottomGp import initGpBottom
from guiMiddleGp import initGpMiddle
from getEnv import env
from functions import folder_creation, finalFolder_creation, working_dirs_creation, dataSets_finalFolder_creation 
from functions import list_search_1, list_search_3 
from functions import folderExtension_creation 
from functions import sub_releases, sub_releases2, list_search_5 
from functions import checkFastvsFull, getCheckedOptions, getCheckedRadioButton
from functions import checkFileName, newName, updateLabelResumeSelected, updateLabelResume
from functions import changeRef2Tmp, changeTmp2Ref, set_finalFolder, check_finalFolder
from Datasets_default import DataSetsFilter, checkCalculValidation # extractDatasets, extractDatasetsFastvsFull, 
from Paths_default import *
from functionGui import clearDataSets, clearDataSetsLists, writeLabelCombo3, clearReleasesList
from functionGui import fillQLW_rel1, fillQLW_rel2_rel, fillQLW_rel2_ref 
from functionGui import enableRadioButtons, disableRadioButtons, disableStdDevButtons, enableStdDevButtons, disableLocationButtons, enableLocationButtons, comparisonRules
from networkFunctions import cmd_load_files
from electronCompare import initRoot
		
#############################################################################
class Gev(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        initVariables(self)
        self.wp.write("initVariables OK\n")
        self.textReport += "initVariables OK<br>"
        
        self.setWindowTitle(self.version) # Modification of the finalFolder setting. It is created at step 3 instead of step 4 and can prevent from overwritting files.
        # also add working_dirs prevent from step 1.
        
        # From top to bottom, there is 4 parts :
        # PART 1 : GroupBoxes for validation choice
        # PART 2 : Resume label for actions listing
        # PART 3 : GroupBoxes for Tag selection
        # BOTTOM PART : buttons
        # FINAL PART : keeping all previous part into one

        ## PART 1 - Options Grp ##
        initGpOptions(self)
        
        ## PART 2 ##
        initGpMiddle(self)
        
        ## BOTTOM PART ##
        initGpBottom(self)

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
        
        initRoot(self)

    def radio11Clicked(self):
        self.radio11.setChecked(True)
        self.validationType1 = 'Full'
        self.checkDataSets2Clicked()
        self.checkSpecTarget1_Clicked()
        self.my_choice_ref_1 = self.reference
        self.my_choice_rel_1 = self.target
        self.releasesList_ref_2 = self.referenceList
        self.ref_list_1  = self.refList
        tmp = "Reference : " + self.my_choice_ref_1
        self.labelCombo2.setText(tmp)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()

    def radio12Clicked(self):
        self.radio12.setChecked(True)
        self.validationType1 = 'Fast'
        self.checkDataSets2Clicked()
        self.checkSpecTarget1_Clicked()
        self.my_choice_ref_1 = self.reference
        self.my_choice_rel_1 = self.target
        self.releasesList_ref_2 = self.referenceList
        self.ref_list_1  = self.refList
        tmp = "Reference : " + self.my_choice_ref_1
        self.labelCombo2.setText(tmp)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
        
    def radio13Clicked(self):
        self.radio13.setChecked(True)
        self.validationType1 = 'FastFull'
        self.checkDataSets2Clicked()
        self.checkSpecTarget1_Clicked()
        changeRef2Tmp(self)

        self.my_choice_ref_0 = self.my_choice_rel_0 # need to see if we have to keep it
        print ("my_choice_rel_0 = ") , self.my_choice_rel_0 # temp
        print ("my_choice_rel_1 = ") , self.my_choice_rel_1 # temp
        print ("my_choice_ref_0 = ") , self.my_choice_ref_0 # temp
        print ("my_choice_ref_1 = ") , self.my_choice_ref_1 # temp
        for item in self.releasesList_ref_2: # temp
            self.wp.write("ItemRelRefClicked2 : %s\n" % item) # temp
            self.textReport += "ItemRelRefClicked2" + item + "<br>"
        self.wp.write("\n") # temp
        self.textReport += "<br>"
        for item in self.ref_list_1: # temp
            self.wp.write("ItemRelRefClicked2 : %s\n" % item) # temp
            self.textReport += "ItemRelRefClicked2" + item + "<br>"
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
        
    def checkSpecTarget1_Clicked(self):
        self.my_choice_ref_1 = self.reference
        self.my_choice_rel_1 = self.target
        self.checkSpecTarget1.setChecked(True)
        self.checkSpecReference1_Clicked()
        self.validationType2 = 'RECO'
        getCheckedOptions(self)
        comparisonRules(self)
        print "Target, self.validationType2 : %s" % self.validationType2
        print "Target, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents()

    def checkSpecTarget2_Clicked(self):
        self.checkSpecTarget2.setChecked(True)
        self.checkSpecReference2_Clicked() #default
        self.validationType2 = 'PU25'
        getCheckedOptions(self)
        comparisonRules(self)
        print "Target, self.validationType2 : %s" % self.validationType2
        print "Target, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents()
        
    def checkSpecTarget3_Clicked(self):
        self.checkSpecTarget3.setChecked(True)
        self.checkSpecReference2_Clicked()
        self.validationType2 = 'PUpmx25'
        getCheckedOptions(self)
        comparisonRules(self)
        print "Target, self.validationType2 : %s" % self.validationType2
        print "Target, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents()
                        
    def checkSpecTarget4_Clicked(self):
        self.checkSpecTarget4.setChecked(True)
        self.validationType2 = 'miniAOD'
        self.checkSpecReference4_Clicked()
        getCheckedOptions(self)
        comparisonRules(self)
        print "Target, self.validationType2 : %s" % self.validationType2
        print "Target, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents()
                        
    def checkAllNone1Clicked(self):
        if self.checkAllNone1.isChecked():
        # ALL : reload the default
#            print "All"
            self.menu.clear()
            self.ag = QActionGroup(self, exclusive=False)
            for item in self.DataSetTable:
                (item_name, item_checked) = item
                a = self.ag.addAction(QAction(item_name, self, checkable=True, checked=item_checked)) # checked=True
                self.menu.addAction(a)
                self.connect(a, SIGNAL('triggered()'), self.QGBoxListsUpdate)
            self.QGBoxListsUpdate() # needed ?
        QtCore.QCoreApplication.processEvents() 

    def checkAllNone2Clicked(self):
        if self.checkAllNone2.isChecked():
        # NONE : uncheck all
#            print "None"
            self.menu.clear()
            self.ag = QActionGroup(self, exclusive=False)
            for item in self.DataSetTable:
                (item_name, item_checked) = item
                a = self.ag.addAction(QAction(item_name, self, checkable=True, checked=False))
                self.menu.addAction(a)
                self.connect(a, SIGNAL('triggered()'), self.QGBoxListsUpdate)
            self.QGBoxListsUpdate() # needed ?
        QtCore.QCoreApplication.processEvents() 

    def checkStdDev1_Clicked(self):
#        print "std"
        QtCore.QCoreApplication.processEvents() 

    def checkStdDev2_Clicked(self):
#        print "dev"
        QtCore.QCoreApplication.processEvents() 

    def checkSpecReference1_Clicked(self):
        self.checkSpecReference1.setChecked(True)
        self.validationType3 = 'RECO'
        getCheckedOptions(self)
        if ( self.checkSpecTarget1.isChecked() ): # RECO vs RECO. If not checked, there must have a pbm !
            if ( self.radio13.isChecked() ): # Fast vs Full
                changeRef2Tmp(self)
            else: # Full vs Full or Fast vs Fast
                changeTmp2Ref(self)
        print "----- Reference, self.validationType2 : %s" % self.validationType2
        print "----- Reference, self.validationType3 : %s" % self.validationType3
        print "----- Reference rel : " + self.my_choice_rel_1
        print "----- Reference ref : " + self.my_choice_ref_1
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkSpecReference2_Clicked(self):
        self.checkSpecReference2.setChecked(True)
        self.validationType3 = 'PU25'
        getCheckedOptions(self)
        if ( self.checkSpecTarget2.isChecked() ): # PU25 vs PU25
            if ( self.radio13.isChecked() ): # Fast vs full same release
                changeRef2Tmp(self)
            else: # Full vs Full or Fast vs Fast
                changeTmp2Ref(self)
        elif ( self.checkSpecTarget3.isChecked() ): # PUpmx25 vs PUpmx25
            changeRef2Tmp(self)
        print "Reference, self.validationType2 : %s" % self.validationType2
        print "Reference, self.validationType3 : %s" % self.validationType3
        print "Reference rel : " + self.my_choice_rel_1
        print "Reference ref : " + self.my_choice_ref_1
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkSpecReference3_Clicked(self):
        self.checkSpecReference3.setChecked(True)
        self.validationType3 = 'PUpmx25'
        getCheckedOptions(self)
        if ( self.checkSpecTarget3.isChecked() ): # PUpmx25 vs PUpmx25
            if ( self.radio13.isChecked() ): # Fast vs full same release
                changeRef2Tmp(self)
            else: # Full vs Full or Fast vs Fast
                changeTmp2Ref(self)
        print "Reference, self.validationType2 : %s" % self.validationType2
        print "Reference, self.validationType3 : %s" % self.validationType3
        print "Reference rel : " + self.my_choice_rel_1
        print "Reference ref : " + self.my_choice_ref_1
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkSpecReference4_Clicked(self):
        self.checkSpecReference4.setChecked(True)
        self.validationType3 = 'miniAOD'
        getCheckedOptions(self)
        if ( self.checkSpecTarget1.isChecked() ): # RECO vs miniAOD same release
            changeRef2Tmp(self)
        elif ( self.checkSpecTarget4.isChecked() ): # miniAOD vs miniAOD
            if ( self.radio13.isChecked() ): # Fast vs full same release
                changeRef2Tmp(self)
            else: # Full vs Full or Fast vs Fast
                changeTmp2Ref(self)
        print "Reference, self.validationType2 : %s" % self.validationType2
        print "Reference, self.validationType3 : %s" % self.validationType3
        print "Reference rel : " + self.my_choice_rel_1
        print "Reference ref : " + self.my_choice_ref_1
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkDataSets2Clicked(self):
        self.wp.write("checkDataSets2Clicked")
        self.textReport += "checkDataSets2Clicked" + "<br>"
        self.checkAllNone1.setChecked(True) # as all DataSets are checked, we need the radiobutton All to be checked
        from Datasets_default import DataSetsFilter
        self.DataSetTable = DataSetsFilter(self)
        reload(sys.modules['Datasets_default'])
        self.menu.clear()
        self.ag = QActionGroup(self, exclusive=False)
        for item in self.DataSetTable:
            (item_name, item_checked) = item
            self.wp.write(item_name + "\n")
            self.textReport += "checkLocation2Clicked" + item_name + "<br>"
            a = self.ag.addAction(QAction(item_name, self, checkable=True, checked=item_checked)) # checked=True
            self.menu.addAction(a)
            self.connect(a, SIGNAL('triggered()'), self.QGBoxListsUpdate)
        #self.setFixedSize(1200, 700)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents() 
    
    def checkLocation2Clicked(self):
        print "checkLocation2Clicked"
        self.wp.write("checkLocation2Clicked")
        self.textReport += "checkLocation2Clicked" + "<br>"
        from Paths_default import LocationFilter
        self.LocationTable = LocationFilter(self)
        reload(sys.modules['Paths_default'])
        self.menu_loc.clear()
        self.loc = QActionGroup(self, exclusive=True)
        for item in self.LocationTable:
            (item_name, item_checked, item_location) = item
            self.wp.write(item_name + "\n")
            a2 = self.loc.addAction(QAction(item_name, self, checkable=True, checked=item_checked)) # checked=True
            self.menu_loc.addAction(a2)
            self.connect(a2, SIGNAL('triggered()'), self.PathUpdate)
        self.PathUpdate()
        QtCore.QCoreApplication.processEvents() 

    def ItemRelRefClicked1(self):
        self.QGBox_rel2.setTitle(self.QLW_rel1.currentItem().text())        
        self.QLW_rel2.clear()
        if self.QGBox_rel0.title() == "Reference list":
            print "reference"
            if (checkFastvsFull(self)):
                self.my_choice_ref_0 = self.my_choice_rel_0
                self.releasesList_ref_1 = self.releasesList_rel_1 # pas la peine de recalculer
                self.ref_list_0 = self.rel_list_0 # pas la peine de recalculer
                for item in self.releasesList_ref_1: # temp
                    self.wp.write("ItemRelRefClicked1 : %s\n" % item)
                    self.textReport += "ItemRelRefClicked1 : " + item + "<br>"
                self.wp.write("\n")
                self.textReport += "<br>"
                for item in self.ref_list_0:
                    self.wp.write("ItemRelRefClicked1 : %s\n" % item)
                    self.textReport += "ItemRelRefClicked1 : " + item + "<br>"
            else:
                self.my_choice_ref_0 = self.QLW_rel1.currentItem().text()
                self.releasesList_ref_1 = list_search_1(self.my_choice_ref_0)
                self.ref_list_0 = sub_releases(self.releasesList_ref_1) #list_search_1(self.my_choice_ref_0))
            print "ItemRefClicked1 : self.my_choice_ref_0 : %s " % self.my_choice_ref_0
            fillQLW_rel2_ref(self)
        else:
            print "release"
            self.my_choice_rel_0 = self.QLW_rel1.currentItem().text()
            print "ItemRelRefClicked1 : self.my_choice_rel_0 : %s " % self.my_choice_rel_0
            self.releasesList_rel_1 = list_search_1(self.my_choice_rel_0)
            self.rel_list_0 = sub_releases(self.releasesList_rel_1) #list_search_1(self.my_choice_rel_0))
            # tester si =0 
            #for it in self.rel_list_0:
            #    item = QListWidgetItem("%s" % it)
            #    self.QLW_rel2.addItem(item)
            fillQLW_rel2_rel(self)
            
    def ItemRelRefClicked2(self):
        #rel_text = self.QLW_rel2.currentItem().text() + " DataSets"
        #if self.QGBox_rel0.title() == "Reference list":
        if ( self.tasks_counter == 1 ):
            print "reference" + str(self.tasks_counter)
            self.ref_list_1 = sub_releases2(str(self.my_choice_ref_1), self.releasesList_ref_2)
            self.my_choice_ref_1 = self.QLW_rel2.currentItem().text()
            self.reference = self.my_choice_ref_1
            self.releasesList_ref_2 = list_search_3(self.releasesList_ref_1, str(self.my_choice_ref_1))
            self.referenceList = self.releasesList_ref_2
            self.ref_list_1 = sub_releases2(str(self.my_choice_ref_1), self.releasesList_ref_2)
            self.refList = self.rel_list_1            
            print "ItemRefClicked2 : self.my_choice_ref_1 : %s " % self.my_choice_ref_1
            tmp = "Reference : " + self.my_choice_ref_1
            self.labelCombo2.setText(tmp)
        else: # self.tasks_counter == 0
            print "release" + str(self.tasks_counter)
            self.my_choice_rel_1 = self.QLW_rel2.currentItem().text()
            self.target = self.my_choice_rel_1
            print "ItemRelRefClicked2 : self.my_choice_rel_1 : %s " % self.my_choice_rel_1
            tmp = "Release : " + self.my_choice_rel_1
            self.labelCombo1.setText(tmp)
            self.releasesList_rel_2 = list_search_3(self.releasesList_rel_1, str(self.my_choice_rel_1))
            self.rel_list_1 = sub_releases2(str(self.my_choice_rel_1), self.releasesList_rel_2)
        updateLabelResume(self)
        
    def Previous_Choice(self):
        print "Previous_Choice tmp: "
        if self.tasks_counter == 0:
            print "no way !, self.tasks_counter = 0"
        else:
            self.tasks_counter -= 1
            self.checkTaskCounter()
        print self.tasks_counter
        
    def Next_Choice(self):
        print "Next_Choice tmp: "
        if self.tasks_counter > self.tasks_counterMax:
            print "no way !, self.tasks_counter = %d" % self.tasks_counterMax
        else:
            self.tasks_counter += 1
            self.checkTaskCounter()
        print self.tasks_counter
        
    def checkTaskCounter(self):
        import re#, os
        writeLabelCombo3(self)
        self.bouton_Previous.setText(self.trUtf8(self.tasks_list[self.tasks_counter-1]))
        
        if self.tasks_counter == 0: # release selection
#            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
#            print "check tasks counter : %s" % self.tasks_list[self.tasks_counter]
#            print "check tasks counter next : %s" % self.tasks_list[self.tasks_counter+1]
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            self.wp.write("release selection")
            self.textReport += 'self.tasks_counter = ' + str(self.tasks_counter) + '/' + str(self.tasks_counterMax) + '<br>'
            self.textReport += '<b><font color=\'blue\'> release selection </font></b>' + '<br>'
            self.bouton_Previous.setEnabled(False)
            self.bouton_Next.setEnabled(True)
            clearDataSets(self)
            self.labelCombo1.setText("Release ") # label used for resuming the rel/ref.
            self.QGBox_rel0.setTitle("Release list")
            self.QGBox_rel2.setTitle("Release")
            self.QGBox_rel0.setVisible(True)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(False)
            #for it in self.releasesList_0:
            #    item = QListWidgetItem("%s" % it)
            #    self.QLW_rel1.addItem(item)
            disableRadioButtons(self)
            disableStdDevButtons(self)
            disableLocationButtons(self)
            fillQLW_rel1(self)
        elif self.tasks_counter == 1: # reference selection
#            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
#            print "check tasks counter : %s" % self.tasks_list[self.tasks_counter]
#            print "check tasks counter next : %s" % self.tasks_list[self.tasks_counter+1]
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            self.wp.write("reference selection")
            self.textReport += 'self.tasks_counter = ' + str(self.tasks_counter) + '/' + str(self.tasks_counterMax) + '<br>'
            self.textReport += '<b><font color=\'blue\'> reference selection </font></b>' + '<br>'
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(True)
            clearDataSets(self)
            self.labelCombo2.setText("Reference ") # label used for resuming the rel/ref.
            self.QGBox_rel0.setTitle("Reference list")
            self.QGBox_rel2.setTitle("Release")
            self.QGBox_rel0.setVisible(True)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(False)
            #for it in self.releasesList_0:
            #    item = QListWidgetItem("%s" % it)
            #    self.QLW_rel1.addItem(item)
            disableRadioButtons(self)
            disableStdDevButtons(self)
            disableLocationButtons(self)
            fillQLW_rel1(self)
        elif self.tasks_counter == 2: # GlobalTag selections
#            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
#            print "check tasks counter : %s" % self.tasks_list[self.tasks_counter]
#            print "check tasks counter next : %s" % self.tasks_list[self.tasks_counter+1]
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            self.wp.write("GlobalTag selections")
            self.textReport += "self.tasks_counter = " + str(self.tasks_counter) + "/" + str(self.tasks_counterMax) + "<br>"
            self.textReport += "GlobalTag selections" + "<br>"
            updateLabelResume(self)
            enableRadioButtons(self)
            comparisonRules(self)
            disableStdDevButtons(self)
            self.lineEdit_ref.setEnabled(False)
            self.lineEdit_rel.setEnabled(False)
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
        elif self.tasks_counter == 3: # resuming selections
#            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
#            print "check tasks counter : %s" % self.tasks_list[self.tasks_counter]
#            print "check tasks counter next : %s" % self.tasks_list[self.tasks_counter+1]
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            self.wp.write("resuming selections")
            self.textReport += "self.tasks_counter = " + str(self.tasks_counter) + "/" + str(self.tasks_counterMax) + "<br>"
            self.textReport += "resuming selections" + "<br>"
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(True)
            self.QGBox_rel0.setTitle("Selected")
            self.QGBox_rel0.setVisible(False)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setTitle("Selected")
            self.QGBox_Selected.setVisible(True)
            disableRadioButtons(self)
            enableStdDevButtons(self)
            enableLocationButtons(self)
            self.lineEdit_ref.setEnabled(True)
            self.lineEdit_rel.setEnabled(True)
            clearReleasesList(self)
            self.PathUpdate()
            #check_finalFolder(self)
            updateLabelResume(self)
            self.QGBoxListsUpdate()
            updateLabelResumeSelected(self) # perhaps need to be redone
            
            print "checkTaskCounter 3 : self.selectedDataSets = %s" % self.selectedDataSets
            print "checkTaskCounter 3 : self.okToPublishDatasets = %s" % self.okToPublishDatasets
            #print "checkTaskCounter 3 : self.okToDisplayDatasets = %s" % self.okToDisplayDatasets
            
            ## here we have a common (rel & ref) dataset named as self.okToPublishDatasets for Full vs Full or Fast vs Fast. 
            ## we also have a common dataset for Fast vs Full named as self.okToPublishFvsFDatasets -> no more used
            ## WARNING : we need to have self.okToPublishFvsFDatasets = self.okToPublishDatasets !! ##
            
            # create list of root files for rel & ref
            print "checkTaskCounter 3 : 0 " + self.selectedRelDatasets
            print "checkTaskCounter 3 : 1 " + self.okToPublishDatasets
            self.releasesList_3 = (self.okToPublishDatasets.replace(" ", "")).split(',') # replace releasesList_rel_3 & releasesList_ref_3
            #self.releasesList_3 = (self.selectedDataSets.replace(" ", "")).split(',') # replace releasesList_rel_3 & releasesList_ref_3
            print "\nRelease :"
            for it1 in self.releasesList_rel_2: # it1 = root file
                #print "checkTaskCounter 3 : %s" % it1
                if checkFileName(self, it1, "rel"):
                    for it2 in self.releasesList_3: # it2 = dataSet
                        if (re.search(str(newName("__RelVal", it2, "__")), it1) and re.search(str(self.selectedRelGlobalTag), it1)): # at least one file here
                             print "checkTaskCounter 3 : %s" % it1
                             if checkCalculValidation(self, it1, "rel"):
                                print it2 + " : " + it1 + " : OK"
                                self.releasesList_rel_5.append(it1)
            # perhaps add a test to verify if there is at least one file and if not, remove the dataSet.
            print "\nReference :"
            for it1 in self.releasesList_ref_2: # it1 = root file
               #print "checkTaskCounter 3 : %s" % it1
               if checkFileName(self, it1, "ref"):
                    for it2 in self.releasesList_3: # it2 = dataSet
                        if (re.search(str(newName("__RelVal", it2, "__")), it1) and re.search(str(self.selectedRefGlobalTag), it1)):
                            print "checkTaskCounter 3 : %s" % it1
                            if checkCalculValidation(self, it1, "ref"):
                                print it2 + " : " + it1 + " : OK"
                                self.releasesList_ref_5.append(it1)
            
            # print the used GlobalTags
            print "checkTaskCounter 3 : self.selectedRelGlobalTag = %s" % self.selectedRelGlobalTag
            print "checkTaskCounter 3 : self.selectedRefGlobalTag = %s" % self.selectedRefGlobalTag
            
            # print length of the arrays
            print "self.releasesList_rel_3 : %d\n" % len(self.releasesList_rel_3) # to be deleted
            print "self.releasesList_ref_3 : %d\n" % len(self.releasesList_ref_3) # to be deleted
            print "self.releasesList_3 : %d\n" % len(self.releasesList_3)
            print "self.releasesList_rel_2 : %d\n" % len(self.releasesList_rel_2)
            print "self.releasesList_ref_2 : %d\n" % len(self.releasesList_ref_2)
            print "self.releasesList_rel_5 : %d\n" % len(self.releasesList_rel_5)
            print "self.releasesList_ref_5 : %d\n" % len(self.releasesList_ref_5)
            #print BaseURL(self) # temporaire
            self.wp.write("BaseUrl = %s\n" % BaseURL(self))
            self.textReport += "BaseUrl = " + BaseURL(self) + "<br>"
          
        elif self.tasks_counter == 4: # folder creation & file loading
#            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
#            print "check tasks counter : %s" % self.tasks_list[self.tasks_counter]
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            self.wp.write("foldercreation & file loading")
            self.textReport += "self.tasks_counter = " + str(self.tasks_counter) + "/" + str(self.tasks_counterMax) + "<br>"
            self.textReport += "<b><font color=\'blue\'>foldercreation & file loading</font></b>" + "<br>"
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(False)
            self.QGBox_Selected.setTitle("Web page")
            self.QGBox_rel0.setVisible(False)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(True)
            os.chdir(self.working_dir_base) # going to base folder
            self.labelResumeSelected.clear() # 
            disableRadioButtons(self)
            disableStdDevButtons(self)
            disableLocationButtons(self)
            self.lineEdit_ref.setEnabled(False)
            self.lineEdit_rel.setEnabled(False)
            selectedText = ""
            
            # collapsing self.releasesList_rel_5, self.releasesList_ref_5 & self.okToPublishDatasets into one list.
            merged_1 = []
            for dts in self.okToPublishDatasets.split(','):
                print dts
                merged_1.append(str(dts))
            #print merged_1
            print "***** self.FinalList *****"
            merged_1 = sorted(set(merged_1), reverse=True)
            #print merged_1
            #print "-----"
            #merged_1b = list(reversed(merged_1)) # merged_1[::-1]
            merged_1b = list(merged_1) # merged_1[::-1]
            #print merged_1b
            
            #####
            tmp_rel = []
            tmp_ref = []
            for it in merged_1b:
                #print "merged_1b : %s" % it
                for val in self.releasesList_rel_5:
                    if ( re.search(str(it + "__"), val) ):
                        #print "OK %s" % val
                        tmp_rel.append(val)
                    #else:
                    #    print "KO %s" % val
                for val in self.releasesList_ref_5:
                    if ( re.search(str(it + "__"), val) ):
                        #print "OK %s" % val
                        tmp_ref.append(val)
                    #else:
                    #    print "KO %s" % val
            #####
            #print "tmp_rel : ", tmp_rel
            #print "tmp_ref : ", tmp_ref
            self.finalList = map(list, zip(merged_1b, tmp_rel, tmp_ref))
            #print "-----"
            #print self.finalList[0][1]
            print self.finalList
            print "***** self.FinalList *****"

            # defining/creating paths & folders
            self.PathUpdate()
            # call for folders creation
            working_dirs_creation(self) # create folders for root files. MUST BE before folder_creation()
            folder_creation(self) # create local folder for files loading and operation resuming
            finalFolder_creation(self) # create the save folder for html and gifs files
            updateLabelResume(self)
            self.QGBoxListsUpdate()
            # loading files
            selectedText += "begin files loading ! <br>"
            print "begin files loading !"
            self.wp.write("begin files loading !\n")
            self.textReport += "begin files loading !" + "<br>"

            #cmd_load_files(self) # no test if the folders are created. We have an error output in PathUpdate() if the was a pbm with the folder creation.
            self.cmd_load_files_2()
            # do something with self.labelResumeSelected.setText(self.trUtf8(selectedText))
            selectedText += "All files loaded <br>"
            self.labelResumeSelected.setText(self.trUtf8(selectedText))
            QtCore.QCoreApplication.processEvents() 
            
            #TEMPORAIRE display list of root files
            print "releasesList_rel_5"
            for line in self.releasesList_rel_5:
                print line

            print "releasesList_ref_5"
            for line in self.releasesList_ref_5:
                print line
                
            # creating the datasets folders
            dataSets_finalFolder_creation(self)
            
            # do something with self.labelResumeSelected.setText(self.trUtf8(selectedText))
            
            print "fin ..."
            
        else:
            print "Hello Houston, we have a pbm !!"

    def PathUpdate(self): # get paths & create folders
        print "PathUpdate menu clicked !"
        print "*-*-**--*-*-*-*-*-* Location"
        self.wp.write("PathUpdate\n")
        self.textReport += "PathUpdate" + "<br>"
        os.chdir(self.working_dir_base) # going into base dir
        self.LocationTable = LocationFilter(self)
        tt = self.loc.actions()
        i_loc = 0
        # perhaps add a check on tasks_counter value
        for it in tt:
            print "self.ag.actions()", it.text()
            if it.isChecked():
                print "%s is checked" % it.text()
                self.wp.write("%s is checked\n" % it.text())
                self.textReport += it.text() + " is checked" + "<br>"
                print "folder path : %s" % self.LocationTable[i_loc][2]
                self.wp.write("folder path : %s\n" % self.LocationTable[i_loc][2])
                self.textReport += "folder path : " + self.LocationTable[i_loc][2] + "<br>"
                if ( self.my_choice_rel_1[6:] == '' ):
                    print "Can not create finalFolder ! "
                    BoiteMessage = QMessageBox()
                    BoiteMessage.setText("cannot create finalFolder !!")
                    self.wp.write("cannot create finalFolder !!")
                    self.textReport += "cannot create finalFolder !!" + "<br>"
                    BoiteMessage.setIcon(QMessageBox.Critical)
                    BoiteMessage.setWindowTitle("WARNING !")
                    BoiteMessage.exec_()
                else:
                    set_finalFolder(self, i_loc)
                    #self.finalFolder = self.LocationTable[i_loc][2] + "/" + self.my_choice_rel_1[6:] + self.temp_rl + '_xxx' + folderExtension_creation(self) # _xxx is temp. must be only _DQM_std/_DMQ_dev.
                    #self.finalFolder += '/' + getCheckedRadioButton(self) + '_'
                    #self.finalFolder += str(self.my_choice_ref_1[6:]) + self.temp_rf #+ '_xxx' + folderExtension_creation(self) # _xxx is temp. must be only _DQM_std/_DMQ_dev.
                    #self.wp.write("self.finalFolder : %s\n" % self.finalFolder)
                    #self.textReport += "self.finalFolder : " + self.finalFolder + "<br>"
                    self.wp.write("self.working_dir_base : %s\n" % self.working_dir_base)
                    self.textReport += "self.working_dir_base : " + self.working_dir_base + "<br>"
                    self.wp.write("self.finalFolder reference : %s\n" % self.finalFolder)
                    self.wp.write("set_finalFolder : %s\n" % set_finalFolder(self, i_loc))
                    #print("set_finalFolder() : %s\n" % set_finalFolder(self, i_loc))
                    #print("set_finalFolder() : %s\n" % self.finalFolder)
                    
                    # call for folders creation
                    #working_dirs_creation(self) # create folders for root files. MUST BE before folder_creation()
                    #folder_creation(self) # create local folder for files loading and operation resuming
                    #finalFolder_creation(self) # create the save folder for html and gifs files
                    #updateLabelResume(self)
            else:
                print "%s is unchecked" % it.text()
                self.wp.write("%s is unchecked\n" % it.text())
                self.textReport += it.text() + " is unchecked\n" + "<br>"
            i_loc += 1
            
    def QGBoxListsUpdate(self):
        print "QGBoxListsUpdate"
        getCheckedOptions(self)
        
#        if (self.my_choice_rel_0 != ''): # print the list of the releases
#            for index in xrange(self.QLW_rel1.count()):
#                print "QGBoxListsUpdate : self.QLW_rel1.item(%d) : %s" % ( index, self.QLW_rel1.item(index).text() )
        if (self.my_choice_ref_1 != ''): # this implies that all others my_choice_ref(l) have been chosen
            self.selectedDataSets = []
            print "QGBoxListsUpdate : self.validationType1 :", self.validationType1
            print "QGBoxListsUpdate : self.validationType2 :", self.validationType2
            print "QGBoxListsUpdate : self.validationType3 :", self.validationType3
            tt = self.ag.actions()
            self.allMenuListDatasetsChecked = False # default
            for it in tt:
                print "QGBoxListsUpdate : self.ag.actions()", it.text()
                if it.isChecked():
                    #print "QGBoxListsUpdate : %s is checked" % it.text()
                    self.selectedDataSets.append(str(it.text()))
                    self.allMenuListDatasetsChecked = True # we need only one Dataset selected
                #else:
                    #print "QGBoxListsUpdate : %s is unchecked" % it.text()
            print "QGBoxListsUpdate : selectedDataSets : ", self.selectedDataSets
            print "QGBoxListsUpdate : allMenuListDatasetsChecked : ", self.allMenuListDatasetsChecked

            #if (self.checkAllNone1.isChecked() and self.allMenuListDatasetsChecked): # ALL and at least one selected
            if (self.allMenuListDatasetsChecked):
                (self.releasesList_rel_3, self.releasesList_rel_3b, self.releasesList_ref_3, self.releasesList_ref_3b) = list_search_5(self)
                # perhaps we can rewrite later as list_search_5(self) instead of (...) = list_search_5(self) 
                # as all the self.releasesList_re[l|f]_3[b] can be wrote in the list_search_5 function directly.

                #doing dataset display                
                tempDataset = self.selectedDataSets
                tempDataset.sort()
                datasetList = self.selectedDataSets[0]
                for it in range(1, len(tempDataset)):
                    datasetList += ', ' + self.selectedDataSets[it]
                print "QGBoxListsUpdate : datasetList = " + datasetList # TEMPORAIRE

                #clearDataSets(self)
                clearDataSetsLists(self) # empty the tables
                print "QGBoxListsUpdate : nb of datasets rel   : ", len(self.releasesList_rel_3) # TEMPORAIRE
                print "QGBoxListsUpdate : nb of globaltags rel : ", len(self.releasesList_rel_3b) # TEMPORAIRE
                print "QGBoxListsUpdate : self.releasesList_rel_3  : " + str(self.releasesList_rel_3)
                print "QGBoxListsUpdate : self.releasesList_rel_3b : " + str(self.releasesList_rel_3b)
                print "QGBoxListsUpdate : self.releasesList_ref_3  : " + str(self.releasesList_ref_3)
                print "QGBoxListsUpdate : self.releasesList_ref_3b : " + str(self.releasesList_ref_3b)
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
                
                print "QGBoxListsUpdate : nb of datasets ref   : ", len(self.releasesList_ref_3) # TEMPORAIRE
                print "QGBoxListsUpdate : nb of globaltags ref : ", len(self.releasesList_ref_3b) # TEMPORAIRE
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
                                    
            else: # NONE & none checked, or ALL & none checked
                print "QGBoxListsUpdate : len of selectedDataSets = %d" % len(self.selectedDataSets)
                #clearDataSets(self)
                clearDataSetsLists(self)

        QtCore.QCoreApplication.processEvents() 
        print "QGBoxListsUpdate end OK"
        
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
        print "ItemSelectedTable_rel : self.selectedRelDatasets : %s - %s " % (self.selectedRelDatasets, self.QTable_rel.item(nRow, nCol).text())
        print "ItemSelectedTable_rel : self.selectedRelGlobalTag : %s " % self.selectedRelGlobalTag
        self.wp.write("ItemSelectedTable_rel : self.selectedRelDatasets : %s\n " % self.selectedRelDatasets)
        self.wp.write("ItemSelectedTable_rel : self.selectedRelGlobalTag : %s\n " % self.selectedRelGlobalTag)
        self.textReport += "ItemSelectedTable_rel : self.selectedRelDatasets : " + self.selectedRelDatasets + "<br>"
        self.textReport += "ItemSelectedTable_rel : self.selectedRelGlobalTag : " + self.selectedRelGlobalTag + "<br>"

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
        self.wp.write("ItemSelectedTable_ref : self.selectedRefDatasets : %s\n " % self.selectedRefDatasets)
        self.wp.write("ItemSelectedTable_ref : self.selectedRefGlobalTag : %s\n " % self.selectedRefGlobalTag)
        self.textReport += "ItemSelectedTable_ref : self.selectedRefDatasets : " + self.selectedRefDatasets + "<br>"
        self.textReport += "ItemSelectedTable_ref : self.selectedRefGlobalTag : " + self.selectedRefGlobalTag + "<br>"

    def showAbout(self):
        print("About")
        
        pixmap2 = QPixmap('/afs/cern.ch/user/a/archiron/lbin/Projet_Validations-Dev/Img/GUI_001.bmp')
        dialog = QDialog()
        layout = QVBoxLayout(dialog)
        labell = QLabel()
        labell.setText(self.version)
        label3 = QLabel()
        label3.setText('<br>All dev made by A. CHIRON<br>Laboratoire Leprince-Ringuet<br>')
        label2 = QLabel()
        label2.setPixmap(pixmap2)
        label4 = QLabel()
        label4.setText('<br>Special thanks to <font color=\'blue\'>Emilia</font> and <font color=\'blue\'>Jean-Baptiste</font> for their help<br>')
        layout.addWidget(labell)
        layout.addWidget(label3)
        layout.addWidget(label2)
        layout.addWidget(label4)
        label2.show()
        dialog.exec_()
    
    def showHelp(self):
        print("Help")
        
        #dialogHelp = QDialog()
        #layoutHelp = QVBoxLayout(dialogHelp)
        #labellHelp = QLabel()
        #labellHelp.setText(self.version)
        #label2Help = QLabel()
        #label2Help.setText('\n')
        #label3Help = QLabel()
        #wikiText = '<a href=\"https://twiki.cern.ch/twiki/bin/view/Main/ElectronValidationGUIHelpPage#Step_' + str(self.tasks_counter + 1) + '\">Step_' + str(self.tasks_counter + 1) + '</a>'
        #print(wikiText)
        #label3Help.setText('<a href=\"https://twiki.cern.ch/twiki/bin/view/Main/ElectronValidationGUIHelpPage#Step_1\">Step 1</a>')
        #label3Help.setText(wikiText)
        #label3Help.setOpenExternalLinks(True)
        link = 'https://twiki.cern.ch/twiki/bin/view/Main/ElectronValidationGUIHelpPage#Step_' + str(self.tasks_counter + 1)
        QDesktopServices.openUrl(QUrl(link))

    def showResume(self):
        print "showResume"
        dialogR = QDialog()
        layoutR = QVBoxLayout(dialogR)
        text = '<b>List of operations</b><br>'
        text += '<br>'
        text += self.textReport
        
        self.QTextR = QTextEdit()
        self.QTextR.setReadOnly(True)
        self.QTextR.setHtml(text)

        layoutR.addWidget(self.QTextR)
        dialogR.exec_()

    def changeText(self):
        self.temp_rl = ''
        if ( self.lineEdit_rel.text() != '' ):
            self.temp_rl = '_' + unicode(self.lineEdit_rel.text())
        self.temp_rf = ''
        if ( self.lineEdit_ref.text() != '' ):
            self.temp_rf = '_' + unicode(self.lineEdit_ref.text())       
        print "temp_rl : %s" % self.temp_rl
        print "temp_rf : %s" % self.temp_rf
        self.PathUpdate()
        updateLabelResume(self)
    
    def cmd_load_files_2(self):
        import re
        import sys
        import os
        from functions import clean_collections2
        from networkFunctions import cmd_fetch_2
        
        print "cmd_load_files 2"
        self.wp.write("cmd_load_files 2 : \n")
   
#    print "cmd_load_files : self.validationType1 = ",  self.validationType1 # temp
#    print "cmd_load_files : self.validationType2 = ",  self.validationType2 # temp
#    print "cmd_load_files : self.validationType3 = ",  self.validationType3 # temp
        validationType_2 = self.validationType2
        validationType_3 = self.validationType3
        temp_toBeRemoved = []

    ## Define options
        option_is_from_data = "mc" # mc ou data
        option_mthreads = 3
        
    ## Use options
        relvaldir = 'RelVal'
        if option_is_from_data == 'data':
            relvaldir = 'RelValData'
    
    #case 1 self.my_choice_rel_0 : RELEASE
        print("cmd_load_files 2 : case 1 %s : RELEASE" % self.my_choice_rel_0)
        option_release_rel = str(self.my_choice_rel_0)
        filedir_url = BaseURL(self) + relvaldir + '/' + str(self.my_choice_rel_0) + '/'
        for line in self.releasesList_rel_5:
            print("cmd_load_files : self.releasesList_rel_5 : %s" % line)
            if not clean_collections2(line, self.validationType1, validationType_2, validationType_3, "rel"):
                print "cmd_load_files : " + filedir_url + line + " removed"
                temp_toBeRemoved.append(line)
    #print("cmd_load_files : self.releasesList_rel_5 : remove lines")
        for line in temp_toBeRemoved:
            self.releasesList_rel_5.remove(line)
    #print("cmd_load_files : copy self.releasesList_rel_5 to selected_files_rel")
        selected_files_rel = self.releasesList_rel_5
    #print("cmd_load_files : selected_files_rel = %s" % str(selected_files_rel))
    
    #print("cmd_load_files : change directory")
        os.chdir(self.working_dir_rel)   # Change current working directory to release directory
    
        print("cmd_load_files : cmd_fetch_2")
        cmd_fetch_2(option_is_from_data, option_release_rel, option_mthreads, filedir_url, selected_files_rel)

    #case 2 self.my_choice_ref_0 : REFERENCE
        temp_toBeRemoved[:] = []# clear the temp array
        print("cmd_load_files : case 2 %s : REFERENCE" % self.my_choice_ref_0)
        option_release_ref = str(self.my_choice_ref_0) 
        filedir_url = BaseURL(self) + relvaldir + '/' + str(self.my_choice_ref_0) + '/'
        for line in self.releasesList_ref_5:
            print("cmd_load_files : self.releasesList_ref_5 : %s" % line)
            if not clean_collections2(line, self.validationType1, validationType_2, validationType_3, "ref"):
                print "cmd_load_files : " + filedir_url + line + " removed"
                temp_toBeRemoved.append(line)
    #print("cmd_load_files : self.releasesList_ref_5 : remove lines")
        for line in temp_toBeRemoved:
            self.releasesList_ref_5.remove(line)
    #print("cmd_load_files : copy self.releasesList_ref_5 to selected_files_ref")
        selected_files_ref = self.releasesList_ref_5
    #print("cmd_load_files : selected_files_ref = %s" % str(selected_files_ref))
    
    #print("cmd_load_files : change directory")
        os.chdir(self.working_dir_ref)   # Change current working directory to release directory
    
        print("cmd_load_files : cmd_fetch_2")
        cmd_fetch_2(option_is_from_data, option_release_ref, option_mthreads, filedir_url, selected_files_ref)
    
        print "cmd_load_files end OK"
        return