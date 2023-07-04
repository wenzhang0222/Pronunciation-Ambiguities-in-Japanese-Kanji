#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 00:37:17 2022

@author: wenzhang
"""

import re


GSD = "gsd.tsv"


def main() -> None:
    with open(GSD, "r") as source:
        for line in source:
            # Skips comment lines.
            if line.startswith("#"):
                continue
            # Skips blank lines.
            line = line.rstrip()
            if not line:
                continue
            columns = line.split("\t")
            # get the kanji.
            lemma = columns[2]
            # get the reading.
            MISC = columns[-1]
            MISC_piece = MISC.split("|")
            for piece in MISC_piece:
                if piece.startswith("Reading"):
                    match = re.match(r"Reading=(.+)", piece)
                    reading = match.group(1)
                    print(lemma + " " + reading)


if __name__ == "__main__":
    main()
