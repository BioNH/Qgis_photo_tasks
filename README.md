Ce script python a été créé pour injecter les coordonnées GPS de points (fichier shape) dans les métadonnées des photos correspondantes, il permet aussi de générer une table avec les noms des nouveaux fichiers photos (new_fichier_gps.jpg du répertoire NEW) de chaque point (station). La table peut être utilisée pour afficher les photos dans QGIS via une liaison.
Toutes les résultats ont été testées uniquement avec QGIS 3.40

> Conditions préalables :

> **Photos** : les fichiers sont dans un même répertoire et sont nommés de façon à pouvoir être identifiés en fonction d'un identifiant station.
> *ex : CodeMission_P{i}_xxx.jpg, ici les noms avec le même P{i}*
> 	
> **Fichier.shp** : la table attributaire des stations contient à minima 
> 
> un champs avec le préfixe des fichiers photos (identifiant station) 
> *par ex : CodeMission_P{i} dans le champs "FICHIER"*
> 
> les coordonnées latitude et longitude de la station exprimés en degrés décimaux 
> *par ex : les champs "LAT_DD" et "LONG_DD"*
> 
> *** Attention à ne pas utiliser d'espace dans les noms de champs ***
 
Etape 1 : Charger un fichier de points 'Station.shp' dans QGIS
 
Etape 2 : Exporter la table Station en .xlsx

Etape 3 : Charger les photos à modifier dans un dossier (n photos en .jpg)

Etape 4 : Faire tourner le script Python "QGIS_photo_tasks"

	  *** Attention à modifier les noms de chemin dans le script avec le bon séparateur "/" ***
	  >>> Création d'un dossier NEW et copie des photos modifiées dans ce dossier
	  >>> Les nouvelles photos portent le suffixe _gps.jpg en fin de nom
	  Vérifier qu'on a bien le même nombre de photos en sortie
	  >>> On obtient un fichier xlsx avec le nom des photos dans les colonnes "PHOTO_1", "PHOTO_2" ...

Etape 5 : Charger le nouveau fichier xslx dans QGIS (faire une jointure avec une autre table en prenant soin de personnaliser/supprimer le préfixe du nom de la table jointe)

Etape 6 : Dans les propriétés de la couche, copier le script "Infobulle - QGIS", en prenant soin de mettre à jour le chemin du répertoire photos
	  >>> Les photos s'affichent en diaporama lorsqu'on clique sur la station
	  *** Attention à activer "Afficher les Info bulles" dans le Menu "Vue" de QGIS

ou Etape 5bis : Importer les nouvelles photos avec leurs coordonnées GPS en métadonnées
