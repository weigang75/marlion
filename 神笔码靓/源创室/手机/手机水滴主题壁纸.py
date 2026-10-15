# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-04
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.手机.手机水珠主题壁纸 import 手机水珠主题壁纸
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.通用工具集 import *

if __name__ == '__main__':
    神笔 = 手机水珠主题壁纸(作品文件路径="手机壁纸_大水珠橙背景.svg", 背景颜色="#DB5B1C", 水珠大小=200, 显示整机=是, 显示状态栏=是,
                  锁屏=是, 手机颜色="#163844")
    神笔.完成()
    # SVG 转 PNG 建议使用 https://svgtopng.com/zh/   滤镜支持
    # 神笔.生成PNG(生成方式=PNG生成方式.cairosvg, 缩放=2) # 不支持滤镜

    神笔 = 手机水珠主题壁纸(作品文件路径="手机壁纸_小水珠绿背景.svg", 背景颜色="#9AFD2B", 水珠大小=50, 显示整机=是, 显示状态栏=是,
                  锁屏=是, 锁屏字体颜色="black", 手机颜色="#163844")
    神笔.完成()
    # SVG 转 PNG 建议使用 https://svgtopng.com/zh/   滤镜支持
    # 神笔.生成PNG(生成方式=PNG生成方式.cairosvg, 缩放=2) # 不支持滤镜
