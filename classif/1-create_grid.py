# Ce script sert principalement a creer le graphe de voisinage pour la 
# premiere etape de la classification (segmentation en "patches" homogenes).

# Il normalise aussi les variables contenues dans les couches matricielles.

import numpy as np
import matplotlib.pyplot as plt
import pickle
import rasterio
import glob
from sklearn.feature_extraction.image import grid_to_graph
from scipy.sparse.csgraph import connected_components

# Creer un premier graphe a partir du masque de la region d'etude
mask = rasterio.open('region_mask_30m.tif').read(1).astype('bool')
gr = grid_to_graph(*mask.shape, mask = mask)
mask1D = mask.ravel() # version "ecrasee" (en 1 dimension) du masque

# Determiner les composantes connectees du graphe
n_comp, labels = connected_components(csgraph=gr, directed=False, return_labels=True)
# Nouveau masque excluant les pixels qui ne sont pas dans la
# plus grande composante connectee (qui on suppose correspond a labels == 0)
mask_connect1D = mask1D
mask_connect1D[np.argwhere(mask1D).ravel()] = labels == 0
mask_connect = np.reshape(mask_connect1D, mask.shape)
# Recreer le graphe avec ce nouveau masque
gr = grid_to_graph(*mask.shape, mask = mask_connect)

## Code optionnel ci-dessous

## Voir le nombre de cellules par composante 
#unique, counts = np.unique(labels, return_counts=True)
#print(np.asarray((unique, counts)).T)

## Visualiser ce qui est exclus de la principale composante connectee
#mask1D_int = mask1D.astype('int') - 1
#mask1D_int[np.argwhere(mask1D).ravel()] = labels > 0
#labels_rast = np.reshape(mask1D_int, mask.shape)
#plt.imshow(labels_rast).savefig('test.png')


# Ecraser les couches matricielles de donnees en 1D,
# exclure les pixels masques, puis normaliser chaque couche
# (soustraire moyenne, diviser par l'ecart-type)
rast_files = glob.glob('aligned/*')
rasts = [rasterio.open(x).read(1).ravel() for x in rast_files]
rasts = [x[mask_connect1D] for x in rasts]
rasts_norm = [(x - np.mean(x))/np.std(x) for x in rasts]
# Finalement combiner en une seule matrice rstack 
#  (pixels en rangees, variables en colonnes)
rasts_norm = [x.reshape(-1, 1) for x in rasts_norm]
rstack = np.concatenate(rasts_norm, axis = 1)

# Sauvegarder les donnees, le graphe et le masque dans des fichiers binaires

with open('region_mat_norm', 'wb') as rstack_file:
    pickle.dump(rstack, rstack_file)
    
with open('region_graph', 'wb') as graph_file:
    pickle.dump(gr, graph_file)
    
with open('region_mask_connect', 'wb') as mask_file:
    pickle.dump(mask_connect, mask_file)
