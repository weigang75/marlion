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

from 神笔码靓.神笔库.元素库 import 元素, 复用元素


class 元素模板(元素):

    def __init__(self, 高清图, 所属组: list):
        super(元素模板, self).__init__(高清图, 所属组)
        self.elements = []
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.elements):
            result = self.elements[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def remove(self, e):
        self.elements.remove(e)

    def 移除元素(self, e):
        self.elements.remove(e)
        return self

    def append(self, e):
        self.elements.append(e)
        return self

    def 添加元素(self, e):
        self.elements.append(e)
        return self

    def 获取元素范围(self):
        return self.获取元素列表范围()

    def 设置视图区(self, 最小x, 最小y, 宽, 高):
        self.设置属性值("视图区", (最小x, 最小y, 宽, 高))
        return self

    # def 旋转(self, 旋转角度, 旋转中心点=None):
    #     raise AttributeError("元素模板不支持“旋转”")
    #
    # def 缩放(self, 缩放X, 缩放Y=None):
    #     raise AttributeError("元素模板不支持“缩放”")
    #
    # def 垂直翻转(self):
    #     raise AttributeError("元素模板不支持“垂直翻转”")
    #
    # def 水平翻转(self):
    #     raise AttributeError("元素模板不支持“水平翻转”")
    #
    # def 平移(self, 位移X, 位移Y=None):
    #     raise AttributeError("元素模板不支持“平移”")
    #
    # def 矩阵(self, a, b, c, d, e, f):
    #     raise AttributeError("元素模板不支持“矩阵”")
    #
    # def 倾斜X(self, 倾斜角度):
    #     raise AttributeError("元素模板不支持“倾斜X”")
    #
    # def 倾斜Y(self, 倾斜角度):
    #     raise AttributeError("元素模板不支持“倾斜Y”")

    def 创造元素(self, x: float = None, y: float = None, 透明度: float = 1.0, id_: str = None) -> 复用元素:
        return self.高清图.复制元素(对象元素=self, x=x, y=y, 透明度=透明度, id_=id_)

    def 添加元素(self, 元素_):
        元素列表_ = self.元素列表
        if 元素_ not in 元素列表_:
            元素列表_.append(元素_)
        return self

    @property
    def 元素列表(self):
        元素列表_ = self.获取属性值("元素列表", None)
        if 元素列表_ is None:
            元素列表_ = []
            self.设置属性值("元素列表", 元素列表_)

        return 元素列表_

    def 构建SVG元素(self):
        P = self.获取属性值
        元素列表 = P("元素列表")
        class_name = P("class_name", None)
        if class_name is None:
            class_name = P("样式类名", None)

        if class_name:
            symbol = self.dwg.symbol(id=self.获取元素id(t="s"), class_=class_name)
        else:
            symbol = self.dwg.symbol(id=self.获取元素id(t="s"))

        from collections.abc import Iterable

        for e in 元素列表:
            self.append(e)
            if isinstance(e.所属组, Iterable):
                if e in e.所属组:
                    e.所属组.remove(e)
                e.所属组 = self
                symbol.add(e.build_svg_element())

        return symbol
