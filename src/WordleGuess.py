from typing import List, Mapping
from dataclasses import dataclass
from enum import Enum

class GuessOutcome(Enum):
    GREY = "grey"
    YELLOW = "yellow"
    GREEN = "green"

class LetterGuess:
    def __init__(self, letter: str="", outcome: GuessOutcome=GuessOutcome.GREY):
        self.letter = letter
        self.outcome = outcome

    def cycle_outcome(self):
        values = list(GuessOutcome)
        self.outcome = values[(values.index(self.outcome) + 1) % len(values)]
        return self.outcome