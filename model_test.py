#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:12:23 2019

@author: smkj33
"""

import pymysql
from queries import *
from db_config import *

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer



def import_content ():

    try:
        conn = pymysql.connect(**connection_properties)
        sql = importContentQuery()
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)


def text_soup_filter(text):
    soup = BeautifulSoup(text, features="html5lib")
    text = re.sub('[^a-z\s]', '',soup.get_text(separator=' ').lower())
    return text

article_master = import_content()

# article_master['reduced_content'] = article_master.apply(
#             lambda row: text_soup_filter(row.bodytext), axis = 1)


# article_master['reduced_content'] = article_master.apply(
#         lambda row: BeautifulSoup(row.bodytext).get_text().lower(), axis = 1)



porter = PorterStemmer()
def porter_stemmer (txt):
    token_words=word_tokenize(txt)
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

article_master['reduced_content_stemmed_nonum'] = article_master.apply(
        lambda row: porter_stemmer(re.sub('[^a-z\s]', '',BeautifulSoup(row.bodytext).get_text(separator=' ').lower())), axis = 1)


print(article_master)
















# from html.parser import HTMLParser


# # Strips HTML tags from text
# def strip_tags(html):
#     s = MLStripper()
#     s.feed(html)
#     # return s.get_data()
#     ret = ''.join([x.strip() for x in s.get_data().split('\r\n')])
#     return ret

# class MLStripper(HTMLParser):
#     def __init__(self):
#         self.reset()
#         self.strict = False
#         self.convert_charrefs= True
#         self.fed = []
#     def handle_data(self, d):
#         self.fed.append(d)
#     def get_data(self):
#         return ''.join(self.fed)



# def import_content ():
#     # user = 'root'
#     # password = 'log'
#     # db = 'db426841_843'
#     # host = '127.0.0.1'

#     # conn = pymysql.connect(host, user, password, db)
#     conn = pymysql.connect(**connection_properties)

#     cursor = conn.cursor()
    
#     try:
#         sql = importContentQuery()
#         cursor.execute(sql)
#         rows = cursor.fetchall()

#         for x in rows:
#             print("Id = ", x[0], )
#             print("Title = ", x[1])
#             print("Content  = ", strip_tags(x[2]))
#             # desired_string = ''.join([x.strip() for x in str(strip_tags(x[2])).split('\r\n')])
#             # print(desired_string )
#         cursor.close()
    
#     except Exception as e :
#         print ("Error while connecting to MySQL", e)
    
#     finally:
#         #closing database connection.
#         if(conn.open):
#             conn.close()
#             print("MySQL connection is closed")


