import pandas as pd

# Load the two CSV files into separate dataframes
planetmarket_df = pd.read_csv('/Users/x/PLANET_ALLDATA_PERFECT_WUXING_Y2006to2023.csv', low_memory=False)
aspects_df = pd.read_csv('/Usersx/aspects_results_2006to2023.csv', low_memory=False)

# Merge the two dataframes on the "Time" column
combined_df = planetmarket_df.merge(aspects_df, on='Time', how='outer')

# Export the combined dataframe to a new CSV file
combined_df.to_csv('/Users/x/alldata_onesheet.csv', index=False)
