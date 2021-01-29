# example from here: https://datascience.stackexchange.com/questions/27506/back-propagation-in-cnn
import fcnetwork
import conv
import pool
from tensor.Tensor import TensorFileManager

import numpy
import os

pathdir = "./tensorfiles"
filename1 = "convtest"

input = numpy.array([(0.51, 0.9, 0.88, 0.84, 0.05), 
              (0.4, 0.62, 0.22, 0.59, 0.1), 
              (0.11, 0.2, 0.74, 0.33, 0.14), 
              (0.47, 0.01, 0.85, 0.7, 0.09),
              (0.76, 0.19, 0.72, 0.17, 0.57)])

filter = numpy.array([[-0.13,0.15], [-0.51, 0.62]])
biases = numpy.zeros((1,))

if not os.path.exists(os.path.join(pathdir, filename1 + ".bs1.npy")):
    tm = TensorFileManager("./tensorfiles")
    tm.save("convtest.bs1", biases)
    tm.save("convtest.ws1", filter)


l1 = conv.ConvLayer(load_path=filename1, pool=pool.PoolLayer())

res1 = l1.compute(input)

print(res1)

filename2 = "networktest"

############# no need to build a fcn actually
ws = numpy.array([[0.61,0.82,0.96,-1], [0.02, -0.5, 0.23, 0.17]])
# biases = numpy.zeros((2,))

# if not os.path.exists(os.path.join(pathdir, filename2 + ".bs1.npy")):
#     tm = TensorFileManager("./tensorfiles")
#     tm.save("networktest.bs1", biases)
#     tm.save("networktest.ws1", ws)


# l2 = fcnetwork.FCLayer(arch=[4, 2], transfer_learning_file=filename2)

# l2.learn(res1.flatten(), numpy.array([1, 0]))
# delta = l2.getLastDelta()
#############

prev_delta = numpy.array([0.25, -0.15]) #delta from the link
delta = numpy.dot(prev_delta, ws)

# print(f"delta = {delta}")

# derivativ = fcnetwork.sigmoid_derivative([[0, 0, 0.27, 0], [0, 0.31, 0, 0], [0, 0.61, 0, 0], [0, 0, 0, 0.19]])

# as the output of maxpooling calls sigmoid, we call its derivative
# derivativ = fcnetwork.sigmoid_derivative(numpy.array([0.27, 0.31, 0.61, 0.19]))
derivativ = fcnetwork.sigmoid_derivative(numpy.array([0.31, 0.27, 0.61, 0.19]))
delta = delta*derivativ
print(f"delta sigmoid{delta}")

# print(f"delta before={delta}")
# print(f"delta before={delta.shape}") #(4,)

#get the delta
#reshape the max_derivative the gradient are only those who are passed through the max pools
max_derivativ = numpy.array([[0, 0, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
print(max_derivativ.shape)

# print(max_derivativ)

#reshape the delta to place the gradient in the output of the conv layer (featuremap)
delta = delta.reshape(2, 2)

delta = delta.repeat(2, axis=0).repeat(2, axis=1) #dupplicate of pool_size side

delta = delta * max_derivativ

print(f"delta = {delta}")

# res = (max_derivativ.T * delta).T #do not work in all cases: try to change the max position in the sub square of 2x2

#get nabla shared weights
outputshape = (4, 4, 2, 2) #size of the output, size of the region a

len_line, len_nb = input.strides

strides = (len_line*1, len_nb*1, len_line, len_nb)

view = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=strides)
# print(f"view = \n{view}")
# print(f"input = \n{input}")

#res in raw because above the res is badly computed
res = numpy.array(
                [(0, 0, 0.0686, 0), 
                (0, 0.0364, 0, 0), 
                (0, 0.0467, 0, 0), 
                (0, 0, 0, -0.0681)])

#get true value with delta

print(numpy.tensordot(delta, view))