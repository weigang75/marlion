# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2025-01-10
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.头像.元素神笔模板 import 头像元素神笔模板
from 神笔码靓.神笔库 import 神笔模板, 神笔绘图板
from 神笔码靓.神笔库.线条工具集 import *
from 神笔码靓.神笔库.通用工具集 import *


class 头像部件:
    def __init__(self, 绘图板: 神笔绘图板):
        self._视图高 = 320
        self._视图宽 = 320
        self.绘图板 = 绘图板

    @property
    def 视图中心(self):
        return self._视图宽 / 2, self._视图高 / 2

    @property
    def 视图高(self):
        return self._视图高

    @property
    def 视图宽(self):
        return self._视图宽

    @property
    def 面部位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0], 视图中心_[1]

    @property
    def 鼻子位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0], 视图中心_[1] + round(self._视图高 / 9.5, 2)

    @property
    def 左眼位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0] + round(self._视图宽 / 10, 2), 视图中心_[1]

    @property
    def 右眼位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0] - round(self._视图宽 / 10, 2), 视图中心_[1]

    @property
    def 左眉位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0] + round(self._视图宽 / 10, 2), \
               视图中心_[1] - round(self._视图高 / 12, 2)

    @property
    def 右眉位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0] - round(self._视图宽 / 10, 2), \
               视图中心_[1] - round(self._视图高 / 12, 2)

    @property
    def 嘴巴位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0], 视图中心_[1]

    @property
    def 头发位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0], 视图中心_[1] - round(self._视图高 / 3, 2)

    @property
    def 左耳位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0] + round(self._视图宽 / 3.8, 2), \
               视图中心_[1] + round(self._视图高 / 40, 2)

    @property
    def 右耳位置(self):
        视图中心_ = self.视图中心
        return 视图中心_[0] - round(self._视图宽 / 3.8, 2), \
               视图中心_[1] + round(self._视图高 / 40, 2)

    def 定位(self, 绘图板, 位置):
        x, y = 位置
        #  x: float, y: float, 宽度: float = 5, 高度: float = 5, 颜色
        return 绘图板.十字(x=x, y=y, 宽度=10, 高度=10, 颜色=颜色.红色)

    def 元素(self):
        return None


if __name__ == '__main__':
    class 眼睛部件(头像部件):
        def 元素(self):
            绘图板 = self.绘图板
            左眼位置 = self.左眼位置
            右眼位置 = self.右眼位置
            眼睛模板 = 绘图板.画圆(x=10, y=10,
                          半径=8, 描边颜色=颜色.黑色).缩放(1.2, 0.8).创建模板()

            眼睛模板.创造元素().平移(-10, -10).平移(*左眼位置)
            眼睛模板.创造元素().平移(-10, -10).平移(*右眼位置)


    绘图板 = 神笔绘图板(作品文件路径="头像部件定位.svg", 宽=320, 高=320)
    眼睛 = 眼睛部件(绘图板)
    绘图板.贴图(x=0, y=0, 图片文件=资源库目录("素材/漫画卡通/头像/参考线.svg"))
    眼睛.元素()
    # 头像部件.定位(绘图板, 头像部件.左眉位置)
    # 绘图板.显示辅助线()
    绘图板.完成()
