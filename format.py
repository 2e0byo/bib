#! /usr/bin/python

import argparse
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bparser import BibTexParser
from pathlib import Path
from io import StringIO
from sys import stderr


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
    parser.add_argument("FNS", help="File to format.", type=Path, nargs="+")
    parser.add_argument(
        "--verify",
        help="Exit with status 0 if nothing to be done else 1.",
        action="store_true",
    )

    args = parser.parse_args()

    for fn in args.FNS:
        fn = fn.expanduser()

        print(f"Loading and uniqifying {fn}")
        db = load_uniq(fn)
        writer = BibTexWriter()
        writer.order_entries_by = ("author", "year")
        writer.comma_first = True
        generated = StringIO(writer.write(db))
        if not args.verify:
            with fn.open("w") as f:
                f.write(generated.read())
            print(f"Saved {fn}")
        else:
            with fn.open() as f:
                for left, right in zip(f, generated):
                    if left != right:
                        stderr.write(f"{fn} failed verification")
                        stderr.flush()
                        exit(1)


if __name__ == "__main__":
    main()
