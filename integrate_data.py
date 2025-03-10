import pandas as pd

def integrate_data(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    combined_df = pd.concat([df1, df2])
    return combined_df

data = integrate_data('data1.csv', 'data2.csv')
print(data.head())

import os

def integrate_data():
    print("Integrating data...")

if __name__ == "__main__":
    integrate_data()
    print("Data integration complete.")


import pandas as pd

def integrate_data():
    print("Integrating data...")
    df = pd.read_csv('sample_data.csv')
    print(df)

if __name__ == "__main__":
    integrate_data()
    print("Data integration complete.")

