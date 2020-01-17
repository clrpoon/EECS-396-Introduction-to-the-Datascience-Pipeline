
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
    #return 0
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
    
    az_city_list = ['Ajo', 'Ak-Chin Village', 'Amado', 'Apache Junction', 'Arizona City', 'Arizona Village', 'Ash Fork', 'Avondale', 'Avra Valley', 'Bagdad', 'Benson', 'Big Park', 'Bisbee', 'Bitter Springs', 'Black Canyon City', 'Blackwater', 'Bluewater', 'Bouse', 'Buckeye', 'Bullhead City', 'Burnside', 'Cameron', 'Camp Verde', 'Canyon Day', 'Carefree', 'Casa Grande', 'Casas Adobes', 'Catalina', 'Catalina Foothills', 'Cave Creek', 'Central Heights-Midland City', 'Chandler', 'Chilchinbito', 'Chinle', 'Chino Valley', 'Chuichu', 'Cibecue', 'Cibola', 'Clarkdale', 'Claypool', 'Clifton', 'Colorado City', 'Congress', 'Coolidge', 'Cordes Lakes', 'Cornville', 'Corona de Tucson', 'Cottonwood', 'Cottonwood-Verde Village', 'Dennehotso', 'Desert Hills', 'Dewey-Humboldt', 'Dilkon', 'Dolan Springs', 'Douglas', 'Drexel-Alvernon', 'Drexel Heights', 'Dudleyville', 'Duncan', 'Eagar', 'East Fork', 'East Sahuarita', 'Ehrenberg', 'Elgin', 'El Mirage', 'Eloy', 'First Mesa', 'Flagstaff', 'Florence', 'Flowing Wells', 'Fort Defiance', 'Fortuna Foothills', 'Fountain Hills', 'Fredonia', 'Gadsden', 'Ganado', 'Gila Bend', 'Gilbert', 'Gisela', 'Glendale', 'Globe', 'Gold Camp', 'Golden Valley', 'Goodyear', 'Grand Canyon Village', 'Greasewood', 'Green Valley', 'Guadalupe', 'Hayden', 'Heber-Overgaard', 'Holbrook', 'Hotevilla-Bacavi', 'Houck', 'Huachuca City', 'Jeddito', 'Jerome', 'Kachina Village', 'Kaibab', 'Kaibito', 'Kayenta', 'Keams Canyon', 'Kearny', 'Kingman', 'Kykotsmovi Village', 'Lake Havasu City', 'Lake Montezuma', 'Lechee', 'Leupp', 'Litchfield Park', 'Littletown', 'Lukachukai', 'McNary', 'Mammoth', 'Many Farms', 'Marana', 'Maricopa', 'Mayer', 'Mesa', 'Mesquite Creek', 'Miami', 'Moenkopi', 'Mohave Valley', 'Mojave Ranch Estates', 'Morenci', 'Mountainaire', 'Munds Park', 'Naco', 'Nazlini', 'New Kingman-Butler', 'New River', 'Nogales', 'Oljato-Monument Valley', 'Oracle', 'Oro Valley', 'Page', 'Paradise Valley', 'Parker', 'Parker Strip', 'Parks', 'Patagonia', 'Paulden', 'Payson', 'Peach Springs', 'Peeples Valley', 'Peoria', 'Peridot', 'Phoenix', 'Picture Rocks', 'Pima', 'Pine', 'Pinetop-Lakeside', 'Pinon', 'Pirtleville', 'Pisinemo', 'Poston', 'Prescott', 'Prescott Valley', 'Quartzsite', 'Queen Creek', 'Queen Valley', 'Red Mesa', 'Rio Rico Northeast', 'Rio Rico Northwest', 'Rio Rico Southeast', 'Rio Rico Southwest', 'Rio Verde', 'Rock Point', 'Rough Rock', 'Round Rock', 'Sacaton', 'Safford', 'Sahuarita', 'St. David', 'St. Johns', 'St. Michaels', 'Salome', 'San Carlos', 'San Luis', 'San Manuel', 'Santan', 'Santa Rosa', 'Sawmill', 'Scottsdale', 'Second Mesa', 'Sedona', 'Seligman', 'Sells', 'Shongopovi', 'Shonto', 'Show Low', 'Sierra Vista', 'Sierra Vista Southeast', 'Snowflake', 'Somerton', 'Sonoita', 'South Tucson', 'Springerville', 'Spring Valley', 'Stanfield', 'Steamboat', 'Strawberry', 'Summit', 'Sun City', 'Sun City West', 'Sun Lakes', 'Sun Valley', 'Supai', 'Superior', 'Surprise', 'Swift Trail Junction', 'Tacna', 'Tanque Verde', 'Taylor', 'Teec Nos Pos', 'Tempe', 'Thatcher', 'Three Points', 'Tolleson', 'Tombstone', 'Tonalea', 'Tonto Basin', 'Top-of-the-World', 'Tortolita', 'Tsaile', 'Tubac', 'Tuba City', 'Tucson', 'Tucson Estates', 'Tumacacori-Carmen', 'Tusayan', 'Vail', 'Valencia West', 'Wellton', 'Wenden', 'Whetstone', 'Whiteriver', 'Wickenburg', 'Wilhoit', 'Willcox', 'Williams', 'Williamson', 'Willow Valley', 'Window Rock', 'Winkelman', 'Winslow', 'Winslow West', 'Yarnell', 'Young', 'Youngtown', 'Yuma']
    geopy_cache = {}
    geolocator = Nominatim(user_agent="specify_your_app_name_here")

    spelling_mistakes = {}
    #"latitude":33.4896269,"longitude":-112.3487379
    #loc = geolocator.reverse('33.582406, -111.680802')
    #loc_raw = loc.raw
    #print(loc_raw)
    #return 0
    #more_failed_geopy = []

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

        
        # check for typos
       # distances = []
        #for c in az_city_list:
         #   distances.append(ed.eval(row.city, c))

        #min_distance = min(distances)
        # if distance less than length, return corrected spelling
        #if min_distance < len(row.city):
         #   if row.city not in spelling_mistakes :
          #      spelling_mistakes[row.city] = az_city_list[distances.index(min_distance)]
           # row.city = az_city_list[distances.index(min_distance)]
            #return row
        

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
    #az_businesses = az_businesses.drop(az_businesses[az_businesses.city == ''].index)

    # Remove vestigial encoding errors
    az_businesses.city = az_businesses.city.apply(lambda city: city.replace(u'\u200b', ''))

    # Convert cities back to pronouns
    az_businesses.city = az_businesses.city.apply(convert_to_pronoun)

    # validate each row for proper cities
    az_businesses['latlong'] = az_businesses.latitude.map(str) + ', ' + az_businesses.longitude.map(str)
    az_businesses= az_businesses.apply(validate_row, axis=1, result_type='expand')

    print('printing df')
    print(az_businesses)
    #removes failures
    az_businesses = az_businesses.drop(az_businesses[az_businesses.city == ''].index)
    print(list(az_businesses.city.unique()))
    print(len(list(az_businesses.city.unique())))

    print('-------------SPELLING MISTAKES CAUGHT-------------')
    print(spelling_mistakes)
    print('--------------------NOT A SPELLING MISTAKE-----------------------')
    print(geopy_cache.keys())

    return 0


if __name__ == "__main__":
    main()


