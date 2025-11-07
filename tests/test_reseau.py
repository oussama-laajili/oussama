def test_reseau_contient_route(reseau_simple, route_simple1):
    # Suppose ReseauRoutier exposes .routes or an accessor
    assert route_simple1 == reseau_simple.routes[route_simple1.nom]
