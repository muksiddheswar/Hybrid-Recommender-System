#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:53:06 2019

@author: smkj33
"""


def importContentQuery ():
    sql = "SELECT uid, title, bodytext FROM tx_news_domain_model_news WHERE deleted = 0"
    return sql


def importMetadataQuery():
    sql = """ 
    SELECT 
    t1.uid article_ID , 
    t1.title title , 
    GROUP_CONCAT(t3.title SEPARATOR ', ') category,
    GROUP_CONCAT(t5.title SEPARATOR ', ') tags, 
    t1.bodytext bodytext
    
    FROM 
    tx_news_domain_model_news t1 
    
    LEFT JOIN 
    sys_category_record_mm t2 
    ON t2.uid_foreign = t1.uid 
    
    LEFT JOIN 
    sys_category t3 
    ON t3.uid = t2.uid_local
    
    LEFT JOIN
    tx_news_domain_model_news_tag_mm t4
    ON t4.uid_local = t1.uid
    
    LEFT JOIN
    tx_news_domain_model_tag t5
    ON t5.uid = t4.uid_foreign
    
    GROUP BY t1.uid , t1.title , t1.bodytext
    """
    return sql
