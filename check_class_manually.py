from pymongo import MongoClient
from pprint import pprint
from collections import Counter
import pickle
import json
import random
import argparse
from bson import ObjectId

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--collection', type=str, default="A", help="Choose A, B, C")
parser.add_argument('-s', '--synthesis', type=str, default="ss", help="Choose else, ss, hc, sg, pc")
parser.add_argument('-n', '--number', type=int, default=10, help="Choose random sampple size")
args = parser.parse_args()
col = args.collection
synt = args.synthesis
n = args.number

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)

print("Connecting to DB...")
"""
#Fill in your credentials
client = MongoClient(
    '...',
    username='...',
    password='...',
    authSource='...',
    authMechanism='...'
)

#connect to a collection of your choice
if col=="A":
    print("Connecting to A")
    paragraphs = client.db.AParagraphs
"""


queryS0 = {"classification": {"$regex": "something_else", "$options": "i"}}
queryS1 = {"classification": {"$regex": "solid_state_ceramic_synthesis", "$options": "i"}}
queryS2 = {"classification": {"$regex": "hydrothermal_ceramic_synthesis", "$options": "i"}}
queryS3 = {"classification": {"$regex": "sol_gel_ceramic_synthesis", "$options": "i"}}
queryS4 = {"classification": {"$regex": "precipitation_ceramic_synthesis", "$options": "i"}}
queries = {"else":queryS0, "ss":queryS1, "hc": queryS2, "sg": queryS3, "pc": queryS4}

query = queries[synt]

docs = [doc for doc in paragraphs.find(query)]
all_sections = set([doc["DOI"].lower() for doc in docs])
print(len(all_sections))
#print(list(all_sections)[:5])

print("Reading training DOIs...")
with open(f"lowered_dois_for_synthesis_bert_training.pkl","rb") as file:
    training_doi_set = pickle.load(file)
print(list(training_doi_set)[:5])

forbidden_doi = all_sections & training_doi_set
print(f"In this collection, we have {len(forbidden_doi)} DOIs that were used for training.")

del all_sections, training_doi_set

if len(forbidden_doi) > 0:
    documents = [doc for doc in docs if doc["DOI"].lower() not in forbidden_doi]
    docs = documents
    del documents

# Randomly select n documents
selected_documents = random.sample(docs, n)

del docs

for i in range(n):
    #print ('\n\n\n= = = = = = = = = = = = = = = = = = =')
    #print(str(i+1)+' out of '+str(n))
    #print('- - - - - - - - - - - - - - - - - -')
    #print(selected_documents[i]["text"])
    #print('- - - - - - - - - - - - - - - - - -')
    #print("Classification: ", selected_documents[i]["classification"])
    #a = input('User classification? ')
    #if len(a)==0: 
    #    print('Ups! Once again, please')
    #    a = input('User classification? ')
    selected_documents[i]['user_classification'] = ""
    #print ('= = = = = = = = = = = = = = = = = = =')
with open(f"{col}_{synt}.json", 'w') as json_file:
    json.dump(selected_documents, json_file, indent=4, cls=CustomJSONEncoder)
print('THE END. GOOD JOB')