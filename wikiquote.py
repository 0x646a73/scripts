#!/usr/bin/env python
#
# Outputs random quote from list of Wikiquote pages
#
# Requires bs4 (BeautifulSoup) to parse Wikiquote website.

import random
import requests
import textwrap

import bs4

# User Variables
# max_length: int - max number of characters to display from quote
# output_width: int - number of characters per line of output
# pages: nested list of strings - [Wikiquote page slug, author display name]
# enable_conky_color: bool - color the author's name via conky color syntax
# NOTE: conky colors not working; color syntax is output literally by conky
# conky_color: RRGGBB - hex color code (omitting #) for author display name
max_length = 512
output_width = 79
pages = [
            ["Alex_Jones", "Alex Jones"],
            ["Bobby_Fischer", "Bobby Fischer"],
            ["L._Ron_Hubbard", "L. Ron Hubbard"]
        ]
enable_conky_color = False
conky_color = "AA2222"

# Functions
def get_page(url, headers):
    """ Get Wikiquote page content.
        Uses python requests to query page content and return "soup" to parse
    """
    r = requests.get(url=url, headers=headers)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    return soup

def get_quote(soup):
    """ Get random quote from Wikiquote page content.
        Quotes on Wikiquote appear after the second <h2> element on the
        page. Iterates through the siblings of that <h2> element and adds
        them to a quote list until reaching the next <h2> element
        (which is typically "Quotes about [Author]" or "External links",
        which we don't want). Adds the first <ul><li> item to the quote
        list (ignoring the quote's source in a subsequent <li>) and
        finally returns a random quote from that quote list.

    """
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
    """ Gets name of quote author.
    Aligns right, adds conky color coding if enabled (not working).
    """
    author = "-- "
    if enable_conky_color:
        author += "${color " + conky_color + "}"
    author += pages[random_author][1]
    if enable_conky_color:
        author += "${color}"
    author = author.rjust(output_width)
    return author

def main():
    """ Main function.
    Prepares variables, calls functions, outputs results.
    """
    base = "https://en.wikiquote.org/wiki/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                "AppleWebKit/537.36 (KHTML, like Gecko) " +
                "Chrome/114.0.0.0 Safari/537.36"}
    random_author = random.randrange(len(pages))
    url = base + pages[random_author][0]

    page = get_page(url, headers)
    quote = get_quote(page)
    author = get_author(random_author)

    print(quote)
    print(author)

# Execute
main()
