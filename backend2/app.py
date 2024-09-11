from flask import Flask, request, jsonify
from crawling.crawler import crawl, save_crawled_data
from indexing.index_builder import build_index
from utils.similarity import query_search
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/crawl', methods=['GET'])
def start_crawling():
    base_url = "https://docs.eyesopen.com/orion-user-interface/index.html"
    max_depth = 1  # Adjust as needed
    crawled_data = crawl(base_url, max_depth)
    data_file = os.path.join(os.path.dirname(__file__), 'crawled_data.json')
    save_crawled_data(crawled_data, data_file)  # Save crawled data to a file
    return jsonify({'message': 'Crawling completed successfully!', 'crawled_data': crawled_data})

@app.route('/index', methods=['GET'])
def start_indexing():
    urls, processed_docs, positions_list, vectorizer, tfidf_matrix = build_index()
    return jsonify({'message': 'Indexing completed successfully!'})

@app.route('/search', methods=['POST'])
def search_query():
    query = request.json.get('query', '')
    urls, processed_docs, positions_list, vectorizer, tfidf_matrix = build_index()
    results = query_search(query, vectorizer, tfidf_matrix, urls, positions_list)
    print(results)
    return jsonify({'results': results})

if __name__ == '__main__':
    print("app is running")
    app.run(debug=True)
