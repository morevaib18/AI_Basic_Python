# Term Frequency
# Inverse Document Frequency
import os
from sklearn.feature_extraction.text \
import TfidfVectorizer
import math

import scipy
from sklearn.feature_extraction import text
from scipy import stats
import collections
# Doc1 ( Books) Term occuring THAT Document = 3
# Total no of terms in THAT Document =11
# TF = 3/11
# Doc2( Books) = 1/5
# IDF = log(total number of documents / number of document where the term occured)
# IDF(Books) = log(3/2)
# TF-IDF = TF * IDF
document=["books are great.",
         " I read  a lot books",
       "One day i will become a author"]

vectorizer = TfidfVectorizer()
tfidfvalues = vectorizer.fit_transform(document)
print(tfidfvalues)
print(vectorizer.vocabulary_)

