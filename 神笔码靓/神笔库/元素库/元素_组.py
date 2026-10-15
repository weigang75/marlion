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
from 神笔码靓.神笔库.元素库 import 可变换元素, 样式可修改元素, 元素模板
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 元素组(可变换元素, 样式可修改元素):

    def __init__(self, 高清图, 所属组: list):
        super(元素组, self).__init__(高清图, 所属组)
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

    def _操作(self, *args, **kwargs):
        操作名 = kwargs["操作名"]
        del kwargs["操作名"]
        for item in self.获取属性值("元素列表"):
            if hasattr(item, 操作名):
                funs = getattr(item, 操作名)
                if callable(funs):
                    funs(*args, **kwargs)
        return self

    def 虚线流动画(self, 方向: int = 1, 持续时间: [float, int] = 3, 周期: [float, int] = None,
              重复次数: int = None, 填充行为="remove"):
        """

        @param 方向:
        @param 持续时间:
        @param 周期:
        @param 重复次数:
        @param 填充行为:
        @return:
        """
        for 元素_ in self.元素列表:
            元素_.元素处理预设(self.动画.虚线流, {
                "方向": 方向, "持续时间": 持续时间, "周期": 周期, "重复次数": 重复次数, "填充行为": 填充行为
            })
        return self

    def __getattr__(self, name):
        # name 是方法名
        def method(*args, **kwargs):
            # print(f"调用的方法名: {name}")
            # print(f"参数: {args}, 关键字参数: {kwargs}")
            kwargs["操作名"] = name
            self._操作(*args, **kwargs)
            return self

        return method

    def remove(self, e):
        self.elements.remove(e)
        return self

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

    def 转为模板(self) -> 元素模板:
        return self.高清图.创建模板(元素列表=[self])

    @property
    def 元素列表(self):
        return self.获取属性值("元素列表", [])

    def 构建SVG元素(self):
        P = self.获取属性值
        元素列表 = P("元素列表")
        class_name = P("class_name", None)
        if class_name is None:
            class_name = P("样式类名", None)

        if class_name:
            gp = self.dwg.g(id=self.获取元素id(t="g"), class_=class_name)
        else:
            gp = self.dwg.g(id=self.获取元素id(t="g"))

        for el in 元素列表:
            if not isinstance(el, list):
                el = [el]
            for e in el:
                self.append(e)
                if e in e.所属组:
                    e.所属组.remove(e)
                e.所属组 = self
                gp.add(e.build_svg_element())

        样式可修改元素.属性修改处理(self, gp)
        可变换元素.属性修改处理(self, gp)

        return gp
