#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:10:09 2018

@author: charleneliu
"""

import numpy as np
import math
import matplotlib.pyplot as plt


xtrain_file = open('./xtrain', 'w')
ytrain_file = open('./ytrain', 'w')
k = 8
xtrain = ''
ytrain = []
# the key of the dictionary is obj_id, and the value is a tuple of features
dic = {}
i = 0
for i in range (5):
    print "file:" + str(i)
    cache_size = i*2 + 30
    trace = '../traces/dvars_lnslbound_w100m.tr_500000_' + str(cache_size) + '.log'
    f = open(trace)
    for eachline in f:
        fields = eachline.split()
        seq_num = int(fields[0])
        obj_id = int(fields[1])
        obj_size = int(fields[2])
        
        # append training label
        if fields[4] == "1" :
            ytrain.append(1)
        else :
            ytrain.append(0)
            
        # update last k requests' sequence number
        if obj_id in dic.keys():
            dic[obj_id][1:k + 1] = dic[obj_id][:k]
            dic[obj_id][0] = seq_num
        else :
            last_k_req_seq = []
            for j in range (k + 1):
                last_k_req_seq.append(0)
            dic[obj_id] = last_k_req_seq
            dic[obj_id][0] = seq_num
               
        # append training features of new data point
        line = ''
        for t in range (k):
            last_k_req_seq = dic[obj_id]
            if last_k_req_seq[t + 1] > 0:
                distance = seq_num - last_k_req_seq[t + 1] + 1
                t_th_freq = float(t + 2) / distance
                line += str(t_th_freq) + ' '
            else :
                line += str(0) + ' '
            
        xtrain += line
        xtrain += (str(obj_size) + ' ')
        xtrain += (str(cache_size) + '\n')

xtrain_file.write(xtrain)
xtrain_file.close()
ytrain_file.write(ytrain)
ytrain_file.close()

