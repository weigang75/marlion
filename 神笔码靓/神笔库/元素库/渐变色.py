# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import svgwrite

from 神笔码靓.神笔库.定义集 import *


class 渐变色:
    def __init__(self, svg_element):

        self.svg_element = svg_element

    def 矩阵(self, a, b, c, d, e, f):
        self.svg_element.matrix(a, b, c, d, e, f)
        return self

    def 缩放(self, 缩放X,缩放Y=None):
        # def scale(self, sx, sy=None):
        # if isinstance(缩放比例, tuple):
        #     sx, sy = 缩放比例
        # else:
        #     sx, sy = 缩放比例, None
        self.svg_element.scale(缩放X,缩放Y)
        return self

    def 垂直翻转(self):
        self.svg_element.scale((-1, 1))
        return self

    def 水平翻转(self):
        self.svg_element.scale((1, -1))
        return self

    def 平移(self, 位移X,位移Y=None):
        # def translate(self, tx, ty=None):
        # if isinstance(位移, tuple):
        #     tx, ty = 位移
        # else:
        #     tx, ty = 位移, None
        self.svg_element.translate(位移X,位移Y)
        return self

    def 倾斜X(self, 倾斜角度):
        self.svg_element.skewX(倾斜角度)
        return self

    def 倾斜Y(self, 倾斜角度):
        self.svg_element.skewY(倾斜角度)
        return self

    def 旋转(self, 旋转角度, 旋转中心点=None):
        self.svg_element.rotate(旋转角度, 旋转中心点)
        return self


class 径向渐变色(渐变色):
    pass


class 线性渐变色(渐变色):
    pass
