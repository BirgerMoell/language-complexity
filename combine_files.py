import pandas as pd

# Read the CSV files
add_analysis_llm_short = pd.read_csv('results/add_analysis_llm_short.csv')
add_analysis = pd.read_csv('results/add_analysis.csv')

# Merge the dataframes on the 'file' column
combined_df = pd.merge(add_analysis_llm_short, add_analysis, on='file', suffixes=('_llm_short', ''))

# Calculate the difference
combined_df['score_difference'] = combined_df['score'] - combined_df['score_llm_short']

# Reorder columns
columns_order = ['file', 'score_llm_short', 'score', 'score_difference', 'text']
combined_df = combined_df[columns_order]

# Save the combined dataframe to a new CSV file
combined_df.to_csv('results/combined_add_analysis.csv', index=False)

print("Combined file created: results/combined_add_analysis.csv")
