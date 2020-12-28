# import num∞py as np
import numpy
from layer import LayerInterface
from tensor.Tensor import TensorFileManager

# image getdata return flatter container
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.getdata

# for image.show
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.load

# for as_strided
# https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.as_strided.html

class ConvLayer(LayerInterface):
    def __init__(self, padding, filtershape, stride_length):
        self.padding = padding
        # self.layershape = layershape

        self.filter = numpy.ndarray(filtershape)
        self.fshape = filtershape
        # self.lrf = lr f
        self.stride_len = stride_length

        self.lastRes = None
        self.lastInput = None
        
    def slidingWindow(self, output): #sliding window
        # side - filter + 1
        container = numpy.ndarray((0, self.lrf[0], self.lrf[1], 3))
        endy = self.input_img_size[1] - self.lrf[1]
        endx = self.input_img_size[0] - self.lrf[0]

        for y in range(0, endy + 1, self.stride_len):
            for x in range(0, endx + 1, self.stride_len):
                chunk = output[x:x+self.lrf[0], y:y+self.lrf[1]] #self.fshape
                try:
                    container = numpy.append(container, chunk.reshape(1, self.lrf[0], self.lrf[1], 3), axis=0)
                except Exception:
                    print(f"x={x}, y={y}")
                    return []        
        return container

    def enhancedSlidingWindow(self, input):
        #for 2d input
        outputshape = ((input.shape[0] - self.fshape[0] + 1) // self.stride_len, (input.shape[1] - self.fshape[1] + 1) // self.stride_len, self.fshape[0], self.fshape[1])

        len_per_row ,len_per_number = input.strides

        strides = (len_per_row * self.stride_len, len_per_number * self.stride_len, len_per_row, len_per_number)

        output = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=strides)

        #for 3d input ...

        return output

    def compute(self, input):
        ## apply padding
        if self.padding != 0:
            input = numpy.pad(input, self.padding)
        output = self.enhancedSlidingWindow(input)
        featuremap = numpy.tensordot(output, self.filter)
        # if res.shape != layershape:
        #     raise Exception("output shape differ from initial one")
        self.lastInput = output
        self.lastRes = featuremap
        return featuremap

    def getType(self):
        return "FeatureMap"
