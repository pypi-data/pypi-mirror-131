'''
These loss classes will make the learning rate go down
'''


class linearloss:
    def __init__(self, lossrate):
        self.lossrate = lossrate
        self.type = "loss"
    
    def __str__(self):
        return "This loss class will make the learning rate go down"

    def newrate(self, learningrate):
        return learningrate - self.lossrate if learningrate - self.lossrate > 0 else learningrate


class timesloss:
    def __init__(self, lossrate):
        self.lossrate = lossrate
        self.type = "loss"

    def __str__(self):
        return "This loss class will make the learning rate go down"

    def newrate(self, learningrate):
        if not learningrate - learningrate * self.lossrate < 0:
            self.prevlearn = learningrate
            return learningrate - learningrate * self.lossrate
        else:
            return self.prevlearn


'''
These boost classes will make the learning rate go up every set amount of epochs
'''


class learnboost:
    def __init__(self, epochnum, boost):
        self.epochnum = epochnum
        self.boostam = boost
        self.type = "boost"

    def __str__(self):
        return "This boost class will make the learning rate go up every set amount of epochs"

    def boost(self, epochs, learning):
        try:
            if epochs % self.epochnum == 0 and epochs != 0:
                return learning + self.boostam
            else:
                return learning
        except:
            return learning


class SmartBoost:
    def __init__(self, epochnum, boost, boostloss=1):
        self.epochnum = epochnum
        self.boostam = boost
        self.type = "SmartBoost"
        self.boostloss = boostloss

    def __str__(self):
        return "This boost class will make the learning rate go up every set amount of epochs"

    def boost(self, epochs, learning, totalepochs):
        try:
            if epochs % self.epochnum == 0 and epochs != 0:
                return learning + self.boostam * abs(1 - epochs / totalepochs / self.boostloss)
            else:
                return learning
        except:
            return learning
