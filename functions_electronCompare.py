#! /usr/bin/env python
#-*-coding: utf-8 -*-

def getHisto(file):
    file.ls()
    t1 = file.Get("DQMData")
    t2 = t1.Get("Run 1")
    t3 = t2.Get("EgammaV")
    t4 = t3.Get("Run summary")
    t5 = t4.Get("ElectronMcSignalValidator")
    return t5

