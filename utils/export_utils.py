# Export and Reporting Utilities
"""
This module contains functions for exporting analysis results and generating reports.
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime


def export_analysis_results(analysis_results, output_dir="../results/"):
    """
    Export all analysis results to CSV files and generate a summary report
    
    Parameters:
    analysis_results (dict): Dictionary containing all analysis results
    output_dir (str): Directory to save the exported files
    
    Returns:
    bool: True if export successful
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    exported_files = []
    
    try:
        # Export descriptive statistics
        if 'stats_summary' in analysis_results:
            stats_df = pd.DataFrame(analysis_results['stats_summary']).T
            stats_path = os.path.join(output_dir, 'descriptive_statistics.csv')
            stats_df.to_csv(stats_path)
            exported_files.append('descriptive_statistics.csv')
        
        # Export customer analysis
        if 'customer_stats' in analysis_results:
            customer_path = os.path.join(output_dir, 'customer_behavior_analysis.csv')
            analysis_results['customer_stats'].to_csv(customer_path)
            exported_files.append('customer_behavior_analysis.csv')
        
        # Export RFM analysis
        if 'rfm_results' in analysis_results:
            rfm_path = os.path.join(output_dir, 'rfm_analysis.csv')
            analysis_results['rfm_results'].to_csv(rfm_path)
            exported_files.append('rfm_analysis.csv')
        
        # Export product analysis
        if 'product_results' in analysis_results:
            product_path = os.path.join(output_dir, 'product_performance_analysis.csv')
            if isinstance(analysis_results['product_results'], dict):
                analysis_results['product_results']['all_products'].to_csv(product_path)
            else:
                analysis_results['product_results'].to_csv(product_path)
            exported_files.append('product_performance_analysis.csv')
        
        # Export country analysis
        if 'country_results' in analysis_results:
            country_path = os.path.join(output_dir, 'country_analysis.csv')
            analysis_results['country_results'].to_csv(country_path)
            exported_files.append('country_analysis.csv')
        
        # Export temporal analysis
        if 'temporal_results' in analysis_results:
            temporal_dir = os.path.join(output_dir, 'temporal_analysis')
            os.makedirs(temporal_dir, exist_ok=True)
            
            for key, data in analysis_results['temporal_results'].items():
                temporal_path = os.path.join(temporal_dir, f'{key}_analysis.csv')
                data.to_csv(temporal_path)
                exported_files.append(f'temporal_analysis/{key}_analysis.csv')
        
        print(f"Analysis results exported to: {output_dir}")
        print("Files created:")
        for file in exported_files:
            print(f"   - {file}")
        
        return True
        
    except Exception as e:
        print(f"Error exporting results: {e}")
        return False


def generate_comprehensive_report(df, analysis_results):
    """
    Generate a comprehensive statistical analysis report
    
    Parameters:
    df (pd.DataFrame): Original dataset
    analysis_results (dict): All analysis results
    
    Returns:
    dict: Comprehensive report
    """
    report = {
        'generated_at': datetime.now().isoformat(),
        'dataset_info': {
            'total_transactions': len(df),
            'total_features': len(df.columns),
            'date_range': {
                'start': df['InvoiceDate'].min().isoformat() if 'InvoiceDate' in df.columns else None,
                'end': df['InvoiceDate'].max().isoformat() if 'InvoiceDate' in df.columns else None
            },
            'total_customers': df['CustomerID'].nunique() if 'CustomerID' in df.columns else 0,
            'total_products': df['StockCode'].nunique() if 'StockCode' in df.columns else 0,
            'total_countries': df['Country'].nunique() if 'Country' in df.columns else 0
        },
        'key_metrics': {
            'total_revenue': float(df['TotalAmount'].sum()) if 'TotalAmount' in df.columns else 0,
            'avg_transaction_value': float(df['TotalAmount'].mean()) if 'TotalAmount' in df.columns else 0,
            'avg_quantity_per_transaction': float(df['Quantity'].mean()) if 'Quantity' in df.columns else 0,
            'avg_unit_price': float(df['UnitPrice'].mean()) if 'UnitPrice' in df.columns else 0
        }
    }
    
    # Add analysis-specific insights
    if 'temporal_results' in analysis_results:
        temporal = analysis_results['temporal_results']
        if 'day_of_week' in temporal:
            report['temporal_insights'] = {
                'best_day_of_week': temporal['day_of_week']['DOW_Total_Revenue'].idxmax(),
                'peak_hour': temporal['hourly']['Hourly_Total_Revenue'].idxmax(),
                'daily_avg_revenue': float(temporal['daily']['Daily_Revenue'].mean())
            }
    
    if 'rfm_results' in analysis_results:
        rfm = analysis_results['rfm_results']
        segment_counts = rfm['Segment'].value_counts()
        report['customer_insights'] = {
            'total_segments': len(segment_counts),
            'largest_segment': segment_counts.idxmax(),
            'champion_customers': int(segment_counts.get('Champions', 0)),
            'at_risk_customers': int(segment_counts.get('At Risk', 0))
        }
    
    if 'product_results' in analysis_results:
        products = analysis_results['product_results']
        if isinstance(products, dict) and 'all_products' in products:
            report['product_insights'] = {
                'total_products': len(products['all_products']),
                'avg_revenue_per_product': float(products['all_products']['TotalAmount_sum'].mean()),
                'top_product_revenue_share': float(
                    (products['top_revenue'].head(10)['TotalAmount_sum'].sum() / 
                     products['all_products']['TotalAmount_sum'].sum()) * 100
                )
            }
    
    return report


def create_executive_summary(analysis_results):
    """
    Create an executive summary of key findings
    
    Parameters:
    analysis_results (dict): All analysis results
    
    Returns:
    str: Executive summary text
    """
    summary_parts = []
    
    summary_parts.append("EXECUTIVE SUMMARY")
    summary_parts.append("=" * 50)
    
    # Dataset overview
    if 'dataset_info' in analysis_results:
        info = analysis_results['dataset_info']
        summary_parts.append(f"\nDataset Overview:")
        summary_parts.append(f"- Total transactions: {info.get('total_transactions', 'N/A'):,}")
        summary_parts.append(f"- Unique customers: {info.get('total_customers', 'N/A'):,}")
        summary_parts.append(f"- Unique products: {info.get('total_products', 'N/A'):,}")
        summary_parts.append(f"- Countries served: {info.get('total_countries', 'N/A')}")
    
    # Key business metrics
    if 'key_metrics' in analysis_results:
        metrics = analysis_results['key_metrics']
        summary_parts.append(f"\nKey Business Metrics:")
        summary_parts.append(f"- Total revenue: ${metrics.get('total_revenue', 0):,.2f}")
        summary_parts.append(f"- Average transaction value: ${metrics.get('avg_transaction_value', 0):.2f}")
        summary_parts.append(f"- Average unit price: ${metrics.get('avg_unit_price', 0):.2f}")
    
    # Temporal insights
    if 'temporal_insights' in analysis_results:
        temporal = analysis_results['temporal_insights']
        summary_parts.append(f"\nTemporal Patterns:")
        summary_parts.append(f"- Best performing day: {temporal.get('best_day_of_week', 'N/A')}")
        summary_parts.append(f"- Peak business hour: {temporal.get('peak_hour', 'N/A')}:00")
        summary_parts.append(f"- Daily average revenue: ${temporal.get('daily_avg_revenue', 0):,.2f}")
    
    # Customer insights
    if 'customer_insights' in analysis_results:
        customer = analysis_results['customer_insights']
        summary_parts.append(f"\nCustomer Segmentation:")
        summary_parts.append(f"- Customer segments identified: {customer.get('total_segments', 0)}")
        summary_parts.append(f"- Largest segment: {customer.get('largest_segment', 'N/A')}")
        summary_parts.append(f"- Champion customers: {customer.get('champion_customers', 0)}")
        summary_parts.append(f"- At-risk customers: {customer.get('at_risk_customers', 0)}")
    
    # Product insights
    if 'product_insights' in analysis_results:
        product = analysis_results['product_insights']
        summary_parts.append(f"\nProduct Performance:")
        summary_parts.append(f"- Total products analyzed: {product.get('total_products', 0)}")
        summary_parts.append(f"- Average revenue per product: ${product.get('avg_revenue_per_product', 0):,.2f}")
        summary_parts.append(f"- Top 10 products revenue share: {product.get('top_product_revenue_share', 0):.1f}%")
    
    return "\n".join(summary_parts)


def save_report_to_file(report, output_dir="../results/", filename="analysis_report.json"):
    """
    Save the comprehensive report to a JSON file
    
    Parameters:
    report (dict): Comprehensive report
    output_dir (str): Output directory
    filename (str): Output filename
    
    Returns:
    str: Path to saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_numpy_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    # Recursively convert numpy types
    def clean_for_json(data):
        if isinstance(data, dict):
            return {key: clean_for_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_for_json(item) for item in data]
        else:
            return convert_numpy_types(data)
    
    cleaned_report = clean_for_json(report)
    
    with open(filepath, 'w') as f:
        json.dump(cleaned_report, f, indent=2, default=str)
    
    return filepath
