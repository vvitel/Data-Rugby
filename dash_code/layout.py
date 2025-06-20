import dash_mantine_components as dmc
import dash_player
from dash import html

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
                    dmc.TabsPanel(
                        children=[
                            html.Br(),
                            dmc.Grid(
                                [
                                    # Création des sélecteurs
                                    dmc.GridCol(
                                        children=[
                                            dmc.Badge("Choisir match", size="lg", radius="lg", color="blue"),
                                            dmc.Select(label="Date", id="select_date", data=dic_date, searchable=True, clearable=True, w="100%"),
                                            dmc.Select(label="Match", id="select_match", data=dic_match, searchable=True, clearable=True, w="100%"),
                                            html.Br(),
                                            dmc.Badge("Choisir joueur", size="lg", radius="lg", color="violet"),
                                            dmc.Select(label="Joueur", id="select_joueur", data=dic_joueur, searchable=True, clearable=True, w="100%")
                                        ],
                                        span=2
                                    ),
                                    # Visualisations graphiques
                                    dmc.GridCol(
                                        children=[
                                            dmc.Center(dmc.Title("Visualisation des données GPS", order=1, mt="lg")),
                                            # Graphique en bar pour les distances parcourues
                                            dmc.Title("Distances parcourues par zone de vitesse", id="title_barplot", order=3, mt="lg", style={"display": "none"}),
                                            dmc.BarChart(id="barplot_dist", h=0, dataKey="", data=[], type="stacked", orientation="vertical", series=[], style={"display": "none"}),
                                            html.Br(),
                                            dmc.Group(children=[dmc.Title("Vitesse et accélération maximale", id="title_scatterspeedaccel", order=3, mt="lg", style={"display": "none"}),
                                                                dmc.Title("Nombre d'accélération", id="title_nbaccel", order=3, mt="lg", style={"display": "none"})],
                                                      grow=True, gap="xl", justify="space-around"),
                                            dmc.Group(children=[dmc.ScatterChart(id="scatter_vitesse_accel", h=300, data=[], dataKey={"x": "vitesse", "y": "acceleration"}, xAxisLabel="Vitesse (km/h)", yAxisLabel="Accélération (m/s)", xAxisProps={"domain": [17, 30]}, yAxisProps={"domain": [2, 7]}, withLegend=True, legendProps={"verticalAlign": "bottom", "height": 10}, style={"display": "none"}),
                                                                dmc.BarChart(id="barplot_accel", h=400, dataKey="", data=[], type="stacked", orientation="vertical", series=[], withBarValueLabel=True, style={"display": "none"})],
                                                      grow=True),
                                            html.Br(),
                                            # Donut pour repésenter note des joueuses
                                            dmc.Title("Comparaison niveau international", id="title_donut", order=3, mt="lg", style={"display": "none"}),
                                            html.Br(),
                                            dmc.Group(children=[dmc.DonutChart(id="donut_vmax", data=[], startAngle=180, endAngle=0, chartLabel="vitesse max.", style={"display": "none"}),
                                                                dmc.DonutChart(id="donut_amax", data=[], startAngle=180, endAngle=0, chartLabel="accélération max.", style={"display": "none"}),],
                                                      grow=False)],
                                        span=10
                                    ),
                                ]
                            ),
                        ],
                        value="tab_gps"
                    ),
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
                                            dmc.Select(label="Action", id="select_action_video", data=[{"value": "essai", "label": "essai"}, {"value": "mêlée", "label": "mêlée"}, {"value": "touche", "label": "touche"}], searchable=True, clearable=True, w="100%"),

                                        ],
                                        span=2
                                    ),
                                    # Affichage de la vidéo
                                    dmc.GridCol(
                                        children=[
                                            dmc.Center(dmc.Title("Visualisation des vidéos", order=1, mt="lg")),
                                            html.Br(),
                                            dmc.Center(html.Div([dash_player.DashPlayer(id="yt_video", url="", controls=True, seekTo=0, style={"display": "none", "width": "100%", "height": "300px"})])),
                                            html.Br(),
                                            dmc.Slider(id="slider_action", restrictToMarks=True, value=0, marks=[{"value": 0}], style={"display": "none"})
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
                            dmc.Group(children=[dmc.Button("Début MT1", color="green"),
                                                dmc.Button("Fin MT1", color="red"),
                                                dmc.Button("Touche", color="blue")],
                                      grow=True, wrap="nowrap"),
                            html.Br(),
                            # Ligne 2
                            dmc.Group(children=[dmc.Button("Début MT2", color="green"),
                                                dmc.Button("Fin MT2", color="red"),
                                                dmc.Button("Mêlée", color="blue")],
                                      grow=True, wrap="nowrap"),
                            html.Br(),
                            # Ligne 3
                            dmc.Group(children=[dmc.TextInput(placeholder="Match", size="sm"),
                                                dmc.Button("Envoyer", color="violet"),
                                                dmc.Button("Essai", color="blue")],
                                      grow=True, wrap="nowrap")],
                            
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

