import pathlib as pl
import os
import numpy as np
import pandas as pd
from math_tools import split_n_by_k


path_csv = pl.Path(os.getcwd()) / f'US Election Data - csv.csv'
with open(path_csv, 'rb') as file:
    data = pd.read_csv(file, index_col=[0, 1])


def get_poll_data(polls_at_date):
    """
    This function extracts polling data at the specified date from a csv file and converts it to a pandas Dataframe.
    :param polls_at_date: A string specifying the date for the file name, e.g. "17-Mar-24"
    :return: A pandas Dataframe containing the polling data
    """
    polls_path_csv = pl.Path(os.getcwd()) / f"Current Poll Data/US Election Data - Polls {polls_at_date}.csv"
    with open(polls_path_csv, 'rb') as polls_file:
        polls_data = pd.read_csv(polls_file, index_col=0)
    return polls_data


def split_dataframe(df, data_split):
    """
    function to divide a dataframe into training, validation and test dataframes
    :param df: the full dataframe which is to be divided
    :param data_split: a list containing the fraction of the full dataframe for each of training and test, in that order
    :return training, test: dataframes for each of the sets
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The data must be input as a Pandas Dataframe.")
    if len(data_split) != 2:
        raise ValueError("The data split should be a list length-2, with the proportions for the training and test "
                         "sets respectively.")
    if sum(data_split) != 1:
        raise ValueError("The data split should sum to 1.")
    if np.product(data_split) < 0:
        raise ValueError("The data split must not contain negative numbers.")
    training = df.sample(frac=data_split[0])
    test = df.drop(training.index)
    return training, test


def k_folds(dataframe, k):
    """
    This is a function that returns a list of k folds of the data. The returned value should be a list of dataframes
    :param dataframe: The input data as a Pandas dataframe.
    :param k: An integer for the number of folds to be made in the data.
    :return: A list of dataframes, where each element is a fold in the data.
    """
    # Create list of how long each fold should be. The folds should be as even as possible in number, but some may need
    # to have an extra data point if the total number of data points isn't divisible by n
    len_folds = split_n_by_k(len(dataframe), k)
    folds = []
    for i in range(k):
        data_ss = dataframe.sample(n=len_folds[i], random_state=20)
        dataframe = dataframe.drop(data_ss.index)
        folds.append(data_ss)
    return folds


def convert_to_xys(dataframe, X_columns, y_columns):
    """
    This function takes a dataframe, and outputs a tuple of numpy arrays for each y, where the tuple is in the form
    (X,y).
    :param dataframe: The data as a Pandas dataframe.
    :param X_columns: A list of the column names in the dataframe which represent the X input variables.
    :param y_columns: A list of the column names in the dataframe which represent the y output variables.
    :return: A list of tuples (X,y).
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("The data must be input as a Pandas Dataframe.")
    for X_column in X_columns:
        if X_column not in dataframe.columns:
            raise ValueError(f"Column specified in X_columns is not present in the dataframe: {X_column}")
    for y_column in y_columns:
        if y_column not in dataframe.columns:
            raise ValueError(f"Column specified in y_columns is not present in the dataframe: {y_column}")
        if y_column in X_columns:
            raise ValueError(f"A column specified in X_columns cannot also be a y column: {y_column}")
    output = [0 for _ in range(len(y_columns))]
    for i, y_column in enumerate(y_columns):
        y = dataframe[y_column].to_numpy()
        X = dataframe[X_columns].to_numpy()
        output[i] = (X, y)
    return output
