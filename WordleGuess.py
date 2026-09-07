from typing import List, Mapping
from dataclasses import dataclass
from enum import Enum

class GuessOutcome(Enum):
    GREY = "Grey"
    YELLOW = "Yellow"
    GREEN = "Green"

@dataclass
class LetterGuess:
    letter: str
    outcome: GuessOutcome

class WordleGuess:
    def __init__(self, guess: str, answer: str):
        self.guess = []
        for idx, char in enumerate(answer):
            if char == guess[idx]:
                self.guess.append(LetterGuess(guess[idx], GuessOutcome.GREEN))
            elif char != guess[idx] and char in guess:
                self.guess.append(LetterGuess(guess[idx], GuessOutcome.YELLOW))
            else:
                self.guess.append(LetterGuess(guess[idx], GuessOutcome.GREY))