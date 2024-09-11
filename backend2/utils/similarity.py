from sklearn.metrics.pairwise import cosine_similarity
from indexing.document_processor import preprocess

def query_search(query, vectorizer, tfidf_matrix, urls, positions_list):
    processed_query, query_positions = preprocess(query)
    query_vec = vectorizer.transform([processed_query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix)
    ranked_indices = similarity_scores.argsort()[0][::-1]

    results = []
    for idx in ranked_indices[:5]:  # Return top 10 results
        url = urls[idx]
        positions = positions_list[idx]
        matched_positions = {term: positions.get(term, []) for term in processed_query.split()}
        results.append((url, matched_positions))
    
    return results
