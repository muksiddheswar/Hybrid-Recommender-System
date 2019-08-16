"""
Created on Wed Aug 14 15:35:59 2019

@author: smkj33
"""

import pymysql
from db_config import mysql


"""
from bs4 import BeautifulSoup

# Requried in PorterStemmer()
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer



# Stemmer declaration here done to avoid repeated declaration
porter = PorterStemmer()


# Creates word tokens and converts tokens to stems for text analysis
def porter_stemmer (txt):
    token_words=word_tokenize(txt)
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)




####################################################
"""

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



"""
####################################################
"""

def import_details ():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    try:
    
        # sql = ""
         cursor.execute("SELECT uid, title, bodytext FROM tx_news_domain_model_news LIMIT 10")
         rows = cursor.fetchall()
    
         for x in rows:
    
              print("Id = ", x[0], )
              print("Title = ", x[1])
              # print("Content  = ", x[2])
              print("Content  = ", strip_tags(x[2]))
             # x[2].apply(lambda content: porter_stemmer(re.sub('[^a-z\s]', '',BeautifulSoup(content).get_text(separator=' ').lower())
    
         cursor.close()
    
    except Exception as e :
        print ("Error while connecting to MySQL", e)
    
    finally:
    
        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")

# import_details()