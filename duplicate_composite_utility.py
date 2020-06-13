import sys
import json
import emoji


def remove_composite_duplicates(list_file_path):
    exists = {}
    duplicates = {}
    duplicates_handled = {}
    with open(list_file_path, 'r') as list_file:
        index = 0
        lines = list_file.readlines()
        for line in lines:
            data = json.loads(line)
            composite_key = build_composite_key(data)
            if exists.get(composite_key):
                print(emoji.emojize(f':thumbsdown: Duplicate data found on line {index}: {composite_key}', use_aliases=True))
                if composite_key in duplicates:
                    duplicates[composite_key].push(index)
                else:
                    duplicates[composite_key] = [index]
            else:
                exists[composite_key] = True
            index += 1
    if len(duplicates) > 0:
        print(emoji.emojize(f':thumbsdown: {len(duplicates)} duplicates found', use_aliases=True))
        with open(list_file_path, 'w') as list_file:
            for line in lines:
                data = json.loads(line)
                composite_key = build_composite_key(data)
                if composite_key not in duplicates or composite_key not in duplicates_handled:
                    if composite_key in duplicates:
                        duplicates_handled[composite_key] = True
                    list_file.write(line)
            print(emoji.emojize(f':thumbsup: Duplicates removed', use_aliases=True))


def build_composite_key(data):
    composite_key = ''
    for key in data.keys():
        composite_key += data[key]
    return composite_key


list_file_path = sys.argv[1]
remove_composite_duplicates(list_file_path)
