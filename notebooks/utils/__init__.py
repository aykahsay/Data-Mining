# Utils Package for Data Mining Statistical Analysis
"""
This package contains modular utility functions for comprehensive statistical analysis
of retail transaction data.

Modules:
- data_loader: Data loading and preprocessing utilities
- descriptive_stats: Descriptive statistics generation
- correlation_analysis: Correlation analysis and relationship exploration
- customer_analysis: Customer behavior analysis and RFM segmentation
- temporal_analysis: Temporal pattern analysis
- product_analysis: Product performance and geographical analysis
- export_utils: Export and reporting utilities
"""

# Import key functions for easy access
from .data_loader import load_transformed_data, validate_data, clean_data
from .descriptive_stats import generate_descriptive_stats, display_stats_table
from .correlation_analysis import correlation_analysis, significant_correlations
from .customer_analysis import customer_behavior_analysis, rfm_analysis
from .temporal_analysis import temporal_analysis, plot_temporal_trends
from .product_analysis import product_analysis, country_analysis
from .export_utils import export_analysis_results, generate_comprehensive_report

__version__ = "1.0.0"
__author__ = "Data Mining Analysis Team"
