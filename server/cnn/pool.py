from layer import LayerInterface
import numpy

# def max_pool_derivative(input):

def helper_pool_backprop(delta, pool_layer):
    derivative = pool_layer.get_derivative()
    pool_size = pool_layer.get_pool_size()
    
    # if len(delta.shape) > 1:
    #     return delta * derivative
    # else:
    # delta = delta.reshape(pool_size)
    before_last, last = (len(delta.shape) - 2, len(delta.shape) - 1)

    delta = delta.repeat(pool_size[-2], axis=before_last).repeat(pool_size[-1], axis=last)
    
    return delta * derivative

class PoolLayer(LayerInterface):
    # if you precise padding, you will only get a padding of 1

    def __init__(self, pad=0, pool_size=(2, 2), stride_length=2, type='max'):
        self.pool_size = pool_size
        self.stride_len = stride_length
        self.pad = pad

    def build_derivative(self, input, resized_input, strides, outputshape):
        
        if len(input.shape) == 3: 
            o1 = numpy.zeros_like(input)

            o1 = numpy.lib.stride_tricks.as_strided(o1, shape=outputshape, strides=strides)
            
            max = numpy.amax(resized_input, axis=(3, 4), keepdims=True)

            reshapedmax = max.repeat(self.pool_size[0], axis=3).repeat(self.pool_size[1], axis=4)

            max_derivative = numpy.equal(reshapedmax, resized_input).astype(int)

            numpy.copyto(o1, max_derivative)

            o1 = numpy.lib.stride_tricks.as_strided(o1, shape=input.shape, strides=input.strides)

            self.derivative = o1
            return o1
        else:
            o1 = numpy.zeros_like(input)

            o1 = numpy.lib.stride_tricks.as_strided(o1, shape=outputshape, strides=strides)
            
            max = numpy.amax(resized_input, axis=(2, 3), keepdims=True)

            reshapedmax = max.repeat(self.pool_size[0], axis=2).repeat(self.pool_size[1], axis=3)

            max_derivative = numpy.equal(reshapedmax, resized_input).astype(int)

            numpy.copyto(o1, max_derivative)

            o1 = numpy.lib.stride_tricks.as_strided(o1, shape=input.shape, strides=input.strides)

            self.derivative = o1
            return o1


    def get_derivative(self):
        return self.derivative
    def get_pool_size(self):
        return self.pool_size

    def compute(self, input):
        #3d
        #smart pad

        if len(input.shape) == 3 and self.pad != 0:
            input = numpy.pad(input, ((0, 0), (1, 1), (1, 1)))
            # print(f"new input here = {input.shape}")
        s = self.stride_len
        stride_input = input.strides
        
        outputshape = [(1 + (input.shape[-2] - self.pool_size[-2])//s), (1 + (input.shape[-1] - self.pool_size[-1])//s)]
        outputstride = [s*stride_input[-2], s*stride_input[-1]]

        if len(input.shape) == 3:
            #add third dim
            outputshape.append(input.shape[0])
            outputstride.append(stride_input[0])

            # add size of the filter
            outputshape = outputshape + list(self.pool_size)
            
            outputstride = outputstride + [stride_input[-2], stride_input[-1]]

            output = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=outputstride)
            
            #get max derivative
            self.build_derivative(input, output, outputstride, outputshape)
            
            output = numpy.amax(output, axis=(3, 4), keepdims=True)


            
            output = output.reshape(outputshape[:3])
            output = output.transpose(2, 0, 1)
            return output

        elif len(input.shape) ==2:
            
            # add size of the filter
            outputshape = outputshape + list(self.pool_size)
            outputstride = outputstride + [stride_input[-2], stride_input[-1]]


            output = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=outputstride)
            
            self.build_derivative(input, output, outputstride, outputshape)
            
            output = numpy.amax(output, axis=(2, 3), keepdims=True)
            output = output.reshape(outputshape[:2])
            return output

    def getType(self):
        return "Pool"

def SPPLayer(LayerInterface):
    def __init__(self, nb_level=3):
        pass

    def compute(self, input):
        pass
    def getType(self):
        pass