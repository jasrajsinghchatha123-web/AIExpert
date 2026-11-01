import re
class SpamShield:
    def __init__(self):
        self.words = {
            "urgent": 3,
            "asap": 3,
            "immediately": 3,
            "allergy": 5,
            "refund": 2,
            "cancel": 2,
            "complaint": 2,
            "delay": 2,
            "today": 1,
            "wrong order": 3,
            "not delivered": 3,
            "late delivery": 2,
            "important": 1
        }
    def calculate_score(self, message):
        score = 0
        message = message.lower()
        for word, weight in self.words.items():
            if word in message:
                score += weight
        return score
    def classify(self, message):
        score = self.calculate_score(message)
        if score >= 3:
            return "URGENT", score
        else:
            return "NORMAL", score
    def count_mistakes(self, messages):
        mistakes = 0
        for item in messages.split("\n"):
            if "|" in item:
                actual, message = item.split("|", 1)
                predicted, score = self.classify(message)
                if actual.strip().upper() != predicted:
                    mistakes += 1
        return mistakes