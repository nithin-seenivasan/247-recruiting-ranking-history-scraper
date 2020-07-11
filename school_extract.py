import json

school_dict = {}
with open('./school-list-normlized.txt', 'r') as schools:
    for line in schools:
        delimited = line.split('\t')
        if len(delimited) == 3:
            school_dict[delimited[0] + ' ' + delimited[1].strip()] = delimited[2].strip()
            school_dict[delimited[0]] = delimited[2].strip()


with open('./merged-timelines.json', 'r') as file:
    school_list = list(school_dict.keys())
    school_list.sort(key=len, reverse= True)
    for line in file:
        event = json.loads(line)
        if event['event_type'] in ['Offer', 'Unofficial Visit', 'Commitment', 'Signing', 'Official Visit', 'Enrollment',
                                   'Coach Visit', 'School Camp', 'Decommit', 'Junior Day']:
            found_school = False
            for school_key in school_list:
                if school_key in event['event_description'] and not found_school:
                    found_school = True
                    event.update({
                        'school':school_dict[school_key]
                    })
                    with open ('./merged-timelines-schools2.json','a') as s:
                            json.dump(event, s)
                            s.write('\n')
        else:
            event.update({
                'school': None
            })
            with open ('./merged-timelines-schools2.json','a') as s:
                    json.dump(event, s)
                    s.write('\n')
            #if not found_school:
                #print(event)