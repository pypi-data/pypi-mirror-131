from typing import List

from sklearn.feature_extraction.text import CountVectorizer


class Sentence2Vec:
    def __init__(self, vocabulary=None):
        if vocabulary:
            # during inference we have to use the same vocabulary as the trained data
            self.vectorizer = CountVectorizer(
                vocabulary=vocabulary,
                analyzer="word",
                max_features=1500,
                min_df=0,
                max_df=0.7,
                stop_words="english",
            )
        else:
            # during training we generate a new vocabulary
            self.vectorizer = CountVectorizer(
                analyzer="word",
                max_features=1500,
                min_df=0,
                max_df=0.7,
                stop_words="english",
            )

    def encode_sentence(self, sentence):
        if type(sentence) is List:
            raise Exception("Encode sentence should pass a string not a list")

        return self.encode_sentences([sentence])

    def encode_sentences(self, sentence):
        return self.vectorizer.fit_transform(sentence).toarray()

    def get_vocabulary(self):
        return self.vectorizer.get_feature_names()
