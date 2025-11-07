import pytest
from core.simulateur import Simulateur
from models.vehicule import Vehicule
from models.route import Route


class TestSimulateurInitialisation:
    """Tests pour l'initialisation du simulateur."""
    
    def test_initialisation_simulateur(self):
        """Teste que le simulateur s'initialise correctement."""
        simulateur = Simulateur()
        assert simulateur.temps_ecoule == 0.0
        assert simulateur.reseau is not None
        assert isinstance(simulateur.reseau.routes, dict)
        assert isinstance(simulateur.reseau.vehicules, dict)


class TestSimulateurAvancement:
    """Tests pour l'avancement des véhicules."""
    
    def test_avancement_vehicule_simple(self, route_simple1):
        """Teste l'avancement d'un véhicule sur une route simple."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        # Créer un véhicule
        vehicule = Vehicule("V1", route_initiale="R1", position=0, vitesse=10, itineraire=["R1"])
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        # Avancer de 5 secondes
        simulateur.mettre_a_jour(5.0)
        
        # Le véhicule devrait avoir avancé de 50m (10m/s * 5s)
        assert vehicule.position == 50.0
        assert vehicule.route_actuelle == "R1"
    
    def test_vehicule_respecte_limite_vitesse(self, route_simple1):
        """Teste qu'un véhicule respecte la limite de vitesse de la route."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        # Véhicule avec vitesse supérieure à la limite
        vehicule = Vehicule("V1", route_initiale="R1", position=0, vitesse=50, itineraire=["R1"])
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        # Avancer de 1 seconde
        simulateur.mettre_a_jour(1.0)
        
        # Le véhicule devrait avoir avancé de 30m (limite de vitesse) et non 50m
        assert vehicule.position == 30.0


class TestSimulateurChangementRoute:
    """Tests pour le changement de route des véhicules."""
    
    def test_changement_route(self, route_simple1, route_simple2):
        """Teste qu'un véhicule change correctement de route."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        # Véhicule avec itinéraire de 2 routes
        vehicule = Vehicule("V1", route_initiale="R1", position=0, vitesse=30, itineraire=["R1", "R2"])
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_route(route_simple2)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        # Placer le véhicule à la fin de R1
        vehicule.position = 950.0
        
        # Avancer de 2 secondes (60m) - devrait dépasser la longueur de R1 (1000m)
        simulateur.mettre_a_jour(2.0)
        
        # Le véhicule devrait être sur R2
        assert vehicule.route_actuelle == "R2"
        assert vehicule.position < route_simple1.longueur  # Position réinitialisée
        assert vehicule.index_itineraire == 1
        assert "V1" in route_simple2.vehicules_presents
        assert "V1" not in route_simple1.vehicules_presents
    
    def test_vehicule_termine_itineraire(self, route_simple1):
        """Teste qu'un véhicule est retiré quand il termine son itinéraire."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        vehicule = Vehicule("V1", route_initiale="R1", position=950, vitesse=30, itineraire=["R1"])
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        assert "V1" in simulateur.reseau.vehicules
        
        # Avancer suffisamment pour terminer la route
        simulateur.mettre_a_jour(2.0)
        
        # Le véhicule devrait être retiré
        assert "V1" not in simulateur.reseau.vehicules
        assert "V1" not in route_simple1.vehicules_presents


class TestSimulateurItineraireLong:
    """Tests pour les itinéraires avec plusieurs routes."""
    
    def test_itineraire_trois_routes(self, route_simple1, route_simple2, route_simple3):
        """Teste un véhicule avec un itinéraire de 3 routes."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        vehicule = Vehicule("V1", route_initiale="R1", position=0, vitesse=30, 
                           itineraire=["R1", "R2", "R3"])
        
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_route(route_simple2)
        simulateur.reseau.ajouter_route(route_simple3)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        # Phase 1: Sur R1
        assert vehicule.route_actuelle == "R1"
        assert vehicule.index_itineraire == 0
        
        # Avancer jusqu'à la fin de R1 (1000m / 30m/s = 33.33s)
        for _ in range(35):
            simulateur.mettre_a_jour(1.0)
            if vehicule.route_actuelle == "R2":
                break
        
        # Phase 2: Sur R2
        assert vehicule.route_actuelle == "R2"
        assert vehicule.index_itineraire == 1
        
        # Avancer jusqu'à la fin de R2 (2000m / 30m/s = 66.67s)
        for _ in range(70):
            simulateur.mettre_a_jour(1.0)
            if vehicule.route_actuelle == "R3":
                break
        
        # Phase 3: Sur R3
        assert vehicule.route_actuelle == "R3"
        assert vehicule.index_itineraire == 2


class TestSimulateurPlusieursVehicules:
    """Tests avec plusieurs véhicules."""
    
    def test_deux_vehicules_meme_route(self, route_simple1):
        """Teste deux véhicules sur la même route."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        v1 = Vehicule("V1", route_initiale="R1", position=0, vitesse=20, itineraire=["R1"])
        v2 = Vehicule("V2", route_initiale="R1", position=100, vitesse=15, itineraire=["R1"])
        
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_vehicule(v1)
        simulateur.reseau.ajouter_vehicule(v2)
        
        assert len(route_simple1.vehicules_presents) == 2
        
        # Avancer de 5 secondes
        simulateur.mettre_a_jour(5.0)
        
        # V1: 20m/s * 5s = 100m
        # V2: 15m/s * 5s = 75m, position totale = 175m
        assert v1.position == 100.0
        assert v2.position == 175.0
    
    def test_vehicules_routes_differentes(self, route_simple1, route_simple2):
        """Teste des véhicules sur des routes différentes."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        v1 = Vehicule("V1", route_initiale="R1", position=0, vitesse=20, itineraire=["R1"])
        v2 = Vehicule("V2", route_initiale="R2", position=0, vitesse=40, itineraire=["R2"])
        
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_route(route_simple2)
        simulateur.reseau.ajouter_vehicule(v1)
        simulateur.reseau.ajouter_vehicule(v2)
        
        assert len(simulateur.reseau.vehicules) == 2
        assert "V1" in route_simple1.vehicules_presents
        assert "V2" in route_simple2.vehicules_presents
        
        simulateur.mettre_a_jour(5.0)
        
        assert v1.position == 100.0  # 20m/s * 5s
        assert v2.position == 200.0  # 40m/s * 5s


class TestSimulateurLancerSimulation:
    """Tests pour la méthode lancer_simulation."""
    
    def test_lancer_simulation_incremente_temps(self, route_simple1):
        """Teste que le temps s'incrémente correctement."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        vehicule = Vehicule("V1", route_initiale="R1", position=0, vitesse=10, itineraire=["R1"])
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        assert simulateur.temps_ecoule == 0.0
        
        # Lancer simulation de 3 tours avec delta_t=2.0
        simulateur.lancer_simulation(n_tours=3, delta_t=2.0)
        
        # Le temps devrait être 3 * 2.0 = 6.0 secondes
        assert simulateur.temps_ecoule == 6.0
    
    def test_lancer_simulation_sans_vehicule(self, route_simple1):
        """Teste une simulation sans véhicule."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        simulateur.reseau.ajouter_route(route_simple1)
        
        # Ne devrait pas lever d'erreur
        simulateur.lancer_simulation(n_tours=2, delta_t=1.0)
        
        assert simulateur.temps_ecoule == 2.0
        assert len(simulateur.reseau.vehicules) == 0


class TestSimulateurCasLimites:
    """Tests pour les cas limites."""
    
    def test_delta_t_zero(self, route_simple1):
        """Teste avec un delta_t de zéro."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        vehicule = Vehicule("V1", route_initiale="R1", position=0, vitesse=10, itineraire=["R1"])
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        position_initiale = vehicule.position
        simulateur.mettre_a_jour(0.0)
        
        # La position ne devrait pas changer
        assert vehicule.position == position_initiale
    
    def test_vehicule_vitesse_nulle(self, route_simple1):
        """Teste un véhicule avec une vitesse nulle."""
        simulateur = Simulateur()
        simulateur.reseau.routes = {}
        simulateur.reseau.vehicules = {}
        
        vehicule = Vehicule("V1", route_initiale="R1", position=0, vitesse=0, itineraire=["R1"])
        simulateur.reseau.ajouter_route(route_simple1)
        simulateur.reseau.ajouter_vehicule(vehicule)
        
        simulateur.mettre_a_jour(5.0)
        
        # Le véhicule ne devrait pas bouger
        assert vehicule.position == 0.0