# 程序主入口文件
import logging, logging.handlers
from bin.Scheduler import Scheduler
from conf.config import *
from bin.Scheduler import Process


def init_log():
    '''
    初始化日志
    :return:
    '''
    log_format = logging.Formatter(
        "%(asctime)s [%(process)d-%(threadName)s] [%(filename)s--%(lineno)s] [%(levelname)s] - %(message)s")
    hanlders = []
    if FILE_ENABLE:
        # 初始化文件日志handler
        log_file = "logs/cookiepool.log"
        file_handler = logging.handlers.TimedRotatingFileHandler(filename=log_file, encoding="utf-8", backupCount=7,
                                                                 when="D",
                                                                 interval=1)
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        hanlders.append(file_handler)
    if CONSOLE_ENABLE:
        # 控制台日志
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(log_format)
        hanlders.append(sh)
    # 配置logging
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format, handlers=hanlders)


def main(env, start_response):
    """
    程序主入口方法
    :param env:
    :param start_response:
    :return:
    """
    # 初始化日志
    init_log()
    # 判断是否启动web服务
    server_process = Process(target=Scheduler.start_server)
    server_process.start()
    # 判断是否启动验证器
    valid_process = Process(target=Scheduler.valid_cookie)
    valid_process.start()


if __name__ == '__main__':
    main(None,None)
