# DSA2040A Summer Semester Group 5

## Group Details

- Exploratory Data Analysis - Ambachow
- Data Visualization - Cynthia & Paul
- Data Transformation - Samuel 
- Statistical Analysis- Justice 
- Data Mining- Misati (670145)

## Project Summary

## ETL Summary

### Data Cleaning

It was identified that the columns:

- InvoiceNo
- StockCode
- InvoiceDate

were properly formatted with no missing or strange values.

To handle the `Description` column it was identified that the values needing imputation were either:

- Blank
- Starting with `?`

To handle this the following algorithm was implemented:

1. The corresponding stock code of the product is identified.
2. The dataframe is filtered to obtain only the rows with the particular stock code.
3. If there is more than one row and at least of one the rows has a value that is not considered strange then the mode of the Description rows values is imputed.
4. Otherwise, the row is dropped since there is no other way of identifying what product it is.

To handle the `Quantity` column:

- The absolute value of the value presently in the column is used.

To handle the `UnitPrice` column it was identified that the values that needed imputation were:

- Zero

To handle this the following algorithm was implemented:

1. The corresponding stock code of the product is identified.
2. The dataframe is filtered to obtain only the rows with the particular stock code.
3. If there is more than one row and at least of one the rows has a value that is not considered strange then the dataframe is filtered even further by the country.
4. If it is found that more than one row and at least one of the rows has a value that is not considered strange then the mode of the prices is imputed.
5. Otherwise, the mode of the first dataframe filtration is used.
6. Otherwise, the row is dropped since there is no other way of identifying what the unti price is.

To handle the `CustomerID` column it was identified that the values that need imputation were:

- Blank

To handle this the following algorithm was implemented:

1. The corresponding invoice number of the customer ID is identified.
2. The dataframe is filtered to obtain only the rows with the particular invoice number.
3. If there is more than one row and at least of one the rows has a value that is not considered strange then the mode of the customer ID rows values is imputed.
4. Otherwise, the row is dropped since there is no other way of identifying what the customer ID is.

To handle the `Country` column it was identified that the values that needed imputation were:

- Unspecified

To handle this the following algorithm was implemented:

1. The corresponding customer ID of the country is identified.
2. If this does not exist then discard the column since there is no way of imputing it.
3. The dataframe is filtered to obtain only the rows with the particular customer ID.
4. If there is more than one row and at least of one the rows has a value that is not considered strange then the mode of the country rows values is imputed.
5. Otherwise, the row is dropped since there is no other way of identifying what the country is.

## Statistical Analysis Summary

### Overview
The statistical analysis module provides comprehensive data analysis capabilities for e-commerce transaction data. The analysis has been developed using a modular approach with reusable utility functions organized in the `utils/` package.

### Analysis Components

#### 1. Data Loading and Validation
- **Data Loading**: Automated loading of transformed CSV data with error handling
- **Data Validation**: Comprehensive validation checks including:
  - Missing value detection
  - Data type verification
  - Range validation for numerical columns
  - Duplicate record identification
- **Data Cleaning**: Configurable cleaning operations with options to remove negative values and handle missing customer IDs

#### 2. Descriptive Statistics
- **Summary Statistics**: Mean, median, mode, standard deviation, variance
- **Distribution Metrics**: Skewness, kurtosis, quartiles, IQR
- **Outlier Detection**: Statistical methods for identifying anomalous data points
- **Professional Reporting**: Formatted statistical tables for business presentations

#### 3. Distribution Analysis
- **Normality Testing**: Shapiro-Wilk and D'Agostino-Pearson tests
- **Distribution Visualization**: Histograms, Q-Q plots, box plots
- **Distribution Comparison**: Side-by-side analysis of multiple variables
- **Statistical Interpretation**: Automated interpretation of distribution characteristics

#### 4. Correlation Analysis
- **Correlation Matrix**: Pearson correlation coefficients between numerical variables
- **Significance Testing**: Statistical significance of correlations with p-values
- **Visualization**: Heatmaps and scatter plots for correlation relationships
- **Threshold Filtering**: Configurable significance thresholds for meaningful relationships

#### 5. Customer Behavior Analysis
- **Customer Metrics**: Transaction frequency, total spending, product diversity
- **RFM Analysis**: Recency, Frequency, Monetary customer segmentation
- **Customer Segmentation**: Automated classification into business-relevant segments:
  - Champions: Best customers with high value and engagement
  - Loyal Customers: Consistent, regular purchasers
  - Potential Loyalists: Recent customers with good potential
  - At Risk: Previously valuable customers showing decline
  - Cannot Lose Them: High-value customers who haven't purchased recently
- **Behavioral Insights**: Purchase patterns and customer lifecycle analysis

#### 6. Temporal Pattern Analysis
- **Time Series Analysis**: Revenue trends over time periods
- **Seasonality Detection**: Monthly, daily, and hourly pattern identification
- **Peak Performance**: Identification of optimal business hours and days
- **Trend Analysis**: Growth patterns and cyclical behaviors
- **Forecasting Support**: Foundation for predictive modeling

#### 7. Product Performance Analysis
- **Revenue Analysis**: Top-performing products by sales volume and revenue
- **Product Metrics**: Sales frequency, customer reach, average transaction value
- **Cross-selling Opportunities**: Product association analysis
- **Performance Ranking**: Comprehensive product performance scoring

#### 8. Geographical Analysis
- **Country-wise Performance**: Revenue and customer distribution by geography
- **Market Penetration**: Customer density and market share analysis
- **Revenue per Customer**: Geographic profitability analysis
- **Market Opportunities**: Identification of underperforming but potential markets

### Technical Architecture

#### Modular Structure
```
utils/
├── __init__.py                 # Package initialization and imports
├── data_loader.py             # Data loading and validation functions
├── descriptive_stats.py       # Statistical summary functions
├── distribution_analysis.py   # Distribution testing and visualization
├── correlation_analysis.py    # Correlation analysis and visualization
├── customer_analysis.py       # Customer behavior and RFM analysis
├── temporal_analysis.py       # Time-based pattern analysis
├── product_analysis.py        # Product and geographical analysis
└── export_utils.py           # Results export and reporting
```

### Business Insights Generated

- **Customer Segmentation**: Actionable customer segments for targeted marketing
- **Revenue Optimization**: Peak performance periods for resource allocation
- **Product Strategy**: Data-driven product performance insights
- **Market Analysis**: Geographic expansion opportunities
- **Operational Efficiency**: Optimal business hours and staffing insights
- **Risk Management**: Customer churn identification and retention strategies

## Techniques Used

### Data Cleaning and Preprocessing
- Missing value imputation using mode-based algorithms
- Outlier detection and treatment
- Data type standardization and validation
- Duplicate record handling

### Statistical Analysis Techniques
- **Descriptive Statistics**: Central tendency, dispersion, and shape measures
- **Inferential Statistics**: Hypothesis testing and confidence intervals
- **Distribution Analysis**: Normality testing (Shapiro-Wilk, D'Agostino-Pearson)
- **Correlation Analysis**: Pearson correlation with significance testing
- **Time Series Analysis**: Temporal pattern recognition and trend analysis
- **Customer Segmentation**: RFM (Recency, Frequency, Monetary) analysis
- **Outlier Detection**: Statistical methods for anomaly identification

### Machine Learning and Data Mining
- Customer behavior clustering
- Pattern recognition in temporal data
- Feature engineering for business metrics
- Predictive modeling foundations

### Data Visualization
- Statistical plots (histograms, box plots, Q-Q plots)
- Correlation heatmaps and scatter plots
- Time series visualizations
- Business dashboard components
- Geographic performance mapping

## Tools Used

### Programming Languages and Core Libraries
- **Python 3.x**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and array operations
- **Matplotlib**: Static plotting and visualization
- **Seaborn**: Statistical data visualization
- **SciPy**: Scientific computing and statistical tests

### Development Environment
- **Jupyter Notebooks**: Interactive development and analysis
- **VS Code**: Code editing and development environment
- **Git**: Version control and collaboration

### Data Processing Tools
- **CSV Processing**: Data import/export capabilities
- **Data Validation**: Custom validation frameworks
- **Statistical Testing**: Automated hypothesis testing

### Visualization and Reporting
- **Power BI**: Business intelligence dashboards
- **Python Plotting Libraries**: Custom statistical visualizations
- **Automated Reporting**: Programmatic report generation

## Instructions to Run Notebooks

### Prerequisites
1. Install the necessary modules for statistical analysis:
   
   ```bash
   pip install jupyter numpy pandas matplotlib seaborn scipy scikit-learn mlxtend
   ```

## Data Visualization 👀
1. The csv file was loaded onto Power Bi and the various visualizations were applied. 
2. Slices have been used to show how the data represents for different countries, stockcodes, the 2 years in the dataset and the item descriptions. Giving a clear representation for each.
3. The powerpoint gives the explanation for each tab.
   
