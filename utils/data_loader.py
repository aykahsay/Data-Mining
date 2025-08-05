# Data Loading and Preprocessing Utilities
"""
This module contains functions for loading and preprocessing retail transaction data.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_transformed_data(filepath):
    """
    Load and prepare retail transaction data for analysis
    
    Parameters:
    filepath (str): Path to the CSV file
    
    Returns:
    pd.DataFrame: Preprocessed dataset with derived features
    """
    df = pd.read_csv(filepath)
    
    # Convert data types for proper analysis
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Quantity'] = df['Quantity'].astype(int)
    df['UnitPrice'] = df['UnitPrice'].astype(float)
    df['CustomerID'] = df['CustomerID'].astype(float)
    
    # Create derived features for analysis
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']  # Revenue per transaction
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
    df['Hour'] = df['InvoiceDate'].dt.hour
    
    print(f"Dataset loaded: {df.shape}")
    print(f"Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
    return df


def validate_data(df):
    """
    Validate the loaded dataset for common data quality issues
    
    Parameters:
    df (pd.DataFrame): Input dataset
    
    Returns:
    dict: Validation results
    """
    validation_results = {
        'total_rows': len(df),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'negative_quantities': (df['Quantity'] < 0).sum() if 'Quantity' in df.columns else 0,
        'negative_prices': (df['UnitPrice'] < 0).sum() if 'UnitPrice' in df.columns else 0,
        'missing_customer_ids': df['CustomerID'].isnull().sum() if 'CustomerID' in df.columns else 0
    }
    
    return validation_results


def clean_data(df, remove_negatives=True, remove_missing_customers=False):
    """
    Clean the dataset by removing problematic records
    
    Parameters:
    df (pd.DataFrame): Input dataset
    remove_negatives (bool): Remove negative quantities and prices
    remove_missing_customers (bool): Remove rows with missing customer IDs
    
    Returns:
    pd.DataFrame: Cleaned dataset
    """
    cleaned_df = df.copy()
    original_size = len(cleaned_df)
    
    if remove_negatives:
        if 'Quantity' in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df['Quantity'] > 0]
        if 'UnitPrice' in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df['UnitPrice'] > 0]
    
    if remove_missing_customers and 'CustomerID' in cleaned_df.columns:
        cleaned_df = cleaned_df.dropna(subset=['CustomerID'])
    
    print(f"Data cleaning complete: {original_size} -> {len(cleaned_df)} rows")
    return cleaned_df
