import argparse
import cv2
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
clt, _, collection_video, _ = connect_mongodb()

# Récupérer la durée de la vidéo
cap = cv2.VideoCapture(lien)
nb_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Créer le document à enregistrer
document = {"date": date,
            "game": game,
            "competition": competition,
            "lien": lien,
            "nb_frames": nb_frames,
            "fps": fps,
            "commentaire": commentaire}
    
# Enregistrer dans la base de données
collection_video.insert_one(document)