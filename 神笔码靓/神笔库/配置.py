# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os

谷歌浏览器根目录 = r"C:\Program Files\Google\Chrome\Application"
谷歌浏览器执行文件 = "chrome.exe"


# 谷歌浏览器根目录 = r"G:\works\gitcode\code_painter"
# 谷歌浏览器执行文件 = "chrome64.exe"

def 自动查找谷歌浏览器():
    global 谷歌浏览器根目录, 谷歌浏览器执行文件
    潜在执行文件 = ["chrome.exe", "GoogleChrome.exe", "chrome64.exe"]
    潜在目录 = [
        r"C:\Program Files\Google\Chrome\Application",
        r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application"
    ]
    for 目录 in 潜在目录:
        for 文件名 in 潜在执行文件:
            chrome_exe = os.path.join(目录, 文件名)
            if os.path.exists(chrome_exe):
                谷歌浏览器根目录 = 目录
                谷歌浏览器执行文件 = 文件名
                return


def 谷歌浏览器是否有效():
    chrome_exe = os.path.join(谷歌浏览器根目录, 谷歌浏览器执行文件)
    if os.path.exists(chrome_exe):
        return True
    return False


if not 谷歌浏览器是否有效():
    自动查找谷歌浏览器()
