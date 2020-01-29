
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import string
import pandas as pd
import editdistance as ed
from geopy.geocoders import Nominatim


def main():
    filepath = sys.argv[1] #filepath to yelp yelp-dataset
    #print(len(['Phoenix', 'Goodyear', 'Glendale', 'Scottsdale', 'Mesa', 'Gilbert', 'Litchfield Park', 'Tempe', 'Peoria', 'Chandler', 'Surprise', 'Buckeye', 'Queen Creek', 'Avondale', 'Cave Creek', 'Sun City', 'Sun City West', 'Carefree', 'El Mirage', 'Paradise Valley', 'Fountain Hills', 'Tolleson', 'Sun Lakes', 'Apache Junction', 'Youngtown', 'Somerton', 'Guadalupe', 'Rio Verde', 'New River', 'Sedona', 'Snowflake', 'Ak-Chin Village', 'Ajo', 'Arizona Village', 'Maricopa', 'Tucson']))
    """
    HELPER FUNCTIONS
    """
    az_city_list = ['Phoenix', 'Tucson', 'Mesa', 'Scottsdale', 'Chandler', 'Glendale', 'Gilbert', 'Tempe', 'Peoria', 'Surprise', 'Yuma', 'Avondale', 'Goodyear', 'Flagstaff', 'Buckeye', 'Casa Grande', 'Lake Havasu City', 'Maricopa', 'Marana', 'Prescott Valley', 'Prescott', 'Oro Valley', 'Apache Junction', 'Queen Creek', 'Sierra Vista', 'Bullhead City', 'El Mirage', 'San Luis', 'Sahuarita', 'Kingman', 'Fountain Hills', 'Florence', 'Nogales', 'Eloy', 'Douglas', 'Payson', 'Paradise Valley', 'Somerton', 'Coolidge', 'Cottonwood', 'Chino Valley', 'Show Low', 'Camp Verde', 'Sedona', 'Winslow', 'Safford', 'Page', 'Wickenburg', 'Globe', 'Tolleson', 'Youngtown', 'Guadalupe', 'Litchfield Park', 'Snowflake', 'South Tucson', 'Cave Creek', 'Bisbee', 'Eagar', 'Holbrook', 'Thatcher', 'Colorado City', 'Benson', 'Pinetop-Lakeside', 'Clarkdale', 'Taylor', 'Dewey-Humboldt', 'Carefree', 'Clifton', 'St. Johns', 'Quartzsite', 'Willcox', 'Williams', 'Superior', 'Wellton', 'Parker', 'Pima', 'Star Valley', 'Kearny', 'Gila Bend', 'Springerville', 'Miami', 'Huachuca City', 'Mammoth', 'Fredonia', 'Tombstone', 'Patagonia', 'Duncan', 'Tusayan', 'Hayden', 'Jerome', 'Winkelman']
    geopy_cache = {}
    geolocator = Nominatim(user_agent="specify_your_app_name_here")

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
    

    def get_city_from_latlong(latlong):
        loc = geolocator.reverse(latlong)
        address = loc.raw['address']
        if 'city' in address:
            return address['city']
        elif 'town' in address:
            return address['town']
        else:
            return ''
    
        
    def validate_row(row):
        # check city
        if row.city in az_city_list:        # perfect match
            return row
        if row.city in geopy_cache:         #already found via geopy
            row.city = geopy_cache[row.city]
            return row

        # ping api with latlong to get city
        # print('calling geopy for city name:', row.city)  
        geopy_city = get_city_from_latlong(row.latlong)
        geopy_cache[row.city] = geopy_city
        row.city = geopy_city
        return row

    """ MAIN BODY """
    business = []
    for l in open(filepath+"/business.json", encoding="utf8").readlines():
        business.append(json.loads(l))
    df_business = pd.DataFrame.from_records(business)

    # Known Arizona Addresses
    az_businesses = df_business.loc[df_business['state'] == 'AZ']
    
    # Removes all punctuation
    az_businesses.city = az_businesses.city.apply(lambda city: city.translate(str.maketrans('', '', string.punctuation)))

    # Fixes lower/upper case incosistencies
    az_businesses.city = az_businesses.city.apply(lambda city: city.lower())
    
    # remove 'az' city name cases
    az_businesses.city = az_businesses.city.apply(remove_az)
    # check lat and longitude

    # Remove vestigial encoding errors
    az_businesses.city = az_businesses.city.apply(lambda city: city.replace(u'\u200b', ''))

    # Convert cities back to pronouns
    az_businesses.city = az_businesses.city.apply(convert_to_pronoun)

    # validate each row for proper cities
    az_businesses['latlong'] = az_businesses.latitude.map(str) + ', ' + az_businesses.longitude.map(str)
    az_businesses= az_businesses.apply(validate_row, axis=1, result_type='expand')

    #print('printing df')
    #print(az_businesses)
    #removes failures
    az_businesses = az_businesses.drop(az_businesses[az_businesses.city == ''].index)
    print(list(az_businesses.city.unique()))
    print(len(list(az_businesses.city.unique())))


    return 0


if __name__ == "__main__":
    main()


