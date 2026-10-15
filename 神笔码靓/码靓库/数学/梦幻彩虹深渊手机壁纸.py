# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-09
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.手机.手机绘图板 import 手机绘图板
from 神笔码靓.神笔库 import 样式工具集
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *


class 梦幻彩虹深渊手机壁纸(手机绘图板):

    def 形状模板和大小(self):
        pass

    def 深渊中心(self):
        return self.屏幕宽 / 2, self.屏幕高 / 2

    def 计算圆坐标(self, 半径, 角度):
        """
        计算以某点为圆心，根据角度算出半径为r圆的坐标
        :param center: 圆心坐标 (x, y)
        :param 半径: 半径
        :param 角度: 角度（单位：度）
        :return: 圆上的点的坐标 (x, y)
        """
        中心X, 中心Y = self.深渊中心()
        # 将角度转换为弧度
        angle_rad = math.radians(角度)

        # 计算圆上点的坐标
        x = 中心X + 半径 * math.cos(angle_rad)
        y = 中心Y + 半径 * math.sin(angle_rad)

        return (x, y)

    def 屏幕元素(self):
        import math
        # self.显示图框()
        扇形列表 = 列表()
        扇形群列表 = 列表()
        self.画矩形(x=0, y=0, 宽=self.屏幕宽, 高=self.屏幕高, 填充颜色=颜色.黑色, id_="黑色背景").添加到列表(扇形列表)
        # 上 = 100
        # 高 = 80
        # 下宽 = 79
        # 描边宽度 = 5
        扇形模板, 宽, 高 = self.形状模板和大小()
        半径 = int(self.屏幕高)
        for i in 范围(50):
            半径 = 半径 / 1.2
            for 角度 in 范围(0, 360, 20):
                if i % 2 == 0:
                    角度 += 10
                x, y = self.计算圆坐标(半径=半径, 角度=角度)
                y += self.高 / 8
                扇形模板.创造元素(x=x, y=y).缩放(半径 / 300).旋转(90 + 角度, (x, y)). \
                    平移(-宽 / 2, -高 / 2).添加到列表(扇形群列表)

        彩虹渐变色 = self.创建彩虹线性渐变色(开始位置=(0, 0), 结束位置=(self.宽, self.高), 彩虹七色=样式工具集.彩虹色2)
        彩虹背景 = self.画矩形(x=0, y=0, 宽=self.屏幕宽, 高=self.屏幕高, 填充颜色=彩虹渐变色, id_="彩虹背景").添加到列表(扇形列表)

        扇形群 = self.创建组合(元素列表=扇形群列表, id_="扇形群")
        self.遮罩(遮罩元素_=扇形群, 被遮元素=彩虹背景, id_="彩虹遮罩")

        return 扇形列表
        # 缩放比 = 0.9
        # 旋转角度 = self.旋转角度
        # for i in range(100):
        #     缩放 = 幂运算(缩放比, i)
        #     宽 = self.宽 * 缩放
        #     高 = self.高 * 缩放
        #     描边宽度 = 6 * 缩放
        #     x, y = (self.宽 - 宽) / 2, (self.高 - 高) / 2
        #
        #     矩形 = self.画矩形(x=x, y=y, 宽=宽, 高=高, 描边颜色=颜色.白色, 描边宽度=描边宽度, 填充颜色=彩虹渐变色)
        #     if 旋转角度 != 0:
        #         矩形.旋转(i * 旋转角度)

