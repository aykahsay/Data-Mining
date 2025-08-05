# Product Analysis Utilities
"""
This module contains functions for analyzing product performance and geographical patterns.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def product_analysis(df, top_n=20):
    """
    Analyze product performance across multiple dimensions
    
    Parameters:
    df (pd.DataFrame): Input dataframe with product transaction data
    top_n (int): Number of top products to analyze
    
    Returns:
    dict: Dictionary containing product analysis results
    """
    # Group by product (StockCode + Description) and calculate key metrics
    product_stats = df.groupby(['StockCode', 'Description']).agg({
        'TotalAmount': ['sum', 'mean', 'count'],  # Total revenue, avg revenue, number of transactions
        'Quantity': ['sum', 'mean'],              # Total and average quantity sold
        'UnitPrice': ['mean', 'std'],             # Average price and price variability
        'CustomerID': 'nunique',                  # Number of unique customers
        'InvoiceNo': 'nunique'                    # Number of unique invoices
    }).round(2)
    
    # Flatten column names
    product_stats.columns = ['_'.join(col).strip() for col in product_stats.columns]
    
    # Calculate additional metrics
    product_stats['Revenue_per_Customer'] = (
        product_stats['TotalAmount_sum'] / product_stats['CustomerID_nunique']
    ).round(2)
    
    product_stats['Avg_Quantity_per_Transaction'] = (
        product_stats['Quantity_sum'] / product_stats['InvoiceNo_nunique']
    ).round(2)
    
    # Create performance categories
    revenue_quartiles = pd.qcut(product_stats['TotalAmount_sum'], 
                               q=4, labels=['Low', 'Medium', 'High', 'Premium'])
    product_stats['Revenue_Category'] = revenue_quartiles
    
    popularity_quartiles = pd.qcut(product_stats['TotalAmount_count'], 
                                  q=4, labels=['Niche', 'Occasional', 'Popular', 'Best-Seller'])
    product_stats['Popularity_Category'] = popularity_quartiles
    
    # Top performers by different metrics
    analysis_results = {
        'all_products': product_stats,
        'top_revenue': product_stats.nlargest(top_n, 'TotalAmount_sum'),
        'top_quantity': product_stats.nlargest(top_n, 'Quantity_sum'),
        'top_transactions': product_stats.nlargest(top_n, 'TotalAmount_count'),
        'top_customers': product_stats.nlargest(top_n, 'CustomerID_nunique'),
        'highest_price': product_stats.nlargest(top_n, 'UnitPrice_mean'),
        'most_variable_price': product_stats.nlargest(top_n, 'UnitPrice_std')
    }
    
    return analysis_results


def country_analysis(df):
    """
    Analyze business performance by country/region
    
    Parameters:
    df (pd.DataFrame): Input dataframe with country information
    
    Returns:
    pd.DataFrame: Country-level analysis
    """
    country_stats = df.groupby('Country').agg({
        'TotalAmount': ['sum', 'mean', 'count'],
        'CustomerID': 'nunique',
        'InvoiceNo': 'nunique',
        'StockCode': 'nunique',
        'Quantity': 'sum'
    }).round(2)
    
    # Flatten column names
    country_stats.columns = ['_'.join(col).strip() for col in country_stats.columns]
    
    # Calculate additional metrics
    country_stats['Revenue_per_Customer'] = (
        country_stats['TotalAmount_sum'] / country_stats['CustomerID_nunique']
    ).round(2)
    
    country_stats['Avg_Transaction_Value'] = (
        country_stats['TotalAmount_sum'] / country_stats['InvoiceNo_nunique']
    ).round(2)
    
    country_stats['Market_Share'] = (
        (country_stats['TotalAmount_sum'] / country_stats['TotalAmount_sum'].sum()) * 100
    ).round(2)
    
    return country_stats.sort_values('TotalAmount_sum', ascending=False)


def product_category_analysis(df, category_column='Description'):
    """
    Analyze product categories if category information is available
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    category_column (str): Column containing category information
    
    Returns:
    pd.DataFrame: Category analysis results
    """
    if category_column not in df.columns:
        print(f"Column '{category_column}' not found. Creating categories from product descriptions.")
        # Simple category extraction from description (can be enhanced)
        df['Category'] = df['Description'].str.extract(r'([A-Z]{2,})', expand=False).fillna('OTHER')
        category_column = 'Category'
    
    category_stats = df.groupby(category_column).agg({
        'TotalAmount': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'CustomerID': 'nunique',
        'StockCode': 'nunique'
    }).round(2)
    
    category_stats.columns = ['_'.join(col).strip() for col in category_stats.columns]
    
    return category_stats.sort_values('TotalAmount_sum', ascending=False)


def plot_product_performance(product_analysis_results, figsize=(15, 12)):
    """
    Create visualizations for product performance analysis
    
    Parameters:
    product_analysis_results (dict): Product analysis results
    figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    
    # Top products by revenue
    top_revenue = product_analysis_results['top_revenue'].head(10)
    axes[0, 0].barh(range(len(top_revenue)), top_revenue['TotalAmount_sum'])
    axes[0, 0].set_yticks(range(len(top_revenue)))
    axes[0, 0].set_yticklabels([desc[:30] + '...' if len(desc) > 30 else desc 
                               for desc in top_revenue.index.get_level_values('Description')])
    axes[0, 0].set_title('Top 10 Products by Revenue')
    axes[0, 0].set_xlabel('Total Revenue')
    
    # Revenue distribution by category
    all_products = product_analysis_results['all_products']
    revenue_category_counts = all_products['Revenue_Category'].value_counts()
    axes[0, 1].pie(revenue_category_counts.values, labels=revenue_category_counts.index, autopct='%1.1f%%')
    axes[0, 1].set_title('Products by Revenue Category')
    
    # Popularity distribution
    popularity_counts = all_products['Popularity_Category'].value_counts()
    axes[0, 2].pie(popularity_counts.values, labels=popularity_counts.index, autopct='%1.1f%%')
    axes[0, 2].set_title('Products by Popularity Category')
    
    # Revenue vs Popularity scatter
    axes[1, 0].scatter(all_products['TotalAmount_count'], all_products['TotalAmount_sum'], alpha=0.6)
    axes[1, 0].set_xlabel('Number of Transactions')
    axes[1, 0].set_ylabel('Total Revenue')
    axes[1, 0].set_title('Revenue vs Popularity')
    
    # Price distribution
    axes[1, 1].hist(all_products['UnitPrice_mean'], bins=50, alpha=0.7)
    axes[1, 1].set_xlabel('Average Unit Price')
    axes[1, 1].set_ylabel('Number of Products')
    axes[1, 1].set_title('Distribution of Average Product Prices')
    
    # Customer reach
    top_customers = product_analysis_results['top_customers'].head(10)
    axes[1, 2].barh(range(len(top_customers)), top_customers['CustomerID_nunique'])
    axes[1, 2].set_yticks(range(len(top_customers)))
    axes[1, 2].set_yticklabels([desc[:30] + '...' if len(desc) > 30 else desc 
                               for desc in top_customers.index.get_level_values('Description')])
    axes[1, 2].set_title('Top 10 Products by Customer Reach')
    axes[1, 2].set_xlabel('Number of Unique Customers')
    
    plt.tight_layout()
    plt.show()


def plot_country_performance(country_analysis_results, top_n=15, figsize=(15, 10)):
    """
    Create visualizations for country performance analysis
    
    Parameters:
    country_analysis_results (pd.DataFrame): Country analysis results
    top_n (int): Number of top countries to display
    figsize (tuple): Figure size
    """
    top_countries = country_analysis_results.head(top_n)
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Revenue by country
    axes[0, 0].barh(range(len(top_countries)), top_countries['TotalAmount_sum'])
    axes[0, 0].set_yticks(range(len(top_countries)))
    axes[0, 0].set_yticklabels(top_countries.index)
    axes[0, 0].set_title(f'Top {top_n} Countries by Revenue')
    axes[0, 0].set_xlabel('Total Revenue')
    
    # Market share pie chart (top 10)
    top_10_countries = country_analysis_results.head(10)
    axes[0, 1].pie(top_10_countries['Market_Share'], labels=top_10_countries.index, autopct='%1.1f%%')
    axes[0, 1].set_title('Market Share by Country (Top 10)')
    
    # Revenue per customer
    axes[1, 0].barh(range(len(top_countries)), top_countries['Revenue_per_Customer'])
    axes[1, 0].set_yticks(range(len(top_countries)))
    axes[1, 0].set_yticklabels(top_countries.index)
    axes[1, 0].set_title(f'Revenue per Customer by Country (Top {top_n})')
    axes[1, 0].set_xlabel('Revenue per Customer')
    
    # Number of customers vs revenue scatter
    axes[1, 1].scatter(country_analysis_results['CustomerID_nunique'], 
                      country_analysis_results['TotalAmount_sum'], alpha=0.7)
    axes[1, 1].set_xlabel('Number of Customers')
    axes[1, 1].set_ylabel('Total Revenue')
    axes[1, 1].set_title('Customers vs Revenue by Country')
    
    # Add country labels for top countries
    for i, country in enumerate(top_countries.head(5).index):
        axes[1, 1].annotate(country, 
                           (country_analysis_results.loc[country, 'CustomerID_nunique'],
                            country_analysis_results.loc[country, 'TotalAmount_sum']))
    
    plt.tight_layout()
    plt.show()


def product_performance_summary(product_analysis_results):
    """
    Generate a comprehensive summary of product performance
    
    Parameters:
    product_analysis_results (dict): Product analysis results
    
    Returns:
    dict: Performance summary
    """
    all_products = product_analysis_results['all_products']
    
    summary = {
        'total_products': len(all_products),
        'total_revenue': all_products['TotalAmount_sum'].sum(),
        'avg_revenue_per_product': all_products['TotalAmount_sum'].mean(),
        'top_10_revenue_share': (product_analysis_results['top_revenue'].head(10)['TotalAmount_sum'].sum() / 
                                all_products['TotalAmount_sum'].sum()) * 100,
        'products_with_single_customer': (all_products['CustomerID_nunique'] == 1).sum(),
        'avg_price_range': {
            'min': all_products['UnitPrice_mean'].min(),
            'max': all_products['UnitPrice_mean'].max(),
            'avg': all_products['UnitPrice_mean'].mean()
        }
    }
    
    return summary
