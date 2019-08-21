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





# Requried for connection to MySQL db
import pymysql
from db_config import *


# DB Queries generated in here
from queries import *

from bs4 import BeautifulSoup


import re



def import_content ():

    try:
        conn = pymysql.connect(**connection_properties)
        sql = importMetadataQuery()
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)



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


# REMOVE FROM HERE
def get_recommendations(title, cosine_sim):

    # Get the index of the article that matches the title
    # article_index = article_map['local_index'].loc[article_map['title'] == title].item()
    article_index_ser = article_map['local_index'].loc[article_map['title'] == title]
    article_index = next(iter(article_index_ser), 'no match')

    # Get the similarity scores
    """
    #-- Retrieve similarity scores corrosponding to the articles from the db 
    """

    # Get the pairwsie similarity scores of all articles with that article
    sim_scores = list(enumerate(cosine_sim[article_index]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar articles
    sim_scores = sim_scores[1:11]

    # Get the article indices
    article_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    # return article_master['title'].iloc[article_indices]
    return article_map['title'].iloc[article_indices]




#-------------------------------------#
# MODEL CREATE DRIVER
#-------------------------------------#



article_master = import_content()


#-------------------------------------#
## Preprocess Content
#-------------------------------------#


# REDUCE CONTENT:
article_master['reduced_content'] = article_master.apply(lambda row: re.sub('[^a-z\s]', '',filter_html(row.bodytext).lower()), axis = 1)

#-- Potential Global Variable
porter = PorterStemmer()
article_master['stemmed_content'] = article_master.apply(lambda row: porter_stemmer(row.reduced_content, porter), axis = 1)



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
cosine_sim_content = linear_kernel(tfidf_matrix_content, tfidf_matrix_content)



tfidf_matrix_title = tfidf.fit_transform(article_master['stemmed_title'])
cosine_sim_title = linear_kernel(tfidf_matrix_title, tfidf_matrix_title)

#-- Potential Global Variable
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(article_master["meta_soup"])
cosine_sim_cat_tags = cosine_similarity(count_matrix, count_matrix)


# FINAL SIMILARITY MATRIX
cosine_sim = (cosine_sim_content + 0.5 * cosine_sim_title +
              0.5 * cosine_sim_cat_tags)/3

"""
#-- At this point the newly calculated similarity model can be written to the database.
"""




article_map = (article_master[['article_ID','title']].copy()).drop_duplicates()
article_map['local_index'] = article_map.index



"""
#-- At this point the newly index map can be written to the database.
"""






# print(get_recommendations('The ICP VR event at Hannover Messe 2018', cosine_sim))
# pd.set_option('max_colwidth', 100)
print(get_recommendations('Utilize all the available energy — Heat recovery', cosine_sim))

