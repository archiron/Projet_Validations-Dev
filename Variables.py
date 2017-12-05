#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import list_search_0#, list_search_1, list_search_2, list_search_3, list_search, explode_item

def initVariables(self):
    self.cmsenv = env()
    self.texte = self.cmsenv.cmsAll()
    self.validationType1 = 'Full'   # default
    self.validationType2 = 'RECO'   # default
    self.validationType3 = 'global' # default
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
    self.releasesList_rel_2 = []
    self.releasesList_ref_2 = []
    self.releasesList_rel_3 = []
    self.releasesList_ref_3 = []
    self.releasesList_rel_3b = []
    self.releasesList_ref_3b = []
    self.releasesList_rel_4 = []
    self.releasesList_rel_4b = []
    self.releasesList_rel_5 = []
    self.releasesList_ref_5 = []
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
    
    try:
        self.wp = open('report.txt', 'w') # report page
    except IOError as ioe:
        print "Could not open file! "
        
    # Release : the release to be validated
    # Reference : the reference release
    # Lists : list of globalTags for release/reference
    # Selected : the selected globalTag and associated DataSets
    self.tasks_list = ['Release list', 'Reference list', 'Lists', 'Selected', 'Web page'] # 
    self.tasks_counter = 0
    self.tasks_counterMax = len(self.tasks_list) -1
    print "self.tasks_counterMax = %d" % self.tasks_counterMax # TEMPORAIRE
    self.wp.write("self.tasks_counterMax = %d\n" % self.tasks_counterMax)
    self.selectedDataSets = []
    
    self.allMenuListDatasetsChecked = False # default
    self.checkFastvsFull = False # default
    
    self.listHeader = ["DataSets", "GlobalTags"]
    
    self.selectedRelDatasets = ""
    self.selectedRefDatasets = ""
    self.selectedRelGlobalTag = ""
    self.selectedRefGlobalTag = ""
    self.selectedFvsFDatasets = "" # FastvsFull
    self.selectedFvsFGlobalTag = "" # FastvsFull
    
    self.okToPublishDatasets = ""
    self.okToPublishFvsFDatasets = ""
    self.okToDisplayDatasets = "" # only for display
    self.okToDisplayFvsFDatasets = "" # only for display
    
    return
    
