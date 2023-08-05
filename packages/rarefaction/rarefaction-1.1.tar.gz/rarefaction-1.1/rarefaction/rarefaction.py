#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rarefaction.py
# Copyright (c) 2021 Xiao-Ning Tank Zhang <tanklovemermaid@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



'''
Sample from tag-count table (e.g. csv or tsv as input) from the cli
rarefaction to fraction times fold of minimal sample depth and random seed supported
more info please refer to README.md file
'''


import numpy as np
import pandas as pd
from multiprocessing import Lock, Pool, Process
import logging
import time
import json
from rarefaction.accumulation.multi_accumu import  accumu, call_back, errorCallback, parse_json
import argparse
from rarefaction.rarefy_filter import binary_dummy, filter, rarefy


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(process)d %(processName)s %(message)s"
)


ITERATIONS = 10


def add(a, b):
    return a+b

    
def test_answer():
    assert add(2, 3) == 5

def main():
    begin = time.time()
    parser = argparse.ArgumentParser(
        prog='rarefaction',
        description='''Python 3.8+ based, 
            Processing subsampling metagenomic feature-count table 
            and calculate the accumulation curve''',
        epilog= '''From 
            Author: Xiao-Ning Tank Zhang 2019-2022 
            Email: tanklovemermaid@gmail.com
            @Bailab@IGDB@UCAS
            ''')
    group1 = parser.add_argument_group('Rarefaction')                                                  
    group2 = parser.add_argument_group('Filter')                                                  
    group3 = parser.add_argument_group('Output')                                                  
    group4 = parser.add_argument_group('Performance')                                                  
    group5 = parser.add_argument_group('Input')                                                  
    group6 = parser.add_argument_group('Miscellaneous')    

    group5.add_argument('-i', "--input", dest="fin", type=str, required=True,
                        help='input of feature-count table')
    group3.add_argument('-o', "--output", dest='fout', type=str, required=True, 
                        help= "output accumulative table of row iterations by columns sample")
    group3.add_argument("--dfout", dest='dfout', type=str, required=True, 
                        help= "output tsv format of json")
    group4.add_argument('-t', "--thread", dest='thread', type=int, required=True, 
                        help=" <int> number of iterations threads to launch")
    group4.add_argument("--mm", dest='memory', type=int, required=False, 
                        help="use memory-mapped I/O for memory share")
    group1.add_argument('-f', "--frac", dest='frac', type=float, required=False,
                        help= "fraction of minimal size fold to rarefy")
    group1.add_argument('-m', "--min_sample_size", dest='min_ss', type=int, required=False, 
                        help="minimal sample size to specify for rarefaction")
    group3.add_argument("--min_ss_out", dest='min_ss_out', type=str, required=False, 
                        help= "output sample size table")
    group1.add_argument("--rarefy_out", dest='rarefy_out', type=str, required=False, 
                        help="rarefy table to output to dest dir")
    group2.add_argument("-p", dest='filter_on', action='store_true', 
                        help="switch of filter, false in default")
    group1.add_argument("--raref_on", dest='rarefy_on', action='store_true', 
                        help="flag switch of rarefy, false in default")
    group2.add_argument('--cut-off-cnt', dest='threshold', type=int, required=False,
                        help="cut-off threshold count to specify")
    group2.add_argument('--cut-off-perc', dest='threshold', type=float, required=False, 
                        help="cut-off threshold percentage to specify, decoupled with -c")
    group2.add_argument('-c', dest='cnt_flag', action='store_true', 
                        help="cut-off switch count to specify, coupled with parametre --cut-off-cnt")
    group6.add_argument('-v',"--version", action='version', version='%(prog)s 1.0')
    # group6.add_argument('-h',"--help", help='show this help and exit')

    args = parser.parse_args()
    data=[]
    # for chunk in pd.read_table("/mnt/m2/dairui/project/rice/sd1/result/map_quant_test/origin/featureCount/id95_length100/origin_id95_length100_count_table.txt", comment='#', index_col=0, chunksize=100000,engine='c'):
    #     data.append(np.round(chunk).astype(np.int))
    for chunk in pd.read_table(args.fin, comment='#', index_col=0, chunksize=100000,engine='c'):
        data.append(np.round(chunk).astype(np.int))

    data = pd.concat(data)
    sampled = data.copy()

    # rarefaction switch
    if args.rarefy_on:
        sampled = rarefy.rarefy(sampled,
                        args.min_ss, 
                        args.frac, 
                        args.min_ss_out, 
                        args.rarefy_out)
    else:
        pass

    # filter switch
    if args.filter_on:
        sampled = filter.filter_percent(sampled,
                                args.cnt_flag,
                                args.threshold,
                                )
    else:
        pass

    ## python version >= 3.8, otherwise parallel error for overflow
    pool = Pool(ITERATIONS)
    for iter in range(ITERATIONS):
        pool.apply_async(accumu, 
                        args=(sampled,iter, args.fout), 
                        callback=call_back, 
                        error_callback=errorCallback)
    pool.close()
    pool.join()

    parse_json(args.fout,args.dfout)
    end = time.time()
    print("total times elapse is %s", str(end - begin))



if __name__ == '__main__':
    main()
