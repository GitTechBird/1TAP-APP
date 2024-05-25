import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import numpy as np
import joblib  # For saving and loading pre-computed vectors
from collections import defaultdict
import traceback

# Load SpaCy model (consider performance-efficient models)
nlp = spacy.load('en_core_web_sm')  # Use a smaller model if possible

# Initialize WordNet Lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to lemmatize text (add more aggressive tokenization for noisy data)
def lemmatize_text(text):
    tokens = nlp(text)
    lemmatized_tokens = [token.lemma_.lower() for token in tokens if token.is_alpha]
    return ' '.join(lemmatized_tokens)

# Function to get synonyms (expand to incorporate contextual synonyms)
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return list(synonyms)

# Load data from Excel (handle potential errors gracefully)
def load_data(file_path, sheet_name, columns):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        data = df[columns].dropna().astype(str)
        return data
    except Exception as e:
        print(f"Error loading data from Excel: {e}")
        return None

# Load preprocessed data (if available)
def load_preprocessed_data(file_path):
    try:
        data = pd.read_pickle(file_path)
        return data
    except FileNotFoundError:
        print("Preprocessed data not found. Please preprocess data first.")
        return None

# Preprocess data (consider combining columns intelligently)
def preprocess_data(data):
    # Combine relevant columns for full text data
    data['text'] = data.apply(lambda row: ' '.join(row[col] for col in data.columns), axis=1)
    data['text'] = data['text'].apply(lemmatize_text)
    return data

# Train TF-IDF Vectorizer and save vectors (optional)
def train_tfidf_vectorizer(text_data, path):
    vectorizer = TfidfVectorizer()
    try:
        vectorizer.fit(text_data)
        print("TF-IDF Vocabulary Length:", len(vectorizer.get_feature_names_out()))
        # Save TF-IDF vectors for future use
        joblib.dump(vectorizer, path)
    except ValueError as e:
        print(f"TF-IDF Vectorizer Error: {e}")
        return None
    return vectorizer

# Load pre-computed TF-IDF vectors (if available)
def load_tfidf_vectors(path):
    try:
        vectorizer = joblib.load(path)
        return vectorizer
    except FileNotFoundError:
        print("TF-IDF vectors not found. Please train them first.")
        return None

def intelligent_search_old(query, data, vectorizer):
    query_lemmatized = lemmatize_text(query)
    query_vector = vectorizer.transform([query_lemmatized])
    similarities = cosine_similarity(query_vector, vectorizer.transform(data['text']))
    data['similarity'] = similarities[0]
    return data.sort_values(by='similarity', ascending=False)

# Function to perform efficient prefix search using pre-computed data
def intelligent_search(query, data, vectorizer, max_results=1000):
    # Preprocess query
    query_lemmatized = lemmatize_text(query)

    # Filter data based on query prefix (optional)
    filtered_data = data[data['text'].str.startswith(query_lemmatized)]

    # Transform query and data using pre-computed vectors
    query_vector = vectorizer.transform([query_lemmatized])
    data_vectors = vectorizer.transform(filtered_data['text'])

    # Calculate similarities
    similarities = cosine_similarity(query_vector, data_vectors)

    # Sort data by similarity and return top results
    sorted_indices = similarities.argsort().flatten()[::-10]
    top_results = filtered_data.iloc[sorted_indices[:max_results]]
    # return top_results
    return top_results['business_activity_group_name'].drop_duplicates().tolist()


def intelligent_search_advance(query, data, vectorizer,max_results=10, alpha=0.8, beta=0.2):
    query_lemmatized = lemmatize_text(query)

    # Combine TF-IDF and word embedding similarity (adjust weights)
    query_vector = vectorizer.transform([query_lemmatized])
    similarities_tfidf = cosine_similarity(query_vector, vectorizer.transform(data['text']))
    # Include stemming-based recall (stem lemmas if stemming is used)
    query_stemmed = WordNetLemmatizer().lemmatize(query_lemmatized, pos='v')  # Stem for verbs
    stemmed_synonyms = get_synonyms(query_stemmed)  # Find stemmed synonyms
    if stemmed_synonyms:
        # Assuming at least one synonym was found and transformed
        stemmed_synonyms_vector = vectorizer.transform(stemmed_synonyms)
        similarities_stemmed = cosine_similarity(stemmed_synonyms_vector, vectorizer.transform(data['text']))
        max_similarity_stemmed = similarities_stemmed.max(axis=0)  # Taking the max similarity across all synonyms
    else:
        # If no synonyms, default to zeros to avoid errors
        max_similarity_stemmed = np.zeros(similarities_tfidf.shape)

    # Combine similarities with weights
    similarities = alpha * similarities_tfidf + beta * max_similarity_stemmed

    #sorted_indices = similarities.argsort().flatten()[::10]
    #search_results = data.iloc[sorted_indices]
    
     # Sort data by similarity and return top results
    sorted_indices = similarities.argsort().flatten()[::-1]
    search_results = data.iloc[sorted_indices[:max_results]]

    return search_results['business_activity_group_name'].drop_duplicates().tolist()