# import num∞py as np
from PIL import Image
import numpy
from layer import LayerInterface
from tensor.Tensor import TensorFileManager

# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.getdata
# show
# https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.load

class FeatureMap(LayerInterface):
    def __init__(self, layershape, padding, filtershape, lrf, stride_length):
        self.padding = padding
        self.layershape = layershape

        self.filter = numpy.ndarray(filtershape)
        self.lrf = lrf
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
                chunk = output[x:x+self.lrf[0], y:y+self.lrf[1]]
                try:
                    container = numpy.append(container, chunk.reshape(1, self.lrf[0], self.lrf[1], 3), axis=0)
                except Exception:
                    print(f"x={x}, y={y}")
                    return []        
        return container

    def compute(self, input):
        ## apply padding
        if self.padding != 0:
            input = numpy.pad(input, self.padding)
        input = self.slidingWindow(input)
        res = numpy.dot(input, filtershape)
        if res.shape != layershape:
            raise Exception("output shape differ from initial one")
        self.lastInput = None
        self.lastRes = None
        return res
    def getType(self):
        return "FeatureMap"

class ImageLoader():
    ## local receptive field, stride length
    # def __init__(self, lrf, stride_length, input_img_size):
    def __init__(self, lrf, stride_length, input_img_size):
        print(lrf)
        
        self.input_img_size = input_img_size
        return

    def getOutputNpArray(self, image_path):
        ##
        ## Find a way to fixed the size of the image: https://arxiv.org/pdf/1406.4729.pdf
        ##
        im = Image.open(image_path)
        print(im.size)
        pix = im.getdata() #The sequence object is flattened, so that values for line one follow directly after the values of line zero, and so on.
        data = numpy.asarray(im)
        # im.show()
        data = numpy.transpose(data, (1, 0, 2))
        # im.show()
        return data

    # def sliceImage(self, output): #sliding window
    #     container = numpy.ndarray((0, self.lrf[0], self.lrf[1], 3))
    #     endy = self.input_img_size[1] - self.lrf[1]
    #     endx = self.input_img_size[0] - self.lrf[0]

    #     #find better way to slice the image
    #     for y in range(0, endy + 1, 1):
    #         for x in range(0, endx + 1, 1):
    #             chunk = output[x:x+self.lrf[0], y:y+self.lrf[1]]
    #             # print(chunk.shape)
    #             # print(chunk.shape)
    #             try:
    #                 container = numpy.append(container, chunk.reshape(1, self.lrf[0], self.lrf[1], 3), axis=0)

    #             except Exception:
    #                 print(f"x={x}, y={y}")
    #                 return []

    #     # print(container.shape)
    #     TensorFileManager().save("testMatrix.tensorfile", container)
        
    #     # out = TensorFileManager().load("testMatrix.tensorfile")
    #     # print(out.shape)
        
    #     return container
    
    # def getOutput(self, image_path):
    #     output = self.getOutputNpArray(image_path)
    #     print(output.shape)
    #     return self.sliceImage(output)

        # res3 = output[0:5,0:5]
        # print("shape:")
        # print(res3.shape)
        # res4 = output[2:4,2:4]

        # container = numpy.ndarray((0, self.lrf[0], self.lrf[1], 3))
        # container = numpy.append(container, res3.reshape(1, 5, 5, 3), axis=0)
        # print(containe)