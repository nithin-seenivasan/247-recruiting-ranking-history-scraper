with open('school-list.txt', 'r') as schools:
    list = []
    for line in schools:
        delimited = line.split('\t')
        if len(delimited) == 2:
            line = line.strip()
            line += '\t' + delimited[0] + '\n'
            list.append(line)

with open('school-list-normlized.txt','w') as f:
    for school in list:
        f.write(school)