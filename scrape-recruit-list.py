import math
import json
import emoji
import re
import urllib.request
from bs4 import BeautifulSoup

recruits_per_page = 50
year_range = range(2010, 2021)


def http_get(url):
    request = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(request)


def get_number_of_pages_for_year(year):
    url = f'https://247sports.com/Season/{year}-Football/CompositeRecruitRankings/'
    response = http_get(url)
    html = response.read()
    base_page = BeautifulSoup(html, 'html.parser')
    count_span = base_page.find('span', class_='count')
    recruit_count = int(count_span.text.strip(' ()'))
    return math.ceil(recruit_count / recruits_per_page)


def parse_page_of_recruits(url, recruit_list, year):
    response = http_get(url)
    html = response.read()
    base_page = BeautifulSoup(html, 'html.parser')
    rankings_page_div = base_page.find('div', class_='rankings-page__main')
    list_items = rankings_page_div.find_all(
        'li', class_='rankings-page__list-item')
    for list_item in list_items:
        recruit = {}
        name_link = list_item.find('a', class_='rankings-page__name-link')
        if name_link is not None:
            recruit = {
                '247_id': name_link['href'].split('-')[-1],
                '247_url': f'https://247sports.com{name_link["href"]}',
                'full_name': name_link.text,
                'year': year,
                'position': list_item.find('div', class_='position').text.strip()
            }
            meta_span_text = list_item.find('span', class_='meta').text
            try:
                high_school_and_hometown = re.findall('^([\w|\W+\s?]+)\((.*?)\)', meta_span_text)[0]
                recruit['high_school'] = high_school_and_hometown[0].strip()
                hometown_split = high_school_and_hometown[1].split(', ')
                recruit['city'] = hometown_split[0]
                recruit['state'] = hometown_split[1]
            except:
                recruit['high_school'] = ''
                recruit['city'] = ''
                recruit['state'] = ''
                print(emoji.emojize(f':thumbsdown: Error parsing high school and hometown "{meta_span_text}" for {recruit["full_name"]}', use_aliases=True))
            ranking_div = list_item.find('div', class_='rankings-page__star-and-score')
            recruit['score'] = ranking_div.find('span', class_='score').text
            star_list = ranking_div.find_all('span', class_='icon-starsolid yellow')
            recruit['stars'] = len(star_list)
            try:
                height_and_weight_text = list_item.find('div', class_='metrics').text.strip()
                height_and_weight_split = height_and_weight_text.split(' / ')
                height_split = height_and_weight_split[0].split('-')
                recruit['height_feet'] = float(height_split[0])
                recruit['height_inches'] = float(height_split[1])
                recruit['weight'] = float(height_and_weight_split[1])
            except:
                recruit['height_feet'] = 0.0
                recruit['height_inches'] = 0.0
                recruit['weight'] = 0.0
                print(emoji.emojize(f':thumbsdown: Error parsing height, feet, and weight "{height_and_weight_text}" for {recruit["full_name"]}', use_aliases=True))
        recruit_list.append(recruit)


for year in year_range:
    recruit_list = []
    number_of_pages_for_year = get_number_of_pages_for_year(year)
    for page_index in range(1, number_of_pages_for_year + 1):
        url = f'https://247sports.com/Season/{year}-Football/CompositeRecruitRankings/?page={page_index}'
        print(emoji.emojize(f':rocket: Fetching: {url}'))
        parse_page_of_recruits(url, recruit_list, year)
    with open(f'recruit-list-{year}.txt', 'w') as output_file:
        json.dump(recruit_list, output_file)
