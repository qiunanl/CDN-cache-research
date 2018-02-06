#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 21:30:41 2018

@author: charleneliu
"""
import matplotlib.pyplot as plt

LRU_ohr = [0.35667, 0.451092, 0.569267, 0.692428, 0.713333]
x = range(5)
x_index = ['1G', '4G', '16G', '64G', '256G']

plt.plot(LRU_ohr, label='LRU')
plt.xticks(x, x_index)
plt.xlabel("cache size")
plt.ylabel("OHR")
plt.title("OHR of vaious admission policy")
plt.legend()



FIFO_ohr = [0.316565, 0.46662, 0.534501, 0.665433, 0.713333]
plt.plot(FIFO_ohr, label='FIFO')
plt.legend()



GDSF_ohr = [0.530694, 0.630455, 0.704346, 0.711148, 0.713333]
plt.plot(GDSF_ohr, label='GDSF')
plt.legend()


GDS_ohr = [0.519349, 0.622052, 0.703488, 0.711129, 0.713333]
plt.plot(GDS_ohr, label='GDS')
plt.legend()


OPTA_ohr = [0.476322, 0.572357, 0.668481, 0.698936, 0.699577]
plt.plot(OPTA_ohr, label='OPTA')
plt.legend()


OPTA_star_ohr = [0.347406, 0.361288, 0.349594, 0.351415, 0.351523]
plt.plot(OPTA_star_ohr, label='OPTA*')
plt.legend()
