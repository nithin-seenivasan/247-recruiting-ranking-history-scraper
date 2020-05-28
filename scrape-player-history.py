import emoji
from http_utility import http_get
from bs4 import BeautifulSoup


def get_ranking_history_url(player_profile_html, full_name):
    base_page = BeautifulSoup(player_profile_html, 'html.parser')
    try:
        return base_page.find('a', class_='rank-history-link')['href']
    except:
        print(emoji.emojize(f':thumbsdown: Error parsing recruiting ranking history page for {full_name}', use_aliases=True))


def get_recruiting_ranking_history(player_id, recruiting_ranking_url):
    recruiting_ranking_html = http_get(recruiting_ranking_url)
    base_page = BeautifulSoup(recruiting_ranking_html, 'html.parser')
    recruiting_ranking_ul = base_page.find('ul', class_='ranking-history-list')
    recruiting_ranking_lis = recruiting_ranking_ul.find_all('li', class_='')
    ranking_history_output = []
    for list_item in recruiting_ranking_lis:
        rank_text = list_item.find('span', class_='rank').text
        delta_element = list_item.find('span', class_='last')
        delta_value = float(delta_element.text) if delta_element.text != '-' else 0.0
        delta_value = delta_value * -1.0 if 'red' in delta_element['class'] else delta_value
        delta_inception_element = list_item.find('span', class_='inception')
        delta_inception_value = float(delta_inception_element.text) if delta_inception_element.text != '-' else 0.0
        delta_inception_value = delta_inception_value * -1.0 if 'red' in delta_inception_element['class'] else delta_inception_value
        ranking_history_output.append({
            '247_id': player_id,
            'rating': float(list_item.find('span', class_='rating').text),
            'rank': float(rank_text) if rank_text != '-' else 0.0,
            'change_date': list_item.find('span', class_='change-date').text,
            'delta': delta_value,
            'delta_inception_value': delta_inception_value
        })
    return ranking_history_output


def get_recruiting_timeline(player_id, player_profile_url):
    event_output_list = []
    recruiting_profile_html = http_get(f'{player_profile_url}TimelineEvents')
    base_page = BeautifulSoup(recruiting_profile_html, 'html.parser')
    timeline_ul = base_page.find('ul', class_='timeline-event-index_lst')
    timeline_lis = timeline_ul.find_all('li')
    for list_item in timeline_lis:
        event_output = {
            '247_id': player_id
        }
        date_and_event_split = list_item.find('b').text.split(': ')
        event_output['event_date'] = date_and_event_split[0]
        event_output['event_type'] = date_and_event_split[1]
        paragraph_tags = list_item.find_all('p')
        event_output['event_description'] = paragraph_tags[1].text
        event_output_list.append(event_output)
    return event_output_list


player_profile_url = 'https://247sports.com/Player/Bryan-Bresee-46038819/'
ranking_history_url = 'https://247sports.com/PlayerSport/Bryan-Bresee-at-Damascus-199727/RecruitRankHistory/'
print(get_recruiting_timeline(46038819, player_profile_url))