import logging

from grimoire.string import StringManipulation


class Sentence:
    def __init__(self, text):
        text = StringManipulation.clean_sentence(text)
        logging.info(f"Sentence new text: {text}")
        self.text = text

    def get_tokenized(self):
        return StringManipulation.tokenize(self.text)

    def len(self):
        return len(self.get_tokenized())
