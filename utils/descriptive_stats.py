# Descriptive Statistics Utilities
"""
This module contains functions for generating comprehensive descriptive statistics.
"""

import pandas as pd
import numpy as np
from scipy import stats


def generate_descriptive_stats(df, numerical_cols=None):
    """
    Generate comprehensive descriptive statistics for numerical columns
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    numerical_cols (list): List of numerical columns to analyze
    
    Returns:
    dict: Dictionary containing statistical measures for each column
    """
    if numerical_cols is None:
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    stats_dict = {}
    for col in numerical_cols:
        if col in df.columns:
            data = df[col].dropna()  # Remove missing values
            stats_dict[col] = {
                'count': len(data),
                'mean': data.mean(),
                'median': data.median(),
                'std': data.std(),
                'min': data.min(),
                'max': data.max(),
                'q25': data.quantile(0.25),
                'q75': data.quantile(0.75),
                'iqr': data.quantile(0.75) - data.quantile(0.25),
                'skewness': stats.skew(data),    # Measure of asymmetry
                'kurtosis': stats.kurtosis(data) # Measure of tail heaviness
            }
    return stats_dict


def display_stats_table(stats_dict):
    """
    Convert statistics dictionary to formatted DataFrame
    
    Parameters:
    stats_dict (dict): Dictionary containing statistical measures
    
    Returns:
    pd.DataFrame: Formatted statistics table
    """
    return pd.DataFrame(stats_dict).T.round(4)


def calculate_outliers(df, columns, method='iqr', factor=1.5):
    """
    Identify outliers in specified columns using IQR or Z-score method
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    columns (list): List of columns to analyze
    method (str): Method to use ('iqr' or 'zscore')
    factor (float): Multiplication factor for IQR method
    
    Returns:
    dict: Dictionary containing outlier information for each column
    """
    outliers_dict = {}
    
    for col in columns:
        if col in df.columns:
            data = df[col].dropna()
            
            if method == 'iqr':
                q1 = data.quantile(0.25)
                q3 = data.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - factor * iqr
                upper_bound = q3 + factor * iqr
                outliers = data[(data < lower_bound) | (data > upper_bound)]
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(data))
                outliers = data[z_scores > factor]
            
            outliers_dict[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(data)) * 100,
                'values': outliers.tolist()[:10]  # Show first 10 outliers
            }
    
    return outliers_dict


def summary_statistics(df):
    """
    Generate a comprehensive summary of the dataset
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    dict: Summary statistics
    """
    summary = {
        'shape': df.shape,
        'memory_usage': df.memory_usage(deep=True).sum(),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict(),
        'numerical_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist()
    }
    
    return summary
