# -*- python -*-
""" ============================================================================ 

                              MONTOCLASS_SCRIPTS

   file: montoTools.py

   description:
       Python module containing common variables and functions

   usage:
       To be imported in python scripts

   author:

       Andrea Montorfano
       andrea.montorfano.it@hotmail.com

 ============================================================================ """

import os
import re
import math
import numpy as np
import csv

try:
    from matplotlib.pyplot import *
    HAVE_MATPLOTLIB=True
except ImportError as e:
    HAVE_MATPLOTLIB=False

# ------------------------------------------------------------------------------
# Line setting for 2D plots

col1 = ['bo-', 'ro-', 'go-', 'co-', 'mo-', 'yo-', 'ko-', 'bs-', 'rs-', 'gs-',\
            'cs-', 'ms-', 'ys-', 'ks-']
col2 = ['bs--', 'rs--', 'gs--', 'cs--', 'ms--', 'ys--', 'ks--', 'bo--',\
        'ro--', 'go--', 'co--', 'mo--', 'yo--', 'ko--']

col3 = ['bo.-', 'ro.-', 'go.-', 'co.-', 'mo.-', 'yo.-', 'ko.-']

col_o = ['bo', 'ro', 'go', 'co', 'mo', 'yo', 'ko', 'bo', 'ro', 'go', 'co', \
             'mo', 'yo', 'ko']

col_s = ['bs', 'rs', 'gs', 'cs', 'ms', 'ys', 'ks', 'bs', 'rs', 'gs', 'cs', \
             'ms', 'ys', 'ks']

col_l1 = ['b-', 'r-', 'g-', 'c-', 'm-', 'y-', 'k-', 'b-', 'r-', 'g-', 'c-', \
              'm-', 'y-', 'k-']

col_mix = ['b-','r-','g-','k-','y-','b--','r--','g--','k--','y--','b:','r:',\
               'g:','k:','y:']

col_l2 = ['b--', 'r--', 'g--', 'c--', 'm--', 'y--', 'k--', 'b--', 'r--', \
              'g--', 'c--', 'm--', 'y--', 'k--']

col_l3 = ['b:', 'r:', 'g:', 'c:', 'm:', 'y:', 'k:', 'b:', 'r:', 'g:', 'c:', \
              'm:', 'y:', 'k:']

mark = ['ko', 'ks', 'k^', 'kD', 'k*', 'kv', 'k+']

mark_l1 = ['ko-', 'ks-', 'k^-', 'kD-', 'kv-', 'k+-']

line = ['k-', 'k.-', 'k:']
# ------------------------------------------------------------------------------
# Coloured screen messages

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[43m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def Info(msg):
    print bcolors.OKBLUE + " [I]  " + msg + bcolors.ENDC

def InfoW(msg):
    print bcolors.OKGREEN + " [I]  " + msg + bcolors.ENDC


def Warn(msg):
    print bcolors.WARNING + " [W]  " + msg + bcolors.ENDC

def Err(msg):
    print bcolors.FAIL + " [E]  " + msg + bcolors.ENDC


# ------------------------------------------------------------------------------
# Create directory and return true if success or folder exists

def mkDir(folder):
    try:
        os.makedirs(folder)
        return True
    except OSError as e:
        if e.errno == 17:
            #print "[I] %s already exists." % folder
            return True
        else:
            print "[E] Cannot access folder %s for writing." % folder
            return False


# ------------------------------------------------------------------------------
# Read parameters from dictionary

def dictLookup(dtype, dictName, key, mustRead=True):

    genStrInt = """\s+([0-9]*)"""
    genStrFloat = """\s+([0-9]*\.?[0-9]*[e|E]?[\+|\-]?[0-9]*)"""
    genStrBool = """\s+(True|true|1|False|false|0)"""
    genStrStr = """\s+([\-A-Za-z0-9_\/\.]*)"""
    lb = """^\s*"""

    try:
        fp = open(dictName,'r')
        dictContent = fp.read()
        fp.close()
    except IOError as e:
        Err("Error in opening file  %s \n" % dictName)
        return None

    if dtype==int:
        searchStr = lb + key + genStrInt
        matchingStr = re.search(searchStr,dictContent,re.M)
        if matchingStr:
            return int(matchingStr.groups()[0])
        else:
            Warn("Field %s not found \n" % key)
            return None
    elif dtype==float:
        searchStr = lb + key + genStrFloat
        matchingStr = re.search(searchStr,dictContent,re.M)
        if matchingStr:
            return float(matchingStr.groups()[0])
        else:
            Warn("Field %s not found \n" % key)
            return None
    elif dtype==bool:
        searchStr = lb + key + genStrBool
        matchingStr = re.search(searchStr,dictContent,re.M)
        if matchingStr:
            return matchingStr.groups()[0] in ['true','True',1]
        else:
            Warn("Field %s not found \n" % key)
            return None
    elif dtype==list:
        result = []
        genStrList = "\s*\(\s*([-_a-zA-Z\s()0-9]*)\s*\);$"
        searchStr = key + genStrList;
        matchingStr = re.search(searchStr,dictContent,re.M)
        if matchingStr:
            wordStr = "\s*([-_a-zA-Z()0-9]*)\s*([-_a-zA-Z\s()0-9]*)"
            strippedList = matchingStr.group(1)
            while strippedList:
                matchingStr = re.search(wordStr,strippedList)
                result.append(matchingStr.group(1))
                strippedList = matchingStr.group(2)
            return result
        else:
            Warn("Field %s not found \n" % key)
            return None
    # matches strings
    else:
        searchStr = lb + key + genStrStr
        matchingStr = re.search(searchStr,dictContent,re.M)
        if matchingStr:
            return matchingStr.groups()[0]
        else:
            if mustRead:
                Warn("Field %s not found \n" % key)
            return None

# ------------------------------------------------------------------------------
# Read parameters from dictionary

def dictLookupOrDefault(dtype, dictName, key, defValue):
    value = dictLookup(dtype, dictName, key)

    if not(value):
        value = defValue

    return value


# ------------------------------------------------------------------------------
# set properties of graphic figure

defaultFont = {'family' : 'Courier New',\
                   'weight' : 'normal', \
                   'size'   : 8,\
                   'style'  : 'normal'
               }

def setProperties(fig, isForPaper = True):
    if isForPaper:
        fig.set(figwidth=3.5,figheight=2.7,facecolor='w',edgecolor='k')
    else:
        fig.set(figwidth=3.5,figheight=3.0,facecolor='w',edgecolor='k')

    ax=fig.gca();
    ax.grid(color='k', linestyle=":", linewidth=.115)
    ax.set_xlabel(ax.get_xlabel(),fontdict=defaultFont,labelpad=4)
    ax.set_ylabel(ax.get_ylabel(),fontdict=defaultFont,labelpad=4)
    setp(ax.get_xticklabels(), fontsize=defaultFont['size'],family=defaultFont["family"])
    setp(ax.get_yticklabels(), fontsize=defaultFont['size'],family=defaultFont["family"])

    if isForPaper:
        ax.set_position([0.22, 0.15, 0.74, 0.8])

    ax.xaxis.set_tick_params(width=0.2)
    ax.yaxis.set_tick_params(width=0.2)

#    leg=ax.get_legend()

    for side in ['top','bottom','left','right']:
        ax.spines[side].set_linewidth(0.2)
    for curve in ax.get_lines():
        curve.set_antialiased(True)
        # curve.set_linewidth(0.5)
#        curve.set_fillstyle(None)
#        curve.set_markeredgewidth(0)
#        curve.set_markersize(3)
    for child in ax.get_children():
        if child is matplotlib.text.Annotation:
            child.set_size(4)

# ------------------------------------------------------------------------------
# read an XY text file. Separator is space and comment is '#'

def readFile(fileName, startCol=1, endCol=None, quiet=False):
    x=[];
    y=[];
    try:
        with open(fileName) as fp:
            for line in fp:
                if line.split() == [] or line.split()[0][0]=='#' :
                    pass
                else:
                    x.append(float(line.split()[0]))
                    t = line.split()[startCol:endCol]
                    iterable = (float(ty) for ty in t);
                    y.append(np.fromiter(iterable,np.float))
        return (np.asarray(x), np.squeeze(y))
    except IOError as e:
        if not quiet:
            Warn("File %s not found" % fileName)

            return (None,None)

# ------------------------------------------------------------------------------

def readCsv(fileName, keys, quiet=False):
    x = []
    y = []
    Info('File %s' % fileName)
    try:
        with open(fileName) as fp:
            data = csv.DictReader(fp,quoting=csv.QUOTE_NONNUMERIC)
            for col in data:
                x.append(col[keys[0]])
                y.append(col[keys[1]])
        return (np.asarray(x), np.asarray(y))
    except IOError as e:
        if not quiet:
            Warn("File %s not found" % fileName)
        return None

# ============================== END-OF-FILE ================================= #
