import pandas as pd

df_raw = pd.read_excel('C:\\Users\\user\\PycharmProjects\\DE2021\\Practice\\[백신]유튜브 댓글 크롤링 url.xlsx')

import os
import pandas as pd
import json
from pandas import json_normalize
import googleapiclient.discovery
import re

df = pd.DataFrame(columns=['channel', 'url', 'title', 'date', 'command'])

def main():
    for j in range(len(df_raw)):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyDkhpDP9jaSlyCYSk3c-hGlYXQiY311LOA"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=200,
            videoId=df_raw['videoId'][j]
        )

        response = request.execute()

        for i in range(len(response["items"])):
            if i > 100:
                break
            json_data = response["items"][i]["snippet"]["topLevelComment"]['snippet']
            df.loc[len(df) + i] = [df_raw['channel'][j], "https://www.youtube.com/watch?v=" + json_data['videoId'],
                                   df_raw['title'][j], df_raw['date'][j], json_data['textDisplay'], ]


if __name__ == "__main__":
    main()

print(df)

# 인덱스 정렬
df=df.reset_index()

# index column 삭제
del df['index']

### 데이터 정제 ### 
# 이모티콘
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"  # dingbats
                           u"\u3030"
                           u"\U00010000-\U0010ffff""]+", flags=re.UNICODE)

# html 태그
cleanr1 = re.compile('</?br/?>')
cleanr2 = re.compile('/?&quot/?')
cleanr3 = re.compile('/?&lt/?')
cleanr4 = re.compile('</?a href.*/?>')
cleanr5 = re.compile('/?&gt/?')
cleanr6 = re.compile('</?i/?>')
cleanr7 = re.compile('/?j&amp;j/?')
cleanr8 = re.compile('/?&#39;/?')

comment_result = []

# 이모티콘, html 태그 삭제
for i in range(len(df)):
    tokens = re.sub(emoji_pattern, "", df['command'].iloc[i])
    tokens = re.sub(cleanr1, "", tokens)
    tokens = re.sub(cleanr2, "", tokens)
    tokens = re.sub(cleanr3, "", tokens)
    tokens = re.sub(cleanr4, "", tokens)
    tokens = re.sub(cleanr5, "", tokens)
    tokens = re.sub(cleanr6, "", tokens)
    tokens = re.sub(cleanr7, "", tokens)
    tokens = re.sub(cleanr8, "", tokens)

    comment_result.append(tokens)

# 정제된 댓글 데이터 프레임 생성
comment_result = pd.DataFrame(comment_result, columns=["command"])
df['new_command'] = comment_result

# 엑셀로 저장
df.to_excel('최종_유튜브.xlsx')