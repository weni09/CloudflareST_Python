# !/usr/bin/env python
# -*-coding:utf-8 -*-
# ===================================================
# @Time : 2025/5/12 16:01                           
# @Author : weni09                                  
# @File : CFSpeedTest.py
# @Description：
# ===================================================
import ctypes
import ipaddress
import os
import re
import shutil
import sys
from typing import List
from SystemInfo import CPUArchitecture, OperatingSystem, SystemInfo
import subprocess
from consts import *
from func import read_txt


class CFSpeedTest:
    def __init__(self):
        self.sys_info = SystemInfo().get_system_info()

    def get_hosts_path(self) -> str:
        if self.sys_info["system"] == OperatingSystem.WINDOWS.value:
            return WINDOWS_HOSTS_PATH
        else:
            return OTHER_HOSTS_PATH

    def backup_hosts(self) -> bool:
        try:
            hosts_path = self.get_hosts_path()
            backup_path = hosts_path + "_backup"
            shutil.copy2(hosts_path, backup_path)
            return True
        except Exception as e:
            print(f"备份hosts失败: {e}")
            return False

    def get_cf_test_core(self) -> str:
        if self.sys_info["system"] == OperatingSystem.WINDOWS.value:
            if self.sys_info["architecture"] == CPUArchitecture.X86.value:
                return CORE_DIR.joinpath("CloudflareST_windows_x86.exe")
            elif self.sys_info["architecture"] == CPUArchitecture.X86_64.value:
                return CORE_DIR.joinpath("CloudflareST_windows_x86_64.exe")
        elif self.sys_info["system"] == OperatingSystem.LINUX.value:
            if self.sys_info["architecture"] == CPUArchitecture.X86.value:
                return CORE_DIR.joinpath("CloudflareST_linux_x86")
            elif self.sys_info["architecture"] == CPUArchitecture.X86_64.value:
                return CORE_DIR.joinpath("CloudflareST_linux_x86_64")
        else:
            return ""

    def run_cloudflarest(self):
        main_program = self.get_cf_test_core()
        if main_program == "":
            print("不支持的操作系统或架构")
            return False
        cmd_args = [main_program] + CF_TEST_PARAMS.split(" ")
        try:
            result = subprocess.run(
                cmd_args,
                check=True,
                timeout=600,  # 10分钟还未执行完成，则报超时
                encoding='utf-8'
            )
            if result.returncode == 0:
                if not RESULT_FILE.exists():
                    return False
                if len(read_txt(RESULT_FILE)) <= 1:
                    return False
                return True
            return False
        except subprocess.TimeoutExpired:
            print("命令执行超时")
            return False
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            return False

    def is_admin_windows(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def enhance_execution_authority_windows(self) -> bool:
        if not self.is_admin_windows():
            # 请求管理员权限重新运行
            print("当前无管理员权限，尝试提升权限...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1
            )
        return True

    @staticmethod
    def is_ipv4(ip):
        try:
            ip_obj = ipaddress.ip_address(ip)
            return isinstance(ip_obj, ipaddress.IPv4Address)
        except ValueError:
            return False

    def update_hosts(self, ip):
        block_pattern = re.compile(
            rf"{re.escape(START_MARK)}.*?{re.escape(END_MARK)}",
            re.DOTALL
        )
        try:
            # 构造新块
            new_block = "\n".join([START_MARK] + self.gen_new_block_lines(ip) + [END_MARK])
            file_path = self.get_hosts_path()
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if block_pattern.search(content):
                # 替换已有块
                updated_content = block_pattern.sub(new_block, content)
            else:
                # 追加新块，确保前面有一个换行
                if content and not content.endswith("\n"):
                    content += "\n"
                updated_content = content + new_block + "\n"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"hosts 更新成功")
        except Exception as e:
            print(f"更新hosts内容失败：{e}")

    def gen_new_block_lines(self, ip) -> List[str]:
        domains = read_txt(DOMAIN_FILE)
        return [ip + " " + x for x in domains]
