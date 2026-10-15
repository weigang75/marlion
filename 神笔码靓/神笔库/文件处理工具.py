# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-07-20
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os.path

import os
import hashlib

from 神笔码靓.神笔库 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.通用工具集 import *

file_id_dict = {}
file_name_keys = ["boy", "girl", "woman", "man"]


def 文件更名_svgrepo(目录):
    global file_id_dict
    pattern = re.compile(r'svgrepo-com.*')
    for fd in os.listdir(目录):
        if not fd.endswith(".svg"):
            continue
        file_path = os.path.join(目录, fd)
        new_file_name = pattern.sub('', fd).strip()
        new_file_name, _ = os.path.splitext(new_file_name)
        new_file_name = new_file_name.strip("-")

        id_no = file_id_dict.get(new_file_name, None)
        if id_no is None:
            file_id_dict[new_file_name] = 100
            id_no = ""
        else:
            file_id_dict[new_file_name] += 1
            id_no += 1
            id_no = f"_{str(id_no).rjust(3, '0')}"

        new_file_name = f"{new_file_name}{id_no}.svg"
        print(fd, "=>", new_file_name)

        if fd != new_file_name:  # 只有在文件名不同的情况下才重命名
            print(f"重命名: {fd} -> {new_file_name}")
            os.rename(os.path.join(目录, fd), os.path.join(目录, new_file_name))

        # for key in file_name_keys:
        #     if key in fd.lower():
        #         id_no = file_id_dict.get(key, None)
        #         if id_no is None:
        #             file_id_dict[key] = 1
        #             id_no = 1
        #         else:
        #             file_id_dict[key] += 1
        #             id_no += 1
        #         new_file_name = f"{key}_{str(id_no).rjust(5, '0')}"
        #         print(fd, "=>", new_file_name)
        #         break


新名称索引 = 1


def 文件更名(目录, 更改名称):
    global 新名称索引
    for fd in os.listdir(目录):
        if not fd.endswith(".svg"):
            continue
        file_path = os.path.join(目录, fd)
        new_file_name = 更改名称 + f"_{str(新名称索引).rjust(3, '0')}" + ".svg"

        新名称索引 += 1

        if fd != new_file_name:  # 只有在文件名不同的情况下才重命名
            print(f"重命名: {fd} -> {new_file_name}")
            os.rename(os.path.join(目录, fd), os.path.join(目录, new_file_name))


def 获取文件的哈希值(file_path):
    """计算文件的哈希值"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def 删除重复的文件(目录):
    """删除指定目录中的重复文件"""
    if not os.path.isdir(目录):
        print(f"{目录} 不是一个有效的目录")
        return

    file_hashes = {}
    for root, _, files in os.walk(目录):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = 获取文件的哈希值(file_path)

            if file_hash in file_hashes:
                print(f"删除重复文件: {file_path}")
                os.remove(file_path)  # 删除重复文件
            else:
                file_hashes[file_hash] = file_path


def 按文件名排序(目录):
    if not os.path.isdir(目录):
        print(f"{目录} 不是一个有效的目录")
        return

    file_list = []
    for root, _, files in os.walk(目录):
        for file in files:
            file_list.append(file)

    # 按文件名排序
    sorted_file_list = sorted(file_list)

    # 输出排序后的文件列表
    for file in sorted_file_list:
        print(file)
    return sorted_file_list


if __name__ == "__main__":
    pass
    # 删除重复的文件(资源库目录("素材/漫画卡通/头像/女头发"))
    # 文件更名(资源库目录("素材/漫画卡通/头像/女头发"), "女生头发")
    # 文件更名(资源库目录("素材/漫画卡通/头像/男头发"), "男生头发")
