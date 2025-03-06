df1.rename(columns={'user_id': 'userID'}, inplace=True)
df2.rename(columns={'userID': 'user_id'}, inplace=True)

import os

def align_schema():
    print("Aligning schema...")

if __name__ == "__main__":
    align_schema()
    print("Schema alignment complete.")

import pandas as pd

def align_schema():
    print("Aligning schema...")
    df = pd.read_csv('sample_data.csv')
    df.columns = ['ID', 'Name', 'Age']
    print(df)

if __name__ == "__main__":
    align_schema()
    print("Schema alignment complete.")

