import shutil

def replace_single_quotes_in_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            modified_line = line.replace("'", "")
            output_file.write(modified_line)

# Specify the paths for the input file and the output file
input_file_path = "title.basics.tsv/data_cassandra.tsv"
output_file_path = "title.basics.tsv/data_cassandra1.tsv"

# Create a new file with modified content
replace_single_quotes_in_file(input_file_path, output_file_path)

# Replace the original file with the modified file
shutil.move(output_file_path, input_file_path)