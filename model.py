from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np


# susceptible: 0
# infected: 1
# dead: 2
# recovered: 3


class AgentSchelling(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, die_rate, max_infection_time):
        super().__init__(unique_id, model)
        self.status = 0
        self.infection = 0
        self.die_rate = die_rate
        self.max_infection_time = max_infection_time

    def step(self):
        """step function"""
        self.die_or_survive()
        self.move()
        # if self.status == 0:
        self.infect()

    def move(self):
        # finds neighboring cells
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        # chooses a cell at random and moves agent
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect(self):
        """method to infect current agent when it enters a new cell"""
        # get list of agents in current cell
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        # loop through cellmates and infect each one with probability infection_rate
        for other in cellmates:
            if len(cellmates) > 1:
                # with 1-probability infection_rate skip to next cellmate
                if self.random.random() > self.model.infection_rate:
                    continue
                # if current is infected and other is susceptible infect other
                if self.status == 1 and other.status == 0:
                    other.status = 1
                    other.infection = self.model.schedule.time

    def die_or_survive(self):
        """chooses whether agent dies or survives"""
        if self.status == 1:
            # choose randomly to die or survive
            alive = np.random.choice([0, 1], p=[self.die_rate, 1-self.die_rate])
            # if chosen to die
            if alive == 0:
                # DIE
                self.model.dead_agents.append(self)
                self.model.schedule.remove(self)
            # get time infected for
            infected_time = self.model.schedule.time - self.infection
            # if infected for long enough recover otherwise stay infected
            if infected_time >= self.max_infection_time:
                self.status = 3


class Schelling(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, infection_rate, proportion_infected, die_rate, max_infection_time):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.infection_rate = infection_rate
        self.running = True
        self.susceptible = 0
        self.infected = 0
        self.recovered = 0
        self.dead = 0
        self.dead_agents = []

        for i in range(self.num_agents):
            a = AgentSchelling(i, self, die_rate, max_infection_time)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            # make some agents infected at start
            infected = np.random.choice([0, 1], p=[1 - proportion_infected, proportion_infected])
            if infected == 1:
                a.status = 1

            self.datacollector = DataCollector(
                model_reporters={"Infected": "infected",
                                 "Susceptible": "susceptible",
                                 "Recovered": "recovered",
                                 "Dead": "dead"}
            )

    def get_info(self):
        """Updates the number of infected, susceptible, recovered and dead"""

        self.infected = len([agent for agent in self.schedule.agents if agent.status == 1])
        self.susceptible = len([agent for agent in self.schedule.agents if agent.status == 0])
        self.recovered = len([agent for agent in self.schedule.agents if agent.status == 3])

        # Dead agents are removed from the scheduler so a list of dead agents is kept
        self.dead = len(self.dead_agents)
        print(f"infected: {self.infected} susceptible: {self.susceptible} recovered: {self.recovered} dead: {self.dead}")

    def step(self):
        """advance model by one step"""

        self.get_info()
        self.datacollector.collect(self)
        self.schedule.step()
