import unittest
import numpy
import fcnetwork as fcn
from tensor.Tensor import TensorFileManager
import os

class TestSum(unittest.TestCase):
    def test_perceptron1(self):
        """
        Test that it can sum a list of integers
        """
        pathdir = "./tensorfiles"
        filename = "perceptest1"
        fullypath = pathdir + "/" + filename
        if not os.path.isdir(os.path.join(pathdir, filename + ".bs.npy")):
            TensorFileManager("./tensorfiles").save(filename + ".bs", numpy.array([0.4]))
            TensorFileManager("./tensorfiles").save(filename + ".ws", numpy.array([1.1]))
        net = fcn.FCNetwork(filename)
        expected_res = fcn.sigmoid(0.4 + 1.1)
        res = net.compute(numpy.array([1]).reshape(1, 1))

        self.assertEqual(res, expected_res)

    # def test_list_fraction(self):
    #     """
    #     Test that it can sum a list of fractions
    #     """
    #     data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 5)]
    #     result = sum(data)
    #     self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()