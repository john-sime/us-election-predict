import numpy as np


def split_n_by_k(n, k):
    """
    This takes a value n which is being divided k ways, and outputs a list of integer segments which sum to n.
    :param n: An integer which is to be divided.
    :param k: An integer which is the divisor.
    :return: A list of integers, which are either equal to n/k rounded up or down. Rounded up numbers are presented
    first, e.g. split_n_by_k(38, 7) = [6, 6, 6, 5, 5, 5, 5].
    """
    output = []
    for i in range(k):
        piece = int(np.ceil(n / (k - i)))
        output.append(piece)
        n -= piece
    return output


def performance_metric(predictions, actual_y):
    """
    This function calculates the performance metric for a set of predictions against the actual y values. The metric is
    equal to the mean of |(y^_2-y^_1)-(y_2-y_1)|, where the predictions and actual ys are in the form [y_1, y_2, y_3].
    :param predictions: A list length-3 of numpy arrays containing the predictions for y_1, y_2 and y_3.
    :param actual_y: A list length-3 of numpy arrays containing the actual y values for y_1, y_2 and y_3.
    :return: A float equal to the mean of |(y^_2-y^_1)-(y_2-y_1)|
    """
    n = len(predictions[0])
    for i in range(1, 3):
        if len(predictions[i]) != n:
            raise ValueError("The number of predictions for each output variable must be the same.")
    for i in range(3):
        if len(actual_y[i]) != n:
            raise ValueError("The number of predictions must be equal to the number of actual y values for each "
                             "variable.")
    running_total = 0
    for i in range(n):
        running_total += abs(predictions[1][i] - predictions[0][i] - actual_y[1][i] + actual_y[0][i])
    return running_total / n


def rmse(predictions, actual_y):
    """
    This function calculates the root mean squared error for each column of predictions after comparing to the actual y
    values.
    :param predictions: A list of numpy arrays (the columns) containing the predictions for a number of output y
    variables.
    :param actual_y: A list of numpy arrays (the columns) containing the actual values for a number of output y
    variables.
    :return: A list of RMSEs calculated for each column.
    """
    if len(predictions) != len(actual_y):
        raise ValueError("The number of output variables (columns) should be equal for the predictions and actual "
                         "values")
    n = len(predictions[0])
    for i in range(1, len(predictions)):
        if len(predictions[i]) != n:
            raise ValueError("The number of predictions for each output variable must be the same.")
    for i in range(len(predictions)):
        if len(actual_y[i]) != n:
            raise ValueError("The number of predictions must be equal to the number of actual y values for each "
                             "variable.")
    output = [0 for _ in range(len(predictions))]
    for i in range(len(predictions)):
        output[i] = np.sqrt(np.mean(np.square(predictions[i] - actual_y[i])))
    return output
