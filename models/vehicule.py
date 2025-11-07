
class Vehicule:
    def __init__(self, id, route_initiale, position, vitesse, itineraire):
        try:
            if not isinstance(id, (int, str)) or (isinstance(id, str) and not id):
                raise ValueError("L'identifiant du véhicule doit être un entier ou une chaîne de caractères non vide.")
            if not isinstance(route_initiale, str) or not route_initiale:
                raise ValueError("La route initiale doit être une chaîne de caractères non vide.")
            if not isinstance(position, (int, float)) or position < 0:
                raise ValueError("La position doit être un nombre positif ou nul.")
            if not isinstance(vitesse, (int, float)) or vitesse < 0:
                raise ValueError("La vitesse doit être un nombre positif ou nul.")
            if not isinstance(itineraire, list) or not all(isinstance(r, str) for r in itineraire):
                raise ValueError("L'itinéraire doit être une liste de noms de routes (chaînes de caractères).")
            if not itineraire:
                raise ValueError("L'itinéraire ne doit pas être vide.")

            self.identifiant = id
            self.position = float(position)
            self.vitesse = float(vitesse)
            self.route_actuelle = route_initiale  # Nom de la route
            self.itineraire = itineraire  # Liste des noms de routes
            
            # Trouver l'index de la route initiale dans l'itinéraire
            try:
                self.index_itineraire = self.itineraire.index(route_initiale)
            except ValueError:
                raise ValueError(f"La route initiale '{route_initiale}' n'est pas présente dans l'itinéraire fourni.")

        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule {id} : {e}")
            raise # Relaisser l'exception pour que l'appelant puisse la gérer
    def avancer(self, delta_t, route_obj):
        """Avance le véhicule pendant delta_t secondes."""
        try:
            if not isinstance(delta_t, (int, float)) or delta_t < 0:
                raise ValueError("Le pas de temps (delta_t) doit être un nombre positif ou nul.")
            if not hasattr(route_obj, 'limite_de_vitesse') or not isinstance(route_obj.limite_de_vitesse, (int, float)) or route_obj.limite_de_vitesse < 0:
                raise ValueError(f"L'objet route ({route_obj}) est invalide ou sa limite de vitesse est manquante/négative.")
            
            # Éviter ZeroDivisionError si delta_t était un dénominateur, bien que pas directement ici
            if delta_t == 0:
                return self.position # Le véhicule ne bouge pas si le temps est nul

            distance = min(self.vitesse, route_obj.limite_de_vitesse) * delta_t
            self.position += distance
            return self.position
        except ValueError as e:
            print(f"Erreur lors de l'avancement du véhicule {self.identifiant} : {e}")
            return self.position # Retourne la position actuelle en cas d'erreur
        except ZeroDivisionError:
            # Cette erreur est moins probable ici, mais on la garde pour l'exemple si des calculs changeaient
            print(f"Erreur de division par zéro lors de l'avancement du véhicule {self.identifiant}.")
            return self.position
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors de l'avancement du véhicule {self.identifiant} : {e}")
            return self.position
    def changer_de_route(self, nouvelle_route):
        """Change le véhicule de route."""
        try:
            if not isinstance(nouvelle_route, str) or not nouvelle_route:
                raise ValueError("La nouvelle route doit être une chaîne de caractères non vide.")
            
            self.route_actuelle = nouvelle_route
            self.position = 0.0
            
            # Incrémenter l'index seulement si on n'est pas à la fin de l'itinéraire
            if self.index_itineraire + 1 < len(self.itineraire):
                self.index_itineraire += 1
            else:
                # Gérer le cas où le véhicule a atteint la fin de son itinéraire
                # On peut choisir de le laisser sur la dernière route ou de signaler qu'il est "arrivé"
                print(f"Attention: Le véhicule {self.identifiant} a atteint la fin de son itinéraire.")

        except ValueError as e:
            print(f"Erreur lors du changement de route pour le véhicule {self.identifiant} : {e}")
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors du changement de route : {e}")
    def a_termine_itineraire(self):
        """Vérifie si le véhicule a terminé son itinéraire."""
        try:
            if not isinstance(self.itineraire, list):
                # Cette erreur devrait normalement être gérée à l'initialisation, mais c'est une sécurité
                raise ValueError("L'itinéraire du véhicule est mal formaté.")
            return self.index_itineraire >= len(self.itineraire)
        except ValueError as e:
            print(f"Erreur lors de la vérification de l'itinéraire du véhicule {self.identifiant} : {e}")
            return True # Considérer l'itinéraire comme terminé ou invalide en cas d'erreur
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors de la vérification de l'itinéraire : {e}")
            return True
    def __repr__(self):
        return f"Vehicule({self.identifiant}, route={self.route_actuelle}, pos={self.position:.1f}m)"