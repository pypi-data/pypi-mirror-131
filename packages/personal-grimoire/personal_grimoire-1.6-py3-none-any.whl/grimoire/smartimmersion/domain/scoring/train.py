import logging

import numpy as np
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from grimoire import s
from grimoire.smartimmersion.config import PROJECT_ROOT
from grimoire.smartimmersion.domain.scoring.dataset import FeatureEngineering


class Train:
    def __init__(self):
        self.dataset = FeatureEngineering()

    def train(self):
        """
        For mlflow to save the file in the correct place you must run this command in the PROJECT_ROOT
        """
        logging.info("Start training")

        dataset = self.dataset.get_dataset()
        train, test = train_test_split(dataset, random_state=14)

        train_y = train.iloc[:, -1]
        train_x = train[train.columns[:-1]]
        test_x = test[test.columns[:-1]]
        test_y = test.iloc[:, -1]

        # @TODO understand why importing it on the top breaks grimoire
        import mlflow
        import mlflow.sklearn

        # transform the variation text to a number vector using word bagging
        with mlflow.start_run():

            class Hyperparameters:
                n_estimators = 1000
                random_state = 42

            rf = RandomForestRegressor(
                n_estimators=Hyperparameters.n_estimators,
                random_state=Hyperparameters.random_state,
            )
            rf.fit(train_x, train_y)
            logging.info(f"Fit done!")

            # test
            predicted = rf.predict(test_x)
            (rmse, mae, r2) = self.evaluate_error(test_y, predicted)

            logging.info(f"rmse:  {rmse}, mae {mae}, r2 {r2}")

            # dump new model
            model_location = PROJECT_ROOT + "/model.joblib"
            dump(rf, model_location)
            logging.info(f"Training done, model dumped to {model_location}")
            dump(
                self.dataset.variation2vec.get_vocabulary(),
                PROJECT_ROOT + "/vocabulary.joblib",
            )

            mlflow.log_param("n_estimators", Hyperparameters.n_estimators)
            mlflow.log_param("random_state", Hyperparameters.random_state)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)
            mlflow.log_param("dataset_size", len(dataset))

            mlflow.sklearn.log_model(rf, "model")

            s.run('notify-send "Train run successfully"')

    def evaluate_error(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
