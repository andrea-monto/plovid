#!/usr/bin/python3
# -*- python -*-
""" ============================================================================

                              MONTOCLASS_SCRIPTS

   file: ploy.py

   description:
       Plot graphs

   usage:
       launch from shell

   author:
       Andrea Montorfano
       andrea.montorfano.it@hotmail.com

 ============================================================================ """

import numpy as np
import matplotlib.pyplot as plt
import montoTools as mnt
import csv
import datetime
import scipy as sp
from scipy import optimize

dataFile = "../COVID-19/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

# larghezza media mobile
N=7

## intestazioni delle colonne. Per riferimento
keys = ['data', 'stato', 'ricoverati_con_sintomi', 'terapia_intensiva',
'totale_ospedalizzati', 'isolamento_domiciliare', 'totale_positivi',
'variazione_totale_positivi', 'nuovi_positivi', 'dimessi_guariti', 'deceduti',
 'totale_casi', 'tamponi', 'note_it', 'note_en']

# font per i grafici
fontDict = {'family' : 'Sans Serif',\
                   'weight' : 'normal', \
                   'size'   : 8,\
                   'style'  : 'normal'
               }


# calcolo media mobile
def runningAvg(xi, N):
    cumsum = np.cumsum(np.insert(xi, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def smooth(t,xi,N):
    return t[N2(N):-N2(N)],runningAvg(xi,N)

def f(x,L,x0,k):
    """Equazione logistica"""
    return L/(1+np.exp(-k*(x-x0)))


def N2(N) -> int:
    if N%2>0:
        return int((N-1)/2)
    else:
        return N/2

def tVec(t):
    return np.asarray([(ti-t[0]).days + round((ti-t[0]).seconds/(24*3600)) for
                       ti in t])
    
def dydt(t ,y):
    tDays = tVec(t)
    return np.diff(y)/np.diff(tDays)


def loadData(datafile, region=None):
    """ Carica i dati:
        - nuovi positivi
        - totale dei casi
    """
    t = []
    nuoviPositivi = []
    totaleCasi = []
    with open(datafile) as fp:
        data = csv.DictReader(fp,quoting=csv.QUOTE_NONE)
        for row in data:
            if region is None:
                pass
            elif region != row['denominazione_regione']:
                continue
            t.append(datetime.datetime.strptime(row['data'], '%Y-%m-%dT%H:%M:%S'))
            nuoviPositivi.append(float(row['nuovi_positivi']))
            totaleCasi.append(float(row['totale_casi']))
    return { "t": t, "totale_casi": totaleCasi, "nuovi_positivi": nuoviPositivi}


def calcFit(t,casi):
    """ Calcolo fit della curva logistica"""
    tDays = tVec(t)
    popt,pcov = sp.optimize.curve_fit(f, tDays, casi,[20000,25,2])
    ti = np.arange(0,tDays[-1]*2);
    casiFit = f(ti,*popt)
    return ti,casiFit

def plotData(t,casi,doFit=True):
    figList = []

    # equazione logistica
    h=plt.figure();
    ax = h.add_subplot(111)
    ax.plot(t,casi,'b');
    ax.grid(True)
    ax.set_xlabel('data')
    ax.set_ylabel('totale casi')
    ax.set_yscale('log')
    if doFit:
        ti,totaleCasiFit = calcFit(t,casi)
        tFit = [t[0] + datetime.timedelta(int(tii)) for tii in ti]
        ax.plot(tFit,totaleCasiFit,'k--')
    figList.append(h)

    # lo stesso, ma in scala lineare
    h=plt.figure();
    ax = h.add_subplot(111)
    ax.plot(t,casi,'b');
    ax.grid(True)
    ax.set_xlabel('data')
    ax.set_ylabel('totale casi')
    if doFit:
        ti,totaleCasiFit = calcFit(t,casi)
        tFit = [t[0] + datetime.timedelta(int(tii)) for tii in ti]
        ax.plot(tFit,totaleCasiFit,'k--')
    figList.append(h)
    
    # derivata della curva logistica
    h=plt.figure()
    ax=h.add_subplot(111)
    ax.set_xlabel('data')
    ax.set_ylabel('differenza casi')
    ax.plot(t[1:],dydt(t,casi),'b-')

    if doFit:
        ax.plot(tFit[1:],dydt(tFit,totaleCasiFit),'k--')
    figList.append(h)

    return figList

if __name__ == '__main__':
    allData = loadData(dataFile);
    t = allData["t"]
    casi = allData["totale_casi"]
    figs = plotData(t,casi)
    figs += plotData(t[N2(N):-N2(N)],runningAvg(casi,N))
    for i,h in enumerate(figs):
        plt.figure(i)
        mnt.setProperties(h,False,fontDict)
        ax=h.gca()
        plt.setp(ax.get_xticklabels(), rotation=90)
        ax.set_position([0.22, 0.15, 0.74, 0.8])
        h.savefig('Figura_%d.png'%i)
#    plt.show()
