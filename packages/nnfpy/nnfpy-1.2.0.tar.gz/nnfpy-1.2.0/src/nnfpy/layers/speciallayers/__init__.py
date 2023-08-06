from decimal import *
from random import uniform
from math import e

getcontext().prec = 25
getcontext().Emax = 2000
getcontext().Emin = -2000
getcontext().traps[Overflow] = False


'''
This class is the endlayer and will predict the output of the network
'''

class endlayer:
    def __init__(self, activation, costcal=None):
        self.activationtype = activation
        if activation == "sig": # Assigns activation function
            self.activation = lambda x: 1 / (1 + Decimal(e) ** Decimal(float(-x)))
        elif activation == "lin":
            self.activation = lambda x: Decimal(float(x))
        elif activation == "relu":
            self.activation = lambda x: Decimal(float(x)) if x > 0 else 0
        elif activation == "softmax":
            self.activation = lambda x, total: Decimal(e) ** Decimal(float(x)) / sum([Decimal(e) ** Decimal(float(i)) for i in total])
        else:
            raise RuntimeError("Not a valid activation function entered")
        self.type = "endlayer"
        self.costcal = costcal
    
    def __str__(self):
        return "This class is the endlayer and will predict the output of the network"


    '''
    This function predicts the output of the network
    This also calculates the cost of the output
    '''


    def out(self, inputs, trueval):
        self.outs = self.pred(inputs)
        if self.costcal is None: # Checks if costcal has been assigned
            self.cost = [float((self.outs[i] - Decimal(float(trueval[i]))) / len(self.outs)) for i in range(len(self.outs))]
        else:
            try:
                self.cost = [(self.costcal(self.outs[i], Decimal(trueval[i]))) / len(self.outs) for i in
                            range(len(self.outs))]
            except:
                raise RuntimeError("Cost calucation is not valid")
        if self.activationtype == "sig": # Chooses the right derivative to calculate the cost
            self.cost = [float(self.cost[i]) * e ** float(self.outs[i]) / (e ** float(self.outs[i]) + 1) ** 2 for i in
                         range(len(self.outs))]
        elif self.activationtype == "relu":
            self.cost = [float(self.cost[i]) if self.outs[i] > 0 else 0 for i in range(len(self.outs))]
        return self.outs, self.cost


    '''
    This function predicts the output of the network without calculating cost
    '''


    def pred(self, inputs):
        if self.activationtype != "softmax": # Checks if activation is softmax
            self.outs = [self.activation(Decimal(float(i))) for i in inputs]
        else:
            self.outs = [self.activation(Decimal(float(i)), inputs) for i in inputs]
        return self.outs


'''
This class changes a 2D input to a 1D input
'''


class twoDtooneD:
    def __init__(self, dimesions):
        self.dimenions = dimesions
        self.type = "twoDtooneD"


    def __str__(self):
        return "This class changes a 2D input to a 1D input"


    '''
    This function changes the 2D input to a 1D input
    '''


    def changeoneD(self, array):
        translatedarray = []
        for i in range(self.dimesions[1]):
            for t in range(self.dimenions[0]):
                translatedarray.append(array[i][t])
        return translatedarray


    '''
    This function changes the 1D input to a 2D input
    '''


    def changetwoD(self, array):
        translatedarray = [[] for _ in range(self.dimenions[1])]
        for i in range(len(array)):
            translatedarray[i // self.dimenions[i]].append(array[i])
        return translatedarray


'''
This is the dropout class
This will remove some of the outputs of the layers
'''


class dropout:
    def __init__(self, inputsize, dropoutchance=0.05):
        self.inputsize = inputsize
        self.dropoutchance = dropoutchance
        self.type = "dropout"


    def __str__(self):
        return "This is the dropout class\nThis will remove some of the outputs of the layers"

    
    '''
    This function drops some of the outputs
    '''


    def drop(self, input):
        for i in range(len(input)):
            if uniform(0, 1) <= self.dropoutchance:
                input[i] = 0
        return input
