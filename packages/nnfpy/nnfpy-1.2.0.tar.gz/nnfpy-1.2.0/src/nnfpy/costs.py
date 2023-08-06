from math import sqrt
from decimal import *
from math import log

getcontext().prec = 25
getcontext().Emax = 2000
getcontext().Emin = -2000
getcontext().traps[Overflow] = False
getcontext().traps[InvalidOperation] = False


'''
These lambda classes calculate the cost of the network
'''


categoricalcrossentropy = lambda pred, trueval: trueval * Decimal(log(pred)) * Decimal(-1)

squared = lambda pred, trueval: (pred - Decimal(trueval)) * abs(pred - Decimal(trueval))

root = lambda pred, trueval: Decimal(sqrt(abs(pred - Decimal(trueval)))) * (
        (pred - Decimal(trueval)) / abs(pred - Decimal(trueval)))


'''
This momentum class adds previously calculated weights and biases to the current
'''


class momentum:
    def __init__(self, momentumeffect):
        self.momentumeffect = momentumeffect
        self.prevweightchange = 0
        self.prevbiaschange = 0

    def __str__(self):
        return "This momentum class adds previously calculated weights and biases to the current"


    '''
    The following classes apply previous weights and biases to the new weights and biases
    '''


    def applymomentumw(self, weightchange):
        try:
            templist = [[weightchange[i][t] + self.prevweightchange[i][t] * self.momentumeffect for t in
                         range(len(self.prevweightchange[i]))] for i in range(len(self.prevweightchange))]
            self.prevweightchange = weightchange
            return templist
        except:
            pass
        return weightchange

    def applymomentumb(self, biaschange):
        try:
            templist = [biaschange + self.prevbiaschange[i] * self.momentumeffect for i in len(self.prevbaischange)]
            self.prevbiaschange = biaschange
            return templist
        except:
            pass
        return biaschange

    def returnmom(self):
        return self.currentmomentum