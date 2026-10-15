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

from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.元素库 import 可变换元素, 元素位置信息, 样式可修改元素


class 路径文字元素(可变换元素, 样式可修改元素):

    def 获取元素范围(self):
        return self.获取路径点列表范围()

    def 字旋转(self, 旋转角度: float):
        self.设置属性值("字旋转", 旋转角度)
        return self

    def 构建文字(self):
        粗体, 斜体, 下划线, 字符间距 = self.批量获取属性(["粗体", "斜体", "下划线", "字符间距"])
        style = self.样式.文字样式生成(粗体, 斜体, 下划线, 字符间距)

        P = self.获取属性值
        C = self.获取颜色值
        t = self.dwg.text("", insert=(0, 0), fill=C("填充颜色"),
                          font_size=P("字体大小"),
                          style=style,
                          text_anchor=P("水平基线对齐"),
                          stroke=C("描边颜色"), stroke_width=P("描边宽度"),
                          # alignment_baseline=P("垂直基线对齐"),
                          font_family=P("字体"),
                          # opacity=P("透明度", 1),
                          id=self.获取元素id(t="t"))

        self.属性修改处理(t)

        # 透明度 = P("透明度", 1)
        # if 透明度 != 1:
        #     t.attribs["opacity"] = 透明度
        #
        # _描边样式 = P("描边样式")
        # if _描边样式 is not None:
        #     t['stroke-dasharray'] = _描边样式
        #
        _字旋转 = P("字旋转", 0)
        if _字旋转 != 0:
            t["rotate"] = _字旋转

        return t

    def 构建路径(self):
        P = self.获取属性值
        C = self.获取颜色值
        点列表 = P("点列表")
        fp = 点列表[0]
        if fp[0] in ["M", "m"]:
            t, x, y = fp
        else:
            t, x, y = "M", fp[0], fp[1]
        path = self.dwg.path(d="{}{:.2f},{:.2f} ".format(t, x, y), stroke=C("描边颜色"), fill="none",
                             stroke_width=0, opacity=P("透明度", 1), shape_rendering='auto',
                             # stroke_linejoin="arcs",
                             id=self.获取元素id(t="p"))

        d_list = 神笔绘图板工具.点列表转SVG路径(点列表)
        # if 转相对坐标:
        #     d_list = 神笔绘图板工具.绝对坐标转相对坐标(d_list)
        for di in d_list[1:]:
            path.push(di)

        if P("闭合", 否):
            path.push('Z')

        _描边样式 = P("描边样式")
        if _描边样式 is not None:
            path['stroke-dasharray'] = _描边样式

        return path

    def 先描边(self):
        self.样式字符串("paint-order:stroke;")
        return self

    def 构建SVG元素(self):
        text = self.构建文字()
        path = self.构建路径()

        P = self.获取属性值

        # text.letter_spacing = 5
        if "x" in text.attribs:
            del text.attribs["x"]
        if "y" in text.attribs:
            del text.attribs["y"]
        if "alignment-baseline" in text.attribs:
            del text.attribs["alignment-baseline"]

        textpath = self.dwg.textPath(path=path, text=P("文字"), startOffset=P("开始位移"), spacing="auto",
                                     method="stretch")

        text.add(textpath)
        _字旋转 = P("字旋转", 0)
        if _字旋转 != 0:
            text["rotate"] = _字旋转
        g = self.dwg.g()

        样式可修改元素.属性修改处理(self, text)
        可变换元素.属性修改处理(self, text)

        g.add(text)
        g.add(path)
        return g
