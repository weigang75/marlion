# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-08
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.神笔库.元素库 import 矩形元素
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.通用工具集 import *


class 手机绘图板(神笔绘图板):
    def __init__(self, 作品文件路径, 屏幕大小=None, 左右边距=50, 上边距=180, 下边距=80, 描边宽度=2, 手机颜色=None,
                 显示整机=否, 显示状态栏=是, 锁屏=是, 熄屏=否, 锁屏字体颜色=颜色.白色, 锁屏时间=None, 锁屏日期=None, 锁屏步数=None):
        if 屏幕大小 is None:
            屏幕大小 = 屏幕分辨率.我的手机()

        if 手机颜色 is None:
            手机颜色 = "#163844"

        self.屏幕大小 = 屏幕大小
        宽, 高 = 屏幕大小

        if 显示整机:
            宽 = 宽 + 左右边距 * 2 + 描边宽度 * 4
            高 = 高 + 上边距 + 下边距 + 描边宽度 * 4

        super(手机绘图板, self).__init__(作品文件路径=作品文件路径, 宽=宽, 高=高, 视图区=f"0 0 {宽} {高}")

        self.显示整机 = 显示整机
        self.显示状态栏 = 显示状态栏
        self.锁屏 = 锁屏
        self.熄屏 = 熄屏
        self.锁屏字体颜色 = 锁屏字体颜色
        self.左右边距 = 左右边距
        self.上边距 = 上边距
        self.下边距 = 下边距
        self.描边宽度 = 描边宽度
        self.屏幕宽, self.屏幕高 = self.屏幕大小
        self.锁屏时间 = 锁屏时间
        self.锁屏日期 = 锁屏日期
        self.锁屏步数 = 锁屏步数

        if isinstance(手机颜色, dict):
            手机颜色 = self.创建线性渐变色(**手机颜色)

        self.手机颜色 = 手机颜色
        self._屏幕元素列表 = 列表()

    def 智能手机已创建(self, 智能手机元素, 屏幕大小, 屏幕位置):
        pass

    def 屏幕元素(self):
        return []

    @property
    def 屏幕元素列表(self):
        return self._屏幕元素列表

    def 矩形背景(self, 填充颜色, 透明度: float = 1.0, id_: str = None) -> 矩形元素:
        """

        @param 填充颜色:
        @param 透明度:
        @param id_:
        @return:
        """
        return self.画矩形(x=0, y=0, 宽=self.屏幕宽, 高=self.屏幕高,
                        填充颜色=填充颜色, 描边宽度=0, 透明度=透明度, id_=id_)

    def 创作(self):
        # self.显示图框()
        # self.显示网格()
        self.创建屏幕元素()

    # def 创建屏幕元素(self):
    #     if len(self._屏幕元素列表) > 0:
    #         return self._屏幕元素列表
    #
    #     self._屏幕元素列表 = self.屏幕元素()
    #     return self._屏幕元素列表

    def 创建屏幕元素(self):
        if len(self._屏幕元素列表) > 0:
            return self._屏幕元素列表

        _屏幕元素 = self.屏幕元素()
        if _屏幕元素 is None:
            _屏幕元素 = self._屏幕元素列表
        else:
            self._屏幕元素列表 = _屏幕元素
        return self._屏幕元素列表

    def 创作前执行(self):
        if (self.显示状态栏 or self.锁屏 or self.熄屏) and self.显示整机:
            手机屏幕模板 = self.神笔模板("手机屏幕", 屏幕大小=self.屏幕大小, 是否锁屏=self.锁屏, 是否熄屏=self.熄屏,
                               锁屏时间=self.锁屏时间, 锁屏日期=self.锁屏日期, 锁屏步数=self.锁屏步数,
                               锁屏字体颜色=self.锁屏字体颜色, id_="手机屏幕")
        else:
            手机屏幕模板 = None

        if self.显示整机:
            智能手机模板 = self.神笔模板("手机外壳", id_="手机外壳",
                               左右边距=self.左右边距, 上边距=self.上边距, 下边距=self.下边距,
                               描边宽度=self.描边宽度, 手机颜色=self.手机颜色, 屏幕大小=self.屏幕大小)

            屏幕大小 = 智能手机模板.神笔模板返回值["屏幕大小"]
            屏幕位置 = 智能手机模板.神笔模板返回值["屏幕位置"]

            智能手机 = 智能手机模板.创造元素()
            self.智能手机已创建(智能手机, 屏幕大小, 屏幕位置)
            屏幕元素_ = self.创建屏幕元素()
            if 屏幕元素_ is not None:
                if isinstance(屏幕元素_, list):
                    屏幕元素_ = self.创建组合(元素列表=屏幕元素_, id_="手机屏幕图像")

                矩形裁剪 = self.画矩形(x=0, y=0, 宽=屏幕大小[0], 高=屏幕大小[1])
                裁剪 = self.裁剪(裁剪元素_=矩形裁剪, 被裁元素=屏幕元素_, id_="手机屏幕图像裁剪")
                屏幕元素_.平移(*屏幕位置)

                if self.熄屏:
                    缩放 = 0.6

                    def 计算缩放平移量(x, y, x_scale, y_scale):
                        translate_x = -(x * x_scale - x) / x_scale
                        translate_y = -(y * y_scale - y) / y_scale
                        return translate_x, translate_y

                    屏幕元素_.缩放(缩放, 缩放).平移(*计算缩放平移量(self.屏幕宽 / 2, 0, 缩放, 缩放))
        else:
            智能手机 = None
            屏幕位置 = None

        if 手机屏幕模板 is not None:
            if 屏幕位置 is not None:
                手机屏幕 = 手机屏幕模板.创造元素().平移(*屏幕位置)
            手机屏幕.置前()

        if 智能手机 is not None:
            智能手机.置前()
