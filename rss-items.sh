#!/usr/bin/env python
#
# Gets item titles from RSS feed and saves to file
#

import argparse
import feedparser
import os

# Arguments
parser = argparse.ArgumentParser(description="Save RSS item titles to file")
parser.add_argument("-i",
                    "--input",
                    dest="url",
                    help="URL of RSS/XML feed to parse.",
                    required=True,
                    type=str)
parser.add_argument("-n",
                    "--number",
                    default=10,
                    dest="max",
                    help="Maximum number of item titles to write to file.",
                    required=True,
                    type=int)
parser.add_argument("-o",
                    "--output",
                    dest="outfile",
                    help="Output file in which to write item titles.",
                    required=True,
                    type=str)
args = parser.parse_args()

xml = feedparser.parse(args.url)
num_items = min(args.max, len(xml.entries))
file = os.path.expanduser(args.outfile)

with open(file, mode="w") as f:
    for i in range(1, num_items):
        f.write(xml.entries[i].title + "\n")

