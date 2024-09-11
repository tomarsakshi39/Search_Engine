def test_start_crawling(client, monkeypatch):
    def mock_crawl(base_url, max_depth):
        return [{'url': base_url, 'depth': max_depth, 'content': 'Sample content'}]

    def mock_save_crawled_data(crawled_data, data_file):
        pass  # Do nothing for now

    monkeypatch.setattr('crawling.crawler.crawl', mock_crawl)
    monkeypatch.setattr('crawling.crawler.save_crawled_data', mock_save_crawled_data)

    response = client.get('/crawl')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Crawling completed successfully!'
    assert 'crawled_data' in data
    assert len(data['crawled_data']) > 0
    try:
        
        assert 'depth' in data['crawled_data'][0]
        assert 'content' in data['crawled_data'][0]
    except:
        raise AssertionError
def test_start_indexing(client, monkeypatch):
    def mock_build_index():
        return (['url1', 'url2'], ['doc1', 'doc2'], ['pos1', 'pos2'], 'vectorizer', 'tfidf_matrix')

    monkeypatch.setattr('indexing.index_builder.build_index', mock_build_index)

    response = client.get('/index')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Indexing completed successfully!'

def test_search_query(client, monkeypatch):
    def mock_build_index():
        return (['url1', 'url2'], ['doc1', 'doc2'], ['pos1', 'pos2'], 'vectorizer', 'tfidf_matrix')

    def mock_query_search(query, vectorizer, tfidf_matrix, urls, positions_list):
        return [{'url': 'url1', 'score': 0.9}, {'url': 'url2', 'score': 0.8}]

    monkeypatch.setattr('indexing.index_builder.build_index', mock_build_index)
    monkeypatch.setattr('utils.similarity.query_search', mock_query_search)

    response = client.post('/search', json={'query': 'test'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data
    assert len(data['results']) > 0
    
   
def test_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
