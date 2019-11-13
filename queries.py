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
    t1.uid article_id , 
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


def export_content_cosine_similarity_query():
    sql = """
    INSERT INTO `recen_cosine_sim_content` (`local_id`, `scores`)
    VALUES(%s, %s)
    """
    return sql


def export_title_similarity_query():
    sql = """
    INSERT INTO `recen_cosine_sim_title` (`local_id`, `scores`)
    VALUES(%s, %s)
    """
    return sql

def export_cat_tags_similarity_query():
    sql = """
    INSERT INTO `recen_cosine_sim_cat_tags` (`local_id`, `scores`)
    VALUES(%s, %s)
    """
    return sql

def export_article_map_query():
    sql = """
    INSERT INTO `recen_article_map` (`local_id`,`article_id`,`title`)
    VALUES(%s, %s, %s)
    """
    return sql


def export_content_similarity_query():
    sql = """
    INSERT INTO `recen_cosine_sim_content` (`local_id`, `scores`)
    VALUES(%s, %s)
    """
    return sql


def export_content_angles_query():
    sql = """
    INSERT INTO `recen_theta_content` (`local_id`, `angle`)
    VALUES(%s, %s)
    """
    return sql


def export_content_distance_query():
    sql = """
    INSERT INTO `recen_distance_content` (`local_id`, `distance`)
    VALUES(%s, %s)
    """
    return sql


def export_content_magnitude_query():
    sql = """
    INSERT INTO `recen_magnitude_content` (`local_id`, `magnitude_diff_square`)
    VALUES(%s, %s)
    """
    return sql

def export_ts_ss_query():
    sql = """
    INSERT INTO `recen_ts_ss_content` (`local_id`, `scores`)
    VALUES(%s, %s)
    """
    return sql


def get_local_id_query():
    sql = """
    SELECT local_id FROM `recen_article_map` 
    WHERE article_id IN (%s)
    """
    return sql

def get_article_query():
    sql = """
    SELECT article_id, title FROM `recen_article_map` 
    WHERE local_id IN (%s)
    """
    return sql

def get_similarity_query():
    sql = """
    SELECT con.local_id local_id, con.scores content_sim, 
    tit.scores title_sim, tag.scores cat_tags_sim
    FROM
    recen_cosine_sim_content con
    LEFT JOIN
    recen_cosine_sim_title tit
    ON con.local_id = tit.local_id
    LEFT JOIN
    recen_cosine_sim_cat_tags tag
    on con.local_id = tag.local_id
    WHERE con.local_id IN (%s)
    """
    return sql

def get_ts_ss_similarity_query():
    sql = """
    SELECT local_id , scores FROM recen_ts_ss_content
    WHERE local_id IN (%s)
    """
    return sql


def get_truncate_query():
    sql1 = """TRUNCATE TABLE recen_cosine_sim_content;"""
    sql2 = """TRUNCATE TABLE recen_cosine_sim_title;"""
    sql3 = """TRUNCATE TABLE recen_cosine_sim_cat_tags;"""
    sql4 = """TRUNCATE TABLE recen_article_map;"""
    sql5 = """TRUNCATE TABLE recen_theta_content;"""
    sql6 = """TRUNCATE TABLE recen_distance_content;"""
    # sql7 = """TRUNCATE TABLE recen_magnitude_content;"""
    sql7 = """TRUNCATE TABLE recen_ts_ss_content"""

    sql = [sql1, sql2, sql3, sql4, sql5, sql6, sql7]
    return sql