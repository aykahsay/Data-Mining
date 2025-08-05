# Customer Analysis Utilities
"""
This module contains functions for customer behavior analysis and RFM segmentation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def customer_behavior_analysis(df):
    """
    Analyze customer purchasing behavior and lifetime value
    
    Parameters:
    df (pd.DataFrame): Input dataframe with customer transaction data
    
    Returns:
    tuple: (customer_stats DataFrame, behavior_summary dict)
    """
    # Remove transactions without customer ID
    customer_df = df.dropna(subset=['CustomerID'])
    
    # Aggregate customer-level metrics
    customer_stats = customer_df.groupby('CustomerID').agg({
        'InvoiceNo': 'nunique',         # Number of unique transactions
        'TotalAmount': ['sum', 'mean'], # Total and average spending
        'Quantity': 'sum',              # Total items purchased
        'InvoiceDate': ['min', 'max'],  # First and last purchase dates
        'StockCode': 'nunique'          # Product variety
    })
    
    # Flatten column names
    customer_stats.columns = ['Transactions', 'Total_Spending', 'Avg_Spending', 
                             'Total_Quantity', 'First_Purchase', 'Last_Purchase', 'Products']
    
    # Calculate customer lifetime in days
    customer_stats['Lifetime_Days'] = (
        customer_stats['Last_Purchase'] - customer_stats['First_Purchase']
    ).dt.days + 1
    
    # Calculate additional metrics
    customer_stats['Spending_per_Day'] = (
        customer_stats['Total_Spending'] / customer_stats['Lifetime_Days']
    ).replace([np.inf, -np.inf], 0)
    
    # Behavior summary
    behavior_summary = {
        'total_customers': len(customer_stats),
        'avg_transactions_per_customer': customer_stats['Transactions'].mean(),
        'avg_total_spending': customer_stats['Total_Spending'].mean(),
        'avg_spending_per_transaction': customer_stats['Avg_Spending'].mean(),
        'avg_customer_lifetime_days': customer_stats['Lifetime_Days'].mean(),
        'avg_products_per_customer': customer_stats['Products'].mean()
    }
    
    return customer_stats, behavior_summary


def rfm_analysis(df):
    """
    Perform RFM (Recency, Frequency, Monetary) customer segmentation
    
    Parameters:
    df (pd.DataFrame): Input dataframe with customer transaction data
    
    Returns:
    pd.DataFrame: RFM scores and segments for each customer
    """
    # Remove rows with missing CustomerID
    customer_df = df.dropna(subset=['CustomerID'])
    
    # Calculate RFM metrics
    max_date = customer_df['InvoiceDate'].max()
    
    rfm = customer_df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (max_date - x.max()).days,  # Days since last purchase (Recency)
        'InvoiceNo': 'nunique',  # Purchase frequency (Frequency)
        'TotalAmount': 'sum'     # Total monetary value (Monetary)
    })
    
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    
    # Create RFM scores using quintiles (1-5 scale)
    try:
        rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), 5, labels=[5,4,3,2,1])  # Lower recency = higher score
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]) # Higher frequency = higher score
        rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1,2,3,4,5])  # Higher monetary = higher score
    except ValueError:
        # Fallback to manual bins if qcut fails due to duplicates
        rfm['R_Score'] = pd.cut(rfm['Recency'], bins=5, labels=[5,4,3,2,1])
        rfm['F_Score'] = pd.cut(rfm['Frequency'], bins=5, labels=[1,2,3,4,5])
        rfm['M_Score'] = pd.cut(rfm['Monetary'], bins=5, labels=[1,2,3,4,5])
    
    # Convert to numeric
    rfm['R_Score'] = pd.to_numeric(rfm['R_Score'], errors='coerce')
    rfm['F_Score'] = pd.to_numeric(rfm['F_Score'], errors='coerce')
    rfm['M_Score'] = pd.to_numeric(rfm['M_Score'], errors='coerce')
    
    # Fill any NaN values with median scores
    rfm['R_Score'] = rfm['R_Score'].fillna(rfm['R_Score'].median())
    rfm['F_Score'] = rfm['F_Score'].fillna(rfm['F_Score'].median())
    rfm['M_Score'] = rfm['M_Score'].fillna(rfm['M_Score'].median())
    
    # Calculate combined RFM score
    rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']
    
    # Segment customers based on RFM score
    def segment_customers(score):
        if score >= 12: return 'Champions'    # Best customers
        elif score >= 10: return 'Loyal'     # Loyal customers
        elif score >= 8: return 'Potential'  # Potential loyalists
        elif score >= 6: return 'At Risk'    # At risk customers
        else: return 'Lost'                   # Lost customers
    
    rfm['Segment'] = rfm['RFM_Score'].apply(segment_customers)
    
    return rfm


def customer_segmentation_analysis(rfm_results):
    """
    Analyze customer segments from RFM results
    
    Parameters:
    rfm_results (pd.DataFrame): RFM analysis results
    
    Returns:
    dict: Segment analysis results
    """
    segment_analysis = {}
    
    for segment in rfm_results['Segment'].unique():
        segment_data = rfm_results[rfm_results['Segment'] == segment]
        
        segment_analysis[segment] = {
            'count': len(segment_data),
            'percentage': (len(segment_data) / len(rfm_results)) * 100,
            'avg_recency': segment_data['Recency'].mean(),
            'avg_frequency': segment_data['Frequency'].mean(),
            'avg_monetary': segment_data['Monetary'].mean(),
            'total_value': segment_data['Monetary'].sum()
        }
    
    return segment_analysis


def plot_customer_distribution(customer_stats, figsize=(15, 10)):
    """
    Create visualizations of customer behavior distributions
    
    Parameters:
    customer_stats (pd.DataFrame): Customer statistics dataframe
    figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    
    # Total spending distribution
    axes[0, 0].hist(customer_stats['Total_Spending'], bins=50, alpha=0.7)
    axes[0, 0].set_title('Distribution of Total Customer Spending')
    axes[0, 0].set_xlabel('Total Spending')
    axes[0, 0].set_ylabel('Number of Customers')
    
    # Transaction frequency distribution
    axes[0, 1].hist(customer_stats['Transactions'], bins=50, alpha=0.7)
    axes[0, 1].set_title('Distribution of Transaction Frequency')
    axes[0, 1].set_xlabel('Number of Transactions')
    axes[0, 1].set_ylabel('Number of Customers')
    
    # Customer lifetime distribution
    axes[0, 2].hist(customer_stats['Lifetime_Days'], bins=50, alpha=0.7)
    axes[0, 2].set_title('Distribution of Customer Lifetime')
    axes[0, 2].set_xlabel('Lifetime (Days)')
    axes[0, 2].set_ylabel('Number of Customers')
    
    # Spending vs Transactions scatter
    axes[1, 0].scatter(customer_stats['Transactions'], customer_stats['Total_Spending'], alpha=0.6)
    axes[1, 0].set_xlabel('Number of Transactions')
    axes[1, 0].set_ylabel('Total Spending')
    axes[1, 0].set_title('Spending vs Transaction Frequency')
    
    # Product variety distribution
    axes[1, 1].hist(customer_stats['Products'], bins=50, alpha=0.7)
    axes[1, 1].set_title('Distribution of Product Variety per Customer')
    axes[1, 1].set_xlabel('Number of Different Products')
    axes[1, 1].set_ylabel('Number of Customers')
    
    # Average spending per transaction
    axes[1, 2].hist(customer_stats['Avg_Spending'], bins=50, alpha=0.7)
    axes[1, 2].set_title('Distribution of Average Spending per Transaction')
    axes[1, 2].set_xlabel('Average Spending')
    axes[1, 2].set_ylabel('Number of Customers')
    
    plt.tight_layout()
    plt.show()


def plot_rfm_segments(rfm_results, figsize=(12, 8)):
    """
    Visualize RFM segments
    
    Parameters:
    rfm_results (pd.DataFrame): RFM analysis results
    figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Segment distribution
    segment_counts = rfm_results['Segment'].value_counts()
    axes[0, 0].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%')
    axes[0, 0].set_title('Customer Segment Distribution')
    
    # RFM Score distribution by segment
    rfm_results.boxplot(column='RFM_Score', by='Segment', ax=axes[0, 1])
    axes[0, 1].set_title('RFM Score by Segment')
    axes[0, 1].set_xlabel('Segment')
    
    # Monetary value by segment
    rfm_results.boxplot(column='Monetary', by='Segment', ax=axes[1, 0])
    axes[1, 0].set_title('Monetary Value by Segment')
    axes[1, 0].set_xlabel('Segment')
    
    # Frequency by segment
    rfm_results.boxplot(column='Frequency', by='Segment', ax=axes[1, 1])
    axes[1, 1].set_title('Purchase Frequency by Segment')
    axes[1, 1].set_xlabel('Segment')
    
    plt.tight_layout()
    plt.show()
