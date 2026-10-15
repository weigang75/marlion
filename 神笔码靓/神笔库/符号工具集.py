# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.神笔库.元素库 import 路径元素
from 神笔码靓.神笔库.定义集 import *


class 符号工具集:
    def __init__(self, 高清图):
        from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
        self.高清图: 神笔绘图板 = 高清图

    def 叉(self, x=0, y=0, 中心点=None, 线长=10) -> 路径元素:
        投影线长 = 线长 * math.sin(45 * math.pi / 180) / 2
        if 中心点 is not None:
            中心点x, 中心点y = 中心点
            x = 中心点x - 投影线长
            y = 中心点y - 投影线长
        路径点列表 = [
            ("移动", x, y), ("直线", x + 2 * 投影线长, y + 2 * 投影线长),
            ("移动", x + 2 * 投影线长, y), ("直线", x, y + 2 * 投影线长)
        ]
        return self.高清图.连线(路径点列表=路径点列表)

    def 圆(self, 中心点=None, 半径=10, 顺时针=是, 旋转角度=0) -> 路径元素:
        cx, cy = 中心点
        from 神笔码靓.神笔库 import 创建圆路径
        路径点列表 = 创建圆路径(cx, cy, 半径, 顺时针=顺时针, 旋转角度=旋转角度)
        return self.高清图.连线(路径点列表=路径点列表)
