# Ce script realise la premiere classification (avec connectivite)
# pour differents nombre de groupes ("patches") 'n_cl' et
# calcule la dispersion intra-groupe

import numpy as np
import numpy_indexed as npi
import pickle

from sklearn.cluster import AgglomerativeClustering

# Fonction pour la dispersion intra-groupe (somme des ecarts carres 
# entre chaque variable de chaque pixel et la moyenne du groupe)
def calc_intra_disp(X, labels):
	n_labels = max(labels) + 1
	X_sort = X[np.argsort(labels),]
	grp_mean = npi.group_by(labels).mean(X)[1]
	grp_count = npi.count(labels)[1]
	mean_rep = np.concatenate([np.tile(grp_mean[i], (grp_count[i], 1)) for i in range(n_labels)])
	return np.sum((X_sort - mean_rep) ** 2)

	
# Charger la matrice de donnees et le graphe de connectivite
with open('region_mat_norm', 'rb') as dat_file:
    dat = pickle.load(dat_file)
    
with open('region_graph', 'rb') as graph_file:
    gr = pickle.load(graph_file)

# Differents nombres de groupes (n_cl) a utiliser
#  (300 valeurs de 10^3 a 10^6 sur une echelle logarithmique)
n_cl_list = np.logspace(3,6,300).astype('int')	

# Effectue la classification avec connectivite pour chaque valeur de n_cl
# calcule la dispersion intra-groupe et l'imprime en sortie
for n_cl in n_cl_list:
    cl = AgglomerativeClustering(n_clusters = n_cl, linkage = 'ward', 
      connectivity = gr, memory = '/scratch/marchanp', compute_full_tree = True)
    cl.fit(dat)
    intra = calc_intra_disp(dat, cl.labels_)
    print(n_cl, intra)
    
# Note: Les arguments 'compute_full_tree' et 'memory' assurent que l'arbre complet
# soit enregistre sur le disque pour la premiere classification, ce qui accelere
# les executions suivantes d'AgglomerativeClustering pour les memes donnees


