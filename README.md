# DSA2040A Summer Semester Group 5

## Group Details

- EDA- Ambachow
- Visualization- Cynthia 
- Transformation- Samuel 
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

## Techniques Used

## Tools Used

## Instructions to Run Notebooks

1. Install the necessary modules
   
   ```bash
   pip install jupyter numpy pandas mlxtend
   ```
