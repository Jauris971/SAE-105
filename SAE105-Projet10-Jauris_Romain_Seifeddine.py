import csv
from datetime import datetime
import matplotlib.pyplot as plt
from pylab import plot, show, xlabel, ylabel, title

# Initialisation des listes pour stocker les données
dates = []
humidite = []
stations = []

fic = 'Q19502023AutresParametres.csv'  # Remplacez par le chemin de votre fichier
with open(fic, newline='') as csvfile:
    rel = csv.reader(csvfile, delimiter=';')
    debut = next(rel)  # a chaque appel de la fonction, next() va récupérer la prochaine valeur du tableau, remplace l'ajout de chaque ligne a une liste
    
    # Obtenir les indices des colonnes
    date = debut.index('AAAAMMJJ')
    hum = debut.index('UM')
    station = debut.index('NOM_USUEL')

    # Lire les lignes et détecter les erreurs
    for row_num, row in enumerate(rel, start=2):  # Les lignes commencent à 2 (1 pour l'en-tête)
        date_str = row[date]
        humidite_str = row[hum].strip()  # Supprimer les espaces autour des données
        station_str = row[station]

        # Vérifier si les données essentielles (humidité ou station) sont vides
        if not humidite_str or not station_str:
            continue  # Si l'humidité ou la station est vide, on passe à la ligne suivante

        # Ajouter aux listes uniquement si les données sont valides
        dates.append(datetime.strptime(date_str, '%Y%m%d'))
        humidite.append(float(humidite_str))
        stations.append(station_str)

# Si des données valides ont été trouvées, procéder à l'analyse
if dates and humidite and stations:
    stations_inferieures_60 = {}

    while True:
        # Demander à l'utilisateur la station, l'année et le mois
        station_choisie_fin = input("Entrez le nom de la station EN MAJUSCULE: ")
        annee = int(input("Entrez l'année (exemple : 2023) : "))
        mois = int(input("Entrez le mois (exemple : 1 pour janvier, 12 pour décembre) : "))

        # Filtrer les données pour la station, l'année et le mois sélectionnés
        dates_filtrees = [d for d, h, s in zip(dates, humidite, stations) if s == station_choisie_fin and d.year == annee and d.month == mois]#  filtre les dates de la liste dates en fonction de la station, de l'année et du mois spécifiés par l'utilisateur. 
    
    # zip() permet d'itérer simultanément sur les listes dates, humidite et stations, et conserve uniquement les dates où la station correspond à celle choisie, et où l'année et le mois de la date correspondent aux critères donnés. Le résultat est stocké dans la liste dates_filtrees. Cela évite de faire de trop longues boucles redondantes et de condition "if"


        humidite_filtrees = [h for d, h, s in zip(dates, humidite, stations) if s == station_choisie_fin and d.year == annee and d.month == mois] # même chose ici

        if dates_filtrees and humidite_filtrees:
            plt.figure(figsize=(10, 6))
            plot(dates_filtrees, humidite_filtrees, marker='o')
            xlabel('Jour')
            ylabel('Humidité (%)')
            title(f'Moyenne des variations de l\'humidité pour {station_choisie_fin} en {mois}/{annee}')
            plt.grid()
            show()

            # Vérifier si la station a un taux d'humidité inférieur à 60% pendant au moins 5 jours
            count_jours_inferieurs_60 = sum(1 for h in humidite_filtrees if h < 60)

            if count_jours_inferieurs_60 >= 5:
                # Ajouter la station et ses dates correspondantes dans le dictionnaire
                stations_inferieures_60[station_choisie_fin] = [d for d, h in zip(dates_filtrees, humidite_filtrees) if h < 60]

            print(f"Station analysée : {station_choisie_fin}.")
            print(f"Nombre de jours avec humidité inférieure à 60% : {count_jours_inferieurs_60}")

        # Demander à l'utilisateur s'il veut analyser une autre station/mois ou arrêter
        continuer = input("Voulez-vous analyser une autre station ou un autre mois ? (appuyez sur 'q' pour quitter, n'importe quelle autre touche pour continuer) : ")
        if continuer.lower() == 'q':
            break

    # Afficher la liste des stations avec une humidité inférieure à 60% pendant au moins 5 jours
    print("\nStations ayant relevé un taux d'humidité inférieur à 60% pendant au moins 5 jours :")
    
    for station, dates_inf in stations_inferieures_60.items():
        print(f"Station : {station}")
        print(f"Dates : {', '.join(d.strftime('%Y-%m-%d') for d in dates_inf)}")

else:
    print("Aucune donnée valide trouvée dans le fichier CSV.")
