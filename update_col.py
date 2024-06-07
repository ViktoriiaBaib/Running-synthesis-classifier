#This script adds "classification" field to paragraphs collection from paragraphsmeta collection

from pymongo import MongoClient
from pprint import pprint

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

query = {"path": {"$regex": "preparation|prepared|experiment|method|material|synthes", "$options": "i"}}
queryS = {"classification": {"$regex": "synthesis", "$options": "i"}}
queryS1 = {"classification": {"$regex": "solid_state_ceramic_synthesis", "$options": "i"}}
queryS2 = {"classification": {"$regex": "hydrothermal_ceramic_synthesis", "$options": "i"}}
queryS3 = {"classification": {"$regex": "sol_gel_ceramic_synthesis", "$options": "i"}}
queryS4 = {"classification": {"$regex": "precipitation_ceramic_synthesis", "$options": "i"}}
#
result = paragraphs.update_many({},{"$set":{"classification":"filtered_out"}})
print(f"Adding classification to all. Documents updated: {result.modified_count}")
del result
result = paragraphs.update_many(query,{"$set":{"classification":"something_else"}})
print(f"Adding something else to those that passed filtration. Documents updated: {result.modified_count}")
del result
for syntclass in ["solid_state_ceramic_synthesis", "hydrothermal_ceramic_synthesis", "sol_gel_ceramic_synthesis", "precipitation_ceramic_synthesis"]:
    query = {"classification": {"$regex": syntclass, "$options": "i"}}
    sections = [doc["_id"] for doc in paragraphsmeta.find(query)]
    for section in sections:
        result = paragraphs.update_one({"_id":section},{"$set":{"classification":syntclass}})

#print examples to see that "classification" field was added
last_five_docs = paragraphs.find().sort('_id', -1).limit(5)
for doc in last_five_docs:
    pprint(doc)