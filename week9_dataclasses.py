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
    with open("jiten_revised.tsv", "r") as source:
        reader = csv.reader(source)
        next(reader, None)
        for line in source:
            homograph = line[0]
            tp = line[2]
            read = line[1]
            table[homograph].append(Entry(tp, read))
        pprint.pprint(table)


if __name__ == "__main__":
    main()
