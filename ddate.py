#!/usr/bin/env python
#
# Converts Gregorian date to Discordian date.
#
# If no argument, converts the current date.
# If argument in Gregorian ISO format of YYYY-MM-DD, converts that date.

import calendar
import datetime
import sys

# Date to convert
if len(sys.argv) > 1:
    gregorian = datetime.date.fromisoformat(sys.argv[1])
else:
    gregorian = datetime.datetime.today()

# Variables
day_of_year = gregorian.timetuple().tm_yday
year = gregorian.year + 1166
season = ""
day = ""
holyday = ""
leap = False

# Leap year
if calendar.isleap(gregorian.year):
    leap = True
    if day_of_year > 60:
        day_of_year -= 1

# Calculate
if leap and day_of_year == 60:
    season = ""
    day = ""
    holyday = "St. Tib's Day"
elif day_of_year <= 73:
    season = "Chaos"
    day = str(day_of_year)
    if day_of_year == 5:
        holyday = "Mungday"
    if day_of_year == 50:
        holyday = "Chaoflux"
elif day_of_year <= 146:
    season = "Discord"
    day = str(day_of_year % 73)
    if day_of_year == 78:
        holyday = "Mojoday"
    if day_of_year == 123:
        holyday = "Discoflux"
elif day_of_year <= 219:
    season = "Confusion"
    day = str(day_of_year % 146)
    if day_of_year == 151:
        holyday = "Syaday"
    if day_of_year == 196:
        holyday = "Confluflux"
elif day_of_year <= 292:
    season = "Bureaucracy"
    day = str(day_of_year % 219)
    if day_of_year == 224:
        holyday = "Zaraday"
    if day_of_year == 269:
        holyday = "Bureflux"
elif day_of_year <= 365:
    season = "The Aftermath"
    day = str(day_of_year % 292)
    if day_of_year == 297:
        holyday = "Maladay"
    if day_of_year == 342:
        holyday = "Afflux"

# Print
if season == "":
    print(f"Today is {holyday}, {year} YOLD.")
elif holyday != "":
    print(f"Today is {holyday}, {season} {day}, {year} YOLD.")
else:
    print(f"Today is {season} {day}, {year} YOLD.")
