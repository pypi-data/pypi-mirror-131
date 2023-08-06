from random import random
from decimal import *
from math import e

getcontext().prec = 25
getcontext().Emax = 2000
getcontext().Emin = -2000
getcontext().traps[Overflow] = False


'''
This is the base layer for other layers
It can be used as a super class for other layers
'''


class baselayer:
    def __init__(self, activation):
        self.activationtype = activation
        if activation == "sig": # Assigns the activations
            self.activation = lambda x: 1 / (1 + Decimal(e) ** Decimal(-x))
        elif activation == "lin":
            self.activation = lambda x: Decimal(x)
        elif activation == "relu":
            self.activation = lambda x: Decimal(x) if x > 0 else 0
        else:
            raise RuntimeError("Not a valid activation function entered")
    
    def __str__(self):
        return "This is the base layer for other layers\nIt can be used as a super class for other layers"


    '''
    This function creates neurons
    It will create the weights and biases for the network
    '''


    def neuroncreate(self, curneur=1, nextneur=1):
        self.weights = [[random() for _ in range(nextneur)] for _ in range(curneur)]
        self.biases = [random()/100000 for _ in range(nextneur)]
        self.neuroncosts = [0 for _ in range(curneur)]
        self.momentum = None


    '''
    This function will pass the inputs through the network
    '''


    def forwardpass(self, inputs):
        self.inputs = inputs
        try:
            if len(inputs) != len(self.weights): # This checks if the input size match the weight size
                raise IndexError("Input of size " + str(len(inputs)) + " should be size " + str(len(self.weights)))
        except:
            pass
        try:
            inputs = [float(i) for i in inputs] # checks if the inputs are floats or integers
        except:
            raise TypeError("List must only contain int or float values")
        tempout = [0 for _ in range(len(self.weights[0]))]
        self.outs = [0 for _ in range(len(self.weights[0]))]
        for i in range(len(self.weights)): # Goes through the the weights and inputs and works out the output
            for t in range(len(self.weights[i])):
                tempout[t] = inputs[i] * self.weights[i][t]
            self.outs = [self.outs[s] + tempout[s] for s in range(len(tempout))]
        for i in range(len(self.outs)): # Goes through the outputs and puts them through the activation type
            self.outs[i] = Decimal(self.activation(float(self.outs[i]) + float(self.biases[i])))
        return self.outs


    '''
    This function backpropogates through the layer and improves the layer
    '''


    def backprop(self, neuroncost, alpha):
        neuroncost = [float(i) for i in neuroncost]
        self.weights = [[float(i) for i in self.weights[t]] for t in range(len(self.weights))]
        self.biases = [float(i) for i in self.biases]
        if self.activationtype == "lin": # Checks what activation type it is to make sure it caclulates the neuron cost with the right derivative
            for i in range(len(self.weights)):
                for t in range(len(self.weights[0])):
                    self.neuroncosts[i] += neuroncost[t] * self.weights[i][t] * self.inputs
        elif self.activationtype == "sig":
            for i in range(len(self.weights)):
                for t in range(len(self.weights[0])):
                    self.neuroncosts[i] += neuroncost[t] * self.weights[i][t] * e ** float(self.inputs[i]) / (
                            e ** float(self.inputs[i]) + 1) ** 2
        elif self.activationtype == "relu":
            for i in range(len(self.weights)):
                for t in range(len(self.weights[0])):
                    self.neuroncosts[i] += neuroncost[t] * self.weights[i][t] if self.inputs[i] > 0 else 0
        self.preweights = [[self.weights[t][i] - self.weights[t][i] * alpha * neuroncost[i] for i in range(len(neuroncost))] for t in range(len(self.weights))] # Applies the new weights and biases to an array to be used later
        self.prebiases = [self.biases[i] - self.biases[i] * alpha * neuroncost[i] for i in range(len(neuroncost))]
        if self.momentum != None: # Checks if momentum has been assigned
            self.preweights = self.momentum.applymomentumw(self.preweights) # Applies the momentum to the weights and biases
            self.prebiases = self.momentum.applymomentumb(self.prebiases)
        return self.neuroncosts


    '''
    This function applies the momentum class to the layer
    '''


    def applymomentum(self, momentum):
        self.momentum = momentum


    '''
    This function applies the weights calculated from the previous back propagation
    '''


    def update(self):
        self.weights = self.preweights
        self.biases = self.prebiases

    
    '''
    This function loads the weights from the pre-loaded weights
    '''


    def loadwb(self, wb):
        self.weights = wb[0]
        self.biases = wb[1]
        if all(not all(isinstance(t, int) or isinstance(t, float) for t in i) for i in self.weights) or not all(
                isinstance(i, int) or isinstance(i, float) for i in self.biases): # Checks if the data is of a valid type
            raise RuntimeError("The weights and biases lists must only contain floats")


    '''
    This returns the weights and biases of the layer
    '''


    def returnwb(self):
        return [self.weights, self.biases]


    '''
    This changes the output of the layer
    This is normally used for dropout
    '''


    def changeouts(self, outs):
        self.outs = outs


'''
This class is the a dense layer
All the neurons are connected to the next layer's neurons
'''

class denselayer(baselayer):
    def __init__(self, activation, curneur=1, nextneur=1):
        super().__init__(activation)
        super().neuroncreate(curneur, nextneur)
        self.type = "fullcon"
    
    def __str__(self):
        return "This class is the a dense layer\nAll the neurons are connected to the next layer's neurons"


'''
This class is a 2D pooling layer
It will find patterns in 2D data
'''


class twoDpoolinglayer(baselayer):
    def __init__(self, activation, poolingdimesions=[2, 2]):
        self.momentum = None
        super().__init__(activation)
        self.poolingdimensions = poolingdimesions
        self.weights = [[random() for _ in range(poolingdimesions[0])] for _ in range(poolingdimesions[1])]
        self.type = "2Dpool"

    def __str__(self):
        return "This class is a 2D pooling layer\nIt will find patterns in 2D data"


    '''
    This function will pass the inputs through the network
    '''


    def forwardpass(self, inputs):
        try:
            inputs = [[Decimal(t) for t in i] for i in inputs]
            self.inputs = inputs
            output = []
            for i in range(len(inputs) - self.poolingdimensions[1] + 1): # Finds the inputs correlating to the pooling dimensions
                xout = []
                for t in range(len(inputs[0]) - self.poolingdimensions[0] + 1):
                    total = 0
                    for y in range(self.poolingdimensions[1]):
                        for x in range(self.poolingdimensions[0]):
                            total += inputs[i + y][t + x] * Decimal(self.weights[y][x]) # This finds the output of the layer
                    xout.append(self.activation(total))
                output.append(xout)
        except:
            raise RuntimeError("Inputs are not of an even shape or not large enough for pooling dimensions")
        self.outputs = output
        return output


    '''
    This function backpropogates through the layer and improves the layer
    '''


    def backprop(self, neuroncost, alpha):
        self.preweightchange = [[0 for _ in range(self.poolingdimesions[0])] for _ in range(self.poolingdimesions[1])]
        self.neuroncost = [[0 for _ in range(neuroncost[0] + self.poolingdimensions[0])] for _ in range(self.poolingdimensions[1])]
        for i in range(len(neuroncost)): # Goes through the costs
            for t in range(len(neuroncost[0])):
                for y in range(self.poolingdimensions[1]):
                    for x in range(self.poolingdimensions[0]):
                        temp = 0
                        if self.activationtype == "lin": # Makes sure it gets the right derivative
                            temp += Decimal(self.weights[y][x]) * neuroncost[i][t] * self.inputs[i][t]
                        elif self.activationtype == "sig":
                            temp += Decimal(self.weights[y][x]) * neuroncost[i][t] * e ** float(self.inputs[i][t]) / (
                                    e ** float(self.inputs[i][t]) + 1) ** 2
                        elif self.activationtype == "relu":
                            temp += Decimal(self.weights[y][x]) * neuroncost[i][t] if self.inputs[i][t] > 0 else 0
                        self.neuroncost[i + y][t + x] += temp
                        self.preweightchange[y][x] += temp
        return self.neuroncost


    '''
    This function applies the weights calculated from the previous back propagation
    '''


    def update(self):
        self.weights = [[self.weights[i][t] + self.preweightchange[i][t] for t in range(self.poolingdimensions[0])] for
                         i in range(self.poolingdimensions[1])]
    

    '''
    This changes the output of the layer
    This is normally used for dropout
    '''


    def changeouts(self, outs):
        self.outs = outs

    def returnwb(self):
        return [self.weights]

    def loadwb(self, wb):
        self.weights = wb[0]
        if all(not all(isinstance(t, int) or isinstance(t, float) for t in i) for i in self.weights): # Checks if the data is of a valid type
            raise RuntimeError("The weights and biases lists must only contain floats")


class recurrent(baselayer):
    def __init__(self, activation, curneur=1, nextneur=1):
        super().__init__(activation)
        self.neuroncreate(curneur, nextneur)
        self.type = "recurrent"


    def neuroncreate(self, curneur=1, nextneur=1):
        self.weights = [[random() for _ in range(nextneur)] for _ in range(curneur)]
        self.recurrentweights = [Decimal(random()) for _ in range(curneur)]
        self.biases = [random()/100000 for _ in range(nextneur)]
        self.neuroncosts = [0 for _ in range(curneur)]
        self.momentum = None
        self.preinputs = [0 for _ in range(curneur)]
        self.inputs = [0 for _ in range(curneur)]

    def forwardpass(self, inputs):
        self.inputs = [float(i) for i in self.inputs]
        self.inputs = [float(inputs[i]) + self.inputs[i] * float(self.recurrentweights[i]) for i in range(len(inputs))]
        try:
            if len(inputs) != len(self.weights): # This checks if the input size match the weight size
                raise IndexError("Input of size " + str(len(inputs)) + " should be size " + str(len(self.weights)))
        except:
            pass
        try:
            inputs = [float(i) for i in inputs] # checks if the inputs are floats or integers
        except:
            raise TypeError("List must only contain int or float values")
        tempout = [0 for _ in range(len(self.weights[0]))]
        self.outs = [0 for _ in range(len(self.weights[0]))]
        for i in range(len(self.weights)): # Goes through the the weights and inputs and works out the output
            for t in range(len(self.weights[i])):
                tempout[t] = inputs[i] * self.weights[i][t]
            self.outs = [self.outs[s] + tempout[s] for s in range(len(tempout))]
        for i in range(len(self.outs)): # Goes through the outputs and puts them through the activation type
            self.outs[i] = Decimal(self.activation(float(self.outs[i]) + float(self.biases[i])))
        return self.outs


    def backprop(self, neuroncost, alpha):
        neuroncost = [float(i) for i in neuroncost]
        self.weights = [[float(i) for i in self.weights[t]] for t in range(len(self.weights))]
        self.biases = [float(i) for i in self.biases]
        if self.activationtype == "lin": # Checks what activation type it is to make sure it caclulates the neuron cost with the right derivative
            for i in range(len(self.weights)):
                for t in range(len(self.weights[0])):
                    self.neuroncosts[i] += neuroncost[t] * self.weights[i][t] * self.inputs
            for i in range(len(self.prerecurrentweights)):
                self.neuroncosts[i] += float(neuroncost[t]) * float(self.recurrentweights[i]) * self.preinputs[i]
        elif self.activationtype == "sig":
            for i in range(len(self.weights)):
                for t in range(len(self.weights[0])):
                    self.neuroncosts[i] += neuroncost[t] * self.weights[i][t] * e ** float(self.inputs[i]) / (e ** float(self.inputs[i]) + 1) ** 2
            for i in range(len(self.prerecurrentweights)):
                self.neuroncosts[i] += float(neuroncost[t]) * float(self.recurrentweights[i]) * e ** float(self.preinputs[i]) / (e ** float(self.preinputs[i]) + 1) ** 2
        elif self.activationtype == "relu":
            for i in range(len(self.weights)):
                for t in range(len(self.weights[0])):
                    self.neuroncosts[i] += neuroncost[t] * self.weights[i][t] if self.inputs[i] > 0 else 0
            for i in range(len(self.neuroncosts)):
                self.neuroncosts[i] += float(neuroncost[t]) * float(self.recurrentweights[i]) if self.inputs[i] > 0 else 0
        self.preweights = [[self.weights[t][i] - self.weights[t][i] * alpha * neuroncost[i] for i in range(len(neuroncost))] for t in range(len(self.weights))] # Applies the new weights and biases to an array to be used later
        self.prebiases = [self.biases[i] - self.biases[i] * alpha * neuroncost[i] for i in range(len(neuroncost))]
        self.prerecurrentweights = [float(self.recurrentweights[i]) * neuroncost[i] * float(self.preinputs[i]) for i in range(len(neuroncost))]
        if self.momentum != None: # Checks if momentum has been assigned
            self.preweights = self.momentum.applymomentumw(self.preweights) # Applies the momentum to the weights and biases
            self.prebiases = self.momentum.applymomentumb(self.prebiases)
        self.preinputs = self.inputs
        return self.neuroncosts

    def update(self):
        self.weights = self.preweights
        self.biases = self.prebiases
        self.recurrentweights = self.prerecurrentweights

    def changeouts(self, outs):
        self.outs = outs

    def returnwb(self):
        return [self.weights, self.biases, self.recurrentweights]

    def loadwb(self, wb):
        self.weights = wb[0]
        self.biases = wb[1]
        self.recurrentweights = wb[2]
        if all(not all(isinstance(t, int) or isinstance(t, float) for t in i) for i in self.weights) or not all(
                isinstance(i, int) or isinstance(i, float) for i in self.biases): # Checks if the data is of a valid type
            raise RuntimeError("The weights and biases lists must only contain floats")

    def resetinps(self):
        self.inputs = [0 for _ in self.inputs]