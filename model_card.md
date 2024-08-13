##Model Description
**Input:** The polling support for the Democratic party candidate, the Republican party candidate, and for the residual uncommitted/third party support.

**Outputs:** The predicted vote share for the Democratic party candidate, the Republican party candidate, and for other candidates.

**Model Architecture:** The underlying model is a Pipeline Linear Regressor that considers polynomial features.

##Performance
Model performance is measured as the mean absolute error on the Republican margin (i.e. predicted Republican vote % less predicted Democrat vote %, minus the actual Republican vote % less actual Democrat vote %).
Note that this measure is equivalent to the mean abolsute error on the Democrat margin.
Cross-validation and testing of the model was performed to first select the polynomial order for the final model, and to evaluated to performance of the model against an unseen test set.
To achieve this the data was randomly split into a training set and test set according to a 70-30 split. The cross-validation was performed along the training set over 20 folds in series.

The performance of the polynomial order 1 (i.e. Linear) model during cross-validation was 3.94%, and was 3.43% on the test set.

The root mean squared error (rmse) was also considered for each of the outputs individually against the test set.
The model for predicting the Democrat vote % had a rmse of 2.15%, whereas the models for predicting the Republican vote % and the Other vote % had rmses of 2.65% and 2.78% respectively.

##Limitations
The model is trained exclusively on US election and polling data, and is not appropriate for use on any other elections.

It should be noted that the final pre-election polls tend to have a very low level of "Other" support when compared to the polls in the current 2024 election cycle.
It is typical for polls that are taken several months prior to an election to have a higher level of "Other" support, though it should also be noted that the independent candidate Kennedy has a significant, albeit uncompetitive level of support in the polls for the 2024 election.

This difference in "Other" support in the current polls when compared to the training dataset may lead to inaccuracies in the model predictions.

##Trade-offs
The final model's linear regression formulae show a sensitivity to the degree of "Other" support in the inputs. Therefore states that have significant levels of "Other" support may produce inaccurate predictions.
