import requests
from datetime import datetime

from .config import access_token_VK
from .retext import re_all

def vk(time_now, time_old):
    # запрос
    url = 'https://api.vk.com/method/newsfeed.get'
    params = {
        "v" : "5.131",
        "access_token" : access_token_VK,
        "filters" : "post",
        "end_time" : time_now,
        "start_time" : time_old,
        'count' : 100
    }
    
    res = requests.get(url, params=params).json()

    ####################################
    # print(requests.get(url, params=params).url)
    ####################################
    
    # import os
    # if os.path.exists('vk.json'):
    #     os.remove('vk.json')

    # import json
    # with open('vk.json', 'a', encoding="utf-8") as file:
    #     json.dump(res, file, indent=2, ensure_ascii=False)
   
    ####################################
    
    # Ошибки запроса
    if res.get('error'):
        err = "VK: {} - {}".format(res['error']['error_code'], res['error']['error_msg'])
        print(err)
        return {"error" : err} 
    
    res = res.get('response')

    # список для возвращения
    data = []

    if len(res.get('items')) == 0:
        return data

    # основной цикл
    for r in res.get('items'):
        # если реклама - пропускаем
        if r.get('marked_as_ads') == 1:
            continue

        unix_time = r.get('date')
        string_time = datetime.fromtimestamp(unix_time).strftime("%H:%M:%S %d %b %Y")

        id_ = r.get('post_id')
        
        # Данные о группе(пользователе)
        source_id = r.get('source_id')
        if source_id < 0 :
            for i in res.get('groups'):
                if i.get('id') == -source_id:
                    user_name = i.get('name')
                    user_name_page = i.get('screen_name')
                    user_image = i.get('photo_50')
                    break
        else:
            for i in res.get('profiles'):
                if i.get('id') == source_id:
                    user_name = "{} {}".format(i.get('first_name'), i.get('last_name'))
                    user_name_page = i.get('screen_name')
                    user_image = i.get('photo_50')
                    break
        
        link = "https://vk.com/{}?w=wall{}_{}".format(user_name_page, source_id, id_)

        text = r.get('text')
        image = None

        ##### вспомогательные функции

        # выбираем максимальное изображение с шириной меньше 700
        def return_image(sizes):
            sizes.sort(key= lambda i: i.get('width'), reverse=True)
            for i in sizes:
                if i.get('width') < 750:
                    return i.get('url')
        
        # attachments - изображение и т.д. - как функция
        def attachments(r_):
            nonlocal image, text
            # тип - 'photo'
            if r_.get('type') == "photo":
                img_sizes = r_.get('photo').get('sizes')
                image = return_image(img_sizes)
            # тип - 'video'
            elif r_.get('type') == "video":
                # ver api <=100
                # i_video = r_.get('video')
                # if i_video.get('photo_800') is not None:
                    # image = i_video.get('photo_800')
                # elif i_video.get('photo_640') is not None:
                    # image = i_video.get('photo_640')
                # else:
                    # image = i_video.get('photo_320')

                # ver api 101=>
                image = r_.get('video').get('image')[-1].get('url')
            # тип - 'link'
            elif r_.get('type') == "link":
                if r_.get('link').get('photo') is not None:
                    img_sizes = r_.get('link').get('photo').get('sizes')
                    image = return_image(img_sizes)
                    text = "{}\n{}".format(text, r_.get('link').get('title'))
            # тип - 'doc'
            elif r_.get('type') == "doc":
                if r_.get('doc').get('preview') is not None:
                    sizes = r_.get('doc').get('preview').get('photo').get('sizes')
                    # аналог return_image, но возвращает 'src' вместо 'url'
                    sizes.sort(key= lambda i: i.get('width'), reverse=True)
                    for i in sizes:
                        if i.get('width') < 750:
                            image = i.get('src')
                            break
                    
        #####

        # проверка attachments
        if r.get('attachments') is not None:
            for attach in r.get('attachments'):
                attachments(attach)
                if image is not None:
                    break

        # проверка на репост
        if r.get('copy_history') is not None:
            copy_history = r.get('copy_history')[0]
            # текст
            text = copy_history.get('text')
            # attachments
            if copy_history.get('attachments') is not None:
                for attach in copy_history.get('attachments'):
                    attachments(attach)
                    if image is not None:
                        break
            # имя + имя репоста
            owner_id = copy_history.get('owner_id')
            if owner_id < 0 :
                for i in res.get('groups'):
                    if i.get('id') == -owner_id:
                        owner_name = i.get('name')
                        break
            else:
                for i in res.get('profiles'):
                    if i.get('id') == owner_id:
                        owner_name = "{} {}".format(i.get('first_name'), i.get('last_name'))
                        break            
            user_name = "{} __репост__ {}".format(user_name, owner_name)

        # регулярные для текста
        text = re_all(text)

        obj = {
            'unix_time' : unix_time,
            'string_time' : string_time,
            'type' : "/static/vk.png",
            'id' : id_,
            'user_name' : user_name,
            'user_image' : user_image,
            'link' : link,
            'text' : text,
            'image' : image,
            'embedded' : None
        }

        data.append(obj)

    return data
