import numpy

def relu(input):
    return numpy.where(input > 0, input, 0)

def relu_derivative(input):
    return numpy.where(input > 0, input / input, 0)

# activation functions
def sigmoid(z):
    # print(f"z = {z.shape}")
    return numpy.exp(z)/(1 + numpy.exp(z))

def sigmoid_derivative(z):
    res = sigmoid(z)
    return res - numpy.power(res, 2)

map_function = {
    "relu": (relu, relu_derivative),
    "sigmoid": (sigmoid, sigmoid_derivative)
}