from sklearn.linear_model import LinearRegression
import pandas as pd
import math
from .data_access import DataSet
import numpy as np

def define_year(df_mask, year, fun):
    if year is None:
        year = fun(df_mask.index)
    
    if isinstance(year, type(str())):
        year = pd.to_datetime(year, format="%Y")

    return year

def mask_dateindex(
    df, df_mask, 
    min_year=None,
    max_year=None,
):
    min_year = define_year(df_mask, min_year, np.min)
    max_year = define_year(df_mask, max_year, np.max)

    return (
        (df.index >= min_year) & (df.index <= max_year) 
    )

def linear_fit(data, fit_df=None):
    if fit_df is None:
        fit_df = pd.DataFrame(columns=data.columns, index=data.columns)

    for col_pred in fit_df:
        for col_known in fit_df[col_pred].index:
            try:
                fit_df.loc[col_known, col_pred] = LinearRegression().fit(
                    data[col_known].values.reshape(-1, 1),
                    data[col_pred].values.reshape(-1, 1)
                )
            except ValueError as eid:
                print(f"Linear regression failed for: '{col_pred}' fit to  '{col_known}':")
                print(f"  Message: {eid}")
    return fit_df

def correlate(
    selector:dict,
    data_sets:[dict, DataSet],
    main_compare:str,
    min_year=None,
    max_year=None,
):
    """ Correlate specific columns of datasets together

    This also returns a linear fit between them.
    """
    data_sets_corr = [c for c in selector if c != main_compare]
    corrs = []
    merged_data = []
    for dataset in data_sets_corr:
        ref_mask = mask_dateindex(data_sets[main_compare], data_sets[dataset])
        targ_mask = mask_dateindex(data_sets[dataset], data_sets[main_compare])
        merged_data.append(
            pd.merge_asof(
                data_sets[main_compare].loc[ref_mask, selector[main_compare]], 
                data_sets[dataset].loc[targ_mask, selector[dataset]], 
                left_index=True, right_index=True, direction='nearest'
            )
        )
        corrs.append(
            merged_data[-1].corr(method='spearman')
            .loc[selector[main_compare], selector[dataset]]
        )

    lin_fit = []
    for corr, data in zip(corrs, merged_data):
        lin_fit.append(
            linear_fit(data, fit_df=pd.DataFrame().reindex_like(corr))
        )

    corr_dict = {}
    for dset, corr, data, fit in zip(data_sets_corr, corrs, merged_data, lin_fit):
        corr_dict[dset] = {
            'correlation': corr,
            'data': data,
            'fit': fit,
        }

    return corr_dict

def apply_prediction(fit_df, x_values, x_col_map=None):
    """ Returns a prediction for the columns of "fit_df" 

    This function applies the model specified in fit_df to the dataframe 
    """
    if x_col_map is None:
        x_col_map = {c:c for c in x_values}

    df_pred = pd.DataFrame(columns=["predictor", "predictor_value", *fit_df.columns])
    for col_pred in x_values:
        df_temp = pd.DataFrame(columns=fit_df.columns, index=x_values.index)
        df_temp["predictor"] = col_pred
        df_temp["predictor_value"] = x_values[col_pred]
        for y_col in fit_df.columns:
            try:
                df_temp[y_col] = fit_df.loc[x_col_map[col_pred], y_col].predict(
                    x_values[col_pred].values.reshape(-1, 1)
                )
            except AttributeError as identifier:
                df_temp[y_col] = np.nan

        df_pred = pd.concat([df_pred, df_temp])
    df_pred.set_index(
        pd.MultiIndex.from_arrays(
            [df_pred["predictor"], df_pred.index],
            names=('predictor', 'date')
        ), inplace=True
    )
    df_pred.drop("predictor",inplace=True, axis=1)
    return df_pred

def display_correlations(correlation_dict, display_fun=print):
    for dset in correlation_dict:
        print("=====================================================================")
        print(f"Pearson correlation coefficients in dataset '{dset}'")
        min_d = correlation_dict[dset]['data'].index.min()
        max_d = correlation_dict[dset]['data'].index.max()
        print(f"\t on data from {min_d.year} to {max_d.year} (inclusive)")
        print("_________________________________________________________")
        display_fun(
            correlation_dict[dset]['correlation']
            .style.background_gradient().set_precision(3)
        )
        print("=====================================================================")
        print("")


def predict_correlation_model(
    independant_variable,
    correlation_dict,
):
    col_with_corona = [c for c in independant_variable if "_with_corona" in c][0]
    col_without_corona = [c for c in independant_variable if "_without_corona" in c][0]
    cols_of_interest = [col_with_corona, col_without_corona]
    independant_variable.drop(
        [c for c in independant_variable if c not in cols_of_interest],
        axis='columns', inplace=True
    )

    pred = apply_prediction(
        correlation_dict['fit'],
        independant_variable,
        {c: 'demand' for c in independant_variable}  # Use only demand
    )

    difference = pred.loc[col_with_corona]-pred.loc[col_without_corona]
    ratio = (difference)/pred.loc[col_without_corona]

    difference["quantity"] = "absolute difference"
    ratio["quantity"] = "relative difference"

    return pred, difference.append(ratio)