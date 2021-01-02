# import num∞py as np
import numpy
from layer import LayerInterface
from tensor.Tensor import TensorFileManager
import pool
from activation_functions import map_function
# image getdata return flatter container
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.getdata

# for image.show
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.load

# for as_strided
# https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.as_strided.html


class ConvLayer(LayerInterface):
    # find way to save and load filters 
    # handle padding but not now, specify size

    def __init__(self, load_path=None, padding=0, nb_filters=1, filtershape=(3, 2, 2), stride_length=1, pool=None, activation_function='relu'):
        self.padding = padding
        self.stride_len = stride_length
        
        if activation_function != None:
            self.activation_function, self.derivative_activation = map_function[activation_function]
            
        self.pool = pool

        self.lastRes = None
        self.lastInput = None

        self.z = None

        if load_path is not None:
            tm = TensorFileManager("./tensorfiles")
            self.filters = tm.load(load_path + ".ws1")
            self.biases = tm.load(load_path + ".bs1")
            self.nb_filters = self.filters.shape[0]
            self.fshape = tuple(self.filters.shape[1:])
        
        if load_path is None:
            self.fshape = filtershape
            self.nb_filters = nb_filters
            
            if nb_filters > 1:
                shape = list(filtershape)
                shape.insert(0, nb_filters)
                self.filters = numpy.ndarray(shape)
                self.biases = numpy.ndarray((nb_filters,))
            else:
                self.filters = numpy.ndarray(filtershape)
                self.biases = numpy.ndarray((nb_filters,))
        
    # def enhancedSlidingWindow(self, input):
    #     #for 2d input and only one filter
    #     outputshape = ((input.shape[0] - self.fshape[0] + 1) // self.stride_len, (input.shape[1] - self.fshape[1] + 1) // self.stride_len, self.fshape[0], self.fshape[1])

    #     len_per_row ,len_per_number = input.strides

    #     strides = (len_per_row * self.stride_len, len_per_number * self.stride_len, len_per_row, len_per_number)

    #     output = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=strides)

    #     #for 3d input ...
    #     return output
    
    def slidingWindow(self, input):
        filtershape = list(self.filters.shape)
        inputshape = list(input.shape)
        s = self.stride_len

        strideInput = input.strides

        std_outputshape = [1+(inputshape[-2]-filtershape[-2])//s, 1+(inputshape[-1]-filtershape[-1])//s]
        output_stride = [s*strideInput[-2], s*strideInput[-1]]

        if len(inputshape) == 3: #if 3d
            
            # add 3 dimension
            std_outputshape.append(inputshape[0])
            output_stride.append(strideInput[0])

            #add filter size
            std_outputshape.append(filtershape[-2])
            std_outputshape.append(filtershape[-1])

            output_stride.append(strideInput[-2])
            output_stride.append(strideInput[-1])
            
            new_input = numpy.lib.stride_tricks.as_strided(input, shape=std_outputshape, strides=output_stride)
            
            self.slicedInput = new_input #used to compute with delta

            output = numpy.tensordot(new_input, self.filters, axes=[[2, 3, 4],[1, 2, 3]]) + self.biases
            output = output.transpose(2, 0, 1)
            return output

        elif len(inputshape) == 2: #if 2d
            std_outputshape.append(filtershape[-2])
            std_outputshape.append(filtershape[-1])

            output_stride.append(strideInput[-2])
            output_stride.append(strideInput[-1])

            new_input = numpy.lib.stride_tricks.as_strided(input, shape=std_outputshape, strides=output_stride) + self.biases

            self.slicedInput = new_input
            # print(std_outputshape)
            # print(self.filters.shape)

            output = numpy.tensordot(new_input, self.filters, axes=[[2, 3],[0, 1]]) + self.biases
            # output = numpy.tensordot(new_input, self.filters, axes=[[2, 3],[1, 2, 3]]) + self.biases
            # print(output.shape)
            return output

    #do not forget activation function
    def compute(self, input):
        
        ## apply padding
        if self.padding != 0:
            input = numpy.pad(input, self.padding)
        
        featuremaps = self.slidingWindow(input)

        if self.pool is not None:
            res = self.pool.compute(featuremaps)
            self.z = res
            
            if self.activation_function != None:
                res = self.activation_function(self.z)
                self.output_shape = res.shape
                return res
            
            self.output_shape = res.shape
            return res

        self.z = featuremaps

        if self.activation_function != None:
            res = self.activation_function(self.z)
            self.output_shape = res.shape
            return res
        self.output_shape = self.z.shape
        return self.z

    def getType(self):
        return "FeatureMap"
    
    def learn(self, delta):
        # in the example it is: maxpool, then sigmoid

        #reshape delta if it come from classifier
        if len(delta.shape) == 1:
            delta = delta.reshape(self.output_shape)

        # get activation function derivative
        if self.activation_function != None:
            delta = delta * self.derivative_activation(self.z)

        if self.pool != None:
            delta = pool.helper_pool_backprop(delta, self.pool)
        
        #have to save the weights to apply sgd
        self.nabla_w = numpy.tensordot(delta, self.slicedInput)
        # print(self.nabla_w)
        #do something with nabla_b

        self.lastDelta = delta

    def getLastDelta(self):
        return np.dot(self.lastDelta, self.filters)
    
    def getNablaW(self):
        return self.nabla_w
