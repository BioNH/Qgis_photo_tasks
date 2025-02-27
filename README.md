Ce script python a été créé pour injecter les coordonnées GPS de points (fichier shape) dans les métadonnées des photos correspondantes, il permet aussi de relier les fichiers photos d'un répertoire à un fichier de points géoréférencés (type shape) via un identifiant.
Toutes les résultats ont été testées uniquement avec QGIS 3.40
 
Etape 1 : Charger le fichier de points Station.shp dans QGIS
 
Etape 2 : Exporter la table Station en .xlsx

Etape 3 : Charger les photos à modifier dans un dossier (n photos en .jpg)

Etape 4 : Faire tourner le script Python "QGIS_photo_tasks"
	  *** Attention à modifier les noms de chemin dans le script ***
	  >>> Création d'un dossier NEW et copie des photos modifiées dans ce dossier
	  >>> Les nouvelles photos portent le suffixe _gps.jpg en fin de nom
	  Vérifier qu'on a bien le même nombre de photos en sortie
	  >>> On obtient un fichier xlsx avec le nom des photos dans les colonnes "PHOTO_1", "PHOTO_2" ...

Etape 5 : Charger le nouveau fichier xslx dans QGIS (faire une jointure avec une autre table en prenant soin de personnaliser/supprimer le prefixe du nom de la table jointe)

Etape 6 : Dans les propriétés de la couche, copier le script "Infobulle - QGIS" 
	  >>> Les photos s'affichent en diaporama lorsqu'on clique sur la station
	  *** Attention à activer "Afficher les Info bulles" dans le Menu "Vue" de QGIS

ou Etape 5bis : Importer les nouvelles photos avec leurs coordonnées GPS en métadonnées
