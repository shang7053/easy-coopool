# 调度类
import time
from multiprocessing import Process
from bin.BaseValidTester import *
from conf.config import *
from bin.EmailUtil import send_mail


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        """
        验证cookie
        :param cycle: 循环间隔，单位秒
        :return: 无返回值
        """
        while True:
            logging.info('Cookies检测进程开始运行')
            redis_conn = RedisClient('accounts', '')
            try:
                # 搜索库里所有accounts开头的哈希表表名
                for name in redis_conn.scan_iter("accounts*"):
                    website = str(name).split(":")[1]
                    validate_url = redis_conn.hget(name, "validate_url")
                    alert_email = redis_conn.hget(name, "alert_email")
                    logging.info("开始检查网站={}，website={},validate_url={}".format(name, website, validate_url))
                    tester = BaseValidator(website, validate_url, alert_email)
                    tester.run()
                    logging.info('Cookies检测完成')
                    del tester
                    cookie_size = redis_conn.countbyname("cookies:" + website)
                    logging.info("检测后可用cookie数量是{}个,当前设置告警阈值是{}".format(cookie_size, COOKIE_ALERM_SIZE))
                    # 验证cookie数量是否低于阈值
                    if cookie_size <= COOKIE_ALERM_SIZE:
                        # 低于阈值时先检测是否已发送告警，如果已发送并处于静默期则不发送，反之发送
                        if redis_conn.get_by_key("alert:{}".format(website)) is None:
                            logging.warning("开始推送邮件通知，收件人:{}".format(alert_email))
                            mail_process = Process(
                                target=Scheduler.send_alert_mail(alert_email, "【SmartJob招聘系统-Cookie池告警】",
                                                                 COOKIE_ALERM_TEXT.format(website,
                                                                                          cookie_size)))
                            redis_conn.setWithExpire("alert:{}".format(website), "1", COOKIE_ALERM_QUIET_TIME)
                            mail_process.start()
                        else:
                            logging.warning("当前处于静默期，不推送告警邮件！")
                    else:
                        # 当高于阈值时判断是否处于告警静默期，如果是，取消静默并发告警恢复邮件
                        if redis_conn.get_by_key("alert:{}".format(website)) is not None:
                            logging.info("告警恢复，开始清除静默标志，key={}".format("alert:{}".format(website)))
                            redis_conn.delete_key("alert:{}".format(website))
                            logging.warning("开始推送邮件通知，收件人:{}".format(alert_email))
                            mail_process = Process(
                                target=Scheduler.send_alert_mail(alert_email, "【SmartJob招聘系统-Cookie池告警恢复】",
                                                                 COOKIE_HEALTH_TEXT.format(website,
                                                                                           cookie_size)))
                            mail_process.start()
                logging.info("Cookies检测进程结束，距离下次运行还有{}秒".format(cycle))
                time.sleep(cycle)
            except Exception as e:
                logging.error(traceback.format_exc(e))

    @staticmethod
    def send_alert_mail(alert_email, title, msg):
        """
        发送邮件
        :param alert_email: 收件人，多个以逗号分隔
        :param title: 邮件标题
        :param msg: 邮件内容
        :return:
        """
        send_mail(alert_email, title, msg)
