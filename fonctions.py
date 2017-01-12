#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re
from getEnv import env
from Paths_default import *

def cmd_folder_creation(choix_calcul, working_dir):
    import subprocess, os, datetime
    now = datetime.datetime.now()
    newDirName = now.strftime("%Y_%m_%d-%H%M%S")
#    print "Making directory " + newDirName
#    print "working dir : ", working_dir
    actual_dir = os.getcwd()
#    print "cmd_folder_creation - actual dir : ", actual_dir
    os.chdir(working_dir)
#    print "cmd_folder_creation - je suis en : ", os.getcwd()
    if ( ( choix_calcul == 'Full' ) or ( choix_calcul == 'gedvsgedFull'  )):
        newDirName = '/GED_' + newDirName
    elif ( choix_calcul == 'Fast' ):
        newDirName = '/FAST_' + newDirName
    elif ( choix_calcul == 'PileUp' ):
        newDirName = '/PU_' + newDirName
    
    m_dir = working_dir + newDirName
    os.makedirs(m_dir)
    tmp = m_dir
    
    os.chdir(actual_dir)
    return tmp

def cmd_working_dirs_creation(self):
#    print "cmd_working_dirs_creation"
    self.working_dir_rel = self.working_dir_base + '/' + str(self.lineedit1.text()[6:])
    self.working_dir_ref = self.working_dir_rel + '/' + str(self.lineedit3.text()[6:])
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
   
def get_choix_calcul(self):
    if self.radio11.isChecked(): # FULL
        self.choix_calcul = 'Full'
        self.choix_calcul = 'gedvsgedFull' # because radio04 is always checked
    if self.radio12.isChecked(): # PU
        self.choix_calcul = 'PileUp'
    if self.radio13.isChecked(): # FAST
        self.choix_calcul = 'Fast'
    return
    
def get_choix_calcul_search(self):
    if self.radio11.isChecked(): # FULL
        get_choix_calcul = 'Full'
    if self.radio12.isChecked(): # PU
        get_choix_calcul = 'PU'
    if self.radio13.isChecked(): # FAST
        get_choix_calcul = 'Fast'
    return get_choix_calcul
    
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
    
def auth_wget2(url, chunk_size=1048576):
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    """Returns the content of specified URL, which requires authentication.
    If the content is bigger than 1MB, then save it to file.
    """
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    opener = build_opener(X509CertOpen())
    url_file = opener.open(Request(url))
    size = int(url_file.headers["Content-Length"])

    if size < 1048576:   # if File size < 1MB
        filename = basename(url)    #still download
        readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
        if filename != '':
            outfile = open(filename, 'wb')  #then write File to local system
            outfile.write(readed)
        return readed

    filename = basename(url)

    if isfile("./%s" % filename):
        print '%s. Exists on disk. Skipping.' % (filename)
        return

    print ' Downloading... %s' % (filename)
    file = open(filename, 'wb')
    chunk = url_file.read(chunk_size)
    while chunk:
        file.write(chunk)
        chunk = url_file.read(chunk_size)
    print '%s.  Done.' % (filename)
    file.close()

def cmd_fetch(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run):
    # fetchall_from_DQM_v2.py -r CMSSW_7_0_0 -e='TTbar,PU,25' --mc --dry
    import re
    import sys
    import os

    from multiprocessing import Pool, Queue, Process
    from Queue import Empty
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    
#    print "\n CMD_FETCH : "
    cmsenv = env()
   
    ## Define options
#    option_is_from_data = "mc" # mc ou data
#    option_release = cmsenv.getCMSSWBASECMSSWVERSION()
#    option_regexp = 'TTbar,PU,25'
#    option_mthreads = 3
#    option_dry_run = True
#    print option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    def auth_wget(url, chunk_size=1048576):
        """Returns the content of specified URL, which requires authentication.
        If the content is bigger than 1MB, then save it to file.
        """
        opener = build_opener(X509CertOpen())
        url_file = opener.open(Request(url))
        size = int(url_file.headers["Content-Length"])

        if size < 1048576:   # if File size < 1MB
            filename = basename(url)    #still download
            readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
            if filename != '':
                outfile = open(filename, 'wb')  #then write File to local system
                outfile.write(readed)
            return readed

        filename = basename(url)
        file_id = selected_files.index(filename)

        if isfile("./%s" % filename):
            print '%d. Exists on disk. Skipping.' % (file_id +1)
            return

        print '%d. Downloading...' % (file_id +1)
        file = open(filename, 'wb')
        # progress = 0
        chunk = url_file.read(chunk_size)
        while chunk:
            file.write(chunk)
            # progress += chunk_size
            chunk = url_file.read(chunk_size)
        print 'cmd_fetch %d.  Done.' % (file_id +1)
        file.close()

    ## Use options
    relvaldir = "RelVal"
    if option_is_from_data == 'data':
        relvaldir = "RelValData"
#    print "relvaldir : ", relvaldir
    release = re.findall('(CMSSW_\d*_\d*_)\d*(?:_[\w\d]*)?', option_release)
#    print release
    if not release:
        parser.error('No such CMSSW release found. Please check the ``--release`` commandline option value.')
    releasedir = release[0] + "x"
#    print "releasedir : ", releasedir
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
    filedir_url = base_url + relvaldir + '/' + releasedir + '/'
#    print "AAAAAAA : ", filedir_url
    filedir_html = auth_wget(filedir_url)

    #auth_wget("https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2012/JetHT/0002029xx/DQM_V0001_R000202950__JetHT__Run2012C-PromptReco-v2__DQM.root")
    #auth_wget("https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelValData/CMSSW_5_3_x/DQM_V0001_R000205921__JetHT__CMSSW_5_3_3_patch1-PR_newconditions_RelVal_R205921_121105-v2__DQM.root")

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names
#    print "cmd_fetch : ", all_files

    ### Fetch the files, using multi-processing
    print "cmd_fetch : ", option_regexp.split(',') + [option_release]
    file_res = [re.compile(r) for r in option_regexp.split(',') + [option_release]]

    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]
#    print selected_files

    print 'Downloading files:'
    for i, name in enumerate(selected_files):
        print '%d. %s' % (i+1, name)
        
    if option_dry_run:
        print "cmd_fetch done"
        return selected_files
    if not option_dry_run:
        print '\nProgress:'
        pool = Pool(option_mthreads)
        pool.map(auth_wget2, [filedir_url + name for name in selected_files])
    
    return 

def list_search(self):
        
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = str(self.lineedit1.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_release_3 = str(self.lineedit3.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
    option_mthreads = 3
    option_dry_run = True # False for loading files
    self.gccs = get_choix_calcul_search(self) 
#    print "**********", "choix calcul : ", self.choix_calcul, self.gccs # to be removed
    
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

def list_search_0(self):
        
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

def cmd_fetch_0(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run):
    # fetchall_from_DQM_v2.py -r CMSSW_7_0_0 -e='TTbar,PU,25' --mc --dry
    import re
    import sys
    import os

    from multiprocessing import Pool, Queue, Process
    from Queue import Empty
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    
    cmsenv = env()
   
    ## Define options
#    option_is_from_data = "mc" 
#    option_release = cmsenv.getCMSSWBASECMSSWVERSION()
#    option_regexp = 'TTbar,PU,25'
#    option_mthreads = 3
#    option_dry_run = True
#    print option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    def auth_wget(url, chunk_size=1048576):
        """Returns the content of specified URL, which requires authentication.
        If the content is bigger than 1MB, then save it to file.
        """
        opener = build_opener(X509CertOpen())
        url_file = opener.open(Request(url))
        size = int(url_file.headers["Content-Length"])

        if size < 1048576:   # if File size < 1MB
            filename = basename(url)    #still download
            readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
            if filename != '':
                outfile = open(filename, 'wb')  #then write File to local system
                outfile.write(readed)
            return readed

        filename = basename(url)
        file_id = selected_files.index(filename)

        if isfile("./%s" % filename):
            print '%d. Exists on disk. Skipping.' % (file_id +1)
            return

        print '%d. Downloading...' % (file_id +1)
        file = open(filename, 'wb')
        # progress = 0
        chunk = url_file.read(chunk_size)
        while chunk:
            file.write(chunk)
            # progress += chunk_size
            chunk = url_file.read(chunk_size)
        print '%d.  Done.' % (file_id +1)
        file.close()

    ## Use options
    relvaldir = "RelVal"
    if option_is_from_data == 'data':
        relvaldir = "RelValData"
    release = re.findall('(CMSSW_\d*_\d*_)\d*(?:_[\w\d]*)?', option_release)
    if not release:
        parser.error('No such CMSSW release found. Please check the ``--release`` commandline option value.')
    releasedir = release[0] + "x"
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
    filedir_url = base_url + relvaldir + '/' # + releasedir + '/'
    filedir_html = auth_wget(filedir_url)

    #auth_wget("https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2012/JetHT/0002029xx/DQM_V0001_R000202950__JetHT__Run2012C-PromptReco-v2__DQM.root")
    #auth_wget("https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelValData/CMSSW_5_3_x/DQM_V0001_R000205921__JetHT__CMSSW_5_3_3_patch1-PR_newconditions_RelVal_R205921_121105-v2__DQM.root")

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names

    ### Fetch the files, using multi-processing
#    file_res = [re.compile(r) for r in option_regexp.split(',') + [option_release]]
    file_res = [re.compile(r) for r in option_regexp.split(',') ]

    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

    if option_dry_run:
#        print "done"
        return selected_files
    
    return 
    
def list_search_1(my_choice_0):
        
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

def cmd_fetch_1(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run):
    # fetchall_from_DQM_v2.py -r CMSSW_7_0_0 -e='TTbar,PU,25' --mc --dry
    import re
    import sys
    import os

    from multiprocessing import Pool, Queue, Process
    from Queue import Empty
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    
    cmsenv = env()
   
    ## Define options
#    option_is_from_data = "mc" 
#    option_release = cmsenv.getCMSSWBASECMSSWVERSION()
#    option_regexp = 'TTbar,PU,25'
#    option_mthreads = 3
#    option_dry_run = True
#    print option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

#    def auth_wget(url, chunk_size=1048576):
    def auth_wget(url, chunk_size=2097152):
        """Returns the content of specified URL, which requires authentication.
        If the content is bigger than 1MB, then save it to file.
        """
        # NOTE 2097152 is needed because CMSSW_7_1_X > 1 MB
        opener = build_opener(X509CertOpen())
        url_file = opener.open(Request(url))
        size = int(url_file.headers["Content-Length"])

#        if size < 1048576:   # if File size < 1MB
        if size < 2097152:   # if File size < 2MB
            filename = basename(url)    #still download
            readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
            if filename != '':
                outfile = open(filename, 'wb')  #then write File to local system
                outfile.write(readed)
            return readed

        filename = basename(url)
        file_id = selected_files.index(filename)

#        if isfile("./%s" % filename):
#            print '%d. Exists on disk. Skipping.' % (file_id +1)
#            return

        print '%d. Downloading...'  % (file_id +1)
        file = open(filename, 'wb')
        # progress = 0
        chunk = url_file.read(chunk_size)
        while chunk:
            file.write(chunk)
            # progress += chunk_size
            chunk = url_file.read(chunk_size)
        print '%d.  Done.'  % (file_id +1)
        file.close()

    ## Use options
    relvaldir = "RelVal"
    if option_is_from_data == 'data':
        relvaldir = "RelValData"
    release = re.findall('(CMSSW_\d*_\d*_)\d*(?:_[\w\d]*)?', option_release)
    if not release:
        parser.error('No such CMSSW release found. Please check the ``--release`` commandline option value.')
    releasedir = release[0] + "x"
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
    filedir_url = base_url + relvaldir + '/'  + releasedir + '/'
    filedir_html = auth_wget(filedir_url)

    #auth_wget("https://cmsweb.cern.ch/dqm/offline/data/browse/ROOT/OfflineData/Run2012/JetHT/0002029xx/DQM_V0001_R000202950__JetHT__Run2012C-PromptReco-v2__DQM.root")
    #auth_wget("https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelValData/CMSSW_5_3_x/DQM_V0001_R000205921__JetHT__CMSSW_5_3_3_patch1-PR_newconditions_RelVal_R205921_121105-v2__DQM.root")

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names

    ### Fetch the files, using multi-processing
#    file_res = [re.compile(r) for r in option_regexp.split(',') + [option_release]]
    file_res = [re.compile(r) for r in option_regexp.split(',') ]

    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

    if option_dry_run:
#        print "done"
        return selected_files
    
    return 
    
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
    print "sub_releases2", len(tab_files)
    i = 0
    temp = []
    for t in tab_files:
        if ( re.search(release, t) ):
#            print 'sub_releases2 : %s' % t
            tt = explode_item(t)
            print 'sub_releases2 : %d, %s, %s' % (i+1, tt[0], tt[1])
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
