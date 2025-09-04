from pymongo import MongoClient

def connect_mongodb():
    uri = ""
    client = MongoClient(uri)
    client.admin.command("ping")
    db = client["GPS_database"]
    collec_gps = db["gps"]
    collec_video = db["video"]
    collec_annotation = db["annotation"]
    return client, collec_gps, collec_video, collec_annotation