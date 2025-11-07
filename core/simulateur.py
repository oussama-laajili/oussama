from models.reseau import ReseauRoutier

class Simulateur:
    def __init__(self):
        """Initialise le simulateur avec la configuration du réseau."""
        self.reseau = ReseauRoutier()
        self.reseau.charger_config()
        self.temps_ecoule = 0.0
    def lancer_simulation(self, n_tours, delta_t):
        """Lance la simulation du trafic."""
        print(f"=== DÉBUT DE LA SIMULATION ===")
        print(f"Nombre de tours: {n_tours}, Intervalle de temps: {delta_t}s\n")
        
        for tour in range(n_tours):
            print(f"--- Tour {tour + 1} (t={self.temps_ecoule:.1f}s) ---")
            self.mettre_a_jour(delta_t)
            self.afficher_etat()
            self.temps_ecoule += delta_t
            print()
        
        print("=== FIN DE LA SIMULATION ===")
    def mettre_a_jour(self, delta_t):
        """Met à jour l'état de tous les véhicules."""
        vehicules_a_retirer = []
        
        for vehicule in self.reseau.vehicules.values():
            if vehicule.a_termine_itineraire():
                vehicules_a_retirer.append(vehicule.identifiant)
                continue
            
            route = self.reseau.routes[vehicule.route_actuelle]
            
            # Avancer le véhicule
            nouvelle_position = vehicule.avancer(delta_t, route)
            
            # Vérifier si le véhicule a atteint la fin de la route
            if nouvelle_position >= route.longueur:
                route_suivante = self.reseau.obtenir_route_suivante(vehicule)
                
                if route_suivante:
                    print(f"  → {vehicule.identifiant} passe de {vehicule.route_actuelle} à {route_suivante}")
                    # Retirer de l'ancienne route
                    route.retirer_vehicule(vehicule)
                    # Changer de route
                    vehicule.changer_de_route(route_suivante)
                    # Ajouter à la nouvelle route
                    self.reseau.routes[route_suivante].ajouter_vehicule(vehicule)
                else:
                    print(f"  → {vehicule.identifiant} a terminé son itinéraire")
                    route.retirer_vehicule(vehicule)
                    vehicules_a_retirer.append(vehicule.identifiant)
        
        # Retirer les véhicules qui ont terminé
        for vid in vehicules_a_retirer:
            del self.reseau.vehicules[vid]
    def afficher_etat(self):
        """Affiche l'état actuel de la simulation."""
        print("\nÉtat des routes:")
        for nom_route, route in self.reseau.routes.items():
            print(f"  {nom_route}: {len(route.vehicules_presents)} véhicule(s) - {route.vehicules_presents}")
        
        print("\nÉtat des véhicules:")
        for vehicule in self.reseau.vehicules.values():
            prochaine_route = self.reseau.obtenir_route_suivante(vehicule)
            print(f"  {vehicule.identifiant}: position={vehicule.position:.1f}m sur {vehicule.route_actuelle}, "
                  f"vitesse={vehicule.vitesse}m/s, prochaine={prochaine_route}")

