from PySide6 import QtCore, QtWidgets, QtGui
from WordleGuess import LetterGuess, GuessOutcome
from typing import List

class LetterBox(QtWidgets.QWidget):
    def __init__(self, char: str="", outcome: GuessOutcome = GuessOutcome.GREY):
        super().__init__()

        if len(char) > 1:
            raise ValueError("String is not a char")
        
        self.letter = LetterGuess(char, outcome)

        self.button = QtWidgets.QPushButton(char)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.click)

        self.set_background_color()

    def set_background_color(self, outcome: GuessOutcome=GuessOutcome.GREY):
        background_color = outcome.value.lower()
        self.setStyleSheet(f"background-color: {background_color}")
        
    def delete_letter(self):
        self.set_background_color()
        self.letter.letter = ""
        self.button.setText("")

    def add_letter(self, char: str):
        self.letter.letter = char
        self.button.setText(char)

    @QtCore.Slot()
    def click(self):
        if len(self.letter.letter) == 0:
            return
        
        self.letter.cycle_outcome()

        self.set_background_color(self.letter.outcome)


class WordGuess(QtWidgets.QWidget):
    def __init__(self, max_word_length: int = 5):
        super().__init__()

        self.max_word_length = max_word_length
        self.word = [LetterBox() for _ in range(max_word_length)]
        self.ltr_idx = 0

        self.button = QtWidgets.QPushButton("")
        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QHBoxLayout(self)

        for letter in self.word:
            self.layout.addWidget(letter)

    def add_letter(self, char: str):       
        if len(char) != 1:
            raise ValueError("String is not a char")

        if self.ltr_idx >= self.max_word_length:
            return
        
        self.word[self.ltr_idx].add_letter(char)
        self.ltr_idx = self.ltr_idx + 1

    def delete_letter(self):       
        if self.ltr_idx == 0:
            return
        
        self.ltr_idx -= 1
        self.word[self.ltr_idx].delete_letter()
        self.word[self.ltr_idx].outcome = GuessOutcome.GREY

    def get_word(self) -> List[LetterGuess]:
        return self.word

    def is_full(self):
        return self.ltr_idx == self.max_word_length

    def keyPressEvent(self, event: QtGui.QKeyEvent):       
        print("key:", event.key())
        if event.key() == QtCore.Qt.Key_Backspace:
            self.delete_letter()
        elif event.text().isalpha():
            self.add_letter(event.text())
        else:
            super().keyPressEvent(event)

class WordGuessList(QtWidgets.QWidget):
    def __init__(self, num_guesses: int=6):
        super().__init__()

        self.guesses = [WordGuess() for _ in range(num_guesses)]
        self.guess_idx = 0
        self.num_guesses = num_guesses

        self.layout = QtWidgets.QVBoxLayout(self)

        for idx, guess in enumerate(self.guesses):
            self.layout.addWidget(guess)

            if idx != self.guess_idx:
                guess.setEnabled(False)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() not in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            super().keyPressEvent(event)

        last_guess = self.guesses[self.guess_idx]

        if last_guess.is_full() is False:
            return

        if self.guess_idx == self.num_guesses - 1:
            return
        
        last_guess.setEnabled(False)

        self.guess_idx += 1

        self.guesses[self.guess_idx].setEnabled(True)
        self.guesses[self.guess_idx].setFocus()