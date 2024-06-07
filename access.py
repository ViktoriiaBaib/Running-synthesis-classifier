from pymongo import MongoClient
from pprint import pprint
from collections import Counter

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
    paragraphs = client.db.AParagraphs
    # New collection for insertions
    paragraphsmeta = client.db.AParagraphsMeta

number_of_documents = paragraphs.count_documents({})
query = {"path": {"$regex": "preparation|prepared|experiment|method|material|synthes", "$options": "i"}}
synt_docs = paragraphs.count_documents(query)
print(f"\n\nParagraphs collection has {number_of_documents} files, need to classify filtered {synt_docs}")

number_of_documents = paragraphsmeta.count_documents({})
queryS = {"classification": {"$regex": "synthesis", "$options": "i"}}
synt_docs = paragraphsmeta.count_documents(queryS)
print(f"Paragraphs Meta collection has {number_of_documents} files, classified as synthesis {synt_docs}\n")

synt_counts = Counter([doc["classification"] for doc in paragraphsmeta.find(queryS)])
print("Paragraphs Meta collection has the following counts for synthesis types:\n", synt_counts)