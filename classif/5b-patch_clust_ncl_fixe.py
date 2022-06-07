# Ce script realise la deuxieme classification (globale) avec l'algorithme Birch
# pour des nombres de groupes specifies; produit comme sortie
# la liste des numeros de groupe associes a chaque patch en format .txt

import numpy as np
import pickle

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin

# Charger la matrice de donnees produite a l'etape 1 (ici, 278500 patches)
# et le resultat de la classification partielle avec l'algorithme Birch
with open('patch_278500', 'rb') as dat_file:
    dat = pickle.load(dat_file)[1]

with open('patch_birch_278500', 'rb') as birch_file:
    birch_res = pickle.load(birch_file)

# Associer chaque element original au groupe le plus pres produit par Birch    
birch_labels = pairwise_distances_argmin(dat, birch_res)

n_cl_list = [9, 26, 32, 44];

for n_cl in n_cl_list:
    cl = AgglomerativeClustering(n_clusters = n_cl, linkage = 'ward',
     memory = '/scratch/marchanp', compute_full_tree = True)
    cl.fit(birch_res)
    dat_labels = cl.labels_[birch_labels]
    np.savetxt('patch_278500_labels' + str(n_cl) + '.txt', dat_labels)
   


