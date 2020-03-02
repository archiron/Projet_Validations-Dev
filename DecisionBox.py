#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import urllib2
import numpy as np

class DecisionBox:
    def __init__(self): 
        self.toto = 1.2

    # calculate the difference of s0
    def getDifference_1(self, s0,e0,s1,e1):
        s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
        s1 = np.asarray(s1) # if not this, ind is returned as b_00x instead of int value
        e0 = np.asarray(e0) # if not this, ind is returned as b_00x instead of int value
        e1 = np.asarray(e1) # if not this, ind is returned as b_00x instead of int value
        diff_max = 0.
        mask = []
        N = len(s0)
        for i in range(0, N):
            a1 = s0[i] - e0[i]
            b1 = s1[i] + e1[i]
            a2 = s0[i] + e0[i]
            b2 = s1[i] - e1[i]
            ab1 = a1 - b1
            ab2 = b2 - a2
            #print(i)
            if (s0[i] > s1[i]):
                if (ab1 > 0.):
                    mask.append(0)
                    if (np.abs(ab1) > diff_max):
                        diff_max = np.abs(ab1)
                        #print('ab1[%d] : %f' % (i, diff_max))
                elif (ab1 <= 0.):
                    mask.append(1)
            elif (s0[i] < s1[i]):
                if (ab2 > 0.):
                    mask.append(0)
                    if (np.abs(ab2) > diff_max):
                        diff_max = np.abs(ab2)
                        #print('ab2[%d] : %f' % (i, diff_max))
                elif (ab2 <= 0.):
                    mask.append(1)
            elif (s0[i] == s1[i]):
                #diff = 0.
                mask.append(1)
            #print('diff max : %f' % diff_max)
        return diff_max, mask
    
    # calculate the difference of s0
    def getDifference_2(self, s0,e0,s1,e1):
        s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
        s1 = np.asarray(s1) # if not this, ind is returned as b_00x instead of int value
        e0 = np.asarray(e0) # if not this, ind is returned as b_00x instead of int value
        e1 = np.asarray(e1) # if not this, ind is returned as b_00x instead of int value
        diff_max = 0.
        mask = []
        N = len(s0)
        for i in range(0, N):
            a1 = s0[i] - e0[i]
            b1 = s1[i] + e1[i]
            a2 = s0[i] + e0[i]
            b2 = s1[i] - e1[i]
            ab1 = a1 - b1
            ab2 = b2 - a2
            #print(i)
            if ((s0[i] + s1[i]) != 0.):
                #print('so[%d] + s1[%d] = %f' % (i,i,s0[i] + s1[i]))
                if (s0[i] > s1[i]):
                    if (ab1 > 0.):
                        mask.append(0)
                        if (np.abs(ab1) > diff_max):
                            diff_max = np.abs(ab1)
                            #print('ab1[%d] : %f' % (i, diff_max))
                    elif (ab1 <= 0.):
                        mask.append(1)
                elif (s0[i] < s1[i]):
                    if (ab2 > 0.):
                        mask.append(0)
                        if (np.abs(ab2) > diff_max):
                            diff_max = np.abs(ab2)
                            #print('ab2[%d] : %f' % (i, diff_max))
                    elif (ab2 <= 0.):
                        mask.append(1)
                elif (s0[i] == s1[i]):
                    #diff = 0.
                    mask.append(1)
            #else:
                #print('so[%d] + s1[%d] = %f' % (i,i,s0[i] + s1[i]))
        #print('diff max : %f' % diff_max)
        return diff_max, mask

    # calculate the difference of s0
    def getDifference_3(self, s0,e0,s1,e1):
        s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
        s1 = np.asarray(s1) # if not this, ind is returned as b_00x instead of int value
        e0 = np.asarray(e0) # if not this, ind is returned as b_00x instead of int value
        e1 = np.asarray(e1) # if not this, ind is returned as b_00x instead of int value
        diff_max = 0.
        mask = []
        N = len(s0)
        for i in range(1, N-1):
            a1 = s0[i] - e0[i]
            b1 = s1[i] + e1[i]
            a2 = s0[i] + e0[i]
            b2 = s1[i] - e1[i]
            ab1 = a1 - b1
            ab2 = b2 - a2
            #print(i)
            if (s0[i] > s1[i]):
                if (ab1 > 0.):
                    mask.append(0)
                    if (np.abs(ab1) > diff_max):
                        diff_max = np.abs(ab1)
                        #print('ab1[%d] : %f' % (i, diff_max))
                elif (ab1 <= 0.):
                    mask.append(1)
            elif (s0[i] < s1[i]):
                if (ab2 > 0.):
                    mask.append(0)
                    if (np.abs(ab2) > diff_max):
                        diff_max = np.abs(ab2)
                        #print('ab2[%d] : %f' % (i, diff_max))
                elif (ab2 <= 0.):
                    mask.append(1)
            elif (s0[i] == s1[i]):
                #diff = 0.
                mask.append(1)
        #else:
            #print('so[%d] + s1[%d] = %f' % (i,i,s0[i] + s1[i]))
        #print('diff max : %f' % diff_max)
        return diff_max, mask

    # get a coefficient from an array of integers 0/1
    def getCoeff(self, m0):
        coeff = np.asarray(m0).mean()
        return coeff

    def getHistoValues(self, histo):
        #print('nb bins : %d' % histo_1.GetXaxis().GetNbins())
        i=0
        s0 = []
        e0 = []
        i=0
        for entry in histo:
            #print("%d/%d : %s - %s") % (i, histo_1.GetXaxis().GetNbins(), entry, histo_1.GetBinError(i))
            s0.append(entry)
            e0.append(histo.GetBinError(i))
            i += 1
        return s0, e0 
       
    # major function to be called
    # ref is GevSeq.py
    def decisionBox(self, h1, h2):
        coeff_1 = 1. 
        coeff_2 = 2.
        coeff_3 = 3.
        s0, e0 = self.getHistoValues(h1)
        s1, e1 = self.getHistoValues(h2)
        d_max_1, r_mask_1 = self.getDifference_1(s0, e0, s1, e1)
        d_max_2, r_mask_2 = self.getDifference_2(s0, e0, s1, e1) # same as above without couples (0., 0.)
        d_max_3, r_mask_3 = self.getDifference_3(s0, e0, s1, e1) # same as above without couples first & end (0., 0.) couple.
        coeff_1 = self.getCoeff(r_mask_1)
        coeff_2 = self.getCoeff(r_mask_2)
        coeff_3 = self.getCoeff(r_mask_3)
        #print('coeff 1 : %6.4f' % coeff_1)
        #print('coeff 2 : %6.4f' % coeff_2)
        #print('coeff 3 : %6.4f' % coeff_3)
        #print(' ')
        return coeff_1, coeff_2, coeff_3
        
    def setColor(self, coeff):
        tmp = str("%6.4f" % coeff)
        if(coeff <= 0.35):
            text = "<font color=\'red\'><b>" + tmp + "</b></font>"
        elif(coeff <= 0.75):
            text = "<font color=\'blue\'><b>" + tmp + "</b></font>"
        else:
            text = "<font color=\'green\'><b>" + tmp + "</b></font>"
        #print("%6.4f : %s" % (coeff, text))
        return text
    
    
		
