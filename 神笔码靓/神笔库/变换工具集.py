# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================


class 变换工具集:

    def __init__(self, 高清图=None):
        from 神笔码靓.神笔库 import 神笔绘图板
        self.高清图: 神笔绘图板 = 高清图
        self.dwg = 高清图.dwg

    def 矩阵(self, SVG元素, a, b, c, d, e, f):
        """
matrix(sx,0,0,sy,TranslateX,TranslateY)
matrix(cos(a), sin(a), -sin(a), cos(a), TranslateX,TranslateY)
matrix(1, skewY=tan(a), skewX=tan(a), 1, TranslateX,TranslateY)

对应矩阵：
a  c  e
b  d  f
0  0  1

1.Translate(tx, ty)
    矩阵：
    1  0  tx
    0  1  ty
    0  0  1
    写法：matrix(1,0,0,1,tx,ty)

2.Scale(sx, sy)
    矩阵：
    sx  0  0
    0  sy  0
    0   0  1
    写法：matrix(sx,0,0,sy,0,0)

3.Rotate(a)
    矩阵：
    cos(a)  -sin(a)  0
    sin(a)   cos(a)  0
    0        0       1
    写法：matrix(cos(a), sin(a), -sin(a), cos(a), 0, 0)

  3+.Rotate(a, cx, cy)
    cos(a)  -sin(a)  -cx × cos(a) + cy × sin(a) + cx
    sin(a)   cos(a)  -cx × sin(a) - cy × cos(a) + cy
    0        0       1
    写法：
    matrix(cos(a), sin(a), -sin(a), cos(a), -cx × cos(a) + cy × sin(a) + cx + tx, -cx × sin(a) - cy × cos(a) + cy + ty)

4.skew(skewX, skewY)
  4.1 skewX
    矩阵：
    1  tan(a)  0
    0     1      0
    0     0      1
    写法：matrix(1, 0, tan(a), 1, 0, 0)

  4.2 skewY
    矩阵：
    1         0     0
    tan(a)    1     0
    0         0     1
    写法：matrix(1, tan(a), 0, 1, 0, 0)

5.如果你的使用包含旋转，缩放，平移等多种
    例如：
    <g transform="translate(20, 50) scale(1, 1) rotate(-30 10 25)">
    对应矩阵：
    cos(a)  -sin(a)  -cx × cos(a) + cy × sin(a) + cx + tx
    sin(a)   cos(a)  -cx × sin(a) - cy × cos(a) + cy + ty
    0        0       1
    此处scale为1，因此不考虑。写法为：
    matrix(cos(a), sin(a), -sin(a), cos(a), -cx × cos(a) + cy × sin(a) + cx + tx, -cx × sin(a) - cy × cos(a) + cy + ty)
    结果为： matrix(0.866, -0.5 0.5 0.866 8.84 58.35).

        :param SVG元素:
        :param a:
        :param b:
        :param c:
        :param d:
        :param e:
        :param f:
        :return:
        """
        SVG元素.matrix(a, b, c, d, e, f)

    def 缩放(self, SVG元素, 缩放X, 缩放Y=None):
        # def scale(self, sx, sy=None):
        SVG元素.scale(缩放X, 缩放Y)

    def 水平翻转(self, SVG元素):
        SVG元素.scale((-1, 1))

    def 垂直翻转(self, SVG元素):
        SVG元素.scale((1, -1))

    def 平移(self, SVG元素, 位移X, 位移Y=None):
        # def translate(self, tx, ty=None):
        SVG元素.translate(位移X, 位移Y)

    def 倾斜X(self, SVG元素, 倾斜角度):
        SVG元素.skewX(倾斜角度)

    def 倾斜Y(self, SVG元素, 倾斜角度):
        SVG元素.skewY(倾斜角度)

    def 旋转(self, SVG元素, 旋转角度, 旋转中心点=None):
        SVG元素.rotate(旋转角度, 旋转中心点)
