import sys
import os


def merge_list(list_directory_path, output_file_path):
    for root, directories, files in os.walk(list_directory_path, onerror=None):
        for file in files:
            path = os.path.join(root, file)
            file_to_merge = open(path)
            output_file = open(output_file_path, 'a')
            for line in file_to_merge.readlines():
                output_file.write(line)
                output_file.write(line)


list_directory_path = sys.argv[1]
output_file_path = sys.argv[2]
merge_list(list_directory_path, output_file_path)