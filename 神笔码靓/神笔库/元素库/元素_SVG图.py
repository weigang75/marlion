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
from PIL import Image
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.元素库 import 图元素, 元素位置信息
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class SVG图元素(图元素):

    def change_colors(self, svg_data):
        颜色替换列表 = self.获取属性值("颜色替换列表", None)
        if 颜色替换列表 is not None:
            for 替换前颜色, 替换后颜色 in 颜色替换列表:
                svg_data = svg_data.replace(str(替换前颜色).encode(), str(替换后颜色).encode())

        return svg_data

    def 颜色替换(self, 替换前颜色, 替换后颜色):
        """

        :param 替换前颜色:
        :param 替换后颜色:
        :return:
        """
        if not hasattr(self, "数据处理回调"):
            self.数据处理(self.change_colors)
            setattr(self, "数据处理回调", 是)

        颜色替换列表 = self.获取属性值("颜色替换列表", None)
        if 颜色替换列表 is None:
            self.设置属性值("颜色替换列表", [])
            颜色替换列表 = self.获取属性值("颜色替换列表", None)

        颜色替换列表.append((替换前颜色, 替换后颜色))

        return self
