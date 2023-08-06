from grimoire.smartimmersion.domain.scoring.dataset import InferenceRequest
from grimoire.smartimmersion.domain.scoring.inference import Inference
from grimoire.smartimmersion.domain.sentence import Sentence
from grimoire.smartimmersion.domain.variations_generator.variation_generator import (
    VariationGenerator,
    WordExceptions,
)


class ScoredVariations:
    def __init__(self, settings):
        self.variations_generator = VariationGenerator(
            WordExceptions(
                settings.easy_words,
                settings.do_not_translate_words,
                settings.manual_translations,
            ),
            settings.translations_percentages,
            settings=settings,
        )
        self.inference = Inference()

    def get_for_sentence(self, sentence: Sentence):
        """returns the model variations sorted by the score"""
        self.inference = Inference()
        results = self.variations_generator.get_variations(sentence)

        def inference(sentence):
            return self.inference.infer(InferenceRequest(sentence, sentence))

        scored_variations = list(
            map(lambda x: x.set_score(inference(x.get_sentence())), results)
        )
        sorted_by_score = sorted(
            scored_variations, key=lambda tup: tup.score, reverse=True
        )
        return sorted_by_score
