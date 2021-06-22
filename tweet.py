import os
from requests_oauthlib import OAuth1Session
import json
import csv
# import pandas as pd
# import numexpr as ne
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pprint


###########  Access Token情報  ###############

KEYS = {
  'consumer_key': 'dR5EaSxLoR5XQgmri2gviAPgJ',
  'consumer_secret': 'dKWkSg5Tf2CJ7fZA3MDPD0xjqVAJosOSGkUOuzfnt8lmmUKAEM',
  'access_token': '723828477556719616-arSpnl9vnnMuOmYOc1M8sxUkTIyRoCJ',
  'access_secret': 'tzFfdhwLMb9gvAddVaTXy2xBAK3nIby5bAd57EgfVnWGH',
}


#################  Twitter  ###################

twitter = OAuth1Session(KEYS['consumer_key'],KEYS['consumer_secret'],KEYS['access_token'],KEYS['access_secret'])


##############  Tweetを取得する  ################

def getTwitterData(key_word, repeat):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params ={'q': key_word, 'count':'100','lang':'ja', 'result_type':'recent'}
    tweets = []
    mid = -1
    break_flag = 0
    
    for i in range(repeat):
        params['max_id'] = mid
        res = twitter.get(url, params = params)
        if res.status_code == 200:
            sub_tweets = json.loads(res.text)['statuses']
            limit = res.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in res.headers else 0
            print("API残接続可能回数：%s" % len(limit))     
            tweet_ids = []
            for tweet in sub_tweets:
                tweet_ids.append(int(tweet['id']))
                tweets.append(tweet)
            if len(tweet_ids) > 0:
                min_tweet_id = min(tweet_ids)
                mid = min_tweet_id - 1
            else:
                break_flag = 1
                break
                
            ## 終了判定
            if break_flag == 1:
                break
                
        else:
            print("Failed: %d" % res.status_code)
            break_flag = 1
    
    print("ツイート取得数：%s" % len(tweets))
        
    return tweets

tweets = getTwitterData("コロナウイルス", 180)
user_info = []
for tweet in range(0, len(tweets)):
  user_info.append(tweets[tweet]['user'])

with open('./covidnineteen_writer.csv', 'w') as f:
  csv_column = [
  'created_at', 'default_profile', 'default_profile_image', 'description', 'favourites_count', 'follow_request_sent',
  'followers_count', 'friends_count', 'has_extended_profile', 'id_str', 'is_translator', 'listed_count',
  'location', 'name', 'profile_background_color', 'profile_background_image_url_https', 'profile_image_url_https', 'profile_sidebar_fill_color',
  'profile_use_background_image', 'protected', 'statuses_count', 'url', 'verified'
]
  writer = csv.DictWriter(f, csv_column, extrasaction='ignore')
  writer.writeheader()
  writer.writerows(user_info)
