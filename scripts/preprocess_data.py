import pandas as pd
import os

def load_and_preprocess(file_path):
    # Load CSV file
    df = pd.read_csv(file_path)

    # Rename the first column to 'Datetime' (assuming it's unnamed)
    df.rename(columns={df.columns[0]: 'Datetime'}, inplace=True)

    # Convert to datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Sort in chronological order
    df.sort_values(by='Datetime', inplace=True)

    # Drop missing values
    df.dropna(inplace=True)

    # Extract time from Datetime
    df['Time'] = df['Datetime'].dt.time

    # Define stock market opening and closing times
    market_open = pd.to_datetime("09:30:00").time()
    market_close = pd.to_datetime("16:00:00").time()
    market_open_end = pd.to_datetime("10:00:00").time()
    market_close_start = pd.to_datetime("15:30:00").time()

    # Create a column indicating if it's in the first/last 30 minutes of market hours
    df['Market_Opening_or_Closing'] = df['Time'].between(market_open, market_open_end) | df['Time'].between(market_close_start, market_close)

    # Create a column indicating if the time is outside of normal trading hours
    df['Outside_Trading_Hours'] = ~df['Time'].between(market_open, market_close)

    # Drop the temporary 'Time' column (optional)
    df.drop(columns=['Time'], inplace=True)

    return df

# Batch processing multiple stock files
if __name__ == "__main__":
    data_folder = "../data"
    output_folder = "../processed_data"  # Change to `data_folder` if overwriting

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all CSV files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(data_folder, filename)
            print(f"Processing {filename}...")

            df = load_and_preprocess(file_path)

            # Save the processed file
            output_path = os.path.join(output_folder, filename)
            df.to_csv(output_path, index=False)
            print(f"Saved processed data to {output_path}")

    print("Processing complete for all stock files!")