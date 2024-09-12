import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('results/edited_complexity.csv')

# Sort the dataframe by the difference column in descending order
df_sorted = df.sort_values('difference', ascending=False)

# Shorten file names
df_sorted['short_name'] = df_sorted['file'].str.replace('.txt', '').str[-10:]

# Set up the plot style
plt.figure(figsize=(12, 6))

# Create a bar plot
x = range(len(df_sorted))
width = 0.35

plt.bar(x, df_sorted['llm_complexity_score'], width, label='LLM', alpha=0.8)
plt.bar([i + width for i in x], df_sorted['local_complexity_score'], width, label='Local', alpha=0.8)

# Customize the plot
plt.xlabel('Files')
plt.ylabel('Complexity Score')
plt.title('LLM vs Local Complexity Scores')
plt.xticks([i + width/2 for i in x], df_sorted['short_name'], rotation=45, ha='right')
plt.legend()

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig('complexity_difference_plot_simple_2.png', dpi=300)
plt.close()

print("Plot saved as complexity_difference_plot_simple.png")
