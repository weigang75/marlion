# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.地理.世界地图数据 import 世界地图数据, 世界高清地图数据
from 神笔码靓.码靓库.地理.中国地图数据 import 中国地图数据, 中国高清地图数据
from 神笔码靓.神笔库.定义集 import *


def 获取世界地图数据(是否高清=否):
    if 是否高清:
        return 世界高清地图数据
    else:
        return 世界地图数据


def 获取中国地图数据(是否高清=否):
    if 是否高清:
        return 中国高清地图数据
    else:
        return 中国地图数据
