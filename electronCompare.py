#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

from getEnv import env
from Paths_default import *

#! /usr/bin/env python
#-*-coding: utf-8 -*-

from ROOT import TFile, TH2F, TCanvas, gStyle, gPad, TRatioPlot

def getHisto(file, tp):
    #file.ls()
    print ("tree path part = %s" % tp)
    t1 = file.Get("DQMData")
    t2 = t1.Get("Run 1")
    t3 = t2.Get("EgammaV")
    t4 = t3.Get("Run summary")
    t5 = t4.Get("ElectronMcSignalValidator")
    t5 = t4.Get(tp)
    return t5

def RenderHisto(histo, canvas):
    if ("ELE_LOGY" in histo.GetOption() and histo.GetMaximum() > 0):
        canvas.SetLogy(1)
    histo_name_flag = 1 ; # use 0 to switch off
    if ( histo.InheritsFrom("TH2") ):
        gStyle.SetPalette(1)
        gStyle.SetOptStat(110+histo_name_flag)
    elif ( histo.InheritsFrom("TProfile") ):
        gStyle.SetOptStat(110+histo_name_flag)
    else: # TH1
        gStyle.SetOptStat(111110+histo_name_flag)

def PictureChoice(histo1, histo2, filename):
    #print filename
    if(histo1.InheritsFrom("TH1F")):
#        print "TH1F : 2 pads"
        createPicture2(histo1, histo2, filename)
    else:
#        print "no TH1F, 1 pad"   
        createPicture(histo1, histo2, filename)
        
def createPicture(histo1, histo2, filename):
    #print "Hello, I will create an histo in createPicture !!"
    
    cnv = TCanvas("canvas","",600,600)
    histo1.Draw()
    histo1.SetStats(1)
    RenderHisto(histo1, cnv)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    histo1.SetLineColor(4)
    histo1.SetMarkerColor(4)
    statBox1.SetTextColor(4)
#    print "histo1 OK"
    
    gPad.Update()
    histo2.Draw()
    histo2.SetStats(1)
    RenderHisto(histo2, cnv)
    cnv.Update()
    statBox2 = histo2.GetListOfFunctions().FindObject("stats")
    histo2.SetLineColor(2)
    histo2.SetMarkerColor(2)
    statBox2.SetTextColor(2)
#    print "histo2 OK"

    y1 = statBox1.GetY1NDC()
    y2 = statBox1.GetY2NDC()
#    print "y1=", y1, ", y2=", y2
    statBox1.SetY1NDC(2*y1-y2)
    statBox1.SetY2NDC(y1)
#    print "statboxes OK"
    histo2.Draw()
    histo1.SetLineWidth(3) 
    histo1.Draw("histsames")

    cnv.Draw()
    cnv.Update()
    cnv.SaveAs(filename)
#    cnv.Draw()

    return
    
def createPicture2(histo1, histo2, filename):
#    print "Hello, I will create an histo in createPicture2 !!"
    #print filename
    
    cnv2 = TCanvas("canvas","",600,800)
    histo1.Draw()
    histo1.SetStats(1)
    RenderHisto(histo1, cnv2)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    histo1.SetLineColor(4)
    histo1.SetMarkerColor(4)
    statBox1.SetTextColor(4)
#    print "histo1 OK"
    
    gPad.Update()
    histo2.Draw()
    histo2.SetStats(1)
    RenderHisto(histo2, cnv2)
    cnv2.Update()
    statBox2 = histo2.GetListOfFunctions().FindObject("stats")
    histo2.SetLineColor(2)
    histo2.SetMarkerColor(2)
    statBox2.SetTextColor(2)
#    print "histo2 OK"

    y1 = statBox1.GetY1NDC()
    y2 = statBox1.GetY2NDC()
#    print "y1=", y1, ", y2=", y2
    statBox1.SetY1NDC(2*y1-y2)
    statBox1.SetY2NDC(y1)
#    print "statboxes OK"
    histo2.Draw()
    histo1.SetLineWidth(3) 
    histo1.Draw("histsames")

    cnv2.Draw()
    rp2 = TRatioPlot(histo1, histo2, "divsym")
    rp2.Draw()
    cnv2.Update()
    #cnv2.SaveAs(filename, "")
    cnv2.SaveAs(filename)
#    cnv2.Draw()
    
    return
    
def createWebPage(self):
    return
    
    