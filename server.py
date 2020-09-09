from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

# LONDON STATS
conf_cases = 27354
deaths = 6079
pop = 8982000
size = 1527 * (10**6)
pop_density = 5701/1000000

# PARAMETERS FOR MODEL
INFECTION_RATE = 0.5
WIDTH = 200
HEIGHT = 200
NUMBER_OF_AGENTS = round(pop_density * WIDTH * HEIGHT * 2)
PROPORTION_INFECTED = 0.1
MAX_INFECTION_TIME = 14
DIE_RATE = (deaths/conf_cases) / MAX_INFECTION_TIME


# Sets the colours and sizes that the different agent states will be on the grid
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                "Filled": "true",
                "r": 0.5}
    if agent.status == 1:
        portrayal['Color'] = 'red'
        portrayal['Layer'] = 0
    elif agent.status == 0:
        portrayal['Color'] = 'orange'
        portrayal['Layer'] = 1
    elif agent.status == 3:
        portrayal['Color'] = 'green'
        portrayal['Layer'] = 2
    else:
        portrayal['Color'] = 'grey'
        portrayal['Layer'] = 3

    return portrayal


# Creates a grid
grid = CanvasGrid(agent_portrayal, WIDTH, HEIGHT, 1000, 1000)

# Creates a chart using data collector data
chart = ChartModule([{"Label": "Infected",
                      "Color": "red"},
                     {"Label": "Susceptible",
                      "Color": "orange"},
                     {"Label": "Recovered",
                      "Color": "green"},
                     {"Label": "Dead",
                      "Color": "black"}
                     ],
                    data_collector_name='datacollector'
                    )

# Establishes server using model

server = ModularServer(
    Schelling,
    [grid, chart],
    "SIR",
    {"N": NUMBER_OF_AGENTS, "width": WIDTH, "height": HEIGHT, "infection_rate": INFECTION_RATE,
     "proportion_infected": PROPORTION_INFECTED, "die_rate": DIE_RATE, "max_infection_time": MAX_INFECTION_TIME}
)

server.port = 8521
server.launch()
