import dash_mantine_components as dmc
from dash import html, dcc


def annot_live():
    return dmc.TabsPanel(
        value="tab_annot",
        children=[
            dmc.Carousel(
                children=[
                    # Carousel de la Gestion
                    dmc.CarouselSlide(
                        dmc.Stack(
                            children=[
                                dmc.Center(
                                    dmc.Title("Gestion du temps", order=1, mt="lg")
                                ),
                                dmc.Card(
                                    children=[
                                        dmc.Group(
                                            children=[
                                                dmc.Button("Début MT1", id="btn_debmt1", color="green"),
                                                dmc.Button("Fin MT1", id="btn_finmt1", color="orange"),
                                            ],
                                        grow=True,
                                        wrap="nowrap"
                                        ),
                                        dmc.Space(h="md"),
                                        dmc.Group(
                                            children=[
                                                dmc.Button("Début MT2", id="btn_debmt2", color="green"),
                                                dmc.Button("Fin MT2", id="btn_finmt2", color="orange"),
                                            ],
                                        grow=True,
                                        wrap="nowrap"
                                        ),
                                        dmc.Space(h="md"),
                                        dmc.Group(
                                            children=[
                                                dmc.TextInput(placeholder="Match", id="input_namegame", size="sm"),
                                                dmc.Button("Supprimer", id="btn_suppr", color="red")
                                            ],
                                        grow=True,
                                        wrap="nowrap"
                                        ),
                                        dmc.Space(h="md"),
                                        dmc.Center(dmc.Button("Sauvegarder", id="btn_senddata", color="violet", size="md"))
                                    ]
                                )
                            ]
                        )
                    ),
                    # Carousel de la Conquête
                    dmc.CarouselSlide(
                        dmc.Stack(
                            children=[
                                dmc.Center(
                                    dmc.Title("Conquête", order=1, mt="lg")
                                ),
                                dmc.Card(
                                    children=[
                                        dmc.Group(
                                            children=[
                                                dmc.Center(dmc.Text("Mêlée Offensive", size="lg")),
                                                dmc.Center(dmc.Text("Touche Offensive", size="lg")),
                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                        dmc.Group(
                                            children=[
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Gagnée", id="btn_scrum_o_won", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Perdue", id="btn_scrum_o_lose", variant="filled", color="red", fullWidth=True),
                                                        dmc.Button("Volée", id="btn_scrum_o_stolen", variant="filled", color="orange", fullWidth=True),
                                                    ]
                                                ),
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Gagnée", id="btn_lineout_o_won", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Perdue", id="btn_lineout_o_lose", variant="filled", color="red", fullWidth=True),
                                                        dmc.Button("Volée", id="btn_lineout_o_stolen", variant="filled", color="orange", fullWidth=True)
                                                    ]
                                                )
                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                        dmc.Group(
                                            children=[
                                                dmc.Center(dmc.Text("Mêlée Défensive", size="lg")),
                                                dmc.Center(dmc.Text("Touche Défensive", size="lg")),
                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                        dmc.Group(
                                            children=[
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Gagnée", id="btn_scrum_d_won", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Perdue", id="btn_scrum_d_lose", variant="filled", color="red", fullWidth=True),
                                                        dmc.Button("Volée", id="btn_scrum_d_stolen", variant="filled", color="orange", fullWidth=True)
                                                    ]
                                                ),
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Gagnée", id="btn_lineout_d_won", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Perdue", id="btn_lineout_d_lose", variant="filled", color="red", fullWidth=True),
                                                        dmc.Button("Volée", id="btn_lineout_d_stolen", variant="filled", color="orange", fullWidth=True)
                                                    ]
                                                )
                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                    ]
                                )
                            ]
                        )
                    ),
                    # Carousel des Scores
                    dmc.CarouselSlide(
                        dmc.Stack(
                            children=[
                                dmc.Center(
                                    dmc.Title("Score", order=1, mt="lg")
                                ),
                                dmc.Card(
                                    children=[
                                        dmc.Center(dmc.Text("ETS", size="xl", fw=700)),
                                        dmc.Group(
                                            children=[
                                                dmc.Button("Essai", id="btn_ets_try", variant="filled", color="violet", fullWidth=True),
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Transformé", id="btn_ets_conversion_success", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Non Transformé", id="btn_ets_conversion_fail", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                )
                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                        dmc.Space(h="md"),
                                        dmc.Group(
                                            children=[
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Pénalité réussie", id="btn_ets_penalty_success", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Pénalité ratée", id="btn_ets_penalty_fail", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                ),
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Drop réussi", id="btn_ets_drop_success", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Drop raté", id="btn_ets_drop_fail", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                )

                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                    ]
                                ),
                                dmc.Card(
                                    children=[
                                        dmc.Center(dmc.Text("ADVERSAIRE", size="xl", fw=700)),
                                        dmc.Group(
                                            children=[
                                                dmc.Button("Essai", id="btn_opponent_try", variant="filled", color="violet", fullWidth=True),
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Transformé", id="btn_opponent_conversion_success", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Non Transformé", id="btn_opponent_conversion_fail", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                )
                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                        dmc.Space(h="md"),
                                        dmc.Group(
                                            children=[
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Pénalité réussie", id="btn_opponent_penalty_success", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Pénalité ratée", id="btn_opponent_penalty_fail", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                ),
                                                dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Drop réussi", id="btn_opponent_drop_success", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Drop raté", id="btn_opponent_drop_fail", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                )

                                            ],
                                            grow=True,
                                            wrap="nowrap"
                                        ),
                                    ]
                                )
                            ]
                        )
                    ),
                    # Carousel du Jeu 
                    dmc.CarouselSlide(
                        dmc.Stack(
                            children=[
                                dmc.Center(
                                    dmc.Title("Dans le Jeu", order=1, mt="lg")
                                ),
                                dmc.Card(
                                    children=[
                                        dmc.Center(dmc.Text("Pénalité", size="lg")),
                                        dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Pour", id="btn_penalty_for", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Contre", id="btn_penalty_against", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                ),
                                        dmc.Center(dmc.Text("Turnover", size="lg")),
                                        dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Pour", id="btn_turnover_for", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Contre", id="btn_turnover_against", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                ),
                                        dmc.Center(dmc.Text("Bras Cassé", size="lg")),
                                        dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Pour", id="btn_freekick_for", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Contre", id="btn_freekick_against", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                ),
                                        dmc.Center(dmc.Text("Franchissement", size="lg")),
                                        dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Pour", id="btn_linebreak_for", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Contre", id="btn_linebreak_against", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                ),
                                        dmc.Center(dmc.Text("Jeu au Pied", size="lg")),
                                        dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Pour", id="btn_kick_for", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Contre", id="btn_kick_against", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                ),
                                        dmc.Center(dmc.Text("Plaquage", size="lg")),
                                        dmc.ButtonGroup(
                                                    children=[
                                                        dmc.Button("Réussi", id="btn_tackle_success", variant="filled", color="green", fullWidth=True),
                                                        dmc.Button("Raté", id="btn_tackle_fail", variant="filled", color="red", fullWidth=True),
                                                    ]
                                                )
                                    ]
                                ),
                                dmc.Card(
                                    id="card_penalty_precision",
                                    children=[
                                        dmc.Group(
                                            children=[
                                                dmc.Button("Ruck", id="btn_penalty_ruck", variant="filled", color="teal", fullWidth=True),
                                                dmc.Button("Mêlée", id="btn_penalty_scrum", variant="filled", color="cyan", fullWidth=True),
                                                dmc.Button("Touche", id="btn_penalty_lineout", variant="filled", color="blue", fullWidth=True),
                                                dmc.Button("Plaquage", id="btn_penalty_tackle", variant="filled", color="indigo", fullWidth=True),
                                                dmc.Button("Hors jeu", id="btn_penalty_offside", variant="filled", color="violet", fullWidth=True)
                                            ],
                                        grow=True,
                                        wrap="nowrap"
                                        )
                                    ],
                                    style={"display": "none"}
                                )
                            ]
                        )
                    ),
                ],
                id="carousel-simple",
                withControls=False,
                emblaOptions = {"loop": True}
            ),
            html.Br(),
            # Afficher les notifications
            dmc.Alert(id="alert_annot_add", title="Annotation ajoutée", color="green", withCloseButton=True, duration=1800, hide=True),
            dmc.Alert(id="alert_suppr_add", title="Annotation supprimée", color="red", withCloseButton=True, duration=1800, hide=True),
            dmc.Alert(id="alert_send_data", title="Annotations enregistrées dans la base de données", color="violet", withCloseButton=True, duration=1800, hide=True),
            dcc.Store(id="store_annot", data=[])
        ]
    )
