import pandas as pd

pd.options.display.max_columns = 99
pd.options.mode.chained_assignment = None

# Insert a column in a custom location in df
df.insert(1, 'Col', list_of_values) # Insert list_of_values with name 'Col' in second position

# Create bins based on intervals ([pd.cut)
bins = [-999, 11, 12, 24, 999]
labels = ['A', 'B', 'C', 'D']
df['ContractDuration'] = pd.cut(df['col'], bins=bins, labels=labels)
