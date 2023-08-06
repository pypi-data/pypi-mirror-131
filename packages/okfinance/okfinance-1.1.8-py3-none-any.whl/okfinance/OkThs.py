import execjs


# 获取同花顺cookie
def get_cookie():
    with open('./ths.min.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cookie = 'v=' + ctx.call("v") + ';'
    print(cookie)
    return cookie


# 获取同花顺cookie
def get_cookie1():
    with open('../ths.min.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cookie = 'v=' + ctx.call("v") + ';'
    print(cookie)
    return cookie


# 获取同花顺cookie
def get_cookie2():
    with open('./js/ths.min.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cookie = 'v=' + ctx.call("v") + ';'
    print(cookie)
    return cookie


# 获取同花顺cookie
def get_cookie3():
    with open('../js/ths.min.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cookie = 'v=' + ctx.call("v") + ';'
    print(cookie)
    return cookie


# 获取同花顺cookie
def get_cookie4():
    with open('./okfinance/js/ths.min.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cookie = 'v=' + ctx.call("v") + ';'
    print(cookie)
    return cookie


get_cookie()
