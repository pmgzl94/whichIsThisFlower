import numpy

def relu(input):
    return numpy.where(input > 0, input, 0)

def relu_derivative(input):
    input[input>0] = 1
    input[input<=0] = 0
    return input

# activation functions
def sigmoid(z):
    return numpy.exp(z)/(1 + numpy.exp(z))

def sigmoid_derivative(z):
    res = sigmoid(z)
    return res - numpy.power(res, 2)

def stable_softmax(X):
    exps = numpy.exp(X - numpy.max(X))
    return exps / numpy.sum(exps)

map_function = {
    "relu": (relu, relu_derivative),
    "sigmoid": (sigmoid, sigmoid_derivative)
}