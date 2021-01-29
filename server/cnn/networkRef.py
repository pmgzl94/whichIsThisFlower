# %load network.py

"""
network.py
~~~~~~~~~~
IT WORKS

A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network.  Gradients are calculated
using backpropagation.  Note that I have focused on making the code
simple, easily readable, and easily modifiable.  It is not optimized,
and omits many desirable features.
"""

#### Libraries
# Standard library
import random

# Third-party libraries
import numpy as np

import tensor

class Network(object):

    def __init__(self, sizes, impvt = False, biases = None, weights = None):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        self.num_layers = len(sizes)
        self.sizes = sizes

        tm = tensor.Tensor.TensorFileManager()

        if biases:
            self.biases = biases
        else:
            self.biases = [np.random.randn(y, 1) for y in sizes[1:]]

        if weights:
            self.weights = weights
        else:
            self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

        tm.saveNet("compare", self.weights, self.biases)

        self.impvt = impvt

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent.  The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs and the desired
        outputs.  The other non-optional parameters are
        self-explanatory.  If ``test_data`` is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out.  This is useful for
        tracking progress, but slows things down substantially."""

        training_data = list(training_data)
        #1 unit of training_data is an array of float
        n = len(training_data)

        if test_data:
            test_data = list(test_data)
            n_test = len(test_data)

        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                 #update weight and biases
                if self.impvt:
                    self.effectiv_update_mini_batch(mini_batch, eta)
                else:
                    self.update_mini_batch(mini_batch, eta)
            if test_data:
                print("Epoch {} : {} / {}".format(j,self.evaluate(test_data),n_test));
            else:
                print("Epoch {} complete".format(j))

    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # x = array of float corresponding of the hue
        # y = expected result aka for 6 we get: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]
        return nabla_w, nabla_b

    def getWeightsAndBiases(self):
        return self.weights, self.biases
    

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        #first application of backward algorithm on the last layer (output layer)
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        #apply the result of delta on preceeding layers
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose()) #multiply with a of (l-1)
        return (nabla_b, nabla_w)

    def effectiv_update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
       
        nabla_b, nabla_w = self.effectiv_backprop(mini_batch)

        sum_nabla_b = [np.sum(b, axis=0) for b in nabla_b]
        sum_nabla_w = [np.sum(w, axis=0) for w in nabla_w]
        self.weights = [w-(eta/len(mini_batch))*nw.T
                        for w, nw in zip(self.weights, sum_nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb.T
                       for b, nb in zip(self.biases, sum_nabla_b)]

    def effectiv_backprop(self, mini_batch):
        

        nabla_b = [np.zeros((len(mini_batch), b.shape[0], b.shape[1])) for b in self.biases]
        nabla_w = [np.zeros((len(mini_batch), w.shape[0], w.shape[1])) for w in self.weights]

        activations = [np.array([tr_input.T for tr_input, expected_val in mini_batch])]
        y = np.array([expected_val.T for tr_input, expected_val in mini_batch])

        #  = activations[0] =activations[0].transpose()
        activation = activations[0]
        zs = []

        for b, w in zip(self.biases, self.weights):
            z = np.dot(activation, w.T) + b.T
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = delta * activations[-2].transpose(0, 2, 1)

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(delta, self.weights[-l+1]) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = delta * activations[-l-1].transpose(0, 2, 1)   #multiply with a of (l-1)
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)

    #these method are implemented to test weight's and biases's updates
    def get_biases(self):
        return self.biases
    def get_weights(self):
        return self.weights

#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
