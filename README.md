# easy-coopool 简单cookie池
## 源自于https://github.com/Python3WebSpider/CookiesPool
主要应对场景是cookie由另外独立机制单独生成，不需要自动生成的场景。<br>
相比于CookiesPool，主要区别如下：<br>
1、easy-coopool没有生成模块，需要调用API主动添加<br>
2、easy-coopool优化验证器代码，使其更易扩展<br>
3、easy-coopool增加cookie阈值告警，当可用数不足时告警<br>
4、easy-coopool优化日志输出，排错更容易<br>
5、easy-coopool简化配置，更易操作<br>
## 依赖环境如下

python>=3.0<br>
requests>=2.13.0<br>
redis>=2.10.5<br>
Flask>=0.12.1<br>

## 0环境初始化脚本
chmod +x install.sh<br>
sh install.sh<br>

## 配置
[uwsgi]<br>
http = :8080<br>
wsgi-file = run.py<br>
callable = app<br>
processes = 2<br>
threads = 50<br>
master = true<br>
pidfile = coopool.pid<br>

## 运行
开发环境：python3 run.py<br>
生产环境：uwsgi -d --ini coopool.ini 

# 接口
restfull接口,响应格式如下：<br>
{<br>
  "status":"1",<br>
  "msg":"成功",<br>
  "data":1<br>
}<br>
status:状态1成功0失败<br>
msg:状态说明<br>
data:响应数据，根据不同接口数据类型不同
## 注册
POST http://host:port/<website>/register<br>
参数：<br>
{<br>
  "validate_url":"http://host:port/index",<br>
  "alert_email":"a@c.com.b@d.com"<br>
}<br>
## 添加
POST http://host:port/<website>/add<br>
参数：<br>
{<br>
  "cookie":"_ga=GA1.2.2068545466.1534464283; xn_dvid_kf_20049=2FB1BB-5425381E-C994-6182-6357-5EC6070D830D; JSESSIONID=node01pvm6qovnp0o0126xk4nvddbm7384.node0"<br>
}
## 获取
GET http://host:port/<website>/random
## 统计
GET http://host:port/<website>/count
