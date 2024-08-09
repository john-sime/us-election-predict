import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from data_tools import convert_to_xys


def fit_model(X, y, order):
    """
    This function creates a scikit-learn regression object with polynomial features and fits it to the X and y data
    :param X: The input variables as a numpy array of dimensions (n,d), where n is the number of data points, and d is
    the dimensionality of the data.
    :param y: The output variable of the data as a numpy array.
    :param order: The order of the polynomial that the model is being fit to.
    :return: A scikit-learn regression object that has been fit to the data.
    """
    model = Pipeline([('poly', PolynomialFeatures(degree=order)),
                      ('linear', LinearRegression(fit_intercept=False))])
    model = model.fit(X, y)
    return model


def cross_validation(folds, X_columns, y_columns, orders, performance_metric_function):
    """
    This function that runs cross-validation on k-folds, where k is the length of the folds list, and then returns the
    mean values of the performance metric for each model.
    :param folds: A list of dataframes which represent the k folds in the dataset.
    :param X_columns: The columns in the dataframes that represent the X input variables.
    :param y_columns: The columns in the dataframes that represent the y output variables.
    :param orders: A list of integers for the polynomial orders of the models to be trained and validated.
    :param performance_metric_function: A function from which the performance is to be measured.
    :return: A dictionary containing the mean values across the folds of the data of the performance metric, for each
    order of model.
    """
    performances = {order: [] for order in orders}
    for i, fold in enumerate(folds):
        # Given the selected fold, create the training and validation sets, and separate into X,y numpy arrays
        validation_set = fold
        validation_xys = convert_to_xys(validation_set, X_columns, y_columns)
        training_folds = [folds[j] for j in range(len(folds)) if j != i]
        training_set = pd.concat(training_folds)
        training_xys = convert_to_xys(training_set, X_columns, y_columns)
        for order in orders:
            # Iterate for each model
            predictions_list = [0 for _ in range(len(training_xys))]  # i.e. [0, 0, 0]
            list_y_validate = [0 for _ in range(len(validation_xys))]  # i.e. [0, 0, 0]
            for j in range(len(training_xys)):  # also equal to the len of y_columns (i.e. 3)
                # Create, train and predict from the model for each y output variable
                X_train, y_train = training_xys[j]
                X_validate, y_validate = validation_xys[j]
                list_y_validate[j] = y_validate
                model = fit_model(X_train, y_train, order)
                predictions_list[j] = model.predict(X_validate)  # an array of predictions for X in validation set
            # Perform checks on predictions, and evaluate performance
            """
            if check_predictions(predictions_list):
                print(f'The predictions from order {order} passed the checks.')
            else:
                print(f'The predictions from order {order} failed the checks.')
            """
            performances[order].append(performance_metric_function(predictions_list, list_y_validate))
    average_performances = {}
    for order, performance_list in performances.items():
        average_performances[order] = np.mean(performance_list, axis=0)
    return average_performances


def bespoke_cross_validation(folds, X_columns, y_columns, evaluation_columns, orders, performance_metric_function):
    """
    This function runs cross validation across k folds for the various models, with predictions being adjusted before
    being assessed. The models predict the multiplier adjusters to be applied to the input variables in order to obtain
    predicted vote share %s, which in turn need to be adjusted so that the sum of vote shares equals 100%.
    :param folds: A list of dataframes which represent the k folds in the dataset.
    :param X_columns: The columns in the dataframes that represent the X input variables.
    :param y_columns: The columns in the dataframes that represent the y output variables.
    :param evaluation_columns: The columns in the dataframes that contain the values against which performance is to be
    evaluated.
    :param orders: A list of integers for the polynomial orders of the models to be trained and validated.
    :param performance_metric_function: A function from which the performance is to be measured.
    :return: A dictionary containing the mean values across the folds of the data of the performance metric, for each
    order of model.
    """
    performances = {order: [] for order in orders}
    input_columns = X_columns + [X_columns[-1]]
    for i, fold in enumerate(folds):
        # Given the selected fold, create the training and validation sets, and separate into X,y numpy arrays
        validation_set = fold
        validation_xys = convert_to_xys(validation_set, X_columns, y_columns)
        training_folds = [folds[j] for j in range(len(folds)) if j != i]
        training_set = pd.concat(training_folds)
        training_xys = convert_to_xys(training_set, X_columns, y_columns)
        for order in orders:
            # Iterate for each model
            predictions_list = [np.zeros(1) for _ in range(len(training_xys))]  # i.e. [[0], [0], [0], [0]]
            list_y_validate = [0 for _ in range(len(validation_xys))]  # i.e. [0, 0, 0, 0]
            for j in range(len(training_xys)):  # also equal to the len of y_columns (i.e. 4)
                # Create, train and predict from the model for each y output variable
                X_train, y_train = training_xys[j]
                X_validate, y_validate = validation_xys[j]
                list_y_validate[j] = validation_set[evaluation_columns[j]].to_numpy()
                model = fit_model(X_train, y_train, order)
                predictions = model.predict(X_validate)  # an array of predictions for X in validation set
                predictions_list[j] = predictions * validation_set[input_columns[j]].to_numpy()
            # Adjust the predictions and evaluate performance over the fold for the model
            for k in range(len(predictions_list[0])):
                # sum_preds = predictions_list[0][k] + predictions_list[1][k] + predictions_list[2][k] + \
                #             predictions_list[3][k]
                sum_preds = predictions_list[0][k] + predictions_list[1][k] + predictions_list[2][k]
                predictions_list[0][k] /= sum_preds
                predictions_list[1][k] /= sum_preds
                predictions_list[2][k] /= sum_preds
                # predictions_list[3][k] /= sum_preds
            performances[order].append(performance_metric_function(predictions_list, list_y_validate))
    average_performances = {}
    for order, performance_list in performances.items():
        average_performances[order] = np.mean(performance_list, axis=0)
    return average_performances


def bespoke_cross_validation_2(folds, X_columns, y_columns, orders, performance_metric_function):
    """
    This function runs cross validation across k folds for the various models, with predictions being adjusted before
    being assessed. The models predict the  vote share %s, which in turn need to be adjusted so that the sum of vote
    shares equals 100%.
    :param folds: A list of dataframes which represent the k folds in the dataset.
    :param X_columns: The columns in the dataframes that represent the X input variables.
    :param y_columns: The columns in the dataframes that represent the y output variables.
    :param orders: A list of integers for the polynomial orders of the models to be trained and validated.
    :param performance_metric_function: A function from which the performance is to be measured.
    :return: A dictionary containing the mean values across the folds of the data of the performance metric, for each
    order of model.
    """
    performances = {order: [] for order in orders}
    for i, fold in enumerate(folds):
        # Given the selected fold, create the training and validation sets, and separate into X,y numpy arrays
        validation_set = fold
        validation_xys = convert_to_xys(validation_set, X_columns, y_columns)
        training_folds = [folds[j] for j in range(len(folds)) if j != i]
        training_set = pd.concat(training_folds)
        training_xys = convert_to_xys(training_set, X_columns, y_columns)
        for order in orders:
            # Iterate for each model
            predictions_list = [np.zeros(1) for _ in range(len(training_xys))]  # i.e. [[0], [0], [0]]
            list_y_validate = [0 for _ in range(len(validation_xys))]  # i.e. [0, 0, 0]
            for j in range(len(training_xys)):  # also equal to the len of y_columns (i.e. 3)
                # Create, train and predict from the model for each y output variable
                X_train, y_train = training_xys[j]
                X_validate, y_validate = validation_xys[j]
                list_y_validate[j] = validation_set[y_columns[j]].to_numpy()
                model = fit_model(X_train, y_train, order)
                predictions_list[j] = model.predict(X_validate)  # an array of predictions for X in validation set
            # Adjust the predictions and evaluate performance over the fold for the model
            for k in range(len(predictions_list[0])):  # i.e. range(3)
                sum_preds = predictions_list[0][k] + predictions_list[1][k] + predictions_list[2][k]
                predictions_list[0][k] /= sum_preds
                predictions_list[1][k] /= sum_preds
                predictions_list[2][k] /= sum_preds
            performances[order].append(performance_metric_function(predictions_list, list_y_validate))
    average_performances = {}
    for order, performance_list in performances.items():
        average_performances[order] = np.mean(performance_list, axis=0)
    return average_performances


def check_predictions(predictions_list, tolerance=0.01):
    """
    This function takes a predictions from a model and performs some checks.
    :param predictions_list: A list with each element being a numpy array containing the predictions of the model(s).
    :param tolerance: The acceptable tolerance for predictions that either are below 0, or sum to more than 1.
    :return: A boolean, True indicating that the predictions passed the checks, False otherwise.
    """
    checks = True
    for i in range(1, len(predictions_list)):
        if len(predictions_list[i]) != len(predictions_list[0]):
            print("The predictions should be of equal length")
            checks = False
    less_than_0_count = 0
    sum_more_than_1_count = 0
    for j in range(len(predictions_list[0])):
        sum_prediction = 0
        for i in range(len(predictions_list)):
            if predictions_list[i][j] < -tolerance:
                less_than_0_count += 1
            sum_prediction += predictions_list[i][j]
        if sum_prediction > 1 + tolerance:
            sum_more_than_1_count += 1
    if less_than_0_count > 0:
        print(f"Some predictions had values of less than 0: {less_than_0_count} instances")
        checks = False
    if sum_more_than_1_count > 0:
        print(f"Some predictions summed to more than 1: {sum_more_than_1_count} instances")
        checks = False
    return checks
