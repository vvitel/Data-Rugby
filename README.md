# Data-Rugby

## Fonctionnement général

L’objectif de ce projet est la mise en place d’un pipeline permettant de collecter, stocker, calculer des indicateurs et visualiser les résultats à partir de données collectées lors de matchs de rugby.

Lors des matchs, les joueurs portent des gps placés dans une brassière. Cela permet de connaître leurs positions et de calculer des indicateurs de distance, de vitesse et d'accélération.
Le schéma ci-dessous présente les différentes parties du projet.

<ins> partie verte </ins> : un gps est attribué à chaque joueur, à la fin du match il faut brancher les gps à un ordinateur pour les recharger et récupérer les données.

<ins> partie jaune </ins> : les données brutes sont récupérables au format json sur la plateforme de la marque des gps. À partir des données de position obtenues à intervalles de temps réguliers, des scripts python permettent de nettoyer et filtrer les données puis de calculer les indicateurs qui nous intéressent. Ils sont ensuite sauvegardés dans une base de données en ligne.

<ins> partie bleue </ins> : les données sont utilisées pour une application de visualisation déployée en ligne. Le but est que les entraîneurs et les joueurs puissent accéder à la synthèse de leurs matchs le plus rapidement possible.

![image](https://github.com/user-attachments/assets/21b8483b-208b-46ae-88e5-f68585846401)


## Traiter et sauvegarder les données

Récupérer les fichiers contenant les données brutes et les placer dans un dossier `temp` à la racine du projet.

La commande ci-dessous permet de traiter les données brutes et de les sauvegarder dans la base de données MongoDB.


```bash
python -B .\send_data.py --game "RCV vs CAB" --competition "proD2" --coord_field "47.65228983174274, -2.760688837801974" --start 1756576949.5643039 --end 1756582791.3155258 --commentaire "J1 proD2"
```




## Défis

Ce projet est pour le moment un prototype. Les ressources allouées au stockage des données et au déploiement de l'application sont limitées. Malgré cela, l'objectif est de disposer d’un outil fonctionnel et de le tester dans des conditions réelles.

## Date d'avancement
1 septembre 2025
