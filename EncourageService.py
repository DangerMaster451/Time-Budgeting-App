import random

class EncourageService():
    @staticmethod
    def giveEncouragement() -> str:
        phrases:list[str] = [
            "\"For there is always light. If only we're brave enough to see it. If only we're brave enough to be it.\"",
            "\"Real change, enduring change, happens one step at a time.\"",
            "\"Just keep swimming, just keep swimming.\"",
            "\"Give up on your dreams and die\"",
            "\"You are never too old to set another goal or to dream a new dream.\"",
            "\"Life is like riding a bicycle. To keep your balance, you must keep moving.\"",
            "\"The bad news is time flies. The good news is you're the pilot.\"",
            "\"Pay attention to the present, you can improve upon it.\"",
            "\"It is not enough to have a good mind; the important thing is to use it well.\"",
            "\"Walk to your goal firmly and with bold steps.\"",
            "\"Every strike brings me closer to the next home run.\"",
            "\"Lay plans for something big by starting with it when small.\"",
            "\"It takes as much energy to wish as it does to plan.\"",
            "\"Do anything, but let it produce joy.\"",
            "\"No one is useless in this world who lightens the burdens of another.\"",
            "\"You only get one shot, so shoot!\"",
            "\"You only live once, so just go freaking nuts!\"",
            "\"You only live one life, for a very short time, so make every second divine!\"",
            "\"Let's take our freaking lives back!\"",
            "\"It's my life, I'll take it back\""    
        ]
        return phrases[random.randint(0, len(phrases)-1)]