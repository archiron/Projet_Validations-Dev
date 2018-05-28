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

from ROOT import * # TFile, TH2F, TCanvas, gStyle, gPad, TRatioPlot
from math import log10

def getHisto(file, tp):
    #file.ls()
    print ("tree path part = %s" % tp)
    t1 = file.Get("DQMData")
    t2 = t1.Get("Run 1")
    t3 = t2.Get("EgammaV")
    t4 = t3.Get("Run summary")
    #t5 = t4.Get("ElectronMcSignalValidator")
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

def initRootStyle():
    #eleStyle = gStyle
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
    #eleStyle.SetPadTopMargin(0.075)
    eleStyle.SetPadRightMargin(0.2) 
    #eleStyle.SetTitleStyle(1001)
    #eleStyle.SetTitleBorderSize(2)
    eleStyle.SetMarkerStyle(21)
    eleStyle.SetMarkerSize(0.8)
    eleStyle.cd()
    ROOT.gROOT.ForceStyle()

def PictureChoice(histo1, histo2, scaled, err, filename):
    if(histo1.InheritsFrom("TH1F")):
        createPicture2(histo1, histo2, scaled, err, filename)
    elif ( histo1.InheritsFrom("TProfile") ):
        createPicture2(histo1, histo2, scaled, err, filename)
    else:
        createPicture(histo1, histo2, scaled, err, filename)
        
def createPicture(histo1, histo2, scaled, err, filename):
    new_entries = histo1.GetEntries()
    ref_entries = histo2.GetEntries()
    #print("new_entries : %d, ref_entries : %d" % (new_entries, ref_entries) )
    if (scaled and (new_entries != 0) and (ref_entries != 0)):
        rescale_factor = new_entries / ref_entries
        histo2.Scale(rescale_factor)
    if (histo2.GetMaximum() > histo1.GetMaximum()):
        histo1.SetMaximum(histo2.GetMaximum() * 1.1)
    if (filename == "h_ele_charge"):
       n_ele_charge = histo1.GetEntries()
       
    cnv = TCanvas("canvas","",960,600)    
    cnv.Clear()
    histo2.Draw()
    cnv.Update()
    gMax2 = ROOT.gPad.GetUymax()
    #print "    histo 2 max : ", ROOT.gPad.GetUymax(), gMax2

    cnv.Clear()
    histo1.Draw()
    cnv.Update()
    gMax1 = ROOT.gPad.GetUymax()
    #print "    histo 1 max : ", ROOT.gPad.GetUymax(), gMax1

    if (gMax1 != gMax2):
        var_1 = log10( abs(gMax1 - gMax2) )
        #print "log = %8.2f" % var_1

    cnv.Clear()
    histo1.Draw()
    histo1.SetMarkerColor(kRed)
    histo1.SetLineWidth(3)
    histo1.SetStats(1)
    RenderHisto(histo1, cnv)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    histo1.SetLineColor(kRed)
    histo1.SetMarkerColor(kRed)
    statBox1.SetTextColor(kRed)
    gPad.Update()
    histo2.Draw()
    histo2.SetLineWidth(3) 
    histo2.SetStats(1)
    RenderHisto(histo2, cnv)
    cnv.Update()
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
    cnv.Draw()
    cnv.Update()
    
    cnv.SaveAs(filename)

    return
    
def createPicture2(histo1, histo2, scaled, err, filename):
    new_entries = histo1.GetEntries()
    ref_entries = histo2.GetEntries()
    #print("new_entries : %d, ref_entries : %d" % (new_entries, ref_entries) )
       
    if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
        rescale_factor = new_entries / ref_entries
        histo2.Scale(rescale_factor)
    if (histo2.GetMaximum() > histo1.GetMaximum()):
        histo1.SetMaximum(histo2.GetMaximum() * 1.1)
    if (filename == "h_ele_charge"):
       n_ele_charge = histo1.GetEntries()
       
    cnv2 = ROOT.TCanvas("canvas", "", 960, 900)    
    cnv2.SetFillColor(10)
    
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0) # ,0,0,0
    pad1.SetBottomMargin(0.05)
    pad1.SetGridx()
    pad1.Draw()
    pad1.cd()
    
    if err == "1":
        newDrawOptions ="E1 P"
    else:
        newDrawOptions = "hist"
    
    histo1.SetStats(1)
    histo1.Draw(newDrawOptions) # 
    RenderHisto(histo1, cnv2)
    if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
        pad1.SetLogy(1)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    statBox1.SetTextColor(kRed)    
    gPad.Update()
    histo2.Draw("sames hist") # ""  same  
    histo2.SetStats(1)
    RenderHisto(histo2, cnv2)
    if ("ELE_LOGY" in histo2.GetOption() and histo2.GetMaximum() > 0):
        pad1.SetLogy(1)
    cnv2.Update()
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

    cnv2.cd()
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3) # ,0,0,0
    pad2.SetTopMargin(0.025)
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.Draw()
    pad2.cd()
    
    histo3 = histo1.Clone("histo3")
    histo3.SetLineColor(kBlack)
    histo3.SetMaximum(2.)
    histo3.Sumw2()
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
   
    cnv2.Draw()
    cnv2.Update()

    cnv2.SaveAs(filename)
#    cnv2.Closed()
        
    return
        
def createWebPage(self):
    return
    
    