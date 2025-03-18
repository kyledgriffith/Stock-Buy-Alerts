import pandas as pd

# Define the correct column names (adjust as needed)
column_names = ["timestamp", "open", "high", "low", "close", "volume", "symbol"]

# Load the CSV file
file_path = "C:/Users/kyleg/OneDrive/Documents/Stocks Forecasting/DPST.csv"  # Change this as needed
df = pd.read_csv(file_path, names=column_names, header=0)

# Display the first few rows
print(df.head())