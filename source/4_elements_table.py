import re


GSD = "gsd.tsv"


def main() -> None:
    with open(GSD, "r") as source:
        tokens = []
        indices = []
        readings = []
        lemmata = []
        for line in source:
            # Skips comment lines.
            if line.startswith("#"):
                continue
            line = line.rstrip()
            if line:
                columns = line.split("\t")
                # Get the tokens.
                token = columns[1]
                tokens.append(token)
                # Get the readings.
                misc = columns[-1]
                misc_piece = misc.split("|")
                for piece in misc_piece:
                    if piece.startswith("Reading"):
                        match = re.match(r"Reading=(.+)", piece)
                        reading = match.group(1)
                        readings.append(reading)
                        # Get the index.
                        indices.append(columns[0])
                        # Get the kanji.
                        lemma = columns[2]
                        lemmata.append(lemma)
                        assert len(readings) == len(lemmata) == len(indices)
            else:  # Print out the 4 elements and skip the blank line to go to the next sentence.
                tokenized_sentence = " ".join(tokens)
                for kanji, index, reading in zip(lemmata, indices, readings):
                    print(kanji, index, reading, tokenized_sentence)
                tokens.clear()
                indices.clear()
                lemmata.clear()
                readings.clear()
                continue


if __name__ == "__main__":
    main()
