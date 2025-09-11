from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    _instance = None
    
    client = None
    collection_gps = None
    collection_video = None
    collection_annotation = None

    def __new__(cls):
        if cls._instance is None:
            client = MongoClient(os.getenv("DATABASE_URI"))
            db = client[os.getenv("DATABASE_NAME")]
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance.client = client
            cls._instance.collection_gps = db["gps"]
            cls._instance.collection_video = db["video"]
            cls._instance.collection_annotation = db["annotation"]
        return cls._instance
    
    def get_distinct_players(self):
        pipeline = [
            {"$group": {"_id": "$player"}},
            {"$project": {"_id": 0, "player": "$_id"}}
        ]
        return list(self.collection_gps.aggregate(
            pipeline,
            maxTimeMS=60000,
            allowDiskUse=True
        ))
        
    def get_distinct_dates(self):
        pipeline = [
            {"$group": {"_id": "$date"}},
            {"$project": {"_id": 0, "date": "$_id"}}
        ]
        return list(self.collection_gps.aggregate(
            pipeline,
            maxTimeMS=60000,
            allowDiskUse=True
        ))
        
    def get_distinct_matchs(self):
        pipeline = [
            {"$group": {"_id": "$game"}},
            {"$project": {"_id": 0, "game": "$_id"}}
        ]
        return list(self.collection_gps.aggregate(
            pipeline,
            maxTimeMS=60000,
            allowDiskUse=True
        ))