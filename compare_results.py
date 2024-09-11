import pandas as pd
import numpy as np
from scipy import stats

# Read the CSV files
add_df = pd.read_csv('results/add_analysis.csv')
complexity_df = pd.read_csv('results/complexity_analysis.csv')

# Check if 'filename' column exists in both dataframes
if 'file' not in add_df.columns or 'file' not in complexity_df.columns:
    print("Error: 'filename' column is missing in one or both dataframes.")
    print(f"Columns in add_df: {add_df.columns}")
    print(f"Columns in complexity_df: {complexity_df.columns}")
    exit(1)

# Merge the dataframes on the filename column
merged_df = pd.merge(add_df, complexity_df, on='file', how='inner')

# Check if the merge was successful
if merged_df.empty:
    print("Error: The merge resulted in an empty dataframe. Check if there are matching filenames.")
    exit(1)

# Calculate the correlation coefficient and p-value
correlation, p_value = stats.pearsonr(merged_df['add_score'], merged_df['complexity_score'])

print(f"Correlation coefficient: {correlation}")
print(f"P-value: {p_value}")

# Interpret the results
if p_value < 0.05:
    print("The correlation is statistically significant.")
    if correlation > 0:
        print("There is a positive correlation between ADD and complexity scores.")
    else:
        print("There is a negative correlation between ADD and complexity scores.")
else:
    print("There is no statistically significant correlation between ADD and complexity scores.")

# Calculate and print the mean scores
print(f"\nMean ADD score: {merged_df['add_score'].mean():.4f}")
print(f"Mean complexity score: {merged_df['complexity_score'].mean():.4f}")

# Find and print the files with the highest and lowest scores for each measure
print("\nFiles with highest and lowest scores:")
for measure in ['add_score', 'complexity_score']:
    highest = merged_df.loc[merged_df[measure].idxmax()]
    lowest = merged_df.loc[merged_df[measure].idxmin()]
    print(f"\nHighest {measure}:")
    print(f"  File: {highest['file']}, Score: {highest[measure]:.4f}")
    print(f"Lowest {measure}:")
    print(f"  File: {lowest['file']}, Score: {lowest[measure]:.4f}")

# Create a scatter plot
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(merged_df['add_score'], merged_df['complexity_score'], alpha=0.5)
plt.xlabel('ADD Score')
plt.ylabel('Complexity Score')
plt.title('ADD Score vs Complexity Score')
plt.savefig('results/add_vs_complexity_scatter.png')
plt.close()

print("\nScatter plot saved as 'results/add_vs_complexity_scatter.png'")
