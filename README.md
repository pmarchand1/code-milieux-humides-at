# Code pour le projet de classification des milieux humides en Abitibi

Philippe Marchand, juin 2022
 
Ce répertoire contient le code utilisé pour le projet de classification des milieux humides en Abitibi (contrat UQAT-MELCC). Le code est organisé en trois dossiers correspondant à la préparation des données (*prep-donnees*), à la classification comme telle (*classif*) et à l'exploration / la visualisation des résultats (*traitement-resultats*). Chaque dossier contient un fichier *README* qui documente les différents fichiers présents.

### Utilisation avec Calcul Canada

J'ai aussi inclus dans ce dossier principal un exemple des scripts Bash pour soumettre un script R (*run_1core_r.sh*) ou Python (*run_1core_py.sh*) à la grappe de calcul de Calcul Canada avec l'ordonnanceur de tâches Slurm. Voici un exemple des commandes utilisées pour soumettre des scripts:

```
sbatch run_1core_py.sh nom_du_script.py
sbatch run_1core_r.sh nom_du_script.R
```
Les arguments *time* et *mem-per-cpu* doivent être ajustés dans le script Bash en fonction des ressources requises pour la tâche. Notons que le script *run_1core_r.sh* charge le module *gdal*, car celui-ci est requis pour le package *raster* dans R. 

Pour plus d'informations, se référer aux pages d'aide de Calcul Canada en ligne (https://docs.alliancecan.ca/wiki/Technical_documentation) en ce qui concerne le fonctionnement de Slurm et l'exécution de code R ou Python sur les serveurs de calcul. 







