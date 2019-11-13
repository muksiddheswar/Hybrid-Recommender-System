import numpy as np
from content_recommendor import *



req = {'article_id': [1011, 1019, 1022],
       'duration': [120, 300, 50]}
df = pd.DataFrame(req)
print(reco_catcher(req))


# from db_functions import *
# truncate_similarities()


