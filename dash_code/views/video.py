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
                                            id="yt_video",
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
                            dcc.Store(id="store_write_js"),
                            html.Br(),
                            dmc.Slider(
                                id="slider_action",
                                restrictToMarks=True,
                                value=0,
                                marks=[{"value": 0}],
                                style={"display": "none"},
                                styles={"markLabel": {"display": "none"}},
                            )
                        ],
                        span=10,
                    ),
                ]
            ),
        ],
        value="tab_video",
    )
