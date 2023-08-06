import numpy as np

# convenience imports
import sklearn.model_selection as ms
import streamlit as st
from sklearn.metrics import mean_squared_error


def npmap(f, x):
    vfunc = np.vectorize(f)
    return vfunc(x)


def np_append_columns(columns_pair):
    return np.column_stack(columns_pair)


def report_prediction_error(y_pred, y_test):
    from sklearn import metrics

    return {
        "Mean absolute error: ": metrics.mean_absolute_error(y_test, y_pred),
        "Mean squared error: ": metrics.mean_squared_error(y_test, y_pred),
        "Root Mean squared error: ": np.sqrt(
            metrics.mean_squared_error(y_test, y_pred)
        ),
    }


def draw_image(boolean_map):
    newarray = npmap(lambda x: 255 if x else 0, boolean_map)
    image = st.empty()
    image.image(newarray)


def xy_split_df(df):
    """
    Splits a data frame in training data and prediction factor
    """
    return df.iloc[:, :-1], df.iloc[:, -1]


def train_test_split(X, y):
    """
    use like:

    X_train, X_test, y_train, y_test = ds.train_test_split(X, y)
    """
    return ms.train_test_split(X, y, test_size=0.2, random_state=123)


def mse(X, Y):
    return mean_squared_error(X, Y)


def rmse(X, Y):
    return np.sqrt(mean_squared_error(X, Y))
