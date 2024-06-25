import pandas as pd

# Load the CSV file
file_path = 'part-00000-bb6b0296-2d8b-4830-818e-331a731983fc-c000.csv/part-00000-bb6b0296-2d8b-4830-818e-331a731983fc-c000.csv'
df = pd.read_csv(file_path)

# Convert 'date' column to datetime for accurate comparison
df['date'] = pd.to_datetime(df['date'])

# Define the specific dates of interest
dates_of_interest = ["2020-06-29", "2022-02-28", "2021-08-30", "2021-11-29", "2021-12-20"]

# Convert dates of interest to datetime
dates_of_interest = [pd.to_datetime(date) for date in dates_of_interest]

# Initialize a DataFrame to hold the counts of flights on the specified dates
result_df_specific_dates = pd.DataFrame(index=dates_of_interest, columns=['Warszawa', 'Ukraine', 'Louisiana', 'La Palma']).fillna(0)

# Populate the result DataFrame with flight counts on the specified dates
for date in dates_of_interest:
    result_df_specific_dates.loc[date, 'Warszawa'] = df[(df['region'].str.lower() == 'warszawa') & (df['date'] == date)].shape[0]
    result_df_specific_dates.loc[date, 'Ukraine'] = df[(df['region'].str.lower() == 'ukraine') & (df['date'] == date)].shape[0]
    result_df_specific_dates.loc[date, 'Louisiana'] = df[(df['region'].str.lower() == 'louisiana') & (df['date'] == date)].shape[0]
    result_df_specific_dates.loc[date, 'La Palma'] = df[(df['region'].str.lower() == 'la palma') & (df['date'] == date)].shape[0]

# Format index as string for better readability
result_df_specific_dates.index = result_df_specific_dates.index.strftime('%Y-%m-%d')

# save and print
result_df_specific_dates.to_csv('flight_counts_on_specific_dates.csv')
print(result_df_specific_dates)

