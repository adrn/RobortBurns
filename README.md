Robort Burns
============

Robot Robert Burns.

- Make the corpus `cd scripts; python make_corpus.py`
- Train the RNN `python lstm.py --train --corpus=../cache/corpus.txt`
- Sample new poems `python lstm.py --sample --weights=../cache/weights_XXX.h5 --seed=42` (change
  `XXX` to whatever weights file index you want to use after training)
