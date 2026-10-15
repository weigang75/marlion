# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.线条工具集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *


class 英语纸打印模板(神笔绘图板):
    def __init__(self, 作品文件路径, 线条颜色="#000000"):
        self.宽, self.高 = 纸张大小.A4_纵向()
        super(英语纸打印模板, self).__init__(作品文件路径=作品文件路径, 宽=self.宽, 高=self.高)
        # self.显示图框(显示网格=否)
        self.线条颜色 = 线条颜色

    def 创作(self):
        上边距, 下边距 = 50, 30
        左边距, 右边距 = 50, 30
        四线高度 = 40
        线条宽度 = 1.0

        两线高度 = 四线高度 / 3
        for i in range(0, 4):
            self.画水平线(x1=左边距, x2=self.宽 - 右边距,
                      y1=上边距 + i * 两线高度, y2=self.高 - 下边距 - 四线高度 + i * 两线高度,
                      数量=15, 描边颜色=self.线条颜色, 描边宽度=线条宽度)

    def 完成(self):
        super(英语纸打印模板, self).完成()
        self.生成PDF()
