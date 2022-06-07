## Pr�paration des donn�es matricielles pour la classification non-supervis�e

Le script R *prep_rasters.R* requiert les donn�es suivantes:

- les couches matricielles des variables de t�l�d�tection, incluses dans le dossier *Indices* avec plusieurs sous-dossiers;

- la carte matricielle d'utilisation du territoire (dans le dossier *utilisation_territoire_2018*) pour masquer les pixels aquatiques;

- le contour de la r�gion d'�tude (shapefile dans le dossier *site_etude*).

Le fichier *rast_files.csv* est une liste des 33 couches matricielles utilis�es pour la classification � ce stade du projet, tel qu'expliqu� dans le dernier rapport. (Ex.: les couches Sentinel 2 ne sont pas incluses en raison de la trop grande superficie o� les donn�es ont �t� rejet�es.) Deux des couches (*asp_east* et *asp_north*) sont d�riv�es de la couche *aspect* dans la premi�re partie du m�me script.

Au final le script produit les donn�es n�cessaires pour la classification:

- l'ensemble des couches matricielles align�es � une grille commune � r�solution de 30 m (dans le dossier *aligned*);

- un masque *region_mask_30m.tif* qui contient la valeur "1" pour les pixels inclus dans la classification et la valeur "0" pour ceux exclus (car ils sont aquatiques, ont des donn�es manquantes, o� sont hors de la r�gion d'�tude). 

Le fait d'utiliser une r�gion d'�tude repr�sentative, mais plus petite que le territoire complet de l'Abitibi vise notamment � acc�l�rer les calculs (la r�gion s�lectionn�e contient environ 20M de pixels inclus dans la classification, vs. 38M pour la r�gion compl�te).

