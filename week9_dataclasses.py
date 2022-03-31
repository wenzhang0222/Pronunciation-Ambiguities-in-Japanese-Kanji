#!/usr/bin/env python

import csv
import collections
import dataclasses
import pprint


@dataclasses.dataclass
class Entry:
    homography: str   # "Type" in the TSV file.
    reading: str      # "Reading" in the TSV file.


def main() -> None:
    table = collections.defaultdict(list)
    with open("jiten_revised.tsv","r") as source:
        reader = csv.reader(source)
        next(reader, None)
        for line in source:     
            homograph = line.split("\t")[0]
            tp = line.split("\t")[2]
            read = line.split("\t")[1]
            table[homograph].append(Entry(tp,read))
        pprint.pprint(table)
   
        for homograph, entries in table.items():
            print(f"{homograph} has {len(entries)} readings")


if __name__ == "__main__":
    main()
