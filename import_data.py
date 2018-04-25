import pickle
import string

from nltk.corpus import stopwords
from tqdm import tqdm, trange
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

#
# Experiment with XML loading
#
#import xmltodict
# kis_json = xmltodict.parse(open("data/kis20180417140617.xml", "rb"))
# pickle.dump(kis_json, open("data/kis_json.p", "wb"))
# kis_json = pickle.load(open("data/kis_json.p", "rb"))

#
# Use CSV loading instead
#
import pandas as pd
import math

kis_course = pd.read_csv('data/KISCOURSE.csv', header=0)
kis_course = kis_course[['UKPRN', 'KISCOURSEID', 'TITLE', 'LTURL']]

kis_course[['TITLE']] = kis_course[['TITLE']].fillna(value='Course Title Missing')

course_location = pd.read_csv('data/COURSELOCATION.csv', header=0)
course_location = course_location[['UKPRN', 'KISCOURSEID', 'LOCID']]

course_w_course_location = kis_course.merge(course_location, how='left', on=['UKPRN', 'KISCOURSEID'])

location = pd.read_csv('data/LOCATION.csv', header=0)
location = location[['UKPRN', 'LOCID', 'LOCNAME', 'LATITUDE', 'LONGITUDE']]

course_w_location = course_w_course_location.merge(location, how='left', on=['UKPRN', 'LOCID'])

#
# Use Google Maps API to generate addresses from Latitude/Longtitude
#


def generate_addresses(course_w_location):
    import googlemaps

    gmaps = googlemaps.Client(key='AIzaSyDLqwt0ZVwG31W2Sam8pA2eohE4ofyd53A')

    # Cache google maps api queries to avoid unnecessary queries
    use_cache = False
    try:
        loc_tuple_dict = pickle.load(open("data/loc_tuple_dict.p", "rb"))
        use_cache = True
    except FileNotFoundError:
        loc_tuple_dict = {}

    addresses = []
    for idx, row in tqdm(course_w_location.iterrows()):
        loc_tuple = (row.LATITUDE, row.LONGITUDE)
        hash_str = str(loc_tuple)
        if hash_str in loc_tuple_dict:
            address = loc_tuple_dict[hash_str]
            # logging.debug(f'Used cached address for {loc_tuple}')
        elif not math.isnan(row.LOCID):
            try:
                reverse_geocode_result = \
                    gmaps.reverse_geocode((row.LATITUDE, row.LONGITUDE))
                loc_tuple_dict[hash_str] = reverse_geocode_result
                address = reverse_geocode_result

            except googlemaps.exceptions.HTTPError:
                address = []
        else:
            logging.warning(f'No location data for UKPRN:{row.UKPRN} KISCOURSEID:{row.KISCOURSEID}')
            address = []

        addresses.append(address)
        pass

    # Save cache
    if not use_cache:
        pickle.dump(loc_tuple_dict, open("data/loc_tuple_dict.p", "wb"))

    return addresses


# addresses = generate_addresses(course_w_location)

#
# Use addresses to assign GEOGRAPHY field to courses
#


def assign_geography(course_w_location, addresses):
    course_w_geo = course_w_location
    course_w_geo = course_w_geo.assign(GEOGRAPHY="")

    address_errors = pd.DataFrame(columns=['LOCNAME', 'LATITUDE', 'LONGITUDE'])
    for idx, row in tqdm(course_w_geo.iterrows()):
        try:
            found_geography = False
            for addr_comp in addresses[idx][1]['address_components']:
                if 'administrative_area_level_2' in addr_comp['types']:
                    course_w_geo.at[idx, 'GEOGRAPHY'] = addr_comp['long_name']
                    found_geography = True
                    break

            if not found_geography:
                for addr_comp in addresses[idx][1]['address_components']:
                    if 'locality' in addr_comp['types']:
                        course_w_geo.at[idx, 'GEOGRAPHY'] = addr_comp['long_name']
                        found_geography = True
                        break

            if not found_geography:
                logging.debug(f'Locality not found for {idx}')
                address_errors.loc[address_errors.shape[0]] = [row.LOCNAME, row.LATITUDE, row.LONGITUDE]
        except IndexError:
            logging.debug(f'Address error: \n {row.LOCNAME}, {row.LATITUDE}, {row.LONGITUDE}')
            address_errors.loc[address_errors.shape[0]] = [row.LOCNAME, row.LATITUDE, row.LONGITUDE]
            pass

    logging.warning('Unable to get Google Map address for:')
    logging.warning(address_errors.drop_duplicates())

    course_w_geo = course_w_geo[course_w_geo.GEOGRAPHY != '']
    course_w_geo = course_w_geo.assign(UNIQKEY=course_w_geo.index)
    course_w_geo.to_csv('data/course_w_geo.csv', index_label='idx', header=True)


# assign_geography(course_w_location, addresses)
course_w_geo = pd.read_csv('data/course_w_geo.csv', header=0, index_col=0)
course_w_geo = course_w_geo.drop_duplicates(subset=['UKPRN', 'KISCOURSEID'])
course_w_geo = course_w_geo.reindex()


def upload_to_elastics(course_w_geo):
    from nltk.tokenize import word_tokenize
    from elasticsearch import Elasticsearch
    import re

    industries = pd.read_csv('data/industries.csv', header=0, index_col=0)
    industries_level_1 = industries.L1
    industries_level_1 = industries_level_1.drop_duplicates()

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    punct_trans = {ord(c): ' ' for c in string.punctuation}
    remove_words = ['a', 'for', 'the']

    for idx, row in tqdm(course_w_geo.iterrows()):
        body = row.to_dict()

        course_keywords_str = body['TITLE'].translate(punct_trans)
        course_keywords_arr = word_tokenize(course_keywords_str)
        course_keywords_arr = [word for word in course_keywords_arr if word not in stopwords.words('english')]
        course_keywords_arr = [i for i in course_keywords_arr if i.lower() not in remove_words]

        matched_industries = []
        for ind_idx, ind_item in industries_level_1.iteritems():
            ind_item_str = str(ind_item)
            ind_item_str = ind_item_str.replace('And ', '')
            ind_item_arr = re.split('; |, ', ind_item_str)
            ind_item_arr = list(map(str.strip, ind_item_arr))

            for ind_term in ind_item_arr:
                for course_term in course_keywords_arr:
                    if len(course_term) > 2 and course_term in ind_term:
                        if ind_term not in matched_industries:
                            matched_industries.append(ind_term)
                        break

        if len(matched_industries) > 0:
            print(course_keywords_arr, matched_industries)

        body['INDUSTRY_MAP'] = matched_industries

        es.index(index='pf_idx', doc_type='courses_w_geo', id=idx, body=body)


upload_to_elastics(course_w_geo)
pass
