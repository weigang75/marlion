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


class 遮罩元素(可变换元素):

    def 获取元素范围(self):
        P = self.获取属性值

        遮罩元素_, 被遮元素 = P("遮罩元素"), P("被遮元素")

        return 遮罩元素_.获取元素范围()

    # def 构建SVG元素(self):
    #     P = self.获取属性值
    #     遮罩元素_, 被遮元素 = P("遮罩元素"), P("被遮元素")
    #     if not isinstance(遮罩元素_, list):
    #         遮罩元素_ = [遮罩元素_]
    #
    #     mask = self.dwg.mask(id=self.获取元素id(t="ma"))
    #
    #     for 元素 in 遮罩元素_:
    #         mask.add(元素.build_svg_element())
    #
    #     if 被遮元素 is not None:
    #         被遮元素.build_svg_element()['mask'] = getattr(mask, "get_funciri")()
    #
    #     return mask

    # 遮罩单位 ——“使用用户空间 | 物体边界框”
    # 定义属性 x、y、宽度和高度所使用的坐标系。
    # 如果遮罩单位为 “使用用户空间”，那么 x、y、宽度和高度表示在引用遮罩元素时所处的当前用户坐标系中的数值（即通过遮罩属性引用遮罩元素的那个元素的用户坐标系）。
    # 如果遮罩单位为 “物体边界框”，那么 x、y、宽度和高度表示应用遮罩的元素的边界框的分数或百分比。
    # 默认值是 “物体边界框”。
    # 遮罩内容单位 ——“使用用户空间 | 物体边界框”
    # 定义遮罩内容所使用的坐标系。
    # 如果遮罩内容单位为 “使用用户空间”，遮罩元素内容的用户坐标系就是在引用遮罩元素时所处的当前用户坐标系（即通过遮罩属性引用遮罩元素的那个元素的用户坐标系）。
    # 如果遮罩内容单位为 “物体边界框”，遮罩内容的用户坐标系是依据应用遮罩的元素的边界框来建立的。
    # 默认值是 “使用用户空间”。

    def 构建SVG元素(self):
        P = self.获取属性值
        遮罩元素_, 被遮元素 = P("遮罩元素"), P("被遮元素")
        if not isinstance(遮罩元素_, list):
            遮罩元素_ = [遮罩元素_]
        遮罩单位 = P("遮罩单位", None)
        遮罩内容单位 = P("遮罩内容单位", None)
        mask = self.dwg.mask(id=self.获取元素id(t="ma"))
        if 遮罩单位:
            mask.attribs["maskUnits"] = 遮罩单位
        if 遮罩内容单位:
            mask.attribs["maskContentUnits"] = 遮罩内容单位
        for 元素 in 遮罩元素_:
            mask.add(元素.build_svg_element())

        if 被遮元素 is not None:
            if not isinstance(被遮元素, list):
                被遮元素 = [被遮元素]

            for 元素 in 被遮元素:
                元素.build_svg_element()['mask'] = getattr(mask, "get_funciri")()

        return mask
