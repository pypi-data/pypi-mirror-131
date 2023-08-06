import execjs


# 获取同花顺cookie
def get_cookie():
    with open('../js/aes.min.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cookie = 'v=' + ctx.call("v") + ';'
    print(cookie)
    return cookie
