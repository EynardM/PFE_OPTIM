# Agent
BREAK_TIME = 2

# Distance
K = 2 

# Score
alpha_Q = 1
alpha_D = -1 
alpha_E = -1  
weight_Q, weight_D, weight_E = (0.25236593059936907, -3.603972606283567, -171.95842969520817)

# Hill Climbing
ITERMAX_HC = 150

# Simulated Annealing
ITERMAX_SA = 134
INITIAL_TEMPERATURE = 100
COOLING_RATE = 0.95
MINIMAL_TEMPERATURE = 0.1

METHODS = ["R", "Q", "D", "E", "HQD", "HQDE"]