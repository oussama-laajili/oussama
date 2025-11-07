import pytest
from models.route import Route
from models.vehicule import Vehicule
from models.reseau import ReseauRoutier

@pytest.fixture
def route_simple1():
    return Route("R1", longueur=1000, limite_de_vitesse=30)

@pytest.fixture
def route_simple2():
    return Route("R2", longueur=2000, limite_de_vitesse=60)

@pytest.fixture
def route_simple3():
    return Route("R3", longueur=3000, limite_de_vitesse=90)

@pytest.fixture
def vehicule_exemple(route_simple1):
    return Vehicule("V1", route_initiale=route_simple1, position=0, vitesse=10, itineraire=["R1"])

@pytest.fixture
def reseau_simple(route_simple1, vehicule_exemple):
    reseau = ReseauRoutier()
    reseau.ajouter_route(route_simple1)
    route_simple1.ajouter_vehicule(vehicule_exemple)
    return reseau