# cookie验证器
import json, requests, traceback
from requests.exceptions import ConnectionError
from bin.RedisDao import *
from bin.IValidTester import IValidator


class BaseValidator(IValidator):
    def __init__(self, website='weibo', validate_url="default", alert_email="default"):
        """
        初始化，直接调用基类的初始化方法进行初始化
        :param website: 站点
        :param validate_url: 验证url
        :param alert_email: 告警邮件收件人
        """
        IValidator.__init__(self, website, validate_url, alert_email)

    def test(self, key, cookies):
        """
        基类抽象方法的实现
        :param key: 哈希表的key
        :param cookies: key对应的cookie
        :return:
        """
        logging.info('正在测试Cookies,key={}'.format(key))
        try:
            cookies = json.loads(cookies)
        except TypeError:
            self.cookies_db.delete(key)
            logging.error('Cookies不合法，key={}，现已删除!'.format(key))
            return
        try:
            response = requests.get(self.validate_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                logging.info('Cookies有效')
            else:
                self.cookies_db.delete(key)
                logging.info(
                    "Cookies已失效，现已删除!response.status_code={},headers={}".format(response.status_code, response.headers))
        except ConnectionError as e:
            logging.error(traceback.format_exc(e))


if __name__ == '__main__':
    BaseValidator().run()
