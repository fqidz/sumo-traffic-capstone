from typing import Deque
import matplotlib.pyplot as plt
import random as rand
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


plt.ion()


def plot(scores, mean_scores):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of episodes')
    plt.ylabel('Amount of cars arrived')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


class DebugGui:
    def __init__(self) -> None:
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.texts = []

    def load_texts(self, texts):
        for i in texts:
            label = QLabel(i)
            self.layout.addWidget(label)

    def update(self):
        self.load_texts(self.texts)
        self.window.show()
        self.app.exec()


if __name__ == "__main__":
    gui = DebugGui()

    for i in range(10000):
        gui.texts = [rand.random(), rand.random(), rand.random(),
                     rand.random(), rand.random()]

        gui.update()
