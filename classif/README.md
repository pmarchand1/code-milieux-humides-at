## Classification hi�rarchique en deux �tapes

La classification comme telle utilise l'algorithme *AgglomerativeClustering* du package scikit-learn dans Python. Nous utilisons ce package (plut�t que les algorithmes correspondant dans R, par exemple) car il permet une classification bas�e sur la connectivit� spatiale, que nous utilisons � la premi�re �tape (d�finition de "patches").

Les diff�rents scripts sont num�rot�s dans l'ordre d'ex�cution.

*1-create_grid.py*

Ce script requiert les donn�es produites par le script *prep_rasters.R* (dossier *prep-donnees*). Son r�le principal est de cr�er le graphe de connectivit� entre les pixels non-masqu�s de la r�gion d'�tude, qui sera utilis� � la premi�re �tape de la classification. 

Notons que puisque l'algorithme utilis� demande que tous les pixels soient connect�s pour la classification, le script cr�e � cette �tape un nouveau masque qui exclut des groupes de pixels non-connect�s � la composante connect�e principale du graphe. En particulier, cela exclut les �les de la classification, car elles sont s�par�es du graphe principal par des pixels aquatiques masqu�s.

Le script effectue aussi la normalisation des couches matricielles (i.e. convertir les valeurs num�riques en nombre d'�carts-types en-dessous ou au-dessus de la moyenne) qui est n�cessaire pour la classification non-supervis�e. 

Il produit � la fin trois fichiers binaires de format *pickle*, soit la matrice des donn�es normalis�es *region_mat_norm* (dimensions: nombre de pixels x nombre de variables), le graphe de connectivit� *region_graph* et le masque final *region_mask_connect* indiquant les pixels retenus pour la classification.


*2-region_clust_choix_ncl.py* et *3-region_clust_ncl_fixe.py*

Ces scripts effectuent la premi�re �tape de la classification, un regroupement hi�rarchique des pixels avec le crit�re de Ward en tenant compte de la connectivit� spatiale. � chaque niveau de l'arbre, cet algorithme regroupe donc les pixels pour produire des groupes connect�s (i.e. des "patches") avec comme objectif de maintenir les groupes les plus homog�nes possibles et les plus diff�rents entre eux possibles; autrement dit, on segmente la r�gion en patches relativement homog�nes. 

Le script 2 effectue le regroupement pour diff�rents nombres de groupes afin de d�terminer des nombres de groupes optimaux. Ensuite, pour un nombre de groupes fixes, le script 3 produit des fichiers binaires en sortie: (1) num�ros de patches associ�s � chaque pixel et (2) nouvelle matrice compos�e des moyennes de chaque variable au niveau des patches, qui sert d'entr�e � la deuxi�me �tape de la classification.

Le premier regroupement (script 2) est l'�tape la plus exigeante en terme de ressources de calcul: avec 20 millions de pixels � l'entr�e, la classification requiert environ 50 heures de calcul et 42 Go de m�moire vive. La m�moire vive n�cessaire augmente lin�airement avec le nombre de pixels, mais le temps de calcul augmente de fa�on environ quadratique. L'utilisation de la cache (arguments *compute_full_tree* et *memory* dans la fonction Python *AgglomerativeClustering*) permet de sauvegarder l'arbre de classification sur le disque, donc apr�s la premi�re ex�cution, la r�p�tition du regroupement pour diff�rents nombres de groupes est tr�s rapide en autant que les donn�es � l'entr�e sont les m�mes.


*cluster_eval.R*

Ce script R accessoire est utilis� pour explorer comment la variance intra-groupe d�pend du nombre de groupes et aide donc � choisir des nombres de groupes "optimaux", dans le sens d'un compromis entre la simplicit� (moins de groupes) et l'homog�n�it� (groupes plus homog�nes).


*4-patch_clust_choix_ncl* et *5-patch_clust_ncl_fixe*

Ce script effectue la deuxi�me �tape de la classification, o� les patches sont regroup�es de fa�on globale (sans crit�re spatial) en fonction de la similitude des variables d'entr�e (toujours selon le crit�re de Ward). Comme pour l'�tape pr�c�dente, il y a deux scripts: le script 4 pour essayer diff�rents nombres de groupes et calculer la dispersion intra- et inter-groupe, puis le script 5 pour choisir des nombres de groupes fixes et produire une liste des num�ros de groupes associ�s � chaque patch.


*4b-patch_clust_choix_ncl* et *5b-patch_clust_ncl_fixe*

Lorsque le nombre de patches est grand (> 100 000, et peut-�tre avant), l'algorithme utilis� jusqu'� maintenant (*AgglomerativeClustering* dans Python) demande trop de ressources, donc on utilise l'algorithme plus rapide *Birch* pour effectuer un premier regroupement des patches, avant d'appliquer *AgglomerativeClustering* aux groupes produits par Birch. Ces deux scripts sont donc �quivalents aux scripts 4 et 5 avec cette �tape suppl�mentaire.