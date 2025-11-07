import core.simulateur as simulateur
import cProfile




simulateur = simulateur.Simulateur()
cProfile.run('simulateur.lancer_simulation(n_tours=3, delta_t=10.0)')

#simulateur.lancer_simulation(n_tours=3, delta_t=10.0)
