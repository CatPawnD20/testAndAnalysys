class DecisionData:
    def __init__(self, date, decision, confidenceRate, phaseIndex):
        self.id = None
        self.date = date
        self.decision = decision
        self.confidenceRate = confidenceRate
        self.phaseIndex = phaseIndex


    def write_my_self(self):
        print("id: " + str(self.id))
        print("date: " + str(self.date))
        print("decision: " + str(self.decision))
        print("confidenceRate: " + str(self.confidenceRate))
        print("phaseIndex: " + str(self.phaseIndex))
