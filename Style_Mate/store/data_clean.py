import pandas as pd
df = pd.read_csv('data.csv')
df.loc[:, ['Name', 'Age']]
print(df)