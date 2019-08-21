#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:00:15 2019

@author: smkj33
"""

#  Function that takes in article title as input and outputs most similar articles

def get_recommendations(title):
    # Get the index of the article that matches the title
    article_index = indices[title]

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
    return article_master['articleTitle'].iloc[article_indices]

