# Data-Rugby

## Fonctionnement général

L’objectif de ce projet est la mise en place d’un pipeline permettant de collecter, stocker, calculer des indicateurs et visualiser les résultats à partir de données collectées lors de matchs de rugby.

Lors des matchs, les joueurs portent des gps placés dans une brassière. Cela permet de connaître leurs positions et de calculer des indicateurs de distance, de vitesse et d'accélération.
Le schéma ci-dessous présente les diffèrentes parties du projet.

<ins> partie verte </ins> : un gps est attribué à chaque joueur, à la fin du match il faut brancher les gps à un ordinateur pour les recharger et récupérer les données.

<ins> partie jaune </ins> : les données brutes sont récupérables au format json sur la plateforme de la marque des gps. À partir des données de position obtenues à intervalles de temps réguliers, des scripts python permettent de nettoyer et filtrer les données puis de calculer les indicateurs qui nous intéressent. Ils sont ensuite sauvegardés dans une base de données en ligne.

<ins> partie bleue </ins> : les données sont utilisées pour une application de visualisation déployée en ligne. Le but est que les entraîneurs et les joueurs puissent accéder à la synthèse de leurs matchs le plus rapidement possible.

![image](https://github.com/user-attachments/assets/8e9c8b14-5cfd-40b2-ad9a-814ffeebac57)

## Défis

Ce projet est pour le moment un prototype. Les ressources allouées au stockage des données et au déploiement de l'application sont limitées. Malgré cela, l'objectif est de disposer d’un outil fonctionnel et de le tester dans des conditions réelles lors d’un tournoi de rugby à VII.

Le code permettant de synchroniser les données GPS et les flux vidéo a été développé, mais il n’est pour le moment pas implémentable au vu des ressources disponibles.

## Date d'avancement
8 juin 2025
