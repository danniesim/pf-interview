import pickle
import string

from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from tqdm import tqdm, trange
import logging


logging.basicConfig(level=logging.WARNING, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

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
    from gensim.models import Word2Vec
    from gensim.models import KeyedVectors
    import re
    import numpy as np
    from scipy import spatial
    import math

    # industries = pd.read_csv('data/industries.csv', header=0, index_col=0)
    ind_tree = pickle.load(open("data/ind_tree.p", "rb"))

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    punct_trans = {ord(c): ' ' for c in string.punctuation}
    course_remove_words = ['a', 'for', 'the']
    generalized_remove_words = ['', 'a', 'for', 'the', 'and', 'or', 'of', 'nec', 's', 'other']
    generalized_truncation_phrases = ['except ', 'exc. ', 'other than ', 'not ', 'without ', 'no ']

    def tokenize_subject_phrase(course_str):
        word_tokens = word_tokenize(course_str)
        words_wo_stop_words = [word for word in word_tokens if word not in stopwords.words('english')]
        tokens = [i for i in words_wo_stop_words if i.lower() not in course_remove_words]
        return tokens

    def tokenize_industry_tree_item(item):
        ind_str = str(item)
        ind_str = ind_str.replace('And ', '')
        ind_str = ind_str.replace('and ', '')
        ind_arr = re.split('; |, ', ind_str)
        return list(map(str.strip, ind_arr))

    def tokenize_generalized(item):
        item_str = str(item).lower()
        for truncation_phrase in generalized_truncation_phrases:
            item_str = item_str.split(truncation_phrase, 1)[0]
        word_list = re.split('[^a-z]', item_str)
        word_list = [word for word in word_list if word not in generalized_remove_words]
        return word_list

    model = KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)
    num_features = 300
    cutoff = 0.42

    # from nltk.corpus import state_union
    # model = Word2Vec(state_union.sents())
    # model.save('data/state_union_vectors.bin')

    # model = Word2Vec.load('data/state_union_vectors.bin')
    # num_features = 100
    # cutoff = 0.7

    def get_avg_vec(tokens_to_vec):
        ind_vec_sum = np.zeros((num_features,), dtype='float32')
        ind_vec_num = 0
        ind_vec_num_match = 0
        for token in tokens_to_vec:
            try:
                ind_vec_sum = ind_vec_sum + model.wv[token]
                ind_vec_num_match = ind_vec_num_match + 1
            except KeyError as e:
                pass
                # logging.warning(e)
            ind_vec_num = ind_vec_num + 1

        return ind_vec_sum / ind_vec_num, ind_vec_num_match

    sim_cache = {}
    # sim_cache = pickle.load(open("data/sim_cache.p", "rb"))

    for idx, row in tqdm(course_w_geo.iterrows()):
        body = row.to_dict()

        course_keywords_str = body['TITLE']
        # course_tokens = tokenize_subject_phrase(course_keywords_str)
        course_tokens = tokenize_generalized(course_keywords_str)

        course_vec_avg, course_vec_num_match = get_avg_vec(course_tokens)

        matched_industries = {}

        if course_keywords_str not in sim_cache:
            sim_cache[course_keywords_str] = {}

        for node_key in ind_tree:

            def get_industry_full_tree_path(node):
                tokens = [node]
                current_node = node

                while current_node['parent'] is not None:
                    current_node = ind_tree[current_node['parent']]
                    tokens.append(current_node)

                return tokens

            ind_tree_path_nodes = get_industry_full_tree_path(ind_tree[node_key])

            for ind_tree_node in ind_tree_path_nodes:
                ind_str = ind_tree_node['value']
                if ind_str not in sim_cache[course_keywords_str]:
                    # Cosine distance of avg vectors of words in sentence
                    ind_tokens = tokenize_generalized(ind_str)
                    # ind_tokens = tokenize_industry_tree_item(ind_tree_token)
                    ind_avg_vec, ind_num_match = get_avg_vec(ind_tokens)
                    sim = 1 - spatial.distance.cosine(ind_avg_vec, course_vec_avg)

                    # Word Movers Distance
                    # sim = 1 - model.wmdistance(course_keywords_str, ind_tree_token)

                    sim_cache[course_keywords_str][ind_str] = sim
                else:
                    sim = sim_cache[course_keywords_str][ind_str]

                # logging.debug(f'{sim}: {ind_tree_token}: {course_keywords_str}')
                if not math.isnan(sim) and sim > cutoff:
                    if ind_tree_node['industry_cat'] not in matched_industries:
                        matched_industries[ind_tree_node['industry_cat']] = []

                    if ind_str not in matched_industries[ind_tree_node['industry_cat']]:
                        matched_industries[ind_tree_node['industry_cat']].append(ind_str)

            #
            # Old string matching method
            #
            # for ind_term in ind_tokens:
            #     for course_token in course_tokens:
            #         if len(course_token) > 3 and course_token in ind_term:
            #             if ind_term not in matched_industries:
            #                 matched_industries.append(ind_term)
                break

        for ind_cat in matched_industries:
            if len(matched_industries[ind_cat]) > 0:
                logging.warning(f'{course_keywords_str}, {matched_industries[ind_cat]}')

            body[f'INDUSTRY_MAP_{ind_cat}'] = matched_industries[ind_cat]

        es.index(index='pf_idx_ind_cat', doc_type='courses_w_geo', id=idx, body=body)
        if not (idx % 1000):
            pickle.dump(sim_cache, open("data/sim_cache.p", "wb"))


upload_to_elastics(course_w_geo)
pass
