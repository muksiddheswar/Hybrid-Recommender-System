#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:12:23 2019

@author: smkj33
"""



import pandas as pd

# TfIdfVectorizer from scikit-learn for text
from sklearn.feature_extraction.text import TfidfVectorizer


# Import CountVectorizer to create count matrix for tags
# This is an alternative to tfidf
from sklearn.feature_extraction.text import CountVectorizer


# Requried to tokenise the text before Stemming
from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.stem import PorterStemmer
from porter2stemmer import Porter2Stemmer

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




#-------------------------------------#
# MODEL EXPORT HELPER FUNCTIONS
#-------------------------------------#

def matrix_to_jason(matrix):
    df = pd.DataFrame(matrix.apply(lambda row: row.to_json(), axis=1), columns = ['jsol_col'])
    df['local_id'] = df.index
    return df


def export_content_similarity (similarity_matrix):
    df = matrix_to_jason(similarity_matrix)
    sql = export_content_similarity_query()
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

# porter = PorterStemmer()
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




"""
#-- At this point the newly stemmed metadata content can be written to the database.
"""

#-------------------------------------#
## Preprocess Content - End
#-------------------------------------#



# MODEL CREATION

# Define a TF-IDF Vectorizer Object.
# Remove all english stop words such as 'the', 'a'
# tfidf = TfidfVectorizer(stop_words='english')
# tfidf_matrix_content = tfidf.fit_transform(article_master['stemmed_content'])
#
# tfidf_matrix_content =
# ts_ss_content =



#
# import pymysql
# from queries import *
# from db_config import *
#
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.stem import PorterStemmer
#
#
# import pandas as pd
#
# def import_content ():
#
#     try:
#         conn = pymysql.connect(**connection_properties)
#         sql = importContentQuery()
#         df = pd.read_sql(sql, conn)
#
#         #closing database connection.
#         if(conn.open):
#             conn.close()
#             print("MySQL connection is closed")
#
#         return df
#
#     except Exception as e :
#         print ("Error while connecting to MySQL", e)
#
#
#
# def export_content(df):
#
#     conn = pymysql.connect(**connection_properties)
#     cursor = conn.cursor()
#
#     try:
#         sql = """
#         INSERT INTO `recen_test` (`uid`, `json_col1`)
#         VALUES(%s, %s)
#         """
#         df.apply(lambda row: cursor.execute(sql, (row.local_id, row.jsol_col1)), axis = 1)
#         conn.commit()
#     	# conn.commit()
#
#         #closing database connection.
#         if(conn.open):
#             # conn.commit()
#             conn.close()
#             print("MySQL connection is closed")
#
#
#     except Exception as e :
#         print ("Error while connecting to MySQL", e)
#
#
#
# # article_master = import_content()
# # # article_master.apply(lambda x: print(x.to_json()), axis=1)
# # df = pd.DataFrame(article_master.apply(lambda row: row.to_json(), axis=1), columns = ['jsol_col1'])
# # df['local_id'] = df.index
# # export_content(df)
# # # print(df)
#
#
#
# def export_map_1(df):
#     sql = export_article_map_query()
#     # """
#     # INSERT INTO `recen_article_map` (`local_id`,`article_id`,`title`)
#     # VALUES(%s, %s, %s)
#     # """
#     conn = pymysql.connect(**connection_properties)
#     cursor = conn.cursor()
#     # sql = export_article_map_query()
#
#     try:
#         df.apply(lambda row: cursor.execute(sql, (row.local_id, row.article_id, row.title )), axis = 1)
#         conn.commit()
#
#         #closing database connection.
#         if(conn.open):
#             conn.close()
#             print("MySQL connection is closed")
#
#
#     except Exception as e :
#         print ("Error while connecting to MySQL", e)
#
#
#
#
#
# # req = {'article_id': [1011,1019,1022],
# #         'duration': [120,300,50]
# #         }
#
# # df = pd.DataFrame(req ,columns= ['article_id', 'duration'])
#
# # print (df)
#
#
#
#
#
#
# req = {'article_id': [1011, 1019, 1022], 'duration': [120, 300, 50]}
# df = pd.DataFrame(req)
# x = (get_local_id(df['article_id']))
# # print(get_local_id(df['article_id']))
# # print(get_similarity(get_local_id(df['article_id'])))
# pd.set_option('max_colwidth', 10)
# sim = get_similarity(x)
#
#
# content_sim = sim['content_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))
# title_sim = sim['title_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))
# cat_tags_sim = sim['cat_tags_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))
#
#
# # print(content_sim)
#
#
#
#
# # def text_soup_filter(text):
# #     soup = BeautifulSoup(text, features="html5lib")
# #     text = re.sub('[^a-z\s]', '',soup.get_text(separator=' ').lower())
# #     return text
#
#
#
# # article_master['reduced_content'] = article_master.apply(
# #             lambda row: text_soup_filter(row.bodytext), axis = 1)
#
#
# # article_master['reduced_content'] = article_master.apply(
# #         lambda row: BeautifulSoup(row.bodytext).get_text().lower(), axis = 1)
#
#
#
# # porter = PorterStemmer()
# # def porter_stemmer (txt):
# #     token_words=word_tokenize(txt)
# #     stem_sentence=[]
# #     for word in token_words:
# #         stem_sentence.append(porter.stem(word))
# #         stem_sentence.append(" ")
# #     return "".join(stem_sentence)
#
# # article_master['reduced_content_stemmed_nonum'] = article_master.apply(
# #         lambda row: porter_stemmer(re.sub('[^a-z\s]', '',BeautifulSoup(row.bodytext).get_text(separator=' ').lower())), axis = 1)
#
#
# # print(article_master)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # from html.parser import HTMLParser
#
#
# # # Strips HTML tags from text
# # def strip_tags(html):
# #     s = MLStripper()
# #     s.feed(html)
# #     # return s.get_data()
# #     ret = ''.join([x.strip() for x in s.get_data().split('\r\n')])
# #     return ret
#
# # class MLStripper(HTMLParser):
# #     def __init__(self):
# #         self.reset()
# #         self.strict = False
# #         self.convert_charrefs= True
# #         self.fed = []
# #     def handle_data(self, d):
# #         self.fed.append(d)
# #     def get_data(self):
# #         return ''.join(self.fed)
#
#
#
# # def import_content ():
# #     # user = 'root'
# #     # password = 'log'
# #     # db = 'db426841_843'
# #     # host = '127.0.0.1'
#
# #     # conn = pymysql.connect(host, user, password, db)
# #     conn = pymysql.connect(**connection_properties)
#
# #     cursor = conn.cursor()
#
# #     try:
# #         sql = importContentQuery()
# #         cursor.execute(sql)
# #         rows = cursor.fetchall()
#
# #         for x in rows:
# #             print("Id = ", x[0], )
# #             print("Title = ", x[1])
# #             print("Content  = ", strip_tags(x[2]))
# #             # desired_string = ''.join([x.strip() for x in str(strip_tags(x[2])).split('\r\n')])
# #             # print(desired_string )
# #         cursor.close()
#
# #     except Exception as e :
# #         print ("Error while connecting to MySQL", e)
#
# #     finally:
# #         #closing database connection.
# #         if(conn.open):
# #             conn.close()
# #             print("MySQL connection is closed")
#
#
