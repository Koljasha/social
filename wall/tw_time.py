from time import strptime, mktime
from datetime import datetime

# получет время как строку в формате Twitter
# возвращает кортеж (unix, string)

def time_twitter(data):

    time_ = data.split(" ")
    time_time = time_[3].split(':')

    time_all = "{} {} {} {}:{}:{}".format(time_[2], time_[1], time_[-1], time_time[0], time_time[1], time_time[2])

    time_obj = strptime(time_all, "%d %b %Y %H:%M:%S")
    
    #приводим к нашему часовому поясу
    time_unix = int(mktime(time_obj)) + 60*60*3
    
    time_string = datetime.fromtimestamp(time_unix).strftime("%H:%M:%S %d %b %Y")

    return (time_unix, time_string)


