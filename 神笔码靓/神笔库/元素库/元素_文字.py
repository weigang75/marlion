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

from 神笔码靓.神笔库 import 获取文字的宽高
from 神笔码靓.神笔库.元素库 import 可变换元素, 元素位置信息, 样式可修改元素, 路径元素
from 神笔码靓.神笔库.元素库.元素转路径支持 import 支持元素转路径
from 神笔码靓.神笔库.定义集 import *


class 文字元素(可变换元素, 样式可修改元素, 支持元素转路径):
    # def __init__(self):
    #     self.元素属性 = {}
    # super(文字元素, self).__init__(高清图)
    def 转路径元素(self, 保留元素=False) -> 路径元素:
        x = self.获取属性值("x")
        y = self.获取属性值("y")
        文字 = self.获取属性值("文字")
        字体 = self.获取属性值("字体")
        字体大小 = self.获取属性值("字体大小")
        填充颜色 = self.获取属性值("填充颜色")
        描边颜色 = self.获取属性值("描边颜色")
        描边宽度 = self.获取属性值("描边宽度")
        字符间距 = self.获取属性值("字符间距")
        # 水平基线对齐=文字水平基线对齐.起始点对齐, 垂直基线对齐=文字垂直基线对齐.顶线对齐,
        水平基线对齐 = self.获取属性值("水平基线对齐", 文字水平基线对齐.中点对齐)
        垂直基线对齐 = self.获取属性值("垂直基线对齐", 文字垂直基线对齐.中线对齐)
        from 神笔码靓.神笔库.字体查找器 import 字体查找器
        finder = 字体查找器(verbose=False)
        字体文件 = finder.get_font_path(字体)
        if 字体文件 is None:
            字体文件 = finder.get_font_path("安卓字体")

        字体宽度, 字体高度 = 获取文字的宽高(字体文件, 字体大小, 文字)
        offset_x = 0
        offset_y = 0
        if 水平基线对齐 == 文字水平基线对齐.起始点对齐:
            offset_x = 0
        elif 水平基线对齐 == 文字水平基线对齐.中点对齐:
            offset_x = 字体宽度 / 2
        elif 水平基线对齐 == 文字水平基线对齐.结束点对齐:
            offset_x = 字体宽度

        if 垂直基线对齐 == 文字垂直基线对齐.顶线对齐:
            offset_y = 0
        elif 垂直基线对齐 == 文字垂直基线对齐.中线对齐:
            offset_y = 字体高度 / 2
        elif 垂直基线对齐 == 文字垂直基线对齐.底线对齐:
            offset_y = 字体高度

        if 字符间距 is None:
            字符间距 = 0

        # from 神笔码靓.神笔库.路径工具集 import 字体文本路径工具
        # 路径 = 字体文本路径工具.(x=x - offset_x, y=y - offset_y, 文字=文字, 字体大小=字体大小, 字体文件=字体文件,
        # # 字符间距 -= 字符间距 * 0.0058
        # 路径 = self.高清图.文字转路径(x=x - offset_x, y=y - offset_y, 文字=文字, 字体大小=字体大小, 字体文件=字体文件,
        #                     字符间距=字符间距, 填充颜色=填充颜色, 描边颜色=描边颜色, 描边宽度=描边宽度)
        路径 = self.文字转路径(x=x - offset_x, y=y - offset_y, 字体文件=字体文件, 字体大小=字体大小, 文字=文字, 字符间距=字符间距)

        if not 保留元素:
            self.删除()

        xmin, xmax, ymin, ymax = 路径.获取元素范围()
        height = ymax - ymin
        scale = 字体大小 / height * 0.9
        路径.坐标缩放(scale, scale)

        return 路径

    def 文字转路径(self, x, y, 字体文件, 字体大小, 文字, 字符间距):
        from 神笔码靓.神笔库.路径工具集 import 字体文本路径工具
        文字路径工具 = 字体文本路径工具(self, 字体文件, 字体大小, 字符间距)
        字符串路径点列表 = 文字路径工具.生成字符串路径(文字, 纵向=否, 文字位置微调=None)

        路径点列表 = []
        for 字符路径点列表 in 字符串路径点列表:
            路径点列表 += 字符路径点列表

        return self.高清图.连线(路径点列表=路径点列表,
                           填充颜色=self.获取属性值("填充颜色", 颜色.透明),
                           描边颜色=self.获取属性值("描边颜色", 颜色.黑色),
                           透明度=self.获取属性值("透明度", 1.0),
                           描边样式=self.获取属性值("描边样式", None),
                           描边宽度=self.获取属性值("描边宽度", 1)).坐标平移(x, y)

    def 保留空格(self):
        # xml:space = "preserve"
        self.设置属性值("空格处理行为", "preserve")
        return self

    def 字旋转(self, 旋转角度: float):
        self.设置属性值("字旋转", 旋转角度)
        return self

    def 文字(self, 文字: str):
        self.设置属性值("文字", 文字)
        return self

    def 字体(self, 字体: str):
        self.设置属性值("字体", 字体)
        return self

    def 字符间距(self, 字符间距: float):
        self.设置属性值("字符间距", 字符间距)
        return self

    def 水平基线对齐(self, 水平基线对齐: 文字水平基线对齐):
        self.设置属性值("水平基线对齐", 水平基线对齐)
        return self

    def 垂直基线对齐(self, 垂直基线对齐: 文字垂直基线对齐):
        self.设置属性值("垂直基线对齐", 垂直基线对齐)
        return self

    def 字体大小(self, 字体大小: [float, str]):
        if isinstance(字体大小, str):
            当前字体大小 = self.获取属性值("字体大小", 16)
            if 字体大小.endswith("%"):
                字体大小 = round(float(字体大小[:-1]) / 100 * 当前字体大小, 2)
            else:
                pass

        self.设置属性值("字体大小", 字体大小)
        return self

    def 粗体(self, 粗体: bool = True):
        self.设置属性值("粗体", 粗体)
        return self

    def 斜体(self, 斜体: bool = True):
        self.设置属性值("斜体", 斜体)
        return self

    def 下划线(self, 下划线: bool = True):
        self.设置属性值("下划线", 下划线)
        return self

    def 获取元素范围(self) -> 元素位置信息:
        P = self.获取属性值

        x, y, 文字, 字体, 字体大小, 水平基线对齐, 垂直基线对齐 = \
            P("x"), P("y"), P("文字"), P("字体"), P("字体大小"), P("水平基线对齐"), P("垂直基线对齐")

        宽, 高 = 获取文字的宽高(字体, 字体大小, 文字)
        宽, 高 = 宽 * 0.75, 高 * 0.9
        if 水平基线对齐 == 文字水平基线对齐.起始点对齐:
            最小x = x
            最大x = x + 宽
        elif 水平基线对齐 == 文字水平基线对齐.中点对齐:
            最小x = x - 宽 / 2
            最大x = x + 宽 / 2
        elif 水平基线对齐 == 文字水平基线对齐.结束点对齐:
            最小x = x - 宽
            最大x = x

        if 垂直基线对齐 == 文字垂直基线对齐.顶线对齐:
            最小y = y
            最大y = y + 高
        elif 垂直基线对齐 == 文字垂直基线对齐.中线对齐:
            最小y = y - 高 / 2
            最大y = y + 高 / 2
        elif 垂直基线对齐 == 文字垂直基线对齐.底线对齐:
            最小y = y - 高
            最大y = y

        return 最小x, 最小y, 最大x, 最大y

    def 构建SVG元素(self):
        粗体, 斜体, 下划线, 字符间距 = self.批量获取属性(["粗体", "斜体", "下划线", "字符间距"])
        style = self.样式.文字样式生成(粗体, 斜体, 下划线, 字符间距)

        P = self.获取属性值
        C = self.获取颜色值
        t = self.dwg.text(P("文字"), insert=(P("x"), P("y")),
                          # fill=C("填充颜色"),
                          # font_size=P("字体大小"),
                          style=style,
                          # text_anchor=,
                          # stroke=C("描边颜色"),
                          # stroke_width=P("描边宽度"),
                          # alignment_baseline=P("垂直基线对齐"),
                          # font_family=P("字体"),
                          # opacity=P("透明度", 1),
                          id=self.获取元素id(t="t"))
        text_anchor = P("水平基线对齐", None)
        alignment_baseline = P("垂直基线对齐", None)
        font_family = P("字体", None)
        font_size = P("字体大小", None)
        空格处理行为 = P("空格处理行为", None)

        if font_size is not None:
            t["font-size"] = font_size

        if text_anchor is not None:
            t["text-anchor"] = text_anchor

        if alignment_baseline is not None:
            t["alignment-baseline"] = alignment_baseline

        if font_family is not None:
            t["font-family"] = font_family

        if 空格处理行为:
            # xml:space = "preserve"
            t["xml:space"] = 空格处理行为

        # self.属性修改处理(t)
        样式可修改元素.属性修改处理(self, t)
        可变换元素.属性修改处理(self, t)
        # 透明度 = P("透明度", 1)
        # if 透明度 != 1:
        #     t.attribs["opacity"] = 透明度
        #
        # 填充颜色 = C("填充颜色", "none")
        # 描边颜色 = C("描边颜色", 颜色.黑色)
        #
        # if 填充颜色 != 颜色.无:
        #     t.fill(填充颜色)
        #
        # if 描边颜色 != 颜色.无:
        #     t.stroke(描边颜色)
        #
        # _描边样式 = P("描边样式")
        # if _描边样式 is not None:
        #     t['stroke-dasharray'] = _描边样式
        #
        _字旋转 = P("字旋转", 0)
        if _字旋转 != 0:
            t["rotate"] = _字旋转

        return t
