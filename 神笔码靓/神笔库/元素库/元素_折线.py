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
from 神笔码靓.神笔库.元素库 import 可变换元素, 样式可修改元素, 元素位置信息, 支持元素转路径, 路径元素
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 折线元素(可变换元素, 样式可修改元素, 支持元素转路径):
    def 转路径元素(self, 保留元素=False) -> 路径元素:
        顶点列表 = self.获取属性值("顶点列表", [])

        polyline = {
            'points': " ".join([f"{x},{y}" for x, y in 顶点列表])
        }

        if not 保留元素:
            self.删除()

        from svgpathtools.svg_to_paths import polyline2pathd
        path = polyline2pathd(polyline)
        return self.高清图.路径(填充颜色=self.获取属性值("填充颜色", 颜色.透明),
                           描边颜色=self.获取属性值("描边颜色", 颜色.黑色),
                           透明度=self.获取属性值("透明度", 1.0),
                           描边样式=self.获取属性值("描边样式", None),
                           描边宽度=self.获取属性值("描边宽度", 1)).原生path(path)

    def 获取元素范围(self):
        P = self.获取属性值

        最小x = float('inf')
        最小y = float('inf')
        最大x = float('-inf')
        最大y = float('-inf')

        顶点列表 = P("顶点列表")

        for 顶点x, 顶点y in 顶点列表:
            if 顶点x < 最小x:
                最小x = 顶点x
            if 顶点x > 最大x:
                最大x = 顶点x
            if 顶点y < 最小y:
                最小y = 顶点y
            if 顶点y > 最大y:
                最大y = 顶点y

        return 最小x, 最小y, 最大x, 最大y

    def 构建SVG元素(self):
        P = self.获取属性值
        C = self.获取颜色值
        points = P("顶点列表")
        polyline = self.dwg.polyline(points=points,
                                   # fill=C("填充颜色"), stroke=C("描边颜色"),
                                   # stroke_width=P("描边宽度"),
                                   # opacity=P("透明度", 1.0),
                                   alignment_baseline="auto",
                                   id=self.获取元素id(t="p"))

        self.属性修改处理(polyline)

        return polyline
