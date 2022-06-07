## Préparation des données matricielles pour la classification non-supervisée

Le script R *prep_rasters.R* requiert les données suivantes:

- les couches matricielles des variables de télédétection, incluses dans le dossier *Indices* avec plusieurs sous-dossiers;

- la carte matricielle d'utilisation du territoire (dans le dossier *utilisation_territoire_2018*) pour masquer les pixels aquatiques;

- le contour de la région d'étude (shapefile dans le dossier *site_etude*).

Le fichier *rast_files.csv* est une liste des 33 couches matricielles utilisées pour la classification à ce stade du projet, tel qu'expliqué dans le dernier rapport. (Ex.: les couches Sentinel 2 ne sont pas incluses en raison de la trop grande superficie où les données ont été rejetées.) Deux des couches (*asp_east* et *asp_north*) sont dérivées de la couche *aspect* dans la première partie du même script.

Au final le script produit les données nécessaires pour la classification:

- l'ensemble des couches matricielles alignées à une grille commune à résolution de 30 m (dans le dossier *aligned*);

- un masque *region_mask_30m.tif* qui contient la valeur "1" pour les pixels inclus dans la classification et la valeur "0" pour ceux exclus (car ils sont aquatiques, ont des données manquantes, où sont hors de la région d'étude). 

Le fait d'utiliser une région d'étude représentative, mais plus petite que le territoire complet de l'Abitibi vise notamment à accélérer les calculs (la région sélectionnée contient environ 20M de pixels inclus dans la classification, vs. 38M pour la région complète).

