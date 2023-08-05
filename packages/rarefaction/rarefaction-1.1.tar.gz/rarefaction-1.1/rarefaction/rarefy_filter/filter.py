#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rarefaction.py
# Copyright (c) 2021 Xiao-Ning Tank Zhang <tanklovemermaid@gmail.com>

def filter_percent(sampled, cnt_flag, threshold):
    # sampled = binary_dummy(sampled)
    if cnt_flag:
        sampled = sampled[sampled.mask(sampled!=0).count(axis=1) >= threshold]
        return sampled
    else:
        sampled = sampled[sampled.mask(sampled!=0).count(axis=1).div(float(len(sampled.columns))) >= threshold]
        return sampled