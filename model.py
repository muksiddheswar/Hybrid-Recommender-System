#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:56:07 2019

@author: smkj33
"""
import pandas as pd

# Requried for connection to MySQL db
import pymysql
from db_config import *

# DB Queries generated in here
from queries import *

# Text Parsing Packages
from html.parser import HTMLParser



# Strips HTML tags from text
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    ret = ''.join([x.strip() for x in s.get_data().split('\r\n')])
    return ret

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)




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




def parse_content ():
    article_master = import_content()
    article_master['reduced_content'] = article_master.apply(lambda row: strip_tags(row.bodytext).lower(), axis = 1)

    pd.set_option('max_colwidth', 100)
    print(article_master['reduced_content'])
    # article_master['reduced_content'] = article_master.apply(lambda row: ((row.content).lower()), axis = 1)


parse_content()