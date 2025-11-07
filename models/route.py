
class Route:
    def __init__(self, nom, longueur, limite_de_vitesse, vehicules_presents=None):
        try:
            if not isinstance(nom, str) or not nom:
                raise ValueError("Le nom de la route doit être une chaîne de caractères non vide.")
            if not isinstance(longueur, (int, float)) or longueur <= 0:
                raise ValueError("La longueur de la route doit être un nombre positif.")
            if not isinstance(limite_de_vitesse, (int, float)) or limite_de_vitesse <= 0:
                raise ValueError("La limite de vitesse doit être un nombre positif.")
            if vehicules_presents is not None and not isinstance(vehicules_presents, list):
                raise ValueError("La liste des véhicules présents doit être une liste ou None.")

            self.nom = nom
            self.longueur = longueur
            self.limite_de_vitesse = limite_de_vitesse
            self.vehicules_presents = vehicules_presents if vehicules_presents else []
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la route : {e}")
            raise # Relaisser l'exception pour que l'appelant puisse la gérer
    def ajouter_vehicule(self, vehicule):
        try:
            if not hasattr(vehicule, 'identifiant'):
                raise ValueError("L'objet véhicule n'a pas d'attribut 'identifiant'.")
            
            if vehicule.identifiant not in self.vehicules_presents:
                self.vehicules_presents.append(vehicule.identifiant)
                print(f"Véhicule {vehicule.identifiant} ajouté à la route {self.nom}.") 
            else:
                print(f"Véhicule {vehicule.identifiant} est déjà sur la route {self.nom}.")

        except ValueError as e:
            print(f"Erreur lors de l'ajout d'un véhicule à la route '{self.nom}' : {e}")
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors de l'ajout d'un véhicule : {e}")
    def retirer_vehicule(self, vehicule):

        try:
            if not hasattr(vehicule, 'identifiant'):
                raise ValueError("L'objet véhicule n'a pas d'attribut 'identifiant'.")

            if vehicule.identifiant in self.vehicules_presents:
                self.vehicules_presents.remove(vehicule.identifiant)
                print(f"Véhicule {vehicule.identifiant} retiré de la route {self.nom}.") # Pour debug
            else:
                print(f"Véhicule {vehicule.identifiant} n'était pas sur la route {self.nom}.") # Pour debug
        except ValueError as e:
            print(f"Erreur lors du retrait d'un véhicule de la route '{self.nom}' : {e}")
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors du retrait d'un véhicule : {e}")
    def __repr__(self):
        return f"Route({self.nom}, {self.longueur}m, {self.limite_de_vitesse}m/s)"