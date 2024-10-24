import random
from pixy import Pixy
from config import POPULATION_SIZE, num_inputs, num_hidden, num_outputs, FRAMES_PER_GENERATION

class Simulation:
    def __init__(self, screen):
        self.population = []
        self.generation = 1
        self.frame = 0
        self.paused = False
        self.running = True
        self.reset(screen)
        self.WIDTH = screen.get_width()
        self.HEIGHT =  screen.get_height() 
        self.screen = screen
        self.walls = []  # Store all collision walls
        

    def reset(self, screen):
        """Reset simulation to initial state."""
        self.population = [Pixy(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), num_inputs, num_hidden, num_outputs, screen)
                           for _ in range(POPULATION_SIZE)]
        self.walls = [CollisionWall((random.randint(0, screen.get_width()), random.randint(0, screen.get_height())),
                            (random.randint(0, screen.get_width()), random.randint(0, screen.get_height())))
                    for _ in range(2)]  # 2 random walls initially
        self.generation = 1
        self.frame = 0

    def add_wall(self, start_pos, end_pos):
            """Add a user-defined wall."""
            self.walls.append(CollisionWall(start_pos, end_pos))
            
    def start(self):
        """Start the simulation."""
        self.running = True
        self.paused = False

    def pause(self):
        """Pause the simulation."""
        if self.running:
            self.paused = not self.paused

    def stop(self):
        """Stop the simulation."""
        self.running = False
    
    def next_generation(self):
        """Manually trigger the next generation."""
        self.new_generation()

    def update(self):
        """Update the simulation (move pixies, handle generations)."""
        if self.running and not self.paused:
            self.frame += 1
            for pixy in self.population:
                pixy.move(self.population)

            # Check if the generation ends
            if self.frame >= FRAMES_PER_GENERATION:
                self.new_generation()

    def new_generation(self):
        """Handle generation transition."""
        selected_pixies = self.selection()
        self.population = [self.crossover_and_mutate(random.choice(selected_pixies), random.choice(selected_pixies)) 
                           for _ in range(POPULATION_SIZE)]
        self.frame = 0
        self.generation += 1

    def selection(self):
        """Select fittest pixies based on fitness."""
        self.population.sort(key=lambda pixy: pixy.fitness())
        return self.population[:int(POPULATION_SIZE / 4)]

    def crossover_and_mutate(self, parent1, parent2):
        """Create a new child through crossover and mutation."""
        child = parent1.crossover(parent2, self.screen)
        child.mutate()
        return child
