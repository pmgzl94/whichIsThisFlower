from PIL import Image, ImageOps
import numpy

class ImageLoader():
    def __init__(self):
        return

    @classmethod
    def getOutputNpArray(self, image_path, gray=False):
        im = Image.open(image_path)
        # print(im.size)
        if gray is True:
            im2 = ImageOps.grayscale(im)
            data = numpy.asarray(im2)
            # print(data.shape)
            # im2.show()
            return data
        else:
            data = numpy.asarray(im)
            data = numpy.transpose(data, (2, 0, 1)) #rgb, y, x
            # print(data.shape)
            # im.show()
            return data
