# Ce script realise la deuxieme classification (globale)
# pour differents nombre de groupes 'n_cl', puis
# calcule la dispersion intra-groupe et inter-groupe

import numpy as np
import numpy_indexed as npi
import pickle

from sklearn.cluster import AgglomerativeClustering

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


# Charger la matrice de donnees produite a l'etape 1 (ici, 28500 patches)
with open('patch_28500', 'rb') as dat_file:
    dat = pickle.load(dat_file)[1]
    
    
# Effectuer la classification hierarchique pour differentes valeurs de n_cl,
# calcule la dispersion intra-groupe et inter-groupe et les imprime en sortie
n_cl_list = np.arange(2,51);

for n_cl in n_cl_list:
    cl = AgglomerativeClustering(n_clusters = n_cl, linkage = 'ward',
     memory = '/scratch/marchanp', compute_full_tree = True)
    cl.fit(dat)
    intra, inter = calc_intra_inter_disp(dat, cl.labels_)
    print(n_cl, intra, inter)

# Note: Les arguments 'compute_full_tree' et 'memory' assurent que l'arbre complet
# soit enregistre sur le disque pour la premiere classification, ce qui accelere
# les executions suivantes d'AgglomerativeClustering pour les memes donnees
   


