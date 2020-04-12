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

import plovid as plv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import montoTools as mnt

start = datetime.date(2020,2,24)

allData = {}
t=[]
totale_casi=[]
regione = 'Lombardia'

while True:
    datafile = "../COVID-19/dati-regioni/dpc-covid19-ita-regioni-%d%02d%02d.csv" \
               % (start.year,start.month,start.day)
    try:
        allData = plv.loadData(datafile,regione)
    except IOError as e:
        break
    totale_casi.append(allData["totale_casi"][0])
    start+=datetime.timedelta(1)
    t.append(start)

figs = plv.plotData(t,np.asarray(totale_casi),True)
for i,h in enumerate(figs):
    plt.figure(i)
    mnt.setProperties(h,False,plv.fontDict)
    ax=h.gca()
    plt.setp(ax.get_xticklabels(), rotation=90)
    ax.set_position([0.22, 0.15, 0.74, 0.8])
    h.savefig('Figura_%d.png'%i)

