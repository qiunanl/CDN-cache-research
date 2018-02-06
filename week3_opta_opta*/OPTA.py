#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 16:50:06 2018

@author: charleneliu
"""
import numpy as np
trace = '../traces/dvars_lnslbound_w100m.tr_500000_38.log'

import math

import matplotlib.pyplot as plt

f = open(trace)
sizes = []

for eachline in f:
    fields = eachline.split()
    sizes.append(int(fields[2]))
    
max_size = max(sizes)
min_size = min(sizes)



max_log = round(math.log(max_size, 1.25), 0)
min_log = round(math.log(min_size, 1.25), 0)


num_of_admit = []
num_of_request = []
admission_prob = []

for i in range (int(max_log) - int(min_log) + 1):
    num_of_admit.append(0)
    num_of_request.append(0)
    admission_prob.append(0.0)

print "haha"
f = open(trace)
for eachline in f:
    fields = eachline.split()
    log_size = int(round(math.log(int(fields[2]), 1.25), 0))
    num_of_request[log_size - 10] = 1 + num_of_request[log_size - 10]
    if fields[4] == "1":
        num_of_admit[log_size - 10] = num_of_admit[log_size - 10] + 1
   


for i in range (int(max_log) - int(min_log) + 1):
    num_of_admit[i] = num_of_admit[i]
    if num_of_request[i] > 0:
        admission_prob[i]  =  1.0 * num_of_admit[i] / num_of_request[i]
        
plt.plot(admission_prob) 
plt.title("OPTA v.s. log object size Cache-size=256G") 
plt.xlabel("log based object size with a 1.25 basis")
plt.ylabel("admission probability")
plt.figure()

coalesce_admit_prob = []
for i in range (17):
    coalesce_admit_prob.append(admission_prob[7])

coalesce_admit_prob [17:] = admission_prob[7:]
plt.plot(coalesce_admit_prob) 
#plt.xlim(xmin = 16)
plt.title("OPTA v.s. log object size Cache-size=256G")
plt.xlabel("log based object size with a 1.25 basis")
plt.ylabel("admission probability")



print type(coalesce_admit_prob)
OPTA = np.array(coalesce_admit_prob)
print type(OPTA)
np.savetxt('../OPTA/256G.csv',OPTA,delimiter=',')
print 'Finish saving csv file'
