import unittest
import os
import numpy

from tensor.Tensor import TensorFileManager
import conv
import pool
import fcnetwork


class TestFcNetwork(unittest.TestCase):

    def test_learn_with_depth_and_multiple_filter(self):
        # input 3, 5, 5
        # filter 3, 3, 2, 2 => output 3, 4, 4
        input = numpy.array([[[0.1, 2, 0.11, 0.3, 1], [0, 0.4, 0.4, 0.36, 1], [0, 0.12, 0.27, 0.34, -3], [0.62, 0.12, 0.11, 10, 1], [0, 56, 11, 23, 44]],
                            [[0.11, 0.58, -1, 2, 0.35], [0.1, 0.36, 0.12, 0.8, 0.27], [0.27, 0, 0.64, 1, 0.12], [1, -1, 0.4, 3, 11], [0, 0.56, 0.11, 0.23, 0.44]],
                            [[1, 3, 0.24, 5, -1], [0.12, 2, 0, 1, 11], [-0.1, 0.2, 0.3, 0.11, 0.22], [12, 0.27, 0.18, 0.2, 0.34], [0, 0.56, 0.11, 0.23, 0.44]]])
        
        pathdir = "./tensorfiles"
        filename = "conv_test_depth_multiple_filter"
        fullypath = pathdir + "/" + filename

        if not os.path.exists(os.path.join(pathdir, filename + ".bs1.npy")):
            tm = TensorFileManager("./tensorfiles")

            containerfilter = numpy.ndarray((0, 3, 2, 2))

            f3 = numpy.array([[[0.3, 0.3], [0.3, 0.3]], [[0.3, 0.3], [0.3, 0.3]], [[0.3, 0.3], [0.3, 0.3]]])
            containerfilter = numpy.insert(containerfilter, 0, f3, 0)
            f2 = numpy.array([[[0.2, 0.2], [0.2, 0.2]], [[0.2, 0.2], [0.2, 0.2]], [[0.2, 0.2], [0.2, 0.2]]])
            containerfilter = numpy.insert(containerfilter, 0, f2, 0)
            f1 = numpy.array([[[0.1, 0.1], [0.1, 0.1]], [[0.1, 0.1], [0.1, 0.1]], [[0.1,0.1], [0.1, 0.1]]])
            containerfilter = numpy.insert(containerfilter, 0, f1, 0)

            biases = numpy.zeros((3,))
            
            tm.save("conv_test_depth_multiple_filter.bs1", biases)
            tm.save("conv_test_depth_multiple_filter.ws1", containerfilter)
        
        l1 = conv.ConvLayer(load_path=filename, pool=pool.PoolLayer(), activation_function="relu")
        output = l1.compute(input)

        filename = "fcn_test_depth_multiple_filter"
        
        if not os.path.exists(os.path.join(pathdir, filename + ".bs1.npy")):
            tm = TensorFileManager("./tensorfiles")

            ws = numpy.array([  [0.1, 0.3, 0.5, 0.12, 0.9, 0.12, 0.9, 0.10, 0.1, 0.11, 0.12, 0.13],
                                [0.34, 0.3, 0.64, 0.12, 1, 0.12, 0.1, 0.1, 0.12, 0.13, 0.15, 0.11]
                                ])
            biases = numpy.zeros((2,))
            
            tm.save("fcn_test_depth_multiple_filter.bs1", biases)
            tm.save("fcn_test_depth_multiple_filter.ws1", ws)

        l2 = fcnetwork.FCLayer(arch=[12, 2], transfer_learning_file="fcn_test_depth_multiple_filter")

        expected_res = numpy.array([1, 0])
        l2.learn(output, expected_res)

        delta = l2.getLastDelta()

        l1.learn(delta)

        nabla_w = l1.getNablaW()

        self.assertEqual(numpy.isclose(nabla_w[0][0][0][0], 4.1609570961e-09), True)
        self.assertEqual(numpy.isclose(nabla_w[1][1][0][0], 1.8135273233e-09), True)

# max_derivative = numpy.array([[[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 1]], [[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]], [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 1]]])
# delta = numpy.array([8.22132387e-10, 7.25410930e-10, 1.54754332e-09, 2.90164372e-10, 2.41803643e-09, 2.90164372e-10, 2.41803643e-10, 2.41803643e-10, 2.90164372e-10, 3.14344736e-10, 3.62705465e-10, 2.65984008e-10])


if __name__ == '__main__':
    unittest.main()