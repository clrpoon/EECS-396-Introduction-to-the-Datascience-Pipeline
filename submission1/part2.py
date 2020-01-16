
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import string
import pandas as pd

def main():
    filepath = sys.argv[1] #filepath to yelp yelp-dataset
    
    """
    HELPER FUNCTIONS
    """
     # Removes all "az" from each city name
    def remove_az(city_name):
        if city_name == 'az':
            return ''
        elif city_name.split(' ')[-1] == 'az':
            return ' '.join(city_name.split(' ')[:-1])
        else:
            return city_name

    # Convert first letter of each word back to uppercase
    def convert_to_pronoun(word):
        tokens = word.split(' ')
        for i in range(len(tokens)):
            if len(tokens[i]) >= 2:
                tokens[i] = tokens[i][0].upper() + tokens[i][1:]
            elif len(tokens[i]) == 1:
                tokens[i] = tokens[i][0].upper()
        return ' '.join(tokens)

    business=[]
    for l in open(filepath+"/business.json", encoding="utf8").readlines():
        business.append(json.loads(l))
    df_business = pd.DataFrame.from_records(business)

    # Known Arizona Addresses
    az_businesses = df_business.loc[df_business['state'] == 'AZ']
    # print(az_businesses)

    # Check for businesses with missing state field
    # missing_state_businesses = df_business.loc[df_business['state'] == '']
    # print(missing_state_businesses.empty)

    # Check for businesses with Arizona for state field
    # arizona_businesses = df_business.loc[df_business['state'] == 'Arizona']
    # print(arizona_businesses.empty)
    
    # Removes all punctuation
    az_businesses.city = az_businesses.city.apply(lambda city: city.translate(str.maketrans('', '', string.punctuation)))

    # Fixes lower/upper case incosistencies
    az_businesses.city = az_businesses.city.apply(lambda city: city.lower())
    
   
    az_businesses.city = az_businesses.city.apply(remove_az)

    # Removes empty cities
    az_businesses = az_businesses.drop(az_businesses[az_businesses.city == ''].index)

    # Remove vestigial encoding errors
    # may need to add more later
    az_businesses.city = az_businesses.city.apply(lambda city: city.replace(u'\u200b', ''))

    # Convert cities back to pronouns
    az_businesses.city = az_businesses.city.apply(convert_to_pronoun)

    print(list(az_businesses.city.unique()))

    return 0


if __name__ == "__main__":
    main()
