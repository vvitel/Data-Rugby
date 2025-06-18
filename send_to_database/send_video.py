import argparse
from functions.connect_database import connect_mongodb

# Définir les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-date", "--date", required=True, type=str)
ap.add_argument("-game", "--game", required=True, type=str)
ap.add_argument("-competition", "--competition", required=True, type=str)
ap.add_argument("-lien", "--lien", required=False, type=str)
ap.add_argument("-commentaire", "--commentaire", required=False, type=str)
args = ap.parse_args()
date, game, competition = args.date, args.game, args.competition
lien, commentaire = args.lien, args.commentaire

# Connection à la base de données
clt, collection_gps, collection_video = connect_mongodb()

# Créer le document à enregistrer
document = {"date": date,
            "game": game,
            "competition": competition,
            "lien": lien,
            "commentaire": commentaire}
    
# Enregistrer dans la base de données
collection_video.insert_one(document)