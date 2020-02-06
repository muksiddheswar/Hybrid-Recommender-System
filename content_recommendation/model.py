#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 18:00:07 2019

@author: smkj33
"""

import pandas as pd
import os
import re
import math
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.stem import PorterStemmer
from porter2stemmer import Porter2Stemmer

from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics import pairwise_distances

from content_recommendation.support.db_functions import *
from content_recommendation.support.queries import *


# -------------------------------------#
# MODEL CREATE HELPER FUNCTIONS
# -------------------------------------#

def filter_html(text):
    soup = BeautifulSoup(text, features="html5lib")
    # text = re.sub('[^a-z\s]', '',soup.get_text(separator=' ').lower())
    text = soup.get_text(separator=' ')
    return text


def text_stemmer(txt, stemmer):
    token_words = word_tokenize(txt)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(stemmer.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def clean_tags(x):
    if isinstance(x, str):
        return str.lower(x.replace(" ", "")).replace(",", " ")

    else:
        return ''


def theta(cosine_similarity):
    sim = np.divide(np.trunc(np.multiply(cosine_similarity, 100000000000000)), 100000000000000)
    angles = np.arccos(sim) + math.radians(10)
    return angles


def magnitude_and_difference(matrix):
    magnitude = np.sqrt(matrix.multiply(matrix).sum(1))
    magnitude_diff = pairwise_distances(magnitude, metric='manhattan')
    return magnitude, magnitude_diff


def euclidean(vectors):
    distances = euclidean_distances(vectors)
    return distances


# -------------------------------------#
# MODEL EXPORT HELPER FUNCTIONS
# -------------------------------------#

def matrix_to_json(matrix):
    df = pd.DataFrame(matrix.apply(lambda row: row.to_json(), axis=1), columns=['data_col'])
    df['local_id'] = df.index
    return df


def export_content_cosine_similarity(similarity_matrix):
    df = matrix_to_json(similarity_matrix)
    sql = export_content_cosine_similarity_query()
    export_data(df, sql)


def export_title_similarity(similarity_matrix):
    df = matrix_to_json(similarity_matrix)
    sql = export_title_similarity_query()
    export_data(df, sql)


def export_cat_tags_similarity(similarity_matrix):
    df = matrix_to_json(similarity_matrix)
    sql = export_cat_tags_similarity_query()
    export_data(df, sql)


def export_content_angles(angles):
    df = matrix_to_json(angles)
    sql = export_content_angles_query()
    export_data(df, sql)


def export_content_distance(distance):
    df = matrix_to_json(distance)
    sql = export_content_distance_query()
    export_data(df, sql)


def export_ts_ss(ts_ss_sim_matrix):
    df = matrix_to_json(ts_ss_sim_matrix)
    sql = export_ts_ss_query()
    export_data(df, sql)


# -------------------------------------#
# MODEL CREATE DRIVER
# -------------------------------------#


truncate_similarities()
# In case the data is read from the database then the following is required.
# article_master = import_content()


# LOCAL IMPORT
article_master = pd.read_csv(os.path.abspath("./data/content_metadata.csv"))

## PREPROCESS CONTENT
print("Previous Model Truncated.")
print("Pre-processing....")

# REDUCE CONTENT:
article_master['reduced_content'] = article_master.apply \
    (lambda row: re.sub('[^a-z\s]', '', filter_html(row.bodytext).lower()), axis=1)


snowball = Porter2Stemmer()

article_master['stemmed_content'] = article_master.apply \
    (lambda row: text_stemmer(row.reduced_content, snowball), axis=1)

article_master['stemmed_content'] = article_master['stemmed_content'].fillna('')

# REDUCE TITLE:
# It must be noted that numbers are removed from the content and not from the title
article_master['reduced_title'] = article_master.apply \
    (lambda row: re.sub('[^a-z0-9\s]', '', row.title.lower()), axis=1)

article_master['stemmed_title'] = article_master.apply \
    (lambda row: text_stemmer(row.reduced_title, snowball), axis=1)

# REDUCE TAGS AND CATEGORY
article_master['reduced_category'] = article_master['category'].apply(clean_tags)
article_master['reduced_tags'] = article_master['tags'].apply(clean_tags)
article_master["meta_soup"] = article_master["reduced_category"] + ' ' + article_master['reduced_tags']

# -------------------------------------#
## Preprocess Content - End
# -------------------------------------#

print("Creating new Model.")

# MODEL CREATION

# Define a TF-IDF Vectorizer Object for Un-normalised TF-IDF vectors
# Remove all english stop words such as 'the', 'a'


tfidf = TfidfVectorizer(stop_words='english', norm=None)
tfidf_vectors = tfidf.fit_transform(article_master['stemmed_content'])

cosine_sim_content = cosine_similarity(tfidf_vectors)

# Export content similarity matrix
df = pd.DataFrame.from_records(cosine_sim_content)
export_content_cosine_similarity(df)
print("Exported Content Cosine Similarity Matrix .")



# Theta, Euclidean Distance and Magnitude of TF-IDF vectors: required for TS-SS similarity
angles = theta(cosine_sim_content)
euclidean_distance = euclidean(tfidf_vectors)
magnitude , magnitude_diff = magnitude_and_difference(tfidf_vectors)
ed_md_square = np.square(euclidean_distance + magnitude_diff)
magnitude_product = linear_kernel(magnitude)
sine_theta = np.sin(angles)
const = (0.5 * np.pi) * 360


ts_ss = np.multiply(magnitude_product, sine_theta, ed_md_square) * const
ts_ss = np.multiply(ts_ss,angles)


# Export Ts_ss similarity matrix
df = pd.DataFrame.from_records(ts_ss)
export_ts_ss(df)


# Export Theta matrix
df = pd.DataFrame.from_records(angles)
export_content_angles(df)

# Export Euclidean Distance  matrix
df = pd.DataFrame.from_records(euclidean_distance)
export_content_distance(df)

# Export Vector Magnitudes
# df = pd.DataFrame.from_records(diff_squares)
# export_content_magnitude(df)

print("Exported Content TS-SS Similarity Matrices .")




# Define a TF-IDF Vectorizer Object for normalised TF-IDF vectors
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix_title = tfidf.fit_transform(article_master['stemmed_title'])
cosine_sim_title = linear_kernel(tfidf_matrix_title, tfidf_matrix_title)

# Export title similarity matrix
df = pd.DataFrame.from_records(cosine_sim_title)
export_title_similarity(df)
print("Exported Title Cosine Similarity Matrix .")



count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(article_master["meta_soup"])
cosine_sim_cat_tags = cosine_similarity(count_matrix, count_matrix)

# Export title similarity matrix
df = pd.DataFrame.from_records(cosine_sim_cat_tags)
export_cat_tags_similarity(df)
print("Exported Tags/Category Cosine Similarity Matrix .")


article_map = (article_master[['article_id','title']].copy()).drop_duplicates()
article_map['local_id'] = article_map.index

# Export article_map
export_map(article_map)

print("Model Created")



