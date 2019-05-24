# rest服务，提供新增账号、获取cookie的接口
import json, time, traceback
from flask import Flask, g, request
from bin.RedisDao import *

__all__ = ['app']

app = Flask("cookie_pool")


@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn(website, action_type):
    """
    根据website和action_type获取redis连接
    :return:
    """
    if not hasattr(g, website):
        setattr(g, website + '_' + action_type, eval('RedisClient' + '("' + action_type + '", "' + website + '")'))
    return g


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie, 访问地址如 /hyperloop/random
    :return: 随机Cookie
    """
    logging.info("进入random方法，website={}".format(website))
    try:
        g = get_conn(website, "cookies")
        cookies = getattr(g, website + '_cookies').random()
        return json.dumps({'status': '0', 'msg': '成功', 'data': json.loads(cookies)})
    except Exception as e:
        logging.error(traceback.format_exc(e))
        return json.dump({'status': '0', "msg": "程序异常"})


def converJsonStr(data: str):
    """
    将浏览器的cookie格式转化成json格式
    :param data: 浏览器的cookie
    :return: json转化后的json
    """
    ret = {}
    for coo in data.split(";"):
        key = coo.split("=")[0]
        value = coo.split("=")[1]
        ret[key] = value
    return json.dumps(ret)


@app.route('/<website>/add', methods=["POST"])
def add(website):
    """
    添加cookie, 访问地址如 /hyperloop/add
    :param website: 站点
    :param cookie: cookie
    :return:
    """
    json_data = request.json
    logging.info("进入add方法，website={},data={}".format(website, json_data))
    try:
        g = get_conn(website, "cookies")
        key = str(round(time.time() * 1000))
        cookie = converJsonStr(json_data["cookie"])
        getattr(g, website + '_cookies').set(key, cookie)
        return json.dumps({'status': '1', "msg": "成功"})
    except Exception as e:
        logging.error(traceback.format_exc(e))
        return json.dump({'status': '0', "msg": "程序异常"})


@app.route('/<website>/register', methods=["POST"])
def register(website):
    """
    注册站点
    :param website: 站点
    :param validate_url: 验证url
    :param alert_email: 告警收件人，多个以逗号分隔
    :return:
    """
    json_data = request.json
    logging.info("进入register方法，website={},data={}".format(website, json_data))
    try:
        g = get_conn(website, "accounts")
        validate_url = json_data["validate_url"]
        alert_email = json_data["alert_email"]
        getattr(g, website + '_accounts').set("validate_url", validate_url)
        getattr(g, website + '_accounts').set("alert_email", alert_email)
        return json.dumps({'status': '1', "msg": "成功"})
    except Exception as e:
        logging.error(traceback.format_exc(e))
        return json.dump({'status': '0', "msg": "程序异常"})


@app.route('/<website>/count')
def count(website):
    """
    获取当前站点可用Cookies总数
    """
    logging.info("进入count方法，website={}".format(website))
    try:
        g = get_conn(website, "cookies")
        cookie_count = getattr(g, website + '_cookies').count()
        return json.dumps({'status': '1', "msg": "成功", 'data': cookie_count})
    except Exception as e:
        logging.error(traceback.format_exc(e))
        return json.dump({'status': '0', "msg": "程序异常"})


if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT)
