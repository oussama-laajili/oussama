import math
import pytest

def test_vehicule_initial(vehicule_exemple, route_simple1):
    assert vehicule_exemple.identifiant == "V1"
    assert vehicule_exemple.route_actuelle is route_simple1
    assert vehicule_exemple.position == 0
    assert vehicule_exemple.vitesse == 10

def test_vehicule_deplacement_simple(vehicule_exemple, route_simple1):
    vehicule_exemple.avancer(1.0, route_simple1)
    assert math.isclose(vehicule_exemple.position, 10.0)


def test_vehicule_ne_depasse_pas_longueur_route(vehicule_exemple, route_simple1):
    vehicule_exemple.vitesse = 5000
    vehicule_exemple.avancer(1.0, route_simple1)
    assert vehicule_exemple.position <= route_simple1.longueur
