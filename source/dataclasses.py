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
        reader = csv.reader(source, delimiter = "\t")
        for homograph, reading, homography in reader:
            table[homograph].append(Entry(homography, reading))
    pprint.pprint(table)


if __name__ == "__main__":
    main()
