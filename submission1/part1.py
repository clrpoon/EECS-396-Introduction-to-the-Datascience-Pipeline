
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import pandas as pd

def main():
    filepath = sys.argv[1] #filepath to yelp yelp-dataset

    """
    QUESTIONS 1 & 2

    """
    # Load jsonl file
    tips_dataset = []
    with open(filepath+'/tip.json', encoding='utf8') as json_file:
        yelp_dataset = list(json_file)

    # Q1: How many reviews are there in tip.json?
    print('Q1:', len(yelp_dataset))

    # Q2: How many reviews have the maximum length of text among all reviews?
    print(yelp_dataset[0])
    return 0

if __name__ == "__main__":
    main()
