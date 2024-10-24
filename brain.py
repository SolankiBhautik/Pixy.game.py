import random
import math

class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden, num_outputs):        
        # Initialize weights for input to hidden layer
        self.weights_input_hidden = [[random.uniform(-0.5, 0.5) for _ in range(num_hidden)] for _ in range(num_inputs)]
        # Initialize weights for hidden to output layer
        self.weights_hidden_output = [[random.uniform(-0.5, 0.5) for _ in range(num_outputs)] for _ in range(num_hidden)]
        
        # Initialize biases for hidden and output layers
        self.bias_hidden = [random.uniform(-1, 1) for _ in range(num_hidden)]
        self.bias_output = [random.uniform(-1, 1) for _ in range(num_outputs)]

    def sigmoid(self, x):
        """
        Sigmoid activation function with input clipping to avoid overflow.
        """
        # Clip the input to avoid overflow in exp
        if x < -700:
            x = -700  # Avoid too large negative numbers
        elif x > 700:
            x = 700   # Avoid too large positive numbers
        return 1 / (1 + math.exp(-x))


    def relu(self, x):
        """
        ReLU activation function.
        """
        return max(0, x)

    def dot_product(self, inputs, weights):
        """
        Perform dot product between input vector and weight matrix.
        """
        return [sum(i * w for i, w in zip(inputs, weight)) for weight in weights]

    def forward_pass(self, inputs):
        """
        Perform a forward pass through the neural network.
        """
        # Input to hidden layer
        hidden_layer = self.dot_product(inputs, self.weights_input_hidden)
        # Apply ReLU activation function to hidden layer
        hidden_layer = [self.relu(h + b) for h, b in zip(hidden_layer, self.bias_hidden)]

        # Hidden to output layer
        output_layer = self.dot_product(hidden_layer, self.weights_hidden_output)
        # Apply sigmoid activation function to output layer
        output_layer = [self.sigmoid(o + b) for o, b in zip(output_layer, self.bias_output)]

        return output_layer
