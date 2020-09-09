How my model works:

One type of simulation is an agent-based model. My model used a 200x200 grid with 456 agents inside. To make 
the model as specific as possible for coronavirus each square in the grid represents 2m x 2m and the number of 
agents was calculated using the population density of London (using population and size). I also calculated 
the probability of dying given that someone has the virus using London’s COVID statistics and set the maximum 
infection time to 14 time steps representing 2 weeks. Each agent has a location in the grid, a state 
(susceptible, infected, recovered or dead) and a maximum time it can be infected for before recovering. At the 
beginning, all the agents are randomly allocated a position on the grid and a certain proportion begin as 
infected. As the model runs each agent randomly moves into a neighbouring cell at every time step. If a 
susceptible agent is in a cell with an infected agent, the susceptible agent is infected with a certain 
probability called the infection rate. At every time step, if an agent is infected, it dies with probability 
called the death rate however if it has been infected for longer that the maximum infection time the state of 
the agent is changed to recovered.

Run server.py to run the model 
Model parameters set as constants at top of server.py
