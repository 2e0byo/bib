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


bibs = {}
for f in Path(".").glob("*.bib"):
    bibs[f.stem] = load_uniq(f)

print("")
total = 0
for k, v in bibs.items():
    n = len(v.entries)
    print(f"{k}: {n} entries")
    total += n

print("Total:", total)

print("")
theology_entries = {x["ID"]: x for x in bibs["theology"].entries}

for name, bib in bibs.items():
    if name == "theology":
        continue
    for entry in bib.entries:
        if entry["ID"] in theology_entries:
            del theology_entries[entry["ID"]]

bibs["theology"].entries = [v for _, v in theology_entries.items()]

total = 0
for k, v in bibs.items():
    n = len(v.entries)
    print(f"{k}: {n} entries")
    total += n

print("Total:", total)

writer = BibTexWriter()
writer.order_entries_by = ("author", "year")
writer.comma_first = True
for name, obj in bibs.items():
    with Path(f"{name}.bib").open("w") as f:
        f.write(writer.write(obj))
