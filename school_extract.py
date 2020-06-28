import json

school_dict = {}
with open('./fbslist.csv','r') as schools:
    for line in schools:
        delimited = line.split('\t')
        if len(delimited) == 2:
            school_dict[delimited[0]+' '+delimited[1].strip()] = True
            school_dict[delimited[0]] = True


with open('./merged-timelines.json', 'r') as file:
    for line in file:
        event = json.loads(line)

        # school = ''
        # if event['event_type'] == 'Offer':
        #     school = event['event_description'][:event['event_description'].find(' offer')]
        # elif event['event_type'] == 'Unofficial Visit':
        #     school = event['event_description'][event['event_description'].find('unofficially visits')+20:]
        # elif event['event_type'] == 'Commitment':
        #     school = event['event_description'][event['event_description'].find('commits to')+11:]
        # elif event['event_type'] == 'Signing' and 'letter of intent' in event['event_description']:
        #     school = event['event_description'][event['event_description'].find('letter of intent to')+len('letter of intent to'):]
        # elif event['event_type'] == 'Official Visit':
        #     school = event['event_description'][event['event_description'].find(' officially visits')+18:]
        # elif event['event_type'] == 'Enrollment':
        #     school = event['event_description'][event['event_description'].find('enrolls at')+11:]
        # elif event['event_type'] == 'Coach Visit':
        #     if 'visits' in event['event_description']:
        #         school = event['event_description'][event['event_description'].find('from')+4:event['event_description'].find('visits')]
        #     elif 'visit' in event['event_description']:
        #         school = event['event_description'][event['event_description'].find('from')+4:event['event_description'].find('visit')]
        #     elif 'evaluates' in event['event_description']:
        #         school = event['event_description'][event['event_description'].find('from')+4:event['event_description'].find('evaluates')]
        # elif event['event_type'] == 'School Camp':
        #     if 'attends' in event['event_description']:
        #         school = event['event_description'][event['event_description'].find('attends')+8:event['event_description'].find('camp')]
        #     elif 'attended' in event['event_description']:
        #         school = event['event_description'][event['event_description'].find('attended')+8:]
        # elif event['event_type'] == 'Decommit':
        #     school = event['event_description'][event['event_description'].find('decommits from')+15:]
        # elif event['event_type'] == 'Junior Day':
        #     school = event['event_description'][event['event_description'].find(' at ')+4:]
        # else:
        #     school = 'Not Found PENIS PENIS PENIS'

        # if school not in school_dict and school != 'Not Found PENIS PENIS PENIS':
        #     found_school = False
        #     for school_key in school_dict.keys():
        #         if school_key in school :
        #             found_school = True
        #             break
        #     if found_school == False:
        #         print(event)
        #         print(school)
        #         raise Exception('no dice chief')

        if event['event_type'] in ['Offer','Unofficial Visit','Commitment','Signing','Official Visit','Enrollment','Coach Visit','School Camp','Decommit','Junior Day']:
            found_school = False
            for school_key in school_dict.keys():
                if school_key in event['event_description'] :
                    found_school = True
                    break
            if found_school == False:
                print(event)
        

# with open('./schools.json', 'w') as file:
#     for item in schools:
#         json.dump(item, file)
#         file.write('\n')