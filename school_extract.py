import json

school_dict = {}
with open('school-list.txt', 'r') as schools:
    for line in schools:
        delimited = line.split('\t')
        if len(delimited) == 2:
            school_dict[delimited[0] + ' ' + delimited[1].strip()] = True
            school_dict[delimited[0]] = True

with open('./merged-timelines.json', 'r') as file:
    for line in file:
        event = json.loads(line)
        if event['event_type'] in ['Offer', 'Unofficial Visit', 'Commitment', 'Signing', 'Official Visit', 'Enrollment',
                                   'Coach Visit', 'School Camp', 'Decommit', 'Junior Day']:
            found_school = False
            for school_key in school_dict.keys():
                if school_key in event['event_description']:
                    found_school = True
                    break
            if not found_school:
                print(event)