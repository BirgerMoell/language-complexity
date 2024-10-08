These are files pertaining to an investigation about how well large language models can estimate language complexity.

LIX
===
The 'real' lix scores are found in the third column of the file:
data/extracted_paragraphs.csv.

The scores lix scores from models were extracted by first calling the LLMs with the scripts:
calculate_lix_with_model.py
calculate_lix_with_openai.py

The output from those scripts ended up in the folder:
data100/lix_raw_data

The results were first extracted from all the verbiage in the raw data files by means of a regular expression, using the script:
extract_lix_from_llm_output.py

The results from running that script is stored in the file:
data100/lix_results.txt

The raw data files from which no result could be automatically extracted were manually screened. The results from that manual screening ended up in:
data100/lix_digging_results.txt

All the results are summarized in:
data100/lix_total_results.txt (for everything)
data100/lix_openai_results.txt
data100/lix_llama_results.txt

UAS
===
The 'real' dependency trees (ground truth according to Stanza) are found in the 'ground_truth' folder.

The models produced dependency parses using the scripts:
call_openAI.py (for o1-mini and gpt-4o-mini)
dep_parse_with_model.py (for llama)

The output from those scripts ended up in the folder:
data100/dep_parse_raw_data

The results were first extracted from the raw data files using the script:
extract_dep_parse_from_llm_output.py

and then cleaned using the script:
clean_dep_parse_output_files.py

The results of the extraction and cleaning ended up in the folder:
data100/dep_parse_results

Then, UAS was computed using the script:
compute_uas.py


