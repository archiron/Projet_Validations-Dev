#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import urllib2

class env:
    def __init__(self): 
        self.CMSSWBASE = os.environ['CMSSW_BASE'] # donne le repertoire de travail
        self.CMSSWBASECMSSWRELEASEBASE = os.environ['CMSSW_RELEASE_BASE'] # donne la release et l'architecture
        self.CMSSWBASECMSSWVERSION = os.environ['CMSSW_VERSION'] # donne la release (CMSSW_7_1_0 par exemple)

    def getCMSSWBASE(self):
        CMSSWBASE = os.environ['CMSSW_BASE']
        return CMSSWBASE
		
    def getCMSSWBASECMSSWRELEASEBASE(self):
        return self.CMSSWBASECMSSWRELEASEBASE
		
    def getCMSSWBASECMSSWVERSION(self):
        return self.CMSSWBASECMSSWVERSION
		
    def cmsAll(self):
        cmsAll="<strong>CMSSW_BASE</strong> : " + self.getCMSSWBASE()
        cmsAll+="<br /><strong>CMSSW_RELEASE_BASE</strong> : " + self.getCMSSWBASECMSSWRELEASEBASE()
        cmsAll+="<br /><strong>CMSSW_VERSION</strong> : " + self.getCMSSWBASECMSSWVERSION()
        return cmsAll

