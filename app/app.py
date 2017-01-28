import os
os.environ['KERAS_BACKEND'] = 'theano'
os.environ['WEIGHTSPATH'] = '../cache/weights_008.h5'

import numpy as np
from flask import Flask, render_template
app = Flask(__name__)

from lstm import sample

test_text = """Once I lov'd a bonie lass,
Ay, and I love her still;
And whilst that virtue warms my breast,
I'll love my handsome Nell.
As bonie lasses I hae seen,
And mony full as braw;
But, for a modest gracefu' mein,
The like I never saw.
"""

@app.route('/')
@app.route('/<seed>')
def poem(seed=None):
    if seed is None:
        seed = np.random.randint(4294967295) # up to 2**32
        text = sample(seed, nchars=512) # rough number of characters

    elif seed == 'test':
        text = test_text

    else:
        seed = int(seed)
        text = sample(seed, nchars=512) # rough number of characters

    lines = text.split("\n")
    return render_template('poem.html', poem_lines=lines, seed=seed)

if __name__ == '__main__':
    from argparse import ArgumentParser

    # Define parser object
    parser = ArgumentParser(description="")

    parser.add_argument('--debug', action='store_true', dest='debug',
                        default=False, help='Debug mode.')

    args = parser.parse_args()

    app.run(debug=args.debug)
