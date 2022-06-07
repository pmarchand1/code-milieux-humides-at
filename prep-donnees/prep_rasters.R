### Preparation des donnees geographiques matricielles pour la classification non-supervisee

library(stringr)
library(raster)
library(rgdal)
library(dplyr)
# Le repertoire temporaire /scratch s'applique aux serveurs de Calcul Canada
rasterOptions(tmpdir = "/scratch/marchanp", maxmemory = 1E9)


# Convertir l'aspect en 2 variables (sud-nord, ouest-est) -----------------

asp_dir <- "Indices/Topographie/Exposition"
asp <- raster(file.path(asp_dir, "r_asp.tif"))

calc(asp, function(x) ifelse(x == -1, 0, sin(x)), 
     filename = file.path(asp_dir, "r_asp_north.tif"))
calc(asp, function(x) ifelse(x == -1, 0, cos(x)), 
     filename = file.path(asp_dir, "r_asp_east.tif"))


# Ramener toutes les couches dans la meme grille ------------------------

# Lire les 33 couches specifiees dans le fichier .csv
rast_files <- read.csv("rast_files.csv")
rasts <- lapply(rast_files$path, raster)
names(rasts) <- sapply(rasts, names)
    
# Utilisant la grille des couches Landsat (resolution 30 m) comme modele,
# generer des grilles qui lui sont alignees avec 10 m et 5 m de resolution
templ10 <- disaggregate(rasts[["Le_ndvi_f"]], fact = 3)
templ5 <- disaggregate(rasts[["Le_ndvi_f"]], fact = 6)

# Aligner les autres grilles a la grille modele avec resample
# puis agreger les donnees a 5 et 10 m a 30 m avec aggregate (prend la moyenne)
for (layer in names(rasts)) {
    if (str_detect(layer, "^AMP")) { # Palsar: reso 30 m, grille differente
        rasts[[layer]] <- rasts[[layer]] %>%
            resample(rasts[["Le_ndvi_f"]])
    } else if (str_detect(layer, "^S1")) { # radar Sentinel1: reso 10 m
        rasts[[layer]] <- rasts[[layer]] %>%
            resample(templ10) %>% 
            aggregate(fact = 3)
    } else if (!str_detect(layer, "^L")) { # couches basees sur le LiDAR: 5 m
            rasts[[layer]] <- rasts[[layer]] %>%
            resample(templ5) %>%
            aggregate(fact = 6)
    }
    writeRaster(rasts[[layer]], filename = paste0("aligned/", layer, "_30m.tif"))
}


# Creation des masques ----------------------------------------------------

# Extraire un masque pour l'eau a partir de la categorie "Aquatique"
# de la carte d'utilisation du territoire
terr <- raster("utilisation_territoire_2018/utilisation_territoire_2018.tif")
terr_classes <- read.csv("utilisation_territoire_2018/utilisation_territoire_2018.csv")
codes_eau <- terr_classes$VALUE[terr_classes$DESC_CAT == "Aquatique"]
templ <- rasts[["Le_ndvi_f"]]
# Reprojeter et aligner a la grille modele avec projectRaster
# (interpolation "ngb" =  nearest neighbor)
terr <- projectRaster(terr, templ, method = "ngb")
eau <- terr %in% codes_eau
writeRaster(eau, filename = "region_eau_30m.tif")
    
# Le masque conserve les cellules qui ne sont pas aquatiques et
# qui n'ont aucune donnee manquante parmi l'ensemble des couches (count_na == 0)
rast_stack <- stack(rasts)
count_na <- calc(rast_stack, fun = function(x) sum(is.na(x)))
region_mask <- eau == 0 & count_na == 0
writeRaster(region_mask, filename = "abitibi_full_mask_30m.tif")

# On ajoute un critere au masque pour seulement conserver la region d'etude
# selectionnee pour ce projet (shapefile dans le dossier "site_etude")
site_etude <- readOGR("site_etude")
site_etude <- spTransform(site_etude, crs(region_mask))
region_mask <- mask(region_mask, site_etude, updatevalue = 0)
writeRaster(region_mask, filename = "region_mask_30m.tif")