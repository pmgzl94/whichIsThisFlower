import unittest
import dropout
import numpy

class TestDropout(unittest.TestCase):

    def simple_dropout_test(self):
        # self.assertEqual(, )
        d = dropout.DropoutLayer(p=0.25, ishape=(2, 2))
        inp = numpy.ones((2, 2))
        res = d.compute(inp)
        self.assertEqual(numpy.count_nonzero(res), 3)

if __name__ == '__main__':
    unittest.main()