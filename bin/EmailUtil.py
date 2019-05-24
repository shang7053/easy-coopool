# email发送工具
import smtplib, sys, importlib, logging, traceback
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import Header
from conf.config import *

# 设置默认字符集为UTF8 不然有些时候转码会出问题
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    importlib.reload(sys)
    sys.setdefaultencoding(default_encoding)


def send_mail(to_addr, title, msg):
    """
    发送邮件的相关信息，根据你实际情况填写
    :param to_addr: 收件人，多个以逗号分隔
    :param title: 邮件标题
    :param msg: 邮件内容
    :return:
    """
    # 初始化邮件
    encoding = 'utf-8'
    mail = MIMEText(msg.encode(encoding), 'plain', encoding)
    mail['Subject'] = Header(title, encoding)
    mail['From'] = EMAIL_ACCOUT
    mail['To'] = to_addr
    mail['Date'] = formatdate()
    try:
        sm_tp = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        sm_tp.set_debuglevel(True)
        sm_tp.ehlo()
        sm_tp.starttls()
        sm_tp.ehlo()
        sm_tp.login(EMAIL_ACCOUT, EMAIL_PWD)
        # 发送邮件
        sm_tp.sendmail(EMAIL_ACCOUT, to_addr.split(","), mail.as_string())
    except Exception as e:
        logging.error(traceback.format_exc(e))
    else:
        logging.debug("邮件发送成功")
    finally:
        sm_tp.close()


if __name__ == "__main__":
    send_mail("chengcai.shang@cmgplex.com,jiafa.dong@cmgplex.com", "【SmartJob招聘系统-Cookie池告警】",
              "网站hyperloop，可以cookie只剩3个了，快去补充点吧")
