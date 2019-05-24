# 程序主入口文件
import logging, logging.handlers, traceback
from bin.Scheduler import Scheduler
from conf.config import *
from bin.Scheduler import Process
from bin.CookieRC import app


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


# 初始化日志
init_log()
# 启动验证器
valid_process = Process(target=Scheduler.valid_cookie)
valid_process.start()


def main():
    """
    程序主入口方法
    :return:
    """
    try:
        # 启动服务器
        logging.info('API接口开始运行')
        app.run(host=SERVER_HOST, port=SERVER_PORT)
    except Exception as e:
        logging.error(traceback.format_exc(e))


if __name__ == '__main__':
    main()
