import requests
from requests_oauthlib import OAuth1

from .config import consumer_key_TW, consumer_secret_TW, access_token_TW, access_token_secret_TW
from .tw_time import time_twitter
from .retext import re_all

def twitter(max_id=None, count=5):
    
    auth = OAuth1(consumer_key_TW, consumer_secret_TW, access_token_TW, access_token_secret_TW)  
    url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
    
    # запрос
    if max_id is not None:
        count += 1
    
    params = {
        "tweet_mode" : "extended",
        "max_id" : max_id,
        "count" : count
    }

    #######
    # from time import time
    # time_start = time()
    #######

    res = requests.get(url, params=params, auth=auth).json()

    #######  
    # print("Twitter respons: {}".format(time()-time_start))
    #######

    #####################################
    
    # import os
    # if os.path.exists('twitter.json'):
    #     os.remove('twitter.json')

    # import json
    # with open('twitter.json', 'a', encoding="utf-8") as file:
    #     json.dump(res, file, indent=2, ensure_ascii=False)
   
    #####################################

    # Ошибки запроса
    if isinstance(res, dict):
        err = "Twitter: {} - {}".format(res.get('errors')[0]['code'], res.get('errors')[0]['message'])
        print(err)
        return {"error" : err}

    # список для возвращения
    data = []

    if max_id is not None:
        res = res [1:]

    # основной цикл
    for r in res:
        time_ = time_twitter(r.get('created_at'))

        if r.get('entities').get('media') is not None:
            image = r.get('entities').get('media')[0].get('media_url')
        else:
            image = None

        id_ = r.get('id_str')
        user_name_page = r.get('user').get('screen_name')
        link = "https://twitter.com/{}/status/{}".format(user_name_page, id_)

        # если нет картинки, идем через api встраиваивания
        embedded = None
        if image is None:
            text = None
            embedded = ' '
        else:
            text = re_all(r.get('full_text'))
        
        obj = {
            'unix_time' : time_[0],
            'string_time' : time_[1],
            'type' : "/static/twitter.png",
            'id' : id_,
            'user_name' : r.get('user').get('name'),
            'user_image' : r.get('user').get('profile_image_url'),
            'link' : link,
            'text' : text,
            'image' : image,
            'embedded' : embedded
        }

        data.append(obj)

    return data


