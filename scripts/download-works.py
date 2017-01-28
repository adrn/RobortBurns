""" Download all of the works of Robert Burns """

# Standard library
from bs4 import BeautifulSoup
import os
import time
from urllib import request
import json

# Third-party
from astropy import log as logger
import astropy.units as u
import numpy as np

# Project
# ...

root_url = "http://www.robertburns.org/works/"

def clean(text):
    arr = [x for x in text if x.isspace() or x.isalpha() or x not in ["@","#","$","%","^","&"]]
    return ''.join(arr).replace("  ", "\n") # for some reason line breaks come back as two spaces?

def write_poem(filename, id, title, poem):
    """
    Write the poem and metadata to the file if it isn't
    already in there
    """

def main():

    cache_file = "burns-poems.???"

    for i in range(1,559+1): # number of works on website
        url = "http://www.robertburns.org/works/{}.shtml".format(i)
        response = request.urlopen(url)

        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        time.sleep(0.5) # wait half a second so we don't get banned

if __name__ == "__main__":
    main()

