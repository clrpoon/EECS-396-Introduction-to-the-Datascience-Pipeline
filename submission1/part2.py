
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import pandas as pd

def main():
    filepath = sys.argv[1] #filepath to yelp yelp-dataset

    business=[]
    for l in open(filepath+"/business.json").readlines():
        business.append(json.loads(l))
    df_business = pd.DataFrame.from_records(business)

    # Known Arizona Addresses
    az_businesses = df_business.loc[df_business['state'] == 'AZ']
    print(az_businesses)

    # Check for businesses with missing state field
    missing_state_businesses = df_business.loc[df_business['state'] == '']
    print(missing_state_businesses.empty)

    # Check for businesses with Arizona for state field
    arizona_businesses = df_business.loc[df_business['state'] == 'Arizona']
    print(arizona_businesses.empty)

    # Check for capitalization issues
    az_cities = az_businesses['city'].map(lambda city: city.lower())

    print(list(az_cities.unique()))

    return 0

if __name__ == "__main__":
    main()
