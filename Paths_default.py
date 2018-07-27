#! /usr/bin/env python
#-*-coding: utf-8 -*-


def BaseURL(self):
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
    return base_url
    
def LocationFilter(self):
    import sys

    table=getattr(sys.modules[__name__], "DataLocation")(self)   
    return table

def localLocation(self):
    import os
    localLocation = os.getcwd()
    return localLocation

def DataLocation(self):
    '''
    WARNING : if you add/remove a line for a path
    DO NOT FORGET to update the pathToURL() function below.
    '''
    table=[
    ["Local", 1, str(localLocation(self))],
    ["Remote afs dev", 0, '/afs/cern.ch/cms/Physics/egamma/www/validation/Electrons/Dev/'],
    ["Remote afs std", 0, '/afs/cern.ch/cms/Physics/egamma/www/validation/Electrons/Releases/'],
    ["Remote eos dev", 0, '/eos/project/c/cmsweb/www/egamma/validation/Electrons/Dev/'],
    ["Remote eos std", 0, '/eos/project/c/cmsweb/www/egamma/validation/Electrons/Releases/'],
    ]
    return table

def pathToURL(self):
    table=[
    ['/afs/cern.ch/cms/Physics/egamma/www/validation/Electrons/Dev/', 'http://cmsdoc.cern.ch/cms/Physics/egamma/www/validation/Electrons/Dev/'],
    ['/afs/cern.ch/cms/Physics/egamma/www/validation/Electrons/Releases/', 'http://cmsdoc.cern.ch/cms/Physics/egamma/www/validation/Electrons/Releases/'],
    ['/eos/project/c/cmsweb/www/egamma/validation/Electrons/Dev/', 'http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/Dev/'],
    ['/eos/project/c/cmsweb/www/egamma/validation/Electrons/Releases/', 'http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/Releases/'],
    ]
    return table
 
 