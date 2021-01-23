from layer import LayerInterface
import numpy

# def max_pool_derivative(input):


## way to compute delta with derivative 
## for pool overlap used in zf5 and alex net model
def reshape_delta_and_compute(derivative, delta, pool_size, stride):
    # for 3d
    
    # return derivative

    # reshape delta
    # shape delta = 256, 6, 6
    reshaped_delta = delta.reshape(*delta.shape, 1, 1)
    before_last, last = (len(reshaped_delta.shape) - 2, len(reshaped_delta.shape) - 1)


    reshaped_delta = reshaped_delta.repeat(pool_size[-2], axis=before_last).repeat(pool_size[-1], axis=last)

    #derivative resized with 
    #shape 256, 13, 13
    
    #init output shape
    tderivative = derivative.T
    part1 = tderivative.shape # 13, 13, 256
    part2 = (delta.shape[-2], delta.shape[-1]) # 6, 6
    part3 = pool_size # 3, 3

    outputshape = (*part1, *part2, *part3)
    
    #init stride output shape
    (s1, s2, s3) = tderivative.strides

    # 13, 13, 256
    part1 = (s1, s2, s3)
    # 6, 6
    part2 = (s2*stride, s1*stride) #x and y are reversed because derivative is transposed
    # 3, 3
    part3 = s2, s1 #x and y are reversed because derivative is transposed
    outputstride = (*part1, *part2, *part3)

    restride_derivative = numpy.lib.stride_tricks.as_strided(tderivative, shape=outputshape, strides=outputstride)

    output = restride_derivative * reshaped_delta
    # print(f"delta * max_derivative = {output.shape}")
    # print(f"restride derivative shape = {restride_derivative.shape}")

    # print(f"restride dtype = {restride_derivative.dtype}")
    # print(f"output dtype = {output.dtype}")
    numpy.copyto(restride_derivative, output)

    #print(f"after computed derivative = {numpy.ma.is_masked(restride_derivative)}")

    computed_derivative = numpy.lib.stride_tricks.as_strided(restride_derivative, shape=tderivative.shape, strides=tderivative.strides)
    
    #print(f"after computed derivative = {numpy.ma.is_masked(computed_derivative)}")

    return (computed_derivative.T)

def helper_pool_backprop(delta, pool_layer):
    derivative = pool_layer.get_derivative()
    pool_size = pool_layer.get_pool_size()
    stride = pool_layer.get_stride_length()

    # print(f"delta shape = {delta.shape}")
    # print(f"derivative = {derivative[0]}")
    ## choose the last two axis
    before_last, last = (len(delta.shape) - 2, len(delta.shape) - 1)
    
    ## reshape delta
    delta = delta.repeat(pool_size[-2], axis=before_last).repeat(pool_size[-1], axis=last)

    return delta * derivative
    # return reshape_delta_and_compute(derivative, delta, pool_size, stride)

class PoolLayer(LayerInterface):
    # if you precise padding, you will only get a padding of 1

    def __init__(self, pad=0, pool_size=(2, 2), stride_length=2, type='max'):
        self.pool_size = pool_size
        self.stride_len = stride_length
        self.pad = pad
        self.type = type

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
            # add third dim
            outputshape.append(input.shape[0])
            outputstride.append(stride_input[0])

            # add size of the filter
            outputshape = outputshape + list(self.pool_size)
            
            outputstride = outputstride + [stride_input[-2], stride_input[-1]]

            output = numpy.lib.stride_tricks.as_strided(input, shape=outputshape, strides=outputstride)
            
            #get max derivative
            self.build_derivative(input, output, outputstride, outputshape)
            
            output = numpy.amax(output, axis=(3, 4), keepdims=True)

            # print(f"output strid shape = {output.shape}")
            
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
    
    def getParams(self):
        map = {}
        map["pool_size"] = self.pool_size
        map["padding"] = self.pad
        map["stride_length"] = self.stride_len
        map["type"] = self.type
        return map

    def get_derivative(self):
        return self.derivative
    def get_pool_size(self):
        return self.pool_size
    def get_stride_length(self):
        return self.stride_len

def SPPLayer(LayerInterface):
    def __init__(self, nb_level=3):
        pass

    def compute(self, input):
        pass
    def getType(self):
        pass