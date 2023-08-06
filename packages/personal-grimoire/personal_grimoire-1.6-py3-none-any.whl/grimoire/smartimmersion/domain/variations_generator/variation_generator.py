import logging
from typing import Any, List

from Levenshtein import distance

from grimoire.random import true_percentage_of_times
from grimoire.smartimmersion.domain.sentence import Sentence
from grimoire.smartimmersion.domain.sentence_variation import Variation
from grimoire.smartimmersion.domain.variations_generator.translator import Translator
from grimoire.string import StringManipulation


class VariationGenerator:
    def __init__(self, exceptions, variations_percentage, settings=None):
        self.variations_percentage = variations_percentage
        self.exceptions = exceptions
        self.translator = Translator(exceptions=exceptions, settings=settings)
        self.settings = settings

    def get_variations(self, sentence: Sentence):
        """
        Returns a list of variations translations from a original sentence
        """

        if len(sentence.text) < 10:
            raise Exception(
                f"Min lenght of sentence = 10, current sentence: {sentence.text}"
            )

        text_vec = sentence.get_tokenized()

        translated_vec = self._get_translation_vector(text_vec)

        variations = self._generate_variations(text_vec, translated_vec)

        # remove duplicates
        result_sentences = []
        result_variations = []
        for variation in variations:
            sentence = variation.get_sentence()
            if sentence in result_sentences:
                continue
            result_sentences.append(sentence)
            result_variations.append(variation)

        return result_variations

    def _get_translation_vector(self, text_vec):

        result = []
        for x in text_vec:
            try:
                result.append(
                    StringManipulation.chomp(self.translator.translate_word(x))
                )
            except Exception as e:
                logging.error("Error happened while translating vector: " + str(e))
                result.append(x)

        return result

    def _generate_variations(self, text_vec, translated_vec) -> List[Any]:
        def create_variation(percentage):
            return Variation(
                self._do_translation(text_vec, translated_vec, percentage), percentage
            )

        return list(map(create_variation, self.variations_percentage))

    def _do_translation(self, text_vec, translated_vec, percentage):
        result = []
        for i, word in enumerate(text_vec):

            translated_word = translated_vec[i]
            if self.exceptions.is_easy(translated_word):
                result.append(translated_word)
                continue

            if self.exceptions and self.exceptions.manual_tranlation(word):
                result.append(self.exceptions.manual_tranlation(word))
                continue

            if not self.settings.DISABLE_TRANSLATIONS_API:
                word_difference = distance(word, translated_word)
                logging.debug(
                    f"Distance ({word_difference}) between {word} and {translated_word}"
                )
                if word_difference < 4:
                    result.append(translated_word)
                    continue

            if true_percentage_of_times(percentage):
                result.append(translated_vec[i])
            else:
                result.append(word)

        return result


class WordExceptions:
    def __init__(self, easy_words, should_not_translate_words, manual_translations):
        self.easy_words = easy_words
        self.should_not_translate_words = should_not_translate_words
        self.manual_translations = manual_translations

    def is_easy(self, word):
        return word.lower() in self.easy_words

    def should_not_translate(self, word):
        return word.lower() in self.should_not_translate_words

    def manual_tranlation(self, term):
        """" returns either a translation or None """
        term = term.lower()
        if term in self.manual_translations:
            return self.manual_translations[term]
