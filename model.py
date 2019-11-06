#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 18:00:07 2019

@author: smkj33
"""



"""
Previous Version: 
    bkp_model_20_Aug.py

-- Removing html filter using HTML.parser 
-- Removing related import statement
-- Beautiful soup will be used in it's place'


    bkp_model_19_Oct.py 
    
--  Replaced Potter Stemmer with Snowball Stemmer
--  Added Cosine similarity with TS-SS.

"""


import pandas as pd
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



from db_functions import *
from queries import *





#-------------------------------------#
# MODEL CREATE HELPER FUNCTIONS
#-------------------------------------#



def filter_html(text):
    soup = BeautifulSoup(text, features="html5lib")
    # text = re.sub('[^a-z\s]', '',soup.get_text(separator=' ').lower())
    text = soup.get_text(separator=' ')
    return text


def text_stemmer (txt, stemmer):
    token_words=word_tokenize(txt)
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(stemmer.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def clean_tags(x):
    if isinstance(x, str):
        return str.lower(x.replace(" ", "")).replace(","," ")

    else:
        return ''


def get_theta(cosine_similarity):
    sim = np.divide(np.trunc(np.multiply(cosine_similarity, 100000000000000)), 100000000000000)
    angles = np.arccos(sim) + math.radians(10)
    return angles


def get_magnitude(matrix):
    magnitude = np.sqrt(matrix.multiply(matrix).sum(1))
    return magnitude


def get_euclidean(vectors):
    magnitudes = euclidean_distances(vectors)
    return magnitudes


#-------------------------------------#
# MODEL EXPORT HELPER FUNCTIONS
#-------------------------------------#

def matrix_to_json(matrix):
    df = pd.DataFrame(matrix.apply(lambda row: row.to_json(), axis=1), columns = ['data_col'])
    df['local_id'] = df.index
    return df


def export_content_cosine_similarity (similarity_matrix):
    df = matrix_to_json(similarity_matrix)
    sql = export_content_cosine_similarity_query()
    export_data(df, sql)


def export_title_similarity (similarity_matrix):
    df = matrix_to_json(similarity_matrix)
    sql = export_title_similarity_query()
    export_data(df, sql)


def export_cat_tags_similarity (similarity_matrix):
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


def export_content_magnitude(vector_size):
    df = matrix_to_json(vector_size)
    df['local_id'] = df.index
    sql = export_content_magnitude_query()
    export_data(df, sql)


#-------------------------------------#
# MODEL CREATE DRIVER
#-------------------------------------#


truncate_similarities()
article_master = import_content()



## PREPROCESS CONTENT
print("Previous Model Truncated.")
print("Pre-processing....")


# REDUCE CONTENT:
article_master['reduced_content'] = article_master.apply\
    (lambda row: re.sub('[^a-z\s]', '',filter_html(row.bodytext).lower()), axis = 1)

#-- Potential Global Variable

snowball = Porter2Stemmer()

article_master['stemmed_content'] = article_master.apply\
    (lambda row: text_stemmer(row.reduced_content, snowball), axis = 1)

article_master['stemmed_content'] = article_master['stemmed_content'].fillna('')



# REDUCE TITLE:
# It must be noted that numbers are removed from the content and not from the title
article_master['reduced_title'] = article_master.apply\
    (lambda row: re.sub('[^a-z0-9\s]', '',row.title.lower()), axis = 1)

article_master['stemmed_title'] = article_master.apply\
    (lambda row: text_stemmer(row.reduced_title, snowball), axis = 1)



# REDUCE TAGS AND CATEGORY
article_master['reduced_category'] = article_master['category'].apply(clean_tags)
article_master['reduced_tags'] = article_master['tags'].apply(clean_tags)
article_master["meta_soup"] = article_master["reduced_category"] + ' ' + article_master['reduced_tags']



#-------------------------------------#
## Preprocess Content - End
#-------------------------------------#

print("Creating new Model.")

# MODEL CREATION

# Define a TF-IDF Vectorizer Object for Un-normalised TF-IDF vectors
# Remove all english stop words such as 'the', 'a'


tfidf = TfidfVectorizer(stop_words = 'english', norm = None)
tfidf_vectors = tfidf.fit_transform(article_master['stemmed_content'])


cosine_sim_content = cosine_similarity(tfidf_vectors)

# Export content similarity matrix
df = pd.DataFrame.from_records(cosine_sim_content)
export_content_cosine_similarity(df)
print("Exported Content Cosine Similarity Matrix .")

# Theta, Euclidean Distance and Magnitude of TF-IDF vectors: required for TS-SS similarity
angles = get_theta(cosine_sim_content)
euclidean_distance = get_euclidean(tfidf_vectors)
vector_magnitude = get_magnitude(tfidf_vectors)

# Export Theta matrix
df = pd.DataFrame.from_records(angles)
export_content_angles(df)

# Export Euclidean Distance  matrix
df = pd.DataFrame.from_records(euclidean_distance)
export_content_distance(df)

# Export Vector Magnitudes
df = pd.DataFrame.from_records(vector_magnitude)
export_content_magnitude(df)

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



