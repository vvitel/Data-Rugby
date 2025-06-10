import numpy as np
import pandas as pd
from dash import callback, Output, Input
from dash_code.layout import create_layout
from send_to_database.functions.connect_database import connect_mongodb
from dash_code.functions.dash_functions import filter_dataframe

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

# Récupérer le front
front = create_layout(date_dic, match_dic, joueur_dic)

# Functions
def format_for_barplot_speeddistance(filter_df, choice):
     # Formater les données
        lst_barplot_speeddistance = []
        for _, row in filter_df.iterrows():
            dist_zone = row["distance_zone"]
            # Mise en forme de liste de dictionnaire
            dic = {"nom": row[choice], "0-5": round(dist_zone[0], 2), "5-10": round(dist_zone[1], 2),
                   "10-15": round(dist_zone[2], 2), "15-20": round(dist_zone[3], 2), "20-25": round(dist_zone[4], 2),
                   "25-30": round(dist_zone[5], 2)}
            lst_barplot_speeddistance.append(dic)
        # Trier par ordre décroissant
        lst_barplot_speeddistance = sorted(lst_barplot_speeddistance, key=lambda x: x["0-5"]+x["5-10"]+x["10-15"]+x["15-20"]+x["20-25"]+x["25-30"], reverse=True)
        return lst_barplot_speeddistance


# Mettre à jour les selects en fonction des sélections en cours - GPS
@callback(
    [Output("select_date", "data"),
     Output("select_match", "data"),
     Output("select_joueur", "data")],
    [Input("select_date", "value"),
     Input("select_match", "value"),
     Input("select_joueur", "value")],
     prevent_initial_call=True)
def update_select(date, match, file):
    # Filtrer les données
    filtered_data = filter_dataframe(df, selected_date=date, selected_match=match, selected_name=file)
    date_options = np.unique(filtered_data.date)
    match_options = np.unique(filtered_data.game)
    player_options = np.unique(filtered_data.player)
    return date_options, match_options, player_options

# Mettre à jour les selects en fonction des sélections en cours - VIDEO
@callback(
    [Output("select_date_video", "data"),
     Output("select_match_video", "data"),
     Output("select_joueur_video", "data")],
    [Input("select_date_video", "value"),
     Input("select_match_video", "value"),
     Input("select_joueur_video", "value")],
     prevent_initial_call=True)
def update_select(date, match, file):
    #filtrer les données
    filtered_data = filter_dataframe(df, selected_date=date, selected_match=match, selected_name=file)
    date_options = np.unique(filtered_data.date)
    match_options = np.unique(filtered_data.game)
    player_options = np.unique(filtered_data.player)
    return date_options, match_options, player_options

# Créer le barplot distance par zone de vitesse
@callback([Output("barplot_dist", "data"),
           Output("barplot_dist", "dataKey"),
           Output("barplot_dist", "series"),
           Output("barplot_dist", "h"),
           Output("title_barplot", "style"),
           Output("barplot_dist", "style")],
           [Input("select_date", "value"),
           Input("select_match", "value"),
           Input("select_joueur", "value")],
           prevent_initial_call=True)
def create_barplot_speeddistance(date, match, joueur):
     # Définir style
    lst_color = [{"name": "0-5", "color": "violet.6"}, {"name": "5-10", "color": "blue.6"}, {"name": "10-15", "color": "teal.6"}, 
                    {"name": "15-20", "color": "green.6"}, {"name": "20-25", "color": "yellow.6"}, {"name": "25-30", "color": "orange.6"}]
    # Cas si on veut les résultats pour un match
    if (date and match) and not joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["date"]== date) & (df["game"]== match)]
        lst_data = format_for_barplot_speeddistance(df_filter, "player")
        height_barplot = 400 if 40 * len(lst_data) < 400 else 40 * len(lst_data)
        return lst_data, "nom", lst_color, height_barplot, {"display": "block"}, {"display": "block"}
    # Cas si on veut les résultats pour un joueur
    elif joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["player"]== joueur)]
        if date : df_filter = df[(df["date"]== date)]
        if match : df_filter = df[(df["game"]== match)]
        lst_data = format_for_barplot_speeddistance(df_filter, "game")
        height_barplot = 400 if 40 * len(lst_data) < 400 else 40 * len(lst_data)
        return lst_data, "nom", lst_color, height_barplot, {"display": "block"}, {"display": "block"}
    else:
         return [], "", [], 0, {"display": "none"}, {"display": "none"}
       







