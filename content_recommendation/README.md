# Content based recommendation generation API

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

