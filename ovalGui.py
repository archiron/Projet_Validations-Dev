#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from Variables import *
from ovalOptionsGp import initGpOptions
from ovalChoiceGp import initGpChoice
from ovalBottomGp import initGpBottom
from getEnv import env
from fonctions import folder_creation, finalFolder_creation, working_dirs_creation # , get_collection_list, get_validationType1, clean_files, copy_files
from fonctions import list_search_1, list_search_3 # list_search_0, , list_search_2, list_search, explode_item
from fonctions import folderExtension_creation # list_simplify, create_file_list, create_commonfile_list, 
from fonctions import sub_releases, sub_releases2, print_arrays, list_search_5 #, list_search_4
from fonctions import checkFastvsFull, getCheckedOptions
from fonctions import checkFileName, newName
from Datasets_default import DataSetsFilter, extractDatasets, extractDatasetsFastvsFull, checkCalculValidation
from Paths_default import *
from functionGui import clearDataSets, clearDataSetsLists, writeLabelCombo3, clearReleasesList
from functionGui import fillQLW_rel1, fillQLW_rel2_rel, fillQLW_rel2_ref, enableRadioButtons, disableRadioButtons
from networkFunctions import cmd_load_files
		
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        initVariables(self)
        self.wp.write("initVariables OK\n")
        
        self.setWindowTitle(self.version)  # minor correction to have release up to the right window for release and reference choice.
        # create fillQLW_rel1 for filling QLW list.
        # new architecture ; the optionGrp is not enabled (greyed) and it is only enabled for tasks_counter == 2
        # conditionnal Fast vs Full is corrected : we can go to Fast vs Full and back to RECO, keeping the old reference and the associated lists.
        
        # Need to rename files in ovalOptions or ovalChoice as option or choice
        
        # Need to create one folder per dataset.
        # Perhaps need to recreate dataset, rel/ref root files structure.
        # Need to fix the Fast list of root files and more generaly the checkCalculValidation function.
        # Need to re-see about comparison of datasets for FastvsFull. In some cases there can not be the same.
        # For pmx vs pmx or pmx vs PU we need to reconsider the tests and the file list because pmx vs PU is with the same release.
     
        # From top to bottom, there is 4 parts :
        # PART 1 : GroupBoxes for validation choice
        # PART 2 : Resume label for actions listing
        # PART 3 : GroupBoxes for Tag selection
        # BOTTOM PART : buttons
        # FINAL PART : keeping all previous part into one

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

    def radio11Clicked(self):
        self.radio11.setChecked(True)
        self.validationType1 = 'Full'
        self.checkDataSets2Clicked()
        if ( self.my_choice_tmp != "" ):
            self.my_choice_ref_1 = self.my_choice_tmp
            self.ref_list_1 = self.ref_list_1_tmp
            self.releasesList_ref_2 = self.releasesList_ref_2_tmp
            self.my_choice_tmp = ""
            self.releasesList_ref_2_tmp = []
            self.ref_list_1_tmp = []
            tmp = "Reference : " + self.my_choice_ref_1
            self.labelCombo2.setText(tmp)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()

    def radio12Clicked(self):
        self.radio12.setChecked(True)
        self.validationType1 = 'Fast'
        self.checkDataSets2Clicked()
        if ( self.my_choice_tmp != "" ):
            self.my_choice_ref_1 = self.my_choice_tmp
            self.ref_list_1 = self.ref_list_1_tmp
            self.releasesList_ref_2 = self.releasesList_ref_2_tmp
            self.my_choice_tmp = ""
            self.releasesList_ref_2_tmp = []
            self.ref_list_1_tmp = []
            tmp = "Reference : " + self.my_choice_ref_1
            self.labelCombo2.setText(tmp)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
        
    def radio13Clicked(self):
        self.radio13.setChecked(True)
        self.validationType1 = 'FastFull'
        self.checkSpecTarget1.setChecked(True)
        self.checkSpecReference1.setChecked(True) #default
        self.checkDataSets2Clicked()
        self.my_choice_tmp = self.my_choice_ref_1
        self.releasesList_ref_2_tmp = self.releasesList_ref_2
        self.ref_list_1_tmp = self.ref_list_1

        self.my_choice_ref_0 = self.my_choice_rel_0
        self.my_choice_ref_1 = self.my_choice_rel_1
        print ("my_choice_rel_0 = ") , self.my_choice_rel_0 # temp
        print ("my_choice_rel_1 = ") , self.my_choice_rel_1 # temp
        print ("my_choice_ref_0 = ") , self.my_choice_ref_0 # temp
        print ("my_choice_ref_1 = ") , self.my_choice_ref_1 # temp
        self.releasesList_ref_2 = self.releasesList_rel_2 # no need to recompute the list
        self.ref_list_1 = self.rel_list_1 # no need to recompute the list
        for item in self.releasesList_ref_2: # temp
            self.wp.write("ItemRelRefClicked2 : %s\n" % item) # temp
        self.wp.write("\n") # temp
        for item in self.ref_list_1: # temp
            self.wp.write("ItemRelRefClicked2 : %s\n" % item) # temp
        tmp = "Reference : " + self.my_choice_ref_1
        self.labelCombo2.setText(tmp)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents()
        
    def checkSpecTarget1_Clicked(self):
        self.checkSpecTarget1.setChecked(True)
        self.checkSpecReference1_Clicked()
        self.validationType2 = 'RECO'
        getCheckedOptions(self)
        print "Target, self.validationType2 : %s" % self.validationType2
        print "Target, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents()

    def checkSpecTarget2_Clicked(self):
        self.checkSpecTarget2.setChecked(True)
        self.checkSpecReference2_Clicked() #default
        self.validationType2 = 'PU25'
        getCheckedOptions(self)
        print "Target, self.validationType2 : %s" % self.validationType2
        print "Target, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents()
        
    def checkSpecTarget3_Clicked(self):
        self.checkSpecTarget3.setChecked(True)
        self.checkSpecReference2_Clicked()
        self.validationType2 = 'PUpmx25'
        getCheckedOptions(self)
        print "Target, self.validationType2 : %s" % self.validationType2
        print "Target, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents()
                        
    def checkSpecTarget4_Clicked(self):
        self.checkSpecTarget4.setChecked(True)
        self.validationType2 = 'miniAOD'
        self.checkSpecReference4_Clicked()
        getCheckedOptions(self)
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
        print "Reference, self.validationType2 : %s" % self.validationType2
        print "Reference, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkSpecReference2_Clicked(self):
        self.checkSpecReference2.setChecked(True)
        self.validationType3 = 'PU25'
        getCheckedOptions(self)
        print "Reference, self.validationType2 : %s" % self.validationType2
        print "Reference, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkSpecReference3_Clicked(self):
        self.checkSpecReference3.setChecked(True)
        self.validationType3 = 'PUpmx25'
        getCheckedOptions(self)
        print "Reference, self.validationType2 : %s" % self.validationType2
        print "Reference, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkSpecReference4_Clicked(self):
        self.checkSpecReference4.setChecked(True)
        self.validationType3 = 'miniAOD'
        getCheckedOptions(self)
        print "Reference, self.validationType2 : %s" % self.validationType2
        print "Reference, self.validationType3 : %s" % self.validationType3
        self.checkDataSets2Clicked()
        QtCore.QCoreApplication.processEvents() 

    def checkDataSets2Clicked(self):
        self.wp.write("checkDataSets2Clicked")
        self.checkAllNone1.setChecked(True) # as all DataSets are checked, we need the radiobutton All to be checked
        from Datasets_default import DataSetsFilter
        self.DataSetTable = DataSetsFilter(self)
        reload(sys.modules['Datasets_default'])
        self.menu.clear()
        self.ag = QActionGroup(self, exclusive=False)
        for item in self.DataSetTable:
            (item_name, item_checked) = item
            self.wp.write(item_name + "\n")
            a = self.ag.addAction(QAction(item_name, self, checkable=True, checked=item_checked)) # checked=True
            self.menu.addAction(a)
            self.connect(a, SIGNAL('triggered()'), self.QGBoxListsUpdate)
        self.setFixedSize(1200, 700)
        self.QGBoxListsUpdate()
        QtCore.QCoreApplication.processEvents() 
    
    def checkLocation2Clicked(self):
        print "checkLocation2Clicked"
        self.wp.write("checkLocation2Clicked")
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
                self.wp.write("\n")
                for item in self.ref_list_0:
                    self.wp.write("ItemRelRefClicked1 : %s\n" % item)
            else:
                self.my_choice_ref_0 = self.QLW_rel1.currentItem().text()
                self.releasesList_ref_1 = list_search_1(self.my_choice_ref_0)
                self.ref_list_0 = sub_releases(self.releasesList_ref_1) #list_search_1(self.my_choice_ref_0))
            print "ItemRefClicked1 : self.my_choice_ref_0 : %s " % self.my_choice_ref_0
            #for it in self.ref_list_0:
            #    item = QListWidgetItem("%s" % it)
            #    self.QLW_rel2.addItem(item)
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
        #    if (checkFastvsFull(self)): # no more used here. To be moved in radio13Clicked
        #        self.my_choice_ref_0 = self.my_choice_rel_0
        #        self.my_choice_ref_1 = self.my_choice_rel_1
        #        print ("my_choice_rel_0 = ") , self.my_choice_rel_0 # temp
        #        print ("my_choice_rel_1 = ") , self.my_choice_rel_1 # temp
        #        print ("my_choice_ref_0 = ") , self.my_choice_ref_0 # temp
        #        print ("my_choice_ref_1 = ") , self.my_choice_ref_1 # temp
        #        self.releasesList_ref_2 = self.releasesList_rel_2 # no need to recompute the list
        #        self.ref_list_1 = self.rel_list_1 # no need to recompute the list
        #        for item in self.releasesList_ref_2: # temp
        #            self.wp.write("ItemRelRefClicked2 : %s\n" % item) # temp
        #        self.wp.write("\n") # temp
        #        for item in self.ref_list_1: # temp
        #            self.wp.write("ItemRelRefClicked2 : %s\n" % item) # temp
        #    else:
        #        self.my_choice_ref_1 = self.QLW_rel2.currentItem().text()
        #        self.releasesList_ref_2 = list_search_3(self.releasesList_ref_1, str(self.my_choice_ref_1))
            self.ref_list_1 = sub_releases2(str(self.my_choice_ref_1), self.releasesList_ref_2)
            self.my_choice_ref_1 = self.QLW_rel2.currentItem().text()
            self.releasesList_ref_2 = list_search_3(self.releasesList_ref_1, str(self.my_choice_ref_1))
            self.ref_list_1 = sub_releases2(str(self.my_choice_ref_1), self.releasesList_ref_2)
            print "ItemRefClicked2 : self.my_choice_ref_1 : %s " % self.my_choice_ref_1
            tmp = "Reference : " + self.my_choice_ref_1
            self.labelCombo2.setText(tmp)
        else: # self.tasks_counter == 0
            print "release" + str(self.tasks_counter)
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
        import re
        if self.tasks_counter == 0:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
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
            fillQLW_rel1(self)
        elif self.tasks_counter == 1:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
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
            fillQLW_rel1(self)
        elif self.tasks_counter == 2:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            enableRadioButtons(self)
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
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(True)
            self.QGBox_rel0.setTitle("Selected")
            self.QGBox_rel0.setVisible(False)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(True)
            clearReleasesList(self)
            self.QGBoxListsUpdate()
            
            selectedText = "<strong>Selected :</strong>"
            selectedText += "<table>"
            if ( checkFastvsFull(self) ): # FastvsFast
                selectedText += "<br /><br /><strong>Fast vs Fast : </strong>"
            selectedText += "<tr>"
            if (self.selectedRelDatasets == self.selectedRefDatasets):
                self.okToPublishDatasets = self.selectedRelDatasets
                selectedText += "<td colspan=\"2\"><br /><strong><font color = \"green\">Datasets : " + self.selectedRelDatasets + "</font></strong><br /></td>"
            else: # need to extract common terms in blue and others in black (red?)
                (self.okToPublishDatasets, self.okToDisplayDatasets) = extractDatasets(self)
                selectedText += "<td colspan=\"2\"><br /><strong>Datasets : " + self.okToDisplayDatasets + "</strong><br /></td>"
            selectedText += "<td>  </td>"
            selectedText += "<td><font color = \"blue\">For Web Page Publish</font><br /><strong><font color = \"red\">" + self.okToPublishDatasets + "</font></strong><br /></td>"           
            selectedText += "</tr><tr><td><strong>GlobalTags : </td>" 
            selectedText += "<td>" + self.my_choice_rel_1 + "<br />" + self.selectedRelGlobalTag + "</td>" 
            selectedText += "<td> &nbsp;&nbsp;&nbsp; </td>"
            selectedText += "<td>" + self.my_choice_ref_1 + "<br />" + self.selectedRefGlobalTag + "</strong></td>"           
            selectedText += "</tr></table>"
            
            if ( checkFastvsFull(self) ): # FastvsFull
                selectedText += "<br /><br /><strong>Fast vs Full : </strong>"
                selectedText += "<table><tr>"
                if (self.selectedRelDatasets == self.selectedFvsFDatasets):
                    self.okToPublishFvsFDatasets = self.selectedRelDatasets
                    selectedText += "<td colspan=\"2\"><br /><strong><font color = \"green\">Datasets : " + self.selectedRelDatasets + "</font></strong><br /></td>"
                else:
                    (self.okToPublishFvsFDatasets, self.okToDisplayFvsFDatasets) = extractDatasetsFastvsFull(self)
                    selectedText += "<td colspan=\"2\"><br /><strong>Selected Fast vs Full Datasets : " + self.okToDisplayFvsFDatasets + "</strong><br /><br /></td>"
                selectedText += "<td>  </td>"
                selectedText += "<td><font color = \"blue\">For Web Page Publish</font><br /><strong><font color = \"red\">" + self.okToPublishFvsFDatasets + "</font></strong></td>"           
                selectedText += "</tr><tr><td><strong>GlobalTags : </td>"
                selectedText += "<td>" + self.my_choice_rel_1 + "<br />" + self.selectedRelGlobalTag  + "</td>" 
                selectedText += "<td> &nbsp;&nbsp;&nbsp; </td>"
                selectedText += "<td>" + self.my_choice_rel_1 + "<br />" + self.selectedFvsFGlobalTag + "</strong></td>"
                selectedText += "</tr>"
            selectedText += "</table>"
            self.labelResumeSelected.setText(self.trUtf8(selectedText))
            
            print "self.okToPublishDatasets = %s" % self.okToPublishDatasets
            print "self.okToPublishFvsFDatasets = %s" % self.okToPublishFvsFDatasets
            print "self.okToDisplayDatasets = %s" % self.okToDisplayDatasets
            print "self.okToDisplayFvsFDatasets = %s" % self.okToDisplayFvsFDatasets
            
            ## here we have a common (rel & ref) dataset named as self.okToPublishDatasets for Full vs Full or Fast vs Fast. 
            ## we also have a common dataset for Fast vs Full named as self.okToPublishFvsFDatasets
            ## WARNING : we need to have self.okToPublishFvsFDatasets = self.okToPublishDatasets !! ##
            
            # create list of root files for rel & ref
            print "0 " + self.selectedRelDatasets
            print "1 " + self.okToPublishDatasets
            #self.releasesList_rel_3 = (self.selectedRelDatasets.replace(" ", "")).split(',') # to be deleted
            #self.releasesList_ref_3 = (self.selectedRefDatasets.replace(" ", "")).split(',') # to be deleted
            self.releasesList_3 = (self.okToPublishDatasets.replace(" ", "")).split(',') # replace releasesList_rel_3 & releasesList_ref_3
            print "\nRelease :"
            for it1 in self.releasesList_rel_2: # it1 = root file
                if checkFileName(self, it1, "rel"):
                    #for it2 in self.releasesList_rel_3: # it2 = dataSet # to be deleted
                    for it2 in self.releasesList_3: # it2 = dataSet
                        #print str(it2)
                        #if (re.search(str(it2), it1) and re.search(str(self.selectedRelGlobalTag), it1)):
                        if (re.search(str(newName("__RelVal", it2, "__")), it1) and re.search(str(self.selectedRelGlobalTag), it1)): # at least one file here
                             if checkCalculValidation(self, it1):
                                print it2 + " : " + it1 + " : OK"
                                self.releasesList_rel_5.append(it1)
            # perhaps add a test to verify if there is at least one file and if not, remove the dataSet.
            print "\nReference :"
            for it1 in self.releasesList_ref_2: # it1 = root file
               if checkFileName(self, it1, "ref"):
                    #for it2 in self.releasesList_ref_3: # it2 = dataSet # to be deleted
                    for it2 in self.releasesList_3: # it2 = dataSet
                        #print ">>>>> " + it2 + " _ " + newName("__RelVal", it2, "__")
                        #if (re.search(str(it2), it1) and re.search(str(self.selectedRefGlobalTag), it1)):
                        if (re.search(str(newName("__RelVal", it2, "__")), it1) and re.search(str(self.selectedRefGlobalTag), it1)):
                            if checkCalculValidation(self, it1):
                                print it2 + " : " + it1 + " : OK"
                                self.releasesList_ref_5.append(it1)
            if ( checkFastvsFull(self) ): # FastvsFull ## to be completed with another test only on Full, RECO
                print "\nFastvsFull :"
                self.wp.write("okToPublishFvsFDatasets FastvsFull = %s\n" % self.okToPublishFvsFDatasets)
                for it1 in self.releasesList_rel_2: # it1 = root file
                    #for it2 in self.releasesList_rel_3: # it2 = dataSet # to be deleted
                    for it2 in self.releasesList_3: # it2 = dataSet
                        if (re.search(str(it2), it1) and re.search(str(self.selectedFvsFGlobalTag), it1)):
                            if checkCalculValidation(self, it1):
                                print it2 + " : " + it1 + " : OK"
                                self.releasesList_FvsF_5.append(it1)
            # print length of the arrays
            print "self.releasesList_rel_3 : %d\n" % len(self.releasesList_rel_3) # to be deleted
            print "self.releasesList_ref_3 : %d\n" % len(self.releasesList_ref_3) # to be deleted
            print "self.releasesList_3 : %d\n" % len(self.releasesList_3)
            print "self.releasesList_rel_2 : %d\n" % len(self.releasesList_rel_2)
            print "self.releasesList_ref_2 : %d\n" % len(self.releasesList_ref_2)
            print "self.releasesList_rel_5 : %d\n" % len(self.releasesList_rel_5)
            print "self.releasesList_ref_5 : %d\n" % len(self.releasesList_ref_5)
            #print "self.releasesList_FvsF_5 : %d\n" % len(self.releasesList_FvsF_5)
            print BaseURL(self) # temporaire
            self.wp.write("BaseUrl = %s\n" % BaseURL(self))
            print_arrays(self) # temporaire
          
        elif self.tasks_counter == 4:
            print "self.tasks_counter = %d/%d" % (self.tasks_counter, self.tasks_counterMax)
            self.wp.write("self.tasks_counter = %d/%d\n" % (self.tasks_counter, self.tasks_counterMax))
            self.bouton_Previous.setEnabled(True)
            self.bouton_Next.setEnabled(False)
            self.QGBox_Selected.setTitle("Web page")
            self.QGBox_rel0.setVisible(False)
            self.QGBox_Lists.setVisible(False)
            self.QGBox_Selected.setVisible(True)
            self.labelResumeSelected.clear() # do not work
            self.PathUpdate()
            self.QGBoxListsUpdate()

            print "begin files loading !"
            self.wp.write("begin files loading !\n")
            cmd_load_files(self)
            #TEMPORAIRE display list of root files
            for line in self.releasesList_rel_5:
                print line

            for line in self.releasesList_ref_5:
                print line

            if (checkFastvsFull(self)):
                for line in self.releasesList_FvsF_5:
                    print line
            #TEMPORAIRE
            
            #### output of the webpage and gifs pictures
            # step 1 : Full vs Full or Fast vs Fast
            dirname = str(self.finalFolder) + '/' 
            if (checkFastvsFull(self)): # Fast to be treated
                dirname += 'FastvsFast_'
            else:
                dirname += 'FullvsFull_'
            dirname += str(self.my_choice_ref_1[6:]) + '_xxx' + folderExtension_creation(self) # _xxx is temp. must be only _DQM_std/_DMQ_dev.
            #dirname += '/gifs' # only for datasets
            self.wp.write("self.finalFolder reference : %s\n" % dirname)
            if not os.path.exists(dirname): # 
                os.makedirs(str(dirname))
            
            # step 2 : Fast vs Full or Fast vs Fast
            if (checkFastvsFull(self)): # Fast to be treated
                dirname = str(self.finalFolder) + '/' + 'FastvsFull_'
                # ....
            ####
            
        else:
            print "Hello Houston, we have a pbm !!"
        writeLabelCombo3(self)
        self.bouton_Previous.setText(self.trUtf8(self.tasks_list[self.tasks_counter-1]))

    def PathUpdate(self):
        print "menu clicked !"
        print "*-*-**--*-*-*-*-*-* Location"
        self.wp.write("PathUpdate\n")
        self.LocationTable = LocationFilter(self)
        tt = self.loc.actions()
        i_loc = 0
        for it in tt:
            print "self.ag.actions()", it.text()
            if it.isChecked():
                print "%s is checked" % it.text()
                self.wp.write("%s is checked\n" % it.text())
                print "folder path : %s" % self.LocationTable[i_loc][2]
                self.wp.write("folder path : %s\n" % self.LocationTable[i_loc][2])
                self.finalFolder = self.LocationTable[i_loc][2] + "/" + self.my_choice_rel_1[6:] + '_xxx' + folderExtension_creation(self) # _xxx is temp. must be only _DQM_std/_DMQ_dev.
                self.wp.write("self.finalFolder : %s\n" % self.finalFolder)
                self.wp.write("self.working_dir_base : %s\n" % self.working_dir_base)
                working_dirs_creation(self)
                folder_creation(self) # create local folder for files loading and operation resuming
                finalFolder_creation(self) # create the save folder for html and gifs files
            else:
                print "%s is unchecked" % it.text()
                self.wp.write("%s is unchecked\n" % it.text())
            i_loc += 1
            
    def QGBoxListsUpdate(self):
        print "menu clicked !"
        print "*-*-**--*-*-*-*-*-* DataSets"
        getCheckedOptions(self)
        
        if (self.my_choice_rel_0 != ''): # print the list of the releases
            for index in xrange(self.QLW_rel1.count()):
                print "self.QLW_rel1.item(%d) : %s" % ( index, self.QLW_rel1.item(index).text() )
        if (self.my_choice_ref_1 != ''): # this implies that all others my_choice_ref(l) have been choosen
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
                tempDataset = self.selectedDataSets
                tempDataset.sort()
                datasetList = self.selectedDataSets[0]
                for it in range(1, len(tempDataset)):
                    datasetList += ', ' + self.selectedDataSets[it]
                print datasetList # TEMPORAIRE

                #clearDataSets(self)
                clearDataSetsLists(self)
                print "nb of datasets rel   : ", len(self.releasesList_rel_3) # TEMPORAIRE
                print "nb of globaltags rel : ", len(self.releasesList_rel_3b) # TEMPORAIRE
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
                
                print "nb of datasets ref   : ", len(self.releasesList_ref_3) # TEMPORAIRE
                print "nb of globaltags ref : ", len(self.releasesList_ref_3b) # TEMPORAIRE
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
                print "len of selectedDataSets = %d" % len(self.selectedDataSets)
                #clearDataSets(self)
                clearDataSetsLists(self)

        QtCore.QCoreApplication.processEvents() 
        
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
        self.wp.write("ItemSelectedTable_rel : self.selectedRelDatasets : %s\n " % self.selectedRelDatasets)
        self.wp.write("ItemSelectedTable_rel : self.selectedRelGlobalTag : %s\n " % self.selectedRelGlobalTag)

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

    def showAbout(self):
        print("About")
        #msg = QMessageBox()
        #pixmap = QPixmap(30,30)
        #pixmap.load('GUI_00.bmp')
        #msg.setIconPixmap(pixmap)
        #msg.setText("About")
        #msg.setInformativeText("This is additional information for about")
        #msg.setWindowTitle("About")
        #msg.setStandardButtons(QMessageBox.Ok)
        #msg.exec_()
        
        pixmap2 = QPixmap('/afs/cern.ch/user/a/archiron/lbin/Projet_Validations-Dev/GUI_001.bmp')
        dialog = QDialog()
        layout = QVBoxLayout(dialog)
        labell = QLabel()
        labell.setText(self.version)
        label3 = QLabel()
        label3.setText('<br>All dev made by A. CHIRON<br>Laboratoire Leprince-Ringuet<br>')
        label2 = QLabel()
        label2.setPixmap(pixmap2)
        label4 = QLabel()
        label4.setText('<br>Special thanks to <font color=\'blue\'>Emilia</font> for her help<br>')
        layout.addWidget(labell)
        layout.addWidget(label3)
        layout.addWidget(label2)
        layout.addWidget(label4)
        label2.show()
        dialog.exec_()
    
    def showHelp(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Help")
        msg.setInformativeText("This is additional information for help")
        msg.setWindowTitle("HELP")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

