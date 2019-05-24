# cookie验证器基类
from bin.RedisDao import *
from abc import abstractmethod


class IValidator(object):
    def __init__(self, website='default', validate_url="default", alert_email="default"):
        """
        初始化
        :param website: 站点
        :param validate_url: cookie验证url
        :param alert_email: 告警邮件收件人
        """
        self.website = website
        self.validate_url = validate_url
        self.alert_email = alert_email
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    @abstractmethod
    def test(self, key, cookies):
        """
        抽象方法需要子类实现
        :param key: 哈希表的key
        :param cookies: key对应的cookie
        :return:
        """
        logging.error("IValidTester不能实例化")
        raise NotImplementedError

    def run(self):
        """
        入口方法
        :return:
        """
        # 获取哈希表中的全部数据
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)