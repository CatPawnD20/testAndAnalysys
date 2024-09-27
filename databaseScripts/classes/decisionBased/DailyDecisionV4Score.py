from databaseScripts.classes.decisionBased.DecisionData import DecisionData


class DailyDecisionV4Score(DecisionData):
    def __init__(self, decision_timestamp, decision, decision_rate,phaseIndex):
        super().__init__(decision_timestamp, decision, decision_rate,phaseIndex)
