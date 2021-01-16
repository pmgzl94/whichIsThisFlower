from layer import LayerInterface
from tensor.Tensor import TensorFileManager
import pool
from activation_functions import map_function

import numpy
import functools
import pickle
import sys
import os

# image getdata return flatter container
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.getdata

# for image.show
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.load

# for as_strided
# https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.as_strided.html


class ConvLayer(LayerInterface):
    # find way to save filters 
    # if you precise padding, you will only get a padding of 1

    def __init__(self, load_path=None, padding=0, nb_filters=1, filtershape=(3, 2, 2), stride_length=1, pool=None, activation_function='relu', ishape=None):
        self.padding = padding
        self.stride_len = stride_length
        self.activation_function_tag = activation_function
        
        if activation_function != None:
            self.activation_function, self.derivative_activation = map_function[activation_function]
            
        self.pool = pool

        self.lastRes = None
        self.lastInput = None

        self.z = None

        self.sum_of_nabla_w = numpy.zeros(filtershape)

        if load_path is not None:
            self.load(load_path)
        
        if load_path is None:
            self.fshape = filtershape
            self.nb_filters = nb_filters
            
            if nb_filters > 1:
                shape = list(filtershape)
                shape.insert(0, nb_filters)
                self.filters = numpy.ndarray(shape)
                self.biases = numpy.ndarray((nb_filters,))
            else:
                # self.filters = numpy.ndarray(filtershape)
                #he intialization

                nb_neurons = functools.reduce(lambda a,b : a*b,list(ishape))

                self.filters = numpy.random.rand(*filtershape)
                # if filtershape == (96, 3, 7, 7):
                #     print(f"filters = {self.filters}")
                #     TensorFileManager().save("filter1", self.filters)
                # self.filters = numpy.random.uniform(-1, 1, filtershape)

                self.filters = numpy.random.randn(*filtershape) * numpy.sqrt(2/nb_neurons)

                # self.biases = numpy.ndarray((nb_filters,))
                self.biases = numpy.random.uniform(-1, 1, (nb_filters,))

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
            
            output = numpy.tensordot(new_input, self.filters, axes=[[2, 3],[0, 1]]) + self.biases
            return output

    #do not forget activation function
    def compute(self, input, learn=False):
        
        ## apply padding
        if self.padding != 0:
            # input = numpy.pad(input, self.padding)
            input = numpy.pad(input, ((0, 0), (1, 1), (1, 1)))
            # print(f"input shape = {input.shape}")

        featuremaps = self.slidingWindow(input)

        # print(featuremaps.shape)

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
        return "Conv"
    
    def learn(self, delta):
        print(f"conv learn")
        # reshape delta if it come from classifier
        if len(delta.shape) == 1:
            delta = delta.reshape(self.output_shape)

        # get activation function derivative
        if self.activation_function != None:
            delta = delta * self.derivative_activation(self.z)

        if self.pool != None:
            delta = pool.helper_pool_backprop(delta, self.pool)
        
        
        #have to save the weights to apply sgd
        self.nabla_w = numpy.tensordot(delta, self.slicedInput)

        self.sumUpNablas(self.nabla_w)

        #do something with nabla_b

        # print(delta.shape)

        print(delta.shape)

        self.lastDelta = delta

    def getLastDelta(self):
        # inspired by this link: https://medium.com/@pavisj/convolutions-and-backpropagations-46026a8f5d2c

        if len(self.lastDelta.shape) == 3:
            h = self.filters.shape[-2] - self.stride_len
            w = self.filters.shape[-1] - self.stride_len
            delta = numpy.pad(self.lastDelta, ((0, 0), (h, h), (w, w)))
        else:
            delta = numpy.pad(self.lastDelta, 1)

        # print(f"delta shape = {delta.shape}")

        flipped_filter = numpy.flip(self.filters)

        #add filter dimensions
        outputshape   = [flipped_filter.shape[-2], flipped_filter.shape[-1]]
        outputstrides = [delta.strides[-2], delta.strides[-1]]

        #add input dimension
        outputshape.insert(0, 1 + (delta.shape[-1] - flipped_filter.shape[-1]) // self.stride_len)
        outputshape.insert(0, 1 + (delta.shape[-2] - flipped_filter.shape[-2]) // self.stride_len)
        
        outputstrides.insert(0, delta.strides[-1]*self.stride_len)
        outputstrides.insert(0, delta.strides[-2]*self.stride_len)

        if len(delta.shape) == 3: #if multiple filter
            #only handle with depth and multiple filter here

            outputshape.insert(2, delta.shape[-3])
            outputstrides.insert(2, delta.strides[-3])
            #have to precise that there is multiple filter

            resized_delta = numpy.lib.stride_tricks.as_strided(delta, shape=outputshape, strides=outputstrides)
            
            filter_axes = [len(flipped_filter.shape) - 3, len(flipped_filter.shape) - 2, len(flipped_filter.shape) - 1]
            delta_axes = [len(resized_delta.shape) - 3, len(resized_delta.shape) - 2, len(resized_delta.shape) - 1]

            # print(f"shapes = {resized_delta.shape} {flipped_filter.shape}")
            # print(f"d_axes = {delta_axes}, f_axes = {filter_axes}")
            flipped_filter = flipped_filter.transpose(1, 0, 2, 3)

            next_delta = numpy.tensordot(resized_delta, flipped_filter, axes=[delta_axes, filter_axes])
            print(f"next delta .shape = {next_delta.transpose(2, 0, 1).shape}")
            return next_delta.transpose(2, 0, 1)
        else: #if only one filter...
            
            #print(f"delta = \n{self.lastDelta}")
            resized_delta = numpy.lib.stride_tricks.as_strided(delta, shape=outputshape, strides=outputstrides)
            
            filter_axes = [len(flipped_filter.shape) - 2, len(flipped_filter.shape) - 1]
            delta_axes = [len(resized_delta.shape) - 2, len(resized_delta.shape) - 1]
            
            next_delta = numpy.tensordot(resized_delta, flipped_filter, axes=[delta_axes, filter_axes])

            return (next_delta)
        
    def save(self, filename): # not only weights and biases
        
        tm = TensorFileManager("./tensorfiles")
        tm.save(filename + ".ws1", self.filters)
        tm.save(filename + ".bs1", self.biases)

        #save params
        params = {}
        if self.pool != None:
            params["pool"] = self.pool.getParams()

        params["padding"] = self.padding
        params["stride_length"] = self.stride_len
        params["activation_function"] = self.activation_function_tag

        dir = "./tensorfiles"
        with open(dir + "/" + filename + ".params", "bw") as f:
            pickle.dump(params, f)
    
    def load(self, filename):
        dir = "./tensorfiles"

        tm = TensorFileManager(dir)
        self.filters = tm.load(filename + ".ws1")
        self.biases = tm.load(filename + ".bs1")
        self.nb_filters = self.filters.shape[0]
        self.fshape = tuple(self.filters.shape[1:],)

        if not os.path.exists(os.path.join(dir, filename + ".params")):
            print(f'Carefull: no params in {dir + "/" + filename + ".params"}', file=sys.stderr)
        else:
            params = {}
            with open(dir + "/" + filename + ".params", "br") as f:
                params = pickle.load(f)
                ## set conv params
                self.padding = params["padding"]
                self.stride_len = params["stride_length"]
                if params.get("activation_function", None) is not None:
                    self.activation_function_tag = params["activation_function"]
                    self.activation_function, self.derivative_activation = map_function[self.activation_function_tag]
                
                ## set pool params
                if (pool_param := params.get("pool", None)) is not None:
                    self.pool = pool.PoolLayer(pool_size=pool_param["pool_size"],\
                    pad=pool_param["padding"], stride_length=pool_param["stride_length"], type=pool_param["type"])

    def getNablaW(self):
        return self.nabla_w

    def sumUpNablas(self, nabla_w):
        self.sum_of_nabla_w += nabla_w

    def modify_weights(self, learning_rate, batch_size):

        self.filters -= learning_rate/batch_size * self.sum_of_nabla_w

        self.sum_of_nabla_w = numpy.zeros(self.filters.shape)
        

        

        
        