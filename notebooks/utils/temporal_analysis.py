# Temporal Analysis Utilities
"""
This module contains functions for analyzing temporal patterns in transaction data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def temporal_analysis(df):
    """
    Analyze transaction patterns across different time dimensions
    
    Parameters:
    df (pd.DataFrame): Input dataframe with transaction data
    
    Returns:
    dict: Dictionary containing temporal analysis results
    """
    temporal_stats = {}
    
    # Daily aggregations - sum revenue and count unique transactions/customers
    daily_stats = df.groupby(df['InvoiceDate'].dt.date).agg({
        'TotalAmount': 'sum',
        'InvoiceNo': 'nunique',
        'CustomerID': 'nunique',
        'Quantity': 'sum'
    })
    daily_stats.columns = ['Daily_Revenue', 'Daily_Transactions', 'Daily_Customers', 'Daily_Quantity']
    
    # Monthly aggregations using period to avoid naming conflicts
    year_month = df['InvoiceDate'].dt.to_period('M')  # Group by month-year periods
    monthly_stats = df.groupby(year_month).agg({
        'TotalAmount': 'sum',
        'InvoiceNo': 'nunique',
        'CustomerID': 'nunique'
    })
    monthly_stats.columns = ['Monthly_Revenue', 'Monthly_Transactions', 'Monthly_Customers']
    
    # Weekly aggregations
    weekly_stats = df.groupby(df['InvoiceDate'].dt.to_period('W')).agg({
        'TotalAmount': 'sum',
        'InvoiceNo': 'nunique'
    })
    weekly_stats.columns = ['Weekly_Revenue', 'Weekly_Transactions']
    
    # Day of week patterns - which days generate most revenue
    dow_stats = df.groupby('DayOfWeek').agg({
        'TotalAmount': ['sum', 'mean'],
        'InvoiceNo': 'nunique'
    })
    dow_stats.columns = ['DOW_Total_Revenue', 'DOW_Avg_Revenue', 'DOW_Transactions']
    
    # Hourly patterns - peak business hours
    hourly_stats = df.groupby('Hour').agg({
        'TotalAmount': ['sum', 'mean'],
        'InvoiceNo': 'nunique'
    })
    hourly_stats.columns = ['Hourly_Total_Revenue', 'Hourly_Avg_Revenue', 'Hourly_Transactions']
    
    temporal_stats = {
        'daily': daily_stats,
        'monthly': monthly_stats,
        'weekly': weekly_stats,
        'day_of_week': dow_stats,
        'hourly': hourly_stats
    }
    
    return temporal_stats


def plot_temporal_trends(temporal_stats, figsize=(15, 12)):
    """
    Create comprehensive temporal trend visualizations
    
    Parameters:
    temporal_stats (dict): Temporal analysis results
    figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(3, 2, figsize=figsize)
    
    # Daily revenue trend over time
    axes[0, 0].plot(temporal_stats['daily'].index, temporal_stats['daily']['Daily_Revenue'])
    axes[0, 0].set_title('Daily Revenue Trend')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Revenue')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Revenue by day of week - reorder to standard week format
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_data = temporal_stats['day_of_week'].reindex(dow_order)
    axes[0, 1].bar(dow_data.index, dow_data['DOW_Total_Revenue'])
    axes[0, 1].set_title('Revenue by Day of Week')
    axes[0, 1].set_xlabel('Day of Week')
    axes[0, 1].set_ylabel('Total Revenue')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Revenue by hour of day - identify peak business hours
    axes[1, 0].bar(temporal_stats['hourly'].index, temporal_stats['hourly']['Hourly_Total_Revenue'])
    axes[1, 0].set_title('Revenue by Hour of Day')
    axes[1, 0].set_xlabel('Hour')
    axes[1, 0].set_ylabel('Revenue')
    
    # Monthly revenue trend
    monthly_data = temporal_stats['monthly']
    axes[1, 1].plot(range(len(monthly_data)), monthly_data['Monthly_Revenue'], marker='o')
    axes[1, 1].set_title('Monthly Revenue Trend')
    axes[1, 1].set_xlabel('Month')
    axes[1, 1].set_ylabel('Revenue')
    
    # Daily transactions trend
    axes[2, 0].plot(temporal_stats['daily'].index, temporal_stats['daily']['Daily_Transactions'])
    axes[2, 0].set_title('Daily Transactions Trend')
    axes[2, 0].set_xlabel('Date')
    axes[2, 0].set_ylabel('Number of Transactions')
    axes[2, 0].tick_params(axis='x', rotation=45)
    
    # Weekly revenue trend
    weekly_data = temporal_stats['weekly']
    axes[2, 1].plot(range(len(weekly_data)), weekly_data['Weekly_Revenue'], marker='s')
    axes[2, 1].set_title('Weekly Revenue Trend')
    axes[2, 1].set_xlabel('Week')
    axes[2, 1].set_ylabel('Revenue')
    
    plt.tight_layout()
    plt.show()


def seasonal_analysis(df, date_column='InvoiceDate'):
    """
    Analyze seasonal patterns in the data
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    date_column (str): Name of the date column
    
    Returns:
    dict: Seasonal analysis results
    """
    df_copy = df.copy()
    df_copy['Quarter'] = df_copy[date_column].dt.quarter
    df_copy['Month'] = df_copy[date_column].dt.month
    df_copy['DayOfYear'] = df_copy[date_column].dt.dayofyear
    
    seasonal_stats = {}
    
    # Quarterly analysis
    quarterly_stats = df_copy.groupby('Quarter').agg({
        'TotalAmount': ['sum', 'mean'],
        'InvoiceNo': 'nunique'
    })
    quarterly_stats.columns = ['Total_Revenue', 'Avg_Revenue', 'Transactions']
    seasonal_stats['quarterly'] = quarterly_stats
    
    # Monthly analysis
    monthly_stats = df_copy.groupby('Month').agg({
        'TotalAmount': ['sum', 'mean'],
        'InvoiceNo': 'nunique'
    })
    monthly_stats.columns = ['Total_Revenue', 'Avg_Revenue', 'Transactions']
    seasonal_stats['monthly'] = monthly_stats
    
    return seasonal_stats


def peak_analysis(temporal_stats):
    """
    Identify peak periods across different time dimensions
    
    Parameters:
    temporal_stats (dict): Temporal analysis results
    
    Returns:
    dict: Peak analysis results
    """
    peaks = {}
    
    # Find peak day
    daily_revenue = temporal_stats['daily']['Daily_Revenue']
    peak_day = daily_revenue.idxmax()
    peaks['peak_day'] = {
        'date': peak_day,
        'revenue': daily_revenue.max(),
        'percentage_of_avg': (daily_revenue.max() / daily_revenue.mean()) * 100
    }
    
    # Find peak day of week
    dow_revenue = temporal_stats['day_of_week']['DOW_Total_Revenue']
    peak_dow = dow_revenue.idxmax()
    peaks['peak_day_of_week'] = {
        'day': peak_dow,
        'revenue': dow_revenue.max(),
        'percentage_of_avg': (dow_revenue.max() / dow_revenue.mean()) * 100
    }
    
    # Find peak hour
    hourly_revenue = temporal_stats['hourly']['Hourly_Total_Revenue']
    peak_hour = hourly_revenue.idxmax()
    peaks['peak_hour'] = {
        'hour': peak_hour,
        'revenue': hourly_revenue.max(),
        'percentage_of_avg': (hourly_revenue.max() / hourly_revenue.mean()) * 100
    }
    
    # Find peak month
    monthly_revenue = temporal_stats['monthly']['Monthly_Revenue']
    peak_month = monthly_revenue.idxmax()
    peaks['peak_month'] = {
        'month': peak_month,
        'revenue': monthly_revenue.max(),
        'percentage_of_avg': (monthly_revenue.max() / monthly_revenue.mean()) * 100
    }
    
    return peaks


def trend_analysis(temporal_stats):
    """
    Analyze trends in temporal data
    
    Parameters:
    temporal_stats (dict): Temporal analysis results
    
    Returns:
    dict: Trend analysis results
    """
    trends = {}
    
    # Daily revenue trend
    daily_revenue = temporal_stats['daily']['Daily_Revenue']
    daily_trend = np.polyfit(range(len(daily_revenue)), daily_revenue, 1)[0]
    trends['daily_revenue_trend'] = daily_trend
    
    # Monthly revenue trend
    monthly_revenue = temporal_stats['monthly']['Monthly_Revenue']
    monthly_trend = np.polyfit(range(len(monthly_revenue)), monthly_revenue, 1)[0]
    trends['monthly_revenue_trend'] = monthly_trend
    
    # Calculate growth rates
    if len(monthly_revenue) > 1:
        monthly_growth = ((monthly_revenue.iloc[-1] - monthly_revenue.iloc[0]) / monthly_revenue.iloc[0]) * 100
        trends['monthly_growth_rate'] = monthly_growth
    
    return trends
