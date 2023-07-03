#!/usr/bin/env python


import csv
import dataclasses
import collections
import pprint


JITEN = "jiten.tsv"
GSD = "gsd.conllu"


@dataclasses.dataclass
class Entry:
    homography: str
    reading: str


def kanji_readings() -> collections.defaultdict[str, list[Entry]]:
    table = collections.defaultdict(list)
    with open(JITEN, "r") as source:
        reader = csv.reader(source, delimiter="\t")
        for homograph, reading, homography in reader:
            table[homograph].append(Entry(homography, reading))
    return table


def main() -> None:
    table = kanji_readings()
    kanji_frequency = collections.Counter()
    with open(GSD, "r") as source:
        for line in source:
            if not line.startswith("#") and not line.isspace():
                form = line.split("\t")[1]
                if form in table:
                    kanji_frequency[form] += 1
    pprint.pprint(kanji_frequency.most_common())


if __name__ == "__main__":
    main()
