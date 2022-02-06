import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import numpy as np
import pandas as pd
import acquire
import time



# ty, AG
def basic_clean(string):
    '''
    This function takes in a string and
    returns the string normalized.
    '''
    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    string = re.sub(r'[^\w\s]', '', string).lower()
    
    return string

# ty AG
def tokenize(string):
    '''
    This function takes in a string and
    returns a tokenized string.
    '''
    # Create tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use tokenizer
    string = tokenizer.tokenize(string, return_str = True)
    
    return string

# ty AG
def stem(string):
    '''
    This function takes in a string and
    returns a string with words stemmed.
    '''
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    
    # Use the stemmer to stem each word in the list of words we created by using split.
    stems = [ps.stem(word) for word in string.split()]
    
    # Join our lists of words into a string again and assign to a variable.
    string = ' '.join(stems)
    
    return string

# ty AG
def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # Join our list of words into a string again and assign to a variable.
    string = ' '.join(lemmas)
    
    return string

# ty AG

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list).difference(set(exclude_words))
    
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))

    # Split words in string.
    words = string.split()
    
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

    
# ty AG
def prep_article_data(df, original, extra_words = [], exclude_words = []):
    
    '''
    This function takes in a dataframe, the original corpus column, a list of extra words to supplement
    the list of stop words, and a list of words to exclude from the stop words list, and returns the dataframe 
    supplemented with clean, stemmed, and lemmatized columns.
    '''
    
    # produce 'original' column
    df = df.rename(columns = {original: 'original'})
    
    # produce 'clean' column. clean and then tokenize
    df['clean'] = df['original'].apply(basic_clean)\
    .apply(tokenize)\
    .apply(remove_stopwords, extra_words = extra_words, exclude_words = exclude_words)
          
    # produce 'stemmed' column
    df['stemmed'] = df['original'].apply(basic_clean)\
    .apply(tokenize)\
    .apply(stem)\
    .apply(remove_stopwords, extra_words = extra_words, exclude_words = exclude_words)
    
    # produce 'lemmatized' column
    df['lemmatized'] = df['original'].apply(basic_clean)\
    .apply(tokenize)\
    .apply(lemmatize)\
    .apply(remove_stopwords, extra_words = extra_words, exclude_words = exclude_words)
    
    return df