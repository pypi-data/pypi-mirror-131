import pytest, unittest
import os
import pickle

from glob import glob
from dlg import droputils

from dlg_example_cmpts import MyBranch, MyDataDROP, FileGlob, PickOne
from dlg.apps.simple import RandomArrayApp
from dlg.drop import InMemoryDROP, NullDROP
from dlg.ddap_protocol import DROPStates
import logging
import numpy as np
from time import sleep

logger = logging.Logger(__name__)

given = pytest.mark.parametrize


class TestMyApps(unittest.TestCase):
    def _runBranchTest(self, arrayDROP):
        """
        Execute the actual test given the arrayDROP on input
        """
        i = NullDROP("i", "i")  # just to be able to start the execution
        m = InMemoryDROP("m", "m")  # the receiving drop
        b = MyBranch("b", "b")  # the branch drop
        n = InMemoryDROP("n", "n")  # the memory drop for the NO branch
        y = InMemoryDROP("y", "y")  # the memory drop for the YES branch

        # connect the graph nodes
        i.addConsumer(arrayDROP)
        m.addProducer(arrayDROP)
        m.addConsumer(b)
        b.addOutput(y)
        b.addOutput(n)
        # start the graph
        with droputils.DROPWaiterCtx(self, b, timeout=1):
            i.setCompleted()

        # read the array back from the intermediate memory drop
        data = pickle.loads(droputils.allDropContents(m))
        # calculate the mean
        mean = np.mean(data)

        # check which branch should have been taken
        t = [y if mean < 0.5 else n][0]
        while t.status < 2:
            # make sure the graph has reached this point
            # status == 2 is COMPLETED, anything above is not expected
            sleep(0.001)
        # load the mean from the correct branch memory drop
        res = pickle.loads(droputils.allDropContents(t))
        # and check whether it is the same as the calculated one
        return (t.oid, res, mean)

    def test_myBranch_class(self):
        """
        Test creates two random arrays in memory drops, one with a
        mean below and the other above 0.5. It runs two graphs against
        each of the arrays drops and checks whether the branch is
        traversed on the correct side. It also checks whether the
        derived values are correct.
        """
        # create and configure the creation of the random array.
        l = RandomArrayApp("l", "l")
        l.integer = False
        l.high = 0.5
        (oid, resLow, meanLow) = self._runBranchTest(l)
        self.assertEqual(oid, "y")
        self.assertEqual(resLow, meanLow)

        h = RandomArrayApp("h", "h")
        h.integer = False
        h.low = 0.5
        h.high = 1
        (oid, resHigh, meanHigh) = self._runBranchTest(h)
        self.assertEqual(oid, "n")
        self.assertEqual(resHigh, meanHigh)

    def test_FileGlob_class(self):
        """
        Testing the globbing method finding *this* file
        """
        i = NullDROP("i", "i")  # just to be able to start the execution
        g = FileGlob("g", "g")
        m = InMemoryDROP("m", "m")
        g.addInput(i)
        m.addProducer(g)
        g.wildcard = os.path.basename(os.path.realpath(__file__))
        g.filepath = os.path.dirname(os.path.realpath(__file__))
        fileList = glob(f"{g.filepath}/{g.wildcard}")
        with droputils.DROPWaiterCtx(self, m, timeout=10):
            i.setCompleted()
        res = pickle.loads(droputils.allDropContents(m))
        self.assertEqual(fileList, res)

    def test_PickOne_class(self):
        """
        Testing the PickOne app
        """
        i = NullDROP("i", "i")  # just to be able to start the execution
        l = RandomArrayApp("l", "l")
        l.integer = True
        l.high = 100
        l.size = 10
        a = InMemoryDROP("a", "a", type="array", nm="start_array")
        p = PickOne("p", "p")
        r = InMemoryDROP("r", "r", type="array", nm="rest_array")
        o = InMemoryDROP("o", "o", type="scalar", nm="value")

        i.addConsumer(l)
        a.addProducer(l)
        p.addInput(a)
        r.addProducer(p)  # this should contain the rest elements
        o.addProducer(p)  # this should contain the first element
        with droputils.DROPWaiterCtx(self, o, timeout=10):
            i.setCompleted()
        in_array = pickle.loads(droputils.allDropContents(a))
        first = pickle.loads(droputils.allDropContents(o))
        rest_array = pickle.loads(droputils.allDropContents(r))
        self.assertEqual(in_array[0], first)
        self.assertEqual(all(in_array[1:]), all(rest_array))

    def test_PickOne_wrong_input_type(self):
        """
        Testing the PickOne with wrong input type
        """
        a = InMemoryDROP("a", "a", type="array", nm="start_array")
        a.write(pickle.dumps(1))  # this is scalar not array
        p = PickOne("p", "p")

        p.addInput(a)
        with droputils.DROPWaiterCtx(self, p, timeout=10):
            a.setCompleted()
        self.assertRaises(TypeError)

    def test_PickOne_0dim(self):
        """
        Testing the PickOne with 0dim input
        """
        a = InMemoryDROP("a", "a")
        a.write(pickle.dumps(np.array(1)))  # this is 0dim not array
        a.name = "start_array"
        p = PickOne("p", "p")

        p.addInput(a)
        with droputils.DROPWaiterCtx(self, p, timeout=10):
            a.setCompleted()
        self.assertRaises(TypeError)

    def test_myData_class(self):
        """
        Dummy getIO method test for data drop
        """
        assert MyDataDROP("a", "a").getIO() == "Hello from MyDataDROP"

    def test_myData_dataURL(self):
        """
        Dummy dataURL method test for data drop
        """
        assert MyDataDROP("a", "a").dataURL == "Hello from the dataURL method"
