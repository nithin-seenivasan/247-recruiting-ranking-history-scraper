Forked from https://github.com/scottenriquez/247-recruiting-ranking-history-scraper

## About College Football Recruiting 
Despite being played by amateur student-athletes, college football has become a multi-billion dollar industry. Most likely due to the emotional connection to an academic institution and the incredibly entertaining and volatile lack of parity and consistency amongst teams, college football fans tend to be even more diehard than their NFL counterparts, particularly in the South. Though college football is played by undergraduate and graduate students, players are scouted as recruits as early as middle school. These recruits are evaluated based on several factors that indicate their success at both the collegiate and professional levels of football. Whether physical attributes like height and weight or skill sets like blocking and catching, all of these attributes plus countless others are synthesized into a rating. Recruits are then offered by universities culminating in commitments and signings. A good recruiting class can be an indication of future success for a college football team provided that the coaching staff develops talents as expected.

## Source Code
This [repository](https://github.com/scottenriquez/247-recruiting-ranking-history-scraper) is a set of Python and shell scripts to fetch and process publicly available data from 247 for non-commercial, personal data analysis use to be done using AWS Athena. It's co-authored by [Callen Trail](https://callen.xyz). As is the nature of web scrapers, the HTML parsing code is brittle. If the page structure changes on the site, the scripts will need to be modified. The process is split into three stages.

## Stage One: Fetching Recruit Lists by Year
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

All Python dependencies are located in `requirements.txt`. To run, simple execute the command `python scrape_recruit_list.py <START_YEAR> <END_YEAR>`. This range dictates the volume of data captured by core logic of the script like so:
```python
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
```

The script will generate a file for each year (i.e. `recruit-list-2020.json`) in the `/recruit-lists` directory. The files in this directory are treated as build output and ignored via the `.gitignore`. There's also some basic exception handling to insert default values for inconsistent or missing data.

## Stage Two: Obtaining Ranking History and Recruiting Timeline Events
With a set of lists generated by stage one, the `process_recruits.py` script fetches and parses the complete ranking history and timeline of events (i.e. official visits, offers, etc.). To run, pass a recruiting list from stage one and the corresponding year to produce the files: `python process_recruits.py 2020 recruit-lists/recruit-list-2020.json`.

Recruit ranking histories are stored in the following path: `/recruit-ranking-histories/{year}/{247_id}.json`. For example, Bryan Bresee's path would be `/recruit-ranking-histories/2020/46038819.json` in the following format:
```json
{
    "247_id": "46038819",
    "rating": 0.9995,
    "rank": 1,
    "change_date": "2020-01-31",
    "delta": -0.0002,
    "delta_inception": 0.0295
}
```

Recruiting timeline events are stored in the following path: `/recruit-timeline-histories/{year}/{247_id}.json`. For example, Bryan Bresee's path would be `/recruit-timeline-histories/2020/46038819.json` in the following format:
```json
{
    "247_id": "46038819",
    "event_date": "2020-01-08",
    "event_type": "Enrollment",
    "event_description": "Bryan Bresee enrolls at Clemson Tigers"
}
```

Given the large amount of data to process during stage two, this repository also includes a bootstrapping shell script for EC2 instances to install the Python tooling, configure the virtual environment, and pull the data from stage one via S3. Pass the following to the user data field when provisioning a new EC2 instance:
```shell
#!/bin/bash
sudo yum install git -y
sudo yum install python3 -y
git clone https://github.com/scottenriquez/247-recruiting-ranking-history-scraper.git
cd 247-recruiting-ranking-history-scraper
mkdir recruit-lists
mkdir recruit-ranking-histories
mkdir recruit-timeline-histories
aws s3 cp s3://247-recruit-rankings-2010-2020/recruit-list/ recruit-lists --recursive
python3 -m venv env
source env/bin/activate
sudo pip3 install -r requirements.txt
```

Note that since S3 bucket names are globally unique, this will need to be changed for any other bucket. An IAM role with access to the target bucket must be attached to the EC2 instances as well.

## Stage Three: Cleanup, Normalization, and Optimization
After the first two stages, there are three output directories containing data:

`/recruit-lists` now contains one file per year containing all recruits from that year.

`/recruit-ranking-histories` now contains subdirectories for each year storing an individual JSON file per recruit capturing ranking changes.

`/recruit-timeline-histories` now contains subdirectories for each year storing an individual JSON file per recruit capturing events like official visits.

There are also several utility scripts to apply additional transformations. The first of these is `merge_utility.py` which merges all recruit files in each of the top-level year directories into a single file. This can be easier to manage than handling the thousands of files generated by stages one and two depending on the use case. Specifically, it is more performant for Athena which prefers larger files (~100MBs is the sweet spot according to the AWS documentation) as opposed to a higher volume of files. To run, use the command `python merge_utility.py <PATH_TO_DIRECTORY_WITH_FILES_TO_MERGE> <PATH_TO_OUTPUT_FILE>`.

Numerous duplicate recruits exist after producing the recruit lists in stage one, so `duplicate_utility.py` can be run to clean a stage one output file in place: `python duplicate_utility.py <PATH_TO_RECRUIT_LIST_FILE>`.

Both the recruiting history and event timeline scraping produced numerous duplicates. These data structure don't have a unique identifier (i.e. `247_id`). `duplicate_composite_utility.py` creates a composite key by concatenating all fields together to detect duplicates and deletes accordingly. To run, use the command `python duplicate_composite_utility.py <PATH_TO_FILE_WITH_COMPOSITE_KEY>`.

## Configuring AWS Athena
For this project, Athena is cheaper and simpler to stand up than a dedicated, relational database that would require additional ETL jobs or scripts to migrate from the JSON source files to tables. Athena uses serverless compute to query these raw files directly from S3 with ANSI SQL. After Athena and the Glue Data Catalog have been configured, SQL queries can be run against the datasets in-place. For example, this query computes when commits from the 2020 class were extended offers by the University of Texas at Austin:
```sql
select recruit.full_name, timeline.event_type, timeline.event_date, timeline.event_description
from timeline_events timeline
join recruit_list recruit on  recruit."247_id" = timeline."247_id"
where timeline.event_type = 'Offer' and timeline.event_description like '%Texas Longhorns%' and recruit.year = 2020
order by event_date desc
```
