from http_utility import http_get
from bs4 import BeautifulSoup
from datetime import datetime
import json
import glob

def event_pages(player_url):
    url = f'{player_url}/TimelineEvents/'
    html = http_get(url)
    base_page = BeautifulSoup(html, 'html.parser')
    try:
        num_event_pages = base_page.find_all('a', class_ = 'pagn_link')[-2].get_text()
    except:
        num_event_pages = 1
    return int(num_event_pages)

def get_event_items(url):
    html = http_get(url)
    base_page = BeautifulSoup(html, 'html.parser')
    events_page_ul = base_page.find('ul', class_='timeline-event-index_lst')
    list_items = events_page_ul.find_all( 'div', class_ = 'left')
    for list_item in list_items:
        event = {}
        if list_item is not None:
            parse_player_from_url = url.split('/')[-3]
            name_id_split = parse_player_from_url.split('-')
            player_name = ' '.join(name_id_split[0:-1])
            player_id = name_id_split[-1]
            event_date_type = list_item.find('b').text.strip()
            event_type = event_date_type.split(':')[-1].strip()
            event_date = event_date_type.split(':')[0].replace(',','')
            date_convert = datetime.strptime(event_date, '%B %d %Y').date()
            event_description = list_item.find('p').text.strip()
            event = {
                '247_id': player_id,
                'player_name': player_name,
                'event_type': event_type,
                'event_date': date_convert.strftime('%Y-%m-%d'),
                'event_description': event_description
            }
            event_list.append(event)

path = './recruit-lists/test-list.json'
for file in glob.glob(path):
    with open(file,'r') as recruit_list:
        for cnt, line in enumerate(recruit_list):
            recruit = json.loads(line)
            player_url = recruit['247_url']
            recruit_pages = event_pages(player_url)
            event_list = []
            for pagen in range(1, recruit_pages + 1):
                url = f'{player_url}/TimelineEvents/?Page={pagen}'
                get_event_items(url)   
            print(event_list)
            file_name = f'./recruit-lists/recruit-lists-events.json1'
            with open(file_name, 'w') as output_file:
                for line in event_list:
                    json.dump(line,output_file)
                    output_file.write('\n')
            print(f'Wrote {file} recruits to {file_name}')