# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-09
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.手机.手机绘图板 import 手机绘图板
from 神笔码靓.码靓库.数学.梦幻彩虹深渊手机壁纸 import 梦幻彩虹深渊手机壁纸
from 神笔码靓.神笔库 import 样式工具集
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *


class 椭圆深渊手机壁纸(梦幻彩虹深渊手机壁纸):

    def 深渊中心(self):
        return self.屏幕宽 / 5, self.屏幕高 / 4

    def 形状模板和大小(self):
        宽 = 100
        高 = 80
        描边宽度 = 5
        x, y = 描边宽度 / 2 + 宽, 描边宽度 / 2 + 高

        椭圆 = self.画椭圆(x=x, y=y, 半径=(宽, 高), 描边颜色=颜色.白色)

        return self.创建模板(元素列表=[椭圆], id_="椭圆模板"), 宽, 高


if __name__ == '__main__':
    神笔 = 椭圆深渊手机壁纸(作品文件路径=f"手机壁纸_椭圆深渊.svg", 显示整机=是, 锁屏=否)

    神笔.完成()
