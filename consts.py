# !/usr/bin/env python
# -*-coding:utf-8 -*-
# ===================================================
# @Time : 2025/5/12 22:33                           
# @Author : weni09                                  
# @File : consts.py
# @Description：
# ===================================================
from pathlib import Path

# 定义常量
BASE_DIR = Path(__file__).absolute().parent
WINDOWS_HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
OTHER_HOSTS_PATH = r"/etc/hosts"
START_MARK = "###### Cloudflare CDN IP Start #####"
END_MARK = "###### Cloudflare CDN IP End #####"
RESULT_FILE = BASE_DIR.joinpath("result_hosts.txt")
DOMAIN_FILE = BASE_DIR.joinpath("domain")
DEFALUT_IPV4_FILE = BASE_DIR.joinpath("ip.txt")
CF_TEST_PARAMS = f"-f {DEFALUT_IPV4_FILE.__str__()} -n 20 -tl 300 -sl 0.5 -dn 3 -dt 10 -p 0 -o {RESULT_FILE.__str__()}"
CORE_DIR = BASE_DIR.joinpath("core")

##这是openwrt中的路径，其它系统请自行修改
ADGUARD_RELOAD = "/etc/init.d/AdGuardHome reload"
ADGUARD_YAML_PATH = "/etc/AdGuardHome.yaml"
