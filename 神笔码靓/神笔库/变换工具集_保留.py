# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import re

from 神笔码靓.神笔库 import 类型转换工具集
from dataclasses import dataclass

from 神笔码靓.神笔库.通用工具集 import 为空


@dataclass
class Scale:
    """
    scale(<x> [<y>]) 变换函数指定一个按 x 和 y 进行缩放的操作。如果没有提供 y，那么假定其等同于 x。
    """
    x: [float, int] = 1
    y: [float, int] = 1

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.x == 1 and (self.y is None or self.y == 1):
            return ""
        values = f"scale({self.x} "
        if self.y is not None:
            values += f"{self.y} "
        return values.strip(" ") + ") "


@dataclass
class Matrix:
    """
    matrix(<a> <b> <c> <d> <e> <f>) 变换函数以六个值的变换矩阵形式指定变换。matrix(a,b,c,d,e,f) 等同于应用变换矩阵：
    """
    a: [float, int] = None
    b: [float, int] = None
    c: [float, int] = None
    d: [float, int] = None
    e: [float, int] = None
    f: [float, int] = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        values = f"matrix({self.a} {self.b} {self.c} {self.d} {self.e} {self.f}) "
        return values


@dataclass
class Translate:
    """
    translate(<x> [<y>]) 变换函数将对象移动 x 和 y。如果没有提供 y，那么其默认为 0
    """
    x: [float, int] = None
    y: [float, int] = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        values = f"translate({self.x} "
        if self.y is not None:
            values += f"{self.y} "
        return values.strip(" ") + ") "


@dataclass
class Rotate:
    """
    rotate(<a> [<x> <y>]) 变换函数指定一个围绕给定点旋转 a 度的操作。如果没有提供可选参数 x 和 y，那么默认绕当前用户坐标系的原点旋转。否则，就以 (x,y) 为原点进行旋转。
    """
    a: [float, int] = 0
    x: [float, int] = None
    y: [float, int] = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.a == 0:
            return ""
        values = f"rotate({self.a} "
        if self.x is not None:
            values += f"{self.x} "
        if self.y is not None:
            values += f"{self.y} "
        return values.strip(" ") + ") "


@dataclass
class SkewX:
    """
    skewX(<a>) 变换函数指定沿 x 轴倾斜 a 度的倾斜变换。
    """
    a: [float, int] = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"skewX({self.a}) "


@dataclass
class SkewY:
    """
    skewY(<a>) 变换函数指定了沿 y 轴倾斜 a 度的倾斜变换。
    """
    a: [float, int] = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"skewY({self.a}) "


@dataclass
class Transform:
    """
    # https://developer.mozilla.org/zh-CN/docs/Web/SVG/Attribute/transform
    """
    scale: Scale = None
    matrix: Matrix = None
    translate: Translate = None
    rotate: Rotate = None
    skewX: SkewX = None
    skewY: SkewY = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        transform_str = ""
        if self.scale is not None:
            transform_str += str(self.scale)
        if self.translate is not None:
            transform_str += str(self.translate)
        if self.rotate is not None:
            transform_str += str(self.rotate)
        if self.skewX is not None:
            transform_str += str(self.skewX)
        if self.skewY is not None:
            transform_str += str(self.skewY)
        if self.matrix is not None:
            transform_str += str(self.matrix)
        return transform_str


class 变换工具集:

    def __init__(self, 高清图=None):
        from 神笔码靓.神笔库 import 神笔绘图板
        self.高清图: 神笔绘图板 = 高清图
        # self.dwg = 高清图.dwg

    def _get_values_list(self, value_str):
        if 为空(value_str):
            return []

        values = value_str.replace(" ", ",").replace(",,", ",").split(",")
        return values

    def _set_transform(self, SVG元素, transform):
        # TODO: 暂时不使用，使用 _append_transform 进行替代
        transform_str = str(transform)
        SVG元素["transform"] = transform_str.strip(" ")

    def _append_transform(self, SVG元素, transform):
        if "transform" in SVG元素.attribs:
            transform_str = SVG元素["transform"]
        else:
            transform_str = ""

        new_transform = transform_str.strip(" ") + " " + str(transform)
        SVG元素["transform"] = new_transform.strip(" ")

    def _get_transform(self, SVG元素):
        """

        :param SVG元素:
        :return:
        """

        return Transform()
        # TODO: 暂时不使用以下代码，但是需要保留
        # if "transform" in SVG元素:
        if "transform" in SVG元素.attribs:
            transform_str = SVG元素["transform"]
        else:
            transform_str = ""

        scale_matches = re.findall(r'scale\((.*?)\)', transform_str)
        translate_matches = re.findall(r'translate\((.*?)\)', transform_str)
        rotate_matches = re.findall(r'rotate\((.*?)\)', transform_str)
        skewx_matches = re.findall(r'skewX\((.*?)\)', transform_str)
        skewy_matches = re.findall(r'skewY\((.*?)\)', transform_str)
        matrix_matches = re.findall(r'matrix\((.*?)\)', transform_str)

        transform = Transform()

        if translate_matches:
            translate_values = self._get_values_list(translate_matches[0])
            if 2 >= len(translate_values) > 0:
                translate = Translate()
                translate.x = 类型转换工具集.转浮点型(translate_values[0])
                if len(translate_values) == 2:
                    translate.y = 类型转换工具集.转浮点型(translate_values[1])

                transform.translate = translate
            else:
                raise Exception("translate 的值错误格式")

        if rotate_matches:
            rotate_values = self._get_values_list(rotate_matches[0])
            if 4 > len(rotate_values) > 0:
                rotate = Rotate()
                rotate.a = 类型转换工具集.转浮点型(rotate_values[0])
                if len(rotate_values) > 1:
                    rotate.x = 类型转换工具集.转浮点型(rotate_values[1])
                if len(rotate_values) > 2:
                    rotate.y = 类型转换工具集.转浮点型(rotate_values[2])

                transform.rotate = rotate
            else:
                raise Exception("rotate 的值错误格式")

        if scale_matches:
            scale_values = self._get_values_list(scale_matches[0])
            if 3 > len(scale_values) > 0:
                scale = Scale()
                scale.x = 类型转换工具集.转浮点型(scale_values[0])
                if len(scale_values) == 2:
                    scale.y = 类型转换工具集.转浮点型(scale_values[1])

                transform.scale = scale
            else:
                raise Exception("scale 的值错误格式")

        if skewx_matches:
            skewx_value = self._get_values_list(skewx_matches[0])
            if len(skewx_value) == 1:
                skewx = SkewX()
                skewx.a = 类型转换工具集.转浮点型(skewx_value[0])
            else:
                raise Exception("skewx 的值错误格式")

            transform.skewX = skewx

        if skewy_matches:
            skewy_value = self._get_values_list(skewy_matches[0])
            if len(skewy_value) == 1:
                skewy = SkewY()
                skewy.a = 类型转换工具集.转浮点型(skewy_value[0])
            else:
                raise Exception("skewy 的值错误格式")

            transform.skewY = skewy

        if matrix_matches:
            matrix_values = self._get_values_list(matrix_matches[0])
            if len(matrix_values) == 6:
                matrix = Matrix()
                matrix.a = 类型转换工具集.转浮点型(matrix_values[0])
                matrix.b = 类型转换工具集.转浮点型(matrix_values[1])
                matrix.c = 类型转换工具集.转浮点型(matrix_values[2])
                matrix.d = 类型转换工具集.转浮点型(matrix_values[3])
                matrix.e = 类型转换工具集.转浮点型(matrix_values[4])
                matrix.f = 类型转换工具集.转浮点型(matrix_values[5])
            else:
                raise Exception("skewx 的值错误格式")

            transform.matrix = matrix

        return transform

    def 矩阵(self, SVG元素, a, b, c, d, e, f):
        SVG元素.matrix(a, b, c, d, e, f)

        # transform = self._get_transform(SVG元素)
        # if transform.matrix is None:
        #     transform.matrix = Matrix()
        #
        # transform.matrix.a = a
        # transform.matrix.b = b
        # transform.matrix.c = c
        # transform.matrix.d = d
        # transform.matrix.e = e
        # transform.matrix.f = f
        #
        # self._append_transform(SVG元素, transform.matrix)

    def 缩放(self, SVG元素, 缩放比例):

        SVG元素.scale(缩放比例)

        # transform = self._get_transform(SVG元素)
        # if transform.scale is None:
        #     transform.scale = Scale()
        #
        # if isinstance(缩放比例, tuple):
        #     scale_x, scale_y = 缩放比例
        # else:
        #     scale_x, scale_y = 缩放比例, 缩放比例
        # transform.scale.x, transform.scale.y = \
        #     scale_x * (transform.scale.x / abs(transform.scale.x)), \
        #     scale_y * (transform.scale.y / abs(transform.scale.y))
        #
        # self._append_transform(SVG元素, transform.scale)

    def 垂直翻转(self, SVG元素):
        SVG元素.scale((-1, 1))

        # transform = self._get_transform(SVG元素)
        # if transform.scale is None:
        #     transform.scale = Scale()
        #
        # transform.scale.x = -transform.scale.x
        #
        # self._append_transform(SVG元素, transform.scale)

    def 水平翻转(self, SVG元素):
        SVG元素.scale((1, -1))
        # transform = self._get_transform(SVG元素)
        # if transform.scale is None:
        #     transform.scale = Scale()
        #
        # transform.scale.y = -transform.scale.y
        #
        # self._append_transform(SVG元素, transform.scale)

    def 平移(self, SVG元素, 位移):

        SVG元素.translate(位移)

        # transform = self._get_transform(SVG元素)
        # if transform.translate is None:
        #     transform.translate = Translate()
        #
        # if isinstance(位移, tuple):
        #     translate_x, translate_y = 位移
        # else:
        #     translate_x, translate_y = 位移, 0
        #
        # transform.translate.x = translate_x
        # if translate_y == 0:
        #     transform.translate.y = None
        # else:
        #     transform.translate.y = translate_y
        #
        # self._append_transform(SVG元素, transform.translate)

    def 倾斜X(self, SVG元素, 倾斜角度):
        if 倾斜角度 == 0:
            return

        SVG元素.skewX(倾斜角度)

        # transform = self._get_transform(SVG元素)
        # if transform.skewX is None:
        #     transform.skewX = SkewX()
        #
        # transform.skewX.a = 倾斜角度
        # self._append_transform(SVG元素, transform.skewX)

    def 倾斜Y(self, SVG元素, 倾斜角度):
        if 倾斜角度 == 0:
            return

        SVG元素.skewY(倾斜角度)

        # transform = self._get_transform(SVG元素)
        # if transform.skewY is None:
        #     transform.skewY = SkewY()
        #
        # transform.skewY.a = 倾斜角度
        # self._append_transform(SVG元素, transform.skewY)

    def 旋转(self, SVG元素, 旋转角度, 旋转中心点=None):
        if 旋转角度 == 0:
            return
        # if 旋转中心点 is None:
        #     pass
        #     # (min_x, min_y), (max_x, max_y) = 神笔绘图板工具.获取元素的坐标信息(SVG元素)
        #     # cx, cy = (min_x + max_x) / 2, (min_y + max_y) / 2
        # else:
        # cx, cy = 旋转中心点

        SVG元素.rotate(旋转角度, 旋转中心点)

        # transform = self._get_transform(SVG元素)
        # if transform.rotate is None:
        #     transform.rotate = Rotate()
        #
        # transform.rotate.a = 旋转角度
        #
        # if 旋转中心点 is not None:
        #     transform.rotate.x = cx
        #     transform.rotate.y = cy
        #
        # self._append_transform(SVG元素, transform.rotate)


if __name__ == '__main__':
    SVG元素 = {}
    SVG元素["transform"] = "translate(10,20) rotate(45) scale(2) skewX(30) skewY(30) matrix(1,0,0,1,50,50)"

    变换工具集().缩放(SVG元素, (1, 1))
    变换工具集().水平翻转(SVG元素)
    变换工具集().垂直翻转(SVG元素)
    print(变换工具集()._get_transform(SVG元素))
