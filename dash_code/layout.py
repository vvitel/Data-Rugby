import dash_mantine_components as dmc
from dash_code.views.annotation import annot_live
from dash_code.views.gps import gps_stat
from dash_code.views.video import gps_video


def create_layout(dic_date, dic_match, dic_joueur):
    return dmc.MantineProvider(
        forceColorScheme="dark",
        children=[
            dmc.Tabs(
                [
                    # Création des panneaux
                    dmc.TabsList(
                        [
                            dmc.TabsTab(
                                "📈", value="tab_gps", style={"fontSize": "30px"}
                            ),
                            dmc.TabsTab(
                                "📽️", value="tab_video", style={"fontSize": "30px"}
                            ),
                            dmc.TabsTab(
                                "🟦", value="tab_annot", style={"fontSize": "30px"}
                            ),
                        ]
                    ),
                    # Panneau pour visualisation des données GPS
                    gps_stat(dic_date, dic_match, dic_joueur),
                    # Panneau pour visualisation des données vidéo
                    gps_video(dic_date, dic_match, dic_joueur),
                    # Boutons d'annotations en live
                    annot_live(),
                ],
                color="blue",
                orientation="horizontal",
                variant="default",
                value="tab_gps",
            )
        ],
    )
