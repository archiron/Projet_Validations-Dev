#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re
from getEnv import env
from Paths_default import *
from functions import clean_collections2 # 

def auth_wget2(url, chunk_size=2097152):
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

#    print "auth_wget2 : url= ", url
    
    opener = build_opener(X509CertOpen())
    url_file = opener.open(Request(url))
    size = int(url_file.headers["Content-Length"])

    if size < 2097152:   # if File size < 1MB
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

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names

    ### Fetch the files, using multi-processing
    file_res = [re.compile(r) for r in option_regexp.split(',') ]

    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

    if option_dry_run:
#        print "done"
        return selected_files
    
    return 
    
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
    
    releasedir = option_release
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
    filedir_url = base_url + relvaldir + '/'  + releasedir + '/'
    filedir_html = auth_wget(filedir_url)

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names

    ### Fetch the files, using multi-processing
    file_res = [re.compile(r) for r in option_regexp.split(',') ]

    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

    if option_dry_run:
#        print "done"
        return selected_files
    
    return 
    
def cmd_load_files(self):
    import re
    import sys
    import os

    from multiprocessing import Pool, Queue, Process
    from Queue import Empty
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    
    print "\n cmd_load_files : "
    self.wp.write("cmd_load_files : \n")
    cmsenv = env()
   
#    print " self.validationType1 = ",  self.validationType1 # temp
#    print " self.validationType2 = ",  self.validationType2 # temp
#    print " self.validationType3 = ",  self.validationType3 # temp
    validationType_2 = self.validationType2
    validationType_3 = self.validationType3
    temp_toBeRemoved = []

    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_mthreads = 3
#    option_dry_run = False # False telecharge , True liste
        
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    ## Use options
    relvaldir = "RelVal"
    if option_is_from_data == 'data':
        relvaldir = "RelValData"
    
    ## MUST TEST IF ARRAYS ARE NOT EMPTY
    
    #case 1 self.my_choice_rel_0 : RELEASE
    print "case 1 self.my_choice_rel_0 : RELEASE"
    filedir_url = BaseURL(self) + relvaldir + '/' + self.my_choice_rel_0 + '/'
    for line in self.releasesList_rel_5:
        if not clean_collections2(line, self.validationType1, validationType_2, validationType_3, "rel"):
            #print filedir_url + line + " removed"
            temp_toBeRemoved.append(line)
    for line in temp_toBeRemoved:
        self.releasesList_rel_5.remove(line)
    os.chdir(self.working_dir_rel)   # Change current working directory to release directory
    pool = Pool(option_mthreads)
    pool.map(auth_wget2, [str(filedir_url) + name for name in self.releasesList_rel_5])

    #case 2 self.my_choice_ref_0 : REFERENCE
    temp_toBeRemoved[:] = []# clear the temp array
    print "case 2 self.my_choice_ref_0 : REFERENCE"
    filedir_url = BaseURL(self) + relvaldir + '/' + self.my_choice_ref_0 + '/'
    for line in self.releasesList_ref_5:
        if not clean_collections2(line, self.validationType1, validationType_2, validationType_3, "ref"):
            #print filedir_url + line + " removed"
            temp_toBeRemoved.append(line)
    for line in temp_toBeRemoved:
        self.releasesList_ref_5.remove(line)
    os.chdir(self.working_dir_ref)   # Change current working directory to release directory
    pool = Pool(option_mthreads) # need to be here. If not, download is made into previous folder (i.e. self.working_dir_rel).
    pool.map(auth_wget2, [str(filedir_url) + name for name in self.releasesList_ref_5])
    

    return