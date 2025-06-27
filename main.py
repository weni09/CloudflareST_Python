# !/usr/bin/env python
# -*-coding:utf-8 -*-
# ===================================================
# @Time : 2025/5/12 15:42                           
# @Author : weni09                                  
# @File : main.py
# @Description：
# ===================================================
import sys

from CFSpeedTest import CFSpeedTest
from consts import *
from pathlib import Path
from func import read_txt
from SystemInfo import OperatingSystem


def do_update(with_ad=False):
    cfst = CFSpeedTest()
    if cfst.run_cloudflarest():
        ip_test_list = read_txt(RESULT_FILE)
        best_ip = ip_test_list[1].split(",")[0]
        if not cfst.is_ipv4(best_ip):
            print("非法IPV4")
            quit(1)
        if cfst.sys_info["system"] == OperatingSystem.WINDOWS.value:
            cfst.enhance_execution_authority_windows()
        if cfst.backup_hosts():  # 备份成功后执行
            cfst.update_hosts(best_ip)
        else:
            print("hosts 备份失败，不执行更新操作")
        if with_ad:
            from AdguardHandler import AdguardHandler
            ad_handler = AdguardHandler(ADGUARD_YAML_PATH, ADGUARD_RELOAD)
            if ad_handler.backup_ad_yaml():
                data = ad_handler.load_yaml()
                ad_handler.replace_all_rewrites(data, best_ip)
                ad_handler.save_yaml(data)
                ad_handler.adguard_reload()
            else:
                print(f"{Path(ADGUARD_YAML_PATH).name} 备份失败，不执行更新操作")
    else:
        print("测速失败，不执行更新操作")
        quit(1)


if __name__ == '__main__':
    is_ad = False
    if len(sys.argv) > 1 and sys.argv[1] == "ad":
        is_ad = True
    do_update(is_ad)