#!/usr/bin/env python
#
# Description:
#   Outputs random quote from list of Wikiquote pages.
#
# Requirements:
#   bs4 (BeautifulSoup) to parse Wikiquote website.
#
# Configuration:
#   max_length (int)
#       Max number of characters to display from a quote.
#
#   output_width (int)
#       Wrap quote at nth character (multi-line output).
#
#   pages (nested list of strings)
#       List of Wikiquote pages to scrape quotes from.
#       Inner lists having two strings: [Wikiquote page slug, author name].
#       e.g. [
#               ["Leo_Tolstoy", "Tolstoy"],
#               ["Robert_Anton_Wilson", "RAW"]
#            ]
#
# How It Works:
#   BeautifulSoup (BS) does the heavy lifting. Picks a random author from the
#   pages variable, builds a Wikiquote URL from it, and requests the page
#   contents from that Wikiquote URL. Parses that Wikiquote page content for
#   quotes, adds them all to a list, and then selects one at random. Finally,
#   outputs that quote and its author's name.
#
#   Identifying quotes from the Wikiquote page content:
#       Wikiquote doesn't have a standardized page structure. Based on test
#       data, the author's quotes appear after the second <h2> element. They
#       are contained within <ul> list items, and each quote's source is also
#       contained within that list, but as it's own <ul> list. The script
#       identifies the second <h2> element to determine where the quotes start
#       and then iterates through each <ul> list where the quotes appear. If
#       there's a nested source/attribution <ul> list, it's first stripped out
#       and the parent <ul> list's text is stored in the script's quote list.
#
#       Example page source:
#           <h2>Quotes</h2>                 <-- 2nd occurance of h2 element
#           <ul>
#               <li>"Quote."</li>           <-- Quote we care about
#               <ul>
#                   <li>Quote source</li>   <-- Attribution to ignore
#               </ul>
#           </ul>
#           <ul>
#               <li>"Quote."</li>           <-- Another quote we care about
#               <ul>
#                   <li>Quote source</li>   <-- Attribution to ignore
#               </ul>
#           </ul>
#           <h2>Quotes about [Author Name]</h2>
#           [etc.]
#

import random
import requests
import textwrap

import bs4

# Configuration
max_length = 512
output_width = 79
pages = [
            ["Alex_Jones", "Alex Jones"],
            ["Bobby_Fischer", "Bobby Fischer"],
            ["L._Ron_Hubbard", "L. Ron Hubbard"]
        ]

# Constants
base = "https://en.wikiquote.org/wiki/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) " +
            "Chrome/114.0.0.0 Safari/537.36"}
random_author = random.randrange(len(pages))
url = base + pages[random_author][0]

# Functions
def get_page(url, headers):
    """ Return Wikiquote page content """
    r = requests.get(url=url, headers=headers)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    return soup

def get_quote(soup):
    """ Return random quote from input Wikiquote page content. """
    quotes = []
    h2 = soup.find_all("h2")[1]
    for sibling in h2.find_next_siblings():
        if sibling.name == "h2":
            break
        if sibling.name == "ul":
            quote = sibling.find("li")
            try:
                quote.ul.decompose()
            except:
                pass
            quote = quote.get_text()
            quotes.append(quote)
    quote = quotes[random.randrange(len(quotes))]
    quote.strip()
    if len(quote) > max_length:
        quote = textwrap.shorten(quote,
                    width=max_length, placeholder="...")
    quote = textwrap.fill(quote, width=output_width)
    return quote

def get_author(random_author):
    """ Return name of quote author, aligned right """
    author = "-- " + pages[random_author][1]
    author = author.rjust(output_width)
    return author

def main():
    """ Prepare variables, call functions, output results. """
    page = get_page(url, headers)
    quote = get_quote(page)
    author = get_author(random_author)

    print(quote)
    print(author)

# Execute
main()
