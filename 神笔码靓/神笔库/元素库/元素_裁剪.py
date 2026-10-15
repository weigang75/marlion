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
from 神笔码靓.神笔库.元素库 import 可变换元素, 元素位置信息
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 裁剪元素(可变换元素):

    def 获取元素范围(self):
        P = self.获取属性值

        裁剪元素, 被裁元素 = P("裁剪元素"), P("被裁元素")

        return 裁剪元素.获取元素范围()

    def 构建SVG元素(self):
        P = self.获取属性值
        href = P("href")
        裁剪元素, 被裁元素 = P("裁剪元素"), P("被裁元素")
        裁剪路径单位 = P("裁剪路径单位", None)
        if not isinstance(裁剪元素, list):
            裁剪元素 = [裁剪元素]

        clip_path = self.dwg.clipPath(id=self.获取元素id(t="clip"))

        if 裁剪路径单位:
            clip_path.attribs["clipPathUnits"] = 裁剪路径单位

        for 元素_ in 裁剪元素:
            clip_path.add(元素_.build_svg_element())

        # 裁剪元素.所属组.remove(裁剪元素)
        # 裁剪元素.所属组 = []
        # 裁剪元素.所属组.append(self)

        if 被裁元素 is not None:
            被裁元素.build_svg_element()['clip-path'] = getattr(clip_path, "get_funciri")()
        return clip_path
