# !/usr/bin/env python
# -*-coding:utf-8 -*-
# ===================================================
# @Time : 2025/5/12 22:29
# @Author : weni09
# @File : AdguardHandler.py
# @Description：
# ===================================================
import yaml
from pathlib import Path
from typing import List
import shutil
from func import read_txt
from consts import *
import subprocess


class AdguardHandler:
    def __init__(self, adguard_yaml_path: str, adguard_reload_cmd: str):
        self.adguard_yaml_path = adguard_yaml_path
        self.adguard_reload_cmd = adguard_reload_cmd

    def load_yaml(self):
        """加载YAML文件"""
        with open(self.adguard_yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def save_yaml(self, data):
        """保存YAML文件"""
        with open(self.adguard_yaml_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True, sort_keys=False)

    def delete_all_rewrites(self, data):
        """完全删除filtering.rewrites部分"""
        if 'filtering' in data and 'rewrites' in data['filtering']:
            del data['filtering']['rewrites']
            print("已完全删除filtering.rewrites部分")
        else:
            print("filtering.rewrites部分不存在")

    def gen_new_rewrites(self, ip) -> List[dict]:
        domains = read_txt(DOMAIN_FILE)
        new_rewrites = []
        for domain in domains:
            new_rewrites.append({
                "domain": domain,
                "answer": ip
            })
        # print(f"生成的新new_rewrites: {new_rewrites}")
        return new_rewrites

    def backup_ad_yaml(self):
        """备份adguard.yaml文件"""
        try:

            backup_path = Path(self.adguard_yaml_path).with_suffix(".yaml.bak")
            shutil.copy2(self.adguard_yaml_path, backup_path)
            print(f"备份文件{backup_path.name}已创建")
            return True
        except Exception as e:
            print(f"备份文件{Path(self.adguard_yaml_path).name}失败：{e}")
            return False

    def replace_all_rewrites(self, data, ip: str):
        """完全替换filtering.rewrites部分"""
        if 'filtering' not in data:
            data['filtering'] = {}
        data['filtering']['rewrites'] = self.gen_new_rewrites(ip)
        print("已完全替换filtering.rewrites部分")

    def adguard_reload(self):
        try:
            cmd_args = self.adguard_reload_cmd.split(" ")
            result = subprocess.run(
                cmd_args,
                check=True,
                encoding='utf-8'
            )
            if result.returncode == 0:
                print("AdGuard成功重新加载")
            else:
                print("AdGuard重新加载失败")
        except Exception as e:
            print(f"AdGuard重新加载失败：{e}")
