from pymongo import MongoClient

def connect_mongodb():
    uri = ""
    client = MongoClient(uri)
    client.admin.command("ping")
    db = client["GPS_database"]
    collec = db["gps"]
    return client, collec