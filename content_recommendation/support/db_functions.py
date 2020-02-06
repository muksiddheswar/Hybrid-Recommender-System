#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 14:37:14 2019

@author: smkj33
"""



#-------------------------------------#
# DB R/W FUNCTIONS
#-------------------------------------#


import pandas as pd
import numpy as np

# Requried for connection to MySQL db
import pymysql
from db_config import *
from queries import *



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


def export_data(df, sql):

    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()

    try:
        df.apply(lambda row: cursor.execute(sql, (row.local_id, row.data_col)), axis = 1)
        conn.commit()

        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")


    except Exception as e :
        print ("Error while connecting to MySQL", e)


def export_map(df):
    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()
    sql = export_article_map_query()

    try:
        df.apply(lambda row: cursor.execute(sql, (row.local_id, row.article_id, row.title )), axis = 1)
        conn.commit()

        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")

    except Exception as e :
        print ("Error while connecting to MySQL", e)


def get_local_id(article_id):
    id_string = ''
    for index, row in enumerate(article_id):
        if index > 0:
            id_string += ', '
        id_string += str(row)

    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()
    sql = get_local_id_query() % id_string

    try:
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
           conn.close()
           print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)


def get_article(local_id):
    id_string = ''
    for i, index in enumerate(np.nditer(local_id)):
        if i > 0:
            id_string += ', '
        id_string += str(index)

    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()
    sql = get_article_query() % id_string

    try:
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
           conn.close()
           print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)


def get_similarity(local_id):
    id_string = ''
    for index, row in local_id.iterrows():
        if index > 0:
            id_string += ', '
        id_string += str(row['local_id'])

    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()
    sql = get_similarity_query() % id_string

    try:
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
           conn.close()
           print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)


def get_ts_ss_similarity(local_id):
    id_string = ''
    for index, row in local_id.iterrows():
        if index > 0:
            id_string += ', '
        id_string += str(row['local_id'])

    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()
    sql = get_ts_ss_similarity_query() % id_string

    try:
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
           conn.close()
           print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)


def truncate_similarities():

    conn = pymysql.connect(**connection_properties)
    queries = get_truncate_query()
    cursor = conn.cursor()
    try:
        for index, sql in enumerate(queries):
            cursor.execute(sql)

        if (conn.open):
            conn.close()
            print("MySQL connection is closed")
        return

    except Exception as e :
        print ("Error while connecting to MySQL", e)