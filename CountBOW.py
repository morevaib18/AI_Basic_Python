from sklearn.feature_extraction.text import CountVectorizer

stopwords = []
stopwords.append("to")
stopwords.append("and")
sentence = ["I love to watch movies, especially action movies"]
#Creating an object of Count Vectorizer. Also stop words as well
cv = CountVectorizer(stop_words=stopwords)
#fit, training alogritham - Data - FIT - Train - Model - Transform - Database
#cv.fit(sentence)
#cvt = cv.transform(sentence)
cvt = cv.fit_transform(sentence)
print(cv.vocabulary_)
print(cvt)
