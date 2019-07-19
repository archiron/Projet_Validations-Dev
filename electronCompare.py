#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning # remove info like : Info in <TCanvas::Print>: gif file gifs/h_ele_vertexPhi.gif has been created
argv.remove( '-b-' )

from Paths_default import *

from ROOT import * 
from math import log10

def getHisto(file, tp):
#    t1 = file.Get("DQMData")
#    t2 = t1.Get("Run 1")
#    t3 = t2.Get("EgammaV")
#    t4 = t3.Get("Run summary")
#    t5 = t4.Get(tp)
    path = 'DQMData/Run 1/EgammaV/Run summary/' + tp
    t_path = file.Get(path)
    return t_path # t5

def RenderHisto(histo, self):
    
    if ("ELE_LOGY" in histo.GetOption() and histo.GetMaximum() > 0):
        self.cnv.SetLogy(1)
    histo_name_flag = 1 ; # use 0 to switch off
    if ( histo.InheritsFrom("TH2") ):
        gStyle.SetPalette(1)
        gStyle.SetOptStat(110+histo_name_flag)
    elif ( histo.InheritsFrom("TProfile") ):
        gStyle.SetOptStat(110+histo_name_flag)
    else: # TH1
        gStyle.SetOptStat(111110+histo_name_flag)

def initRoot(self):
    initRootStyle()
    self.cnv = TCanvas("canvas")    

def initRootStyle():
    eleStyle = ROOT.TStyle("eleStyle","Style for electron validation")
    eleStyle.SetCanvasBorderMode(0)
    eleStyle.SetCanvasColor(kWhite)
    eleStyle.SetCanvasDefH(600)
    eleStyle.SetCanvasDefW(800)
    eleStyle.SetCanvasDefX(0)
    eleStyle.SetCanvasDefY(0)
    eleStyle.SetPadBorderMode(0)
    eleStyle.SetPadColor(kWhite)
    eleStyle.SetPadGridX(False)
    eleStyle.SetPadGridY(False)
    eleStyle.SetGridColor(0)
    eleStyle.SetGridStyle(3)
    eleStyle.SetGridWidth(1)
    eleStyle.SetOptStat(1)
    eleStyle.SetPadTickX(1)
    eleStyle.SetPadTickY(1)
    eleStyle.SetHistLineColor(1)
    eleStyle.SetHistLineStyle(0)
    eleStyle.SetHistLineWidth(2)
    eleStyle.SetEndErrorSize(2)
    eleStyle.SetErrorX(0.)
    eleStyle.SetTitleColor(1, "XYZ")
    eleStyle.SetTitleFont(42, "XYZ")
    eleStyle.SetTitleXOffset(1.0)
    eleStyle.SetTitleYOffset(1.0)
    eleStyle.SetLabelOffset(0.005, "XYZ") # numeric label
    eleStyle.SetTitleSize(0.05, "XYZ")
    eleStyle.SetTitleFont(22,"X")
    eleStyle.SetTitleFont(22,"Y")
    eleStyle.SetPadBottomMargin(0.13) # 0.05
    eleStyle.SetPadLeftMargin(0.15)
    eleStyle.SetPadRightMargin(0.2) 
    eleStyle.SetMarkerStyle(21)
    eleStyle.SetMarkerSize(0.8)
    eleStyle.cd()
    ROOT.gROOT.ForceStyle()

def PictureChoice(histo1, histo2, scaled, err, filename, self):
    if(histo1.InheritsFrom("TH1F")):
        createPicture2(histo1, histo2, scaled, err, filename, self)
    elif ( histo1.InheritsFrom("TProfile") ):
        createPicture2(histo1, histo2, scaled, err, filename, self)
    else:
        createPicture(histo1, histo2, scaled, err, filename, self)
        
def createPicture(histo1, histo2, scaled, err, filename, self):
    new_entries = histo1.GetEntries()
    ref_entries = histo2.GetEntries()
    if (scaled and (new_entries != 0) and (ref_entries != 0)):
        rescale_factor = new_entries / ref_entries
        histo2.Scale(rescale_factor)
    if (histo2.GetMaximum() > histo1.GetMaximum()):
        histo1.SetMaximum(histo2.GetMaximum() * 1.1)
    if (filename == "h_ele_charge"):
       n_ele_charge = histo1.GetEntries()
       
    self.cnv.SetCanvasSize(960, 600)
    self.cnv.Clear()
    histo2.Draw()
    self.cnv.Update()
    gMax2 = ROOT.gPad.GetUymax()

    self.cnv.Clear()
    histo1.Draw()
    self.cnv.Update()
    gMax1 = ROOT.gPad.GetUymax()

    if (gMax1 != gMax2):
        var_1 = log10( abs(gMax1 - gMax2) )

    self.cnv.Clear()
    histo1.Draw()
    histo1.SetMarkerColor(kRed)
    histo1.SetLineWidth(3)
    histo1.SetStats(1)
    RenderHisto(histo1, self)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    histo1.SetLineColor(kRed)
    histo1.SetMarkerColor(kRed)
    statBox1.SetTextColor(kRed)
    gPad.Update()
    histo2.Draw()
    histo2.SetLineWidth(3) 
    histo2.SetStats(1)
    RenderHisto(histo2, self)
    self.cnv.Update()
    statBox2 = histo2.GetListOfFunctions().FindObject("stats")
    histo2.SetLineColor(kBlue)
    histo2.SetMarkerColor(kBlue)
    statBox2.SetTextColor(kBlue)
    y1 = statBox1.GetY1NDC()
    y2 = statBox1.GetY2NDC()
    statBox2.SetY1NDC(2*y1-y2)
    statBox2.SetY2NDC(y1)
    histo1.Draw()
    histo2.Draw("histsames")
    self.cnv.Draw()
    self.cnv.Update()
    
    self.cnv.SaveAs(filename)

    return
    
def createPicture2(histo1, histo2, scaled, err, filename, self):
    new_entries = histo1.GetEntries()
    ref_entries = histo2.GetEntries()
       
    if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
        rescale_factor = new_entries / ref_entries
        histo2.Scale(rescale_factor)
    if (histo2.GetMaximum() > histo1.GetMaximum()):
        histo1.SetMaximum(histo2.GetMaximum() * 1.1)
    if (filename == "h_ele_charge"):
       n_ele_charge = histo1.GetEntries()
       
    self.cnv.SetCanvasSize(960, 900)
    self.cnv.Clear()
    self.cnv.SetFillColor(10)
    
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.25, 1, 1.0) # ,0,0,0
    pad1.SetBottomMargin(0.05)
    pad1.Draw()
    pad1.cd()
    
    if err == "1":
        newDrawOptions ="E1 P"
    else:
        newDrawOptions = "hist"
    
    histo1.SetStats(1)
    histo1.Draw(newDrawOptions) # 
    RenderHisto(histo1, self)
    if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
        pad1.SetLogy(1)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    statBox1.SetTextColor(kRed)    
    gPad.Update()
    histo2.Draw("sames hist") # ""  same  
    histo2.SetStats(1)
    RenderHisto(histo2, self)
    if ("ELE_LOGY" in histo2.GetOption() and histo2.GetMaximum() > 0):
        pad1.SetLogy(1)
    self.cnv.Update()
    statBox2 = histo2.GetListOfFunctions().FindObject("stats")
    statBox2.SetTextColor(kBlue)
    y1 = statBox1.GetY1NDC()
    y2 = statBox1.GetY2NDC()
    statBox2.SetY1NDC(2*y1-y2)
    statBox2.SetY2NDC(y1)
    newDrawOptions = "sames "
    if err == "1":
        newDrawOptions += "E1 P"
    else:
        newDrawOptions += "hist"
    histo1.Draw(newDrawOptions)
    histo2.Draw("sames hist")

    self.cnv.cd()
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.25) # ,0,0,0
    pad2.SetTopMargin(0.025)
    pad2.SetBottomMargin(0.2)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    
    histo3 = histo1.Clone("histo3")
    histo3.SetLineColor(kBlack)
    histo3.SetMaximum(2.)
    histo3.SetStats(0)
    histo3.Divide(histo2)
    histo3.SetMarkerStyle(21)
    histo3.Draw("ep")
    
    histo1.SetMarkerColor(kRed)
    histo1.SetLineWidth(3) 
    histo1.SetLineColor(kRed)
    histo1.GetYaxis().SetTitleSize(25)
    histo1.GetYaxis().SetTitleFont(43)
    histo1.GetYaxis().SetTitleOffset(2.00)
    
    histo2.SetLineColor(kBlue)
    histo2.SetMarkerColor(kBlue)
    histo2.SetLineWidth(3) 
    
    histo3.SetTitle("")
    histo3.GetYaxis().SetTitle("ratio h1/h2 ")
    histo3.GetYaxis().SetNdivisions(505)
    histo3.GetYaxis().SetTitleSize(20)
    histo3.GetYaxis().SetTitleFont(43)
    histo3.GetYaxis().SetTitleOffset(1.55)
    histo3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    histo3.GetYaxis().SetLabelSize(15)
    # X axis ratio plot settings
    histo3.GetXaxis().SetTitleSize(20)
    histo3.GetXaxis().SetTitleFont(43)
    histo3.GetXaxis().SetTitleOffset(4.)
    histo3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    histo3.GetXaxis().SetLabelSize(15)
   
    self.cnv.Draw()
    self.cnv.Update()

    self.cnv.SaveAs(filename)
    
    return
        
def createWebPage(input_rel_file, input_ref_file, tp_1, tp_2, cnv):
    f_rel = ROOT.TFile(input_rel_file)
    h1 = getHisto(f_rel, tp_1)

    f_ref = ROOT.TFile(input_ref_file)
    h2 = getHisto(f_ref, tp_2)

    CMP_CONFIG = 'ElectronMcSignalHistos.txt'
    CMP_TITLE = ' SOME BEAUTIFUL TITLE '
    CMP_RED_FILE = input_rel_file
    CMP_BLUE_FILE = input_ref_file
    image_up = "img/up.gif"
    image_point = "img/point.gif"
    f = open(CMP_CONFIG, 'r')

    wp = open('index.html', 'w') # web page
    wp.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
    wp.write("<html>\n")
    wp.write("<head>\n")
    wp.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
    wp.write("<title> " + CMP_TITLE + " </title>\n") #option -t dans OvalFile
    wp.write("</head>\n")
    wp.write("<a NAME=\"TOP\"></a>")
    wp.write("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"img/up.gif\" alt=\"Up\"/></a>&nbsp; " + CMP_TITLE + " </h1>\n" ) # option -t dans OvalFile
        
    # some text added such as GlobalTag for release & reference.
#    wp.write("<b><font color='red'> " + self.validationType2 + " " + self.my_choice_rel_1 + " </font></b>")
#    wp.write(" : " + self.selectedRelGlobalTag )
#    wp.write(" : " + elt[1] )
#    wp.write("<br>\n")
#    wp.write("<b><font color='blue'> " + self.validationType3 + " " + self.my_choice_ref_1 + " </font></b>")
#    wp.write(" : " + self.selectedRefGlobalTag )
#    wp.write(" : " + elt[2] )
    wp.write("<br>\n")
    
    if (f_ref == 0):
        wp.write("<p>In all plots below, there was no reference histograms to compare with")
        wp.write(", and the " + CMP_RED_FILE + " histograms are in red.") # new release red in OvalFile
    else:
        wp.write("<p>In all plots below")
        wp.write(", the <b><font color='red'> " + CMP_RED_FILE + " </font></b> histograms are in red") # new release red in OvalFile
        wp.write(", and the <b><font color='blue'> " + CMP_BLUE_FILE + " </font></b> histograms are in blue.") # ref release blue in OvalFile
    wp.write(" Some more details") # 
    wp.write(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms") # histos list .txt file
    wp.write(", <a href=\"gifs/\">images</a> of histograms" + "." )
    wp.write("</p>\n")

    # filling the title array & dict
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

    # end of filling the title array & dict
    f.close()
    wp.write( "<table border=\"1\" cellpadding=\"5\" width=\"100%\">" )
    
    for i in range(0, len(titlesList)):
        if ( i % 5  == 0 ):
            wp.write( "\n<tr valign=\"top\">" )
        textToWrite = ""
        wp.write( "\n<td width=\"10\">\n<b> " + titlesList[i] + "</b>" )
        titles = titlesList[i].split()
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
#                histo_name = histo_names[0]
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
                [after, before, common] = testExtension(short_histo_name, histoPrevious)
                   
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
#                histo_name = histo_names[0]
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
                gif_name = "GIFS/" + short_histo_names[0] + ".gif"
                histo_name_recomp = short_histo_names[0]
#                print("short_histo_names[0] : %s" % short_histo_names[0])
                histo_2 = h2.Get(short_histo_names[0]) #  
                if checkRecompInName(histo_name_recomp): # 
                    short_histo_names[0] = histo_name_recomp.replace("_recomp", "")
                    gif_name = "GIFS/" + short_histo_names[0] + "_recomp.gif"
                    
                histo_1 = h1.Get(short_histo_names[0])
                # the following is only for recomp histos.  
#                if checkRecompInName(histo_name_recomp) and self.checkSpecTarget1.isChecked(): # RECO vs miniAOD. For miniAOD vs miniAOD, we do not do this.
                    # we inverse histo1 & histo2 in order to keep the term "recomputed" into the title.
#                    PictureChoice(histo_2, histo_1, histo_positions[1], histo_positions[2], gif_name, cnv)
#                else:
#                    PictureChoice(histo_1, histo_2, histo_positions[1], histo_positions[2], gif_name, cnv)
                PictureChoice(histo_1, histo_2, histo_positions[1], histo_positions[2], gif_name, cnv)
                    
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
        
    return
    
def createWebPageLite(input_rel_file, input_ref_file, tp_1, tp_2, cnv): # simplified version of createWebPage()
    f_rel = ROOT.TFile(input_rel_file)
    h1 = getHisto(f_rel, tp_1)
#    h1.ls()
    
    f_ref = ROOT.TFile(input_ref_file)
    h2 = getHisto(f_ref, tp_2)
#    h2.ls()
    
    CMP_CONFIG = 'ElectronMcSignalHistosLite.txt'
    CMP_TITLE = ' SOME BEAUTIFUL TITLE '
    CMP_RED_FILE = input_rel_file
    CMP_BLUE_FILE = input_ref_file
    image_up = "img/up.gif"
    image_point = "img/point.gif"
    f = open(CMP_CONFIG, 'r')

    wp = open('index2.html', 'w') # web page
    wp.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
    wp.write("<html>\n")
    wp.write("<head>\n")
    wp.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
    wp.write("<title> " + CMP_TITLE + " </title>\n") #option -t dans OvalFile
    wp.write("</head>\n")
    wp.write("<a NAME=\"TOP\"></a>")
    wp.write("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"img/up.gif\" alt=\"Up\"/></a>&nbsp; " + CMP_TITLE + " </h1>\n" ) # option -t dans OvalFile
        
    # here you can add some text such as GlobalTag for release & reference.
    wp.write("<br>\n")
    
    if (f_ref == 0):
        wp.write("<p>In all plots below, there was no reference histograms to compare with")
        wp.write(", and the " + CMP_RED_FILE + " histograms are in red.") # new release red in OvalFile
    else:
        wp.write("<p>In all plots below")
        wp.write(", the <b><font color='red'> " + CMP_RED_FILE + " </font></b> histograms are in red") # new release red in OvalFile
        wp.write(", and the <b><font color='blue'> " + CMP_BLUE_FILE + " </font></b> histograms are in blue.") # ref release blue in OvalFile
    wp.write(" Some more details") # 
    wp.write(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms") # histos list .txt file
    wp.write(", <a href=\"gifs/\">images</a> of histograms" + "." )
    wp.write("</p>\n")

    # filling the title array & dict
    histoArray_0 = {}
    titlesList = [] # need with python < 3.7. dict does not keep the correct order of the datasets histograms
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
    # end of filling the title array & dict
    f.close()
    wp.write( "<table border=\"1\" cellpadding=\"5\" width=\"100%\">" )
    
    for i in range(0, len(titlesList)):
        if ( i % 5  == 0 ):
            wp.write( "\n<tr valign=\"top\">" )
        textToWrite = ""
        wp.write( "\n<td width=\"10\">\n<b> " + titlesList[i] + "</b>" )
        titles = titlesList[i].split()
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
            histo_names = elem.split("/")
            histoShortNames = histo_names[0]
            short_histo_names = histoShortNames.split(" ")
            histo_name = short_histo_names[0].strip().replace('\n', ' ').replace('\r', '')
            short_histo_name = histo_name.replace("h_", "")
            if "ele_" in short_histo_name:
                short_histo_name = short_histo_name.replace("ele_", "")
            if "scl_" in short_histo_name:
                short_histo_name = short_histo_name.replace("scl_", "")
            if "bcl_" in short_histo_name:
                short_histo_name = short_histo_name.replace("bcl_", "")
                   
            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=\'blue\'>" + short_histo_name + "</font></a>" + "&nbsp;\n"
                    
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
                histoShortNames = histo_names[0]
                short_histo_names = histoShortNames.split(" ")
                histo_name = short_histo_names[0].strip().replace('\n', ' ').replace('\r', '')
                short_histo_name = histo_name.replace("h_", "")
                if "ele_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("ele_", "")
                if "scl_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("scl_", "")
                if "bcl_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("bcl_", "")
                gif_name = "GIFS_LITE/" + histo_name + ".gif"
                
                histo_2 = h2.Get(histo_name)
                histo_1 = h1.Get(histo_name)
                PictureChoice(histo_1, histo_2, "1", "1", gif_name, cnv)
                    
                wp.write( "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + image_up + " alt=\"Top\"/></a></td>\n" )
                wp.write( "<td>" )
                wp.write( "<a id=\"" + short_histo_name + "\" name=\"" + short_histo_name + "\"></a>" )
                wp.write( "<a href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a>" )
                wp.write( "</td></tr><tr valign=\"top\">" )

    wp.write( "</tr></table>\n" )
    wp.close()
        
    return
    