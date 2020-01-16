
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import pandas as pd

def main():
    filepath = sys.argv[1] #filepath to yelp yelp-dataset

    # Load jsonl file
    # tips_dataset = []
    # with open(filepath+'/tip.json', encoding='utf8') as json_file:
    #     yelp_dataset = list(json_file)

    # Using pandas
    d=[]
    for l in open(filepath+"/tip.json", encoding="utf8").readlines():
        d.append(json.loads(l))
    df = pd.DataFrame.from_records(d)

    business=[]
    for l in open(filepath+"/business.json", encoding="utf8").readlines():
        business.append(json.loads(l))
    df_business = pd.DataFrame.from_records(business)

    # Q1: How many reviews are there in tip.json?
    print('Q1:', df.count().loc['user_id'])

    # Q2: How many reviews have the maximum length of text among all reviews?
    # print(yelp_dataset[3851]) # example of review with 500 characters
    print('Q2:',df.loc[lambda df: df['text'].apply(len) == df['text'].apply(len).max()].count().loc['user_id']) # another way to do it

    # Q3: We say that a user is "outstanding" if it makes the number of reviews six standard-derivations more than an 
    # average user. (That is, #reviews from a user >= average #reviews of all users + 6*std of #reviews of all users). 
    # How many outstanding users are there?
    user_id_counts = df['user_id'].value_counts()
    outstanding_threshold = user_id_counts.mean() + 6*user_id_counts.std()
    print('Q3:', user_id_counts.loc[lambda df: df >= outstanding_threshold].count())

    # Q4: What is the name of the location with the most reviews? 
    # (Hint: you may need to join multiple JSON files using pandas)
    business_id_counts = df['business_id'].value_counts()
    business_most_reviews = df_business.loc[df_business['business_id'] == business_id_counts.idxmax()]
    print('Q4:', business_most_reviews['name'].values[0])

    # Q5: In the above location, which hour has the least number of reviews? 
    # (Hint: the answer should be an integer from [0, 23])
    reviews = df.loc[df['business_id'] == business_id_counts.idxmax()]
    reviews_date = reviews.date.map(lambda review: review.split(" ")[1].split(":")[0])
    print('Q5:', reviews_date.value_counts().idxmin())

    return 0

if __name__ == "__main__":
    main()
