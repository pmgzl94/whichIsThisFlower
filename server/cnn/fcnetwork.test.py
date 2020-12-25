import unittest
import numpy
import fcnetwork as fcn
from tensor.Tensor import TensorFileManager
import os

class TestFcNetwork(unittest.TestCase):
    #### forward test
    def test_perceptron1(self):
        pathdir = "./tensorfiles"
        filename = "perceptest1"
        fullypath = pathdir + "/" + filename
        if not os.path.isdir(os.path.join(pathdir, filename + ".bs1.npy")):
            TensorFileManager("./tensorfiles").save(filename + ".bs1", numpy.array([[0.4]]))
            TensorFileManager("./tensorfiles").save(filename + ".ws1", numpy.array([[1.1]]))
        net = fcn.FcLayer(arch=[1, 1], transfer_learning_file=filename)
        expected_res = fcn.sigmoid(0.4 + 1.1)
        res = net.compute(numpy.array([1]))

        self.assertEqual(res, expected_res)

    ### test with a bigger network
    def test_shallow_network1(self):
        pathdir = "./tensorfiles"
        filename = "shallow_network1"
        fullypath = pathdir + "/" + filename
        if not os.path.isdir(os.path.join(pathdir, filename + ".bs1.npy")):
            # ws = [[numpy.array([1, 0.7]), numpy.array([0.1, 0.8]), numpy.array([0.4, 0.9])], [numpy.array([0.9, 0.7, 0.1])]]
            ws1 = numpy.array([[1, 0.7], [0.1, 0.8], [0.4, 0.9]])
            ws2 = numpy.array([[0.9, 0.7, 0.1]])
            ws  = [ws1, ws2]
            bs1 = [[0, 0, 0]]
            bs2 = [[0]]
            # return
            TensorFileManager("./tensorfiles").save(filename + ".bs1", bs1)
            TensorFileManager("./tensorfiles").save(filename + ".bs2", bs2)
            TensorFileManager("./tensorfiles").save(filename + ".ws1", ws1)
            TensorFileManager("./tensorfiles").save(filename + ".ws2", ws2)
        net = fcn.FcLayer(arch=[2, 3, 1], transfer_learning_file=filename)

        input = numpy.array([0.3, 0.4])
        expected_res = 0.7406534729647368
        res = net.compute(input)

        self.assertEqual(res, expected_res)


    def test_online_learning1(self):
        pathdir = "./tensorfiles"
        filename = "online_learning1"
        fullypath = pathdir + "/" + filename
        if not os.path.isdir(os.path.join(pathdir, filename + ".bs1.npy")):
            # print("la2")
            ws1 = numpy.array([[0.2, 0.3], [0.4, 0.5], [1.1, 0.1]])
            # print(f"w = {ws1.shape}")
            ws2 = numpy.array([[0.9, 0.3, 0.1], [0.3, 0.4, 0.1]])
            ws  = [ws1, ws2]
            bs1 = [0, 0, 0]
            bs2 = [0, 0]

            # return
            TensorFileManager("./tensorfiles").save(filename + ".bs1", bs1)
            TensorFileManager("./tensorfiles").save(filename + ".bs2", bs2)
            TensorFileManager("./tensorfiles").save(filename + ".ws1", ws1)
            TensorFileManager("./tensorfiles").save(filename + ".ws2", ws2)
        net = fcn.FcLayer(arch=[2, 3, 2], transfer_learning_file=filename)

        input = numpy.array([0.1, 0.2])
        expected_res = numpy.array([1,  0])
        expected_delta = numpy.array([-0.00601069,  0.00878729,  0.00173201])
        
        net.learn(input, expected_res)
        returnedDelta = net.getLastDelta()

        res  = numpy.isclose(returnedDelta, expected_delta, atol=1e-5)
        # print(returnedDelta)
        # print(expected_delta)
        # print(res.all())

        self.assertEqual(res.all(), True)

    # def test_list_fraction(self):
    #     """
    #     Test that it can sum a list of fractions
    #     """
    #     data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 5)]
    #     result = sum(data)
    #     self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()