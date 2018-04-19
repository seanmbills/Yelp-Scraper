# Yelp-Scraper
This python application is intended to scrape the Yelp website for the results located when searching for a query/location combination and then return the results in an interesting manner. Still in development.\n


TO DO:\n
    1) Find out why the search/scrape for places is duplicating some locations.\n
        a) Fix this functionality.\n
            NOTE: seems to be iterating through the same page's results over and over again.\n
    2) Add in a fix to allow a user to choose a start location.\n
        a) Then implement the OSRM Trip functionality to allow for trips of specified number of stops.\n
        b) Also add in way for user to specify number of stops they want to make.\n
            i) Make sure to include default max/None if not specified.\n
    3) Should look into making a Location object/class so that I can clean up the code related to individual locations instead of making such a cluttered mess everywhere.\n
        a) Would allow me to instead track a list of Locations instead of a list of tuples with tons of information.\n
    4) Fix the output on the GUI screen.\n
        a) Namely, fix tabbing/spacing issues.\n
        b) Also need to look into turning this into a list of selectable items somehow. Again, might be easier if using a Location class.\n
    5) Create a .exe/executable file using either pyInstaller or py2exe (whichever will work appropriately).\n
    6) Look into finding a better API to replace the geopy one currently in use as it seems to be struggling to identify quite a few of the addresses given to it.\n
    7) Need to revisit the efficiencies of the overall order in which things occur. Doesn't necessarily make sense to generate all of these lists and then run analysis on the entirety of the list after its generation. Probably makes more sense to get the coordinates of items as they're scraped from the page, as this should cut down on run-time. \n
        a) Consider moving the geopy (or other) API calls to when the information is generated from the scraping to avoid running geopy on the entirety of the list later, causing bad run-time.\n
        b) Currently has an absolutely terrible runtime with larger datasets (aka hundreds of addresses to generate coordinates for).\n
        c) Potential Fix: don't even add locations to the list if they don't contain the targeted search city. This should serve to cut down on many of the offending locations that cause the run time to increase.\n
    8) Should try to declutter the main "search" method. Right now the majority of code is here and makes for a bit of a mess.\n
        a) Try to break things out into separate files if possible.\n
        b) Try to at least break things out into separate methods to clean up code and allow for better readability.\n

