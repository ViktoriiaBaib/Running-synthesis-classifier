from pymongo import MongoClient
from synthesis_classifier import get_model, get_tokenizer, run_batch
from pymongo.errors import BulkWriteError
import argparse
from bson import ObjectId

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', type=int, default=0)
parser.add_argument('-f', '--fileid', type=int, default=0)
parser.add_argument('-b', '--size', type=int, default=400000)
parser.add_argument('-c', '--collection', type=str, default='A')
args = parser.parse_args()

size = args.size
col = args.collection
fileid = args.fileid
index = args.index

print("Connecting to DB...")

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
    collection = client.db.AParagraphs
    # New collection for insertions
    new_collection = client.db.AParagraphsMeta

#to choose synthesis paragraphs
query = {"path": {"$regex": "preparation|prepared|experiment|method|material|synthes", "$options": "i"}}

all_documents = [doc for doc in collection.find(query)]

start = size*index

documents = all_documents[start:min(start+size, len(all_documents))]
#free memory
del all_documents
n_doc = len(documents)
print(f"Today we work with {n_doc} relevant paragraphs.")

batch_size = 16
n_batches = n_doc // batch_size

print("\n\nMatBERT synthesis classifier\n\n")

# Preparing model and tokenizer
model = get_model()
tokenizer = get_tokenizer()

# Running classification and inserting to the new DB
for j in range(0,n_batches+1):
    batch = documents[j*batch_size:min((j+1)*batch_size,n_doc)]
    # "text" is where actual paragraph is stored
    texts = [doc["text"] for doc in batch]
    results = run_batch(texts, model, tokenizer)
    # Creating new docs from results and original documents
    new_docs = []
    for doc, res in zip(batch, results):
        max_classification = max(res["scores"], key=res["scores"].get)
        new_doc = {
            "_id": doc["_id"],
            "text": doc["text"],
            "scores": res["scores"],
            "classification": max_classification
        }
        new_docs.append(new_doc)

    # Inserting in bulk for efficiency
    try:
        new_collection.insert_many(new_docs)
        print(f"Batch {j} success!")
    except BulkWriteError as bwe:
        print("Bulk Write Error encountered:", bwe.details)

#CHECK INSERTIONS
#print("Final lenght of new collection is: ",len(list(new_collection.find())))