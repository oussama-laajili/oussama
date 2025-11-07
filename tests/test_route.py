def test_ajout_vehicule_dans_route(route_simple1, vehicule_exemple):
    route = route_simple1
    v = vehicule_exemple

    route.ajouter_vehicule(v)
    assert v.identifiant in route.vehicules_presents  # or route.get_vehicules()
    assert v.route_actuelle is route
