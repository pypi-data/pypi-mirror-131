from urllib import request

import execjs


# 获取同花顺cookie
def get_cookie(url):
    """
    获取同花顺cookie
    :param url:
    :return:
    """
    page = request.urlopen(url)
    js = page.read().decode('utf-8')
    ctx = execjs.compile(js)
    cookie = 'v=' + ctx.call("v") + ';'
    print(cookie)
    return cookie

