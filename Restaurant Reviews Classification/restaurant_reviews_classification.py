# -*- coding: utf-8 -*-
"""Restaurant Reviews Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FQzYmWNf-YHUeHjzufTO9FCVVmtIKjPv

# Part 1: Data preprocessing

Dataset link: https://www.kaggle.com/datasets/d4rklucif3r/restaurant-reviews?select=Restaurant_Reviews.tsv

## Importing the lib and dataset
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# creating a variable dataset to read the dataset
# delimeter is used as \t because the dataset is int .tsv
# The delimiter parameter tells pandas how the columns in the file are separated.
# quoting = 3 to remove all the double quotings
# quoting=3: Indicates that quotes in the file should be treated as regular characters,
# with no special meaning.

dataset = pd.read_csv('/content/Restaurant_Reviews.tsv', delimiter ='\t', quoting=3)

dataset.head()

"""## Data Exploration"""

dataset.shape

dataset.info()

dataset.columns

# statistical summary
dataset.describe()

"""## Dealing with missing values"""

dataset.isnull().values.any()

"""## Countplot"""

sns.countplot(x='Liked', data=dataset)
plt.show()

# Getting the exact count of positive reviews
(dataset.Liked == 1).sum()

# Getting the exact count of negative reviews
(dataset.Liked == 0).sum()

"""## Length of messages"""

dataset.head()

# Creating a new column to Length to get the len of the sentence
dataset['Length'] = dataset['Review'].apply(len)

dataset.head()

# Histogram
# The bins parameter determines how the data is divided into intervals (bins) for the histogram.
# The kind parameter specifies the type of plot you want to create.
# In this case, kind='hist' indicates that you want to create a histogram.

dataset['Length'].plot(bins=100, kind='hist')

"""Average length of characters in a message is around 60"""

dataset.Length.describe()

# Longest message
dataset[dataset['Length']== 149]['Review'].iloc[0]

# Shortest message
dataset[dataset['Length']== 11]['Review'].iloc[0]

# creating variables
positive = dataset[dataset['Liked'] == 1]

negative = dataset[dataset['Liked'] == 0]

positive

negative

"""## Cleaning the text"""

# Importing the libraries
# re is regular expression library
# nltk is natural language processing library

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# creating a list that will store the cleaned and processed reviews.
# line uses regular expressions (re.sub) to remove any characters that are not letters (a-z or A-Z).
# Everything else (numbers, punctuation, etc.) is replaced with a space
# The review text is converted to lowercase to ensure that the processing is case-insensitive
# split the reviews into a list of words.
# initialize the Porter Stemmer, which is a tool used to reduce words to their root form (e.g., "running" becomes "run").

# all_stopwords = stopwords.words('english')
# This loads a list of common English stopwords (e.g., "the", "is", "in")
# that don't add much meaning to the text and are often removed.

# all_stopwords.remove('not')
# removes the word "not" from the stopwords list

# review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
# Only keeps words that are not in the stopwords list
# Reduces each word to its root form.

# This takes the list of words and joins them back into a single string,
# with each word separated by a space.

corpus = []

for i in range(0,1000):
  review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
  review = review.lower()
  review = review.split()

  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
  review = ' '.join(review)
  corpus.append(review)

"""It removes unwanted characters, converts text to lowercase, splits it into words, removes stopwords (except "not"), stems the words to their root form, and then recombines them into a cleaned string."""

print(corpus)

len(corpus)

"""## Create the Bag of Words Model"""

# Creating sparse matrix
# rows will contain different reviews and column will conatin all diffrent words

# CountVectorizer is a tool used to convert a collection of text documents into a matrix of token counts
# (basically, it counts the frequency of each word in the text).

from sklearn.feature_extraction.text import CountVectorizer

# CountVectorizer to keep only the top 1500 most frequent words (features) in the text corpus.
# If there are more than 1500 unique words in your text data,
# it will keep only the 1500 most common ones

cv = CountVectorizer(max_features= 1500)

dataset.head()

# CountVectorizer to the corpus (learning the vocabulary from the text) and
# then transforms the corpus into a matrix. Each row in this matrix corresponds to a review,
# and each column corresponds to a word in the 1500 most frequent words.
# The values in the matrix represent the count of each word in each review.
# .toarray(): Converts the matrix into a NumPy array so it's easier to work with
# dataset.iloc[:, 1] selects all rows (:) from the second column (1) of the dataset.
# iloc is used for integer-based indexing.

x = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:,1]

x.shape

y.shape

"""## Split the dataset"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)

x_train.shape

x_test.shape

y_train.shape

y_test.shape

"""# Part 2: Model Building

## Naive bayes
"""

from sklearn.naive_bayes import GaussianNB
classifier_nb = GaussianNB()
classifier_nb.fit(x_train, y_train)

y_pred = classifier_nb.predict(x_test)

# Evalute the performs of this machine learning model

from sklearn.metrics import accuracy_score, confusion_matrix

acc = accuracy_score(y_test, y_pred)
print(acc*100)

cm = confusion_matrix(y_test, y_pred)
print(cm)

"""There are total 50 + 14 incorrect predictions which is 64

## XGBoost classier
"""

from xgboost import XGBClassifier
classifier_xgb = XGBClassifier()
classifier_xgb.fit(x_train,y_train)

y_pred = classifier_xgb.predict(x_test)

acc = accuracy_score(y_test, y_pred)
print(acc*100)

cm = confusion_matrix(y_test, y_pred)
print(cm)

"""The incorrect predictions are the diagonaly opp ones 31 + 16 which is 47 which is good for xgboost than in naive bayes

# Final model(XGBoost Classifier)
"""

from xgboost import XGBClassifier
classifier = XGBClassifier()
classifier.fit(x_train,y_train)

y_pred = classifier_xgb.predict(x_test)

acc = accuracy_score(y_test, y_pred)
print(acc*100)

cm = confusion_matrix(y_test, y_pred)
print(cm)

