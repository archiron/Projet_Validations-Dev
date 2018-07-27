#! /usr/bin/env python
#-*-coding: utf-8 -*-

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

import os,sys,subprocess, shutil
import urllib2
import re
from PyQt4 import QtCore
from getEnv import env
from Paths_default import *
from Datasets_default import extractDatasets, extractDatasetsFastvsFull, testForDataSetsFile # DataSetsFilter, checkCalculValidation, 
from electronCompare import *

from ROOT import TCanvas

def working_dirs_creation(self): # working dir are for resuming the computation. Used for root files loading.
    import errno
    self.working_dir_rel = self.working_dir_base + '/' + str(self.my_choice_rel_1[6:]) # self.lineedit1.text()[6:]
    self.working_dir_ref = self.working_dir_rel + '/' + str(self.my_choice_ref_1[6:]) # self.lineedit3.text()[6:]
    self.wp.write("self.working_dir_rel : %s\n" % self.working_dir_rel)
    self.wp.write("self.working_dir_ref : %s\n" % self.working_dir_ref)
    self.textReport += "self.working_dir_rel : " + self.working_dir_rel + "<br>"
    self.textReport += "self.working_dir_ref : " + self.working_dir_ref + "<br>"
    
    if not os.path.exists(self.working_dir_rel):
        os.chdir(self.working_dir_base) # going to base folder
        try:
            os.makedirs(str(self.working_dir_rel))
        except OSError as e:
            if e.errno != errno.EEXIST: # the folder did not exist
                raise  # raises the error again
        self.wp.write("Creation of %s release folder\n" % str(self.working_dir_rel))
        self.textReport += "Creation of " + str(self.working_dir_rel) + " folder" + "<br>"
        self.exist_working_dir_rel = False
    else:
        self.wp.write("release folder %s already created\n" % str(self.working_dir_rel))
        self.textReport += "release folder " + str(self.working_dir_rel) + " already created" + "<br>"
        self.exist_working_dir_rel = True
    os.chdir(self.working_dir_rel)   # Change current working directory
    if not os.path.exists(self.working_dir_ref):
        try:
            os.makedirs(str(self.working_dir_ref))
        except OSError as e:
            if e.errno != errno.EEXIST: # the folder did not exist
                raise  # raises the error again
        self.wp.write("Creation of %s reference folder\n" % str(self.working_dir_ref))
        self.textReport += "Creation of " + str(self.working_dir_ref) + " reference folder" + "<br>"
        self.exist_working_dir_ref = False
    else:
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
    self.wp.write("fieldname : %s\n" % fieldname)
    self.textReport += "fieldname : " + fieldname + "<br>"
    
    m_dir = self.working_dir_rel + "/" + fieldname
    self.wp.write("m_dir : %s\n" % m_dir)
    self.textReport += "m_dir : " + m_dir + "<br>"
    self.working_dir_report = self.working_dir_rel + "/" + fieldname
    os.chdir(self.working_dir_rel) # going into release dir
    if not os.path.exists(m_dir): # 
        os.makedirs(m_dir) # create reference folder
        self.wp.write("creating : %s folder\n" % m_dir)
        self.textReport += "creating : " + m_dir + " folder" + "<br>"
    else:
        self.wp.write("%s already created\n" % m_dir)
        self.textReport += m_dir + " already created" + "<br>"
    os.chdir(actual_dir)
               
    return 

def finalFolder_creation(self):
    check_finalFolder(self)
    if self.exist_finalFolder: # True
        self.wp.write("%s already created\n" % str(self.finalFolder))
        self.textReport += "final folder " + str(self.finalFolder) + " already created" + "<br>"
    else: # False
        os.makedirs(str(self.finalFolder))
    updateLabelResume(self)
    return
    
def dataSets_finalFolder_creation(self):
    actual_dir = os.getcwd()
    os.chdir(self.finalFolder) # going into finalFolder
    # create datasets folders
    selectedText = self.labelResumeSelected.text() # ""
    report_name = self.working_dir_report + '/report.olog'
    wr = open(report_name, 'w') # report page
    wr.write("Validation report : \n")
    
    for i, elt in enumerate(self.finalList):
        wr.write("\ndataset=%s\n" % elt[0])
        dts = elt[0]
        # do something with self.labelResumeSelected.setText(self.trUtf8(selectedText))
        selectedText += "<strong>" + dts
        self.labelResumeSelected.setText(self.trUtf8(selectedText))
        QtCore.QCoreApplication.processEvents()
        
        dataSetFolder = str(self.validationType2 + '-' + self.validationType3 + '_' + dts)
#        print("\ndataset = %s" % elt[0])
#        print("finalFolder = %s" % self.finalFolder)
#        print("dataSetFolder = %s" % dataSetFolder)
        if not os.path.exists(dataSetFolder): # create dataSetFolder
            wr.write("%s does not exist. Creating it\n" % dataSetFolder)
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
            wr.write("%s already created\n" % dataSetFolder)
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
        [it1, it2, tp_1, tp_2] = testForDataSetsFile(self, dts)
        self.wp.write("config file for target : %s \n" % it1)
        self.wp.write("config file for reference : %s \n" % it2)
        wr.write("config file for target : %s \n" % it1)
        wr.write("config file for reference : %s \n" % it2)
        self.textReport += "config file for target : " + it1 + "<br>"
        self.textReport += "config file for reference : " + it2 + "<br>"
        self.wp.write("tree path for target : %s \n" % tp_1)
        self.wp.write("tree path for reference : %s \n" % tp_2)
        wr.write("tree path for target : %s \n" % tp_1)
        wr.write("tree path for reference : %s \n" % tp_2)
        self.textReport += "tree path for target : " + tp_1 + "<br>"
        self.textReport += "tree path for reference : " + tp_2 + "<br>"
        
        shutil.copy2(it1, 'config_target.txt')
        shutil.copy2(it2, 'config_reference.txt')
        # create gifs pictures & web page
        
        CMP_CONFIG = 'config_target.txt'
        CMP_TITLE = 'gedGsfElectrons ' + dts
        CMP_RED_FILE = self.my_choice_rel_1
        CMP_BLUE_FILE = self.my_choice_ref_1
        image_up = "http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/up.gif"
        image_point = "http://cms-egamma.web.cern.ch/cms-egamma/validation/Electrons/img/point.gif"
       
        f = open(CMP_CONFIG, 'r')
        input_rel_file = self.working_dir_rel + '/' + elt[1]
        f_rel = ROOT.TFile(input_rel_file)
        h1 = getHisto(f_rel, tp_1)

        input_ref_file = self.working_dir_ref + '/' + elt[2]
        f_ref = ROOT.TFile(input_ref_file)
        h2 = getHisto(f_ref, tp_2)
        wr.write("CMP_CONFIG = %s\n" % CMP_CONFIG)
        wr.write("input_rel_file = %s\n" % input_rel_file)
        wr.write("input_ref_file = %s\n" % input_ref_file)

        wp = open('index.html', 'w') # web page
        wp.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
        wp.write("<html>\n")
        wp.write("<head>\n")
        wp.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
        wp.write("<title> " + CMP_TITLE + " </title>\n") #option -t dans OvalFile
        wp.write("</head>\n")
        wp.write("<a NAME=\"TOP\"></a>")
        wp.write("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"../../../../img/up.gif\" alt=\"Up\"/></a>&nbsp; " + CMP_TITLE + " </h1>\n" ) # option -t dans OvalFile
        
        wp.write("<b><font color='red'> " + self.validationType2 + " " + self.my_choice_rel_1 + " </font></b>")
        wp.write(" : " + self.selectedRelGlobalTag )
        wp.write(" : " + elt[1] )
        wp.write("<br>\n")
        wp.write("<b><font color='blue'> " + self.validationType3 + " " + self.my_choice_ref_1 + " </font></b>")
        wp.write(" : " + self.selectedRefGlobalTag )
        wp.write(" : " + elt[2] )
        wp.write("<br>\n")
        
        if (f_ref == 0):
            wp.write("<p>In all plots below, there was no reference histograms to compare with")
            wp.write(", and the " + CMP_RED_FILE + " histograms are in red.") # new release red in OvalFile
        else:
            wp.write("<p>In all plots below")
            wp.write(", the <b><font color='red'> " + CMP_RED_FILE + " </font></b> histograms are in red") # new release red in OvalFile
            wp.write(", and the <b><font color='blue'> " + CMP_BLUE_FILE + " </font></b> histograms are in blue.") # ref release blue in OvalFile
        wp.write(" Some more details") # 
        wp.write(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms") # .txt file
        wp.write(", <a href=\"gifs/\">images</a> of histograms" + "." ) # 
        wp.write("</p>\n")

        # remplissage tableau titres et dict
        histoArray_0 = {}
        titlesList = [] # need with python < 3.7. dict does not keep the corrrect order of the datasets histograms
        key = ""
        tmp = []
        for line in f:
            if ( len(line) == 1 ): # len == 0, empty line
                if ( ( len(key) != 0 ) and ( len(tmp) != 0) ): 
                    histoArray_0[key] = tmp
                    key = ""
                    tmp = []
            else: # len <> 0
                if ( len(key) == 0 ):
                    key = line # get title
                    titlesList.append(line)
                else:
                    tmp.append(line) # histo name
                    t1 = line.split("/")
                    t2 = str(t1[1])
                    short_positions = t2.split()
                    if ( short_positions[3] == '1' ): # be careful it is '1' and not 1 (without quote)
                        tmp.append("endLine")

        # fin remplissage tableau titres et dict
        f.close()
        wp.write( "<table border=\"1\" cellpadding=\"5\" width=\"100%\">" )
        
        for i in range(0, len(titlesList)):
            if ( i % 5  == 0 ):
                wp.write( "\n<tr valign=\"top\">" )
            textToWrite = ""
            wp.write( "\n<td width=\"10\">\n<b> " + titlesList[i] + "</b>" )
            titles = titlesList[i].split() # explode(" ", $clefs[$i])
            if len(titles) > 1 :
                titleShortName = titles[0] + "_" + titles[1]
            else:
                titleShortName = titles[0]
            wp.write( "&nbsp;&nbsp;" + "<a href=\"#" + titleShortName + "\">" ) # write group title
            wp.write( "<img width=\"18\" height=\"15\" border=\"0\" align=\"center\" src=" + image_point + " alt=\"Top\"/>" + "<br><br>" )
            textToWrite += "</a>"
            histoPrevious = ""
            numLine = 0
            
            for elem in histoArray_0[titlesList[i]]:
                otherTextToWrite = ""
                
                if ( elem == "endLine" ): 
                    otherTextToWrite += "<br>"
                else: # no endLine
                    histo_names = elem.split("/")
                    histo_name = histo_names[0]
                    histoShortNames = histo_names[1]
                    histo_pos = histoShortNames
                    histo_positions = histo_pos.split()
                    short_histo_names = histoShortNames.split(" ")
                    short_histo_name = short_histo_names[0].replace("h_", "")
                    if "ele_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("ele_", "")
                    if "scl_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("scl_", "")
                    if "bcl_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("bcl_", "")
                    [after, before, common] = testExtension(short_histo_name, histoPrevious, self)
                    
                    if ( histo_positions[3] == "0" ):
                        if ( numLine == 0 ):
                            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=\'green\'>" + short_histo_name + "</font></a>" + "&nbsp;\n"
                            common = short_histo_name
                            numLine += 1
                        else: # $numLine > 0
                            if ( after == "" ):
                                otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=green>" + before + "</font></a>" + "&nbsp;\n"
                            else: # $after != ""
                                otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=green>" + after + "</font></a>" + "&nbsp;\n"
                            common = before
                    else: # histo_positions[3] == "1"
                        if ( numLine == 0 ):
                            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=grey>" + short_histo_name + "</font></a>" + "&nbsp;\n"
                            common = short_histo_name
                        else: # $numLine > 0
                            if ( after == "" ):
                                otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=blue>" + before + "</font></a>" + "&nbsp;\n"
                            else: # after != ""
                                otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=blue>" + after + "</font></a>" + "&nbsp;\n"
                        numLine = 0
                    
                    histoPrevious = common
                    if ( histo_positions[4] == "1" ):
                        otherTextToWrite += "<br>"
                    otherTextToWrite = otherTextToWrite.replace("<br><br>", "<br>")
                textToWrite += otherTextToWrite
            textReplace = True
            while textReplace :
                textToWrite = textToWrite.replace("<br><br>", "<br>")
                if ( textToWrite.count('<br><br>') >= 1 ):
                    textReplace = True
                else:
                    textReplace = False
            if ( textToWrite.count("</a><br><a") >= 1 ):
                    textToWrite = textToWrite.replace("</a><br><a", "</a><a")
            wp.write( textToWrite )
                    
            wp.write( "</td>" )
            if ( i % 5 == 4 ):
                wp.write( "</tr>" )
        
        wp.write( "</table>\n" )
        wp.write( "<br>" )
        
        lineFlag = True
        wp.write( "<table border=\"0\" cellpadding=\"5\" width=\"100%\">" )
        for i in range(0, len(titlesList)):
            wp.write( "\n<tr valign=\"top\">" )
            wp.write( "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + image_up + " alt=\"Top\"/></a></td>\n" )
            titles = titlesList[i].split()
            if len(titles) > 1 :
                titleShortName = titles[0] + "_" + titles[1]
            else:
                titleShortName = titles[0]
            wp.write( "\n<td>\n<b> " )
            wp.write( "<a id=\"" + titleShortName + "\" name=\"" + titleShortName + "\"></a>" )
            wp.write( titlesList[i] + "</b></td>" )
            wp.write( "</tr><tr valign=\"top\">" )
            for elem in histoArray_0[titlesList[i]]:
                if ( elem != "endLine" ): 
                    histo_names = elem.split("/")
                    histo_name = histo_names[0]
                    histoShortNames = histo_names[1]
                    histo_pos = histoShortNames
                    histo_positions = histo_pos.split()
                    short_histo_names = histoShortNames.split(" ")
                    short_histo_name = short_histo_names[0].replace("h_", "")
                    if "ele_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("ele_", "")
                    if "scl_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("scl_", "")
                    if "bcl_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("bcl_", "") # ARRET
                    gif_name = "gifs/" + short_histo_names[0] + ".gif"
                    histo_name_recomp = short_histo_names[0]
                    histo_2 = h2.Get(short_histo_names[0]) #  
                    if checkRecompInName(histo_name_recomp): # 
                        short_histo_names[0] = histo_name_recomp.replace("_recomp", "")
                        gif_name = "gifs/" + short_histo_names[0] + "_recomp.gif"
                    
                    histo_1 = h1.Get(short_histo_names[0]) #  
                    if checkRecompInName(histo_name_recomp) and self.checkSpecTarget1.isChecked(): # RECO vs miniAOD. For miniAOD vs miniAOD, we do not do this.
                        # we inverse histo1 & histo2 in order to keep the term "recomputed" into the title.
                        PictureChoice(histo_2, histo_1, histo_positions[1], histo_positions[2], gif_name, self)
                    else:
                        PictureChoice(histo_1, histo_2, histo_positions[1], histo_positions[2], gif_name, self)
                    
                    if ( lineFlag ):
                        wp.write( "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + image_up + " alt=\"Top\"/></a></td>\n" )
                    if (  histo_positions[3] == "0" ):
                        wp.write( "<td>" )
                        wp.write( "<a id=\"" + short_histo_name + "\" name=\"" + short_histo_name + "\"></a>" )
                        wp.write( "<a href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a>" )
                        wp.write( " </td>\n" )
                        lineFlag = False
                    else: # line_sp[3]=="1"
                        wp.write( "<td>" )
                        wp.write( "<a id=\"" + short_histo_name + "\" name=\"" + short_histo_name + "\"></a>" )
                        wp.write( "<a href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a>" )
                        wp.write( "</td></tr><tr valign=\"top\">" )
                        lineFlag = True

        wp.write( "</tr></table>\n" )
        wp.close()
        os.chdir('../') # back to the final folder.
        
        selectedText += " : <b><font color='blue'> DONE ! </font></b></strong>"
        wr.write("Dataset %s DONE\n" % elt[0])
        self.textReport += "Dataset " + elt[0] + "DONE"
        if ( getURL(dataSetFolder, self.URL)[:4] == 'http' ):
            selectedText += '\t\t<a href=\"' + getURL(dataSetFolder, self.URL) + "\">" + getURL(dataSetFolder, self.URL) + "</a><br>"
        else:
            selectedText += "<br>"
        wr.write(" Dataset URL%s\n" % getURL(dataSetFolder, self.URL))
        self.textReport += " Dataset URL " + getURL(dataSetFolder, self.URL)
        self.labelResumeSelected.setText(self.trUtf8(selectedText))
        QtCore.QCoreApplication.processEvents()
    
    self.labelResumeSelected.setText(self.trUtf8(selectedText))
    QtCore.QCoreApplication.processEvents()
    wr.close() # close the report file for the bottom operations.
    #back to initial dir
    os.chdir(actual_dir) # going back
    return

def testExtension(histoName, histoPrevious, self):
    after = "" # $histoName
    common = ""
    
    if '_' in histoName:
        afters = histoName.split('_')
        before = afters[0]
        nMax = len(afters)
        
        if ( afters[nMax - 1] == "endcaps" ):
            after = "endcaps"
            for i in range(1, nMax-1):
                before += "_" + afters[i]
        elif ( afters[nMax - 1] == "barrel" ):
            after = "barrel"
            for i in range(1, nMax-1):
                before += "_" + afters[i]
        else:
            if ( histoPrevious == "" ):
                before = histoName
                after = "" 
                common = histoName
            else:
                avant =  afters[0]
                after = ""
                for i in range(1, nMax-1):
                    avant += "_" + afters[i]
                    if avant == histoPrevious:
                        before = avant
                        common = histoPrevious
                        break
                for j in range(nMax-1, nMax):
                    after += "_" + afters[j]
                after = after[1:]
                
    else: # no _ in histoName
        before = histoName
        common = histoName
    
    return [after, before, common]
        
def clean_collections2(collectionItem, validationType_1, validationType_2, validationType_3, relrefChoice):
    import re
    temp = True
    checkFvsF = ""
    if ( ( relrefChoice == "ref") and (validationType_1 == "FastFull") ):
        checkFvsF = "Full"
    if ( ( relrefChoice == "rel") and (validationType_1 == "FastFull") ):
        checkFvsF = "Fast"
    
    valType = validationType_2 # default
    if ( relrefChoice == "ref" ):
        valType = validationType_3
    
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
        tt = list_search_1(item[0:-1])
        if (len(tt) > 0):
             temp_0.append(item[0:-1])

    return temp_0

def list_search_1(my_choice_0):
    from networkFunctions import cmd_fetch_1
        
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = str( my_choice_0 )
    option_mthreads = 3
    option_dry_run = True # False for loading files
    
    option_regexp = '' 
    (liste_releases_1) = cmd_fetch_1(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)

    i = 0
    temp_1 = []  
    if ( len(liste_releases_1) > 0 ):
        for item in liste_releases_1:
            temp_1.append(item)

    return temp_1

def list_search_2(collection, filtre):
    import re

    temp_1 = []  
    filtre = sorted(set(filtre), reverse=True)
    for item1 in collection:
        for item2 in filtre:
            if (item2 == item1):
                temp_1.append(item1)
                break
    temp_1 = sorted(set(temp_1), reverse=True)
    return temp_1
    
def list_search_3(collection, filtre):
    import re

    temp_1 = []  
    for item1 in collection:
        if re.search(filtre, item1):
            temp_1.append(item1)
    return temp_1
       
def list_search_5(self):
    import re

    self.wp.write("list_search_5 : self.validationType1 = %s\n " % self.validationType1)
    self.wp.write("list_search_5 : self.validationType2 = %s\n " % self.validationType2)
    self.wp.write("list_search_5 : self.validationType3 = %s\n " % self.validationType3)
    self.textReport += "list_search_5 : self.validationType1 = " + self.validationType1 + "<br>"
    self.textReport += "list_search_5 : self.validationType2 = " + self.validationType2 + "<br>"
    self.textReport += "list_search_5 : self.validationType3 = " + self.validationType3 + "<br>"
    
    temp_1 = [] # DQM_V0001_R00000000X__Dataset__CMSSW_9_1_0_pre3-91X_upgrade2017_realistic_v3-v1__DQMIO.root files
    temp_2 = [] # 91X_upgrade2017_realistic_v3-v1 Global tags
    temp_12 = []
    temp_rel = []
    temp_3 = []
    temp_4 = []
    temp_34 = []
    temp_ref = []

    filtre = sorted(set(self.selectedDataSets), reverse=True)
    self.wp.write("list_search_5 : self.selectedDataSets = %s\n " % str(self.selectedDataSets))
    self.wp.write("list_search_5 : filtre = %s\n " % str(filtre))
    self.textReport += "list_search_5 : self.selectedDataSets = " + str(self.selectedDataSets) + "<br>"
    self.textReport += "list_search_5 : filtre = " + str(filtre) + "<br>"
    validationType_2 = self.validationType2
    validationType_3 = self.validationType3
    
    # DATASET
    self.rel_list_2 = list_search_2(self.rel_list_1, self.selectedDataSets) # get dataset list used in rel_list_1
    self.ref_list_2 = list_search_2(self.ref_list_1, self.selectedDataSets) # get dataset list used in ref_list_1
    
    # PART RELEASE
    filtre = sorted(set(self.rel_list_2), reverse=True)
    self.wp.write("list_search_5 : filtre = %s\n " % str(filtre))
    self.textReport += "list_search_5 : filtre = " + str(filtre) + "<br>"
    for item1 in self.releasesList_rel_2:
        for item2 in filtre:
            if re.search(item2 + '__', item1):
                if clean_collections2(item1, self.validationType1, validationType_2, validationType_3, "rel"):
                    temp_12.append([explode_item(item1)[2], item2])
                break

    if ( len(temp_12) > 0 ):
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
    self.wp.write("list_search_5 : filtre = %s\n " % str(filtre))
    self.textReport += "list_search_5 : filtre = " + str(filtre) + "<br>"
    if (( validationType_3 == 'miniAOD' ) and ( validationType_2 == 'RECO' )): # case RECO vs miniAOD
        temp_3 = temp_1
        temp_4 = temp_2
    else:
        releasesTemp = self.releasesList_ref_2
        if ( checkFastvsFull(self) ): # Fast vs Full
            releasesTemp = self.releasesList_rel_2
        for item1 in releasesTemp:
            for item2 in filtre:
                if re.search(item2 + '__', item1):
                    if clean_collections2(item1, self.validationType1, validationType_2, validationType_3, "ref"):
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
    
    return (temp_1, temp_2, temp_3, temp_4)
    
def sub_releases(tab_files):
    i = 0
    temp = []
    for t in tab_files:
        tt = explode_item(t)
        temp.append(tt[1])
        i += 1
    temp = sorted(set(temp), reverse=True)
    return temp
    
def sub_releases2(release, tab_files):
    import re
    i = 0
    temp = []
    for t in tab_files:
        if ( re.search(release, t) ):
            tt = explode_item(t)
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
    
    temp_item = item[22:] # DQM_V0001_R000000001__ removed
    temp_item = temp_item[:-12] # __DQMIO.root removed
    temp_item = temp_item[6:] # RelVal removed
    temp_item = temp_item.split('__')
    temp_item2 = temp_item[1].split('-', 1)
    temp_item = [ temp_item[0] ]
    for it in temp_item2:
        temp_item.append(it)

    return temp_item

def checkFastvsFull(self):
    if ( self.radio13.isChecked() ):
        self.checkFastvsFull = True
    else:
        self.checkFastvsFull = False
    return self.checkFastvsFull

def newName(prefix, fileName, suffix):
    newName = prefix + fileName + suffix
    return newName

def checkFileName(self, fileName, case):
    checkFileName = True

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

    self.wp.write("validationType1 : %s, validationType2 : %s, validationType3 : %s\n " % (str(self.validationType1), str(self.validationType2), str(self.validationType3)))
    self.textReport += "validationType1 : " + str(self.validationType1) + "validationType2 : " + str(self.validationType2) + "validationType3 : " + str(self.validationType3) + "<br>"
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
        self.okToPublishDatasets = extractDatasets(self)
    selectedText += "<td>  </td>"
    selectedText += "</tr><tr><td><strong>GlobalTags : </td>" 
    selectedText += "<td>" + self.my_choice_rel_1 + "<br />" + self.selectedRelGlobalTag + "</td>" 
    selectedText += "<td> &nbsp;&nbsp;&nbsp; </td>"
    selectedText += "</tr></table>"
            
    self.labelResumeSelected.clear() # 
    self.labelResumeSelected.setText(self.trUtf8(selectedText))
    QtCore.QCoreApplication.processEvents()
    
    return

def updateLabelResume(self):
    check_working_dirs(self)
    check_finalFolder(self)
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
    
#    print "back to reference"
#    print "actual : " + self.my_choice_ref_1
#    print "native : " + self.my_choice_tmp
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
    
def checkRecompInName(name):
    if re.search('recomp', name):
        return True
    else:
        return False

def set_finalFolder(self, i_loc):
    self.location = self.LocationTable[i_loc][2] # get the chosen location for histos folder
    if (i_loc != 0):
        self.URL = pathToURL(self)[i_loc-1][1]
    else: # i_loc = 0
        self.URL = "" # put to empty
    folderADD = "/" + self.my_choice_rel_1[6:] + self.temp_rl + '_DQM_std' 
    folderADD += '/' + getCheckedRadioButton(self) + '_'
    folderADD += str(self.my_choice_ref_1[6:]) + self.temp_rf
    self.finalFolder = self.location + folderADD
    self.URL += folderADD

def check_finalFolder(self):
    if not os.path.exists(self.finalFolder): # only create the first folder for saving gifs, i.e. release folder. 
        self.wp.write("testExist_finalFolder ; (%s) folder not exist\n" % str(self.finalFolder))
        self.textReport += "testExist_finalFolder : " + str(self.finalFolder) + " final folder not exist" + "<br>"
        self.exist_finalFolder = False
    else:
        self.wp.write("%s already created\n" % str(self.finalFolder))
        self.textReport += "final folder " + str(self.finalFolder) + " already created" + "<br>"
        self.exist_finalFolder = True
    return

def check_working_dirs(self): # 
    import errno
    self.working_dir_rel = self.working_dir_base + '/' + str(self.my_choice_rel_1[6:]) # self.lineedit1.text()[6:]
    self.working_dir_ref = self.working_dir_rel + '/' + str(self.my_choice_ref_1[6:]) # self.lineedit3.text()[6:]
    self.wp.write("self.working_dir_rel : %s\n" % self.working_dir_rel)
    self.wp.write("self.working_dir_ref : %s\n" % self.working_dir_ref)
    self.textReport += "self.working_dir_rel : " + self.working_dir_rel + "<br>"
    self.textReport += "self.working_dir_ref : " + self.working_dir_ref + "<br>"
    
    if not os.path.exists(self.working_dir_rel):
        self.wp.write("%s release folder not exist\n" % str(self.working_dir_rel))
        self.textReport += str(self.working_dir_rel) + " folder not exist" + "<br>"
        self.exist_working_dir_rel = False
    else:
        self.wp.write("release folder %s already created\n" % str(self.working_dir_rel))
        self.textReport += "release folder " + str(self.working_dir_rel) + " already created" + "<br>"
        self.exist_working_dir_rel = True

    if not os.path.exists(self.working_dir_ref):
        self.wp.write("%s reference folder not exist\n" % str(self.working_dir_ref))
        self.textReport += str(self.working_dir_ref) + " reference folder not exist" + "<br>"
        self.exist_working_dir_ref = False
    else:
        self.wp.write("reference folder %s already created\n" % str(self.working_dir_ref))
        self.textReport += "reference folder " + str(self.working_dir_ref) + " already created" + "<br>"
        self.exist_working_dir_ref = True
    return

def getURL(folder, urlBase):
#    print("path    : %s" % path)
#    print("folder  : %s" % folder)
#    print("choix   : %s" % location)
#    print("urlBase : %s" % urlBase)
    URL = urlBase + '/' + folder
#    print("URL     : %s" % urlBase + '/' + folder)
    return URL
    