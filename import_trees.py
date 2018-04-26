import string

import pandas as pd

from tqdm import tqdm
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle

import logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

#
# Attempts to analyze text to get named entity classification
#
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer
#
# custom_sent_tokenizer = PunktSentenceTokenizer()
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
#
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
#
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         for i in tokenized[5:]:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#             namedEnt = nltk.ne_chunk(tagged, binary=False)
#             namedEnt.draw()
#     except Exception as e:
#         print(str(e))
#
# process_content()

def generate_industries_tree():
    industries_csv = pd.read_csv('data/trees_industry.csv', header=None, names=['L1', 'L2', 'L3', 'L4'])

    l1 = None
    l2 = None
    l3 = None
    l4 = None

    l2_key = None
    l3_key = None
    l4_key = None

    industries = pd.DataFrame(columns=['L1', 'L2', 'L3', 'L4'])
    ind_tree = {}

    for idx, row in industries_csv.iterrows():
        str_l1 = str(row.L1)
        str_l2 = str(row.L2)
        str_l3 = str(row.L3)
        str_l4 = str(row.L4)

        l1_sep = str_l1.find(':')
        if l1_sep != -1:
            l1 = str_l1[l1_sep+1:].strip()
            ind_tree[l1] = {'parent': None, 'value': l1, 'level': 1}
            pass

        if str_l2 != 'nan':
            l2 = str_l2.strip()
            l2_key = ":".join([l1, l2])
            ind_tree[l2_key] = {'parent': l1, 'value': l2, 'level': 2}
        else:
            if l2 is None:
                l2 = ""

        if str_l3 != 'nan':
            l3 = str_l3.strip()
            l3_key = ":".join([l1, l2, l3])
            ind_tree[l3_key] = {'parent': l2_key, 'value': l3, 'level': 3}
        else:
            if l3 is None:
                l3 = ""

        if str_l4 != 'nan':
            l4 = str_l4.strip()
            l4_key = ":".join([l1, l2, l3, l4])
            ind_tree[l4_key] = {'parent': l3_key, 'value': l4, 'level': 4}
        else:
            if l4 is None:
                l4 = ""

        if l1 is not None:
            industries.loc[industries.shape[0]+1] = [l1, l2, l3, l4]
            l4 = None

    # industries.to_csv('data/industries.csv', index_label='idx', header=True)
    pickle.dump(ind_tree, open("data/ind_tree.p", "wb"))


generate_industries_tree()


def generate_sentence_similarity():
    #
    # Attempt to use word net synonyms to infer relevance, not effective hence superseded with word2vec
    #
    industries = pd.read_csv('data/industries.csv', header=0, index_col=0)
    industries = industries.fillna('')

    course_w_geo = pd.read_csv('data/course_w_geo.csv', header=0, index_col=0)
    # stop_words = set(stopwords.words('english'))

    punct_trans = {ord(c): ' ' for c in string.punctuation}
    score_df = pd.DataFrame(columns=['course_title', 'industry', 'score'])
    score_cache = {}
    # Iterate through courses
    for c_idx, c_row in tqdm(course_w_geo.iterrows()):
        course_str = c_row.TITLE.strip()
        course_str = course_str.translate(punct_trans)
        c_word_tokens = word_tokenize(course_str)
        score_cache[course_str] = {}
        # Iterate through Industries
        for t_idx, t_row in industries.iterrows():
            for l in range(1):
                score = 0
                num_syms = 0
                industry_str = t_row[f'L{l+1}'].strip()
                industry_str = industry_str.translate(punct_trans)
                if course_str in score_cache and industry_str in score_cache[course_str]:
                    score = score_cache[course_str][industry_str]
                else:
                    t_word_tokens = word_tokenize(industry_str)
                    for t_tok in t_word_tokens:
                        for c_tok in c_word_tokens:
                            # Find synonym sets for industry and course word tokens
                            t_ss = wn.synsets(t_tok)
                            c_ss = wn.synsets(c_tok)
                            # Sum and average WUP path similarity for all found synonyms
                            for t_s in t_ss:
                                for c_s in c_ss:
                                    t_score = t_s.wup_similarity(c_s)
                                    if t_score:
                                        num_syms = num_syms + 1
                                        score = score + t_score
                    if num_syms > 0:
                        score = score / num_syms
                    logging.debug(f'{course_str} - {industry_str}: {score} ({num_syms})')
                    score_cache[course_str][industry_str] = score

                score_df.loc[score_df.shape[0]+1] = [course_str, industry_str, score]
                pass
        pickle.dump(score_cache, open("data/score_cache.p", "wb"))
        score_df.to_csv('data/course_to_industry_score.csv', index_label='idx', header=True)


# generate_sentence_similarity()
pass
