import numpy as np
from dash import callback, clientside_callback, Output, Input, State
from dash_code.repository.mongo import MongoDB
from dash_code.managers.videocache import VideoCacheManager
import plotly.graph_objects as go

# Connection à la base de données
mongo = MongoDB()

cache_manager = VideoCacheManager()

BUFFER_SIZE = 300
FPS = 29.97002997002997


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
        Output("player_video", "style"),
    ],
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


@callback(
    Output("map_chart", "figure"),
    [
        Input("select_date_video", "value"),
        Input("select_match_video", "value"),
        Input("player_video", "currentTime"),
    ],
    prevent_initial_call=True,
)
def display_plot_player_position(date, match, current_time):

    if not date or not match or not current_time:
        return

    frame = int(round(current_time * FPS))

    # Check si on a dans le cache la data
    tracking = cache_manager.get(date, match, frame)

    # sinon faire un update avec la bdd
    if tracking == None:
        cache_manager.clear_key(date, match)

        document_coordinates = mongo.find_coordinates_by_date_and_match(
            date, match, frame, BUFFER_SIZE
        )
        res = {}
        for doc in document_coordinates:
            res[doc["player"]] = {"x": doc["x"], "y": doc["y"]}

        tracking = cache_manager.set(date, match, frame, frame + BUFFER_SIZE, res)

    index = (frame - tracking["start"]) % BUFFER_SIZE

    points = [
        go.Scatter(
            x=[50, 50],
            y=[-60, 0],
            mode="lines",
            line={"color": "black", "width": 2},
            showlegend=False,
        )
    ]

    for player_name, player_data in tracking["players"].items():
        points.append(
            go.Scatter(
                x=[player_data["x"][index]],
                y=[player_data["y"][index]],
                mode="markers",
                marker={"size": 12, "color": "blue"},
                showlegend=False,
            )
        )

    return go.Figure(
        data=points,
        layout=go.Layout(
            plot_bgcolor="lightgreen",
            height=300,
            margin=go.layout.Margin(t=0, b=0, l=0, r=0),
            xaxis=go.layout.XAxis(
                autorange=False,
                dtick=1,
                range=[100, 0],
                showticklabels=False,
            ),
            yaxis=go.layout.YAxis(
                autorange=False,
                dtick=1,
                range=[0, -60],
                showticklabels=False,
            ),
        ),
    )


# Déclencher le script JS pour dessiner sur la vidéo
clientside_callback(
    """
    function(date, match) {
        if (date && match) {
            setTimeout(function() {
                window.trigger();
            }, 500);
        }
        return "";
    }
    """,
    Output("store_inutile_utile", "data", allow_duplicate=True),
    Input("select_date_video", "value"),
    Input("select_match_video", "value"),
    prevent_initial_call=True,
)
