import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import numpy as np
from .NLP_search import preprocess_data, train_tfidf_vectorizer, intelligent_search


# Define search function
def search1(data, query):
    # Preprocessing the data
    data = pd.DataFrame(data)
    # Initialize WordNet Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Preprocess data
    data = preprocess_data(data)

    # Train TF-IDF Vectorizer
    vectorizer = train_tfidf_vectorizer(data['text'])
    if not vectorizer:
        return {'error': 'Vectorization not available'}
    # query = query
    if not query:
        return {'error': 'Query parameter missing'}

    results = intelligent_search(query, data, vectorizer)
    # results = results['business_activity_group_name'].drop_duplicates().to_list()
    return results.head().to_dict(orient='records')
