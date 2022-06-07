# Code pour visualiser la variation de la dispersion intra-groupe en fonction
# du nombre de groupes 'k' afin de choisir un nombre optimal pour la classification

library(dplyr)
library(ggplot2)

# Premiere etape de classification

n <- 19983777 # nombre de pixels a regrouper en patches

res <- read.table("res_cluster/clust_region.txt")
colnames(res) <- c("k", "intra")
# Quantites derivees:
#  - v_intra = variance intra-patch, 
#  - diff_intra = pente et variation de la pente de log(v_intra) vs. log(k)
#  - diff2_intra = variation de la pente
#  - min = indique un nombre de groupes ou diff2_intra atteint un minimum local 
res <- mutate(res, v_intra = intra / (n - k),
              log_v_intra = log(v_intra), log_k = log(k),
              diff_intra = c(NA, diff(log_v_intra) / diff(log_k)),
              diff2_intra = c(NA, diff(diff_intra) / diff(log_k)),
              min = diff2_intra < 0 & lead(diff2_intra) > 0)

# On cherche des minima locaux de diff_intra qui sont suivis par un plateau
#  (plus difficile a voir pour de grands k, on peut magnifier le graphique ou
#   refaire le calcul de v_intra pour davantage de valeurs de k)
ggplot(filter(res, k < 350000), aes(x = k/1000, y = diff_intra)) +
    labs(x = "Nombre de patches (milliers)", y = "Taux de réduction de variance") +
    geom_line() +
    scale_x_log10(breaks = c(1, 3, 10, 30, 100, 300)) +
    geom_vline(xintercept = c(1.662, 3.999, 10.077, 28.500, 45.239, 164.964, 278.494),
               color = "red", linetype = "dotted") +
    geom_line()


###

# Deuxieme etape de classification

# Nombre de patches
n <- 28500

res <- read.table("res_cluster/patch_clust_28500.txt")

colnames(res) <- c("k", "intra", "inter")

# Quantites derivees:
#  - v_intra et v_inter: Variance intra- et inter-patch
#  - ch: Indice de Calinski-Harabasz (rapport v_inter / v_intra)
#  - diff_ch: pente de ch vs. k
#  - diff_intra et diff2_intra: pente et variation de la pente de v_intra vs. k
res <- mutate(res, v_intra = intra/(n-k), v_inter = inter/(k-1), 
              ch = v_inter / v_intra, diff_ch = c(NA, diff(ch)),
              diff_intra = c(NA, diff(v_intra)), diff2_intra = c(NA, diff(diff_intra)))

ggplot(res, aes(x = k, y = diff_intra)) + 
    geom_point() + 
    geom_line()

