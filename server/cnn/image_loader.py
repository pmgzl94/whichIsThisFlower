from PIL import Image, ImageOps
import numpy

class ImageLoader():
    def __init__(self):
        return

    @classmethod
    def getCropedImage(self, image_path, tpl=(0, 0, 224, 224)):
        im = Image.open(image_path)
        # print(f"initial image size: {im.size}")
        # tpl = (0, 0, 244, 244)
        im = im.crop(box=tpl)

        # im.show()
        # print(im.size)
        return im

    @classmethod
    def getOutputNpArray(self, image_path, gray=False, crop=False):
        
        if crop:
            im = self.getCropedImage(image_path)
            data = numpy.asarray(im)
            data = numpy.transpose(data, (2, 0, 1))
            print(f"shape = {data.shape}")
            return data

        # print(im.size)
        im = Image.open(image_path)

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
