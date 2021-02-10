import unittest
import os
import numpy

from tensor.Tensor import TensorFileManager
import conv
import pool
import fcnetwork

import model

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
        
        l1 = conv.ConvLayer(load_path=filename, filtershape=(3, 3, 2, 2), pool=pool.PoolLayer(), activation_function="relu")
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

        l2 = fcnetwork.FCLayer(arch=[12, 2], load_path="fcn_test_depth_multiple_filter")

        expected_res = numpy.array([1, 0])

        l2.compute(input=output, learn=True)
        l2.learn(expected_res)

        delta = l2.getLastDelta()

        l1.learn(delta)

        nabla_w = l1.getNablaW()

        self.assertEqual(numpy.isclose(nabla_w[0][0][0][0], 4.1609570961e-09), True)
        self.assertEqual(numpy.isclose(nabla_w[1][1][0][0], 1.8135273233e-09), True)

    def test_learn_with_depth_and_multiple_filter(self):
        print("al")
        net = fcnetwork.FCLayer(arch=[784, 100, 10], load_path=None)

        enhancedModel = model.Model(learning_rate=0.1, dataset=None, layerContainer=[net])


        net = enhancedModel.getLayerContainer()[0]

        before_w, before_b = net.getWeightsAndBiases()

        enhancedModel.test_learn_mnist(epoch=1, batch_size=30)

        net = enhancedModel.getLayerContainer()[0]
        
        after_w, after_b = net.getWeightsAndBiases()

        for b, a in zip(before_w, after_w):
            print("la")
            print(b)
            print(a)
            self.assertEqual((b == a).all(), False)
        for b, a in zip(before_b, after_b):
            print("la")
            self.assertEqual((b == a).all(), False)

    # def test_delta_computation_in_pool_layer(self):
    #     # def reshape_delta_and_compute(derivative, delta, pool_size, stride):
    #     #derivative shape 1,5,5
    #     #pool_size = 2, 2 with stride_len = 3
    #     #so delta shape =  1, 2, 2


    #     ##pool for stride len of 1
    #     # pool_derivative = numpy.array([[[1, 0, 1, 0, 0], [0, 1, 0, 1, 0], 
    #     #             [0, 0, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 1, 0]]])
        
    #     pool_derivative = numpy.array(
    #         [[[0, 0, 0, 0, 0], 
    #           [0, 1, 0, 1, 0], 
    #           [0, 0, 1, 0, 0], 
    #           [0, 0, 0, 0, 0], 
    #           [0, 0, 0, 1, 0]]], dtype="float64")

    #     delta = numpy.array([[[0.3, 0.2], [1, 0.3]]])
    #     print(f"pool_derivative shape = {pool_derivative.shape}")
    #     print(f"delta shape = {delta.shape}")
        

    #     exp_result = numpy.array(
    #         [[[0, 0, 0, 0, 0], [0, 9*0.3, 0, 12*0.2, 0], 
    #       [0, 0, 8*1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0.3*9, 0]]])
        
    #     got = pool.reshape_delta_and_compute(pool_derivative, delta, (3, 3), 2)
    #     print(got)

    #     compare_res = (exp_result == got).all()
    #     self.assertEqual(compare_res, True)

        # [1, 0, 1, 0, 0]
        # [0, 1, 0, 1, 0]
        # [0, 0, 0, 0, 0]
        # [1, 1, 0, 0, 0]
        # [0, 0, 0, 1, 0]


        
# max_derivative = numpy.array([[[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 1]], [[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]], [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 1]]])
# delta = numpy.array([8.22132387e-10, 7.25410930e-10, 1.54754332e-09, 2.90164372e-10, 2.41803643e-09, 2.90164372e-10, 2.41803643e-10, 2.41803643e-10, 2.90164372e-10, 3.14344736e-10, 3.62705465e-10, 2.65984008e-10])


if __name__ == '__main__':
    unittest.main()