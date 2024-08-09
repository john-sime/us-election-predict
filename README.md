# us-election-predict
# Description of the problem
The purpose of this model is to investigate the bias in US presidential election polling, and to attempt to make predictions based on recent polling data for the 2024 election.
Areas of particular interest are how bias may vary between Democrat and Republican strongholds and in battleground states, as well as how the uncommitted/other proportion of the electorate in a state impacts on this bias.
# Data - used for model training and predictions
The data used to train the model has been collated by myself from various sources. The complete spreadsheet including notes on data cleaning and data sources can be found at:

https://docs.google.com/spreadsheets/d/1byPOPY8E6ImigvaPBOo7npWcA5zB4IWwFhoRuKYUzpg/edit?usp=sharing

The highlights are as follows:
* The inputs for training the model are the final polls before the 2016 and 2020 US elections, with a breakdown state by state (and congressional district where applicable). These are divided into poll % shares for the Democrat candidate, the Republican candidate and a third column for the residual (denoted as "other").
* The outputs for training the model are the actual election results from 2016 and 2020, also broken down by state and congressional district.
* The inputs for making predictions using the model are the polls in each state (and congressional district if available) in the lead up to 20 July 2024. Since President Biden stood down as a Presidential candidate on 21 July 2024, the predictions made by the model could be considered as a projection of the scenario where President Biden continued to be the Democrat candidate in 2024.
# Methodology and assumptions
The model used for this project is a Linear Regression model using polynomial features. The polynomial orders that were considered are those from 0 order (i.e. constant) to the 5th order ( i.e. quintic formula for each feature). Seperate models of the chosen polynomial order are used to predict Democrat, Republican and "other" vote share %s, with the predictions then normalised so that they add to 100%.

The assumptions taken in this model and approach are as follows:
* That the relationship between polls and results can be effectively described using a polynomial relationship
* That the predictor variables are normally distributed
* That the variances for each of the predictor variables are broadly consistent
* That the bias in polling from 2016 and 2020 will be consistent with the bias in polling for 2024

The data set was split to be 70% training data and 30% test data. Cross-validation over 20 folds of the training data was performed for each of the considered polynomial orders. The performance metric chosen to evaluate the models in the cross-validation is the mean abolsute error on the Republican margin (i.e. predicted Republican vote % minus predicted Democrat vote %, versus actual Republican vote % minus Democrat vote %). Note that this metric is the equivalent to the mean absolute error on the Democrat margin.

The polynomial order that had the best performance from the cross-validation was order 1 (i.e. linear formula for each feature), with a mean absolute error on margin of 3.94%. The polynomial order 2 models (i.e. quadratic models) had a mean absolute error on margin of 3.99%, so this could also be a suitable model to consider.
The chosen model (polynomial order 1) was then tested against the test set to verify the performance level and evaluate the error margin of the model. The predictions versus actual outputs in the test set are detailed below:

      pred-D    pred-R      pred-Other  Result-D  Result-R      Result-Other
      0.346694  0.631832    0.021474    0.3657    0.6203        0.0139
      0.416379  0.544029    0.039592    0.4277    0.5283        0.0439
      0.319456  0.654471    0.026073    0.3478    0.6240        0.0283
      0.524905  0.431116    0.043979    0.5540    0.4190        0.0271
      0.395828  0.573662    0.030511    0.4151    0.5614        0.0235
      0.371436  0.615102    0.013461    0.3615    0.6209        0.0176
      0.530375  0.432010    0.037615    0.5309    0.4402        0.0288
      0.578548  0.358191    0.063261    0.6011    0.3702        0.0287
      0.439690  0.482594    0.077716    0.4482    0.5226        0.0291
      0.616585  0.312720    0.070695    0.6536    0.3215        0.0249
      0.656846  0.279356    0.063798    0.6560    0.3214        0.0225
      0.497667  0.453755    0.048578    0.5240    0.4528        0.0233
      0.432632  0.540332    0.027036    0.4055    0.5692        0.0254
      0.196947  0.807546   -0.004493    0.2234    0.7536        0.0230
      0.542178  0.458956   -0.001134    0.5271    0.4536        0.0194
      0.468169  0.510547    0.021285    0.4859    0.4993        0.0148
      0.598114  0.404247   -0.002360    0.5645    0.4037        0.0318
      0.687793  0.276456    0.035751    0.6609    0.3067        0.0324
      0.525134  0.424053    0.050814    0.5457    0.4093        0.0451
      0.364825  0.605755    0.029420    0.3845    0.5809        0.0346
      0.486406  0.445633    0.067961    0.4783    0.4487        0.0730
      0.587213  0.357513    0.055273    0.6001    0.3281        0.0718
      0.479070  0.458654    0.062277    0.4644    0.4492        0.0864
      0.339612  0.565999    0.094389    0.3575    0.5617        0.0808
      0.457252  0.491829    0.050919    0.4792    0.4550        0.0658
      0.462626  0.468237    0.069137    0.4698    0.4661        0.0641
      0.572160  0.395326    0.032514    0.5901    0.3652        0.0448
      0.469321  0.510535    0.020144    0.4617    0.4983        0.0400
      0.502621  0.443113    0.054266    0.5007    0.3909        0.1084
      0.343879  0.576547    0.079574    0.3174    0.6153        0.0673
      0.613261  0.336063    0.050676    0.5668    0.3027        0.1305
      0.529859  0.420474    0.049667    0.5254    0.3683        0.1063
      0.292867  0.657096    0.050036    0.2643    0.6850        0.0507

The root mean squared errors on these predictions for the Democrat, Republican and other models were 2.15%, 2.65% and 2.78% respectively. The error margin, calculated as the mean abolsute error on margin was 3.43%, which is broadly similar (and better) than the performance metric for the model during cross-validation.

# Results and comments on bias
After retraining the models using the whole datasets, the models can then be used to make predictions based on the recent polling for the 2024 election. The formulae produced from training the models are:
* Democrat model: D = 0.20284186 + 0.87949739 * d - 0.30151956 * r - 0.28721582 * o
* Republican model: R = -4.43007293 + 4.37198629 * d + 5.54786465 * r + 4.50305536 * o
* Other model: O = 5.22353513 - 5.24779223 * d - 5.24266692 * r - 4.21208382 * o

(note that d, r and o are the predictors representing the polling data for Democrats, Republicans and other respectively)

These formulae look a little weird, however when you consider that d+r+o=1 (i.e. vote share equals 100%) and let m=r-d (the Republican margin), then these formulae transform into:
* Democrat model: D = 0.491830775 - 0.590508475 * m - 0.576204735 * o
* Republican model: R = 0.52985254 + 0.58793918 * m - 0.45687011 * o
* Other model: O = -0.021694445 + 0.002562655 * m + 1.033145755 * o

In particular note the formula for the predicted Republican margin allows us to identify some factors relating to the biases in the polling data:
* R-D = 0.038021765 + 1.178447655 * m + 0.119334625 * o
* The constant term represents an inherent bias in the polling in favour of the Democrat candidates from 2016 and 2020, that amounts to approximately 3.8%
* The margin coefficient represents a bias where the polls underestimate results in Democrat/Republican strongholds, amounting to approximately 17.8% of the margin
* The other coefficient represents a bias where polls with uncommitted/third party supporters underestimate the Republican vote share, representing a net swing equivalent of 11.9% of the reported uncommitted/third party support

An example breakdown of the 20 July 2024 polls compared to the prediction from the model is as follows (using the polls/predicted result for New Mexico):
* Poll margin      D+2      (poll reports D 49% and R 47%)
* Margin adj.      D+0.36   (margin underestimation adjustment: 17.8% of D+2)
* Other adj.       R+0.48   (net swing to R from other: 11.9% of 4% residual)
* Inherent bias    R+3.80
* Prediction       R+1.92

Using the error margin calculated against the test set (3.43%), we can classify each predicted result as "Tilt", "Lean" or "Likely" if the predicted margin is within 1, 2 or 4 error margins respectively, or "Safe" if the predicted margin is more than 4 error margins. The predicted results for each race is outlined in the table below and in the image of the projected electoral map. Note that no polls have been released for Delaware or the District of Columbia (3 Electoral votes each) or for the 1st and 3rd Congressional Districts of Nebraska (1 Electoral vote each) - this is presumably because the former 2 are solid Democrat strongholds, and the latter 2 are similarly solid for Republicans.

      State Alpha   Party win Likelihood  pred-D  pred-R  pred-O
      WY            R           Safe       8.09   76.38   15.53
      ND            R           Safe      23.34   68.41    8.25
      AR            R           Safe      18.75   63.71   17.54
      UT            R           Safe      19.92   63.58   16.51
      OK            R           Safe      25.69   67.10    7.21
      KY            R           Safe      21.11   61.35   17.53
      ID            R           Safe      21.11   61.35   17.53
      TN            R           Safe      23.42   62.66   13.92
      WV            R           Safe      23.44   61.09   15.46
      VT            D           Safe      59.41   28.89   11.70
      IN            R           Safe      30.44   60.31    9.25
      SD            R           Safe      27.02   55.48   17.51
      AK            R           Safe      32.78   60.04    7.18
      AL            R           Safe      34.51   61.42    4.08
      MT            R           Safe      32.22   58.54    9.24
      MS            R           Safe      32.79   59.00    8.21
      KS            R           Safe      27.06   52.34   20.60
      MD            D           Safe      56.47   31.30   12.23
      ME-2          R           Safe      20.09   51.04   28.88
      SC            R           Safe      34.00   55.73   10.26
      LA            R           Safe      35.15   56.65    8.20
      MO            R           Safe      40.92   61.22   -2.13
      CA            D           Safe      52.95   33.26   13.79
      IA            R           Safe      36.34   55.47    8.19
      HI            D           Safe      57.52   39.53    2.95
      NE-AL         R           Safe      34.64   51.49   13.87
      OH            R           Safe      38.67   55.21    6.12
      TX            R           Safe      39.25   55.14    5.60
      MA            D           Safe      45.98   31.44   22.58
      NV            R         Likely      39.05   51.66    9.28
      AZ            R         Likely      39.10   51.62    9.27
      FL            R         Likely      39.11   50.99    9.90
      WA            D         Likely      49.38   38.36   12.26
      NC            R         Likely      41.17   50.86    7.97
      PA            R         Likely      41.69   51.22    7.09
      OR            D         Likely      51.66   42.28    6.06
      GA            R         Likely      41.77   51.06    7.17
      NY            D         Likely      51.65   43.32    5.03
      NH            R         Likely      39.94   47.77   12.30
      MI            R         Likely      41.03   48.69   10.29
      NJ            R         Likely      37.64   44.89   17.46
      WI            R         Likely      42.82   49.77    7.41
      CO            D           Lean      49.33   42.54    8.14
      NE-2          R           Lean      39.96   45.68   14.36
      CT            D           Lean      48.16   42.67    9.17
      IL            D           Lean      41.24   37.19   21.57
      VA            R           Lean      43.38   47.43    9.19
      ME-1          D           Tilt      36.62   34.58   28.80
      NM            R           Tilt      48.06   49.98    1.96
      MN            R           Tilt      45.76   47.63    6.61
      ME-AL         R           Tilt      50.36   51.81   -2.17
      RI            D           Tilt      37.76   36.53   25.71

# Final Comments
The projected results in the table above and in the electoral map image would represent a considerable landslide for President Trump in the scenario where President Biden continued to be the Democrat candidate. The main contributing factors for this prediction from the machine learning models are:
* The poor performance in the polls from President Biden in the period leading up to his stepping down as the candidate
* The bias in the polling from the 2016 and 2020 elections, that incorrectly predicted the vote shares in those elections favouring the Democrat candidate by a considerable margin on both occasions, relative to the actual results.

Some flaws in the model arise in states where there is a considerable amount of uncommitted voters/third party support. An obvious example is in Rhode Island, which is typically considered to be a Democrat stronghold, yet the model predicts that it will be a close race. This is due to the training data having very few states with a high proportion of voters in the "other" category, yet the poll for Rhode Island had 27% as uncommitted to either of the main two parties. Other examples of this situation are in the congressional districts of Maine, Massachusetts, Illinois, Kansas and New Jersey, each of which have been predicted to be more Republican than they are likely to actually be.

I would note that the model used for this project is not very sophisticated, but it was chosen due to it being easily interpretable once the coefficients from the Regression were extracted.

With additional scope for the project, I would like to consider other types of machine learning models, such as Regression Decision Trees, and compare the error margins and predictions of the other models.
