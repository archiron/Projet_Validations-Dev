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
    t1 = file.Get("DQMData")
    t2 = t1.Get("Run 1")
    t3 = t2.Get("EgammaV")
    t4 = t3.Get("Run summary")
    t5 = t4.Get(tp)
    return t5

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
        
def createWebPage(self):
    return
    
    