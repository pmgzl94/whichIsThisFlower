import numpy
import itertools
import functools

def evaluate_test_data(self, test_data):
    test_res = [(numpy.argmax(self.compute(x)), numpy.argmax(exp)) for (x, exp) in test_data]
    return sum([int(idx_got == idx_exp) for (idx_got, idx_exp) in test_res])

##test flower

refTable = ["daisy", "dandelion", "rose", "sunflower", "tulip"]

#display percentage evaluation among the different species of flower
def evaluate_test_flower_verbose(self, test_data):
    ##
    percentage = {
        "daisy": (0, 0),
        "dandelion": (0, 0),
        "rose": (0, 0),
        "sunflower": (0, 0),
        "tulip": (0, 0),
    }
    for (x, y) in test_data:
        got_idx = numpy.argmax(self.compute(x))
        expec_idx  = numpy.argmax(y)
        # print(f"expec = {expec_idx}")
        # print(f"got = {got_idx}")
        key = refTable[expec_idx]
        if got_idx == expec_idx:
            percentage[key] = (percentage[key][0] + 1, percentage[key][1])
        percentage[key] = (percentage[key][0], percentage[key][1] + 1)
    
    print("### verbose evaluation ###")
    for key, val in percentage.items(): print(f"{key} = {val[0]}/{val[1]} ", end="")

    print("")

    total = functools.reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), list(percentage.values()), (0, 0))
    print(f"total = {total[0]}/{total[1]}")
    print("###########################")
    return total[0]