import unittest
import numpy
import os

from tensor.Tensor import TensorFileManager

import conv

class TestFcNetwork(unittest.TestCase):
    
    def test_sliding_window3d_1(self):
        input = numpy.ndarray((3, 4, 3))
        conv1 = conv.ConvLayer(nb_filters=64)

        output = conv1.slidingWindow(input)
        self.assertEqual(output.shape, (64, 3, 2))
    
    # def test_sliding_window2d_1(self):
    #     input = numpy.ndarray((3, 4, 3))
    #     conv1 = conv.ConvLayer(nb_filters=64)

    #     output = conv1.slidingWindow(input)
    #     self.assertEqual(output.shape, (64, 3, 2))

    def test_sliding_window_2(self):
        pathdir = "./tensorfiles"
        filename = "conv_sliding_window2"
        fullypath = pathdir + "/" + filename
        if not os.path.exists(os.path.join(pathdir, filename + ".bs1.npy")):
            tm = TensorFileManager("./tensorfiles")

            containerfilter = numpy.ndarray((0, 3, 2, 2))

            f3 = numpy.array([[[3, 3], [3, 3]], [[3, 3], [3, 3]], [[3, 3], [3, 3]]])
            containerfilter = numpy.insert(containerfilter, 0, f3, 0)
            f2 = numpy.array([[[2, 2], [2, 2]], [[2, 2], [2, 2]], [[2, 2], [2, 2]]])
            containerfilter = numpy.insert(containerfilter, 0, f2, 0)
            f1 = numpy.array([[[1, 1], [1, 1]], [[1, 1], [1, 1]], [[1, 1], [1, 1]]])
            containerfilter = numpy.insert(containerfilter, 0, f1, 0)

            biases = numpy.zeros((3,))
            
            tm.save("conv_sliding_window2.bs1", biases)
            tm.save("conv_sliding_window2.ws1", containerfilter)
        
        conv1 = conv.ConvLayer(load_path="conv_sliding_window2")
        input = numpy.ones((3, 4, 3))
        output = conv1.slidingWindow(input)
        self.assertEqual(output.shape, (3, 3, 2))
        
        expected_o1 = numpy.ones((3,2)) * 12
        self.assertEqual((output[0] == expected_o1).all(), True)
        expected_o2 = numpy.ones((3,2)) * 24
        self.assertEqual((output[1] == expected_o2).all(), True)
        expected_o3 = numpy.ones((3,2)) * 36
        self.assertEqual((output[2] == expected_o3).all(), True)

if __name__ == '__main__':
    unittest.main()