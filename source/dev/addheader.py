#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:02:13 2022

@author: wenzhang
"""

import pandas as pd


def main():
    file = pd.read_csv("場1.tsv", sep='\t', header=None)
    headerList = ["kanji","index","reading","sentence"]
    
    file.to_csv("場.tsv", sep='\t',header=headerList, index=False)
    
main()
