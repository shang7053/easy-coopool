#!/bin/bash
# author:scc
# 一键安装基础环境
# requests>=2.13.0
# redis>=2.10.5
# Flask>=0.12.1

echo "start install"
cd /opt
echo "install python3"
mkdir soft/python3
cd soft/python3
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
tar xvzf Python-3.6.8.tgz
cd Python-3.6.8
yum install zlib zlib-devel gcc libffi-devel openssl openssl-devel -y
ln -s /usr/include/openssl /usr/bin/ssl
./configure --with-ssl
make && make install
echo "update pip"
python3 -m pip install --upgrade pip
echo "install requests reids flask uwsgi"
pip3 install requests redis flask uwsgi