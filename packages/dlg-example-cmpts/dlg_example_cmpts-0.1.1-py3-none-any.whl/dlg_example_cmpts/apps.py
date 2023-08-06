"""
dlg_example_cmpts appComponent module.

This is the module of dlg_example_cmpts containing DALiuGE
application components.
Here you put your main application classes and objects.

Typically a component project will contain multiple components and will
then result in a single EAGLE palette.

Be creative! do whatever you need to do!
"""

__version__ = "0.1.0"
import logging
import pickle
from glob import glob

import numpy as np
from dlg import droputils
from dlg.drop import BarrierAppDROP, BranchAppDrop

logger = logging.getLogger(__name__)

##
# @brief MyBranch
# @details Simple app to demonstrate how to write a branch actually making a
# decision and passing data on.
# Most of the code is boilerplate and can be copied verbatim. Note that a
# branch app is allowed
# to have multiple inputs, but just exactly two outputs. This example is using
# just a single input. There is an associated logical graph available on
# github:
#
#    https://github.com//EAGLE-graph-repo/examples/branchDemo.graph
#
# The application assumes to receive a random floating point array with values
# in the range [0,1] on input. It will calculate the mean of that array and
# then branch depending on whether the mean is smaller or larger than 0.5.
#
# @par EAGLE_START
# @param category PythonApp
# @param[in] param/appclass Application Class/
# dlg_example_cmpts.appCmpts.MyBranch/String/readonly/
#     \~English Import direction for application class
# @param[in] port/array Array/float/
#     \~English Port receiving the input array
# @param[out] port/Y Y/float/
#     \~English Port carrying the mean value of the array if mean < 0.5
# @param[out] port/N N/float/
#     \~English Port carrying the mean value of the array if mean >= 0.5
# @par EAGLE_END


class MyBranch(BranchAppDrop):
    def initialize(self, **kwargs):
        BranchAppDrop.initialize(self, **kwargs)

    def run(self):
        """
        Just reading the input array and calculating the mean.
        """
        input = self.inputs[0]
        data = pickle.loads(droputils.allDropContents(input))
        self.value = data.mean()

    def writeData(self):
        """
        Prepare the data and write to port (self.ind) identified by condition.
        """
        output = self.outputs[self.ind]
        d = pickle.dumps(self.value)
        output.len = len(d)
        logger.info(f">>>>>>> Writing value {self.value} to output {self.ind}")
        output.write(d)

    def condition(self):
        """
        Check value, call write method and return boolean.
        """
        if self.value < 0.5:
            self.ind = 0
            result = True
        else:
            self.ind = 1
            result = False
        self.writeData()
        return result


##
# @brief FileGlob
# @details An App that uses glob to find all files matching a
# template given by a filepath and a wildcard string
#
# @par EAGLE_START
# @param category PythonApp
# @param[in] param/wildcard wildcard/"*"/String/readwrite/
#     \~English Wildcard used to search for files
# @param[in] param/filepath filepath/"."/String/readwrite/
#     \~English Path to search for files
# param/appclass Application Class/
# dlg_example_cmpts.appCmpts.FileGlob/String/readonly/
#     \~English Import path for application class
# @param[out] port/file_list file_list/array/
#     \~English Port carrying the list of files
# @par EAGLE_END


class FileGlob(BarrierAppDROP):
    """
    Simple app collecting file names in a directory
    based on a wild-card pattern
    """

    def initialize(self, **kwargs):
        self.wildcard = self._getArg(kwargs, "wildcard", "*")
        self.filepath = self._getArg(kwargs, "filepath", ".")
        BarrierAppDROP.initialize(self, **kwargs)

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        for output in self.outputs:
            d = pickle.dumps(self.value)
            output.len = len(d)
            output.write(d)

    def run(self):
        filetmpl = f"{self.filepath}/{self.wildcard}"
        self.value = glob(filetmpl)
        self.writeData()


##
# @brief PickOne
# @details App that picks the first element of an input list, passes that
# to all outputs, except the first one. The first output is used to pass
# the remaining array on. This app is useful for a loop.
#
# @par EAGLE_START
# @param category PythonApp
# param/appclass Application Class/
# dlg_example_cmpts.appCmpts.PickOne/String/readonly/
#     \~English Import path for application class
# @param[in] port/rest_array rest_array//array/readwrite/
#     \~English List of elements
# @param[out] port/element element/complex/
#     \~English Port carrying the first element of input array
#               the type is dependent on the list element type.
# @par EAGLE_END
class PickOne(BarrierAppDROP):
    """
    Simple app picking one element at a time. Good for Loops.
    """

    def initialize(self, **kwargs):
        BarrierAppDROP.initialize(self, **kwargs)

    def readData(self):
        input = self.inputs[0]
        data = pickle.loads(droputils.allDropContents(input))

        # make sure we always have a ndarray with at least 1dim.
        if type(data) not in (list, tuple) and not isinstance(
            data, (np.ndarray)
        ):
            raise TypeError
        if isinstance(data, np.ndarray) and data.ndim == 0:
            data = np.array([data])
        else:
            data = np.array(data)
        self.value = data[0] if len(data) else None
        self.rest = data[1:] if len(data) > 1 else []

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        # write rest to array output
        # and value to every other output
        for output in self.outputs:
            if output.name == "rest_array":
                d = pickle.dumps(self.rest)
                output.len = len(d)
            else:
                d = pickle.dumps(self.value)
                output.len = len(d)
            output.write(d)

    def run(self):
        self.readData()
        self.writeData()
