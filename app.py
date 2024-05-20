from flask import Flask, render_template, request
import re
import urllib.parse
from nltk.corpus import wordnet 


app = Flask(__name__)

Word_synoms = {}
import os

# Get the current directory where app.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))




def tokenize_query(query):
    return re.findall(r'\b\w+\b', query.lower())


def binary_search(word, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        start = 0
        end = f.seek(0, 2)  
        while start < end:
            mid = (start + end) // 2
            f.seek(mid) 
            f.readline()  
            line = f.readline().strip()  
            if not line:  
                break
            current_word, urls = line.split('\t', 1)
            if current_word < word:
                start = mid + 1
            elif current_word > word:
                end = mid
            else:
                url_counts = {}
                for url_count in urls.split(';'):
                    if ':' in url_count: 
                        url, count = url_count.split(':')
                        url_counts[url] = int(count)
                    else:
                        url_counts[url_count] = 1 
                return url_counts
    return {}

def calculate_tf(query_tokens, inverted_index):
    tf_scores = {}
    for token in query_tokens:
        urls = inverted_index.get(token, {})
        for url, count in urls.items():
            tf_scores[url] = tf_scores.get(url, 0) + count
    return tf_scores

def rank_urls(tf_scores):
    return sorted(tf_scores.items(), key=lambda x: x[1], reverse=True)

def search(query, inverted_index_file):
    query_tokens = tokenize_query(query)
    inverted_index = {}

    for token in query_tokens:
        entry = binary_search(token, inverted_index_file)
        if entry:
            inverted_index[token] = entry

    tf_scores = calculate_tf(query_tokens, inverted_index)
    ranked_urls = rank_urls(tf_scores)
    
    ranked_urls = [(url, score) for url, score in ranked_urls if url]
    
    return ranked_urls

def get_url_from_filename(filename):
    try:
        decoded_filename = urllib.parse.unquote(filename, encoding='utf-8')
        return decoded_filename
    except Exception as e:
        print("An error occurred:", e)
        return None

def get_page_rank(url, page_rank_file):
    with open(page_rank_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            url_in_file, rank = line.split(': ')
            if url == url_in_file:
                return float(rank)
    return 0.0  
def AItokenize_query(query):
    return re.findall(r'\b\w+\b', query.lower())

def AIfind_synonyms(word):
    
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    synonyms.add(word)
    Word_synoms[word] = synonyms 
    return list(synonyms)

def AIbinary_search(word, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        start = 0
        end = f.seek(0, 2) 
        while start < end:
            mid = (start + end) // 2
            f.seek(mid)  
            f.readline() 
            line = f.readline().strip()  
            if not line:  
                break
            current_word, urls = line.split('\t', 1)  
            if current_word < word:
                start = mid + 1
            elif current_word > word:
                end = mid
            else:
                url_counts = {}
                for url_count in urls.split(';'):
                    if ':' in url_count: 
                        url, count = url_count.split(':')
                        url_counts[url] = int(count)
                    else:
                        url_counts[url_count] = 1  
                return url_counts
    return {}

def AIcalculate_tf(query_tokens, inverted_index):
    
    tf_scores = {}
    for token in query_tokens:
        synonyms = AIfind_synonyms(token)
        search_words = [token] + synonyms
        for word in search_words:
            urls = inverted_index.get(word, {})
            for url, count in urls.items():
                tf_scores[url] = tf_scores.get(url, {})
                tf_scores[url][word] = count
    return tf_scores

def AIrank_urls(tf_scores):
    ranked_urls = []
    for url, word_counts in tf_scores.items():
        total_score = sum(word_counts.values())
        ranked_urls.append((url, total_score, word_counts))
    return sorted(ranked_urls, key=lambda x: x[1], reverse=True)

def AIsearch(query, inverted_index_file):
    query_tokens = AItokenize_query(query)   
    tf_scores = {}
    for token in query_tokens:
        synonyms = AIfind_synonyms(token)
        for synonym in synonyms:
            urls_counts = AIbinary_search(synonym, inverted_index_file)
            for url, count in urls_counts.items():
                tf_scores[url] = tf_scores.get(url, {})
                tf_scores[url][synonym] = count
    ranked_urls = AIrank_urls(tf_scores)
    return ranked_urls

def AIget_url_from_filename(filename):
    try:
        decoded_filename = urllib.parse.unquote(filename, encoding='utf-8')
        return decoded_filename
    except Exception as e:
        print("An error occurred:", e)
        return None
def TFsearch(query, inverted_index_file):
    query_tokens = tokenize_query(query)
    inverted_index = {}
    for token in query_tokens:
        entry = binary_search(token, inverted_index_file)
        if entry:
            inverted_index[token] = entry
    tf_scores = TFcalculate_tf(query_tokens, inverted_index)
    
    ranked_urls = TFrank_urls(tf_scores)
    return ranked_urls
def TFcalculate_tf(query_tokens, inverted_index):
    tf_scores = {}
    for token in query_tokens:
        urls = inverted_index.get(token, {})
        for url, count in urls.items():
            tf_scores[url] = tf_scores.get(url, {})
            tf_scores[url][token] = count
    return tf_scores

def TFrank_urls(tf_scores):
    ranked_urls = []
    for url, word_counts in tf_scores.items():
        total_score = sum(word_counts.values())
        ranked_urls.append((url, total_score, word_counts))
    return sorted(ranked_urls, key=lambda x: x[1], reverse=True)

#=================================================================================
#=================================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    query = None
    search_results = None
    if request.method == 'POST':
        query = request.form['query']
        # Construct the path to the file in the Data folder
        inverted_index_file = os.path.join(current_dir, "Data", "part-r-00000.txt")
        search_results = TFsearch(query, inverted_index_file)
        print(search_results)
        formatted_results = []
        for url, total_score, word_counts in search_results:
            url = AIget_url_from_filename(url)
            if url:
                formatted_results.append((url, total_score, word_counts))
            else:
                print("Invalid URL for filename:", url)
        return render_template('index.html', search_results=formatted_results, query=query, active_page='index')
    return render_template('index.html', search_results=search_results, query=query, active_page='index')

@app.route('/pageranking', methods=['GET', 'POST'])
def pageranking():
    if request.method == 'POST':
        query = request.form['query']
        inverted_index_file = os.path.join(current_dir, "Data", "part-r-00000.txt")
        search_results = search(query, inverted_index_file)
        page_rank_file = os.path.join(current_dir, "Data", "page_ranks2__1000.txt")
        formatted_results = []  
        for url, score in search_results:
            decoded_url = get_url_from_filename(url)
            page_rank = get_page_rank(decoded_url, page_rank_file)

            formatted_results.append((decoded_url, score, page_rank))
            
        sorted_results = sorted(formatted_results, key=lambda x: x[2], reverse=True)
        return render_template('pageranking.html', search_results=sorted_results, query=query, active_page='pageranking')
    return render_template('pageranking.html', search_results=[], query='', active_page='pageranking')

@app.route('/smartsearch', methods=['GET', 'POST'])
def smartsearch():
    return render_template('smartSearch.html', active_page='smartsearch')

@app.route('/TF-IDF-synonyms', methods=['GET', 'POST'])
def aimodel():
    global Word_synoms  
    Word_synoms = {}
    if request.method == 'POST':
        query = request.form['query']
        inverted_index_file = os.path.join(current_dir, "Data", "part-r-00000.txt")
        search_results = AIsearch(query, inverted_index_file)
        print("Search results for query '{}':".format(query))
        for i in range(len(search_results)):
            url, total_score, word_counts = search_results[i]
            url = AIget_url_from_filename(url)
            if url:
                search_results[i] = (url, total_score, word_counts)
                print("URL:", url)
                print("Total Score:", total_score)
                print("Words contributing to this score:")
                for word, score in word_counts.items():
                    print("  - Word:", word)
                    print("    TF Score:", score)
        return render_template('aiModel.html', search_results=search_results, active_page='aimodel', query=query, word_synoms=Word_synoms)  # Pass the word_synoms variable here
    return render_template('aiModel.html', search_results=[], active_page='aimodel', query='', word_synoms=Word_synoms)  # Pass the word_synoms variable here



if __name__ == '__main__':
    app.run(debug=True,port=8000)