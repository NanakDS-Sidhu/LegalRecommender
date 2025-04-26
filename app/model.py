from collections import Counter
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
pipe = pipeline("token-classification", model="dominguesm/legal-bert-ner-base-cased-ptbr")


entity_freq_df = pd.read_pickle('vector.pkl')
df = pd.read_pickle('file.pkl')

def match_subsection_by_freq(input_freq, freq_df, top_n=1):
    """
    Given an input frequency dictionary (e.g., {'B-ORGANIZACAO': 3, 'I-ORGANIZACAO': 1, ...})
    and a frequency DataFrame (with columns 'number', 'subsec_id', and entity tags),
    this function computes cosine similarity between the input vector and each subsection vector,
    returning the top_n matching subsections along with their similarity scores.
    """
    # Identify tag columns (exclude identifier columns)
    tag_columns = [col for col in freq_df.columns if col not in ['number', 'subsec_id']]
    
    # Build the input vector in the same column order, using 0 if a tag is missing in input_freq
    input_vector = np.array([input_freq.get(tag, 0) for tag in tag_columns]).reshape(1, -1)
    
    # Extract the frequency matrix for each subsection
    matrix = freq_df[tag_columns].values
    
    # Compute cosine similarity between the input vector and each subsection vector
    similarities = cosine_similarity(input_vector, matrix).flatten()
    
    # Identify indices for the top_n most similar subsections
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    
    # Create a result DataFrame with the matching rows and add the similarity scores
    result = freq_df.iloc[top_indices].copy()
    result['similarity'] = similarities[top_indices]
    
    return result

def evaluate(text):
    data=pipe(text)
    entities = [entry['entity'] for entry in data]
    entity_counts = Counter(entities)
    top_matches = match_subsection_by_freq(entity_counts,entity_freq_df,top_n=3)
    print(top_matches)
    indices=top_matches["number"]
    result = df['desc'].iloc[indices]
    return result
