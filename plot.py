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

datafile = "../COVID-19/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

## intestazioni delle colonne. Per riferimento
keys = ['data', 'stato', 'ricoverati_con_sintomi', 'terapia_intensiva',
'totale_ospedalizzati', 'isolamento_domiciliare', 'totale_positivi',
'variazione_totale_positivi', 'nuovi_positivi', 'dimessi_guariti', 'deceduti',
 'totale_casi', 'tamponi', 'note_it', 'note_en']

allData = []
t       = []
nuovi_positivi=[]
totale_positivi=[]
tamponi = []

# calcolo media mobile
def runningAvg(xi, N):
    cumsum = np.cumsum(np.insert(xi, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

# equazione logistica
def f(x,L,x0,k):
    return L/(1+np.exp(-k*(x-x0)))

def N2(N) -> int:
    if N%2>0:
        return int((N-1)/2)
    else:
        return N/2
    

# carica i dati:
# - nuovi positivi
# - n. tamponi
# - totale casi
with open(datafile) as fp:
    data = csv.DictReader(fp,quoting=csv.QUOTE_NONE)
    for row in data:
        t.append(datetime.datetime.strptime(row['data'], '%Y-%m-%dT%H:%M:%S'))
        nuovi_positivi.append(float(row['nuovi_positivi']))
        tamponi.append(float(row['tamponi']))
        totale_positivi.append(float(row['totale_casi']))

# figura 1: nuovi positivi
N=7
h=plt.figure(1);
ax = h.add_subplot(111)
ax.plot(t[N2(N):-N2(N)],runningAvg(nuovi_positivi,N),'k.-')

ax.plot(t,nuovi_positivi,'o')
for curve in ax.get_lines():
    curve.set_linewidth(0.5)
    curve.set_fillstyle(None)
    curve.set_markeredgewidth(0)
    curve.set_markersize(3)

mnt.setProperties(h)

ax.grid(True)
ax.set_xlabel('data ')
ax.set_ylabel('nuovi positivi')
plt.setp(ax.get_xticklabels(), rotation=90)

# figura 2: nuovi positivi/n_tamponi
# h=plt.figure(2);
# ax = h.add_subplot(111)
# ax.plot(t[1:],np.asarray(nuovi_positivi[1:])/np.diff(np.asarray(tamponi)))
# mnt.setProperties(h)
# ax.grid(True)
# ax.set_xlabel('$data$ ')
# ax.set_ylabel('nuovi positivi/N tamponi')
# plt.setp(ax.get_xticklabels(), rotation=90)

# figura 3: n. totale di casi
h=plt.figure(3);
ax = h.add_subplot(111)
ax.plot(t,np.asarray(totale_positivi),'b');
mnt.setProperties(h)
ax.grid(True)

# calcolo fit della curva logistica
t_days = np.asarray([(ti-datetime.datetime.today()).days for ti in t])+len(t)
popt,pcov = sp.optimize.curve_fit(f, t_days, np.asarray(totale_positivi),[50000,25,2])
ti = np.arange(0,t_days[-1]*2);

yy = f(ti,*popt)
xi = [t[0] + datetime.timedelta(int(tii)) for tii in ti]
ax.plot(xi,yy,'k--')

ax.set_xlabel('data')
ax.set_ylabel('totale casi')
ax.set_yscale('log')
mnt.setProperties(h)
plt.setp(ax.get_xticklabels(), rotation=90)
ax.set_position([0.22, 0.2, 0.74, 0.8])
h.savefig('Totale.png')

# figura 4: derivata della curva logistica
h=plt.figure(4)
ax=h.add_subplot(111)
ax.set_xlabel('data')
ax.set_ylabel('differenza casi')
ax.plot(t[1:],np.diff(np.asarray(totale_positivi)),'b-',xi[1:],np.diff(yy),'k--')
mnt.setProperties(h)
ax.set_position([0.22, 0.15, 0.74, 0.8])
plt.setp(ax.get_xticklabels(), rotation=90)
h.savefig('Variazione.png')


