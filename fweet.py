#!/usr/bin/python
#
# Scrape fweet.org to get local copy of Finnegans Wake w/ page & line numbers
# e.g.
# 003.01 riverrun, past Eve and Adam's, from swerve of shore to bend
# 003.02 of bay, brings us by a commodius vicus of recirculation back to
# 003.03 Howth Castle and Environs.
#
# Note: at 2 seconds/page, will take 1,250 seconds or ~21 min. to complete.

import csv
import os
import requests
import sys

from bs4 import BeautifulSoup

first_page = 3
last_page = 628
output_txt = "finneganswake.txt"
output_csv = "finneganswake.csv"

# - Example for requesting page 23:
# - fweet.org/cgi-bin/fw_grep.cgi?regex=1&showtxt=1&hideelu=1&srch=^023
base_url = "http://www.fweet.org/cgi-bin/fw_grep.cgi" + \
           "?regex=1&showtxt=1&hideelu=1&srch=^"

with open(output_txt, "a") as t, open(output_csv, "a", newline="") as c:
    csvwriter = csv.writer(c, delimiter=",", quoting=csv.QUOTE_ALL)
    # Iterate through each page
    for page in range(first_page, last_page + 1):
        # Make soup, target relevant table
        url = base_url + str(page).zfill(3)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        table = soup.find_all("table")[1]
        trs = table.find_all("tr")
        print(str(page).zfill(3))
        for tr in trs:
            # Write to file
            page_line = tr.find("th").text.strip()
            line_text = tr.find("td").text.strip()
            t.write(page_line + " " + line_text + "\n")
            csvwriter.writerow([page_line, line_text])

