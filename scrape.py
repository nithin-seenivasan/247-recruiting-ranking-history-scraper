import urllib.request
from bs4 import BeautifulSoup

url = "https://247sports.com/Season/2020-Football/CompositeRecruitRankings/?InstitutionGroup=HighSchool"

request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(request)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
rankings_page_div = soup.find('div', class_='rankings-page__main')
list_items = rankings_page_div.find_all(
    'li', class_='rankings-page__list-item')
for list_item in list_items:
    name_link = list_item.find('a', class_='rankings-page__name-link')
    if(name_link != None):
        print(name_link['href'].split('-')[-1])
        print(name_link.text)
