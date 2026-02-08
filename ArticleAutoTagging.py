import os
from sklearn.feature_extraction.text \
import CountVectorizer
import scipy
from sklearn.feature_extraction import text

# Step 1 :- Get all the files from folder
mypath = os.getcwd() + "\\Articles"
print(mypath)
for file in os.listdir(mypath):
    f = open(mypath + "\\" + file,"r")
    document = []
    temp = ""
    # Step 2 :- read the content into document collection
    for line in f.readlines():
        temp = temp + line

    document.append(temp)

    # Step 3 :- pass this document to vectorizer
    vectorizer = CountVectorizer(stop_words=list(text.ENGLISH_STOP_WORDS))
    # CountVectorizer will take the document content and train himself
    counts = vectorizer.fit_transform(document)
    bows = vectorizer.vocabulary_
    # print(bows)
    # print(counts)
    # print(type(bows)) #<class 'dict'>
    # print(type(counts)) #<class 'scipy.sparse._csr.csr_matrix'>
    #Create Coo matrix based on counts received in scipy.sparse._csr.csr_matrix
    coo = scipy.sparse.coo_matrix(counts)
    #create a file object and open it for writing
    fileBow = open(f.name + "bow.txt", "w")
    #For loop to read data count data from coo and string keys from bows e.g. 1 -- Introduction
    for _count, _bowname in zip(coo.data, bows.keys()):
            # Check for count which is greater than 2
            if (_count > 2):
                # print(str(_count) + " "+ str(_bowname))
                fileBow.write(str(_count) + " -- " + _bowname + "\n")

    #Close the file which is open for write
    fileBow.close()


