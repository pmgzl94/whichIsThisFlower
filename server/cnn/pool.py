from layer import LayerInterface
import numpy

class PoolLayer(LayerInterface):

    def __init__(self, pad=0, filter=(2, 2), stride_length=2, type='max'):
        self.filter = filter
        self.stride_len = stride_length

    def compute(self, input):
        #3d
        #smart pad

        s = self.stride_len
        stride_input = input.strides
        print("la")
        print(input)

        outputshape = [(1 + (input.shape[-2] - self.filter[-2])//s), (1 + (input.shape[-1] - self.filter[-1])//s)]
        outputstride = [s*stride_input[-2], s*stride_input[-1]]

        if len(input.shape) == 3:
            #add third dim
            outputshape.append(input.shape[0])
            outputstride.append(stride_input[0])

            # add size of the filter
            outputshape = outputshape + list(self.filter)
            outputstride = outputstride + [stride_input[-2], stride_input[-1]]

            output = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=outputstride)
            output = numpy.amax(output, axis=(3, 4), keepdims=True)
            print(output.shape)
            output = output.reshape(outputshape[:3])
            output = output.transpose(2, 0, 1)
            return output

        elif len(input.shape) ==2:
            
            # add size of the filter
            outputshape = outputshape + list(self.filter)
            outputstride = outputstride + [stride_input[-2], stride_input[-1]]

            
            output = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=outputstride)
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