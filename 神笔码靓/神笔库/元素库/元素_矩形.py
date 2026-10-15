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


class 矩形元素(样式可修改元素, 可变换元素, 支持元素转路径):
    def 转路径元素(self, 保留元素=False) -> 路径元素:
        rect = {
            'x': self.获取属性值("x", 0),
            'y': self.获取属性值("y", 0),
            'width': self.获取属性值("宽", 10),
            'height': self.获取属性值("高", 10),
        }
        if not 保留元素:
            self.删除()
        from svgpathtools.svg_to_paths import rect2pathd
        path = rect2pathd(rect)
        return self.高清图.路径(填充颜色=self.获取属性值("填充颜色", 颜色.透明),
                                描边颜色=self.获取属性值("描边颜色", 颜色.黑色),
                                透明度=self.获取属性值("透明度", 1.0),
                                描边样式=self.获取属性值("描边样式", None),
                                描边宽度=self.获取属性值("描边宽度", 1)).原生path(path)

    def 获取元素范围(self):
        P = self.获取属性值

        x, y, 宽, 高 = P("x"), P("y"), P("宽"), P("高")
        最小x = x
        最小y = y
        最大x = x + 宽
        最大y = y + 高

        return 最小x, 最小y, 最大x, 最大y

    @property
    def 圆角半径(self):
        P = self.获取属性值
        C = self.获取颜色值
        return P("圆角半径", None)

    @圆角半径.setter
    def 圆角半径(self, 半径):
        self.设置属性值("圆角半径", 半径)

    def 构建SVG元素(self):
        P = self.获取属性值
        C = self.获取颜色值
        圆角半径 = P("圆角半径", None)

        if 圆角半径 is None:
            rx, ry = None, None
        elif isinstance(圆角半径, tuple):
            rx, ry = 圆角半径[0], 圆角半径[1]
        else:
            rx, ry = 圆角半径, 圆角半径

        填充颜色 = C("填充颜色", "none")
        rect = self.dwg.rect(insert=(P("x"), P("y")),
                             size=(P("宽"), P("高")),
                             # fill=填充颜色,
                             # stroke=C("描边颜色"),
                             rx=rx, ry=ry,
                             # stroke_width=P("描边宽度"),
                             # opacity=P("透明度", 1.0),
                             alignment_baseline="auto",
                             id=self.获取元素id(t="rc"))

        样式可修改元素.属性修改处理(self, rect)
        可变换元素.属性修改处理(self, rect)
        # 透明度 = P("透明度", 1)
        # if 透明度 != 1:
        #     rect.attribs["opacity"] = 透明度
        #
        # if 填充颜色 != 颜色.无:
        #     rect.fill(填充颜色)
        #
        # _描边样式 = P("描边样式")
        # if _描边样式 is not None:
        #     rect['stroke-dasharray'] = _描边样式

        return rect
