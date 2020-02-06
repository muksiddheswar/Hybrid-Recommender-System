# Content based recommendation generation API

## ENVIRONMENT SETUP:

### Database Configuration:
The **db_cofig.py** file has the database details. (Connection via SSH testing not done; I have tested this by replicating the database into my local Linux virtual machine.)

### SQL Queries:
If the database model has changed in that case the queries need to be modified accordingly. The queries.py file is the place to do this. The present queries are based on the default database schema of the TYPO3 News theme. To be specific the following tables are used as source:

•	tx_news_domain_model_news
•	sys_category_record_mm
•	sys_category
•	tx_news_domain_model_news_tag_mm
•	tx_news_domain_model_tag

Further explanation of the queries are included as comments in the relevant files.

### Recommendation Specific Tables:
The following tables are required to store the pre-calculated similarity matrices. 
•	recen_magnitude_content
•	recen_distance_content
•	recen_ts_ss_content
•	recen_theta_content
•	recen_distance_content
•	recen_article_map


### Similarity Calculation Weights:
The similarity scores based on the content and the remaining metadata are calculated and stored separately in the database.   
At the time of suggestion generation, they are retrieved and then a weighted average is calculated based on the weights specified in **weights.py** .

### Python Libraries:
The following open source libraries are required to be installed in the environment so that the model is successfully generated.
•	pandas, numpy, math, re, BeautifulSoup, sklearn, nltk

Thereafter database connectivity and API generation requires the following libraries:
•	pymysql, flask

**Note:** It is suggested to use Python3 since that was used to develop the engine. Backward compatibility cannot be ensured in this POC.




**db_cofig.py** - Contains the database configurations.
**weights.py**  - Contains weights that detemine the additional business logic. (Details in the report)

**db_functions.py** - Article metadata queries need to be changed of the database schema is changes. As of now the queries are based in the TYPO3 news theme scehma.

* * *

## OPERATION:

**model.py** - Creates the static recommendation model by importing all articles from the database. This needs to be rerun after addition of new articles.  
**reco.py**  - Contains function necessary to suggest recommendations. (This is used by the API file).  

**api.py**   - Python file for creating a live API.

* Run the api.py file and this is enough to test the API.
* Testing needs to be done using POSTMAN or any API tester.  
* Details of API testing is included in the report.

NOTE: It is assumed that the mysql database instance is already running in the background.

* * * 
## POSSIBLE IMPROVEMENTS
1.  CUDA implementation in model.py for faster model creation.
2.  Incremental update of the model. (Required for scalability) 
    For this the term count and the document count matrices need to stored seperately and incrementally updated with each new article.
3.  Model creation via API.
4.  API security checks.

