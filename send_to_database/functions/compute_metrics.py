import numpy as np
import pandas as pd
from pyproj import Proj
from scipy.signal import medfilt
from sklearn.cluster import DBSCAN

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

# Interpoler les données manquantes
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

# Calculer distances parcourues en mètre
def compute_distance(x_utm, y_utm):
    """
    Calculer distance entre les mesures GPS
    in: arrays contenant coordonnées (x;y) en utm
    out: array contenant les distances entre deux mesures GPS
    """
    diff_x = np.diff(x_utm)
    diff_y = np.diff(y_utm)
    dist = np.sqrt(diff_x**2 + diff_y**2)
    return dist

# Calculer vitesse et accélération
def compute_speed(dist, time):
    """
    Calculer vitesse et accélération entre les mesures GPS
    in: array contenant les distances entre deux mesures GPS, fréquence GPS en Hz
    out: array contenant les vitesses et accélération entre deux mesures GPS
    """
    # Intervalle de temps
    time_interval = np.diff(time)
    # Calcul vitesse en m/s
    speed = dist / time_interval
    # Acceleration en m/s²
    accel = np.diff(speed) / time_interval[1:]
    return speed, accel

# Filtrer les données gps incohérentes
def clean_outliers(speed, accel, time):
    """
    Supprimer les points gps incohérents - Implementation de la méthode Miguens
    in: arrays contenant les vitesses, les accélérations et les temps
    out: arrays contenant les vitesses, les accélérations et les temps sans les points incohérents
    note: basé sur les articles https://doi.org/10.1186/s40798-023-00672-7 et https://doi.org/10.1080/02640414.2021.1993656
    """
    # Filtrer vitesse et accélération
    speed = medfilt(speed, kernel_size=9)
    accel = medfilt(accel, kernel_size=9)
    # Valeurs théoriques
    x1, y1 = 8.547 + 3 * 0.51, 0 #vitesse
    x2, y2 = 0, 5.629 + 3 * 0.26 #accélération
    # Calculer équation droite vitesse accélération
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    array_filter = a * speed + b
    # Filtrer les arrays vitesse et accélération
    speed_clean = speed[1:][array_filter[1:] > accel]
    accel_clean = accel[array_filter[1:] > accel]
    time_clean = time[2:][array_filter[1:] > accel]
    # Appliquer clustering dbscan pour supprimer les points isolés
    X = np.column_stack((speed_clean, accel_clean))
    db = DBSCAN(eps=0.2, min_samples=1).fit(X)
    unique, counts = np.unique(db.labels_, return_counts=True)
    # Identifier les clusters avec moins de 5 points 
    isolated_clusters = unique[counts < 5]
    # Récupérer les temps associés à de bonnes valeurs
    time_clean2 = time_clean[~np.isin(db.labels_, isolated_clusters)]
    speed_clean2 = speed_clean[~np.isin(db.labels_, isolated_clusters)]
    accel_clean2 = accel_clean[~np.isin(db.labels_, isolated_clusters)]
    return time_clean2, speed_clean2, accel_clean2

# Calculer distances parcourues par zone de vitesse
def compute_speed_zone(array, max_min_speed, step_speed):
    """
    Calculer distance parcourue par zone de vitesse
    in: array contenant les métriques, zone de vitesse et step
    out: zone de vitesse
    """
    zone_vitesse = []
    for i in range(max_min_speed[0], max_min_speed[1], step_speed):
        mask = (array[:, 2].astype(float) * 3.6 >= i) & (array[:, 2].astype(float) * 3.6 <= i + step_speed)
        # Distance parcourue
        distance_zone_vitesse = np.sum(array[mask, 1].astype(float))
        # Ajouter au dictionnaire
        zone_vitesse.append(distance_zone_vitesse)
    return zone_vitesse

# Compter le nombre d'accélération
def count_nb_accel(array_accel, array_time, threshold_speed, threshold_time):
    """
    Compter le nombre d'accélération au-delà d'un seuil
    in: array accélération et temps, se
    out: nombre d'accélération
    """
    indices = np.where(array_accel > threshold_speed)[0]
    data = array_time[indices]
    # Parcourir les temps et sélectionner si écart suffisant
    lst_complete, lst_temp = [], []
    for i in range(1, len(data)):
        if data[i] - data[i-1] < threshold_time:
            lst_temp.append(data[i-1])
        else:
            lst_complete.append(lst_temp)
            lst_temp = []
    # Filtrer la liste
    lst_complete = [l for l in lst_complete if l and len(l) > 5]
    # Compter nombre d'accélération
    nb_accel = len(lst_complete)
    return nb_accel

# Créer une fonction unique
def compute_all(lat, lon, time, zone=18):
    """
    Appliquer l'ensemble des fonctions de calcul
    in: array latitude, array longitude, zone utm
    out: ensemble des indicateurs à envoyer dans la base de données
    """
    # Convertir en utm
    x_utm, y_utm = convert_utm(lat, lon, zone)
    # Interpoler valeurs manquantes
    x_interp, y_interp, time = manage_missing_data(x_utm, y_utm, time)
    # Calculer la distance
    dist = compute_distance(x_interp, y_interp)
    # Calculer la vitesse et l'accélération
    speed, accel = compute_speed(dist, time)
    # Retirer les outliers
    time_clean, speed_clean, accel_clean = clean_outliers(speed, accel, time)
    # Recalculer distance
    distance_clean = np.diff(time_clean) * speed_clean[1:]
    distance_clean = np.insert(distance_clean, 0, 0)
    # Mettre sous la forme d'un array
    bd = np.column_stack((time_clean, distance_clean, speed_clean, accel_clean))
    # Calculer zone de vitesse
    lst_dist_speed = compute_speed_zone(bd, (0, 35), 5)
    # Vitesse maximale - 100 observations
    sorted_speed = bd[bd[:, 2].argsort()[::-1]]
    lst_speed = list(sorted_speed[:100, 2])
    lst_speed_time = list(sorted_speed[:100, 0])
    # Accélération maximale - 100 observations
    sorted_accel = bd[bd[:, 3].argsort()[::-1]]
    lst_accel = list(sorted_accel[:100, 3])
    lst_accel_time = list(sorted_accel[:100, 0])
    #Nombre d'accélération
    nb_accel = count_nb_accel(accel_clean, time_clean, 3, 8)
    return lst_dist_speed, lst_speed, lst_speed_time, lst_accel, lst_accel_time, nb_accel