import numpy as np
import plotly.graph_objs as go
from collections import defaultdict
from dash import callback, clientside_callback, Output, Input, State, no_update
from dash_code.repository.mongo import MongoDB

# Connection à la base de données
mongo = MongoDB()

# Constantes d'affichage
visible = {"display": "block"}
hidden = {"display": "none"}

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
        duration_vidéo = document["nb_frames"] / document["fps"]
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
        return value, marks, visible
    else:
        return 0, [{"value": 0}], hidden

# Afficher la vidéo
@callback(
    [
        Output("player_video", "url"),
        Output("player_video", "seekTo"),
        Output("player_video", "style")
    ],
    [
        Input("select_date_video", "value"),
        Input("select_match_video", "value"),
        Input("select_joueur_video", "value"),
        Input("select_metrique_video", "value"),
        Input("select_action_video", "value"),
        Input("slider_action", "value"),
        Input("slider_action", "marks")
    ],
    prevent_initial_call=True,
)
def show_video(date, match, joueur, metric, action, value, marks):
    # Cas si on veut voir toute la vidéo
    if (date and match) and not action and not joueur and not metric:
        # Requêter la base de données
        document_video = mongo.find_video_by_date_and_match(date, match)
        lien = document_video["lien"]
        return lien, 0, visible
    # Cas ou on souhaite voir vidéo métrique max
    if date and match and joueur and metric and not action:
        # Requêter la base de données
        document_video = mongo.find_video_by_date_and_match(date, match)
        lien = document_video["lien"]
        kickoff = document_video["kickoff"]
        # Requêter la base de données
        document_gps = mongo.find_gps_by_date_and_match_and_player(date, match, joueur)
        # Trouver temps correspondant à la valeur maximale
        tps_max = document_gps[f"{metric}_temps"][0]
        # Convertir le temps - on ajoute 4 heures
        tps_max_convert = (tps_max + 14400) - float(kickoff)
        tps_max_convert = round(tps_max_convert)
        return lien, tps_max_convert, visible
    # Afficher la vidéo avec possibilité de sélectionner les actions
    if (date and match and action) and not joueur and not metric:
        # Requêter la base de données
        document_video = mongo.find_video_by_date_and_match(date, match)
        lien = document_video["lien"]
        tps_sec = next(item["label"] for item in marks if item["value"] == value)
        return lien, tps_sec, visible
    else:
        return "", 0, hidden
    

# Requêter la base de données pour avoir les positions des joueurs
@callback(
    [
        Output("store_coordinates", "data"),
        Output("trigger_request", "data", allow_duplicate=True)
    ],
    [
        Input("select_date_video", "value"),
        Input("select_match_video", "value"),
        Input("trigger_request", "data")
    ],
    [
        State("start_request", "data"),
    ],
    prevent_initial_call=True,
)
def get_player_position(date, match, trigger_request, start_request):
    if (date and match and trigger_request):
        trigger_request = False
        document_coordinates = mongo.find_coordinates_by_date_and_match(date, match, int(start_request))
        res = {}
        for doc in document_coordinates:
            res[doc["player"]] = {"x": doc["x"], "y": doc["y"]}
        return res, trigger_request
    else:
        trigger_request = True
        return no_update, trigger_request


# Réaliser le graphique de la position des joueurs
@callback(
    [
        Output("map_chart", "figure"),
        Output("map_chart", "style"),
        Output("start_request", "data"),
        Output("trigger_request", "data", allow_duplicate=True)
    ],
    [
        Input("select_date_video", "value"),
        Input("select_match_video", "value"),
        Input("store_coordinates", "data"),
        Input("player_video", "currentTime"),
        Input("select_joueur_video", "value"),
        Input("select_metrique_video", "value"),
        Input("select_action_video", "value"),
        State("start_request", "data")
    ],
    prevent_initial_call=True,
)
def create_position_plot(date, match, data, time_video, joueur, metric, action, start_request):
    if all([date, match, time_video]) and not any([joueur, metric, action]):
        # Calculer la frame par rapport au temps de la vidéo
        fps = 29.97002997002997
        #if frame is None: time_video = 0
        frame = round(time_video * fps)
        # Si on sort de la range de la requête
        if (frame < start_request or frame >= start_request + 7_000):
            fig, fig_style, start_request, trigger_request = go.Figure(), hidden, frame, True
            return fig, fig_style, start_request, trigger_request
        # Si on est dans la range de la requête
        else:
            # On ne relance pas la requête
            trigger_request = False
            # Initialiser l'index
            index = (frame - start_request) % 7_000
            # Parcourir l'index pour récupérer les coordonnées
            x, y = [], []
            for player in data:
                x.append(data[player]["x"][index])
                y.append(data[player]["y"][index])
            # Créer le graphique
            fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="markers", marker=dict(size=8))],
                            layout=go.Layout(
                                xaxis=dict(range=[100, 0], showticklabels=False, ticks="", showgrid=False),
                                yaxis=dict(range=[0, -60], showticklabels=False, ticks="", showgrid=False),
                                margin=dict(l=0, r=0, t=0, b=0),
                                height=300,
                                plot_bgcolor="lightgreen",
                                shapes=[
                                    dict(
                                        type="line",
                                        x0=50, x1=50,
                                        y0=0, y1=-60,
                                        line=dict(color="black", width=2)
                                    )
                                ]
                            )
                    )
            fig_style = visible
            return fig, fig_style, start_request, trigger_request
    else:
        fig, fig_style, start_request, trigger_request = go.Figure(), hidden, 0, True
        return fig, fig_style, start_request, trigger_request