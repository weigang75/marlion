# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os
import svgwrite

from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.元素库 import 可变换元素, 元素位置信息
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 元素图案(可变换元素):

    def __init__(self, 高清图, 所属组: list):
        super(元素图案, self).__init__(高清图, 所属组)
        self.elements = []

    def remove(self, e):
        self.elements.remove(e)

    def append(self, e):
        self.elements.append(e)

    def 获取元素范围(self):
        P = self.获取属性值

        最小x = float('inf')
        最小y = float('inf')
        最大x = float('-inf')
        最大y = float('-inf')

        return 最小x, 最小y, 最大x, 最大y

    def 构建SVG元素(self):
        P = self.获取属性值
        元素列表 = P("元素列表")
        class_name = P("class_name")

        x = P("x")
        y = P("y")
        宽 = P("宽")
        高 = P("高")

        if class_name:
            gp = self.dwg.pattern(id=self.获取元素id(t="pa"), insert=(x, y), size=(宽, 高), class_=class_name,
                                  patternUnits='userSpaceOnUse')
        else:
            gp = self.dwg.pattern(id=self.获取元素id(t="pa"), insert=(x, y), size=(宽, 高),
                                  patternUnits='userSpaceOnUse')

        for e in 元素列表:
            self.append(e)
            e.所属组.remove(e)
            e.所属组 = self
            gp.add(e.svg_element)

        return gp
