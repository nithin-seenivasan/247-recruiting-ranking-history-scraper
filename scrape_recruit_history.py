import emoji
from http_utility import http_get
from date_utility import *
from bs4 import BeautifulSoup


def get_ranking_history_url(player_profile_url, full_name):
    html = http_get(player_profile_url)
    base_page = BeautifulSoup(html, 'html.parser')
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
        rating_text = list_item.find('span', class_='rating').text
        rating_value = float(rating_text) if rating_text != '-' else 0.0
        delta_element = list_item.find('span', class_='last')
        delta_value = float(delta_element.text) if delta_element.text != '-' else 0.0
        delta_value = delta_value * -1.0 if 'red' in delta_element['class'] else delta_value
        delta_inception_element = list_item.find('span', class_='inception')
        delta_inception_value = float(delta_inception_element.text) if delta_inception_element.text != '-' else 0.0
        delta_inception_value = delta_inception_value * -1.0 if 'red' in delta_inception_element['class'] else delta_inception_value
        ranking_history_output.append({
            '247_id': player_id,
            'rating': rating_value,
            'rank': float(rank_text) if rank_text != '-' else 0.0,
            'change_date': convert_to_year_month_day_from_number_month(list_item.find('span', class_='change-date').text),
            'delta': delta_value,
            'delta_inception_value': delta_inception_value
        })
    return ranking_history_output


def get_recruiting_timeline(player_id, player_profile_url, full_name):
    recruiting_profile_html = http_get(f'{player_profile_url}/TimelineEvents')
    base_page = BeautifulSoup(recruiting_profile_html, 'html.parser')
    number_of_timeline_pages = 1
    try:
        number_of_timeline_pages = int(base_page.find_all('a', class_='pagn_link')[-2].text)
    except:
        print(emoji.emojize(f':warning: Couldn\'t parse pagination for {full_name}',
                            use_aliases=True))
    event_output_list = []
    timeline_ul = base_page.find('ul', class_='timeline-event-index_lst')
    timeline_lis = timeline_ul.find_all('li')
    for page in range(0, number_of_timeline_pages):
        if page != 0:
            recruiting_profile_html = http_get(f'{player_profile_url}/TimelineEvents/?page={page}')
            base_page = BeautifulSoup(recruiting_profile_html, 'html.parser')
            timeline_ul = base_page.find('ul', class_='timeline-event-index_lst')
            timeline_lis = timeline_ul.find_all('li')
        for list_item in timeline_lis:
            event_output = {
                '247_id': player_id
            }
            date_and_event_split = list_item.find('b').text.split(': ')
            event_output['event_date'] = convert_to_year_month_day_from_word_month(date_and_event_split[0])
            event_output['event_type'] = date_and_event_split[1]
            paragraph_tags = list_item.find_all('p')
            event_output['event_description'] = paragraph_tags[1].text
            event_output_list.append(event_output)
    return event_output_list
