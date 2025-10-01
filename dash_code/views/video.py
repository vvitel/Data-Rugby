import dash_mantine_components as dmc
import dash_player
from dash import html, dcc

def gps_video(dic_date, dic_match, dic_joueur):
    return dmc.TabsPanel(
        children=[
            html.Br(),
            dmc.Grid(
                [
                    # Création des sélecteurs
                    dmc.GridCol(
                        children=[
                            dmc.Badge(
                                "Choisir match", size="lg", radius="lg", color="blue"
                            ),
                            dmc.Select(
                                label="Date",
                                id="select_date_video",
                                data=dic_date,
                                searchable=True,
                                clearable=True,
                                w="100%",
                            ),
                            dmc.Select(
                                label="Match",
                                id="select_match_video",
                                data=dic_match,
                                searchable=True,
                                clearable=True,
                                w="100%",
                            ),
                            html.Br(),
                            dmc.Badge(
                                "Choisir joueur", size="lg", radius="lg", color="violet"
                            ),
                            dmc.Select(
                                label="Joueur",
                                id="select_joueur_video",
                                data=dic_joueur,
                                searchable=True,
                                clearable=True,
                                w="100%",
                            ),
                            html.Br(),
                            dmc.Badge(
                                "Choisir métrique",
                                size="lg",
                                radius="lg",
                                color="grape",
                            ),
                            dmc.Select(
                                label="Métrique",
                                id="select_metrique_video",
                                data=[
                                    {"value": "vitesse", "label": "vitesse max."},
                                    {"value": "accel", "label": "acceleration max."},
                                ],
                                searchable=True,
                                clearable=True,
                                w="100%",
                            ),
                            html.Br(),
                            dmc.Badge(
                                "Choisir action", size="lg", radius="lg", color="pink"
                            ),
                            dmc.Select(
                                label="Action",
                                id="select_action_video",
                                data=[
                                    {"value": "essai", "label": "essai"},
                                    {"value": "mêlée", "label": "mêlée"},
                                    {"value": "touche", "label": "touche"},
                                ],
                                searchable=True,
                                clearable=True,
                                w="100%",
                            ),
                        ],
                        span=2,
                    ),
                    # Affichage de la vidéo et dessin dessus
                    dmc.GridCol(
                        children=[
                            dmc.Center(
                                dmc.Title("Visualisation des vidéos", order=1, mt="lg")
                            ),
                            html.Br(),
                            dmc.Center(
                                html.Div(
                                    [
                                        dash_player.DashPlayer(
                                            id="player_video",
                                            url="",
                                            controls=True,
                                            playing=True,
                                            seekTo=0,
                                            style={
                                                "display": "none",
                                                "width": "100%",
                                                "height": "300px",
                                            },
                                        ),
                                        html.Canvas(
                                            id="canvas",
                                            style={
                                                "position": "absolute",
                                                "top": 0,
                                                "left": 0,
                                                "width": "100%",
                                                "height": "315px",
                                                "cursor": "crosshair",
                                                "zIndex": 1,
                                            },
                                        ),
                                    ],
                                    style={"position": "relative"},
                                )
                            ),
                            html.Br(),
                            # Slider pour sélectionner les temps forts
                            dmc.Slider(
                                id="slider_action",
                                restrictToMarks=True,
                                value=0,
                                marks=[{"value": 0}],
                                style={"display": "none"},
                                styles={"markLabel": {"display": "none"}},
                            ),
                            # Mettre à jour le graphique en fonction de la vidéo
                            html.Br(),
                            # Stocker positions des joueurs
                            dcc.Store(id="store_coordinates"),
                            # Stocker la première frame de la requête,
                            dcc.Store(id="start_request", data=0),
                            # Stocker un booléen pour déclencher la requête pour avoir le positions
                            dcc.Store(id="trigger_request", data=1),
                            # Sorties inutiles mais utiles pour clientside_callback
                            dcc.Store(id="store_inutile_utile"),
                            # Affichage graphique avec les positions
                            dmc.Center(
                                dcc.Graph(
                                    id="map_chart",
                                    figure={},
                                    style={"display": "none"}
                                )
                            ),
                        ],
                        span=10,
                    ),
                ]
            ),
        ],
        value="tab_video",
    )
