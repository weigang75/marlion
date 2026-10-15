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
from 神笔码靓.神笔库.元素库 import 可变换元素, 样式可修改元素, 元素位置信息
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 复用元素(可变换元素, 样式可修改元素):

    def 获取元素范围(self):
        P = self.获取属性值

        对象元素 = P("对象元素")

        return 对象元素.获取元素范围()

        # return 最小x, 最小y, 最大x, 最大y

    # def 设置子元素属性(self, 元素序号, 属性名, 属性值):
    #     P = self.获取属性值
    #     子元素属性字典 = P("子元素属性字典", None)
    #     if 子元素属性字典 is None:
    #         self.设置属性值("子元素属性字典", {})
    #         子元素属性字典 = P("子元素属性字典", None)
    #
    #     子元素属性 = 子元素属性字典.get(元素序号, None)
    #     if 子元素属性 is None:
    #         子元素属性字典[元素序号] = {}
    #         子元素属性 = 子元素属性字典.get(元素序号, None)
    #
    #     子元素属性[属性名] = 属性值
    def 填充颜色(self, 颜色):
        self.设置属性值("填充颜色", 颜色)
        return self

    def 构建SVG元素(self):
        P = self.获取属性值
        R = self.获取对象引用
        对象引用 = R("对象元素")
        # 对象元素 = P("对象元素")
        # 宽, 高 = P("宽"), P("高")
        use_element = self.dwg.use(href=对象引用,
                                   x=P("x", 0), y=P("y", 0),
                                   # width=宽, height=高,
                                   # opacity=P("透明度", 1),
                                   alignment_baseline="middle",
                                   id=self.获取元素id(t="u"))

        self.属性修改处理(use_element)
        # 透明度 = P("透明度", 1)
        # if 透明度 != 1:
        #     use_element.attribs["opacity"] = 透明度
        #
        # 填充颜色 = P("填充颜色", None)
        # if 填充颜色 is not None:
        #     use_element.fill(填充颜色)
        # 子元素属性字典 = P("子元素属性字典", None)
        # if 子元素属性字典 is not None:
        #     use_element.fill("red")
        # for 元素序号 in 子元素属性字典:
        #     element = use_element.elements[元素序号]

        return use_element
