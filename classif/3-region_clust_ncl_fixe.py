# Ce script realise la premiere classification (avec connectivite)
# pour un nombre fixe de groupes ("patches"); produit comme sorties
# (1) la liste des numeros de patch associes a chaque pixel et 
# (2) une nouvelle matrice de donnees avec la moyenne de chaque 
#     variable de teledetection par patch
import numpy as np
import numpy_indexed as npi
import pickle

from sklearn.cluster import AgglomerativeClustering

# Charger la matrice de donnees et le graphe de connectivite
with open('region_mat_norm', 'rb') as dat_file:
    dat = pickle.load(dat_file)
    
with open('region_graph', 'rb') as graph_file:
    gr = pickle.load(graph_file)

# Realiser la classification pour un n_cl groupes
n_cl = 28500
cl = AgglomerativeClustering(n_clusters = n_cl, linkage = 'ward', 
                             connectivity = gr, memory = '/scratch/marchanp')
cl.fit(dat)

# Charger le masque des pixels inclus dans la classification
with open('region_mask_connect', 'rb') as mask_file:
    mask_connect = pickle.load(mask_file)
    
# Assigner le numero de groupe a chaque pixel non-masque (pixels masques restent 0)
mask_labels = mask_connect.flatten().astype('int')
mask_labels[np.argwhere(mask_labels == 1).ravel()] = cl.labels_ + 1

mask_labels = np.reshape(mask_labels, mask_connect.shape)
np.savetxt('region_mask_labels' + str(n_cl) + '.txt', mask_labels)

# Calculer la moyenne des variables d'entree de la classification par groupe
dat_patch = npi.group_by(cl.labels_).mean(dat)

with open('patch_' + str(n_cl), 'wb') as dat_patch_file:
	pickle.dump(dat_patch, dat_patch_file)

	
