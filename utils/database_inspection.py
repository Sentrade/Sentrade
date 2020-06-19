from pymongo import MongoClient
import os

def get_database_count(client_address, database_name):
    client = MongoClient(client_address)
    db = client[database_name]
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    for company in companies:
        print("In {:<15} {:<9} contains {:>6} entries".format(database_name, company, db[company].count_documents({})))
        
if __name__ == "__main__":
    client_address = os.environ["CLIENT_ADDR"]
    get_database_count(client_address, "twitter_filtered")
    get_database_count(client_address, "twitter_data")


