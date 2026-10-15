# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-02
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import math
import os

from 神笔码靓.码靓库.手机.手机绘图板 import 手机绘图板
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *
from 神笔码靓.码靓库.共用.国家简码 import 国家简码
from 神笔码靓.神笔库.通用工具集 import *
from PIL import Image


class 手机文字像素艺术画(手机绘图板):

    def __init__(self, 作品文件路径, 图片路径, 文字内容=None, 像素形状="圆像素", 像素透明度=0.2, 像素缩放=1,
                 像素列数=30, 左空字数=3, 右空字数=3, 上字空数=3, 图片左移像素点=0, 自己来控制像素=False,
                 显示整机=否, 显示状态栏=是, 锁屏=是, 锁屏字体颜色=颜色.白色, 熄屏=否, 手机颜色="#163844", 显示图片=否):
        """

        :param 作品文件路径:
        :param 图片路径:
        :param 文字内容:
        :param 像素形状: 圆像素、五边形像素、四边形像素、六边形像素、心形像素、菱形像素  倒角矩(倒角方)
        :param 像素透明度:
        :param 像素缩放:
        :param 像素列数:
        :param 左空字数:
        :param 右空字数:
        :param 上字空数:
        :param 图片左移像素点:
        """
        self.屏幕宽, self.屏幕高 = 屏幕分辨率.我的手机()
        super(手机文字像素艺术画, self).__init__(作品文件路径=作品文件路径, 屏幕大小=(self.屏幕宽, self.屏幕高), 显示整机=显示整机,
                                        显示状态栏=显示状态栏, 锁屏=锁屏, 熄屏=熄屏, 锁屏字体颜色=锁屏字体颜色, 手机颜色=手机颜色)
        # self.显示图框()
        self.图片路径 = 图片路径
        self.文字内容 = 文字内容
        self.像素列数 = 像素列数
        self.左空字数 = 左空字数
        self.右空字数 = 右空字数
        self.上字空数 = 上字空数
        self.圆像素宽 = self.屏幕宽 / 像素列数
        self.图片左移像素 = 图片左移像素点
        self.圆像素透明度 = 像素透明度
        self.圆像素缩放 = 像素缩放
        self.圆像素形状 = 像素形状
        self.自己来控制像素 = 自己来控制像素
        self.像素元素列表 = 列表()
        self.显示图片 = 显示图片

        # self.设置背景色("#ff706C")

    def 控制像素的形状大小颜色(self, 圆像素形状, 像素尺寸大小, 颜色RGB):
        return 圆像素形状, 像素尺寸大小, 颜色.RGB(*颜色RGB)

    def 屏幕元素(self):
        屏幕元素_ = 列表()

        图片 = Image.open(self.图片路径).convert('RGBA')
        图片宽, 图片高 = 图片.size
        像素步长 = int(取最小数(图片宽 / self.屏幕宽, 图片高 / self.屏幕高) // (1 / self.圆像素宽))
        图像缩放 = 1

        # 像素步长 = 6
        # 图像缩放 = 21.4/像素步长

        字体大小缩放 = 0.9
        文字位置微调 = 0, -1
        左边距 = 0
        上边距 = 0

        换行列数 = -1
        退出行数 = -7
        换行列数 = 0
        退出行数 = 0
        像素列数 = 图片宽 // 像素步长
        像素行数 = 图片高 // 像素步长

        if self.显示图片:
            图片缩放 = max(像素列数 * self.圆像素宽 / 图片宽, 像素行数 * self.圆像素宽 / 图片高)
            平移 = 像素步长 / 图片缩放
            # 平移 = 0
            self.SVG贴图(x=0, y=0, 图片文件=self.图片路径).缩放(图片缩放).透明度(0.6).平移(平移, 平移).添加到列表(屏幕元素_)
        # .平移(self.左右边距 , self.上边距)

        if 换行列数 == 0:
            换行列数 = 像素列数 + 2
        elif 换行列数 < 0:
            换行列数 = 像素列数 + 换行列数 + 1

        if 退出行数 == 0:
            退出行数 = 像素行数 + 2
        elif 退出行数 < 0:
            退出行数 = 像素行数 + 退出行数 + 1

        # from PIL import Image
        # 图片 = Image.open(self.图片路径).convert('RGBA')
        def 取像素色(x, y):
            像素步长 = 3
            pixels = []
            for xi in range(像素步长):
                if 图片宽 <= x + xi:
                    break
                for yi in range(像素步长):
                    if 图片高 <= y + yi:
                        break
                    pixel = 图片.getpixel((x + xi, y + yi))
                    pixels.append(pixel)
            # 计算每个通道的平均值
            r_total = g_total = b_total = a_total = 0
            count = len(pixels)

            if count == 1:
                return pixels[0][0], pixels[0][1], pixels[0][2]
                # return 颜色.RGB(*list(pixels[0])[:-1])

            for pixel in pixels:
                r_total += pixel[0]
                g_total += pixel[1]
                b_total += pixel[2]
                a_total += pixel[3]

            # 计算平均值
            average_pixel = (
                r_total // count,
                g_total // count,
                b_total // count,
                a_total // count
            )
            return average_pixel[0], average_pixel[1], average_pixel[2]
            # return 颜色.RGB(*list(average_pixel)[:-1])
            # return 颜色.RGB(*list(pixel)[:-1])

        hi, wi = 0, 0
        直径 = self.圆像素宽
        i = 0
        字体 = "小篆体"
        字体 = 系统字体.幼圆
        for h in range(0, 图片高, 像素步长):
            # row = []
            if hi >= 退出行数:
                break
            for w in range(self.图片左移像素, 图片宽, 像素步长):
                if wi >= 换行列数:
                    break
                # 以图片像素为坐标，每个像素点到中心的距离

                cx, cy = 左边距 + (wi + 0.5) * 直径, 上边距 + (hi + 0.5) * 直径
                # pixel = 图片.getpixel((w, h))
                # print(pixel, center)
                r, g, b = 取像素色(w, h)
                像素尺寸大小 = 直径 * 0.5 * self.圆像素缩放
                if self.自己来控制像素:
                    圆像素形状, 像素尺寸大小, 填充颜色 = self.控制像素的形状大小颜色(self.圆像素形状, 像素尺寸大小, (r, g, b))
                else:
                    填充颜色 = 颜色.RGB(r, g, b)
                    圆像素形状 = self.圆像素形状

                if "圆像素" in 圆像素形状:
                    像素圆 = self.画圆(cx, cy, 像素尺寸大小, 填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                elif "四边形像素" in 圆像素形状:
                    像素圆 = self.画正四边形(cx, cy, 像素尺寸大小, 填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                elif "五边形像素" in 圆像素形状:
                    像素圆 = self.画正五边形(cx, cy, 像素尺寸大小, 填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                elif "六边形像素" in 圆像素形状:
                    像素圆 = self.画正六边形(cx, cy, 像素尺寸大小, 填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                elif "心形像素" in 圆像素形状:
                    像素圆 = self.画爱心(cx, cy, 像素尺寸大小, 填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                    # 像素圆 = self.写字(cx, cy, "❤", 字体大小=直径 * 1.15,字体=系统字体.Verdana,
                    # 填充颜色=填充颜色, 描边宽度=0).缩放(1, 1.25)
                elif "菱形像素" in 圆像素形状:
                    像素圆 = self.画菱型(cx, cy, 像素尺寸大小, 填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                elif "倒角矩" in 圆像素形状 or "倒角方" in 圆像素形状:
                    像素圆 = self.画矩形(cx - 像素尺寸大小, cy - 像素尺寸大小, 2 * 像素尺寸大小, 2 * 像素尺寸大小,
                                   圆角半径=像素尺寸大小 / 3, 填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                else:
                    像素圆 = self.写字(cx, cy, 文字=圆像素形状, 字体大小=像素尺寸大小, 字体=系统字体.微软雅黑,
                                  填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_)
                    # 像素圆 = self.画圆(cx, cy, 直径 * 0.5 * self.圆像素缩放, 填充颜色=填充颜色, 描边宽度=0)

                无字圆像素透明度 = 返回最小值(self.圆像素透明度 * 1.6, 1)
                if 不为空(self.文字内容):
                    if wi >= self.左空字数 and wi < self.像素列数 - self.右空字数 and hi >= self.上字空数:
                        if i < 返回长度(self.文字内容):
                            字 = self.文字内容[i]
                            self.写字(x=cx, y=cy, 文字=字, 字体=字体, 字体大小=直径 * 0.8 * 字体大小缩放,
                                    填充颜色=填充颜色, 描边宽度=0).添加到列表(屏幕元素_).平移(文字位置微调[0], 文字位置微调[1])

                            if 字 != 全角空格:
                                像素圆.透明度(self.圆像素透明度)
                                无字圆像素透明度 = None
                            i += 1

                if 无字圆像素透明度:
                    像素圆.透明度(无字圆像素透明度)

                self.像素元素列表.添加元素(像素圆)
                if self.显示图片:
                    像素圆 = 像素圆.透明度(0.5)
                wi += 1

            # print(wi)
            hi += 1
            wi = 0

        return 屏幕元素_
