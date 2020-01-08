import pandas as pd
from News import News
from News import newsList


def readFile(path):
    counter = 0
    range = 100000000     # maximum number of news
    offset = 0   # minimum number of news

    if path.endswith('csv'):
        dfs = pd.read_csv(path)
        dfs.to_excel(path[:-3] + 'xlsx', index=None, header=True)

    dfs = pd.read_excel(path, sheet_name=None)

    for key, value in dfs.items():
        for index, row in value.iterrows():
            if counter < offset:
                counter += 1
                continue
            newsList.append(News(row['publish_date'],
                                 row['title'],
                                 row['url'],
                                 row['summary'],
                                 row['meta_tags'],
                                 row['content'],
                                 row['thumbnail']))
            counter += 1
            if counter == range + offset:
                break
