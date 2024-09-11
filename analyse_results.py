import pandas as pd
import os

def analyze_complexity_results(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Sort the dataframe by complexity score
    df_sorted = df.sort_values('complexity_score', ascending=False)

    # Get the 10 most complex, 10 least complex, and 10 middle complexity texts
    most_complex = df_sorted.head(10)
    least_complex = df_sorted.tail(10)
    middle_complex = df_sorted.iloc[len(df_sorted)//2-5:len(df_sorted)//2+5]

    # Combine the results
    results = pd.concat([most_complex, middle_complex, least_complex])

    # Save the results to a file
    with open(output_file, 'w') as f:
        f.write("10 Most Complex Texts:\n")
        f.write(most_complex.to_string(index=False) + "\n\n")

        f.write("10 Middle Complexity Texts:\n")
        f.write(middle_complex.to_string(index=False) + "\n\n")

        f.write("10 Least Complex Texts:\n")
        f.write(least_complex.to_string(index=False) + "\n\n")

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    input_file = "results/complexity_analysis.csv"
    output_file = "results/complexity_summary.txt"

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
    else:
        analyze_complexity_results(input_file, output_file)