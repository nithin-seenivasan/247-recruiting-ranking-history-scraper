import os
import sys
from scrape_recruit_history import *
from file_utility import *

def create_output_directory(path):
    try:
        os.mkdir(path)
    except:
        emoji.emojize(f':warning: Directory at {path} already exists', use_aliases=True)

year = sys.argv[1]
recruit_list_file_path = sys.argv[2]
recruit_ranking_history_output_directory_base = './recruit-ranking-histories'
recruit_timeline_output_directory_base = './recruit-timeline-histories'
create_output_directory(recruit_ranking_history_output_directory_base)
create_output_directory(recruit_timeline_output_directory_base)
create_output_directory(f'{recruit_ranking_history_output_directory_base}/{year}')
create_output_directory(f'{recruit_timeline_output_directory_base}/{year}')


with open(recruit_list_file_path, 'r') as recruit_list_file:
    for index, line in enumerate(recruit_list_file):
        recruit = json.loads(line)
        try:
            ranking_history_url = get_ranking_history_url(recruit['247_url'], recruit['full_name'])
            if ranking_history_url is not None:
                ranking_history = get_recruiting_ranking_history(recruit['247_id'], ranking_history_url,
                                                                 recruit['full_name'])
            else:
                print(emoji.emojize(f':warning: No ranking history URL found for {recruit["full_name"]}',
                                    use_aliases=True))
                ranking_history = []
            ranking_history_file_name = f'{recruit_ranking_history_output_directory_base}/{year}/{recruit["247_id"]}.json'
            write_to_file_for_s3_athena(index, ranking_history, ranking_history_file_name)
        except Exception as exception:
            print(emoji.emojize(f':thumbsdown: Error processing ranking history for recruit {recruit["full_name"]}', use_aliases=True))
            print(emoji.emojize(f':x: {exception}', use_aliases=True))
        try:
            timeline_events = get_recruiting_timeline(recruit['247_id'], recruit['247_url'], recruit['full_name'])
            timeline_events_file_name = f'{recruit_timeline_output_directory_base}/{year}/{recruit["247_id"]}.json'
            write_to_file_for_s3_athena(index, timeline_events, timeline_events_file_name)
        except Exception as exception:
            print(emoji.emojize(f':thumbsdown: Error processing timeline events for recruit {recruit["full_name"]}', use_aliases=True))
            print(emoji.emojize(f':x: {exception}', use_aliases=True))
