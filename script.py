import pandas as pd
import numpy as np
from model_tools import fit_model, cross_validation, bespoke_cross_validation_2
from data_tools import data, get_poll_data, split_dataframe, k_folds, convert_to_xys
from math_tools import performance_metric, rmse


def classify_predictions(predictions_list, error_margin):
    """
    This function takes a list of numpy arrays containing the predictions output from a model, and determines which
    party wins each row (state), and classifies the likelihood rating based on the error_margin.
    :param predictions_list: A list of numpy arrays containing the predictions output from a model.
    :param error_margin: The error margin of the model, determined from the performance metric evaluated against the
    test set.
    :return: A tuple of numpy arrays for the list of parties winning each row, the list of likelihood ratings, and the
    margins for each row
    """
    n = len(predictions_list[0])  # number of rows
    parties = np.array(["A" for _ in range(n)])
    likelihoods = np.array(["AAAAAA" for _ in range(n)])
    margins = np.zeros(n)
    for i in range(n):
        D_opposition = max(predictions_list[1][i], predictions_list[2][i])
        R_opposition = max(predictions_list[0][i], predictions_list[2][i])
        Other_opposition = max(predictions_list[0][i], predictions_list[1][i])
        margin = 0
        if predictions_list[0][i] > D_opposition:  # Democrat win
            parties[i] = "D"
            margin = predictions_list[0][i] - D_opposition
        elif predictions_list[1][i] > R_opposition:  # Republican win
            parties[i] = "R"
            margin = predictions_list[1][i] - R_opposition
        elif predictions_list[2][i] > Other_opposition:  # Other win
            parties[i] = "Other"
            margin = predictions_list[2][i] - Other_opposition
        margins[i] = margin
        if margin < error_margin:
            likelihoods[i] = "Tilt"
        elif margin < 2 * error_margin:
            likelihoods[i] = "Lean"
        elif margin < 4 * error_margin:
            likelihoods[i] = "Likely"
        else:
            likelihoods[i] = "Safe"
    return parties, likelihoods, margins


def script():
    # SET UP TRAINING AND TEST DATA
    df = data.copy()
    train_data, test_data = split_dataframe(df, [0.7, 0.3])  # 70% into training, 30% into testing
    X_columns = ["Poll-D", "Poll-R", "Poll-Other"]
    y_columns = ['Result-D', 'Result-R', 'Result-Other']
    # CROSS-VALIDATION OF MODELS
    train_folds = k_folds(train_data, 20)  # Consider 20 folds of the training data
    orders = [i for i in range(5)]
    print("Perform cross-validation across 20 folds of the training data.")
    performances = bespoke_cross_validation_2(train_folds, X_columns, y_columns, orders, performance_metric)
    optimal_performance = 100  # dummy number, trying to minimise
    optimal_order = -1  # dummy number, refers to the model order
    for order, performance in performances.items():
        print(f'The performance for the model of order {order} was: {performance}')
        if performance < optimal_performance:
            optimal_performance = performance
            optimal_order = order
    print(f'Best performing model is of order {optimal_order}.')
    # TEST THE BEST MODEL
    print("Evaluate performance of chosen model against the test set.")
    training_xys = convert_to_xys(train_data, X_columns, y_columns)
    test_xys = convert_to_xys(test_data, X_columns, y_columns)
    result_D_array = test_data['Result-D'].to_numpy()
    result_R_array = test_data['Result-R'].to_numpy()
    result_O_array = test_data['Result-Other'].to_numpy()
    results_list = [result_D_array, result_R_array, result_O_array]
    predictions_list = [np.zeros(len(result_D_array)) for _ in range(len(training_xys))]
    model_names = ["Democrat", "Republican", "Other"]
    for i in range(len(training_xys)):  # i.e. range(3)
        print(f'Model: {model_names[i]}')
        X_train, y_train = training_xys[i]
        X_test, y_test = test_xys[i]
        model = fit_model(X_train, y_train, order=optimal_order)
        print(f'Coefficients: {model.named_steps["linear"].coef_}')
        print(f'Intercept: {model.named_steps["linear"].intercept_}')
        predictions_list[i] = model.predict(X_test)
    # Rescale predictions to sum to 1
    for i in range(len(predictions_list[0])):
        sum_preds = predictions_list[0][i] + predictions_list[1][i] + predictions_list[2][i]
        predictions_list[0][i] /= sum_preds
        predictions_list[1][i] /= sum_preds
        predictions_list[2][i] /= sum_preds
    df_predictions = pd.DataFrame({
        'pred-D': predictions_list[0],
        'pred-R': predictions_list[1],
        'pred-Other': predictions_list[2],
        'Result-D': result_D_array,
        'Result-R': result_R_array,
        'Result-Other': result_O_array
    })
    pd.set_option('display.max_columns', None)
    print(df_predictions)
    print(rmse(predictions_list, results_list))
    error_margin = performance_metric(predictions_list, results_list)
    print(error_margin)
    # MAKE PREDICTIONS ON CURRENT POLLING DATA
    print("Use chosen model to predict outcome based on current data.")
    current_polls_date = "20-Jul-24"  # To be changed with each review
    polls_data = get_poll_data(current_polls_date)
    print(polls_data.head())
    polls_X = polls_data[X_columns].to_numpy()
    overall_xys = convert_to_xys(df, X_columns, y_columns)
    predictions_list = [np.zeros(1) for _ in range(len(overall_xys))]
    for i in range(len(overall_xys)):
        print(f'Model: {model_names[i]}')
        overall_X, overall_y = overall_xys[i]
        model = fit_model(overall_X, overall_y, order=optimal_order)
        print(f'Coefficients: {model.named_steps["linear"].coef_}')
        print(f'Intercept: {model.named_steps["linear"].intercept_}')
        predictions_list[i] = model.predict(polls_X)
    # Rescale predictions to sum to 1
    for i in range(len(predictions_list[0])):
        sum_preds = predictions_list[0][i] + predictions_list[1][i] + predictions_list[2][i]
        predictions_list[0][i] /= sum_preds
        predictions_list[1][i] /= sum_preds
        predictions_list[2][i] /= sum_preds
    # Determine whether each state prediction gives to D or R, and give a rating from tilt to safe based on error margin
    parties, likelihoods, margins = classify_predictions(predictions_list, error_margin)
    # Express predictions as a percentage to 2 d.p.
    for i in range(len(predictions_list)):
        predictions_list[i] = np.around(100 * predictions_list[i], 2)
    # Print out the results as a dataframe
    df_results = pd.DataFrame({
        "State Alpha": polls_data.index.values,
        "Party win": parties,
        "Likelihood": likelihoods,
        "pred-D": predictions_list[0],
        "pred-R": predictions_list[1],
        "pred-O": predictions_list[2],
        "margin": margins
    }).set_index("State Alpha")
    df_results = df_results.sort_values(by="margin", ascending=False)
    df_results = df_results.drop("margin", axis=1)
    print(df_results)
    print([round(100*i*error_margin, 2) for i in [1, 2, 4]])
