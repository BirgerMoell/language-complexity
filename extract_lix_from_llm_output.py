import os
import re

# Replace with the actual path to your directory
directory = 'c:/GitHub/birger/language-complexity/data100/lix_raw_data/long_prompt/gemini-pro'

output_file = 'c:/GitHub/birger/language-complexity/data100/lix_results_gemini-pro.txt'

with open(output_file, 'w', encoding='utf-8') as out_file:
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as in_file:
                    content = in_file.read()
                    lix_matches = re.findall(r'.*LIX\s*(=|≈)\s*(\d+((\.|,)\d+)?).*', content)
                    if lix_matches:
                        last_lix_line = f"LIX {lix_matches[-1][0]} {lix_matches[-1][1]}"
                        out_file.write(f"{file}: {last_lix_line}\n")
                    else:
                        out_file.write(f"{file}: No LIX found\n")
print(f"LIX results have been written to {output_file}")
