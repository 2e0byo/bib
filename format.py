#! /usr/bin/python

import argparse
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bparser import BibTexParser
from pathlib import Path


def load_uniq(fn):
    with Path(fn).open() as f:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        parsed = bibtexparser.load(f, parser)
    seen = {}
    parsed.entries = [
        seen.setdefault(x["ID"], x) for x in parsed.entries if x["ID"] not in seen
    ]

    return parsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FN", help="File to format.", type=Path)

    args = parser.parse_args()
    fn = args.FN.expanduser()

    print(f"Loading and uniqifying {fn}")
    db = load_uniq(fn)
    writer = BibTexWriter()
    writer.order_entries_by = ("author", "year")
    writer.comma_first = True
    with fn.open("w") as f:
        f.write(writer.write(db))
    print(f"Saved {fn}")


if __name__ == "__main__":
    main()
