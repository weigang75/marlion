# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-30
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================

from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *

import math

import math


class 坐标点:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"x:{self.x},y:{self.y}"

    def __str__(self):
        return self.__repr__()


def 计算圆角(p1, p2, p3, p4, 半径):
    # p2 到 p1 向量
    v1 = {'x': p1.x - p2.x, 'y': p1.y - p2.y}
    # p2 到 p3 的向量
    v2 = {'x': p4.x - p3.x, 'y': p4.y - p3.y}

    # 求叉积
    cp = v1['x'] * v2['y'] - v2['x'] * v1['y']
    if cp == 0:
        # 平行，无法生成圆角
        return None

    # 计算法向量
    if cp < 0:
        法向量1 = {'x': v1['y'], 'y': -v1['x']}
        法向量2 = {'x': -v2['y'], 'y': v2['x']}
    else:
        法向量1 = {'x': -v1['y'], 'y': v1['x']}
        法向量2 = {'x': v2['y'], 'y': -v2['x']}

    # 沿法向量偏移半径长度的 line1
    t1 = 半径 / 计算距离(p1, p2)
    d1 = {'x': 法向量1['x'] * t1, 'y': 法向量1['y'] * t1}
    偏移线1 = [
        坐标点(p1.x + d1['x'], p1.y + d1['y']),
        坐标点(p2.x + d1['x'], p2.y + d1['y']),
    ]

    # 沿法向量偏移半径长度的 line2
    t2 = 半径 / 计算距离(p3, p4)
    d2 = {'x': 法向量2['x'] * t2, 'y': 法向量2['y'] * t2}
    偏移线2 = [
        坐标点(p3.x + d2['x'], p3.y + d2['y']),
        坐标点(p4.x + d2['x'], p4.y + d2['y']),
    ]

    # 求偏移后两条直线的交点，这个交点就是圆心
    圆心 = 计算直线交点(偏移线1[0], 偏移线1[1], 偏移线2[0], 偏移线2[1])

    # 求圆心到两条线的垂足
    起点 = 最近点在线(p1, p2, 圆心, True)['point']
    终点 = 最近点在线(p3, p4, 圆心, True)['point']

    # 圆心到垂足的弧度
    基准角度 = {'x': 1, 'y': 0}
    起始角度 = 计算扫角(基准角度, {'x': 起点.x - 圆心.x, 'y': 起点.y - 圆心.y})
    终止角度 = 计算扫角(基准角度, {'x': 终点.x - 圆心.x, 'y': 终点.y - 圆心.y})

    return {
        '偏移线1': 偏移线1,
        '偏移线2': 偏移线2,
        '圆心': 圆心,
        '起点': 起点,
        '终点': 终点,
        '起始角度': 起始角度,
        '终止角度': 终止角度,
        '角度方向': cp < 0,  # 正 -> 顺时针
    }


def 计算距离(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx * dx + dy * dy)


def 计算直线交点(p1, p2, p3, p4):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    a = y2 - y1
    b = x1 - x2
    c = x1 * y2 - x2 * y1
    d = y4 - y3
    e = x3 - x4
    f = x3 * y4 - x4 * y3

    # 计算分母
    分母 = a * e - b * d
    if abs(分母) < 1e-9:
        return None  # 平行

    px = (c * e - f * b) / 分母
    py = (a * f - c * d) / 分母
    return 坐标点(px, py)


def 最近点在线(p1, p2, p, can_outside=False):
    if p1.x == p2.x and p1.y == p2.y:
        return {
            't': 0,
            'd': 计算距离(p1, p),
            'point': 坐标点(p1.x, p1.y),
        }

    dx = p2.x - p1.x
    dy = p2.y - p1.y
    t = ((p.x - p1.x) * dx + (p.y - p1.y) * dy) / (dx * dx + dy * dy)

    if not can_outside:
        t = max(0, min(1, t))

    最近点 = 坐标点(p1.x + t * dx, p1.y + t * dy)
    return {
        't': t,
        'd': 计算距离(p, 最近点),
        'point': 最近点,
    }


def 计算扫角(a, b):
    dot = a['x'] * b['x'] + a['y'] * b['y']
    d = math.sqrt(a['x'] ** 2 + a['y'] ** 2) * math.sqrt(b['x'] ** 2 + b['y'] ** 2)
    cos_theta = dot / d

    # 修正精度问题导致的 cos_theta 超出 [-1, 1] 的范围
    cos_theta = max(-1, min(1, cos_theta))
    theta = math.acos(cos_theta)

    # 通过叉积判断方向
    if a['x'] * b['y'] - a['y'] * b['x'] < 0:
        theta = -theta

    return theta


def 计算倒圆角切点坐标(点1, 交点, 点2, 倒角半径):
    p1 = 坐标点(点1[0], 点1[1])
    p2 = 坐标点(交点[0], 交点[1])
    p3 = p2
    p4 = 坐标点(点2[0], 点2[1])
    result = 计算圆角(p1, p2, p3, p4, 倒角半径)
    起点 = result["起点"]
    终点 = result["终点"]
    角度方向 = result["角度方向"]

    return 起点, 终点, 角度方向


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    p1 = 坐标点(30, 140)
    p2 = 坐标点(50, 0)
    p3 = 坐标点(50, 0)
    p4 = 坐标点(200, 110)

    plt.figure(figsize=(6, 8), dpi=400)

    result = 计算圆角(p1, p2, p3, p4, 30)
    offsetLine1 = result["偏移线1"]
    offsetLine2 = result["偏移线2"]
    circleCenter = result["圆心"]
    start = result["起点"]
    end = result["终点"]
    startAngle = result["起始角度"]
    endAngle = result["终止角度"]
    angleDir = result["角度方向"]

    print(result)

    pts = [(p.x, p.y) for p in [p1, p2, p3, p4]]
    x, y = zip(*pts)
    plt.plot(x, y, 'b-')

    pts = [(p.x, p.y) for p in offsetLine1]
    x, y = zip(*pts)
    plt.plot(x, y, 'r-')

    pts = [(p.x, p.y) for p in offsetLine2]
    x, y = zip(*pts)
    plt.plot(x, y, 'r-')

    plt.scatter([circleCenter.x, start.x, end.x], [circleCenter.y, start.y, end.y])

    # print(点2, 点3)

    # 设置坐标轴范围，确保五边形完全可见
    plt.xlim(-100, 210)
    plt.ylim(-100, 297)
    # 设置坐标轴为等比例，这样五边形看起来就不会是椭圆形
    plt.gca().set_aspect('equal', adjustable='box')
    # 显示图形
    plt.show()
