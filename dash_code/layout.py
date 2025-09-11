import dash_mantine_components as dmc
import dash_player
from dash import html, dcc
from dash_code.views.gps import gps_stat


def create_layout(dic_date, dic_match, dic_joueur):
    return dmc.MantineProvider(
        forceColorScheme="dark",
        children=[
            dmc.Tabs(
                [
                    # Création des panneaux
                    dmc.TabsList(
                        [
                            dmc.TabsTab("📈", value="tab_gps", style={"fontSize": "30px"}),
                            dmc.TabsTab("📽️", value="tab_video", style={"fontSize": "30px"}),
                            dmc.TabsTab("🟦", value="tab_annot", style={"fontSize": "30px"})
                        ]
                    ),
                    # Panneau pour visualisation des données GPS
                    gps_stat(dic_date, dic_match, dic_joueur), 
                    # Panneau pour visualisation des données vidéo
                    dmc.TabsPanel(
                        children=[
                            html.Br(),
                            dmc.Grid(
                                [
                                    # Création des sélecteurs
                                    dmc.GridCol(
                                        children=[
                                            dmc.Badge("Choisir match", size="lg", radius="lg", color="blue"),
                                            dmc.Select(label="Date", id="select_date_video", data=dic_date, searchable=True, clearable=True, w="100%"),
                                            dmc.Select(label="Match", id="select_match_video", data=dic_match, searchable=True, clearable=True, w="100%"),
                                            html.Br(),
                                            dmc.Badge("Choisir joueur", size="lg", radius="lg", color="violet"),
                                            dmc.Select(label="Joueur", id="select_joueur_video", data=dic_joueur, searchable=True, clearable=True, w="100%"),
                                            html.Br(),
                                            dmc.Badge("Choisir métrique", size="lg", radius="lg", color="grape"),
                                            dmc.Select(label="Métrique", id="select_metrique_video", data=[{"value": "vitesse", "label": "vitesse max."}, {"value": "accel", "label": "acceleration max."}], searchable=True, clearable=True, w="100%"),
                                            html.Br(),
                                            dmc.Badge("Choisir action", size="lg", radius="lg", color="pink"),
                                            dmc.Select(label="Action", id="select_action_video", data=[{"value": "essai", "label": "essai"}, {"value": "mêlée", "label": "mêlée"}, {"value": "touche", "label": "touche"}, {"value": "engagement", "label": "engagement"}], searchable=True, clearable=True, w="100%"),

                                        ],
                                        span=2
                                    ),
                                    # Affichage de la vidéo et dessin dessus
                                    dmc.GridCol(
                                        children=[
                                            dmc.Center(dmc.Title("Visualisation des vidéos", order=1, mt="lg")),
                                            html.Br(),
                                            dmc.Center(
                                                html.Div([
                                                    dash_player.DashPlayer(id="yt_video", url="", controls=True, playing=True, seekTo=0, style={"display": "none", "width": "100%", "height": "300px"}),
                                                    html.Canvas(id="canvas", style={"position": "absolute", "top": 0, "left": 0, "width": "100%", "height": "315px", "cursor": "crosshair", "zIndex": 1})],
                                                style={"position": "relative"})),
                                            dcc.Store(id="store_inutile"),
                                            html.Br(),
                                            dmc.Slider(id="slider_action", restrictToMarks=True, value=0, marks=[{"value": 0}], style={"display": "none"}, styles={"markLabel": {"display": "none"}})
                                            #{"markLabel": {"display": "none"}
                                        ],
                                        span=10
                                    )
                                ]
                            ),
                        ],
                        value="tab_video"
                    ),
                dmc.TabsPanel(
                        children=[
                            dmc.Center(dmc.Title("Annotation des matchs", order=1, mt="lg")),
                            html.Br(),
                            # Ligne 1
                            dmc.Group(children=[dmc.Button("Début MT1", id="btn_debmt1", color="green"),
                                                dmc.Button("Fin MT1", id="btn_finmt1", color="orange"),
                                                dmc.Button("Touche", id="btn_touche", color="blue")],
                                      grow=True, wrap="nowrap"),
                            html.Br(),
                            # Ligne 2
                            dmc.Group(children=[dmc.Button("Début MT2", id="btn_debmt2", color="green"),
                                                dmc.Button("Fin MT2", id="btn_finmt2", color="orange"),
                                                dmc.Button("Mêlée", id="btn_melee", color="blue")],
                                      grow=True, wrap="nowrap"),
                            html.Br(),
                            # Ligne 3
                            dmc.Group(children=[dmc.Button("Supprimer", id="btn_suppr", color="red"),
                                                dmc.Button("Temps fort", id="btn_highlight", color="blue"),
                                                dmc.Button("Renvoi", id="btn_renvoi", color="blue")],
                                      grow=True, wrap="nowrap"),
                            html.Br(),
                            # Ligne 4
                            dmc.Group(children=[dmc.TextInput(placeholder="Match", id="input_namegame", size="sm"),
                                                dmc.Button("Envoyer", id="btn_senddata", color="violet"),
                                                dmc.Button("Essai", id="btn_essai", color="blue")],
                                      grow=True, wrap="nowrap"),
                            html.Br(),
                            # Afficher les notifications
                            dmc.Alert(id="alert_annot_add", title="Annotation ajoutée", color="green", withCloseButton=True, duration=1800, hide=True),
                            dmc.Alert(id="alert_suppr_add", title="Annotation supprimée", color="red", withCloseButton=True, duration=1800, hide=True),
                            dmc.Alert(id="alert_send_data", title="Annotations enregistrées dans la base de données", color="violet", withCloseButton=True, duration=1800, hide=True),
                            dcc.Store(id="store_annot", data=[])],
                        value="tab_annot"
                    ),
                ],
                color="blue",
                orientation="horizontal",
                variant="default",
                value="tab_gps"
            )
        ]
    )
