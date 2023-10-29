
from helper import fundamentals
import pandas as pd

# insert Symbol here
symbols = ['532406']
key=['Quarterly Results', 'Profit & Loss']

data = fundamentals(symbols = symbols, key= key)
for result, key in zip(data, key):
    key = key.replace(' ', '_')
    first_key = next(iter(result))
    df = pd.DataFrame(result[first_key])

    # Save the DataFrame to an Excel file
    excel_file_path = f'{first_key.capitalize()}_{key}_data.xlsx'
    df.to_excel(excel_file_path, index=False)

    print(f'Data saved to {excel_file_path}')
