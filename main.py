
from helper import fundamentals
import pandas as pd
from matplotlib import pyplot as plt 
import os

# insert Symbol here
company_name = input("Enter the symbol => ")

symbols = [company_name]
key=['Quarterly Results', 'Profit & Loss']

data = fundamentals(symbols = symbols, key= key)

# Create a directory for the company's plots (if it doesn't exist)
plot_folder = f"{company_name.lower()}_plots"
os.makedirs(plot_folder, exist_ok=True)

transposed_data = data.transpose()

# Set the first row as the column headers
transposed_data.columns = transposed_data.iloc[0]

# Remove the first row (it's a duplicate of column names)
transposed_data = transposed_data[1:]

# Define percentage columns
percentage_columns = ['OPM%', 'Tax%']
for column in percentage_columns:
    transposed_data[column] = transposed_data[column].str.replace('%', '').str.replace(',', '')

# Convert percentage columns to float
transposed_data[percentage_columns] = transposed_data[percentage_columns].astype(float)

# Iterate through the columns and create histograms
for column in transposed_data.columns:
    plt.figure(figsize=(10, 5))
    if column in percentage_columns:
        # Skip applying 'str' accessor to percentage columns
        values = transposed_data[column].astype(float)
    else:
        # For other columns, remove commas and convert to float
        values = transposed_data[column].str.replace(',', '').astype(float)
    
    bars = plt.bar(transposed_data.index, values)
    
    # Add value labels on top of the bars
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, value, str(value), ha='center', va='bottom')
    
    plt.title(f'Plot of {column}')
    plt.xlabel('Dates')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot in the folder
    plot_filename = os.path.join(plot_folder, f'{company_name.lower()}_{column}_plot.png')
    plt.savefig(plot_filename)
    plt.close()

print(f"Plots saved in the folder: {plot_folder}")



