#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rarefaction.py
# Copyright (c) 2021 Xiao-Ning Tank Zhang <tanklovemermaid@gmail.com>

import numpy as np
import pandas as pd
import logging
import os 
import json

def accumu(sampled, iter, fout):
    logging.info(f'calculate the accumulation...')
    # print(iter)
    sampled_dpcp = sampled.copy(deep = True)
    # sampled.to_csv("count_round_table.txt",sep='\t')

    ## shuffle columns to permutation test
    dict_c = {}
    acc = []
    
    shuff_col = sampled_dpcp.columns.to_list()
#     print(shuff_col)
    np.random.seed(iter)
    np.random.shuffle(shuff_col)
    print(type(shuff_col))
    # shuff_col = list(shuff_col.split(' '))
    
    sampled_dpcp = sampled_dpcp.reindex(columns = shuff_col)
    new = np.zeros_like(sampled_dpcp)
    temp = np.zeros(len(sampled_dpcp))
    
    for idx, col in enumerate(sampled_dpcp.columns):
        if idx==0:
            print(col)
        for i in range(len(temp)):
            if  sampled_dpcp.iloc[i,idx] or temp[i]:
                new[i,idx] = 1
            else:
                pass
        temp = new[:,idx]
        acc.append(int(temp.sum()))
    dict_c[str(iter)] = acc
    return (dict_c,fout)


def call_back(result):
    fout = result[1]
    dict_c = result[0]
    logging.info(f'\t\t write out accumulaiton result')
    with open(fout, encoding='utf-8', mode="a+") as fd:
        if  os.path.getsize(fout):
            # print("there")
            fd.seek(0)
            dict = json.load(fd)
            fd.close()
            # print(dict)
            # print(type(dict_c))
            dict.update(dict_c)
            # print(dict)
            with open(fout, 'w') as fw:
                json.dump(dict,fw)
        else:
            # print("here")
            json.dump(dict_c,fd)


def errorCallback(exception):
    print(exception)


def parse_json(fd, dfout):
    logging.info(f'parsing json file and output tsv format...')
    with open(fd, 'r') as fh:
        dict = json.load(fh)
    df = pd.DataFrame.from_dict(dict, orient = 'index')
    df.to_csv(dfout, sep='\t') 
