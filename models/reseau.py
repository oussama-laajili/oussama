import json
from models.route import Route
from models.vehicule import Vehicule
import os
class ReseauRoutier:
    def __init__(self):
        self.routes = {}  # Dict: nom -> Route
        self.intersections = {}  # Dict: nom -> liste de routes connectées
        self.vehicules = {}  # Dict: id -> Vehicule
    def ajouter_route(self, route):
        self.routes[route.nom] = route

    def ajouter_intersection(self, intersection):
        self.intersections[intersection['nom']] = intersection['connecte']
    def ajouter_vehicule(self, vehicule):
        self.vehicules[vehicule.identifiant] = vehicule
        try:
            if vehicule.route_actuelle in self.routes:
                self.routes[vehicule.route_actuelle].ajouter_vehicule(vehicule)
            else:
                raise ValueError(f"La route actuelle '{vehicule.route_actuelle}' du véhicule '{vehicule.identifiant}' n'existe pas dans le réseau.")
        except ValueError as e:
            print(f"Erreur lors de l'ajout du véhicule à sa route : {e}")
    def charger_config(self):
        fichier_json = None
        if fichier_json is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)
            fichier_json = os.path.join(base_dir, 'data', 'config_reseau.json')
        else:
            fichier_json = os.path.abspath(fichier_json)
    
        try:
            if not os.path.exists(fichier_json):
                raise FileNotFoundError(f"Le fichier de configuration '{fichier_json}' est manquant.")
            
            print(f"Chargement du fichier: {fichier_json}")
            with open(fichier_json, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            for route_data in config_data.get("routes", []):
                try:
                    route = Route(**route_data)
                    self.ajouter_route(route)
                except TypeError as e:
                    raise ValueError(f"Données invalides pour une route : {route_data}. Erreur: {e}")
            
            for intersection in config_data.get("intersections", []):
                try:
                    self.ajouter_intersection(intersection)
                except KeyError as e:
                    raise ValueError(f"Données invalides pour une intersection : {intersection}. Clé manquante: {e}")
            
            for vehicule_data in config_data.get("vehicules", []):
                try:
                    vehicule = Vehicule(**vehicule_data)
                    self.ajouter_vehicule(vehicule)
                except TypeError as e:
                    raise ValueError(f"Données invalides pour un véhicule : {vehicule_data}. Erreur: {e}")

        except FileNotFoundError as e:
            print(f"Erreur : {e}")
        except json.JSONDecodeError as e:
            print(f"Erreur de lecture du fichier JSON : Le fichier '{fichier_json}' est mal formaté. Erreur: {e}")
        except ValueError as e:
            print(f"Erreur de données invalides lors du chargement de la configuration : {e}")
        except Exception as e: 
            print(f"Une erreur inattendue est survenue lors du chargement de la configuration : {e}")
    def obtenir_route_suivante(self, vehicule):

        try:
            if vehicule.itineraire is None or not isinstance(vehicule.itineraire, list):
                raise ValueError(f"L'itinéraire du véhicule '{vehicule.identifiant}' est invalide ou inexistant.")
            if vehicule.index_itineraire < 0:
                raise ValueError(f"L'index d'itinéraire du véhicule '{vehicule.identifiant}' est négatif.")
            
            if vehicule.index_itineraire + 1 < len(vehicule.itineraire):
                return vehicule.itineraire[vehicule.index_itineraire + 1]
            else:
                return None
        except ValueError as e:
            print(f"Erreur lors de l'obtention de la route suivante pour le véhicule '{vehicule.identifiant}' : {e}")
            return None
        except ZeroDivisionError:
            print("Erreur : Tentative de division par zéro (non applicable ici mais inclus pour l'exercice).")
            return None
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors de l'obtention de la route suivante : {e}")
            return None