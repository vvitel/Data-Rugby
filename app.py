import pandas as pd
from send_to_database.functions.connect_database import connect_mongodb
from dash import Dash
from dash_code.layout import create_layout
from dash_code.callbacks import *
from pymongo import MongoClient

# Connection à la base de données
clt, collection = connect_mongodb()

# Récupérer tous les documents en dataframe
documents = collection.find({})
documents = list(documents)
df = pd.DataFrame(documents)

# Récupérer les informations pour les noms, dates, matchs
date_dic = [{"value": i, "label": i} for i in pd.unique(df["date"])]
match_dic = [{"value": i, "label": i} for i in pd.unique(df["game"])]
joueur_dic = [{"value": i, "label": i} for i in pd.unique(df["player"])]

# Création du front de l'app
front = create_layout(date_dic, match_dic, joueur_dic)

# Code de l'application
app = Dash(__name__)
server = app.server
app.layout = front

if __name__ == "__main__":
    app.run(debug=True)