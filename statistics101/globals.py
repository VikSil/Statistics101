from .models import Source

# ----------------------------------------------------------------------------
# This module contains global variables that are used throughout the website
# All are initialised when the server is started
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Navigation pane defines website structure and contains information to:
#     * construct floating menu on layout template
#     * dynamically add paths to urls.py
#     * refer to check inline link validity in templates
# ----------------------------------------------------------------------------
global NAVIGATION_PANE
NAVIGATION_PANE = {
    "data": {
        "long": "Data",
        "type": "dict",
        "links": {
            "qqdata": "Types of Data",
            "popsample": "Population & Sample",
            "surveys": "Surveys",
            "experiments": "Experiments",
        },
    },
    "stats": {
        "long": "Statistics",
        "type": "dict",
        "links": {
            "mean": "Mean",
            "median": "Median",
            "stdev": "Standard Deviation",
            "percentiles": "Percentiles",
        },
    },
    "charts": {
        "long": "Charts",
        "type": "dict",
        "links": {
            "piechart": "Pie Chart",
            "barchart": "Bar Graph",
            "histogram": "Histogram",
            "linechart": "Line Graph",
            "boxplot": "Boxplot",
        },
    },
    "ds": {
        "long": "Data Sets",
        "type": "dict",
        "links": {
            "inbuilts": "Inbuilt Data Sets",
            "userdata": "My Data Sets",
        },
    },
    "sources": {
        "long": "Sources",
        "type": "str",
        "links": "sources",
    },
}


def order_sources():
    """
    Retrieves all data from Sources model and sorts it
    according to the source type in alphabetical order,
    depending on what information about the source is available

    Is called upon server initialisaion and assigned to
    ALL_SOURCES global variable.

    ALL_SOURCES is used by sources template and get_source_number() in utils.py
    """

    # Initialise the collection to look like Sources model
    all_sources = Source.objects.none()
    # Get all books from DB
    books = Source.objects.filter(SourceType=1).values()
    book_dict = {}
    # Create a string representing each book
    for book in books:
        if book["Editorial"]:
            source = book["Author"] + " eds.: " + book["Title"] + "."
        else:
            source = book["Author"] + ": " + book["Title"] + "."
        if book["Place"]:
            source = (
                source
                + " "
                + book["Place"]
                + ": "
                + book["Publisher"]
                + " "
                + str(book["Year"])
            )
        else:
            source = source + ": " + book["Publisher"] + " " + str(book["Year"])
        if book["ISBN10"]:
            source = source + ", ISBN10: " + book["ISBN10"]
        if book["ISBN13"]:
            source = source + ", ISBN13: " + book["ISBN13"]

        # Add the book into a dictionary
        book_dict[book["id"]] = source.lower()
    # Sort the book dictionary by value alphabetically and reassign keys in that order
    book_dict = dict(sorted(book_dict.items(), key=lambda item: item[1]))
    # Add books into the sources collection
    for key in book_dict:
        all_sources |= books.filter(id=key)

    # To be added once there are sources of coresponding type in the DB
    videos = Source.objects.filter(SourceType=2).values()
    publications = Source.objects.filter(SourceType=3).values()

    # Get all websites from DB
    websites = Source.objects.filter(SourceType=4).values()
    website_dict = {}
    # Create a string representing each video
    for website in websites:
        if website["Container"]:
            source = website["Container"] + ": " + website["Title"]
        else:
            source = website["Title"]
        if website["Author"]:
            source = source + " by " + website["Author"]
        if website["Publisher"]:
            source = source + ", in domain of " + website["Publisher"]
        if website["FullDate"]:
            source = source + ", last accessed " + str(website["FullDate"])
        else:
            source = source + ", last accessed " + str(website["Year"])
        source = source + ", " + website["URL"]
        # Add website into a dictionary
        website_dict[website["id"]] = source.lower()
    # Sort the website dictionary by value alphabetically and reassign keys in that order
    website_dict = dict(sorted(website_dict.items(), key=lambda item: item[1]))
    # Add website into the sources collection
    for key in website_dict:
        all_sources |= websites.filter(id=key)

    # Get all references to external datasets from DB
    datasets = Source.objects.filter(SourceType=5).values()
    dataset_dict = {}
    # Create a string representing each reference to external dataset
    for dataset in datasets:
        if dataset["Container"]:
            source = dataset["Container"] + ": " + dataset["Title"]
        else:
            source = dataset["Title"]
        if dataset["Author"]:
            source = source + " by " + dataset["Author"]
        if dataset["Publisher"]:
            source = source + ", in domain of " + dataset["Publisher"]
        if dataset["FullDate"]:
            source = source + ", last accessed " + str(dataset["FullDate"])
        else:
            source = source + ", last accessed " + str(dataset["Year"])
        source = source + ", " + dataset["URL"]
        # Add references to datasets into a dictionary
        dataset_dict[dataset["id"]] = source.lower()
    # Sort dictionary by value alphabetically and reassign keys in that order
    dataset_dict = dict(sorted(dataset_dict.items(), key=lambda item: item[1]))
    # Add references to external datasets into the sources collection
    for key in dataset_dict:
        all_sources |= datasets.filter(id=key)

    # Return ordered collection
    return all_sources


global ALL_SOURCES
ALL_SOURCES = order_sources()
