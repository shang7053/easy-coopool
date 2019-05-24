# redis操作类
import random
import redis
from conf.config import *
import logging


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取Hash的名称
        :return: Hash名称
        """
        hash_name = "{type}:{website}".format(type=self.type, website=self.website)
        logging.info("redis hash_name={}".format(hash_name))
        return hash_name

    def set(self, key, value):
        """
        （哈希表操作）设置键值对（自动填充哈希表表名）
        :param key: key
        :param value: value
        :return:
        """
        logging.debug("set,key={},value={}".format(key, value))
        return self.db.hset(self.name(), key, value)

    def setWithExpire(self, key, value, expire):
        """
        （普通操作）设置键值对并设置过期时间，单位秒
        :param key: key
        :param value: value
        :param expire: expire过期时间，单位秒
        :return:
        """
        logging.debug("set,key={},value={}".format(key, value))
        ret = self.db.set(key, value)
        self.db.expire(key, expire)
        return ret

    def get(self, key):
        """
        （哈希表操作）根据键名获取键值（自动填充哈希表表名）
        :param key: key
        :return:
        """
        logging.debug("get,key={}".format(key))
        return self.db.hget(self.name(), key)

    def get_by_key(self, key):
        """
        （普通操作）根据键名获取键值
        :param key: key
        :return:
        """
        logging.debug("get_by_key,key={}".format(key))
        return self.db.get(key)

    def delete(self, key):
        """
        （哈希表操作）根据键名删除键值对（自动填充哈希表表名）
        :param key: key
        :return: 删除结果
        """
        logging.debug("delete,key={}".format(key))
        return self.db.hdel(self.name(), key)

    def count(self):
        """
        （哈希表操作）获取指定hash表名下所有key的数目（自动填充哈希表表名）
        :return: 数目
        """
        logging.debug("count")
        return self.db.hlen(self.name())

    def countbyname(self, name):
        """
        获取数目
        :return: 数目
        """
        logging.debug("countbyname,name={}".format(name))
        return self.db.hlen(name)

    def random(self):
        """
        （哈希表操作）随机得到键值，用于随机Cookies获取（自动填充哈希表表名）
        :return: 随机Cookies
        """
        logging.debug("random")
        values = self.db.hvals(self.name())
        if len(values) > 0:
            return random.choice(values);
        else:
            return "{}"

    def hkeys(self):
        """
        （哈希表操作）获取指定hash表名下所有key（自动填充哈希表表名）
        :return: 所有key
        """
        logging.debug("hkeys")
        return self.db.hkeys(self.name())

    def hkeys_by_name(self, name):
        """
        （哈希表操作）获取所有账户信息（手动填充哈希表表名）
        :param name: name
        :return: 所有key
        """
        logging.debug("hkeys_by_name,name={}".format(name))
        return self.db.hkeys(name)

    def all(self):
        """
        （哈希表操作）获取所有键值对（自动填充哈希表表名）
        :return: key和密码或Cookies的映射表
        """
        logging.debug("all")
        return self.db.hgetall(self.name())

    def scan_iter(self, match_str):
        """
        （哈希表操作）获取所有匹配的key
        :param match_str: 匹配字符串
        :return: 匹配的key
        """
        logging.debug("scan_iter,match_str={}".format(match_str))
        return self.db.scan_iter(match_str)

    def hget(self, name, key):
        """
        （哈希表操作）根据key和name获取value（手动填充哈希表表名）
        :return: key和密码或Cookies的映射表
        """
        logging.debug("hget,name={},key={}".format(name, key))
        return self.db.hget(name, key)


if __name__ == '__main__':
    conn = RedisClient('accounts', '')
    # result = conn.set('hell2o', 'sss3s')
    # logging.info(result)
    for item in conn.all():
        logging.info(item)
    for item in conn.scan_iter("cookies*"):
        logging.info(item)
        logging.info(str(item).split(":")[0])
        logging.info(str(item).split(":")[1])
        for hkey in conn.hkeysbykey(item):
            logging.info(hkey)
            logging.info(conn.hget(item, hkey))
