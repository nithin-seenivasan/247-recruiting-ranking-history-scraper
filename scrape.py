import math
import json
import urllib.request
from bs4 import BeautifulSoup

recruits_per_page = 50
year_range = range(2020, 2021)


def get_number_of_pages_for_year(year):
    url = f'https://247sports.com/Season/{year}-Football/CompositeRecruitRankings/'
    request = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(request)
    html = response.read()
    base_page = BeautifulSoup(html, 'html.parser')
    count_span = base_page.find('span', class_='count')
    recruit_count = int(count_span.text.strip(' ()'))
    return math.ceil(recruit_count / recruits_per_page)


def parse_page_of_recruits(url, recruit_list, year):
    request = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(request)
    html = response.read()
    base_page = BeautifulSoup(html, 'html.parser')
    rankings_page_div = base_page.find('div', class_='rankings-page__main')
    list_items = rankings_page_div.find_all(
        'li', class_='rankings-page__list-item')
    for list_item in list_items:
        name_link = list_item.find('a', class_='rankings-page__name-link')
        if(name_link != None):
            recruit_list.append({
                '247_id': name_link['href'].split('-')[-1],
                'full_name': name_link.text,
                'year': year
            })


for year in year_range:
    recruit_list = []
    number_of_pages_for_year = get_number_of_pages_for_year(year)
    for page_index in range(1, number_of_pages_for_year + 1):
        url = f'https://247sports.com/Season/{year}-Football/CompositeRecruitRankings/?page={page_index}'
        print(url)
        parse_page_of_recruits(url, recruit_list, year)
        print(recruit_list)
    with open(f'recruit-list-{year}.txt', 'w') as output_file:
        json.dump(recruit_list, output_file)
