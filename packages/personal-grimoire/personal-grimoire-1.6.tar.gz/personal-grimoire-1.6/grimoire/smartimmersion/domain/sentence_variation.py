from typing import List


class Variation:
    """
    @todo decide if the logic of generating variations should go here as well

    This is a domain object, no side-effect should go here
    """

    def __init__(self, text: List[str], translated_percentage):
        self.text = text
        self.translated_percentage = translated_percentage
        self.score = None

    def get_sentence(self):
        return Variation._vector_to_sentence(self.text)

    @staticmethod
    def _vector_to_sentence(word_vec):
        return " ".join(word_vec)

    def set_score(self, score):
        self.score = score

        return self
