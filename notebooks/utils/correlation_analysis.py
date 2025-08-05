# Correlation Analysis Utilities
"""
This module contains functions for correlation analysis and relationship exploration.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr, kendalltau


def correlation_analysis(df, method='pearson', figsize=(10, 8)):
    """
    Generate correlation matrix and heatmap visualization
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    method (str): Correlation method ('pearson', 'spearman', 'kendall')
    figsize (tuple): Figure size for heatmap
    
    Returns:
    pd.DataFrame: Correlation matrix
    """
    # Select only numerical columns
    numerical_df = df.select_dtypes(include=[np.number])
    corr_matrix = numerical_df.corr(method=method)
    
    # Create correlation heatmap with upper triangle mask
    plt.figure(figsize=figsize)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # Hide upper triangle
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": .8})
    plt.title(f'{method.capitalize()} Correlation Matrix')
    plt.tight_layout()
    plt.show()
    
    return corr_matrix


def significant_correlations(corr_matrix, threshold=0.5):
    """
    Extract correlations above specified threshold
    
    Parameters:
    corr_matrix (pd.DataFrame): Correlation matrix
    threshold (float): Correlation threshold
    
    Returns:
    pd.DataFrame: Significant correlations
    """
    # Get upper triangle of correlation matrix
    upper_tri = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    
    # Find correlations above threshold
    significant_corr = []
    for col in upper_tri.columns:
        for idx in upper_tri.index:
            if not pd.isna(upper_tri.loc[idx, col]) and abs(upper_tri.loc[idx, col]) >= threshold:
                significant_corr.append({
                    'Variable_1': idx,
                    'Variable_2': col,
                    'Correlation': upper_tri.loc[idx, col],
                    'Abs_Correlation': abs(upper_tri.loc[idx, col]),
                    'Strength': 'Strong' if abs(upper_tri.loc[idx, col]) >= 0.7 else 'Moderate'
                })
    
    return pd.DataFrame(significant_corr).sort_values('Abs_Correlation', ascending=False)


def correlation_with_target(df, target_column, method='pearson', top_n=10):
    """
    Calculate correlations with a specific target variable
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    target_column (str): Target variable name
    method (str): Correlation method
    top_n (int): Number of top correlations to return
    
    Returns:
    pd.DataFrame: Correlations with target variable
    """
    numerical_df = df.select_dtypes(include=[np.number])
    
    if target_column not in numerical_df.columns:
        raise ValueError(f"Target column '{target_column}' not found in numerical columns")
    
    correlations = numerical_df.corr(method=method)[target_column].drop(target_column)
    correlations = correlations.sort_values(key=abs, ascending=False)
    
    correlation_df = pd.DataFrame({
        'Variable': correlations.index,
        'Correlation': correlations.values,
        'Abs_Correlation': abs(correlations.values)
    })
    
    return correlation_df.head(top_n)


def plot_correlation_scatter(df, x_col, y_col, figsize=(10, 6)):
    """
    Create scatter plot with correlation statistics
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    x_col (str): X-axis column
    y_col (str): Y-axis column
    figsize (tuple): Figure size
    """
    # Calculate correlations
    pearson_corr, pearson_p = pearsonr(df[x_col].dropna(), df[y_col].dropna())
    spearman_corr, spearman_p = spearmanr(df[x_col].dropna(), df[y_col].dropna())
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Scatter plot
    axes[0].scatter(df[x_col], df[y_col], alpha=0.6)
    axes[0].set_xlabel(x_col)
    axes[0].set_ylabel(y_col)
    axes[0].set_title(f'Scatter Plot: {x_col} vs {y_col}')
    
    # Add trend line
    z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
    p = np.poly1d(z)
    axes[0].plot(df[x_col], p(df[x_col]), "r--", alpha=0.8)
    
    # Correlation heatmap for these two variables
    corr_subset = df[[x_col, y_col]].corr()
    sns.heatmap(corr_subset, annot=True, cmap='coolwarm', center=0, ax=axes[1])
    axes[1].set_title('Correlation Heatmap')
    
    # Add correlation statistics as text
    stats_text = f'Pearson r: {pearson_corr:.3f} (p={pearson_p:.3f})\n'
    stats_text += f'Spearman ρ: {spearman_corr:.3f} (p={spearman_p:.3f})'
    
    plt.figtext(0.02, 0.02, stats_text, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
    
    plt.tight_layout()
    plt.show()


def correlation_matrix_comparison(df, methods=['pearson', 'spearman', 'kendall'], figsize=(15, 5)):
    """
    Compare correlation matrices using different methods
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    methods (list): List of correlation methods to compare
    figsize (tuple): Figure size
    """
    numerical_df = df.select_dtypes(include=[np.number])
    n_methods = len(methods)
    
    fig, axes = plt.subplots(1, n_methods, figsize=figsize)
    if n_methods == 1:
        axes = [axes]
    
    for i, method in enumerate(methods):
        corr_matrix = numerical_df.corr(method=method)
        
        # Create heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', 
                   center=0, square=True, ax=axes[i], cbar_kws={"shrink": .8})
        axes[i].set_title(f'{method.capitalize()} Correlation')
    
    plt.tight_layout()
    plt.show()
