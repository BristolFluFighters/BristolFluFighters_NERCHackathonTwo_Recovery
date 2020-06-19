## Framework methodology with case study
The framework is built on a Holt-Winter’s Seasonal Smoothing model which can be used to predict future values in a time series based on the decomposition of a historical values into three categories: an overall trend, seasonal variation and remaining residuals. Below is an example of the average energy demand [MW] in the UK since 2012 which is shown alongside the deconstruction of these values into components previously mentioned.

![Decomposition of original signal](/img/seasonal_decomposition_not_smoothed.png)

It can be seen that the original values can successfully be decomposed into:
- A long term trend which is gradually declining, likely due to increased emphasis on energy efficiency and energy use;
- An annual cycle which peaks in the winter due to the use of central heating and lack of outdoor entertainment;
- Remaining residuals that can’t be accounted for by the other components

A Holt-Winter’s Seasonal Smoothing model requires that the data be statistically stationary, i.e. have constant mean and variance. A common way to check for this is to use an Augmented Dickey-Fuller test. The results of this test for this dataset are shown below.
ADF Statistic: -3.227
Critical Values:
- 1%: -3.432
- 5%: -2.862
- 10%: -2.567
p-value: 1.8%
It can be seen that the ADF statistic is between the critical values for 1% and 5% and has been calculated to be exactly 1.8% which is sufficient for the data set to be used as is. If the dataset failed this test then a number of transformations can be performed to make the data stationary.

There are a number of hyper-parameters, or settings, that are available to be altered to ensure the best predictions can be made. Therefore, we must explore different combinations of these hyper-parameters to evaluate which provide the most accurate, and robust model. To do this we split our dataset into a train and test set. We will subsequently train the model on the train set and evaluate its predictive performance on the test set. Assessing the model in this way, instead of fitting it on all the data, ensures that the trends the model is learning are general and that the model has not been overfitted. As the purpose of this model is to predict the value of a given metric if there had been no Covid-19 based behaviour changes, there are two datasets used for the model. One will contain data prior to the influence of the pandemic, defined as the start of 2020, and the other will include data up to the present day. For the hyper-parameter testing we shall split the first dataset in two: up to and including 2017 as the training set and 2018 onwards as the test set. We will show how this process works for two hyper-parameters: a smoothing window on the underlying data and one of the options for the model itself. Below is shown the training data, the prediction of the training data, the test data, and the prediction of the test data for the case with no smoothing and with a seven day rolling average.

![Hyper-parameter testing - not smoothed](/img/hyper-parameter_testing_not_smoothed_trend_add_seasonal_mul_damped.png)
![Hyper-parameter testing - smoothed](/img/hyper-parameter_testing_smoothed_trend_add_seasonal_mul_damped.png)

A visual inspection of these figures would indicate that the model has been fitted and predicted well. The Root Mean Squared Error (RMSE) denoted in the legend is used to quantify the differences between the observed and predicted data. It can be seen in both cases that the error is worse in the prediction as the model has not been fitted on this dataset. However, in the non smoothed set these values are similar but in the smoothed set they differ greatly which suggests that the model has been overfitted and is therefore not as general which will be detrimental to its prediction capabilities.

The other parameter to investigate is the damping option in the model itself. Below is a similar plot with the damping setting off and on.

![Hyper-parameter testing - not damped](/img/hyper-parameter_testing_not_smoothed_trend_add_seasonal_mul_not_damped.png)
![Hyper-parameter testing - damped](/img/hyper-parameter_testing_not_smoothed_trend_add_seasonal_mul_damped.png)

In this instance it is visually obvious that the predictions with the damping parameter off is worse than when it is on. This is confirmed by the large increase in the RMSE. Therefore, the remainder of the case study shall be performed using non smoothed data with the damping parameter on.

The dataset before the pandemic can now be used to create a model with the chosen hyper-parameters. The model can then be used to predict the values that would have been expected had there been no pandemic. Similarly, a model an be created using the dataset that includes the pandemic which can be used to predict the value for the rest of the year. Subsequently, the predictions for a year without a pandemic can be compared to the observed/predicted values for the year that will have been influenced by the changes in behaviour that Covid-19 has caused. Below is a comparison of the predicted values had the pandemic not happened with the actual values that have been observed.

![with-without comparison](/img/with_without_comparison_not_smoothed_trend_add_seasonal_mul_damped.png)

The difference between these two sets of values is the change in the given metric from what would have been expected. This reduction, along with the mean, are shown below.

![reduction](/img/estimated_reduction_not_smoothed_trend_add_seasonal_mul_damped.png)

It can be seen that the reduction in energy demand is almost always positive and shows a trend that increases with the severity of the pandemic, and its accompanying restrictions, but reduces in recent months and behaviour starts to return to normal.