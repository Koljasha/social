from time import time
from threading import Thread
import json
import os
from time import time

from .twitter import twitter
from .vk import vk

class Wall:
    # сколько возвращаем и создаем
    count_return=5
    # VK возвращает максимум 100 записей
    count_create=20

    # переменные
    def __init__(self, log=False):
        self.data = []
        self.error = None
        self.last_twit_id = None
        self.last_vk_time = None
        self.last_index = None
        self.log = log
        # проверка на  существование файла log
        if log and os.path.exists('log.json'):
            os.remove('log.json')

        # для ускорения Twitter
        self.first() 
    
    # заполнение в первый рез
    def first(self):
        # twitter

        # проверка времени запроса twitter
        # if self.log:
        #     time_start = time()
        
        tw_ = twitter(count=Wall.count_create)
        # проверка на ошибки
        if isinstance(tw_, dict):
            self.error = tw_
            return
        self.data.extend(tw_)
        self.last_twit_id = self.data[-1].get('id')
        
        # проверка времени запроса twitter
        # if self.log:
        #     print("Twitter: {}".format(time()-time_start))
        
        #vk

        # проверка времени запроса VK
        # if self.log:
        #     time_start = time()

        last_twit_time = self.data[-1].get('unix_time')

        vk_ = vk(time(), last_twit_time)
        # проверка на ошибки
        if isinstance(vk_, dict):
            self.error = vk_
            return
        self.data.extend(vk_)
        self.last_vk_time = self.data[-1].get('unix_time')

        # проверка времени запроса VK
        # if self.log:
        #     print("VK: {}".format(time()-time_start))
        
        #sort
        self.data.sort(key= lambda i: i.get('unix_time'), reverse=True)

    # заполнение в другие разы
    def next(self):
        temp_data = []

        # twitter
        tw_ = twitter(self.last_twit_id, count=Wall.count_create)
        # проверка на ошибки
        if isinstance(tw_, dict):
            self.error = tw_
            return
        temp_data.extend(tw_)
        self.last_twit_id = temp_data[-1].get('id') 

        #vk
        last_twit_time = temp_data[-1].get('unix_time')
        vk_ = vk(self.last_vk_time-1, last_twit_time)
        # проверка на ошибки
        if isinstance(vk_, dict):
            self.error = vk_
            return
        temp_data.extend(vk_)
        self.last_vk_time = temp_data[-1].get('unix_time')

        #sort
        temp_data.sort(key= lambda i: i.get('unix_time'), reverse=True)
        
        self.data.extend(temp_data)

    # обнуляет data
    def data_reset(self):
        self.data = []
        self.error = None
        self.last_index = 0

    # возвращаем записи - JSON
    def data_return(self):
        # если ошибка
        if self.error is not None:
            return self.error
        
        start = self.last_index
        end = self.last_index + Wall.count_return
        self.last_index = end

        # проксирование следующих элементов
        if self.last_index + 2*Wall.count_return >= len(self.data) :
            Thread(target=self.next).start()

        # логирование
        if self.log:
            print("Start: {} End: {} All: {}".format(start, end, len(self.data)))
            with open('log.json', 'a', encoding="utf-8") as file:
                json.dump(self.data[start:end], file, indent=2, ensure_ascii=False)
            
        return self.data[start:end]
