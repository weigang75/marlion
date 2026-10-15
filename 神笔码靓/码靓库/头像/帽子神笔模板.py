# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-10
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.头像.元素神笔模板 import 头像元素神笔模板
from 神笔码靓.神笔库 import 神笔模板, 神笔绘图板
from 神笔码靓.神笔库.线条工具集 import *
from 神笔码靓.神笔库.通用工具集 import *


class 头像帽子神笔模板(头像元素神笔模板):
    def 模板ID(self):
        return "头像.帽子"


if __name__ == '__main__':
    宽, 高 = 屏幕分辨率.我的手机()
    神笔 = 神笔绘图板(作品文件路径="头像_帽子.svg")
    神笔.神笔模板("头像.帽子", 文件="帽子01").创造元素(id_="头像_帽子")
    神笔.完成()
