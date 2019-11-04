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

"""


import pandas as pd

# TfIdfVectorizer from scikit-learn for text
from sklearn.feature_extraction.text import TfidfVectorizer


# Import CountVectorizer to create count matrix for tags
# This is an alternative to tfidf
from sklearn.feature_extraction.text import CountVectorizer


# Requried to tokenise the text before Stemming
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

# Import linear_kernel for Cosine Similarity calculation of bodytext and title
# This wil be applied on a tfidf matrix and NOT a count matrix
from sklearn.metrics.pairwise import linear_kernel

# Compute the Cosine Similarity matrix based on a count_matrix
from sklearn.metrics.pairwise import cosine_similarity



# Funtions interacting with the database
from db_functions import *

# DB Queries generated in here
from queries import *

from bs4 import BeautifulSoup


import re


#-------------------------------------#
# MODEL CREATE HELPER FUNCTIONS
#-------------------------------------#



def filter_html(text):
    soup = BeautifulSoup(text, features="html5lib")
    # text = re.sub('[^a-z\s]', '',soup.get_text(separator=' ').lower())
    text = soup.get_text(separator=' ')
    return text



def text_stemmer(article_master, porter):
    # The following line produces the stem of every word and then removes all non alphabet characters
    article_master['stemmed_content'] = article_master.apply(lambda row: porter_stemmer(re.sub('[^a-z\s]', '', row.reduced_content), porter), axis = 1)
    article_master['stemmed_content'] = article_master['stemmed_content'].fillna('')
    return article_master


def porter_stemmer (txt, porter):
    token_words=word_tokenize(txt)
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def clean_tags(x):
    if isinstance(x, str):
        return str.lower(x.replace(" ", "")).replace(","," ")

    else:
        return ''




#-------------------------------------#
# MODEL EXPORT HELPER FUNCTIONS
#-------------------------------------#

def matrix_to_jason(matrix):
    df = pd.DataFrame(matrix.apply(lambda row: row.to_json(), axis=1), columns = ['jsol_col'])
    df['local_id'] = df.index
    return df


def export_content_similarity (similarity_matrix):
    df = matrix_to_jason(similarity_matrix)
    sql = export_content_cosine_similarity_query()
    export_data(df, sql)


def export_title_similarity (similarity_matrix):
    df = matrix_to_jason(similarity_matrix)
    sql = export_title_similarity_query()
    export_data(df, sql)


def export_cat_tags_similarity (similarity_matrix):
    df = matrix_to_jason(similarity_matrix)
    sql = export_cat_tags_similarity_query()
    export_data(df, sql)





#-------------------------------------#
# MODEL CREATE DRIVER
#-------------------------------------#



article_master = import_content()



## PREPROCESS CONTENT



# REDUCE CONTENT:
article_master['reduced_content'] = article_master.apply\
    (lambda row: re.sub('[^a-z\s]', '',filter_html(row.bodytext).lower()), axis = 1)

#-- Potential Global Variable
porter = PorterStemmer()
article_master['stemmed_content'] = article_master.apply\
    (lambda row: porter_stemmer(row.reduced_content, porter), axis = 1)



# REDUCE TITLE:
# It must be noted that numbers are removed from the content and not from the title
article_master['reduced_title'] = article_master.apply(lambda row: re.sub('[^a-z0-9\s]', '',row.title.lower()), axis = 1)
article_master['stemmed_title'] = article_master.apply(lambda row: porter_stemmer(row.reduced_title, porter), axis = 1)



# REDUCE TAGS AND CATEGORY
article_master['reduced_category'] = article_master['category'].apply(clean_tags)
article_master['reduced_tags'] = article_master['tags'].apply(clean_tags)
article_master["meta_soup"] = article_master["reduced_category"] + ' ' + article_master['reduced_tags']




"""
#-- At this point the newly stemmed metadata content can be written to the database.
"""

#-------------------------------------#
## Preprocess Content - End
#-------------------------------------#



# MODEL CREATION

# Define a TF-IDF Vectorizer Object.
# Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix_content = tfidf.fit_transform(article_master['stemmed_content'])


# Create additional step that uses TS-SS similarity.
cosine_sim_content = linear_kernel(tfidf_matrix_content, tfidf_matrix_content)

# Export content similarity matrix
df = pd.DataFrame.from_records(cosine_sim_content)
export_content_similarity(df)




tfidf_matrix_title = tfidf.fit_transform(article_master['stemmed_title'])
cosine_sim_title = linear_kernel(tfidf_matrix_title, tfidf_matrix_title)

# Export title similarity matrix
df = pd.DataFrame.from_records(cosine_sim_title)
export_title_similarity(df)



#-- Potential Global Variable
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(article_master["meta_soup"])
cosine_sim_cat_tags = cosine_similarity(count_matrix, count_matrix)

# Export title similarity matrix
df = pd.DataFrame.from_records(cosine_sim_cat_tags)
export_cat_tags_similarity(df)



article_map = (article_master[['article_id','title']].copy()).drop_duplicates()
article_map['local_id'] = article_map.index

# Export article_map
export_map(article_map)

print("Model Created")



