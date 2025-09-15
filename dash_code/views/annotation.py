import dash_mantine_components as dmc
from dash import html, dcc


def annot_live():
    return dmc.TabsPanel(
            children=[
                dmc.Center(dmc.Title("Annotation des matchs", order=1, mt="lg")),
                html.Br(),
                # Ligne 1
                dmc.Group(
                    children=[
                        dmc.Button("Début MT1", id="btn_debmt1", color="green"),
                        dmc.Button("Fin MT1", id="btn_finmt1", color="orange"),
                        dmc.Button("Touche", id="btn_touche", color="blue"),
                    ],
                    grow=True,
                    wrap="nowrap",
                ),
                html.Br(),
                # Ligne 2
                dmc.Group(
                    children=[
                        dmc.Button("Début MT2", id="btn_debmt2", color="green"),
                        dmc.Button("Fin MT2", id="btn_finmt2", color="orange"),
                        dmc.Button("Mêlée", id="btn_melee", color="blue"),
                    ],
                    grow=True,
                    wrap="nowrap",
                ),
                html.Br(),
                # Ligne 3
                dmc.Group(
                    children=[
                        dmc.Button("Supprimer", id="btn_suppr", color="red"),
                        dmc.Button("Temps fort", id="btn_highlight", color="blue"),
                        dmc.Button("Renvoi", id="btn_renvoi", color="blue"),
                    ],
                    grow=True,
                    wrap="nowrap",
                ),
                html.Br(),
                # Ligne 4
                dmc.Group(
                    children=[
                        dmc.TextInput(
                            placeholder="Match", id="input_namegame", size="sm"
                        ),
                        dmc.Button("Envoyer", id="btn_senddata", color="violet"),
                        dmc.Button("Essai", id="btn_essai", color="blue"),
                    ],
                    grow=True,
                    wrap="nowrap",
                ),
                html.Br(),
                html.Br(),
                # Ligne 5
                dmc.Text("Ajout ETS", size="xl", td="underline", c="red"),
                dmc.Group(
                    children=[
                        dmc.Button("Pénalité pour", id="btn_penalite_pour", color="indigo"),
                        dmc.Button("Pénalité contre", id="btn_penalite_contre", color="grape"),
                    ],
                    grow=True,
                    wrap="nowrap",
                ),
                html.Br(),
                # Ligne 6
                dmc.Group(
                    children=[
                        dmc.Button("Franchissement pour", id="btn_franchissement_pour", color="indigo"),
                        dmc.Button("Franchissement contre", id="btn_franchissement_contre", color="grape"),
                    ],
                    grow=True,
                    wrap="nowrap",
                ),
                html.Br(),
                # Afficher les notifications
                dmc.Alert(
                    id="alert_annot_add",
                    title="Annotation ajoutée",
                    color="green",
                    withCloseButton=True,
                    duration=1800,
                    hide=True,
                ),
                dmc.Alert(
                    id="alert_suppr_add",
                    title="Annotation supprimée",
                    color="red",
                    withCloseButton=True,
                    duration=1800,
                    hide=True,
                ),
                dmc.Alert(
                    id="alert_send_data",
                    title="Annotations enregistrées dans la base de données",
                    color="violet",
                    withCloseButton=True,
                    duration=1800,
                    hide=True,
                ),
                dcc.Store(id="store_annot", data=[]),
            ],
            value="tab_annot",
        )
