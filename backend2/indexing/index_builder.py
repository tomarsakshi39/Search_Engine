import json
from indexing.document_processor import process_documents

def build_index():
    with open("crawled_data.json", "r", encoding='utf-8') as file:
        crawled_data = json.load(file)
    return process_documents(crawled_data)
