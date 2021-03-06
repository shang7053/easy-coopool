# 配置类
# -----------------------redis-----------------------
# Redis数据库地址
REDIS_HOST = '192.168.1.97'
# Redis端口
REDIS_PORT = 6379
# Redis密码，如无填None
REDIS_PASSWORD = None
# -----------------------end-----------------------
# -----------------------timer-----------------------
# 验证器循环周期,单位秒
CYCLE = 10 * 60
# -----------------------end-----------------------
# -----------------------server-----------------------
# sever地址和端口
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8090
# -----------------------end-----------------------
# -----------------------email-----------------------
# 服务器
EMAIL_SERVER = "mail.cmgplex.com"
#  端口
EMAIL_PORT = 587
# 用户名
EMAIL_ACCOUT = "smartjob@cmgplex.com"
# 密码
EMAIL_PWD = "Lumiai!@#"
# -----------------------end-----------------------
# -----------------------alert-----------------------
# cookie告警阈值
COOKIE_ALERM_SIZE = 1
# cookie告警文本
COOKIE_ALERM_TEXT = "您好，渠道KEY={}，当前可用cookie只剩{}个了，为避免系统爬取时无cookie可用请尽快补充，谢谢。"
# cookie告警恢复文本
COOKIE_HEALTH_TEXT = "您好，渠道KEY={}，cookie可用个数已恢复正常，当前可用cookie{}个。"
# cookie告警静默时间，即发送一次告警后间隔多久再发下一次，单位秒
COOKIE_ALERM_QUIET_TIME = 4 * 60 * 60
# -----------------------end-----------------------
# -----------------------log-----------------------
# 是否启用文件日志
FILE_ENABLE = True
# 是否启用控制台日志
CONSOLE_ENABLE = True
