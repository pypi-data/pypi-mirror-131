import logging
import uuid

import pandas as pd
from joblib import load
from pandas.io.json import json_normalize
from tinydb import Query, TinyDB

from grimoire.smartimmersion.config import PROJECT_ROOT
from grimoire.smartimmersion.domain.scoring.sentence2vec import Sentence2Vec
from grimoire.string import StringManipulation
from grimoire.time import Date


class DataSourceEntry:
    @staticmethod
    def from_dict(data: dict):
        given_uuid = data.get("uuid", None)
        date_created = data.get("date_created", None)
        obj = DataSourceEntry(
            sentence=data["sentence"],
            variation=data["variation"],
            score=data["score"],
            date_created=date_created,
            given_uuid=given_uuid,
        )
        return obj

    def __init__(self, sentence, variation, score, date_created=None, given_uuid=None):
        self.sentence = StringManipulation.clean_sentence(sentence)
        self.variation = StringManipulation.clean_sentence(variation)
        self.score = score
        self.date_created = date_created if date_created else Date().today_str()
        self.uuid = given_uuid if given_uuid else str(uuid.uuid4())

    def to_dict(self):
        return {
            "sentence": self.sentence,
            "variation": self.variation,
            "score": self.score,
            "date_created": self.date_created,
            "uuid": self.uuid,
        }


class SourceDataset:
    def __init__(self):
        self.dataset_file = PROJECT_ROOT + "/dataset_db.json"
        self.db = TinyDB(self.dataset_file, sort_keys=True, indent=4)

    def save_entry(self, entry: DataSourceEntry):
        logging.info(
            f"New dataset entry, score: {entry.score}, variation: {entry.variation}"
        )
        self.db.insert(entry.to_dict())

    def load_as_pandas(self):
        result = self.db.all()
        return json_normalize(result)

    def number_of_entries(self):
        return len(self.load_as_pandas())

    def _reapply_save(self):
        """
        apply save again so the schema definition runs over the file
        """
        result = self.db.all()

        for i in result:
            Entry = Query()
            self.db.update(
                DataSourceEntry.from_dict(i).to_dict(), Entry.sentence == i["sentence"]
            )


class FeatureEngineering:
    def __init__(self):
        self.dataset = SourceDataset()
        self.variation2vec = Sentence2Vec()

    def get_dataset(self):
        """
        the end result of this process is a pandas dataframe  where all but the last column are features the last one is the score
        """
        data = self.dataset.load_as_pandas()
        word_bagging_vector = self.variation2vec.encode_sentences(
            data["variation"].to_list()
        )
        word_bagging_pandas = pd.DataFrame(word_bagging_vector)

        sentence_size = data.apply(lambda x: len(x["sentence"]), axis=1).reset_index(
            name="sentence_size"
        )

        percentage_tranlated = data.apply(
            lambda x: TranslationPercentage.percentage_difference(
                x["sentence"], x["variation"]
            ),
            axis=1,
        ).reset_index(name="percentage_translated")

        # merge all features in a dataset
        result = pd.concat(
            [
                word_bagging_pandas,
                sentence_size["sentence_size"],
                percentage_tranlated["percentage_translated"],
                data["score"],
            ],
            axis=1,
        )

        return result


class TranslationPercentage:
    @staticmethod
    def percentage_difference(sentence, sentence_translated):
        words_sentence = sentence.split(" ")
        words_translated = sentence_translated.split(" ")
        total = len(words_sentence)
        difference = 0
        logging.debug(
            f"Computing the translation percentage for sentence: ({sentence}) and translation ({sentence_translated})"
        )

        if len(words_translated) < len(words_sentence):
            raise Exception(
                f"Sentence and translated sentence do not match in size original: {words_sentence} translated: {words_translated} "
            )

        for i, w in enumerate(words_sentence):
            if words_sentence[i] != words_translated[i]:
                difference += 1

        return difference / total


class InferenceRequest:
    def __init__(self, original_sentence, generated_sentence):
        self.original_sentence = original_sentence
        self.generated_sentence = generated_sentence


class FeaturesBuilder:
    def __init__(self):
        vocabulary = load(PROJECT_ROOT + "/vocabulary.joblib")
        self.sentence2vec = Sentence2Vec(vocabulary)

    def build_features(self, inference_request: InferenceRequest) -> pd.DataFrame:
        bagging = self.sentence2vec.encode_sentence(
            inference_request.generated_sentence
        )
        df = pd.DataFrame(bagging)
        df["sentence_size"] = len(inference_request.generated_sentence)
        df["percentage_translated"] = TranslationPercentage.percentage_difference(
            inference_request.original_sentence, inference_request.generated_sentence
        )

        return df
