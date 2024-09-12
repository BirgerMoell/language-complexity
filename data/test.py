import os
import shutil
import random

def create_short_folders():
    # Create new folders
    os.makedirs('diva_short', exist_ok=True)
    os.makedirs('mimers_brunn_short', exist_ok=True)

def select_and_copy_files(source_folder, dest_folder, prefix, num_files=5):
    # Get all text files from the source folder
    all_files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
    
    # Randomly select 5 files
    selected_files = random.sample(all_files, min(num_files, len(all_files)))
    
    for i, file in enumerate(selected_files, 1):
        source_path = os.path.join(source_folder, file)
        dest_path = os.path.join(dest_folder, f'{prefix}_short_{i}.txt')
        
        # Read a few sentences from the source file
        with open(source_path, 'r', encoding='utf-8') as source:
            content = source.read().split('.')[:5]  # Get first 5 sentences
            short_content = '. '.join(content) + '.'  # Rejoin with periods
        
        # Write the short content to the new file
        with open(dest_path, 'w', encoding='utf-8') as dest:
            dest.write(short_content)

# Create folders and copy files
create_short_folders()
select_and_copy_files('data/diva', 'diva_short', 'diva')
select_and_copy_files('data/mimers_brunn', 'mimers_brunn_short', 'mimers_brunn')

print("Short text files have been created in 'diva_short' and 'mimers_brunn_short' folders.")
