#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 23:44:45 2022

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
            # get the kanji
            lemma = columns[2]
            if lemma in ["年", "月", "日", "人", "者", "後", "中", "店", "時", "市",
                         "会", "氏", "目", "方", "大", "県", "前", "上", "家", "部",
                         "駅", "他", "化", "彼", "間", "見", "私", "車", "所", "機",
                         "生", "内", "事", "側", "何", "線", "長", "軍", "際", "国",
                         "分", "党", "地", "型", "本", "名", "戦", "点", "社", "手",
                         "世", "新", "同", "初", "力", "気", "式", "次", "用", "位",
                         "員", "話", "元", "町", "体", "今", "金", "州", "共", "出",
                         "不", "場"]:
                kanji = lemma
            # get the reading
            MISC = columns[-1]
            MISC_piece = MISC.split("|")
            for piece in MISC_piece:
                if piece.startswith("Reading"):
                    match = re.match(r"Reading=(.+)", piece)
                    reading = match.group(1)
                    print(kanji + " " + reading)


if __name__ == "__main__":
    main()
