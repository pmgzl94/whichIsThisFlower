import unittest
import numpy
import os

from tensor.Tensor import TensorFileManager

import pool

class TestFcNetwork(unittest.TestCase):
    
    def test_max_pool3d_1(self):
        maxPoolLayer = pool.PoolLayer()

        input = numpy.arange(start=1, stop=49, step=1).reshape(3, 4, 4)

        expected_res = numpy.array([[[6,8],[14,16]], [[22,24],[30,32]], [[38,40],[46,48]]])

        output = maxPoolLayer.compute(input)

        self.assertEqual(output.shape, (3, 2, 2))

        # print(f"output = {output}")

        cmp = (output == expected_res)
        
        self.assertEqual(cmp.all(), True)
    
    def test_derivative_with_depth3(self):
        input = numpy.array([[[1, 2, 11, 0.3], [0, 4, 4, 36], [0, 12, 27, 34], [62, 12, 11, 10]],
                             [[11, 58, -1, 2], [1, 36, 12, 8], [27, 0, 64, 1], [1, -1, 4, 3]],
                            [[1, 3, 24, 5], [12, 2, 0, 1], [-1, 2, 3, 11], [12, 27, 18, 2]]])
        
        p = pool.PoolLayer()
        p.compute(input)

        expected_res = numpy.array([[[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1], [1, 0, 0, 0]],
                             [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 1, 0], [0, 0, 0, 0]],
                            [[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]]])
        res = p.get_derivative()
        print(res)

        cmp = (res == expected_res)
        self.assertEqual(cmp.all(), True)
        

if __name__ == '__main__':
    unittest.main()