# Code pour le projet de classification des milieux humides en Abitibi

Philippe Marchand, juin 2022
 
Ce r�pertoire contient le code utilis� pour le projet de classification des milieux humides en Abitibi (contrat UQAT-MELCC). Le code est organis� en trois dossiers correspondant � la pr�paration des donn�es (*prep-donnees*), � la classification comme telle (*classif*) et � l'exploration / la visualisation des r�sultats (*traitement-resultats*). Chaque dossier contient un fichier *README* qui documente les diff�rents fichiers pr�sents.

### Utilisation avec Calcul Canada

J'ai aussi inclus dans ce dossier principal un exemple des scripts Bash pour soumettre un script R (*run_1core_r.sh*) ou Python (*run_1core_py.sh*) � la grappe de calcul de Calcul Canada avec l'ordonnanceur de t�ches Slurm. Voici un exemple des commandes utilis�es pour soumettre des scripts:

```
sbatch run_1core_py.sh nom_du_script.py
sbatch run_1core_r.sh nom_du_script.R
```
Les arguments *time* et *mem-per-cpu* doivent �tre ajust�s dans le script Bash en fonction des ressources requises pour la t�che. Notons que le script *run_1core_r.sh* charge le module *gdal*, car celui-ci est requis pour le package *raster* dans R. 

Pour plus d'informations, se r�f�rer aux pages d'aide de Calcul Canada en ligne (https://docs.alliancecan.ca/wiki/Technical_documentation) en ce qui concerne le fonctionnement de Slurm et l'ex�cution de code R ou Python sur les serveurs de calcul. 







