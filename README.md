# Yelp-Scraper
This python application is intended to scrape the Yelp website for the results located when searching for a query/location combination and then return the results in an interesting manner. Still in development.


TO DO:
    1) Find out why the search/scrape for places is duplicating some locations.
        a) Fix this functionality.
    2) Add in a fix to allow a user to choose a start location.
        a) Then implement the OSRM Trip functionality to allow for trips of specified number of stops.
        b) Also add in way for user to specify number of stops they want to make.
            i) Make sure to include default max/None if not specified.
    3) Should look into making a Location object/class so that I can clean up the code related to individual locations instead of making such a cluttered mess everywhere.
        a) Would allow me to instead track a list of Locations instead of a list of tuples with tons of information.
    4) Fix the output on the GUI screen.
        a) Namely, fix tabbing/spacing issues.
        b) Also need to look into turning this into a list of selectable items somehow. Again, might be easier if using a Location class.
    5) Create a .exe/executable file using either pyInstaller or py2exe (whichever will work appropriately).

