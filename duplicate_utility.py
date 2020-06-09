import sys
import json
import emoji


def remove_duplicates(list_file_path, identifying_attribute):
    exists = {}
    duplicates = {}
    duplicates_handled = {}
    with open(list_file_path, 'r') as list_file:
        index = 0
        lines = list_file.readlines()
        for line in lines:
            data = json.loads(line)
            if exists.get(data[identifying_attribute]):
                print(emoji.emojize(f':thumbsdown: Duplicate data found on line {index}: {data[identifying_attribute]}', use_aliases=True))
                if data[identifying_attribute] in duplicates:
                    duplicates[data[identifying_attribute]].push(index)
                else:
                    duplicates[data[identifying_attribute]] = [index]
            else:
                exists[data[identifying_attribute]] = True
            index += 1
    if len(duplicates) > 0:
        print(emoji.emojize(f':thumbsdown: {len(duplicates)} duplicates found', use_aliases=True))
        with open(list_file_path, 'w') as list_file:
            for line in lines:
                data = json.loads(line)
                if data[identifying_attribute] not in duplicates or data[identifying_attribute] not in duplicates_handled:
                    if data[identifying_attribute] in duplicates:
                        duplicates_handled[data[identifying_attribute]] = True
                    list_file.write(line)
            print(emoji.emojize(f':thumbsup: Duplicates removed', use_aliases=True))


list_file_path = sys.argv[1]
remove_duplicates(list_file_path, identifying_attribute='247_id')
