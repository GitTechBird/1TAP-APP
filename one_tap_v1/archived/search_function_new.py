import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import numpy as np
from .NLP_search_new import preprocess_data, train_tfidf_vectorizer, intelligent_search, intelligent_search_old, load_tfidf_vectors, load_preprocessed_data, intelligent_search_advance
import frappe


# Define search function
def search3(query):
    # Load preprocessed data or preprocess if not available
    vector_path = '/home/frappe-1tap/frappe-bench/apps/one_tap_v1/one_tap_v1/tfidf_vectors.pkl'
    preprocess_data_path = '/home/frappe-1tap/frappe-bench/apps/one_tap_v1/one_tap_v1/preprocessed_data.pkl'
    preproc_file_data = load_preprocessed_data(preprocess_data_path)
    if preproc_file_data is None:
        # Load and preprocess data (if preprocessed data not found)
        activities = frappe.get_all("OT Business Activity", fields=["business_activity_name", "business_activity_group_name", "business_activity_description"])
        # return activities
        doc_data = []
        for activity in activities:
            doc_data.append({
                "business_activity_name": activity.business_activity_name if activity.business_activity_name else "",
                "business_activity_group_name": activity.business_activity_group_name if activity.business_activity_group_name else "",
                "business_activity_description": activity.business_activity_description if activity.business_activity_description else ""
            })
        doc_data = pd.DataFrame(doc_data)

        if doc_data is not None:
            preproc_file_data = preprocess_data(doc_data)
            # Save preprocessed data for future use
            preproc_file_data.to_pickle(preprocess_data_path)
        
    # Load pre-trained TF-IDF vectorizer
    vectorizer = load_tfidf_vectors(vector_path)
    if not vectorizer:
    # Train and save TF-IDF vectors if not available
        vectorizer = train_tfidf_vectorizer(preproc_file_data['text'], vector_path)
    if not query:
        return {'error': 'Query parameter missing'}
    # results = intelligent_search(query, preproc_file_data, vectorizer)
    results = intelligent_search_old(query, preproc_file_data, vectorizer)
    # return results
    return results.head().to_dict(orient='records')






    # # Load preprocessed data or preprocess if not available
    # vector_path = '/home/frappe-1tap/frappe-bench/apps/one_tap_v1/one_tap_v1/tfidf_vectors.pkl'
    # preprocess_data_path = '/home/frappe-1tap/frappe-bench/apps/one_tap_v1/one_tap_v1/preprocessed_data.pkl'
    # preproc_file_data = load_preprocessed_data(preprocess_data_path)
    # if preproc_file_data is None:
    #     # Load and preprocess data (if preprocessed data not found)
    #     activities = frappe.get_all("OT Business Activity", fields=["business_activity_name", "business_activity_group_name", "business_activity_description"])
    #     doc_data = []
    #     for activity in activities:
    #         doc_data.append({
    #             "business_activity_name": activity.business_activity_name if activity.business_activity_name else "",
    #             "business_activity_group_name": activity.business_activity_group_name if activity.business_activity_group_name else "",
    #             "business_activity_description": activity.business_activity_description if activity.business_activity_description else ""
    #         })
    #     doc_data = pd.DataFrame(doc_data)

    #     if doc_data is not None:
    #         preproc_file_data = preprocess_data(doc_data)
    #         # Save preprocessed data for future use
    #         preproc_file_data.to_pickle(preprocess_data_path)
        
    # # Load pre-trained TF-IDF vectorizer
    # vectorizer = load_tfidf_vectors(vector_path)
    # if not vectorizer:
    # # Train and save TF-IDF vectors if not available
    #     vectorizer = train_tfidf_vectorizer(preproc_file_data['text'], vector_path)
    # if not query:
    #     return {'error': 'Query parameter missing'}
    # results = intelligent_search(query, preproc_file_data, vectorizer)
    # return results.head().to_dict(orient='records')