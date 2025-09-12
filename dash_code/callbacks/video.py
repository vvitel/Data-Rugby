import numpy as np
from dash import callback, Output, Input
from dash_code.repository.mongo import MongoDB

# Connection à la base de données
mongo = MongoDB()

# Créer slider pour sélectionner les événements
@callback(
    [
        Output("slider_action", "value"),
        Output("slider_action", "marks"),
        Output("slider_action", "style"),
    ],
    [
        Input("select_date_video", "value"),
        Input("select_match_video", "value"),
        Input("select_joueur_video", "value"),
        Input("select_metrique_video", "value"),
        Input("select_action_video", "value"),
    ],
    prevent_initial_call=True,
)
def create_slider(date, match, joueur, metric, action):
    if (date and match and action) and not joueur and not metric:
        # Requêter la base de données
        document = mongo.find_video_by_date_and_match(date, match)
        kickoff = document["kickoff"]
        duration_vidéo = document["temps"]
        # Occurences de l'action sélectionnée
        event = np.array(document[action]).astype(float)
        # Convertir le temps - on ajoute 4 heures
        event_time = event - float(kickoff)
        event_percent = event_time * 100 / duration_vidéo
        # Créer les marques sur le slider
        marks = [
            {"value": round(percent), "label": round(label - 15)}
            for label, percent in zip(event_time, event_percent)
        ]
        value = marks[0]["value"]
        return value, marks, {"display": "block"}
    else:
        return 0, [{"value": 0}], {"display": "none"}

# Afficher la vidéo
@callback(
    [Output("yt_video", "url"), Output("yt_video", "style")],
    [
        Input("select_date_video", "value"),
        Input("select_match_video", "value"),
        Input("select_joueur_video", "value"),
        Input("select_metrique_video", "value"),
        Input("select_action_video", "value"),
        Input("slider_action", "value"),
        Input("slider_action", "marks"),
    ],
    prevent_initial_call=True,
)
def show_video(date, match, joueur, metric, action, value, marks):
    
    # Cas si on veut voir toute la vidéo
    if (date and match) and not action and not joueur and not metric:
        # Requêter la base de données
        document_video = mongo.find_video_by_date_and_match(date, match)
        id_vid = document_video["lien"]
        url = f"https://www.youtube.com/watch?v={id_vid}"
        return url, {"display": "block"}
    # Cas ou on souhaite voir vidéo métrique max
    if date and match and joueur and metric and not action:
        # Requêter la base de données
        document_video = mongo.find_video_by_date_and_match(date, match)
        id_vid = document_video["lien"]
        kickoff = document_video["kickoff"]
        url = f"https://www.youtube.com/watch?v={id_vid}"
        # Requêter la base de données
        document_gps = mongo.find_gps_by_date_and_match_and_player(date, match, joueur)
        # Trouver temps correspondant à la valeur maximale
        tps_max = document_gps[f"{metric}_temps"][0]
        # Convertir le temps - on ajoute 4 heures
        tps_max_convert = (tps_max + 14400) - float(kickoff)
        tps_max_convert = round(tps_max_convert)
        # Préciser le temps dans l'url
        url = f"{url}&t={tps_max_convert}s"
        return url, {"display": "block"}
    # Afficher la vidéo avec possibilité de sélectionner les actions
    if (date and match and action) and not joueur and not metric:
        # Requêter la base de données
        document_video = mongo.find_video_by_date_and_match(date, match)
        id_vid = document_video["lien"]
        url = f"https://www.youtube.com/watch?v={id_vid}"

        
        tps_sec = next(item["label"] for item in marks if item["value"] == value)
        # Préciser le temps dans l'url
        url = f"{url}&t={tps_sec}s"
        return url, {"display": "block"}
    else:
        return "", {"display": "none"}








    

