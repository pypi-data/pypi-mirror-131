# SPDX-FileCopyrightText: 2020 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

class Solution:
    """
    iData = list : model inputs (optimization variables) values
    oData = list : model outputs (objective functions + constraints) values
    fData = list : free outputs values
    """
    iData = []
    oData = []
    fData = []

    def __init__(self, inp, out, freeOutputs=[]):
        self.iData = inp
        self.oData = out
        self.fData = freeOutputs


class Iterations:
    """
    At each gradient computation, gets the inputs and outputs of the model.
    solutions: class Solution
    iNames = list : model inputs names
    oNames = list : model outputs names
    fNames = list : model free outputs names
    """
    solutions: Solution = []
    iNames = []
    oNames = []
    fNames = []

    def __init__(self, iNames, oNames, fNames=[], handler = None):
        self.iNames = iNames
        self.oNames = oNames
        self.fNames = fNames
        self.solutions = []
        self.handler = handler #TODO : n'est plus utilisé. Modifier la création
        # automatique du Handler (dans constructeur Wrapper) lorsqu'il s'agit
        # d'un affichage dynamique : dynamicPlot.update

    def updateData(self, inp, out, freeOutputs=[]):
        """
        Adds the inputs and outputs of the model computed at each iteration
        to the Solution class.
        :param inp: list of model inputs
        :param out: list of model outputs
        :param freeOutputs : list of freeOutputs (optional)
        :return: /
        """
        self.solutions.append(Solution(inp.copy(), out.copy(),
                                       freeOutputs.copy()))
        if (self.handler):
            self.handler(self.solutions)

    def print(self):
        """
        Displays the inputs and outputs of the model at each iteration.
        :return: /
        """
        print([sol.iData for sol in self.solutions])
        print([sol.oData for sol in self.solutions])
        if self.fNames !=[]:
            print([sol.fData for sol in self.solutions])

    def plotXY(self):
        import noload.gui.plotIterations as pi
        pi.plotXY(self)
    def plotIO(self):
        import noload.gui.plotIterations as pi
        pi.plotIO(self)


def printHandler(sols:List[Solution]):
    """
    Displays the inputs and outputs of the model computed during the last
    iteration.
    :param sols: class Solution
    :return: /
    """
    sols
    print(sols[-1].iData)
    print(sols[-1].oData)
    if sols.fData != []:
        print(sols[-1].fData)

