import dash_mantine_components as dmc
from dash import html, dcc

def gps_stat(dic_date, dic_match, dic_joueur):
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
                                id="select_date",
                                data=dic_date,
                                searchable=True,
                                clearable=True,
                                w="100%",
                            ),
                            dmc.Select(
                                label="Match",
                                id="select_match",
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
                                id="select_joueur",
                                data=dic_joueur,
                                searchable=True,
                                clearable=True,
                                w="100%",
                            ),
                            html.Br(),
                            dmc.Button(
                                "Télécharger les données",
                                id="btn_download_data",
                                size="compact-lg",
                                w="100%",
                                color="indigo",
                            ),
                            dcc.Download(id="download_data"),
                        ],
                        span=2,
                    ),
                    # Visualisations graphiques
                    dmc.GridCol(
                        children=[
                            dmc.Center(
                                dmc.Title(
                                    "Visualisation des données GPS", order=1, mt="lg"
                                )
                            ),
                            # Graphique en bar pour les distances parcourues
                            dmc.Title(
                                "Distances parcourues par zone de vitesse",
                                id="title_barplot",
                                order=3,
                                mt="lg",
                                style={"display": "none"},
                            ),
                            dmc.BarChart(
                                id="barplot_dist",
                                h=0,
                                dataKey="",
                                data=[],
                                type="stacked",
                                orientation="vertical",
                                series=[],
                                style={"display": "none"},
                            ),
                            html.Br(),
                            # Titres et graphiques vmax et nombre d'accélérations
                            dmc.Group(
                                children=[
                                    dmc.Title(
                                        "Vitesse et accélération maximale",
                                        id="title_scatterspeedaccel",
                                        order=3,
                                        mt="lg",
                                        style={"display": "none"},
                                    ),
                                    dmc.Title(
                                        "Nombre de sprints",
                                        id="title_nbaccel",
                                        order=3,
                                        mt="lg",
                                        style={"display": "none"},
                                    ),
                                ],
                                grow=True,
                                gap="xl",
                                justify="space-around",
                            ),
                            dmc.Group(
                                children=[
                                    dmc.ScatterChart(
                                        id="scatter_vitesse_accel",
                                        h=300,
                                        data=[],
                                        dataKey={"x": "vitesse", "y": "acceleration"},
                                        xAxisLabel="Vitesse (km/h)",
                                        yAxisLabel="Accélération (m/s)",
                                        xAxisProps={"domain": [20, 35]},
                                        yAxisProps={"domain": [2, 7]},
                                        withLegend=True,
                                        legendProps={
                                            "verticalAlign": "bottom",
                                            "height": 10,
                                        },
                                        style={"display": "none"},
                                    ),
                                    dmc.BarChart(
                                        id="barplot_accel",
                                        h=400,
                                        dataKey="",
                                        data=[],
                                        type="stacked",
                                        orientation="vertical",
                                        series=[],
                                        withBarValueLabel=True,
                                        style={"display": "none"},
                                    ),
                                ],
                                grow=True,
                            ),
                            # Titre et graphique nombre d'impacts
                            dmc.Group(
                                children=[
                                    dmc.Title(
                                        "Nombre d'impacts",
                                        id="title_nbimpact",
                                        order=3,
                                        mt="lg",
                                        style={"display": "none"},
                                    ),
                                    dmc.Title(
                                        "",
                                        id="title_empty",
                                        order=3,
                                        mt="lg",
                                        style={"display": "block"},
                                    ),
                                ],
                                grow=True,
                                gap="xl",
                                justify="space-around",
                            ),
                            dmc.Group(
                                children=[
                                    dmc.BarChart(
                                        id="barplot_impact",
                                        h=400,
                                        dataKey="",
                                        data=[],
                                        type="stacked",
                                        orientation="vertical",
                                        series=[],
                                        withBarValueLabel=True,
                                        style={"display": "none"},
                                    ),
                                    dmc.ScatterChart(
                                        id="scatter_empty",
                                        h=300,
                                        data=[],
                                        dataKey={"x": "vitesse", "y": "acceleration"},
                                        xAxisLabel="Vitesse (km/h)",
                                        yAxisLabel="Accélération (m/s)",
                                        xAxisProps={"domain": [20, 35]},
                                        yAxisProps={"domain": [2, 7]},
                                        withLegend=True,
                                        legendProps={
                                            "verticalAlign": "bottom",
                                            "height": 10,
                                        },
                                        style={"display": "none"},
                                    ),
                                ],
                                grow=True,
                            ),
                            html.Br(),
                            # Donut pour repésenter note des joueuses
                            dmc.Title(
                                "Comparaison niveau international",
                                id="title_donut",
                                order=3,
                                mt="lg",
                                style={"display": "none"},
                            ),
                            html.Br(),
                            dmc.Group(
                                children=[
                                    dmc.DonutChart(
                                        id="donut_vmax",
                                        data=[],
                                        startAngle=180,
                                        endAngle=0,
                                        chartLabel="vitesse max.",
                                        style={"display": "none"},
                                    ),
                                    dmc.DonutChart(
                                        id="donut_amax",
                                        data=[],
                                        startAngle=180,
                                        endAngle=0,
                                        chartLabel="accélération max.",
                                        style={"display": "none"},
                                    ),
                                ],
                                grow=False,
                                gap="xl",
                            ),
                        ],
                        span=10,
                    ),
                ]
            ),
        ],
        value="tab_gps",
    )
