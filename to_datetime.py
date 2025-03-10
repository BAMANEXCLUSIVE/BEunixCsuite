import pandas as pd

# Example of standardizing date formats
df1['date'] = pd.to_datetime(df1['date'], format='%Y-%m-%d')
df2['date'] = pd.to_datetime(df2['date'], format='%d-%m-%Y')