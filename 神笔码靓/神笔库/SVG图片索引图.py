# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-07-20
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os.path

import os
import hashlib

from 神笔码靓.神笔库 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.文件处理工具 import 按文件名排序
from 神笔码靓.神笔库.通用工具集 import *


class SVG图片索引图(神笔绘图板):
    def 指定目录(self, 目录):
        self.目录 = 目录

    def 创作(self):
        左边距 = 50
        上边距 = 50
        x = 0
        y = 0
        X间距 = 80
        Y间距 = 100

        for 文件 in 按文件名排序(self.目录):
            if "图片索引" in 文件:
                continue
            文件路径 = os.path.join(self.目录, 文件)
            from 神笔码靓.神笔库 import 神笔绘图板工具
            try:
                宽, 高 = 神笔绘图板工具.获取SVG图片大小(文件路径)
            except Exception as e:
                print(e)
                continue
            缩放 = X间距 / 取最大数(宽, 高)
            self.SVG贴图(x=左边距 + x * X间距, y=上边距 + y * Y间距, 图片文件=文件路径).缩放(缩放 * 0.9)

            if len(文件) > 20:
                文件 = [文件[:20], 文件[20:]]
            else:
                文件 = [文件]

            for i, f in enumerate(文件):
                self.写字(x=左边距 + x * X间距, y=上边距 + y * Y间距 + X间距 + i * 8, 文字=f, 字体大小=6,
                        水平基线对齐=文字水平基线对齐.起始点对齐)
            x = x + 1
            if 左边距 + x * X间距 > self.宽:
                x = 0
                y = y + 1

        self.最大高度 = 上边距 + (y + 1) * Y间距

    def 完成前执行(self):
        # print("最大页数", self.最大页数)
        # 高 = self.页高 * self.最大页数
        self.修改绘图板大小(高=self.最大高度)


if __name__ == "__main__":
    SVG图片根目录 = 资源库目录("素材/漫画卡通/头像/女_选")

    SVG图片根目录 = r"G:\works\gitcode\code_painter\资源库\素材\中国元素"

    神笔 = SVG图片索引图(os.path.join(SVG图片根目录, "SVG图片索引.svg"))
    神笔.指定目录(SVG图片根目录)
    神笔.完成()
