# !/usr/bin/env python
# -*-coding:utf-8 -*-
# ===================================================
# @Time : 2025/5/12 22:52                           
# @Author : weni09                                  
# @File : func.py
# @Description：
# ===================================================
from pathlib import Path
from typing import List


def read_txt(path: str | Path) -> List[str]:
    data_lines: List[str] = []
    with open(path, "rt", encoding="utf-8") as f:
        data_lines = f.readlines()
    data_lines = [
        line.strip() for line in data_lines
    ]
    return list(filter(lambda x: x != "", data_lines))
