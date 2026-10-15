# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-11-05
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os
import svgwrite

from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.元素库 import 元素
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 链接元素(元素):
    def 构建SVG元素(self):
        元素对象, 链接地址, 链接提示, 链接描述, 新开窗口 = self.批量获取属性(["元素对象", "链接地址", "链接提示", "链接描述", "新开窗口"])
        if 新开窗口:
            target = '_blank'
        else:
            target = '_self'

        if hasattr(元素对象,"___绑定链接"):
            if getattr(元素对象, "___绑定链接") == True:
                raise Exception(f"{元素对象}已经绑定了一个链接，无法再绑定其他链接")

        # 创建一个带有超级链接的文本元素
        link = self.dwg.add(self.dwg.a(href=链接地址, target=target))
        link.add(元素对象.build_svg_element())
        # link.set_title(链接说明)

        link.set_desc(title=链接提示, desc=链接描述)
        setattr(元素对象, "___绑定链接", True)
        # 将图形元素添加到SVG文档中
        # dwg.add(link_text)

        return link
