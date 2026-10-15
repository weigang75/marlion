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
from 神笔码靓.神笔库.元素库 import 可变换元素, 样式可修改元素, 支持元素转路径, 路径元素
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 线元素(可变换元素, 样式可修改元素, 支持元素转路径):
    def 转路径元素(self, 保留元素=False) -> 路径元素:
        开始位置 = self.获取属性值("开始位置", (0, 0))
        结束位置 = self.获取属性值("结束位置", (0, 0))

        class line:
            attrib = {
                'x1': str(开始位置[0]),
                'y1': str(开始位置[1]),
                'x2': str(结束位置[0]),
                'y2': str(结束位置[1])
            }

        if not 保留元素:
            self.删除()
        from svgpathtools.svg_to_paths import line2pathd
        path = line2pathd(line)
        return self.高清图.路径(填充颜色=self.获取属性值("填充颜色", 颜色.透明),
                           描边颜色=self.获取属性值("描边颜色", 颜色.黑色),
                           透明度=self.获取属性值("透明度", 1.0),
                           描边样式=self.获取属性值("描边样式", None),
                           描边宽度=self.获取属性值("描边宽度", 1)).原生path(path)

    # def 追加顶点(self, 顶点命令):
    #     P = self.获取属性值
    #     点列表 = P("点列表")
    #     点列表.append(顶点命令)
    #     return self
    #
    # def 追加顶点列表(self, 追加顶点列表):
    #     P = self.获取属性值
    #     点列表 = P("点列表")
    #     点列表 += 追加顶点列表
    #     return self
    #
    # def 获取元素范围(self):
    #      return self.获取路径点列表范围()

    def 构建SVG元素(self):
        P = self.获取属性值
        C = self.获取颜色值

        开始位置 = P("开始位置")
        结束位置 = P("结束位置")
        x1, y1 = 开始位置
        x2, y2 = 结束位置

        line = self.dwg.line(start=(x1, y1), end=(x2, y2),
                             # stroke=C("描边颜色"),
                             # fill=C("填充颜色"),
                             # stroke_width=P("描边宽度"),
                             # opacity=P("透明度", 1),
                             shape_rendering='auto',
                             # stroke_linejoin="arcs",
                             id=self.获取元素id(t="l"))

        样式可修改元素.属性修改处理(self, line)
        可变换元素.属性修改处理(self, line)

        return line
