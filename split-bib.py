#!/usr/bin/python

from argparse import ArgumentParser
from pathlib import Path
import subprocess
from getkey import getkey
from pymdownx import keys

# from https://gist.github.com/martin-ueding/4007035
class Colorcodes(object):
    """
    Provides ANSI terminal color codes which are gathered via the ``tput``
    utility. That way, they are portable. If there occurs any error with
    ``tput``, all codes are initialized as an empty string.
    The provides fields are listed below.
    Control:
    - bold
    - reset
    Colors:
    - blue
    - green
    - orange
    - red
    :license: MIT
    """

    def __init__(self):
        try:
            self.bold = subprocess.check_output("tput bold".split()).decode()
            self.reset = subprocess.check_output("tput sgr0".split()).decode()

            self.blue = subprocess.check_output("tput setaf 4".split()).decode()
            self.green = subprocess.check_output("tput setaf 2".split()).decode()
            self.orange = subprocess.check_output("tput setaf 3".split()).decode()
            self.red = subprocess.check_output("tput setaf 1".split()).decode()
        except subprocess.CalledProcessError as e:
            self.bold = ""
            self.reset = ""

            self.blue = ""
            self.green = ""
            self.orange = ""
            self.red = ""


_c = Colorcodes()


def candidate_names():
    s = _c.bold + _c.orange + "Output to: "
    keys = {"s": None}
    for f in outfs:
        for i in range(len(f)):
            if f[i].lower() not in keys:
                break
        keys[f[i].lower()] = f
        f = f[:i] + _c.green + f[i].upper() + _c.orange + f[i + 1 :]
        s += f"{f}  "
    s = s.rstrip()
    s += "? ("
    s += _c.green + "S" + _c.orange + " to skip)"
    s += _c.reset
    return s, keys


def process_region(region, count):
    print(f"{_c.orange}{_c.bold}Item {count}{_c.reset}")
    print(region)
    print("")
    print(options_string)
    choice = getkey()
    while choice.lower() not in keys:
        print("Incorrect input; try again")
        choice = getkey()
    if choice != "s":
        f = outfs[keys[choice]]
        print(f"Writing to {f.name}")
        f.write("\n\n" + region)
    print("")


def main():
    global outfs, options_string, keys

    parser = ArgumentParser()
    parser.add_argument("INF", help="File to read.", type=Path)
    parser.add_argument(
        "OUTFS", nargs="+", help="Output files to split into.", type=Path
    )
    parser.add_argument("--skip", default=0, help="Entries to skip", type=int)
    args = parser.parse_args()

    assert args.OUTFS
    outfs = {x.stem: x.expanduser().open("a") for x in args.OUTFS}

    options_string, keys = candidate_names()

    region = ""
    count = 0
    with args.INF.expanduser().open() as f:
        for line in f.readlines():
            if not line.strip() and region.strip():
                count += 1
                if count > args.skip:
                    process_region(region.strip(), count)
                region = ""
            else:
                region += line
    count += 1
    if count > args.skip:
        process_region(region.strip(), count)

    for _, f in outfs.items():
        f.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting safely")
        for _, f in outfs.items():
            print(f)
            f.close()
