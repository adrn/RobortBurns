""" Download all of the works of Robert Burns """

# Standard library
from bs4 import BeautifulSoup
import os
from os.path import abspath, exists, join
import time
from urllib import request
import json

cache_path = abspath('../cache')
if not exists(abspath('../scripts')):
    raise RuntimeError('You must run from the scripts directory.')

if not exists(cache_path):
    os.makedirs(cache_path, exist_ok=True)

url_base = "http://www.robertburns.org/works/{}.shtml"

def clean(text):
    arr = [x for x in text if x.isspace() or x.isalpha() or x not in ["@","#","$","%","^","&"]]
    return ''.join(arr).replace("  ", "\n") # for some reason line breaks come back as two spaces?

def get_poem(index):
    response = request.urlopen(url_base.format(index))

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    poem_title = soup.find('h1').get_text()
    poem_title = clean(poem_title)

    poem_text = soup.find('blockquote').get_text()
    poem_text = clean(poem_text).replace("  ", "\n")

    return poem_title, poem_text.strip()

def write_poem(filename, key, title, poem):
    """
    Write the poem and metadata to the file if it isn't
    already in there
    """

    with open(filename, 'r') as f:
        data = json.loads(f.read())

        if key not in data:
            data[key] = dict(title=title, text=poem)

    with open(filename, 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))

def main(index=None):

    cache_file = join(cache_path, "burns-poems.json")
    if not exists(cache_file):
        with open(cache_file, 'w') as f:
            f.write(json.dumps({}, sort_keys=True, indent=4))

    if index is None:
        for i in range(1,559+1): # number of works on website
            print(i)
            title,text = get_poem(i)
            time.sleep(0.25) # wait a bit so we don't get banned
            write_poem(cache_file, str(i), title, text)

    else:
        title,text = get_poem(index)
        print(title)
        print("-"*len(title))
        print(text)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

