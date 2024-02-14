K = 2 # Pour se rapprocher de la réalité
weight_Q = 1 # Poids pour maximiser Q
weight_D = -1 # Poids pour minimiser d
weight_E = -1  # Poids pour minimiser u
BREAK_TIME = 2

ITERMAX = 20

METHODS = ["R", "Q", "D", "E", "HQD", "HQDE"]