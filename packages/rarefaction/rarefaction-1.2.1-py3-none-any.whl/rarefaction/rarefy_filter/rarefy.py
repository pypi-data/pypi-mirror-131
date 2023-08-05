#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rarefaction.py
# Copyright (c) 2021 Xiao-Ning Tank Zhang <tanklovemermaid@gmail.com>

from skbio.stats import subsample_counts
import json
import logging

def rarefy(data, min_sample_size, frac, min_ss_out, rarefy_out):
    smp_est = []
    smp_pnt = []
    for i, c in enumerate(data.columns):
        c_data = data[c].copy()
        sum_tmp = sum(c_data)
        smp_est.append(sum_tmp)
        smp_pnt.append(c)
    mapped = dict(zip(smp_pnt,smp_est))
    with open(min_ss_out, encoding='utf-8', mode="w") as fd:
        json.dump(mapped, fd)

    # colsums minimal as sample_size
    min_smp_size = min(smp_est)
    print("minimal sample size is %s" %min_smp_size)
    if min_sample_size > min_smp_size:
        logging.info("Warning: your given sample size larger than the minimal colsums, we reset to the default")
        min_sample_size = min_smp_size

    sampled = data.copy()
    for idx,col in enumerate(data.columns):
        col_data = data[col].copy()
        recol = subsample_counts(col_data.values.astype(int), round(min_sample_size*frac))
        sampled[col] = recol
        print("iteration by {}/{}".format(idx+1,len(data.columns)))
    sampled.to_csv(rarefy_out,sep = '\t')
