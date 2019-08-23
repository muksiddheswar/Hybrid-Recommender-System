#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:33:16 2019

@author: smkj33
"""


# Weights for combining the similarities cased on different factors
from weights import *


# REMOVE FROM HERE
def get_recommendations(title, cosine_sim):

    # Get the index of the article that matches the title
    # article_index = article_map['local_index'].loc[article_map['title'] == title].item()
    article_index_ser = article_map['local_id'].loc[article_map['title'] == title]
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
# RECOMMENDATION DRIVER
#-------------------------------------#

def reco_catcher(request_frame):

    local_id = get_local_id(request_frame['article_id'])
    sim = get_similarity(local_id)

    content_sim = sim['content_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))
    title_sim = sim['title_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))
    cat_tags_sim = sim['cat_tags_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))


    # -- BUSINESS LOGIC-- #

    # Similarity combination
    cosine_sim = (content_sim * float(weights_values['content_weight'])) + (title_sim * float(weights_values['title_weight'])) + (cat_tags_sim * float(weights_values['cat_tags_weight']))
    cosine_sim /= 3

    duration_weight = request_frame['duration']
    duration_weight = (duration_weight - duration_weight.min())/(duration_weight.max() - duration_weight.min())

    final_score = cosine_sim.mul(duration_weight, axis = 0)

    matrix = final_score.to_numpy()
    index = np.unravel_index(np.argsort(matrix, axis=None), matrix.shape)
    index = index[1][:10]

    final_list = get_article(index)

    pd.set_option('max_colwidth', 100)
    print(final_list)






    # Extract list of final local_id s
    # Select corrosponding article_id, title

    # return in json format
