from datetime import datetime


def convert_to_year_month_day_from_word_month(month_day_year_string):
    return datetime.strptime(month_day_year_string.replace(',', ''), '%B %d %Y').date().strftime('%Y-%m-%d')


def convert_to_year_month_day_from_number_month(month_day_year_string):
    return datetime.strptime(month_day_year_string, '%m/%d/%Y').date().strftime('%Y-%m-%d')
