import pandas as pd
import os
from PIL import Image
import piexif


# >>> TRAITEMENT DU XLSX EN EXIF GPS

def convert_to_dms(decimal_degrees):

    degrees = abs(int(decimal_degrees))
    minutes = int((abs(decimal_degrees) - abs(degrees)) * 60)
    seconds = (abs(decimal_degrees) - degrees - (minutes/60)) * 3600

    return (degrees, 1), (minutes, 1), (int(seconds * 100), 100)

def create_gps_column(df, colonne_latitude, colonne_longitude, colonne_profondeur):

    df['GPS_info'] = None # Créer une colonne vide GPS_info

    gps_dict_list = []

    for index, row in df.iterrows(): # Remplir la colonne 'GPS_info' avec des données GPS converties
        latitude = row[colonne_latitude]
        longitude = row[colonne_longitude]
        altitude = row[colonne_profondeur]  # Utilisation de PROFONDEUR comme l'altitude

        # Convertir la latitude et la longitude en DMS
        latitude_dms = convert_to_dms(latitude)
        longitude_dms = convert_to_dms(longitude)

        gps_dict = {
            piexif.GPSIFD.GPSLatitudeRef: b'N' if latitude >= 0 else b'S',
            piexif.GPSIFD.GPSLatitude: latitude_dms,
            piexif.GPSIFD.GPSLongitudeRef: b'E' if longitude >= 0 else b'W',
            piexif.GPSIFD.GPSLongitude: longitude_dms,
            piexif.GPSIFD.GPSAltitude: (int(altitude), 1)
            }

        gps_dict_list.append(gps_dict)

    df['GPS_info'] = gps_dict_list # Ajouter la liste GPS_info à la colonne 'GPS_info'

    return df

def import_gps_from_xlsx(file_path, nom_colonne,  colonne_latitude, colonne_longitude, colonne_profondeur):

    df = pd.read_excel(file_path)

    result_df = df[[nom_colonne, colonne_latitude, colonne_longitude, colonne_profondeur]].copy()  # Créer une copie explicite
    result_df_gps = create_gps_column(result_df, colonne_latitude, colonne_longitude, colonne_profondeur)

    # print(result_df_gps)
    return result_df_gps

# >>> TRAITEMENT DES PHOTOS

def add_gps_to_photos(df, photos_directory, nom_colonne, identifiant_xlsx, identifiant_photo):

    new_directory = os.path.join(photos_directory, f'NEW_{identifiant_xlsx}') # Créer le sous-dossier 'NEW' s'il n'existe pas déjà
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    for index, row in df.iterrows():     # Parcourir chaque ligne du dataframe
        fichier = row[nom_colonne]  # Le nom de la station (ex: OFB2023_Pilier_P1)
        gps_info = row['GPS_info']  # Les coordonnées GPS à ajouter associées à cette station
        # print(f'Ligne issue du SIG {fichier}')

        if identifiant_xlsx in fichier:
            station_number = fichier.split(identifiant_xlsx)[1]  # Extraire le numéro du Pilier (i) à partir de 'OFB2023_Pilier_P{i}'
            print(f'Code mission correct : Station associée = {station_number}')

            photo_list = []

            # Recherche des photos dans le répertoire spécifié
            for filename in os.listdir(photos_directory):
                if f"{identifiant_photo}{station_number}_" in filename: # Si le nom du fichier de l'image contient _P{i} (par exemple _P1_ pour Pilier 1)

                    photo_list.append(filename)

                    image_path = os.path.join(photos_directory, filename)
                    img = Image.open(image_path)  # Ouvrir l'image
                    print(f"Ajout des coordonnées GPS à {filename} avec {gps_info}")

                    exif_dict = piexif.load(img.info.get('exif', b""))
                    exif_dict['GPS'] = gps_info
                    exif_bytes = piexif.dump(exif_dict)

                    new_filename = filename.replace(".JPG", "_gps.JPG")
                    new_image_path = os.path.join(new_directory, new_filename)
                    img.save(new_image_path, exif=exif_bytes) # Sauvegarder l'image avec les nouvelles métadonnées EXIF

            for i, photo in enumerate(photo_list):
                col_name = f'PHOTO_{i + 1}'
                df.at[index, col_name] = photo
        else:
            print(f'Code mission incorrect : {fichier} ignoré')

    print("Fin du traitement")

    return df
# **********************************************

# VARIABLES POUR L'EXPLOITATION DU FICHIER EXCEL

source_file_path_xlsx = 'C:/Chemin/vers/fichier/Table_stations_exportées.xlsx' #Fichier xlsx issu de QGIS
nom_colonne = 'FICHIER' #nom de la colonne qui contient le nom des stations
colonne_latitude = 'LAT_DD'
colonne_longitude = 'LONG_DD'
colonne_profondeur = 'PROFONDEUR'

new_file_path_xlsx = 'C:/Chemin/vers/fichier/Nouveau_fichier_avec_Nom_photos.xlsx' #Nom du nouveau fichier Excel avec les photos

identifiant_xlsx = 'CodeMission_PrefixSta' #ce qui permet de trouver le numéro de la station à partir du nom stocké dans le fichier EXCEL - split
identifiant_photo = 'PrefixSta' #ce qui permet de trouver le numéro {i} de la station dans le nom de la photo au format xxxx_P{i}_xxx entouré de "_" - contains
photos_directory = 'C:/Chemin/vers/repertoire_photos_originales/'  # Remplacez par le chemin du répertoire des photos

#STEP 1 : On crée un dataframe à partir du fichier Excel issu de QGIS avec des données GPS au bon format pour une opération sur les métadonnées
result_df = import_gps_from_xlsx(source_file_path_xlsx, nom_colonne, colonne_latitude, colonne_longitude, colonne_profondeur)
#STEP 2 : On parcourt le répertoire photo en ajoutant les métadonnées GPS et en ajoutant une colonne au dataframe avec le nom des photos (des photos modifiées)
updated_df = add_gps_to_photos(result_df, photos_directory, nom_colonne, identifiant_xlsx, identifiant_photo)
#STEP 3 : On enregistre le nouveau dataframe avec le nom des photos au format .xlsx
updated_df.to_excel(new_file_path_xlsx, index=False)

#SANS "GPS INFO"
without_gps_df = updated_df.drop('GPS_info', axis=1).copy()
new_file_path_xlsx_2 = new_file_path_xlsx.replace('.xlsx', '_2.xlsx')
without_gps_df.to_excel(new_file_path_xlsx_2, index=False)

# NB. Sources d'erreur possible : JPG ou jpg, identifiant_xlsx ou identifiant_photo mal définis (qui ne permettent pas de bien identifier le numéro de la station)
