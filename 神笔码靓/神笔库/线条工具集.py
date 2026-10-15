# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================

import math

from 神笔码靓.神笔库.定义集 import *


def 找粘贴区域点(点A, 点B, 距离, 角度):
    x1, y1 = 点A
    x2, y2 = 点B

    # 计算线段AB的长度
    length_AB = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # 计算旋转后的点的坐标
    x3 = x1 + 距离 * (x2 - x1) / length_AB
    y3 = y1 + 距离 * (y2 - y1) / length_AB

    angle_rad = math.radians(角度)
    x_rotated = x1 + (x3 - x1) * math.cos(angle_rad) - (y3 - y1) * math.sin(angle_rad)
    y_rotated = y1 + (x3 - x1) * math.sin(angle_rad) + (y3 - y1) * math.cos(angle_rad)

    return x_rotated, y_rotated


def 计算粘贴区域点(粘贴区域线集合, 距离=50.0, 角度=33.0, 强制计算=True):
    new_list = []
    for l in 粘贴区域线集合:
        if not 强制计算 and len(l) > 2:
            new_list.append(l)
            continue
        p1 = 找粘贴区域点(l[0], l[-1], 距离, 角度)
        p2 = 找粘贴区域点(l[-1], l[0], 距离, -角度)
        # p13, e11, r1 = get_center(l[0], l[-1], 10, 10)
        new_list.append([l[0], p1, p2, l[-1]])
    return new_list


def 计算曲线粘贴区域点(曲线路径, 开始点=0, 结束点=1, 步长=0.1, 粘贴区域距离=10.0, 粘贴区角度=-45):
    粘贴线集合 = []
    p_list = list(range(int(开始点 * 10000), int(结束点 * 10000), int(步长 * 10000)))
    for pidx, pp in enumerate(p_list):
        if pidx == 0:
            continue
        last_pp = p_list[pidx - 1]
        p = round(pp / 10000, 6)
        last_p = round(last_pp / 10000, 6)
        last_x, last_y = 曲线路径.位置坐标(last_p)
        点x, 点y = 曲线路径.位置坐标(p)
        粘贴线集合.append((round(last_x, 2), round(last_y, 2)))
        # [[A, B], [B, C], [C, D], [D, E], [E, e]]
        pts = 计算粘贴区域点([[(last_x, last_y), (点x, 点y)]], 距离=粘贴区域距离, 角度=粘贴区角度)
        _, p1, p2, _ = pts[0]
        粘贴线集合.append((round(p1[0], 2), round(p1[1], 2)))
        粘贴线集合.append((round(p2[0], 2), round(p2[1], 2)))

        粘贴线集合.append((点x, 点y))

    return 粘贴线集合

def 计算曲线法线点(曲线路径, 开始点=0, 结束点=1, 步长=0.1, 粘贴区域距离=10.0, 方向=1):
    粘贴线集合 = []
    if 方向 == -1:
        粘贴区角度 = -90
    else:
        粘贴区角度 = 90
    p_list = list(range(int(开始点 * 10000), int(结束点 * 10000), int(步长 * 10000)))
    for pidx, pp in enumerate(p_list):
        if pidx == 0:
            continue
        last_pp = p_list[pidx - 1]
        p = round(pp / 10000, 6)
        last_p = round(last_pp / 10000, 6)
        last_x, last_y = 曲线路径.位置坐标(last_p)
        点x, 点y = 曲线路径.位置坐标(p)
        # 粘贴线集合.append((round(last_x, 2), round(last_y, 2)))
        # [[A, B], [B, C], [C, D], [D, E], [E, e]]
        pts = 计算粘贴区域点([[(last_x, last_y), (点x, 点y)]], 距离=粘贴区域距离, 角度=粘贴区角度)
        _, p1, p2, _ = pts[0]
        粘贴线集合.append((round(p1[0], 2), round(p1[1], 2)))
        # 粘贴线集合.append((round(p2[0], 2), round(p2[1], 2)))

        # 粘贴线集合.append((点x, 点y))

    return 粘贴线集合

def 创建矩形路径(x, y, 宽=100, 高=100, 倒角半径=(5, 5), 顺时针=否):
    if isinstance(倒角半径, tuple):
        倒角半径X, 倒角半径Y = 倒角半径
    else:
        倒角半径X, 倒角半径Y = 倒角半径, 倒角半径

    if 顺时针:
        开始X, 开始Y = x + 倒角半径X, y

        px1, py1 = 开始X, 开始Y
        px2, py2 = x + 宽 - 倒角半径X, y
        ax3, ay3 = x + 宽, y + 倒角半径Y
        px4, py4 = x + 宽, y + 高 - 倒角半径Y
        ax5, ay5 = x + 宽 - 倒角半径X, y + 高
        px6, py6 = x + 倒角半径X, y + 高
        ax7, ay7 = x, y + 高 - 倒角半径Y
        px8, py8 = x, y + 倒角半径Y

        路径 = [("移动", px1, py1),
                ("水平线", px2),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 1, ax3, ay3),
                ("垂直线", py4),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 1, ax5, ay5),
                ("水平线", px6),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 1, ax7, ay7),
                ("垂直线", py8),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 1, px1, py1),
                ("闭合",)
                ]
    else:
        开始X, 开始Y = x, y + 倒角半径Y

        px1, py1 = 开始X, 开始Y
        px2, py2 = x, y + 高 - 倒角半径Y
        ax3, ay3 = x + 倒角半径X, y + 高
        px4, py4 = x + 宽 - 倒角半径X, y + 高
        ax5, ay5 = x + 宽, y + 高 - 倒角半径Y
        px6, py6 = x + 宽, y + 倒角半径Y
        ax7, ay7 = x + 宽 - 倒角半径X, y
        px8, py8 = x + 倒角半径X, y

        路径 = [("移动", px1, py1),
                ("垂直线", py2),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 0, ax3, ay3),
                ("水平线", px4),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 0, ax5, ay5),
                ("垂直线", py6),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 0, ax7, ay7),
                ("水平线", px8),
                ("椭圆弧线", 倒角半径X, 倒角半径Y, 0, 0, 0, px1, py1),
                ("闭合",)
                ]

    return 路径


# def 创建矩形路径(x, y, 宽=100, 高=100, 倒角半径=2, 顺时针=否):
#     开始X, 开始Y = x, y + 倒角半径
#
#     px1, py1 = 开始X, 开始Y
#     px2, py2 = x, y + 高 - 倒角半径
#     ax3, ay3 = x + 倒角半径, y+ 高
#     px4, py4 = x + 宽 - 倒角半径, y+ 高
#     ax5, ay5 = x + 宽 , y  + 高 - 倒角半径
#     px6, py6 = x + 宽, y + 倒角半径
#     ax7, ay7 = x+ 宽-倒角半径, y
#     px8, py8 = x+ 倒角半径, y
#
#     路径 = [("移动", px1, py1),
#           ("垂直线", py2),
#           ("椭圆弧线", 倒角半径, 倒角半径, 0, 0, 0, ax3, ay3),
#           ("水平线", px4),
#           ("椭圆弧线", 倒角半径, 倒角半径, 0, 0,0, ax5, ay5),
#           ("垂直线", py6),
#           ("椭圆弧线", 倒角半径, 倒角半径, 0, 0, 0, ax7, ay7),
#           ("水平线", px8),
#           ("椭圆弧线", 倒角半径, 倒角半径, 0, 0, 0, px1, py1),
#           ("闭合",)
#           ]
#
#     return 路径

def 创建椭圆路径(x, y, x半径, y半径, 顺时针=是, 旋转角度=0):
    点路径列表 = [("M", x, y),
                  ("M", x - x半径, y),
                  ("A", x半径, y半径, 0, 1, 1 if 顺时针 else 0, x半径 + x, y),
                  ("A", x半径, y半径, 0, 1, 1 if 顺时针 else 0, x - x半径, y),
                  ("Z",)
                  ]

    if 旋转角度 != 0:
        弧度 = math.radians(旋转角度)
        x0, y0 = x, y
        for i in range(len(点路径列表)):
            操作, *参数 = 点路径列表[i]
            if 操作 == "M":
                x, y = 参数
                x1 = math.cos(弧度) * (x - x0) - math.sin(弧度) * (y - y0) + x0
                y1 = math.sin(弧度) * (x - x0) + math.cos(弧度) * (y - y0) + y0
                点路径列表[i] = ("M", x1, y1)
            elif 操作 == "A":
                rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y = 参数
                x1 = math.cos(弧度) * (x - x0) - math.sin(弧度) * (y - y0) + x0
                y1 = math.sin(弧度) * (x - x0) + math.cos(弧度) * (y - y0) + y0
                点路径列表[i] = ("A", rx, ry, x_axis_rotation + 旋转角度, large_arc_flag, sweep_flag, x1, y1)

    return 点路径列表


def 创建圆路径(x, y, 半径, 顺时针=是, 旋转角度=0):
    return 创建椭圆路径(x=x, y=y, x半径=半径, y半径=半径, 顺时针=顺时针, 旋转角度=旋转角度)
    # 点路径列表 = [("M", x, y),
    #          ("M", x - 半径, y),
    #          ("A", 半径, 半径, 0, 1, 1 if 顺时针 else 0, 半径 + x, y),
    #          ("A", 半径, 半径, 0, 1, 1 if 顺时针 else 0, x - 半径, y)
    #          ]
    #
    # if 旋转角度 != 0:
    #     弧度 = math.radians(旋转角度)
    #     x0, y0 = x, y
    #     for i in range(len(点路径列表)):
    #         操作, *参数 = 点路径列表[i]
    #         if 操作 == "M":
    #             x, y = 参数
    #             x1 = math.cos(弧度) * (x - x0) - math.sin(弧度) * (y - y0) + x0
    #             y1 = math.sin(弧度) * (x - x0) + math.cos(弧度) * (y - y0) + y0
    #             点路径列表[i] = ("M", x1, y1)
    #         elif 操作 == "A":
    #             rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y = 参数
    #             x1 = math.cos(弧度) * (x - x0) - math.sin(弧度) * (y - y0) + x0
    #             y1 = math.sin(弧度) * (x - x0) + math.cos(弧度) * (y - y0) + y0
    #             点路径列表[i] = ("A", rx, ry, x_axis_rotation + 旋转角度, large_arc_flag, sweep_flag, x1, y1)
    #
    # return 点路径列表


def N边形路径(x, y, 半径大小, n=5, 旋转角度=0):
    点路径列表 = []
    for i in range(n):
        angle = i * 2 * math.pi / n - math.pi / 180 * (90 - 旋转角度)
        x_ = x + 半径大小 * math.cos(angle)
        y_ = y + 半径大小 * math.sin(angle)
        if len(点路径列表) == 0:
            点路径列表.append(("M", x_, y_))
        else:
            点路径列表.append(("L", x_, y_))
    点路径列表.append(("z",))
    return 点路径列表


def 菱型路径(x, y, 半径):
    if isinstance(半径, tuple):
        半径X, 半径Y = 半径
    else:
        半径X, 半径Y = 半径, 半径
    点路径列表 = []
    点路径列表.append(("M", x, y - 半径Y))
    点路径列表.append(("L", x - 半径X, y))
    点路径列表.append(("L", x, y + 半径Y))
    点路径列表.append(("L", x + 半径X, y))
    点路径列表.append(("z",))
    return 点路径列表


def 爱心路径(x, y, 半径大小):
    d = 0.8525
    点路径列表 = []
    半径大小调整 = 半径大小 * d
    点路径列表.append(("M", x, y - 半径大小调整 * d))
    点路径列表.append(("A", 半径大小调整 / 2, 半径大小调整 / 2, 0, 0, 0, x - 半径大小调整, y))
    点路径列表.append(("L", x, y + 半径大小调整))
    点路径列表.append(("L", x + 半径大小调整, y))
    点路径列表.append(("A", 半径大小调整 / 2, 半径大小调整 / 2, 0, 0, 0, x, y - 半径大小调整 * d))
    点路径列表.append(("z",))
    return 点路径列表


def 五边形绘画路径(cx, cy, 半径大小, 旋转角度=0, 闭合路径=是):
    点路径列表 = []
    for i in range(5):
        角度 = math.radians(72 * i - 90 + 旋转角度)
        if i == 0:
            点路径列表.append(("M", cx + 半径大小 * math.cos(角度), cy + 半径大小 * math.sin(角度)))
        else:
            点路径列表.append(("L", cx + 半径大小 * math.cos(角度), cy + 半径大小 * math.sin(角度)))
    if 闭合路径:
        点路径列表.append(("z",))
    return 点路径列表


def 五角星绘画路径(x, y, 半径大小, 旋转角度=0):
    """
    平常绘画五角星的路径，线条在五角星的内部
    :param x:
    :param y:
    :param 半径大小:
    :param 旋转角度:
    :return:
    """
    点路径列表 = 五边形绘画路径(x, y, 半径大小, 旋转角度, 闭合路径=否)
    p1, p2, p3, p4, p5 = 点路径列表[0][1:], 点路径列表[1][1:], 点路径列表[2][1:], 点路径列表[3][1:], 点路径列表[4][1:]
    点路径列表 = [
        ("M", p1[0], p1[1]),
        ("L", p3[0], p3[1]),
        ("L", p5[0], p5[1]),
        ("L", p2[0], p2[1]),
        ("L", p4[0], p4[1]),
        ("L", p1[0], p1[1]),
    ]
    return 点路径列表


def N角星路径(x, y, 半径大小, n=5, 内角点占比=0.382, 旋转角度=0):
    """
    N角星外部边缘的路径
    :param x: 中心X位置
    :param y: 中心Y位置
    :param 半径大小:
    :param n: 默认=5，为五角星
    :param 内角点占比:
            N角星的内角点距中心点的距离除以大小的比例。默认 0.382，
            注意：虽然是内角点，但是如果值大于1，则该点成为了外角点。
            如果等于1，则形状为 “2 x N 边形”
    :param 旋转角度:
    :return:
    """
    点路径列表 = []
    for i in range(n * 2):
        angle = i * 2 * math.pi / (n * 2) - math.pi / 180 * (90 - 旋转角度)
        if i % 2 == 0:
            x_ = x + 半径大小 * math.cos(angle)
            y_ = y + 半径大小 * math.sin(angle)
        else:
            x_ = x + 半径大小 * 内角点占比 * math.cos(angle)
            y_ = y + 半径大小 * 内角点占比 * math.sin(angle)
        if len(点路径列表) == 0:
            点路径列表.append(("M", x_, y_))
        else:
            点路径列表.append(("L", x_, y_))
    点路径列表.append(("z",))
    return 点路径列表


def 四角星路径(x, y, 半径大小, 旋转角度=0):
    """
    四角星外部边缘的路径
    :param x: 中心X位置
    :param y: 中心Y位置
    :param 半径大小:
    :param 旋转角度:
    :return:
    """
    return N角星路径(x, y, 半径大小, n=4, 旋转角度=旋转角度)


def 五角星路径(x, y, 半径大小, 旋转角度=0):
    """
    五角星外部边缘的路径
    :param x: 中心X位置
    :param y: 中心Y位置
    :param 半径大小:
    :param 旋转角度:
    :return:
    """
    return N角星路径(x, y, 半径大小, n=5, 旋转角度=旋转角度)


def 六角星路径(x, y, 半径大小, 旋转角度=0):
    """
    六角星外部边缘的路径
    :param x: 中心X位置
    :param y: 中心Y位置
    :param 半径大小:
    :param 旋转角度:
    :return:
    """
    return N角星路径(x, y, 半径大小, n=6, 旋转角度=旋转角度)


def 版权印章路径():
    return [('移动', 78.43, 26.63),
            ('曲线', 87.03, 21.8, 106.97, 10.9, 134.97, 10.53),
            ('曲线', 148.3, 10.37, 173.57, 10.07, 195.9, 28.1),
            ('曲线', 200.5, 31.83, 213.73, 45.4, 219.67, 65.9),
            ('曲线', 224.97, 84.1, 221.97, 93.93, 223.17, 113.43),
            ('曲线', 226.93, 137.1, 228.87, 136.8, 228.67, 153.7),
            ('曲线', 228.47, 172.4, 228.1, 184.5, 232.43, 192.83),
            ('曲线', 235.6, 196.8, 236.97, 199.1, 240.33, 204.57),
            ('曲线', 244.3, 210.97, 247.2, 220.93, 245.3, 236.7),
            ('曲线', 244.93, 259.4, 245.77, 237.5, 244.6, 281.13),
            ('曲线', 239.7, 304.8, 244.93, 281.33, 239.63, 305.0),
            ('曲线', 229.47, 327.8, 239.97, 305.0, 228.83, 328.17),
            ('曲线', 222.23, 341.97, 213.73, 349.6, 202.67, 356.1),
            ('曲线', 182.87, 367.83, 164.3, 368.6, 144.2, 369.43),
            ('曲线', 119.3, 370.47, 101.33, 367.9, 77.93, 359.57),
            ('曲线', 67.0, 353.2, 62.7, 349.37, 48.2, 341.8),
            ('曲线', 38.5, 338.4, 34.9, 336.87, 29.7, 330.37),
            ('曲线', 26.43, 326.27, 22.0, 322.67, 21.43, 312.23),
            ('曲线', 15.37, 277.9, 23.83, 271.37, 20.3, 253.73),
            ('曲线', 19.17, 251.33, 17.33, 241.73, 15.87, 237.5),
            ('曲线', 13.5, 230.63, 13.77, 224.27, 14.0, 211.13),
            ('曲线', 14.3, 195.2, 14.1, 194.27, 14.37, 177.13),
            ('曲线', 14.47, 170.07, 14.27, 166.03, 14.1, 160.8),
            ('曲线', 13.53, 143.87, 15.13, 143.87, 17.53, 139.5),
            ('曲线', 21.9, 131.57, 22.23, 135.2, 25.9, 127.23),
            ('曲线', 28.37, 121.83, 31.53, 115.03, 31.23, 106.53),
            ('曲线', 31.0, 99.6, 32.6, 96.93, 39.9, 77.93),
            ('曲线', 52.53, 49.57, 53.43, 50.97, 57.27, 46.27),
            ('曲线', 64.3, 37.8, 70.37, 31.17, 78.43, 26.63),
            ('结束',)]


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 8), dpi=400)
    粘贴区域线集合 = [[(0, 0), (100, 0)]]
    pts = 计算粘贴区域点(粘贴区域线集合, 距离=10, 角度=33)
    x, y = zip(*pts[0])
    plt.plot(x, y, 'b-')

    # print(点2, 点3)

    # 设置坐标轴范围，确保五边形完全可见
    plt.xlim(-100, 210)
    plt.ylim(-100, 297)
    # 设置坐标轴为等比例，这样五边形看起来就不会是椭圆形
    plt.gca().set_aspect('equal', adjustable='box')
    # 显示图形
    plt.show()
