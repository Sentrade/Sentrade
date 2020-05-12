from pymongo import MongoClient

def get_database_count(client_address, database_name):
    client = MongoClient(client_address)
    db = client[database_name]
    companies = ["apple", "amazon", "facebook", "google", "microsoft", "netflix", "tesla", "uber"]
    for company in companies:
        print("In {:<15} {:<9} contains {:>6} entries".format(database_name, company, db[company].count_documents({})))
        
if __name__ == "__main__":
    client_address = "mongodb://admin:sentrade@45.76.133.175:27017"
    get_database_count(client_address, "twitter_filtered")
    get_database_count(client_address, "twitter_data")


