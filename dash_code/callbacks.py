import numpy as np
import pandas as pd
from dash import callback, dcc, Output, Input
from dash_code.layout import create_layout
from send_to_database.functions.connect_database import connect_mongodb
from dash_code.functions.dash_functions import filter_dataframe

# Connection à la base de données
clt, collection_gps, collection_video = connect_mongodb()

# Récupérer tous les documents gps en dataframe
documents_gps = collection_gps.find({})
documents_gps = list(documents_gps)
df = pd.DataFrame(documents_gps)

# Récupérer tous les documents video en dataframe
documents_video = collection_video.find({})
documents_video = list(documents_video)
df_video = pd.DataFrame(documents_video)

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
            # Mise en forme de liste de dictionnaires
            dic = {"nom": row[choice], "0-5": round(dist_zone[0], 2), "5-10": round(dist_zone[1], 2),
                   "10-15": round(dist_zone[2], 2), "15-20": round(dist_zone[3], 2), "20-25": round(dist_zone[4], 2),
                   "25-30": round(dist_zone[5], 2)}
            lst_barplot_speeddistance.append(dic)
        # Trier par ordre décroissant
        lst_barplot_speeddistance = sorted(lst_barplot_speeddistance, key=lambda x: x["0-5"]+x["5-10"]+x["10-15"]+x["15-20"]+x["20-25"]+x["25-30"], reverse=True)
        return lst_barplot_speeddistance

def format_for_scatter_speedaccel(filter_df, choice):
     #Formater les données
     lst_scatter_speedaccel = []
     filter_df.reset_index(drop=True, inplace=True)
     for i, row in filter_df.iterrows():
          name = row[choice]
          max_speed = round(row["vitesse"][0] * 3.6, 2)
          max_accel = round(row["accel"][0], 2)
          lst_color = ["red.5", "pink.5", "grape.5", "violet.5", "indigo.5", "blue.5", "cyan.5",
                       "teal.5", "green.5", "lime.5", "yellow.5", "orange.5", "gray.5", "cyan.0"]
          # Mise en forme de liste de dictionnaires
          lst_scatter_speedaccel.append({"color": lst_color[i],
                                         "name": name,
                                         "data": [{"vitesse": max_speed, "acceleration": max_accel}]})
     return lst_scatter_speedaccel

def format_for_barplot_accel(filter_df, choice):
     # Formatter les données
     lst_barplot_accel = []
     for i, row in filter_df.iterrows():
          name = row[choice]
          nb_accel = row["nb_acceleration"]
          dic = {"nom": name, "nombre d'accélération":nb_accel}
          lst_barplot_accel.append(dic)
          lst_barplot_color = [{"name": "nombre d'accélération", "color": "violet.6"}]
     # Trier par ordre décroissant
     lst_barplot_accel = sorted(lst_barplot_accel, key=lambda x: x["nombre d'accélération"], reverse=True)
     return lst_barplot_accel, lst_barplot_color

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
        df_filter = df[(df["date"] == date) & (df["game"] == match)]
        lst_data = format_for_barplot_speeddistance(df_filter, "player")
        height_barplot = 400 if 40 * len(lst_data) < 400 else 40 * len(lst_data)
        return lst_data, "nom", lst_color, height_barplot, {"display": "block"}, {"display": "block"}
    # Cas si on veut les résultats pour un joueur
    elif joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["player"] == joueur)]
        if date : df_filter = df_filter[(df_filter["date"] == date)]
        if match : df_filter = df_filter[(df_filter["game"] == match)]
        lst_data = format_for_barplot_speeddistance(df_filter, "game")
        height_barplot = 400 if 40 * len(lst_data) < 400 else 40 * len(lst_data)
        return lst_data, "nom", lst_color, height_barplot, {"display": "block"}, {"display": "block"}
    else:
         return [], "", [], 0, {"display": "none"}, {"display": "none"}

# Créer le scatterplot vitesse/acceleration
@callback([Output("scatter_vitesse_accel", "data"),
           Output("scatter_vitesse_accel", "style"),
           Output("title_scatterspeedaccel", "style")],
           [Input("select_date", "value"),
           Input("select_match", "value"),
           Input("select_joueur", "value")],
           prevent_initial_call=True)
def create_scatter_speedaccel(date, match, joueur):
    # Cas si on veut les résultats pour un match
    if (date and match) and not joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["date"] == date) & (df["game"] == match)]
        lst_data = format_for_scatter_speedaccel(df_filter, "player")
        return lst_data, {"display": "block"}, {"display": "block"}
     # Cas si on veut les résultats pour un joueur
    elif joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["player"] == joueur)]
        if date : df_filter = df_filter[(df_filter["date"] == date)]
        if match : df_filter = df_filter[(df_filter["game"] == match)]
        lst_data = format_for_scatter_speedaccel(df_filter, "game")
        return lst_data, {"display": "block"}, {"display": "block"}
    else:
         return [], {"display": "none"}, {"display": "none"}

# Créer le barplot nombre d'accélération
@callback([Output("barplot_accel", "data"),
           Output("barplot_accel", "dataKey"),
           Output("barplot_accel", "series"),
           Output("title_nbaccel", "style"),
           Output("barplot_accel", "style")],
           [Input("select_date", "value"),
           Input("select_match", "value"),
           Input("select_joueur", "value")],
           prevent_initial_call=True)
def create_barplot_accel(date, match, joueur):
    # Cas si on veut les résultats pour un match
    if (date and match) and not joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["date"] == date) & (df["game"] == match)]
        lst_data, lst_color = format_for_barplot_accel(df_filter, "player")
        return lst_data, "nom", lst_color, {"display": "block"}, {"display": "block"}
     # Cas si on veut les résultats pour un joueur
    elif joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["player"] == joueur)]
        if date : df_filter = df_filter[(df_filter["date"] == date)]
        if match : df_filter = df_filter[(df_filter["game"] == match)]
        lst_data, lst_color = format_for_barplot_accel(df_filter, "game")
        return lst_data, "nom", lst_color, {"display": "block"}, {"display": "block"}
    else:
         return [], "nom", [], {"display": "none"}, {"display": "none"}
    
# Créer donutchart pour comparaison avec le niveau international
@callback([Output("donut_vmax", "data"),
           Output("donut_vmax", "style"),
           Output("donut_amax", "data"),
           Output("donut_amax", "style"),
           Output("title_donut", "style")],
           Input("select_joueur", "value"),
           prevent_initial_call=True)
def create_donutchart(joueur):
    if joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["player"] == joueur)]
        df_filter.reset_index(drop=True, inplace=True)
        measured_vmax = max([i[0] for i in df_filter["vitesse"]])
        measured_amax = max([i[0] for i in df_filter["accel"]])
        # Calculer une note sur 100
        note_100_vmax = round(measured_vmax * 100 / 9.53, 1)
        note_100_amax = round(measured_amax * 100 / 5.70, 1)
        remainder_100_vmax = round(100 - note_100_vmax, 1)
        remainder_100_amax = round(100 - note_100_amax, 1)
        # Éléments à retourner
        data_donut_vmax = [{"name": "vmax mesurée", "value": note_100_vmax, "color": "indigo.4"}, {"name": "vmax théorique", "value": remainder_100_vmax, "color": "gray.4"}]
        data_donut_amax = [{"name": "vmax mesurée", "value": note_100_amax, "color": "indigo.4"}, {"name": "vmax théorique", "value": remainder_100_amax, "color": "gray.4"}]
        return data_donut_vmax, {"display": "block"}, data_donut_amax, {"display": "block"}, {"display": "block"}
    else:
        return [], {"display": "none"}, [], {"display": "none"}, {"display": "none"}

# Télécharger les données
@callback([Output("download_data", "data"),
           Output("btn_download_data", "n_clicks")],
          [Input("select_date", "value"),
           Input("select_match", "value"),
           Input("select_joueur", "value"),
           Input("btn_download_data", "n_clicks")],
           prevent_initial_call=True)
def download_data(date, match, joueur, n_clicks):
    # Cas si on veut les résultats pour un match
    if (date and match) and not joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["date"] == date) & (df["game"] == match)]
    # Cas si on veut les résultats pour un joueur
    elif joueur:
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["player"] == joueur)]
        if date : df_filter = df_filter[(df_filter["date"] == date)]
        if match : df_filter = df_filter[(df_filter["game"] == match)]
    # Télécharger si on clique sur le bouton
    if (n_clicks) and ("df_filter" in locals()):
        return dcc.send_data_frame(df_filter.to_csv, filename="data_RQ.csv", index=False), 0
    else:
        return None, 0

# Créer slider pour sélectionner les événements
@callback([Output("slider_action", "value"),
           Output("slider_action", "marks"), 
           Output("slider_action", "style")],
           [Input("select_date_video", "value"),
           Input("select_match_video", "value"),
           Input("select_joueur_video", "value"),
           Input("select_metrique_video", "value"),
           Input("select_action_video", "value")],
           prevent_initial_call=True)
def create_slider(date, match, joueur, metric, action):
    if (date and match and action) and not joueur and not metric:
        # Filtrer les données en fonction de la valeurs des selects
        kickoff = df_video["kickoff"][(df_video["date"] == date) & (df_video["game"] == match)].iloc[0]
        # Récupérer la durée de la vidéo
        duration_vidéo = df_video["temps"][(df_video["date"] == date) & (df_video["game"] == match)].iloc[0]
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df_video[(df_video["date"] == date) & (df_video["game"] == match)]
        df_filter.reset_index(drop=True, inplace=True)
        # Occurences de l'action sélectionnée
        event = np.array(df_filter[action].iloc[0]).astype(float)
        # Convertir le temps - on ajoute 4 heures
        event_time = event - float(kickoff)
        event_percent = event_time * 100 / duration_vidéo
        # Créer les marques sur le slider
        marks = [{"value": round(percent), "label": round(label - 15)} for label, percent in zip(event_time, event_percent)]
        value = marks[0]["value"]
        return value, marks, {"display": "block"}
    else:
        return 0, [{"value": 0}], {"display": "none"}

# Afficher la vidéo
@callback([Output("yt_video", "url"),
           Output("yt_video", "style")],
           [Input("select_date_video", "value"),
           Input("select_match_video", "value"),
           Input("select_joueur_video", "value"),
           Input("select_metrique_video", "value"),
           Input("select_action_video", "value"),
           Input("slider_action", "value"),
           Input("slider_action", "marks")],
           prevent_initial_call=True)
def show_video(date, match, joueur, metric, action, value, marks):
     # Cas si on veut voir toute la vidéo
     if (date and match) and not action and not joueur and not metric:
        # Filtrer les données en fonction de la valeurs des selects
        id_vid = df_video["lien"][(df_video["date"] == date) & (df_video["game"] == match)].iloc[0]
        url = f"https://www.youtube.com/watch?v={id_vid}"
        return url, {"display": "block"}
     # Cas ou on souhaite voir vidéo métrique max
     if date and match and joueur and metric and not action:
        id_vid = df_video["lien"][(df_video["date"] == date) & (df_video["game"] == match)].iloc[0]
        kickoff = df_video["kickoff"][(df_video["date"] == date) & (df_video["game"] == match)].iloc[0]
        url = f"https://www.youtube.com/watch?v={id_vid}"
        # Filtrer les données en fonction de la valeurs des selects
        df_filter = df[(df["date"] == date) & (df["game"] == match) & (df["player"] == joueur)]
        # Trouver temps correspondant à la valeur maximale
        tps_max = df_filter[f"{metric}_temps"].iloc[0][0]
        # Convertir le temps - on ajoute 4 heures
        tps_max_convert = (tps_max + 14400) - float(kickoff)
        tps_max_convert = round(tps_max_convert)
        # Préciser le temps dans l'url
        url = f"{url}&t={tps_max_convert}s"
        return url, {"display": "block"}
     # Afficher la vidéo avec possibilité de sélectionner les actions
     if (date and match and action) and not joueur and not metric:
        id_vid = df_video["lien"][(df_video["date"] == date) & (df_video["game"] == match)].iloc[0]
        url = f"https://www.youtube.com/watch?v={id_vid}"
        tps_sec = next(item["label"] for item in marks if item["value"] == value)
        # Préciser le temps dans l'url
        url = f"{url}&t={tps_sec}s"
        return url, {"display": "block"}
     else:
         return "", {"display": "none"}
     
         