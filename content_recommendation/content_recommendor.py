#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:33:16 2019

@author: smkj33
"""

# Weights for combining the similarities cased on different factors
from weights import *
from db_functions import *
import numpy as np


# -------------------------------------#
# GET RECOMMENDATION DRIVER
# -------------------------------------#

def reco_catcher_ts_ss(request_frame):
    local_id = get_local_id(request_frame['article_id'])
    sim = get_ts_ss_similarity(local_id)
    content_sim = sim['scores'].apply(lambda row: pd.read_json(row, typ='list'))

    duration_weight = pd.DataFrame(request_frame['duration'])
    final_list = business_logic(duration_weight, content_sim)
    return final_list


def reco_catcher_cosine(request_frame):
    local_id = get_local_id(request_frame['article_id'])
    sim = get_similarity(local_id)

    content_sim = sim['content_sim'].apply(lambda row: pd.read_json(row, typ='list'))
    title_sim = sim['title_sim'].apply(lambda row: pd.read_json(row, typ='list'))
    cat_tags_sim = sim['cat_tags_sim'].apply(lambda row: pd.read_json(row, typ='list'))

    # Similarity combination
    cosine_sim = (content_sim * float(weights_values['content_weight'])) + \
                 (title_sim * float(weights_values['title_weight'])) \
                 + (cat_tags_sim * float(weights_values['cat_tags_weight']))

    cosine_sim /= (float(weights_values['content_weight']) + float(weights_values['title_weight']) + float(
        weights_values['cat_tags_weight']))

    duration_weight = pd.DataFrame(request_frame['duration'])
    final_list = business_logic(duration_weight, cosine_sim)

    return final_list


# --ADDITIONAL BUSINESS LOGIC HERE-- #
def business_logic(duration_weight, similarities):
    # In the following step, the duration values are normalised
    duration_weight = (duration_weight - duration_weight.min()) / (duration_weight.max() - duration_weight.min())
    final_score = similarities.mul(duration_weight, axis=0)

    matrix = final_score.to_numpy()
    index = np.unravel_index(np.argsort(matrix, axis=None), matrix.shape)
    index = index[1][:10]

    final_list = get_article(index)

    return final_list
