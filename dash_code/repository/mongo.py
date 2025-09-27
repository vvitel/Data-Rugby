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
    collection_coordinates = None

    def __new__(cls):
        if cls._instance is None:
            client = MongoClient(os.getenv("DATABASE_URI"))
            db = client[os.getenv("DATABASE_NAME")]
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance.client = client
            cls._instance.collection_gps = db["gps"]
            cls._instance.collection_video = db["video"]
            cls._instance.collection_annotation = db["annotation"]
            cls._instance.collection_coordinates = db["coordinates"]
        return cls._instance
    
    def get_distinct_players(self, collection):
        pipeline = [
            {"$group": {"_id": "$player"}},
            {"$project": {"_id": 0, "player": "$_id"}}
        ]
        return list(collection.aggregate(
            pipeline,
            maxTimeMS=60000,
            allowDiskUse=True
        ))
        
    def get_distinct_dates(self, collection):
        pipeline = [
            {"$group": {"_id": "$date"}},
            {"$project": {"_id": 0, "date": "$_id"}}
        ]
        return list(collection.aggregate(
            pipeline,
            maxTimeMS=60000,
            allowDiskUse=True
        ))
        
    def get_distinct_matchs(self, collection):
        pipeline = [
            {"$group": {"_id": "$game"}},
            {"$project": {"_id": 0, "game": "$_id"}}
        ]
        return list(collection.aggregate(
            pipeline,
            maxTimeMS=60000,
            allowDiskUse=True
        ))
    
    def find_gps_unique(self, date=None, match=None, player=None):
        query = {}
        if date:
            query["date"] = date
        if match:
            query["game"] = match
        if player:
            query["player"] = player

        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "dates": {"$addToSet": "$date"},
                "matches": {"$addToSet": "$game"},
                "players": {"$addToSet": "$player"}
            }},
            {"$project": {"_id": 0}}
        ]
        res = list(self.collection_gps.aggregate(pipeline))
        if res:
            return res[0]["dates"], res[0]["matches"], res[0]["players"]
        return [], [], []    

    def find_gps_by_player(self, player):
        return self.collection_gps.find({"player": player})    

    def find_gps_by_date_and_match(self, date, match):
        return self.collection_gps.find({"date": date, "game": match})
    
    def find_gps_by_date_and_match_and_player(self, date, match, player):
        return self.collection_gps.find_one({"date": date, "game": match, "player": player})

    def find_video_by_date_and_match(self, date, match):
        return self.collection_video.find_one({"date": date, "game": match})
    
    def find_coordinates_by_date_and_match(self, date, match, start, buffer_size):
        pipeline = [
            {"$match": {"game": match, "date": date}},
            {
                "$project": {
                    "x": {"$slice": ["$x", start, start + buffer_size]},
                    "y": {"$slice": ["$y", start, start + buffer_size]},
                    "player": "$player",
                }
            },
        ]
        return list(
            self.collection_coordinates.aggregate(
                pipeline, maxTimeMS=60000, allowDiskUse=True
            )
        )