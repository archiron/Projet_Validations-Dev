#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re
from getEnv import env
from Paths_default import *

def folder_creation(self):
    import subprocess, os, datetime
    now = datetime.datetime.now()
    newDirName = now.strftime("%Y_%m_%d-%H%M%S")

    actual_dir = os.getcwd()
    fieldname = self.validationType1 + "_"
    fieldname = fieldname + self.validationType2
    fieldname = fieldname + "_" + now.strftime("%Y_%m_%d-%H%M%S")
    print("fieldname : %s") % fieldname
    self.wp.write("fieldname : %s\n" % fieldname)
    
    m_dir = self.working_dir_rel + "/" + fieldname
    self.wp.write("m_dir : %s\n" % m_dir)
    os.chdir(self.working_dir_rel)
    os.makedirs(m_dir)
    
    os.chdir(actual_dir)
    return # m_dir

def finalFolder_creation(self):
#    print "cmd_working_dirs_creation"
    if not os.path.exists(self.finalFolder):
        os.makedirs(str(self.finalFolder))
    return
    
def working_dirs_creation(self): # working dir are for resuming the computation.
#    print "cmd_working_dirs_creation"
    self.working_dir_rel = self.working_dir_base + '/' + str(self.my_choice_rel_1) # self.lineedit1.text()[6:]
    self.working_dir_ref = self.working_dir_rel + '/' + str(self.my_choice_ref_1) # self.lineedit3.text()[6:]
    self.wp.write("self.working_dir_rel : %s\n" % self.working_dir_rel)
    self.wp.write("self.working_dir_ref : %s\n" % self.working_dir_ref)
    
    if not os.path.exists(self.working_dir_rel):
        os.chdir(self.working_dir_base) # going to base folder
        print "Creation of (%s) folder" % str(self.working_dir_rel)
        os.makedirs(str(self.working_dir_rel))
    os.chdir(self.working_dir_rel)   # Change current working directory
    if not os.path.exists(self.working_dir_ref):
        print "Creation of (%s) folder" % str(self.working_dir_ref)
        os.makedirs(str(self.working_dir_ref))

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
   
def get_validationType1(self):
    if self.radio11.isChecked(): # FULL
        self.validationType = 'Full'
        self.validationType = 'gedvsgedFull' # because radio04 is always checked
    if self.radio12.isChecked(): # FAST
        self.validationType = 'Fast'
    return
    
def get_validationType1_search(self):
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
            if ( re.search('PU', items) ):
                print " PU exist in Full", items # to be removed
            elif ( re.search('Fast', items) ):
                print " Fast exist in Full", items # to be removed
            else:
                temp.append(items)
        elif ( gccs == 'PU' ):
            if ( re.search('Fast', items) ):
                print " Fast exist in PU", items # to be removed
                temp.append(items) # TEMP. To be removed
            else:
                temp.append(items)
        else: # gccs == 'FAST'
            if ( re.search('PU', items) ):
                print " PU exist in Fast", items # to be removed
            else:
                temp.append(items)
    return temp

def clean_collections2(collectionItem, validationType_1, validationType_2, validationType_3):
    import re
    temp = True
    if ( validationType_1 == 'Full' ): # does not take into account miniAOD
        if ( re.search('Fast', collectionItem) ):
            print " Fast exist in Full", collectionItem # to be removed
            temp = False
        else: # all Full + PU + pmx + miniAOD
            temp= True # temporaire
            if ( ( validationType_2 == 'RECO' ) or ( validationType_2 == 'miniAOD' ) ):
                if ( re.search('PU', collectionItem) ):
                    temp = False
            elif ( ( validationType_2 == 'PU' )): 
                if ( re.search('PU', collectionItem) ):
                    print " PU ask for PU", collectionItem # to be removed
                    if ( re.search('pmx', collectionItem) ):
                        temp = False
                    else:
                        temp = True
                else:
                    temp = False
            elif ( validationType_2 == 'pmx' ):
                if ( re.search('pmx', collectionItem) ):
                    print " pmx ask for pmx", collectionItem # to be removed
                    temp = True
                elif ( re.search('PU', collectionItem) and ( validationType_3 == 'global' ) ):
                    temp = True
                else:
                    temp = False
    else: # validationType_1 == 'FAST', does not take into account PU & Fast
        if ( re.search('Fast', collectionItem) ): #  match Fast all Fast + PU + pmx + miniAOD
            print " Fast added", collectionItem # to be removed
            temp = True # Temporaire
            if ( ( validationType_2 == 'RECO' ) or ( validationType_2 == 'miniAOD' ) ):
                if ( re.search('PU', collectionItem) ):
                    temp = False
            elif ( validationType_2 == 'PU' ):
                if ( re.search('PU', collectionItem) ):
                    print " PU ask for PU", collectionItem # to be removed
                    if ( re.search('pmx', collectionItem) ):
                        temp = False
                    else:
                        temp = True
                else:
                    temp = False
            elif ( validationType_2 == 'pmx' ):
                if ( re.search('pmx', collectionItem) ):
                    print " pmx ask for pmx", collectionItem # to be removed
                    temp = True
                elif ( re.search('PU', collectionItem) and ( validationType_3 == 'global' ) ):
                    temp = True
                else:
                    temp = False
        else:
            temp = False
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
#    print "lg temp : ", len(temp_1)
    return temp_1
    
def list_search_4(collection, filtre, validationType_1, validationType_2):
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
    temp_56 = []
    temp_FastvsFull = []
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
                if clean_collections2(item1, self.validationType1, validationType_2, validationType_3):
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
    if ( validationType_2 == 'miniAOD' ):
        temp_3 = temp_1
        temp_4 = temp_2
    else:
        for item1 in self.releasesList_ref_2:
            for item2 in filtre:
                if re.search(item2, item1):
                    if clean_collections2(item1, self.validationType1, validationType_2, validationType_3):
                        temp_34.append([explode_item(item1)[2], item2])
                    break
    
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
    
    # FAST vs FULL TREATMENT
#    if ( self.validationType1 == "Fast" and self.validationType2 == "RECO" ): # FAST vs FULL TREATMENT
    self.releasesList_rel_4 = []
    self.releasesList_rel_4b = []
    if ( checkFastvsFull(self) ):
        print "Fast vs Full treatment :"
        for item1 in self.releasesList_rel_2:
            for item2 in filtre:
                if re.search(item2, item1):
                    if clean_collections2(item1, "Full", validationType_2, validationType_3):
                        temp_56.append([explode_item(item1)[2], item2])
                        print "len = %i" % len(temp_56)
                    break

        print "len of temp_56 = %i." % len(temp_56)
        if ( len(temp_56) > 0 ):
            #print "temp_56 : ", temp_56
            temp_56.sort()

            temp_FastvsFull.append( [temp_56[0][0], temp_56[0][1]] )
            k = 0
            for i in range(1, len(temp_56)):
                if ( temp_56[i][0] == temp_FastvsFull[k][0] ):
                    temp_FastvsFull[k][1] += ', ' + temp_56[i][1]
                else:
                    k +=1
                    temp_FastvsFull.append( [temp_56[i][0], temp_56[i][1]] )
        
        for i in range(0, len(temp_FastvsFull)):
            self.releasesList_rel_4.append(temp_FastvsFull[i][1])
            self.releasesList_rel_4b.append(temp_FastvsFull[i][0])

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

        f.write("\n" + "self.releasesList_rel_4b" + "\n")
        self.wp.write("\n" + "self.releasesList_rel_4b" + "\n")
        for line in self.releasesList_rel_4b:
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

        f.write("\n" + "self.releasesList_FvsF_5" + "\n")
        self.wp.write("\n" + "self.releasesList_FvsF_5" + "\n")
        for line in self.releasesList_FvsF_5:
            f.write(line + "\n") # write the line
            self.wp.write(line + "\n") # write the line
        f.close()
    return

def checkFastvsFull(self):
    if ( self.radio12.isChecked() and self.radio21.isChecked() ):
    # check for FastvsFull for Fast and RECO.
    # if you want to use it also for PU you have to modify the previous test
        self.checkFastvsFull = True
    else:
        self.checkFastvsFull = False
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

def checkCalculValidation(self, fileName):
#Full, RECO    : (not PU) and (not Fast)
#Full, PU      : PU and (not Fast)
#Full, pmx     : pmx and (not Fast) for rel, PU and (not Fast) for rel
#Full, miniAOD : idem Full, RECO

#Fast, RECO    : Fast and (not PU)
    
    checkCalculValidation = True
    if ( self.radio11.isChecked() and self.radio21.isChecked() ): #Full, RECO
#        print ">>>>>>>> Full, RECO"
        if ( re.search("PU", fileName) or re.search("Fast", fileName) ):
#            print ">>>> PU, Fast : " + fileName
            checkCalculValidation = False
    if ( self.radio11.isChecked() and self.radio22.isChecked() ): #Full, PU
        print ">>>>>>>> Full, PU"
    return checkCalculValidation

def extractDatasets(self):
    extraction = ""
    extractionDisplay = ""
    # display of the datasets strings
    print "datasets release   : ", self.selectedRelDatasets
    print "datasets reference : ", self.selectedRefDatasets
    # cutting self.selectedRelDatasets
    cuttedRelease = str(self.selectedRelDatasets).split(',')
    print "cuttedRelease : ", cuttedRelease
    # searching in self.selectedRefDatasets
    for elem in cuttedRelease:
        print elem
        if re.search(elem, self.selectedRefDatasets):
            print "OK"
            extraction += ', ' + elem
            extractionDisplay += ', ' + "<font color = \"blue\">" + elem + "</font>"
        else:
            print "KO"
            extractionDisplay += ', ' + elem

    extraction = extraction[2:]
    extractionDisplay = extractionDisplay[2:]
    
    return extraction, extractionDisplay
    
def extractDatasetsFastvsFull(self): # do not verify if checkFastvsFull(self) !! MUST be called inside a if(checkFastvsFull(self)): !!
    extractionFastvsFull = ""
    extractionFastvsFullDisplay = ""
    # display of the datasets strings
    print "datasets release   : ", self.selectedRelDatasets
    print "datasets reference : ", self.selectedFvsFDatasets
    # cutting self.selectedRelDatasets
    cuttedRelease = str(self.selectedRelDatasets).split(',')
    print "cuttedRelease : ", cuttedRelease
    # searching in self.selectedFvsFDatasets
    for elem in cuttedRelease:
        print elem
        if re.search(elem, self.selectedFvsFDatasets):
            print "OK"
            extractionFastvsFull += ', ' + elem
            extractionFastvsFullDisplay += ', ' + "<font color = \"blue\">" + elem + "</font>"
        else:
            print "KO"
            extractionFastvsFullDisplay += ', ' + elem
    
    extractionFastvsFull = extractionFastvsFull[2:]
    extractionFastvsFullDisplay = extractionFastvsFullDisplay[2:]
    
    return extractionFastvsFull, extractionFastvsFullDisplay
 