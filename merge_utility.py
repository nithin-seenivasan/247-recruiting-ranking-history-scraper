import os

def merge_timeline_history():
    for root, dirs, files in os.walk('./recruit-timeline-histories/', onerror=None):
        for file in files:
            path = os.path.join(root, file)
            f = open(path)
            f2 = open("merged-timelines.json", "a")
            for line in f.readlines():
                f2.write(line)

def merge_ranking_history():
    for root, dirs, files in os.walk('./recruit-ranking-histories/', onerror=None):
        for file in files:
            path = os.path.join(root, file)
            f = open(path)
            f2 = open("merged-rankings.json", "a")
            for line in f.readlines():
                f2.write(line)

def merge_recruit_list():
    for root, dirs, files in os.walk('./recruit-lists/', onerror=None):
        for file in files:
            path = os.path.join(root, file)
            f = open(path)
            f2 = open("merged-recruits.json", "a")
            for line in f.readlines():
                f2.write(line)