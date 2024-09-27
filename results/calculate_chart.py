import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('results/result_with_difference__lama.csv')

# Remove rows with N/A differences
df = df.dropna(subset=['Difference'])

# Create a box plot
plt.figure(figsize=(12, 6))
sns.boxplot(x='Model', y='Difference', data=df)

# Customize the plot
plt.title('Difference from Ground Truth by Model')
plt.xlabel('Model')
plt.ylabel('Difference from Ground Truth')
plt.xticks(rotation=45)

# Add a horizontal line at y=0 to represent the ground truth
plt.axhline(y=0, color='r', linestyle='--')

# Adjust layout and display the plot
plt.tight_layout()
plt.show()
# Save the plot to a file
plt.savefig('results/model_difference_boxplot.png')
plt.close()  # Close the plot to free up memory

print("Box plot saved as 'results/model_difference_boxplot.png'")

# Calculate and print summary statistics
summary = df.groupby('Model')['Difference'].agg(['mean', 'median', 'std', 'min', 'max'])
print("Summary Statistics:")
print(summary)

# Calculate average difference for each model
average_difference = df.groupby('Model')['Difference'].mean()

# Save average difference to a file
average_difference.to_csv('results/average_lix_difference_by_model.csv')
print("Average LIX score difference by model saved to 'results/average_lix_difference_by_model.csv'")
