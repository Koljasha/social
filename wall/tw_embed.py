import requests

def twitter_embedded(link):
    url_oembed = 'https://publish.twitter.com/oembed'
    params_oembed = {
        'url' : link,
        'hide_thread' : True,
        'hide_media' : False,
        'theme' : 'dark',
        'omit_script' : True
    }
    return requests.get(url_oembed, params=params_oembed).json()
