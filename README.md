# 247 Sports Recruiting Ranking Scraper
This project is a set of Python scripts to fetch and process publicly available data from 247 for non-commercial, personal data analysis use. I have no intention of supporting this project, so if any of the HTML changes on the site, the scraper will need to be modified.

# Getting a List of Players for a Year Range 
Players are scraped from the recruiting index page in the following format:
```json
{
  "247_id": "46038819",
  "247_url": "https://247sports.com/Player/Bryan-Bresee-46038819",
  "full_name": "Bryan Bresee",
  "year": 2020,
  "position": "DT",
  "high_school": "Damascus",
  "city": "Damascus",
  "state": "MD",
  "score": "0.9995",
  "stars": 5,
  "height_feet": 6.0,
  "height_inches": 5.0,
  "weight": 290.0
}
``` 
There's also some basic exception handling to insert default values for inconsistent or missing data.
![Error Handling](./screenshots/error-handling.png)

Before running the script, be sure to change the year range to fetch for:
```python
year_range = range(2010, 2021)
```

All dependencies are located in `requirements.txt`. To run, simple execute the command `python scrape-recruit-list.py`. The script will generate a file for each year (i.e. `recruit-list-2020.txt`) in the root directory. These files are ignored by Git.