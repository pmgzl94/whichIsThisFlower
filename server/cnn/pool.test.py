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

if __name__ == '__main__':
    unittest.main()