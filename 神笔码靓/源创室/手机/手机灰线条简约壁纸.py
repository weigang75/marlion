# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-11
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.手机.手机绘图板 import 手机绘图板
from 神笔码靓.码靓库.手机.手机重复渐近色壁纸 import 手机重复渐近色壁纸
from 神笔码靓.神笔库.元素库 import 元素模板, 线性渐变色, 径向渐变色
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *


class 手机灰线条简约壁纸(手机重复渐近色壁纸):

    def 颜色列表和分界线模糊度(self):
        return ["#3E404C", "#535561"], 0.00


if __name__ == '__main__':
    壁纸 = 手机灰线条简约壁纸("手机壁纸_灰线条简约壁纸.svg", 显示整机=是)
    壁纸.完成()
