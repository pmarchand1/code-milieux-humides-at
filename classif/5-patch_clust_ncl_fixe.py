# Ce script realise la deuxieme classification (globale)
# pour des nombres de groupes specifies; produit comme sortie
# la liste des numeros de groupe associes a chaque patch en format .txt

import numpy as np
import pickle

from sklearn.cluster import AgglomerativeClustering

# Charger la matrice de donnees produite a l'etape 1 (ici, 28500 patches)
with open('patch_28500', 'rb') as dat_file:
    dat = pickle.load(dat_file)[1]

n_cl_list = [8, 18, 33, 39];

for n_cl in n_cl_list:
    cl = AgglomerativeClustering(n_clusters = n_cl, linkage = 'ward',
     memory = '/scratch/marchanp', compute_full_tree = True)
    cl.fit(dat)
    np.savetxt('patch_28500_labels' + str(n_cl) + '.txt', cl.labels_)    


