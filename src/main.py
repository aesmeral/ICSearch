# main.py
# Dan Tablac: 59871000
# Anthony Esmeralda: [ID]

# Just testing that the program can go through all the folders in the directory
# and print the url found in each json file in each folder
# 
# We'll need to use the data['content'] for the index instead.

import os
import sys
import json
import re
from bs4 import BeautifulSoup

# ---------- Global Variables ---------- #

doc_id_counter = 1    # Unique doc_id counter

inverted_index = dict()      # Store word(str) -> posting(list) pairings.

doc_ids = dict()    # Store doc_id -> doc_name pairings

# ---------- Index Implementation ---------- #

# store postings in python STL list

class Posting:
    def __init__(self, id, score):
        self.id = id                # document id that token was found (from doc_ids)
        self.score = score          # "tf_ifd score"

    def __repr__(self):
        return str('(doc_id: {}, score: {})'.format(self.id, self.score))

# ------------------------------------------ #

def _assign_doc_id(document):
    ''' Assign document id to a document. '''
    global doc_ids
    global doc_id_counter

    doc_ids[doc_id_counter] = document
    returning_doc_id = doc_id_counter    # temp store of original doc_id before incrementing
    doc_id_counter += 1
    return returning_doc_id

def _add_posting(token, id):
    ''' Adds/updates a posting, of the token's occurence in a document (id), in the inverted index '''
    global inverted_index
    token2 = token.lower()
    posting_updated = False
    try:
        for posting in inverted_index[token2]:
            if posting.id == id:
                posting.score += 1
                posting_updated = True
                break
        if posting_updated == False:
            inverted_index[token2].append(Posting(id, 1))
    except KeyError:
        inverted_index[token2] = []
        inverted_index[token2].append(Posting(id, 1))

def access_json_files(root):
    ''' Access each domain folder and their respected json files. '''
    # directory concept: https://realpython.com/working-with-files-in-python/#listing-all-files-in-a-directory
    # json concept: https://www.geeksforgeeks.org/read-json-file-using-python/
    # re and BeautifulSoup documentations referenced

    corpus = os.listdir(root)    # list containing each domain in 'DEV'
    
    # --- Check each domain (folder) --- #
    for domain in corpus[:1]:
        if os.path.isdir(os.path.join(root, domain)):  # Only get folders. Ignores .DS_Store in mac
            print('----------{}----------'.format(domain))  # just for showing which urls belong to what
            
            sub_dir = '{}/{}'.format(root,domain)           # Path to domain within root
            pages = os.listdir(sub_dir)                     # list json files, or 'pages', in domain
            for page in pages[:3]:
                id = _assign_doc_id(page)                         # give json file a unique doc_id
                json_file_location = sub_dir + '/{}'.format(page) # Path to page

                file = open(json_file_location, 'r')              # open JSON file
                data = json.load(file)                            # JSON object becomes dict
                file.close()

                # --- Do Stuff with the data --- #
                soup = BeautifulSoup(data['content'], 'html.parser')
                tokens = re.findall('[a-zA-Z0-9]+',soup.get_text())
                for token in tokens:
                    _add_posting(token, id)

# ------------------------------------------ #

# For now, just prints the the tokens and postings in the first domain for 3 documents (indices above)

if __name__ == '__main__':
    access_json_files('../DEV') # 'DEV' directory contains domains (extract developer.zip first)
    for word in inverted_index:
        postings = inverted_index[word]
        if len(postings) > 1:
            print('{} : {}'.format(word, postings))
    print('Number of documents: {}'.format(doc_id_counter-1))
    print('Unique keys: {}'.format(len(list(inverted_index.keys()))))
    print('Size of index: {} kilobytes'.format(sys.getsizeof(inverted_index) / 1000))
    