import argparse
import gzip
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyproj import Proj

# Définir les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-file", "--file", required=True, type=str)
ap.add_argument("-start", "--start", required=False, type=float)
ap.add_argument("-end", "--end", required=False, type=float)
ap.add_argument("-mode", "--mode", required=False, type=str)
args = ap.parse_args()
file, start, end, mode = args.file, args.start, args.end, args.mode

# Récupérer les données
def get_data(source, debut, fin):
    """
    Lire le fichier contenant les données brutes au format json 
    in: chemin du fichier contenant les données, time stamp début et time stamp fin
    out: date, nom et 3 arrays contenant latitude, longitude, temps
    """
    # Ouvrir le fichier
    data = gzip.open(source, "rb").read()
    data = json.loads(data)
    debut, fin = debut - 14400, fin - 14400
    # Récupérer date et nom
    day = data["date"]
    user = data["user"]["name"]
    # Récupérer latitude, longitude et temps
    lst_time, lst_lat, lst_lon = [], [], []
    for i in range(len(data["gpss"])):
        if debut <= data["gpss"][i]["stamp"] <= fin:
            lst_time.append(data["gpss"][i]["stamp"])
            lst_lat.append(data["gpss"][i]["lat"])
            lst_lon.append(data["gpss"][i]["lon"])
    # Convertir en array numpy
    stamp, lat, lon = np.array(lst_time), np.array(lst_lat), np.array(lst_lon)
    return day, user, stamp, lat, lon

# Gérer les données manquantes
def manage_missing_data(x_utm, y_utm, time):
    """
    Gérer les données manquantes en les interpolant 
    in: arrays contenant coordonnées (x;y) en utm, array temps
    out: arrays contenant coordonnées (x;y) en utm, array temps sans valeurs manquantes
    """
    # Trouver séquences sans données
    missing_value = np.isnan(x_utm)
    # Identifier la première séquence manquantes
    cpt = 0
    while missing_value[cpt] != 0:
        cpt += 1
    # Retirer la première séquence
    x_utm, y_utm= x_utm[cpt:], y_utm[cpt:]
    time = time[cpt:]
    # Interpolation linéaire des valeurs manquantes
    x, y = pd.Series(x_utm), pd.Series(y_utm)
    x_interp, y_interp = x.interpolate().values, y.interpolate().values
    return x_interp, y_interp, time

# Convertir en utm
def convert_utm(lat, lon, zone=18):
    """
    Convertir les données latitude et longitude en utm
    in: arrays contenant latitude, longitude et zone utm
    out: arrays contenant coordonnées (x;y) en utm
    """
    pp = Proj(proj="utm", zone=zone, ellps="WGS84", preserve_units=False)
    x_utm, y_utm = pp(lon, lat)
    return x_utm, y_utm

# Convertir coordonnées dans repère terrain
def transpose_data(x_utm, y_utm, coord_field, zone=18):
    """
    Transposer les coordonnées utm dans un repère du terrain
    in: arrays contenant coordonnées (x;y), array contenant les coordonnées terrain
    out: conversion des arrays dans le repère du terrain
    """
    # Convertir coord_field en UTM
    pp = Proj(proj="utm", zone=zone, ellps="WGS84", preserve_units=False)
    x_coord_utm, y_coord_utm = pp(coord_field[:, 1], coord_field[:, 0])
    # Calcul angle de rotation
    hypothenuse = np.sqrt((x_coord_utm[2] - x_coord_utm[1])**2 + (y_coord_utm[2] - y_coord_utm[1])**2)
    oppose = np.sqrt((x_coord_utm[2] - x_coord_utm[2])**2 + (y_coord_utm[2] - y_coord_utm[1])**2)
    teta = np.arcsin(oppose / hypothenuse)
    # Translation
    x_repere, y_repere = x_coord_utm - x_coord_utm[1], y_coord_utm - y_coord_utm[1]
    x_trans, y_trans = x_utm - x_coord_utm[1], y_utm - y_coord_utm[1]

    # Appliquer la rotation
    x_repere_rot = x_repere * np.cos(teta) - y_repere * np.sin(teta)
    y_repere_rot = x_repere * np.sin(teta) + y_repere * np.cos(teta)
    x = x_trans * np.cos(teta) - y_trans * np.sin(teta)
    y = x_trans * np.sin(teta) + y_trans * np.cos(teta)
    coord = np.array([x_repere_rot, y_repere_rot]).T
    return x, y, coord

# Coordonnées du terrain
"""
0#--------------------#1
 |                    |
 |                    |
 |                    |
 |                    |
2#--------------------#
"""

coords_terrain = np.array([[45.51821001690672, -73.67134118460669],
                           [45.51717113817702, -73.67205015629314],
                           [45.516943637696265, -73.6713536707345]])

# Appeler les fonctions
date, player, time, latitude, longitude = get_data(file, start, end)
x_convert, y_convert = convert_utm(latitude, longitude, zone=18)
x_convert, y_convert, time = manage_missing_data(x_convert, y_convert, time)
x_plot, y_plot, repere = transpose_data(x_convert, y_convert, coords_terrain, zone=18)


def viz_classique():
    #graphique simple
    plt.scatter(x_plot, y_plot, alpha=0.1)
    plt.scatter(*A, color="red")
    plt.scatter(*B, color="green")
    plt.scatter(*C, color="blue")
    plt.scatter(*D, color="orange")
    plt.xlim(repere[1, 0]-10, repere[2, 0]+10)
    plt.ylim(repere[1, 1]-10, repere[0, 1]+10)
    plt.axis("equal")
    plt.title(player)
    plt.show()

def viz_heatmap():
    #visualisation heatmap
    counts, xedges, yedges = np.histogram2d(x_plot, y_plot, bins=30)
    z_min, z_max = -np.abs(counts).max(), np.abs(counts).max()

    c = plt.pcolormesh(xedges, yedges, counts.T, cmap="RdBu_r", vmin=z_min, vmax=z_max)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.title(player)
    plt.show()



#calcul du point pour fermer le rectangle
A = repere[0]
A[0] = 0 #correctif 
B = repere[1]
C = repere[2]
D = C - (B - A)
milieu_gauche = (A + B) / 2
milieu_droite = (D + C) / 2

#tracer lignes terrain
plt.plot([C[0], B[0]], [C[1], B[1]], color="k")      
plt.plot([B[0], A[0]], [B[1], A[1]], color="k")    
plt.plot([A[0], D[0]], [A[1], D[1]], color="k")     
plt.plot([D[0], C[0]], [D[1], C[1]], color="k")   
#tracer la ligne horizontale centrale
plt.plot([milieu_gauche[0], milieu_droite[0]], [milieu_gauche[1], milieu_droite[1]], color="k")
#plt.plot([milieu_gauche[0], milieu_droite[0]], [milieu_gauche[1]+10, milieu_droite[1]+10], color="k", linestyle="--")

if mode == "classique":
    viz_classique()
elif mode == "heatmap":
    viz_heatmap()










"""

"""