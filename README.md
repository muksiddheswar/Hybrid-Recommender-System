# Hybrid Article Recommendation System

## INTRODUCTION
This project focuses on creation of a Proof-Of-Concept (POC) for a customised Recommendation Engine that suggests reading material to end users of a content marketing website maintained and managed by EEIP. This is the first step towards a mobile-first website focused on user experience. This work was undertaken in close collaboration with other team members of EEIP, working on content categorisation, company taxonomy and master data management. However, the decision on the algorithm side, was left open by the organisation, and the final code has been developed using standard open source libraries in Python. The final API has been developed to run using the minimum possible infrastructure. The focus has been on making an economically viable  Recommendation System. Hence there are multiple improvements that need to be made to achieve high speed results. Suggestions for the same have been made in the concluding sections.

## BUSINESS REQUIREMENT :
Content Marketing Website that displays articles to end users.

- Website gets ~100,000 hits per month, 75% from Europe.

- There is no provision of registration or user login. IP addresses / Session IDs will be used to track user behaviour (interest in different topics, languages etc).

- Currently homepage content, readable articles, are presented to all website viewers in the same default order. In future “user behaviour data” will be used to show content in order of relevance for users.

- Suggested reading links are recommended at the end of each article, which, at the moment are manually set. In future usage of “user behaviour data” will be used to show dynamically generated relevant suggestions.


The environment consists of a TYPO3 website which will use a customised Recommendation Engine (RE).   
The RE will consist of 3 parts:
1.	Content Based Similarity
2.	Collaborative Similarity
3.	Additional Business Logic

The Recommendation core will be accessible via various APIs. Apart from the standard recommendation methods, the final list is created by applying additional business rules. This logic and the learning models have been discussed in the individual sections.




<br><br>

## REFERENCE
http://yifanhu.net/PUB/cf.pdf  
https://realpython.com/build-recommendation-engine-collaborative-filtering/   
https://github.com/benfred/implicit   
https://towardsdatascience.com/building-a-collaborative-filtering-recommender-system-with-clickstream-data-dffc86c8c65   
https://implicit.readthedocs.io/en/latest/als.html?source=post_page-----dffc86c8c65----------------------   
https://medium.com/radon-dev/als-implicit-collaborative-filtering-5ed653ba39fe   
https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/Articles%20Rec%20System%20Implicit.ipynb   
https://github.com/taki0112/Vector_Similarity   
https://en.wikipedia.org/wiki/Matrix_factorization_(recommender_systems)   
