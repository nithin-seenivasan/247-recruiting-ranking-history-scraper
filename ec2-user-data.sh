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
python3 process_recruits.py ./recruit-lists/recruit-list-2020.json
