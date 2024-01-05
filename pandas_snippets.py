import pandas as pd

pd.options.display.max_columns = 99
pd.options.mode.chained_assignment = None

# Insert a column in a custom location in df
df.insert(1, 'Col', list_of_values) # Insert list_of_values with name 'Col' in second position

# Create bins based on intervals ([pd.cut)
bins = [0, 29, 39, 55, 150]
labels = ['18-29', '30-39', '40-55', '56+']
df['AgeRange'] = pd.cut(df['Age'], bins=bins, labels=labels)
