#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rarefaction.py
# Copyright (c) 2021 Xiao-Ning Tank Zhang <tanklovemermaid@gmail.com>

def binary_dummy(sampled):
    return sampled.applymap(lambda x: 1 if x >= 1 else 0)