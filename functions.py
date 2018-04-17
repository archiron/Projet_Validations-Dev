#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess, shutil
import urllib2
import re
from getEnv import env
from Paths_default import *
from Datasets_default import DataSetsFilter, extractDatasets, extractDatasetsFastvsFull, checkCalculValidation, testForDataSetsFile
from electronCompare import *

def working_dirs_creation(self): # working dir are for resuming the computation. Used for root files loading.
    import errno
#    print "cmd_working_dirs_creation"
    self.working_dir_rel = self.working_dir_base + '/' + str(self.my_choice_rel_1[6:]) # self.lineedit1.text()[6:]
    self.working_dir_ref = self.working_dir_rel + '/' + str(self.my_choice_ref_1[6:]) # self.lineedit3.text()[6:]
    self.wp.write("self.working_dir_rel : %s\n" % self.working_dir_rel)
    self.wp.write("self.working_dir_ref : %s\n" % self.working_dir_ref)
    self.textReport += "self.working_dir_rel : " + self.working_dir_rel + "<br>"
    self.textReport += "self.working_dir_ref : " + self.working_dir_ref + "<br>"
    
    if not os.path.exists(self.working_dir_rel):
        os.chdir(self.working_dir_base) # going to base folder
        print "Creation of %s release folder" % str(self.working_dir_rel)
        try:
            os.makedirs(str(self.working_dir_rel))
        except OSError as e:
            if e.errno != errno.EEXIST: # the folder did not exist
                raise  # raises the error again
        self.wp.write("Creation of %s release folder\n" % str(self.working_dir_rel))
        self.textReport += "Creation of " + str(self.working_dir_rel) + " folder" + "<br>"
        self.exist_working_dir_rel = False
    else:
        print "release folder %s already created" % str(self.working_dir_rel)
        self.wp.write("release folder %s already created\n" % str(self.working_dir_rel))
        self.textReport += "release folder " + str(self.working_dir_rel) + " already created" + "<br>"
        self.exist_working_dir_rel = True
    os.chdir(self.working_dir_rel)   # Change current working directory
    if not os.path.exists(self.working_dir_ref):
        print "Creation of %s reference folder" % str(self.working_dir_ref)
        try:
            os.makedirs(str(self.working_dir_ref))
        except OSError as e:
            if e.errno != errno.EEXIST: # the folder did not exist
                raise  # raises the error again
        self.wp.write("Creation of %s reference folder\n" % str(self.working_dir_ref))
        self.textReport += "Creation of " + str(self.working_dir_ref) + " reference folder" + "<br>"
        self.exist_working_dir_ref = False
    else:
        print "reference folder %s already created" % str(self.working_dir_ref)
        self.wp.write("reference folder %s already created\n" % str(self.working_dir_ref))
        self.textReport += "reference folder " + str(self.working_dir_ref) + " already created" + "<br>"
        self.exist_working_dir_ref = True

    updateLabelResume(self)
    return
    
def folder_creation(self): # create the folders for the choice. the resuming text file will be put in.
    import subprocess, os, datetime
    now = datetime.datetime.now()
    newDirName = now.strftime("%Y_%m_%d-%H%M%S")

    actual_dir = os.getcwd()
    fieldname = self.validationType1 + "_"
    fieldname = fieldname + self.validationType2
    fieldname = fieldname + "_" + now.strftime("%Y_%m_%d-%H%M%S")
    print("fieldname : %s") % fieldname
    self.wp.write("fieldname : %s\n" % fieldname)
    self.textReport += "fieldname : " + fieldname + "<br>"
    
    m_dir = self.working_dir_rel + "/" + fieldname
    self.wp.write("m_dir : %s\n" % m_dir)
    self.textReport += "m_dir : " + m_dir + "<br>"
    os.chdir(self.working_dir_rel) # going into release dir
    if not os.path.exists(m_dir): # 
        os.makedirs(m_dir) # create reference folder
        self.wp.write("creating : %s folder\n" % m_dir)
        self.textReport += "creating : " + m_dir + " folder" + "<br>"
    else:
        print "%s already created" % m_dir
        self.wp.write("%s already created\n" % m_dir)
        self.textReport += m_dir + " already created" + "<br>"
    os.chdir(actual_dir)
               
    return # m_dir

def finalFolder_creation(self):
    print "finalFolder_creation"
    actual_dir = os.getcwd()
    if not os.path.exists(self.finalFolder): # only create the first folder for saving gifs, i.e. release folder. 
        os.makedirs(str(self.finalFolder))
        self.wp.write("Creation of (%s) folder\n" % str(self.finalFolder))
        self.textReport += "Creation of " + str(self.finalFolder) + " final folder" + "<br>"
        self.exist_finalFolder = False
    else:
        print "%s already created" % str(self.finalFolder)
        self.wp.write("%s already created\n" % str(self.finalFolder))
        self.textReport += "final folder " + str(self.finalFolder) + " already created" + "<br>"
        self.exist_finalFolder = True
    updateLabelResume(self)
    return
    
def dataSets_finalFolder_creation(self):
    actual_dir = os.getcwd()
    print "actual dir : %s" % actual_dir
    os.chdir(self.finalFolder) # going into finalFolder
    print "here : %s" % os.getcwd()
    print "okToPublishDatasets"
    print self.selectedRelDatasets
    print self.okToPublishDatasets
    # create datasets folders
    for i, elt in enumerate(self.finalList):
#        print elt[0]
        dts = elt[0]
#    for dts in self.okToPublishDatasets.split(','):
        dataSetFolder = str(self.validationType2 + '_' + dts)
        print '%s : %s' % (dts, dataSetFolder)
        if not os.path.exists(dataSetFolder): # create dataSetFolder
            os.makedirs(dataSetFolder) # create reference folder
            self.wp.write("creating : %s folder\n" % dataSetFolder)
            self.textReport += "creating : " + dataSetFolder + " folder" + "<br>"
            os.chdir(dataSetFolder)
            # create gifs folders
            os.makedirs('gifs') # create gifs folder for pictures
            self.wp.write("creating : gifs folder\n")
            self.textReport += "creating gifs folder" + "<br>"
            os.chdir('../')
        else: # dataSetFolder already created
            print "%s already created" % dataSetFolder
            self.wp.write("%s already created\n" % dataSetFolder)
            self.textReport += dataSetFolder + " already created" + "<br>"
            os.chdir(dataSetFolder)
            if not os.path.exists('gifs'): # 
                # create gifs folders
                os.makedirs('gifs') # create gifs folder for pictures
                self.wp.write("creating : gifs folder\n")
                self.textReport += "creating gifs folder" + "<br>"
            else:
                self.wp.write("gifs folder already created\n")
                self.textReport += "gifs folder already created" + "<br>"
            os.chdir('../')
        # get config files 
        os.chdir(dataSetFolder) # going to dataSetFolder
        [it1, it2] = testForDataSetsFile(self, dts)
        self.wp.write("config file for target : %s \n" % it1)
        self.wp.write("config file for reference : %s \n" % it2)
        self.textReport += "config file for target : " + it1 + "<br>"
        self.textReport += "config file for reference : " + it2 + "<br>"
        print "config file for target : " + it1
        print "config file for reference : " + it2
        
        shutil.copy2(it1, 'config_target.txt')
        shutil.copy2(it2, 'config_reference.txt')
        # create gifs pictures & web page
        CMP_CONFIG = 'config_target.txt'
        CMP_TITLE = 'gedGsfElectrons ' + dts
        CMP_RED_FILE = self.my_choice_rel_1
        CMP_BLUE_FILE = self.my_choice_ref_1
        
        f = open(CMP_CONFIG, 'r')
        for line in f:
            print line
            #line_read = line.split()
        input_rel_file = self.working_dir_rel + '/' + elt[1]
        print("input_rel_file : %s" % input_rel_file )
        f_rel = ROOT.TFile(input_rel_file)
        f_rel.ls()
        #h1 = getHisto(f_rel)

        input_ref_file = self.working_dir_ref + '/' + elt[2]
        print("input_ref_file : %s" % input_ref_file )
        f_ref = ROOT.TFile(input_ref_file)
        f_ref.ls()
        #h2 = getHisto(f_ref)

        wp = open('index.html', 'w') # web page
        wp.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
        wp.write("<html>\n")
        wp.write("<head>\n")
        wp.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
        wp.write("<title> " + CMP_TITLE + " </title>\n") #option -t dans OvalFile
        wp.write("</head>\n")
        wp.write("<a NAME=\"TOP\"></a>")
        wp.write("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"../../../../img/up.gif\" alt=\"Up\"/></a>&nbsp; " + CMP_TITLE + " </h1>\n" ) # option -t dans OvalFile
        if (f_ref == 0):
            wp.write("<p>In all plots below, there was no reference histograms to compare with")
            wp.write(", and the " + CMP_RED_FILE + " histograms are in red.") # new release red in OvalFile
        else:
            wp.write("<p>In all plots below")
            wp.write(", the <b><font color='red'> " + CMP_RED_FILE + " </font></b> histograms are in red") # new release red in OvalFile
            wp.write(", and the <b><font color='blue'> " + CMP_BLUE_FILE + " </font></b> histograms are in blue.") # ref release blue in OvalFile

        wp.write(" " + "red_comment" + " " + "blue_comment" + " Some more details") # comments from OvalFile
        wp.write(": <a href=\"electronCompare.C\">script</a> used to make the plots")
        wp.write(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms") # .txt file
        wp.write(", <a href=\"GIF/\">images</a> of histograms" + "." ) # GIF to be rename into gifs
        wp.write("</p>\n")

        f.close()
        wp.close()
        #f_rel.close()
        #f_ref.close()

        os.chdir('../') # back to the final folder.
        #print self.filesHistos # TEMPORAIRE
        #for file in self.filesHistos:
        #    print "%s" % self.working_dir_base + '/' + file
    
    # create index.html file
    
    #back to initial dir
    os.chdir(actual_dir) # going back
    return
    
def get_collection_list(self):
    import subprocess, os
    collection_list = []
    if self.radio11.isChecked(): # FULL
        if self.check31.isChecked():
            collection_list.append('Pt10Startup_UP15')
        if self.check32.isChecked():
            collection_list.append('Pt35Startup_UP15')
        if self.check33.isChecked():
            collection_list.append('Pt1000Startup_UP15')
        if self.check34.isChecked():
            collection_list.append('QcdPt80120Startup_13') # QcdPt80Pt120Startup_13
        if self.check35.isChecked():
            collection_list.append('TTbarStartup_13')
        if self.check36.isChecked():
            collection_list.append('ZEEStartup_13')
    else: #FAST, PU
        if self.check37.isChecked():
            collection_list.append('TTbarStartup')
        if self.check38.isChecked():
            collection_list.append('ZEEStartup')
    return collection_list

def get_collection_list_search(self):
    import subprocess, os
    collection_list = []
    if self.radio11.isChecked(): # FULL 
        if self.check31.isChecked():
            collection_list.append('RelValSingleElectronPt10_UP15')
        if self.check32.isChecked():
            collection_list.append('RelValSingleElectronPt35_UP15')
        if self.check33.isChecked():
            collection_list.append('RelValSingleElectronPt1000_UP15')
        if self.check34.isChecked():
            collection_list.append('RelValQCD_Pt_80_120_13')
        if self.check35.isChecked():
            collection_list.append('RelValTTbar_13')
        if self.check36.isChecked():
            collection_list.append('RelValZEE_13')
    else: #FAST, PU
        if self.check37.isChecked():
            collection_list.append('TTbar_13')
        if self.check38.isChecked():
            collection_list.append('ZEE_13')
    return collection_list
   
def get_validationType1(self): # no more used
    if self.radio11.isChecked(): # FULL
        self.validationType = 'Full'
        self.validationType = 'gedvsgedFull' # because radio04 is always checked
    if self.radio12.isChecked(): # FAST
        self.validationType = 'Fast'
    return
    
def get_validationType1_search(self): # no more used
    if self.radio11.isChecked(): # FULL
        get_validationType1 = 'Full'
    if self.radio12.isChecked(): # FAST
        get_validationType1 = 'Fast'
    return get_validationType1
    
def clean_files(self):
    import os,sys,subprocess,glob,shutil
#    print 'folder : ', self.folder_name
    for items in glob.glob('dd*.olog'): 
        os.remove(items)
    for items in glob.glob('dqm*.root'): 
        os.remove(items)
    for items in glob.glob(self.working_dir_base + '/*.olog'): 
        shutil.move(items, self.folder_name)
#    for items in glob.glob('*.root'): 
#        shutil.copy(items, self.folder_name)
#        shutil.move(items, self.folder_name)
    shutil.copy('OvalFile', self.folder_name)
    return
    
def copy_files(self):
    import os,sys,subprocess,glob,re,shutil
    for items in glob.glob('DQM*.root'): 
        pref1,pref2,chaine,exten = items.split("__")
        new_name = 'electronHistos.' + chaine + '.root'
        shutil.copyfile(items, new_name)
    return
    
def list_search(self):
    from networkFunctions import cmd_fetch
    
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = str(self.lineedit1.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_release_3 = str(self.lineedit3.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
    option_mthreads = 3
    option_dry_run = True # False for loading files
    self.gccs = get_validationType1_search(self) 
#    print "**********", "choix calcul : ", self.validationType, self.gccs # to be removed
    
    # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
    coll_list = get_collection_list_search(self)
    
    self.rel_list = []
    self.ref_list = []
    
    for items in coll_list:
        print "ITEMS : ", items
        option_regexp = str( items ) + '__'
        if ( self.gccs != 'Full' ):
            option_regexp += ',' + str(self.gccs)
#        print "**********", items, "- ", option_release_1 # to be removed
        (liste_fichiers_1) = cmd_fetch(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)
        self.rel_list += liste_fichiers_1
#        print "**********", items, "- ", option_release_3 # to be removed
        (liste_fichiers_3) = cmd_fetch(option_is_from_data, option_release_3, option_regexp, option_mthreads, option_dry_run)
        self.ref_list += liste_fichiers_3
        
#    print "\n****** cleaning ******"
    self.rel_list = clean_collections(self.rel_list, self.gccs)
    self.ref_list = clean_collections(self.ref_list, self.gccs)
#    print "****** done ******"
    
    # si on veut comparer deux releases par fichiers DQM
    # self.listeReference.currentText() pour la reference
    #print "reference : ", self.listeReference.currentText() # reste à extraire la release de reference
    #option_release = 'CMSSW_7_2_0_pre4' # self.listeReference.currentText()    
    #cmd_fetch(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run)

    return 

def clean_collections(collection, gccs):
    import re
    i = 0
    temp = []
    for items in collection:
#        print "data ", i, " : ", items
        i += 1
        if ( gccs == 'Full' ):
            if ( re.search('PU25', items) ):
                print " PU25 exist in Full", items # to be removed
            elif ( re.search('Fast', items) ):
                print " Fast exist in Full", items # to be removed
            else:
                temp.append(items)
        elif ( gccs == 'PU25' ):
            if ( re.search('Fast', items) ):
                print " Fast exist in PU25", items # to be removed
                temp.append(items) # TEMP. To be removed
            else:
                temp.append(items)
        else: # gccs == 'FAST'
            if ( re.search('PU25', items) ):
                print " PU exist in Fast", items # to be removed
            else:
                temp.append(items)
    return temp

def clean_collections2(collectionItem, validationType_1, validationType_2, validationType_3, relrefChoice):
    import re
    temp = True
    checkFvsF = ""
    # relrefChoice == "ref" and validationType1 == "FastFull" ==> Full, validationType_3
    # relrefChoice == "rel" and validationType1 == "FastFull" ==> Fast, validationType_2
    if ( ( relrefChoice == "ref") and (validationType_1 == "FastFull") ):
        checkFvsF = "Full"
    if ( ( relrefChoice == "rel") and (validationType_1 == "FastFull") ):
        checkFvsF = "Fast"
    
    valType = validationType_2 # default
    if ( relrefChoice == "ref" ):
        valType = validationType_3
    #print "relrefChoice : %s, valType : %s" %(relrefChoice, valType)
    
    c_Fast = False
    if ( re.search('Fast', collectionItem) ): #  match Fast 
        c_Fast = True
    c_PU25 = False
    if ( re.search('PU25', collectionItem) ): #  match PU AND PUpmx
        c_PU25 = True
    c_pmx25 = False
    if ( re.search('PUpmx25', collectionItem) ): #  match pmx
        c_pmx25 = True
    
    if ( valType == "PU25" ): # PU test (PU and not pmx)
        if ( not c_PU25 ):
            temp = False
    else: # valType != "PU25"
        if (c_PU25):
            temp = False
    
    if ( valType == "PUpmx25" ): # 
        if (not c_pmx25): # pmx test
            temp = False
    else:
        if (c_pmx25): # pmx test
            temp = False

    if ( (validationType_1 == "Fast") or ( checkFvsF == "Fast" )):
        if (not c_Fast):
            temp = False
    else:
        if (c_Fast): # Fast test
            temp = False
    
    # RESUMING
    #print "relrefChoice : %s, c_Fast : %s, c_PU25 : %s, c_pmx25 : %s - temp : %s)" % (collectionItem, c_Fast, c_PU25, c_pmx25, temp)
    
    return temp

def list_search_0(self):
    from networkFunctions import cmd_fetch_0
        
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
    option_mthreads = 3
    option_dry_run = True # False for loading files
    
    
    option_regexp = '' 
    (liste_releases_0) = cmd_fetch_0(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)

    i = 0
    temp_0 = []  
    for item in liste_releases_0:
        # find if some elements are empty or not. if no -> append
#        print item[0:-1], " : "
        tt = list_search_1(item[0:-1])
        if (len(tt) > 0):
 #           print len(tt)
            temp_0.append(item[0:-1])

    return temp_0

def list_search_1(my_choice_0):
    from networkFunctions import cmd_fetch_1
        
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = str( my_choice_0 )
#    print "**list search 1 : ", option_release_1
#    option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
    option_mthreads = 3
    option_dry_run = True # False for loading files
    
    option_regexp = '' 
    (liste_releases_1) = cmd_fetch_1(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)

    i = 0
    temp_1 = []  
#    print "longueur : ", len(liste_releases_1)
    if ( len(liste_releases_1) > 0 ):
        for item in liste_releases_1:
#            print "list search 1 : ", item
            temp_1.append(item)

    return temp_1

def list_search_2(collection, filtre):
    import re

    temp_1 = []  
    filtre = sorted(set(filtre), reverse=True)
    print "filtre : ", filtre
#    print "collection : ", collection
    for item1 in collection:
        for item2 in filtre:
            if (item2 == item1):
                temp_1.append(item1)
#                print "OK : ", item2, item1
                break
#            else:
#                print "KO : ", item2, item1
    temp_1 = sorted(set(temp_1), reverse=True)
    return temp_1
    
def list_search_3(collection, filtre):
    import re

#    print "lg collection : ", len(collection)
#    print "lg filtre     : ", len(filtre), filtre
    temp_1 = []  
    for item1 in collection:
        if re.search(filtre, item1):
            temp_1.append(item1)
#            print "OK : ", filtre, item1
#        else:
#            print "KO : ", filtre, item1
    return temp_1
    
def list_search_4(collection, filtre, validationType_1, validationType_2): # no more used
    import re

    temp_1 = []
    temp_2 = []
    filtre = sorted(set(filtre), reverse=True)
#    print "filtre : ", filtre
#    print "collection : ", collection
    for item1 in collection:
        for item2 in filtre:
            if re.search(item2, item1):
                if clean_collections2(item1, validationType_1, validationType_2):
                    temp_1.append(item1)
                    temp_2.append(explode_item(item1)[2])
                break
#            else:
#                print "KO : ", item2, item1
    temp_1 = sorted(set(temp_1), reverse=True)
    temp_2 = sorted(set(temp_2), reverse=True)
    return (temp_1, temp_2)
    
def list_search_5(self):
    import re

    print " self.validationType1 = ",  self.validationType1
    print " self.validationType2 = ",  self.validationType2
    print " self.validationType3 = ",  self.validationType3
    #print " self.selectedDataSets = ", self.selectedDataSets # OK
    #print " self.releasesList_rel_2 = ", self.releasesList_rel_2 # OK
    #print " self.releasesList_ref_2 = ", self.releasesList_ref_2 # OK
    
    temp_1 = [] # DQM_V0001_R00000000X__Dataset__CMSSW_9_1_0_pre3-91X_upgrade2017_realistic_v3-v1__DQMIO.root files
    temp_2 = [] # 91X_upgrade2017_realistic_v3-v1 Global tags
    temp_12 = []
    temp_rel = []
    temp_3 = []
    temp_4 = []
    temp_34 = []
    temp_ref = []

    filtre = sorted(set(self.selectedDataSets), reverse=True)
    validationType_2 = self.validationType2
    validationType_3 = self.validationType3
    
    # DATASET
    self.rel_list_2 = list_search_2(self.rel_list_1, self.selectedDataSets) # get dataset list used in rel_list_1
    self.ref_list_2 = list_search_2(self.ref_list_1, self.selectedDataSets) # get dataset list used in ref_list_1

    # PART RELEASE
    filtre = sorted(set(self.rel_list_2), reverse=True)
    for item1 in self.releasesList_rel_2:
        for item2 in filtre:
            if re.search(item2, item1):
                if clean_collections2(item1, self.validationType1, validationType_2, validationType_3, "rel"):
                    temp_12.append([explode_item(item1)[2], item2])
                    print "len = %i" % len(temp_12)
                break

    print "len of temp_12 = %i." % len(temp_12)
    if ( len(temp_12) > 0 ):
#        print temp_12
        temp_12.sort()

        temp_rel.append( [temp_12[0][0], temp_12[0][1]] )
        k = 0
        for i in range(1, len(temp_12)):
            if ( temp_12[i][0] == temp_rel[k][0] ):
                temp_rel[k][1] += ', ' + temp_12[i][1]
            else:
                k +=1
                temp_rel.append( [temp_12[i][0], temp_12[i][1]] )
    for i in range(0, len(temp_rel)):
        temp_1.append(temp_rel[i][1])
        temp_2.append(temp_rel[i][0])
        
    # PART REFERENCE
    filtre = sorted(set(self.ref_list_2), reverse=True)
    if (( validationType_3 == 'miniAOD' ) and ( validationType_2 == 'RECO' )): # case RECO vs miniAOD
        temp_3 = temp_1
        temp_4 = temp_2
    else:
        releasesTemp = self.releasesList_ref_2
        if ( checkFastvsFull(self) ): # Fast vs Full
            releasesTemp = self.releasesList_rel_2
        for item1 in releasesTemp:
            for item2 in filtre:
                if re.search(item2, item1):
                    if clean_collections2(item1, self.validationType1, validationType_2, validationType_3, "ref"):
                        temp_34.append([explode_item(item1)[2], item2])
                        print "len = %i" % len(temp_34)
                    break
    
    print "len of temp_34 = %i." % len(temp_34)
    if ( len(temp_34) > 0 ):
        temp_34.sort()

        temp_ref.append( [temp_34[0][0], temp_34[0][1]] )
        k = 0
        for i in range(1, len(temp_34)):
            if ( temp_34[i][0] == temp_ref[k][0] ):
                temp_ref[k][1] += ', ' + temp_34[i][1]
            else:
                k +=1
                temp_ref.append( [temp_34[i][0], temp_34[i][1]] )
    for i in range(0, len(temp_ref)):
        temp_3.append(temp_ref[i][1])
        temp_4.append(temp_ref[i][0])
    

    return (temp_1, temp_2, temp_3, temp_4)
    
def sub_releases(tab_files):
    print "sub_releases", len(tab_files)
    i = 0
    temp = []
    for t in tab_files:
        tt = explode_item(t)
#        print '%d, %s' % (i+1, tt[1])
        temp.append(tt[1])
        i += 1
    temp = sorted(set(temp), reverse=True)
    return temp
    
def sub_releases2(release, tab_files):
    import re
    print "sub_releases2 : ", len(tab_files)
    print "release : ", release
    i = 0
    temp = []
    for t in tab_files:
        if ( re.search(release, t) ):
#            print 'sub_releases2 : %s' % t
            tt = explode_item(t)
#            print 'sub_releases2 : %d, %s, %s' % (i+1, tt[0], tt[1])
            temp.append(tt[0])
        i += 1
    temp = sorted(set(temp)) # , reverse=True
    return temp
    
def explode_item(item):
    # initial file name : DQM_V0001_R000000001__RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # prefix in DQM_V0001_R000000001__ removed : RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # suffix in __DQMIO.root removed : RelVal
    # new prefix in RelVal removed : TTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting with __ : TTbar_13 CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting second term with - : TTbar_13 CMSSW_7_4_0_pre8 PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    
#    print "explode item : ", item
    temp_item = item[22:] # DQM_V0001_R000000001__ removed
    temp_item = temp_item[:-12] # __DQMIO.root removed
    temp_item = temp_item[6:] # RelVal removed
    temp_item = temp_item.split('__')
#    print "coucou : ", temp_item
    temp_item2 = temp_item[1].split('-', 1)
    temp_item = [ temp_item[0] ]
    for it in temp_item2:
        temp_item.append(it)
#    print "coucou : ", temp_item

    return temp_item

def list_simplify(tablo):
    # simplification of tablo and self.ref_list_mod
    # WARNING : test before about len() = 1 -> do nothing

    temp = []
    item_line = tablo[0]
    temp2 = [item_line[2]]
    temp3 = [item_line[3]]
    
    item_line = ( tablo[0][0], tablo[0][1], [ tablo[0][2] ], [ tablo[0][3] ] )
#    print "\nlist_simplify : ", item_line

#    print "list_simplify : longueur tablo : ", len(tablo)
    if ( len(tablo) == 1 ):
        item_line = ( tablo[0][0], tablo[0][1], [ tablo[0][2] ], [ tablo[0][3] ] )
#        print "item_line : ", item_line
        
#    for items in tablo:
#        print "list_simplify - debut : ", items  
    for i in range(1, len(tablo)-0):
#        print "i = ", i
        (t, u, v, w) = tablo[i]
        if ( t == item_line[0]):
            if (u == item_line[1]):
                temp2.append(v)
                temp3.append(w)
                item_line = (item_line[0], item_line[1], temp2, temp3 )
                if ( i == len(tablo)-1 ):
                    temp.append(item_line)
            else :
                temp2 = (item_line[0], item_line[1], temp2) # to be removed ?
                temp.append(item_line)
                item_line = ( tablo[i][0], tablo[i][1], [ tablo[i][2] ], [ tablo[i][3] ] )
                temp2 = item_line[2]
                temp3 = item_line[3]
#                print "new item_line a : ", item_line
                if ( i == len(tablo)-1 ):
                    temp.append(item_line)
        else:
            temp.append(item_line)
            item_line = ( tablo[i][0], tablo[i][1],  [ tablo[i][2] ], [ tablo[i][3] ]  )
            temp2 = item_line[2]
            temp3 = item_line[3]
#            print "new item_line a : ", item_line
            if ( i == len(tablo)-1 ):
                temp.append(item_line)
    
#    print "longueur tablo : ", len(temp)
    if ( len(temp) == 0):
        temp.append(item_line)

#    for items in temp:
#        print "list_simplify - fin : ", items  
    
    return temp
      
def compare_datasets(t1, t2):
    import re
    temp = []
#    print "compare datasets"
    i = 0

    for it1 in t1:
        it11 = it1.replace('Startup', '')
        it11 = (it11.replace('_', '')).upper()
        for it2 in t2:
            it21 = (it2.replace('_', '')).upper()
            # to be continued avec re.search
            if ( re.search(it11, it21) ):
#                print "search : ", it11, " ", it21
                it22 = it21[-2:]
                if ( ( it22 == '13' ) or ( it22 == '15' ) ):
#                    print "OK"
                    temp.append([it1, it2])
                else:
                    print "KO : ", it22, it2, it1
    
    return temp

def create_file_list(tablo):
    temp = []
    print "\ncreate_file_list", tablo
#    part_1 = tablo[0]
#    part_2 = tablo[1]
    itl2 = tablo[2]
    itl3 = tablo[3]
#    print "create_file_list itl2", itl2
#    print "create_file_list itl3", itl3
#    print "create_file_list :", itl3
#    name_base = "DQM_V0001_R000000001__RelVal" 
#    name_suffix = "__" + part_1 + "-" + part_2 + "__DQMIO.root"
    i = 0
    for part_3 in itl2:
#        print "create_file_list %d : %s \n"% (i, part_3)
#        name_rel = name_base + part_3 + name_suffix
#        temp.append([part_3, name_rel])
        temp.append([part_3, itl3[i] ])
        i += 1
    return temp

def create_commonfile_list(t1, t2):
    import re
    temp = []
#    print "create commonfile list"
    for it1 in t1:
        for it2 in t2:
#            print it1, it2
            if (it1[0] == it2[0]):
#                print "create commeon file list : ", it1, it2
                temp.append([it1[0], it1[1], it2[1]])
    
    return temp

def clean_files_list(t1, t2):
    temp = []
#    print "clean_files_list"
    for it1 in t1:
#        print "clean : ",it1[0], it1[1]
        for it2 in t2:
#            print "clean : ", it2, it1[1], it2[0]
            if ( it1[1] == it2[0] ):
#                print 'ok'
                tmp = [it1[0], it1[1], it2[1], it2[2]]
                temp.append(tmp)
    return temp

def print_arrays(self):

    with open("array_list.txt", "w+") as f:
        f.write("self.releasesList_0" + "\n")
        self.wp.write("\n" + "self.releasesList_0" + "\n")
        for line in self.releasesList_0:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_rel_1" + "\n")
        self.wp.write("\n" + "self.releasesList_rel_1" + "\n")
        for line in self.releasesList_rel_1:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_ref_1" + "\n")
        self.wp.write("\n" + "self.releasesList_ref_1" + "\n")
        for line in self.releasesList_ref_1:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_rel_2" + "\n")
        self.wp.write("\n" + "self.releasesList_rel_2" + "\n")
        for line in self.releasesList_rel_2:
            self.wp.write(line + "\n") # write the line
            f.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_ref_2" + "\n")
        self.wp.write("\n" + "self.releasesList_ref_2" + "\n")
        for line in self.releasesList_ref_2:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_rel_3" + "\n")
        self.wp.write("\n" + "self.releasesList_rel_3" + "\n")
        for line in self.releasesList_rel_3:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_ref_3" + "\n")
        self.wp.write("\n" + "self.releasesList_ref_3" + "\n")
        for line in self.releasesList_ref_3:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.rel_list_0" + "\n")
        self.wp.write("\n" + "self.rel_list_0" + "\n")
        for line in self.rel_list_0:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.ref_list_0" + "\n")
        self.wp.write("\n" + "self.ref_list_0" + "\n")
        for line in self.ref_list_0:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.rel_list_1" + "\n")
        self.wp.write("\n" + "self.rel_list_1" + "\n")
        for line in self.rel_list_1:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.ref_list_1" + "\n")
        self.wp.write("\n" + "self.ref_list_1" + "\n")
        for line in self.ref_list_1:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.rel_list_2" + "\n")
        self.wp.write("\n" + "self.rel_list_2" + "\n")
        for line in self.rel_list_2:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.ref_list_2" + "\n")
        self.wp.write("\n" + "self.ref_list_2" + "\n")
        for line in self.ref_list_2:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_rel_3b" + "\n")
        self.wp.write("\n" + "self.releasesList_rel_3b" + "\n")
        for line in self.releasesList_rel_3b:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_ref_3b" + "\n")
        self.wp.write("\n" + "self.releasesList_ref_3b" + "\n")
        for line in self.releasesList_ref_3b:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_rel_5" + "\n")
        self.wp.write("\n" + "self.releasesList_rel_5" + "\n")
        for line in self.releasesList_rel_5:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.write("\n" + "self.releasesList_ref_5" + "\n")
        self.wp.write("\n" + "self.releasesList_ref_5" + "\n")
        for line in self.releasesList_ref_5:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line

        f.close()
    return

def checkFastvsFull(self):
    if ( self.radio13.isChecked() ):
    # check for FastvsFull for Fast.
        self.checkFastvsFull = True
        print("checkFastvsFull = True")
    else:
        self.checkFastvsFull = False
        print("checkFastvsFull = False")
    return self.checkFastvsFull

def newName(prefix, fileName, suffix):
    newName = prefix + fileName + suffix
    return newName

def checkFileName(self, fileName, case):
    checkFileName = True
#    print self.my_choice_rel_1 + " - " + self.my_choice_ref_1
#    newName1 = "__" + self.my_choice_rel_1 + "-"
#    nN = newName("__", self.my_choice_rel_1, "-")
#    print "<<<<<< : " + newName1 + " - " + fileName + " - " + nN

    if ( case == "rel" ):
        name = self.my_choice_rel_1
    elif ( case == "ref" ):
        name = self.my_choice_ref_1
    elif ( case == "FvsF" ):
        name = self.my_choice_rel_1
    else:
        name = self.my_choice_rel_1

    if ( re.search(str(newName("__", name, "-")), fileName) ):
        checkFileName = True
    else:
        checkFileName = False

    return checkFileName

def folderExtension_creation(self):
    extension = '_DQM_'
    if ( self.checkStdDev1.isChecked()  ):
        extension += 'std'
    else: # default suppose that self.checkStdDev2 is checked
        extension += 'dev'
    return extension

def folderSuffixe_creation(self):
    suffixe = ""
    if ( self.checkSpecTarget1.isChecked() ):
        suffixe = "RECO"
    if ( self.checkSpecTarget2.isChecked() ):
        suffixe = "PU25"
    if ( self.checkSpecTarget3.isChecked() ):
        suffixe = "PUpmx25"
    if ( self.checkSpecTarget4.isChecked() ):
        suffixe = "miniAOD"
    return
    
def getCheckedRadioButton(self):
    value = "FullvsFull"
    if self.radio11.isChecked():
        value = 'FullvsFull'
    elif self.radio12.isChecked():
        value = 'FastvsFast'
    elif self.radio13.isChecked():
        value = 'FastvsFull'
        
    return value
    
def getCheckedOptions(self):
    if self.radio11.isChecked():
        self.validationType1 = 'Full'
    elif self.radio12.isChecked():
        self.validationType1 = 'Fast'
    elif self.radio13.isChecked():
        self.validationType1 = 'FastFull'
        
    if self.checkSpecTarget1.isChecked():
        self.validationType2 = 'RECO'
    elif self.checkSpecTarget2.isChecked():
        self.validationType2 = 'PU25'
    elif self.checkSpecTarget3.isChecked():
        self.validationType2 = 'PUpmx25'
    elif self.checkSpecTarget4.isChecked():
        self.validationType2 = 'miniAOD'
    
    if self.checkSpecReference1.isChecked():
        self.validationType3 = 'RECO'
    elif self.checkSpecReference2.isChecked():
        self.validationType3 = 'PU25'
    elif self.checkSpecReference3.isChecked():
        self.validationType3 = 'PUpmx25'
    elif self.checkSpecReference4.isChecked():
        self.validationType3 = 'miniAOD'

    print "validationType1 : %s, validationType2 : %s, validationType3 : %s" % (self.validationType1, self.validationType2, self.validationType3)
    return
    
def updateLabelResumeSelected(self):
    selectedText = "<strong>"
    if self.radio11.isChecked(): # FULL vs FULL
        selectedText += "FULL vs FULL "
    elif self.radio12.isChecked(): # FAST vs FAST
        selectedText += "FAST vs FAST "
    elif self.radio13.isChecked(): # FAST vs FULL
        selectedText += "FAST vs FULL "
    else:
        print("Houston we have a pbm !!")
            
    selectedText += "Selected :</strong>"
    selectedText += "<table>"
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
            
    self.labelResumeSelected.setText(self.trUtf8(selectedText))
            
    return

def updateLabelResume(self):
    resume_text = self.texte
    resume_text += "<br />Release   : " + self.my_choice_rel_1
    resume_text += "<br />Reference : " + self.my_choice_ref_1
    resume_text += "<br />working dir release : " + str(self.working_dir_rel)
    if  ( self.exist_working_dir_rel ):
        resume_text += ' <b><font color=\'red\'>already created !</font></b>'
    resume_text += "<br />working dir reference : " + str(self.working_dir_ref)
    if  ( self.exist_working_dir_ref ):
        resume_text += ' <b><font color=\'red\'>already created !</font></b>'
    resume_text += '<br />resume folder : ' + str(self.finalFolder)
    if ( self.exist_finalFolder ):
        resume_text += ' <b><font color=\'blue\'>already created !</font></b>'
    
    self.LabelResume.setText(self.trUtf8(resume_text))   
    return

def changeRef2Tmp(self): # put ref into memory, and put ref == rel
    self.my_choice_tmp = self.my_choice_ref_1 # keep the chosen reference into memory
    self.releasesList_ref_2_tmp = self.releasesList_ref_2 # keep the reference root files list into memory
    self.ref_list_1_tmp = self.ref_list_1 # keep the reference datasets list into memory
    self.my_choice_ref_1 = self.my_choice_rel_1
    self.releasesList_ref_2 = self.releasesList_rel_2 # no need to recompute the list
    self.ref_list_1 = self.rel_list_1 # no need to recompute the list
    tmp = "Reference : " + self.my_choice_ref_1
    self.labelCombo2.setText(tmp)
    return
    
def changeTmp2Ref(self): # retrieve rel != ref
    if ( self.my_choice_tmp != "" ): # we have an old choice for reference
#        print "back to reference"
#        print "actual : " + self.my_choice_ref_1
#        print "native : " + self.my_choice_tmp
        self.wp.write("back to reference\n")
        self.wp.write("actual : %s\n" % self.my_choice_ref_1)
        self.wp.write("native : %s\n" % self.my_choice_tmp)
        self.textReport += "back to reference" + "<br>"
        self.textReport += "actual : " + self.my_choice_ref_1 + "<br>"
        self.textReport += "native : " + self.my_choice_tmp + "<br>"
        self.my_choice_ref_1 = self.my_choice_tmp # keep the reference back
        self.ref_list_1 = self.ref_list_1_tmp # keep the reference datasets list back
        self.releasesList_ref_2 = self.releasesList_ref_2_tmp # keep the reference root files list back
        self.my_choice_tmp = ""
        self.releasesList_ref_2_tmp = []
        self.ref_list_1_tmp = []
        tmp = "Reference : " + self.my_choice_ref_1
        self.labelCombo2.setText(tmp)
    return
    
    print "back to reference"
    print "actual : " + self.my_choice_ref_1
    print "native : " + self.my_choice_tmp
    self.wp.write("back to reference\n")
    self.wp.write("actual : %s\n" % self.my_choice_ref_1)
    self.wp.write("native : %s\n" % self.my_choice_tmp)
    self.textReport += "back to reference" + "<br>"
    self.textReport += "actual : " + self.my_choice_ref_1 + "<br>"
    self.textReport += "native : " + self.my_choice_tmp + "<br>"
    self.my_choice_ref_1 = self.my_choice_tmp # keep the reference back
    self.ref_list_1 = self.ref_list_1_tmp # keep the reference datasets list back
    self.releasesList_ref_2 = self.releasesList_ref_2_tmp # keep the reference root files list back
    self.my_choice_tmp = ""
    self.releasesList_ref_2_tmp = []
    self.ref_list_1_tmp = []
    tmp = "Reference : " + self.my_choice_ref_1
    self.labelCombo2.setText(tmp)
    return
    
