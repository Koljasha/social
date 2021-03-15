import re

# преобразуем ***... в *******
def re_stars(str_):
    return re.sub(r"\*{5,}","*******", str_)

# преобразуем \n в тег
def re_br(str_):
    return re.sub(r"\n", " <br>", str_)

# преобразуем vk.cc в ссылку
def re_vkcc(str_):
    return re.sub(r"vk.cc", "https://vk.cc", str_)

# преобразуем ссылки
def re_http(str_):
    # выбор http httpd
    match = re.search(r'(https://)|(http://)', str_, re.IGNORECASE)
    if match is None:
        return str_

    s_start = str_[0:match.span()[0]]
    s_http = str_[match.span()[0]:]

    # проверяем строку с http на пробел
    match = re.search(r'\s', s_http)
    if match is None:
        return "{}<a href=\"{}\" target=\"_blank\">link..</a>".format(s_start, s_http)
    s_http_ = s_http[0:match.span()[0]]
    s_end = s_http[match.span()[0]:]
    s_end = re_http(s_end)
    return "{} <a href=\"{}\" target=\"_blank\">link..</a> {}".format(s_start, s_http_, s_end)

# общая на регулярки
def re_all(str_):
    return re_http(re_vkcc(re_br(re_stars(str_))))
