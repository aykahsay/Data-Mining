# Distribution Analysis Utilities
"""
This module contains functions for analyzing data distributions and testing normality.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import normaltest, shapiro, kstest, jarque_bera


def analyze_distributions(df, columns, figsize=(15, 10)):
    """
    Create histograms and box plots to analyze data distributions
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    columns (list): List of columns to analyze
    figsize (tuple): Figure size for plots
    """
    n_cols = len(columns)
    fig, axes = plt.subplots(2, n_cols, figsize=figsize)
    if n_cols == 1:
        axes = axes.reshape(-1, 1)
    
    for i, col in enumerate(columns):
        data = df[col].dropna()
        
        # Histogram shows frequency distribution
        axes[0, i].hist(data, bins=50, alpha=0.7, edgecolor='black')
        axes[0, i].set_title(f'Distribution of {col}')
        axes[0, i].set_xlabel(col)
        axes[0, i].set_ylabel('Frequency')
        
        # Box plot shows quartiles and outliers
        axes[1, i].boxplot(data)
        axes[1, i].set_title(f'Box Plot of {col}')
        axes[1, i].set_ylabel(col)
    
    plt.tight_layout()
    plt.show()


def test_normality(df, columns, alpha=0.05):
    """
    Test if data follows normal distribution using multiple statistical tests
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    columns (list): List of columns to test
    alpha (float): Significance level
    
    Returns:
    pd.DataFrame: Results of normality tests
    """
    results = []
    
    for col in columns:
        data = df[col].dropna()
        
        # Use sample for large datasets to avoid computational issues
        sample_data = data.sample(5000, random_state=42) if len(data) > 5000 else data
        
        # Shapiro-Wilk test (best for small samples)
        shapiro_stat, shapiro_p = shapiro(sample_data)
        
        # D'Agostino's normality test (good for larger samples)
        if len(data) >= 8:
            dagostino_stat, dagostino_p = normaltest(data)
        else:
            dagostino_stat, dagostino_p = np.nan, np.nan
        
        # Jarque-Bera test
        if len(data) >= 2:
            jb_stat, jb_p = jarque_bera(data)
        else:
            jb_stat, jb_p = np.nan, np.nan
        
        results.append({
            'Column': col,
            'Shapiro_Stat': shapiro_stat,
            'Shapiro_p': shapiro_p,
            'Shapiro_Normal': shapiro_p > alpha,
            'DAgostino_Stat': dagostino_stat,
            'DAgostino_p': dagostino_p,
            'DAgostino_Normal': dagostino_p > alpha if not np.isnan(dagostino_p) else np.nan,
            'JarqueBera_Stat': jb_stat,
            'JarqueBera_p': jb_p,
            'JarqueBera_Normal': jb_p > alpha if not np.isnan(jb_p) else np.nan
        })
    
    return pd.DataFrame(results)


def plot_distribution_comparison(df, column, figsize=(12, 8)):
    """
    Create a comprehensive distribution plot with multiple visualizations
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    column (str): Column to analyze
    figsize (tuple): Figure size
    """
    data = df[column].dropna()
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Histogram with KDE
    axes[0, 0].hist(data, bins=50, density=True, alpha=0.7, edgecolor='black')
    data.plot.kde(ax=axes[0, 0], color='red', linewidth=2)
    axes[0, 0].set_title(f'Histogram + KDE: {column}')
    axes[0, 0].set_xlabel(column)
    axes[0, 0].set_ylabel('Density')
    
    # Box plot
    axes[0, 1].boxplot(data)
    axes[0, 1].set_title(f'Box Plot: {column}')
    axes[0, 1].set_ylabel(column)
    
    # Q-Q plot
    from scipy import stats
    stats.probplot(data, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title(f'Q-Q Plot: {column}')
    
    # Violin plot
    axes[1, 1].violinplot([data])
    axes[1, 1].set_title(f'Violin Plot: {column}')
    axes[1, 1].set_ylabel(column)
    
    plt.tight_layout()
    plt.show()


def distribution_summary(df, columns):
    """
    Generate a summary of distribution characteristics
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    columns (list): List of columns to analyze
    
    Returns:
    pd.DataFrame: Distribution summary
    """
    from scipy import stats
    
    summary_data = []
    
    for col in columns:
        data = df[col].dropna()
        
        summary_data.append({
            'Column': col,
            'Mean': data.mean(),
            'Median': data.median(),
            'Mode': data.mode().iloc[0] if not data.mode().empty else np.nan,
            'Std': data.std(),
            'Skewness': stats.skew(data),
            'Kurtosis': stats.kurtosis(data),
            'Min': data.min(),
            'Max': data.max(),
            'Range': data.max() - data.min()
        })
    
    return pd.DataFrame(summary_data)
