
from helper import fundamentals, sector
import pandas as pd
from matplotlib import pyplot as plt 
import os
import numpy as np

# insert Symbol here
company_name = input("Enter the company's symbol => ")

symbols = [company_name]

def stock_plots(symbols):
    key=['Quarterly Results', 'Profit & Loss', 'Balance Sheet', 'Cash Flows', 'Ratios', 'Shareholding Pattern']

    data, title = fundamentals(symbols = symbols, key= key)

    plots = ['QoQ', 'YoY', 'Balance_Sheet', 'Cash_Flows', 'Ratios', 'Shareholding Pattern']

    count = 1

    for dfs, plot in zip(data, plots):
        # Create a directory for the company's plots (if it doesn't exist)
        plot_folder = f"plots\\{title.lower()}_{plot}_plots"
        os.makedirs(plot_folder, exist_ok=True)

        transposed_data = dfs.transpose()

        # Set the first row as the column headers
        transposed_data.columns = transposed_data.iloc[0]

        # Remove the first row (it's a duplicate of column names)
        transposed_data = transposed_data[1:]

        if count == 1:
            percentage_columns = ['OPM%', 'Tax%']

        elif count == 2:
            percentage_columns = ['OPM%', 'Tax%', 'DividendPayout%']


        elif count == 3 or count == 4:
            percentage_columns = []

        elif count == 5:
            percentage_columns = ['ROCE%']
            # transposed_data[transposed_data.columns[:-1].tolist()] = transposed_data[transposed_data.columns[:-1].tolist()].apply(pd.to_numeric, errors='coerce')

        elif count == 6:
            percentage_columns = transposed_data.columns[:-1].tolist()

        try:
            selected_columns = [col for col in transposed_data.columns if col not in percentage_columns]
            transposed_data[selected_columns] = transposed_data[selected_columns].apply(pd.to_numeric, errors='coerce')
            transposed_data = transposed_data.fillna(0)
        except Exception as e:
            print(str(e))

        for column in percentage_columns:
            if column in transposed_data.columns:
                transposed_data[column] = transposed_data[column].str.replace('%', '').str.replace(',', '')
        
        try:
            # Convert percentage columns to float
            transposed_data[percentage_columns] = transposed_data[percentage_columns].astype(float)
        except:
            transposed_data[percentage_columns] = transposed_data[percentage_columns].apply(lambda x: pd.to_numeric(x.str.strip(), errors='coerce'))

            # Convert the columns to float, replacing NaN with None
            transposed_data[percentage_columns] = transposed_data[percentage_columns].astype(float).replace({np.nan: None})


        # Iterate through the columns and create histograms
        for column in transposed_data.columns:
            plt.figure(figsize=(10, 5))
            if column in percentage_columns:
                # Skip applying 'str' accessor to percentage columns
                values = transposed_data[column].astype(float)
            else:
                try:
                    # For other columns, remove commas and convert to float
                    values = transposed_data[column].str.replace(',', '').astype(float)
                except:
                    values = transposed_data[column].astype(float)
            
            bars = plt.bar(transposed_data.index, values)
            
            # # Add value labels on top of the bars
            for bar, value in zip(bars, values):
                if np.isfinite(value):
                    plt.text(bar.get_x() + bar.get_width() / 2, value, str(value), ha='center', va='bottom')
            
            plt.title(f'Plot of {column}')
            plt.xlabel('Dates')
            plt.ylabel('Values')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the plot in the folder
            plot_filename = os.path.join(plot_folder, f'{company_name.lower()}_{column}_{plot}_plot.png')
            plt.savefig(plot_filename)
            plt.close()

        # incrementing the count for tables
        count += 1
        print(f"Plots saved in the folder: {plot_folder}")


stock_plots(symbols = symbols)

print("-"* 70)

ls = sector(symbols = symbols)
print(ls)



