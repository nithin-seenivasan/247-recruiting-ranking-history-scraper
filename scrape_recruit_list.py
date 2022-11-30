import sys
import math
import json
import emoji
import re
from http_utility import http_get
from bs4 import BeautifulSoup


def get_number_of_pages_for_year(year, recruits_per_page):
    url = f'https://247sports.com/Season/{year}-Football/CompositeRecruitRankings/'
    html = http_get(url)
    base_page = BeautifulSoup(html, 'html.parser')
    count_span = base_page.find('span', class_='count')
    #recruit_count = int(count_span.text.strip('()')) 
    #It was reading weirdly from the website, so had to change to this (29.11.22)
    s=count_span.text
    x = s[s.find('(')+1:s.find(')')]
    recruit_count=int(x)
    return math.ceil(recruit_count / recruits_per_page)

    return math.ceil(recruit_count / recruits_per_page)


def parse_page_of_recruits(url, recruit_list, year):
    html = http_get(url)
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
                print(emoji.emojize(
                    f':thumbsdown: Error parsing high school and hometown "{meta_span_text}" for {recruit["full_name"]}',
                    use_aliases=True))
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
                print(emoji.emojize(
                    f':thumbsdown: Error parsing height, feet, and weight "{height_and_weight_text}" for {recruit["full_name"]}',
                    use_aliases=True))
        recruit_list.append(recruit)


recruits_per_page = 50
year_range = range(int(sys.argv[1]), int(sys.argv[2]))
recruit_list_path = './recruit-lists'
for year in year_range:
    recruit_list = []
    number_of_pages_for_year = get_number_of_pages_for_year(year, recruits_per_page)
    for page_index in range(1, number_of_pages_for_year + 1):
        url = f'https://247sports.com/Season/{year}-Football/CompositeRecruitRankings/?page={page_index}'
        print(emoji.emojize(f':rocket: Fetching: {url}'))
        parse_page_of_recruits(url, recruit_list, year)
    file_name = f'{recruit_list_path}/recruit-list-{year}.json'
    with open(file_name, 'w') as output_file:
        json.dump(recruit_list, output_file)
    print(emoji.emojize(f':file_folder: Wrote {year} recruits to {file_name}'))
