from WordleGuess import WordleGuess, GuessOutcome, LetterGuess
import os

DEFAULT_DICTIONARY_PATH = "answer-dictionary.txt"

class WordleSolver:
    def __init__(self):
        self.load_dictionary()
        self.guesses = []

    def load_dictionary(self):
        dict_dir = os.environ.get("DICT_DIR", DEFAULT_DICTIONARY_PATH)
        
        with open(dict_dir, "r") as file:
            self.possible_answers = [line.strip() for line in file]

    def reset(self):
        self.loadDictionary()
        self.guesses = []

    def add_guess(self, guess: WordleGuess):
        self.guesses.append(guess)

        def valid_word(word: str):
            for idx, letter_guess in enumerate(guess.guess):
                if (letter_guess.outcome is GuessOutcome.GREEN 
                    and word[idx] == letter_guess.letter):
                    continue
                elif (letter_guess.outcome is GuessOutcome.YELLOW 
                      and word[idx] != letter_guess.letter and letter_guess.letter in word):
                    continue
                elif (letter_guess.outcome is GuessOutcome.GREY 
                      and word[idx] != letter_guess.letter and letter_guess.letter not in word):
                    continue
                else:
                    return False

            return True

        new_answers = []

        for answer in self.possible_answers:
            if valid_word(answer) is True:
                new_answers.append(answer)

        self.possible_answers = new_answers

    def get_answers(self):
        return self.possible_answers
    