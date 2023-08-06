import logging

from joblib import load

from grimoire.smartimmersion.config import PROJECT_ROOT
from grimoire.smartimmersion.domain.scoring.dataset import (
    FeaturesBuilder,
    InferenceRequest,
)


class Inference:
    def __init__(self):
        model_path = PROJECT_ROOT + "/model.joblib"
        logging.info(f"Loading new model from: {model_path}")
        self.rf = load(model_path)
        self.features_builder = FeaturesBuilder()

    def infer(self, inference_request: InferenceRequest):
        """ "
        For a list of sentences (simple strings) returns a list of scores, 1 for each
        """
        features = self.features_builder.build_features(inference_request)

        return self.rf.predict(features)[0]
