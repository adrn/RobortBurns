""" Turn JSON file of poems into a single text file """

# Standard library
import os
from os.path import abspath, exists, join
import json

cache_path = abspath('../cache')
if not exists(abspath('../scripts')):
    raise RuntimeError('You must run from the scripts directory.')

if not exists(cache_path):
    os.makedirs(cache_path, exist_ok=True)

def main(index=None):

    cache_file = join(cache_path, "burns-poems.json")
    corpus_file = join(cache_path, "corpus.txt")
    char_indices_file = join(cache_path, "char_indices.json")

    with open(cache_file, 'r') as f:
        data = json.loads(f.read())

    all_poems = []
    for key in data:
        all_poems.append(data[key]['text'])

    fulltext = "\n".join(all_poems)
    with open(corpus_file, "w") as f:
        f.write(fulltext)

    chars = sorted(list(set(fulltext.lower())))
    print('total chars:', len(chars))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    with open(char_indices_file, "w") as f:
        f.write(json.dumps({'chars': chars,
                            'char_indices': char_indices,
                            'indices_char': indices_char},
                           indent=4))

if __name__ == "__main__":
    main()

