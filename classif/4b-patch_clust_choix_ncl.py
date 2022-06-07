# Ce script realise la deuxieme classification (globale) avec l'algorithme Birch
# pour differents nombre de groupes 'n_cl', puis
# calcule la dispersion intra-groupe et inter-groupe

import numpy as np
import numpy_indexed as npi
import pickle

from sklearn.cluster import Birch
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin

# Fonction pour la dispersion intra-groupe (somme des ecarts carres entre 
# chaque variable de chaque pixel et la moyenne du groupe) et inter-groupe
# (somme des ecarts carres entre la moyenne des groupes et la moyenne generale, 
#  multiplies par les effectifs de chaque groupe)
def calc_intra_inter_disp(X, labels):
	n_labels = max(labels) + 1
	X_sort = X[np.argsort(labels),]
	grp_mean = npi.group_by(labels).mean(X)[1]
	grp_count = npi.count(labels)[1]
	mean_rep = np.concatenate([np.tile(grp_mean[i], (grp_count[i], 1)) for i in range(n_labels)])
	intra = np.sum((X_sort - mean_rep) ** 2)
	inter = np.sum(grp_count * np.sum(grp_mean**2, axis = 1))
	return intra, inter

# Charger la matrice de donnees produite a l'etape 1 (ici, 278500 patches)
with open('patch_278500', 'rb') as dat_file:
    dat = pickle.load(dat_file)[1]

# Effectuer un premier regroupement avec l'algorithme Birch
# et un seuil de distance specifie (ici, 2)
cl = Birch(n_clusters = None, threshold = 2)
for x in dat:
    cl.partial_fit(x.reshape(1, -1))

# Sauvegarder les centroides des groupes produits par Birch dans un fichier binaire
birch_res = cl.subcluster_centers_

with open('patch_birch_278500', 'wb') as birch_file:
    pickle.dump(birch_res, birch_file)
    
# Associer chaque element original au centroide le plus pres avec pairwise_distance_argmin    
birch_labels = pairwise_distances_argmin(dat, birch_res)
    
# Effectuer le regroupement final des centroides produits par Birch pour differents
# nombre de groupes et produit en sortie la dispersion intra-groupe et inter-groupe
n_cl_list = np.arange(2,51);

for n_cl in n_cl_list:
    cl = AgglomerativeClustering(n_clusters = n_cl, linkage = 'ward',
     memory = '/scratch/marchanp', compute_full_tree = True)
    cl.fit(birch_res)
    # La ligne ci-dessous permet d'associer les numeros de groupes aux elements
    # originaux (patches) plutot qu'aux groupes produits par Birch
    dat_labels = cl.labels_[birch_labels]
    intra, inter = calc_intra_inter_disp(dat, dat_labels)
    print(n_cl, intra, inter)
