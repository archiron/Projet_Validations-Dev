#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

def initDataSets(self):
    print "initDataSets"

    self.QLW_dataset.clear()
    for it in self.DataSetTable: # list of DataSets
        item = QListWidgetItem("%s" % it)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        item.setCheckState(QtCore.Qt.Checked)
        self.QLW_dataset.addItem(item)
    return
    