## Classification hiérarchique en deux étapes

La classification comme telle utilise l'algorithme *AgglomerativeClustering* du package scikit-learn dans Python. Nous utilisons ce package (plutôt que les algorithmes correspondant dans R, par exemple) car il permet une classification basée sur la connectivité spatiale, que nous utilisons à la première étape (définition de "patches").

Les différents scripts sont numérotés dans l'ordre d'exécution.

*1-create_grid.py*

Ce script requiert les données produites par le script *prep_rasters.R* (dossier *prep-donnees*). Son rôle principal est de créer le graphe de connectivité entre les pixels non-masqués de la région d'étude, qui sera utilisé à la première étape de la classification. 

Notons que puisque l'algorithme utilisé demande que tous les pixels soient connectés pour la classification, le script crée à cette étape un nouveau masque qui exclut des groupes de pixels non-connectés à la composante connectée principale du graphe. En particulier, cela exclut les îles de la classification, car elles sont séparées du graphe principal par des pixels aquatiques masqués.

Le script effectue aussi la normalisation des couches matricielles (i.e. convertir les valeurs numériques en nombre d'écarts-types en-dessous ou au-dessus de la moyenne) qui est nécessaire pour la classification non-supervisée. 

Il produit à la fin trois fichiers binaires de format *pickle*, soit la matrice des données normalisées *region_mat_norm* (dimensions: nombre de pixels x nombre de variables), le graphe de connectivité *region_graph* et le masque final *region_mask_connect* indiquant les pixels retenus pour la classification.


*2-region_clust_choix_ncl.py* et *3-region_clust_ncl_fixe.py*

Ces scripts effectuent la première étape de la classification, un regroupement hiérarchique des pixels avec le critère de Ward en tenant compte de la connectivité spatiale. À chaque niveau de l'arbre, cet algorithme regroupe donc les pixels pour produire des groupes connectés (i.e. des "patches") avec comme objectif de maintenir les groupes les plus homogènes possibles et les plus différents entre eux possibles; autrement dit, on segmente la région en patches relativement homogènes. 

Le script 2 effectue le regroupement pour différents nombres de groupes afin de déterminer des nombres de groupes optimaux. Ensuite, pour un nombre de groupes fixes, le script 3 produit des fichiers binaires en sortie: (1) numéros de patches associés à chaque pixel et (2) nouvelle matrice composée des moyennes de chaque variable au niveau des patches, qui sert d'entrée à la deuxième étape de la classification.

Le premier regroupement (script 2) est l'étape la plus exigeante en terme de ressources de calcul: avec 20 millions de pixels à l'entrée, la classification requiert environ 50 heures de calcul et 42 Go de mémoire vive. La mémoire vive nécessaire augmente linéairement avec le nombre de pixels, mais le temps de calcul augmente de façon environ quadratique. L'utilisation de la cache (arguments *compute_full_tree* et *memory* dans la fonction Python *AgglomerativeClustering*) permet de sauvegarder l'arbre de classification sur le disque, donc après la première exécution, la répétition du regroupement pour différents nombres de groupes est très rapide en autant que les données à l'entrée sont les mêmes.


*cluster_eval.R*

Ce script R accessoire est utilisé pour explorer comment la variance intra-groupe dépend du nombre de groupes et aide donc à choisir des nombres de groupes "optimaux", dans le sens d'un compromis entre la simplicité (moins de groupes) et l'homogénéité (groupes plus homogènes).


*4-patch_clust_choix_ncl* et *5-patch_clust_ncl_fixe*

Ce script effectue la deuxième étape de la classification, où les patches sont regroupées de façon globale (sans critère spatial) en fonction de la similitude des variables d'entrée (toujours selon le critère de Ward). Comme pour l'étape précédente, il y a deux scripts: le script 4 pour essayer différents nombres de groupes et calculer la dispersion intra- et inter-groupe, puis le script 5 pour choisir des nombres de groupes fixes et produire une liste des numéros de groupes associés à chaque patch.


*4b-patch_clust_choix_ncl* et *5b-patch_clust_ncl_fixe*

Lorsque le nombre de patches est grand (> 100 000, et peut-être avant), l'algorithme utilisé jusqu'à maintenant (*AgglomerativeClustering* dans Python) demande trop de ressources, donc on utilise l'algorithme plus rapide *Birch* pour effectuer un premier regroupement des patches, avant d'appliquer *AgglomerativeClustering* aux groupes produits par Birch. Ces deux scripts sont donc équivalents aux scripts 4 et 5 avec cette étape supplémentaire.