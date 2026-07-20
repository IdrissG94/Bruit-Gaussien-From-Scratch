# Génération et Validation de Bruit Gaussien sur Images (Méthode de Box-Muller)

## Introduction et description du projet :

Ce projet en Python permet de générer et d'appliquer un **bruit gaussien additif** sur une image couleur ($RGB$) en utilisant la **méthode de Box-Muller**. Il comprend également un outil de validation statistique permettant de vérifier la conformité du bruit généré par rapport à la loi normale théorique $\mathcal{N}(0, \sigma^2)$.

## Fonctionnalités

* **Algorithme de Box-Muller** : Transformation de variables aléatoires uniformes $\mathcal{U}(0, 1)$ en variables normales centrées réductrices ou ajustées avec un écart-type $\sigma$.
* **Génération de Bruit sur Image RGB** : Adaptation dynamique de la matrice de bruit à la taille $(H, W, C)$ de l'image.
* **Validation Statistique** : Affichage de l'histogramme empirique du bruit généré superposé à la densité de probabilité théorique $\mathcal{N}(0, \sigma^2)$.
* **Bruitage & Normalisation** : Ajout du bruit à l'image, écrêtage (`clip`) dans l'intervalle $[0, 255]$ et sauvegarde du résultat.
* **Boucle Interactive** : Test dynamique de plusieurs valeurs de $\sigma$ sur une même image.

## Projet :

# Détails Mathématiques & Algorithmiques
Méthode de Box-Muller
Si $U_1, U_2 \sim \mathcal{U}(0, 1)$ sont deux variables aléatoires indépendantes uniformes, alors les variables $Z_0$ et $Z_1$ définies par :  
$$Z_0 = \sigma \sqrt{-2 \ln(U_1)} \cos(2\pi U_2)$$  
$$Z_1 = \sigma \sqrt{-2 \ln(U_1)} \sin(2\pi U_2)$$  
suivent de manière indépendante une loi normale $\mathcal{N}(0, \sigma^2)$.
