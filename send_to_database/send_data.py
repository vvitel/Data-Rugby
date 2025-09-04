import argparse
import os
from functions.compute_metrics import compute_all
from functions.connect_database import connect_mongodb
from functions.read_data import get_data
from tqdm import tqdm

# Définir les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-game", "--game", required=True, type=str)
ap.add_argument("-competition", "--competition", required=True, type=str)
ap.add_argument("-coord_field", "--coord_field", required=False, type=str)
ap.add_argument("-start", "--start", required=False, type=float)
ap.add_argument("-end", "--end", required=False, type=float)
ap.add_argument("-commentaire", "--commentaire", required=False, type=str)
args = ap.parse_args()
game, competition, coord_field = args.game, args.competition, args.coord_field
start, end = args.start, args.end
commentaire = args.commentaire

# Connection à la base de données
clt, collection_gps, collection_video = connect_mongodb()

# Récupérer les données
files = os.listdir("../temp")
for f in tqdm(files):
    date, player, time, latitude, longitude = get_data(f"../temp/{f}", start, end)

    # Calculer les métriques
    l1, l2, l3, l4, l5, nb_accel = compute_all(latitude, longitude, time, zone=18)

    # Créer le document à enregistrer
    document = {"player": player,
                "date": date,
                "game": game,
                "competition": competition,
                "coord_field": coord_field,
                "commentaire": commentaire,
                "distance_zone": l1,
                "vitesse": l2,
                "vitesse_temps": l3,
                "accel": l4,
                "accel_temps": l5,
                "nb_acceleration": nb_accel,
                "nb_impact": 0}
    
    # Enregistrer dans la base de données
    collection_gps.insert_one(document)

# Afficher fin de l'ajout
print("Données ajoutées dans la base de données")