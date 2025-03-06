df1.drop_duplicates(inplace=True)
df1.fillna(method='ffill', inplace=True)

import os

def cleanse_data():
    print("Cleansing data...")

if __name__ == "__main__":
    cleanse_data()
    print("Data cleansing complete.")

