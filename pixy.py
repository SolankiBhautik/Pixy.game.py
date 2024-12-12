import random
import pygame

from brain import NeuralNetwork
from config import Pixy_Size, WIDTH, HEIGHT, num_inputs, num_hidden, num_outputs, MUTATION_RATE


class Pixy:
    def __init__(self, x, y, num_inputs, num_hidden, num_outputs, screen):
        self.x = x
        self.y = y
        self.size = Pixy_Size
        # Initialize the neural network (brain) for this Pixy
        self.brain = NeuralNetwork(num_inputs, num_hidden, num_outputs)
        self.WIDTH = screen.get_width()
        self.HEIGHT =  screen.get_height()
    
    # Sensor Inputs
    def get_position_inputs(self):
        """
        Get the current x and y positions of the pixy.
        """
        return [self.x, self.y]

    def get_edge_distances(self):
        """
        Calculate distances from the pixy to the edges of the screen.
        """
        return [self.x, self.WIDTH - self.x, self.y, self.HEIGHT - self.y]

    def get_nearby_pixies(self, population, radius=50):
        """
        Find nearby pixies within a specified radius and return their relative positions.
        Limits to the closest 5 pixies (10 inputs: 2 inputs per pixy).
        """
        inputs = []
        for other in population:
            if other != self:
                distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                if distance < radius:
                    inputs.append(other.x - self.x)  # Relative x distance
                    inputs.append(other.y - self.y)  # Relative y distance
        return inputs[:10]  # Limit to 5 pixies (10 inputs)
    
    def get_sensor_inputs(self, population):
        """
        Function to collect sensor inputs for the neural network.
        This can include the pixy's position, distance to walls, distance to other pixies, etc.
        """
        inputs = []

        # Add sensor data (e.g., distance to walls, distance to other pixies, etc.)
        inputs.extend(self.get_nearby_pixies(population)) 
        inputs.extend(self.get_edge_distances())
        inputs.extend(self.get_position_inputs())

        # Here you can add additional inputs such as distance to other pixies, etc.

        return inputs

    # Fitness Function
    def fitness(self):
        """
        Calculate fitness based on the distance from the right edge of the screen.
        Fitness is normalized between 0 (far left) and 1 (right edge).
        """
        return self.x / self.WIDTH



    # Output Actions (Movement)
    def move_up(self):
        if self.y > 0:
            self.y -= 1

    def move_down(self):
        if self.y < self.HEIGHT - self.size:
            self.y += 1

    def move_left(self):
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        if self.x < self.WIDTH - self.size:
            self.x += 1

    def stay_still(self):
        pass  # No movement
    
    def perform_action(self, action_index):
        """
        Perform an action based on the output of the neural network.
        0 = Up, 1 = Down, 2 = Left, 3 = Right, 4 = Stay Still
        """
        if action_index == 0:
            self.move_up()
        elif action_index == 1:
            self.move_down()
        elif action_index == 2:
            self.move_left()
        elif action_index == 3:
            self.move_right() 
        elif action_index == 4:
            self.stay_still()

    def draw(self, screen):
        """
        Draw the pixy as a small square on the screen, with color based on its neural network (brain).
        """
        # Helper function to flatten nested lists
        def flatten(lst):
            return [item for sublist in lst for item in sublist]
        
        # Flatten all weights and biases into a single list
        brain_values = flatten(self.brain.weights_input_hidden) + flatten(self.brain.weights_hidden_output) + self.brain.bias_hidden + self.brain.bias_output
        
        # Calculate RGB color based on brain values
        avg_weight = sum(brain_values) / len(brain_values)
        
        # Normalize values between 0 and 255 for RGB
        red = int((avg_weight % 1.0) * 255)  # Red based on the average weight (normalized)
        green = int((self.brain.weights_hidden_output[0][0] % 1.0) * 255)  # Green based on first hidden-output weight
        blue = int((self.brain.bias_output[0] % 1.0) * 255)  # Blue based on first output bias
        
        # Draw the Pixy with the calculated color
        pygame.draw.rect(screen, (red, green, blue), (int(self.x), int(self.y), self.size, self.size))




    # Move Function (To be replaced by neural network actions later)
    def move(self, population):
        """
        Move function based on neural network outputs.
        """
        # Prepare the input for the neural network (sensors)
        inputs = self.get_sensor_inputs(population)
        
        # Get the output from the neural network 
        outputs = self.brain.forward_pass(inputs)
        
        # Determine the action based on the neural network's output
        action_index = outputs.index(max(outputs))  # Choose the action with the highest score
        
        # Perform the action
        self.perform_action(action_index)


    def crossover(self, other, screen):
        """
        Perform crossover between two pixies to produce a child Pixy.
        """
        child = Pixy(
            random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT),  # Random position
            num_inputs, num_hidden, num_outputs, screen  # Use the same network structure as parents
        )

        # Crossover between neural networks of self and other (parent1 and parent2)
        for i in range(len(self.brain.weights_input_hidden)):
            for j in range(len(self.brain.weights_input_hidden[0])):
                child.brain.weights_input_hidden[i][j] = random.choice([self.brain.weights_input_hidden[i][j], other.brain.weights_input_hidden[i][j]])

        for i in range(len(self.brain.weights_hidden_output)):
            for j in range(len(self.brain.weights_hidden_output[0])):
                child.brain.weights_hidden_output[i][j] = random.choice([self.brain.weights_hidden_output[i][j], other.brain.weights_hidden_output[i][j]])

        for i in range(len(self.brain.bias_hidden)):
            child.brain.bias_hidden[i] = random.choice([self.brain.bias_hidden[i], other.brain.bias_hidden[i]])

        for i in range(len(self.brain.bias_output)):
            child.brain.bias_output[i] = random.choice([self.brain.bias_output[i], other.brain.bias_output[i]])

        return child

    def mutate(self):
        """
        Perform mutation to introduce random changes to neural network weights and biases.
        """
        for i in range(len(self.brain.weights_input_hidden)):
            for j in range(len(self.brain.weights_input_hidden[0])):
                if random.random() < MUTATION_RATE:  # 1% chance to mutate
                    self.brain.weights_input_hidden[i][j] += random.uniform(-0.1, 0.1)

        for i in range(len(self.brain.weights_hidden_output)):
            for j in range(len(self.brain.weights_hidden_output[0])):
                if random.random() < MUTATION_RATE:  # 1% chance to mutate
                    self.brain.weights_hidden_output[i][j] += random.uniform(-0.1, 0.1)

        for i in range(len(self.brain.bias_hidden)):
            if random.random() < MUTATION_RATE:  # 1% chance to mutate
                self.brain.bias_hidden[i] += random.uniform(-0.1, 0.1)

        for i in range(len(self.brain.bias_output)):
            if random.random() < MUTATION_RATE:  # 1% chance to mutate
                self.brain.bias_output[i] += random.uniform(-0.1, 0.1)

