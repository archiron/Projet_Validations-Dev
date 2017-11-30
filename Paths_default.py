#! /usr/bin/env python
#-*-coding: utf-8 -*-


def BaseURL(self):
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
    return base_url
    
def LocationFilter(self):
    import sys

    table=getattr(sys.modules[__name__], "DataLocation")(self)   
    return table

def DataLocation(self):
    print "Location"
    table=[
    ["Local", 1],
    ["Remote afs", 0],
    ["Remote eos", 0],
    ]
    return table

def localLocation(self):
    import os
    localLocation = os.getcwd()
    return localLocation
