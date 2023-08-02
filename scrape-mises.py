#!/usr/bin/python3
#
# Downloads PDFs from the mises.org book library
#

from bs4 import BeautifulSoup
import datetime
import os.path
import re
import requests

# Number of pages for [pdf] on Mises Book archive.
## Test the following URL with &page=57, etc. then update the variable below
## when you've identified the last pagination number.
## https://mises.org/library/books?book_type=539&page=56
pagination = 56

# Base URL to parse.
## book_type=539 is for PDF
url = "https://mises.org/library/books?book_type=539"

def sanitize(text):
  text = re.sub(r"[^a-zA-Z0-9]+", "", text.title())
  return text

def scrape_page(soup):
  #print("Scraping page...")
  for entry in soup.find_all("div", {"class": re.compile("^result-*")}):
    scrape_entry(entry)

def scrape_entry(entry):
  #print("Scraping entry...")
  title = [t.get_text() for t in entry.find_all("h2", {"class": "teaser-title"})]
  author = [u.get_text() for u in entry.find_all("span", {"class": "author"})]
  date = [d.get_text() for d in entry.find_all("span", {"class": "date"})]
  pdf = [a["href"] for a in entry.find_all("a", {"type": re.compile("^application/pdf*")})]

  title = sanitize(title[0])
  author = sanitize(author[0])
  date = datetime.datetime.strptime(date[0], "%m/%d/%Y").strftime("%Y-%m-%d")
  pdf = pdf[0]

  download_entry(title, author, date, pdf)

def download_entry(title, author, date, pdf):
  filename =  date + "_" + author + "_" + title + ".pdf"
  if os.path.isfile(filename):
    print("Already downloaded " + filename)
  else:
    print("Downloading " + filename)
    dl = requests.get(pdf)
    with open(filename, 'wb') as f:
      f.write(dl.content)

for p in range(1, 55):
  req = requests.get(url + "&page=" + str(p))
  soup = BeautifulSoup(req.content, "lxml")
  print("Scraping page " + str(p))
  scrape_page(soup)
