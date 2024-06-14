from pymongo import MongoClient
from pprint import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--collection', type=str, default="IOP")
args = parser.parse_args()

col = args.collection

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
SynDev_client = MongoClient(
    'mongodb://synthesisproject.lbl.gov:27017',
    username='vbaibakova',
    password='vbaibakova2023',
    authSource='SynDev',
    authMechanism='SCRAM-SHA-1'
)

syndev_db = SynDev_client.SynDev

if col=="Elsevier":
    print("Connecting to Elsevier")
    paragraphs = syndev_db.ElsevierParagraphs
if col=="AIP":
    print("Connecting to AIP")
    paragraphs = syndev_db.AIPParagraphs
if col=="RSC":
    print("Connecting to RSC")
    paragraphs = syndev_db.RSCParagraphs
if col=="IOP": #UPDATE TO V2
    print("Connecting to IOP")
    paragraphs = syndev_db.IOPParagraphs_v2
if col=="Nature":
    print("Connecting to Nature")
    paragraphs = syndev_db.SpringerNatureParagraphs

number_of_documents = paragraphs.count_documents({})
query0 = {"classification": {"$regex": "filtered_out", "$options": "i"}}
query1 = {"classification": {"$regex": "something_else", "$options": "i"}}
#query = {"path": {"$regex": "preparation|prepared|experiment|method|material|synthes", "$options": "i"}}
queryS = {"classification": {"$regex": "synthesis", "$options": "i"}}
fo_docs = paragraphs.count_documents(query0)
se_docs = paragraphs.count_documents(query1)
synt_docs = paragraphs.count_documents(queryS)
print(f"\n\n{col} Paragraphs collection files: {number_of_documents} \n filtered out: {fo_docs} \n something else: {se_docs} \n synthesis: {synt_docs}")

queryS1 = {"classification": {"$regex": "solid_state_ceramic_synthesis", "$options": "i"}}
queryS2 = {"classification": {"$regex": "hydrothermal_ceramic_synthesis", "$options": "i"}}
queryS3 = {"classification": {"$regex": "sol_gel_ceramic_synthesis", "$options": "i"}}
queryS4 = {"classification": {"$regex": "precipitation_ceramic_synthesis", "$options": "i"}}

ss_docs = paragraphs.count_documents(queryS1)
hc_docs = paragraphs.count_documents(queryS2)
sg_docs = paragraphs.count_documents(queryS3)
pc_docs = paragraphs.count_documents(queryS4)
print(f" solid_state: {ss_docs} \n hydrothermal: {hc_docs} \n sol_gel: {sg_docs} \n precipitation: {pc_docs}")