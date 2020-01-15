
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
    # tips_dataset = []
    # with open(filepath+'/tip.json', encoding='utf8') as json_file:
    #     yelp_dataset = list(json_file)

    # Using pandas
    d=[]
    for l in open(filepath+"/tip.json").readlines():
        d.append(json.loads(l))
    df = pd.DataFrame.from_records(d)

    # Q1: How many reviews are there in tip.json?
    print('Q1:', df.count().loc['user_id'])

    # Q2: How many reviews have the maximum length of text among all reviews?
    # print(yelp_dataset[3851]) # example of review with 500 characters
    print('Q2:', df['text'].apply(len).value_counts().loc[500])
    # print(df.loc[lambda df: df['text'].apply(len) == 500].count().loc['user_id']) # another way to do it

    # Q3: We say that a user is "outstanding" if it makes the number of reviews six standard-derivations more than an 
    # average user. (That is, #reviews from a user >= average #reviews of all users + 6*std of #reviews of all users). 
    # How many outstanding users are there?
    user_id_counts = df['user_id'].value_counts()
    outstanding_threshold = user_id_counts.mean() + 6*user_id_counts.std()
    print('Q3:', user_id_counts.loc[lambda df: df >= outstanding_threshold].count())

    return 0

if __name__ == "__main__":
    main()
