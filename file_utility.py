import json
import emoji


def write_to_file_for_s3_athena(index, data_list, file_name):
    try:
        if len(data_list) > 0:
            with open(file_name, 'a') as file:
                for item in data_list:
                    json.dump(item, file)
                    file.write('\n')
            print(emoji.emojize(f':file_folder: Wrote recruit at index {index} to {file_name}', use_aliases=True))
        else:
            print(emoji.emojize(f':file_folder: Nothing to write for recruit at index {index} for {file_name}', use_aliases=True))
    except:
        print(emoji.emojize(f':thumbsdown: Failed to write recruit at index {index} to {file_name}', use_aliases=True))