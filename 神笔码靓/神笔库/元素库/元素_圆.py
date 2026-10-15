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


class 圆元素(可变换元素, 样式可修改元素, 支持元素转路径):
    def 转路径元素(self, 保留元素=False) -> 路径元素:
        ellipse = {
            'cx': self.获取属性值("x", 0),
            'cy': self.获取属性值("y", 0),
            'r': self.获取属性值("半径", 10)
        }
        if not 保留元素:
            self.删除()
        from svgpathtools.svg_to_paths import ellipse2pathd
        path = ellipse2pathd(ellipse)
        return self.高清图.路径(填充颜色=self.获取属性值("填充颜色", 颜色.透明),
                           描边颜色=self.获取属性值("描边颜色", 颜色.黑色),
                           透明度=self.获取属性值("透明度", 1.0),
                           描边样式=self.获取属性值("描边样式", None),
                           描边宽度=self.获取属性值("描边宽度", 1)
                           ).原生path(path)

    def 获取元素范围(self):
        P = self.获取属性值

        x, y, 半径 = P("x"), P("y"), P("半径")

        最小x = x - 半径
        最小y = y - 半径
        最大x = x + 半径
        最大y = y + 半径

        return 最小x, 最小y, 最大x, 最大y

    def 构建SVG元素(self):
        P = self.获取属性值
        C = self.获取颜色值
        c = self.dwg.circle(center=(P("x"), P("y")), r=P("半径"),
                            # fill=C("填充颜色"),
                            alignment_baseline="auto",
                            # stroke_width=P("描边宽度"),
                            # stroke=C("描边颜色"),
                            # opacity=P("透明度", 1.0),
                            id=self.获取元素id(t="c"))

        样式可修改元素.属性修改处理(self, c)
        可变换元素.属性修改处理(self, c)

        # 透明度 = P("透明度", 1)
        # if 透明度 != 1:
        #     c.attribs["opacity"] = 透明度
        #
        # 填充颜色 = C("填充颜色", "none")
        # 描边颜色 = C("描边颜色", 颜色.黑色)
        #
        # if 填充颜色 != 颜色.无:
        #     c.fill(填充颜色)
        #
        # if 描边颜色 != 颜色.无:
        #     c.stroke(描边颜色)
        #
        # _描边样式 = P("描边样式")
        # if _描边样式 is not None:
        #     c['stroke-dasharray'] = _描边样式

        return c
