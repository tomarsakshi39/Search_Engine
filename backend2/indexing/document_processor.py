import string
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    positions = {}
    pos = 0
    clean_tokens = []
    for word in tokens:
        if word not in stop_words and word not in string.punctuation:
            stemmed_word = ps.stem(word)
            clean_tokens.append(stemmed_word)
            if stemmed_word not in positions:
                positions[stemmed_word] = []
            positions[stemmed_word].append(pos)
        pos += 1
    return ' '.join(clean_tokens), positions

def process_documents(crawled_data):
    urls, documents = zip(*crawled_data)
    processed_docs = []
    positions_list = []

    for doc in documents:
        clean_doc, positions = preprocess(doc)
        processed_docs.append(clean_doc)
        positions_list.append(positions)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_docs)

    return urls, processed_docs, positions_list, vectorizer, tfidf_matrix
