from grimoire.smartimmersion.domain.sentence import Sentence


class Paragraph:
    def __init__(self, text):
        self.text = text
        self.sentences = []

        sentence_str = text.split(".")
        for i in sentence_str:
            self.sentences.append(Sentence(i))
