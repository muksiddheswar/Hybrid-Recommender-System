#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:53:06 2019

@author: smkj33
"""

def importContentQuery ():
    sql = "SELECT uid, title, bodytext FROM tx_news_domain_model_news LIMIT 10"
    return sql


def importContentMetadata():
    return ''
