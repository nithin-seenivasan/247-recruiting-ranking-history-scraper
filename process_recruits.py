import sys
import json
from scrape_recruit_history import *
import emoji

recruit_list_file_path = sys.argv[1]
if len(sys.argv) > 2:
    recruit_ranking_history_output_directory_base = sys.argv[2]
    recruit_timeline_output_directory_base = sys.argv[3]
else:
    recruit_ranking_history_output_directory_base = './recruit-ranking-histories'
    recruit_timeline_output_directory_base = './recruit-timeline-histories'


with open(recruit_list_file_path, 'r') as recruit_list_file:
    for count, line in enumerate(recruit_list_file):
        recruit = json.loads(line)
        ranking_history_url = get_ranking_history_url(recruit['247_url'], recruit['full_name'])
        ranking_history = get_recruiting_ranking_history(recruit['247_id'], ranking_history_url)
        timeline_events = get_recruiting_timeline(recruit['247_id'], recruit['247_url'], recruit['full_name'])
        ranking_history_file_name = f'{recruit_ranking_history_output_directory_base}/{recruit["247_id"]}.json'
        with open(ranking_history_file_name, 'a') as ranking_history_file:
            for event in ranking_history:
                json.dump(event, ranking_history_file)
                ranking_history_file.write('\n')
        print(emoji.emojize(f':file_folder: Wrote {recruit_list_file_path} recruits to {ranking_history_file_name}', use_aliases=True))
        timeline_events_file_name = f'{recruit_timeline_output_directory_base}/{recruit["247_id"]}.json'
        with open(timeline_events_file_name, 'a') as timeline_events_file:
            for event in timeline_events:
                json.dump(event, timeline_events_file)
                timeline_events_file.write('\n')
        print(emoji.emojize(f':file_folder: Wrote {recruit_list_file_path} recruits to {timeline_events_file_name}', use_aliases=True))

