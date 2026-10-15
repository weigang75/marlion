# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os

from svgpathtools import parse_path, Path, Line, CubicBezier, QuadraticBezier, Arc
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely.ops import unary_union
from shapely.validation import make_valid
import math
from fontTools.ttLib import TTFont
from 神笔码靓.神笔库 import 五角星绘画路径, 五角星路径
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *


def 修正SvgPath(d):
    d = d.replace("-", " -")
    # 匹配连续的数字和小数点
    pattern = r'(-?\d+\.\d+|\d+\.)'
    # 用空格替换匹配到的内容
    formatted_d = re.sub(pattern, r'\1 ', d)
    # if new_d == "M43.1 50.6c-5.2 0-9.6-3-9.6-6.5s4.4-6.5 9.6-6.5c5.2 0 9.6 3 9.6 6.5c-.1 3.5-4.4 6.5-9.6 6.5":
    #     return new_d.replace("-", " -") #"M43.1 50.6c -5.2 0 -9.6 -3 -9.6 -6.5s4.4 -6.5 9.6 -6.5c5.2 0 9.6 3 9.6 6.5c -.1 3.5 -4.4 6.5 -9.6 6.5"
    return "M43.1 50.6 L600 500 L300 1000 z"


def 图片轮廓转路径(图片文件路径, 阈值1=30, 阈值2=100):
    import cv2
    import shutil

    temp_file = "_temp.jpg"
    if os.path.exists(temp_file):
        os.remove(temp_file)
    # 复制文件
    shutil.copy(图片文件路径, temp_file)

    image = cv2.imread(temp_file)  # 读取图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将图像转换为灰度图
    inverted_gray_image = cv2.bitwise_not(gray_image)  # 取反灰度图像
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)  # 高斯模糊
    inverted_blurred_image = cv2.bitwise_not(blurred_image)  # 取反模糊图像
    pencil_sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

    # 转换为灰度图像
    gray = pencil_sketch_image  # cv2.cvtColor(pencil_sketch_image, cv2.COLOR_BGR2GRAY)

    # 应用Canny边缘检测器
    # edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    edges = cv2.Canny(gray, threshold1=阈值1, threshold2=阈值2)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if os.path.exists(temp_file):
        os.remove(temp_file)
    # shutil.rmtree(temp_file)
    路径集合 = []
    for contour in contours:
        路径 = []
        for i, d in enumerate(contour):
            x, y = d[0]
            if i == 0:
                路径.append(("移动", x, y))
            else:
                路径.append(("直线", x, y))
            # print( x, y)
        # 神笔.连线(路径点列表=路径)
        路径集合.append(路径)
    return 路径集合


class 字体文本路径工具:
    fonts_cache = {}

    def __init__(self, 高清图, 字体, 字体大小, 字符间距=None):
        self.字体 = 字体
        self.高清图: 神笔绘图板 = 高清图
        self.debug = False
        # self.debug = True
        if 字体 in 字体文本路径工具.fonts_cache:
            self.font, self.uninames, self.char_dict = 字体文本路径工具.fonts_cache[字体]
        else:
            self.font = TTFont(字体)

            # self.uninames = self.font.getGlyphNames()[1:-1]  # 获取所有字符的unicode编码
            self.uninames = self.font.getGlyphNames()
            self.char_dict = {}
            for u in self.uninames:
                try:
                    self.char_dict[u] = u
                    uchar = self.Unicode转字符(u)
                    self.char_dict[uchar] = u
                except ValueError as ve:
                    # ValueError: chr() arg not in range(0x110000)
                    pass
                except OverflowError:
                    pass

            字体文本路径工具.fonts_cache[字体] = self.font, self.uninames, self.char_dict

        self.字体标准宽度 = 1000
        self._字体大小 = 字体大小
        if 字符间距 is None:
            字符间距 = 0
        if isinstance(字符间距, str):
            if 字符间距.endswith("%"):  # "50%"
                字符间距 = float(字符间距[:-1]) / 100 * 字体大小

        self._字符间距 = 字符间距

        if self.debug:
            # 获取各节点名称，返回为列表：
            print("获取各节点名称", self.font.keys())

            # 获取getGlyphOrder节点的name值，返回为列表：
            print("获取getGlyphOrder节点", self.font.getGlyphOrder())
            print("获取getGlyphOrder节点的name值", self.font.getGlyphNames())

            # 获取cmap节点code与name值映射, 返回为字典：
            print("获取cmap节点code与name值映射", self.font.getBestCmap())
        self.平移x, self.平移y = 0, 0

    def 平移(self, 平移x, 平移y):
        self.平移x, self.平移y = 平移x, 平移y

    @staticmethod
    def Unicode转字符(unicode_value):
        if isinstance(unicode_value, str):
            if unicode_value.startswith("uni"):
                unicode_value_ = unicode_value[3:]
            elif unicode_value.startswith("char"):
                unicode_value_ = unicode_value[4:]
            elif unicode_value.startswith("u") and len(unicode_value) > 1:
                unicode_value_ = unicode_value[1:]
            else:
                unicode_value_ = unicode_value
            try:
                unicode_value_ = int(unicode_value_, 16)
            except Exception as e:
                return unicode_value
        else:
            print(unicode_value)

        c = chr(unicode_value_)
        if c.startswith(r"\U"):
            pass

        return c

    def 生成字符串路径(self, 字符串, 纵向=否, 文字位置微调=None):
        paths = []
        if 文字位置微调 is None:
            文字位置微调 = {}
        for 索引, 字符 in enumerate(字符串):
            微调 = 文字位置微调.get(索引, None)
            path = self.生成字符路径(字符, 索引, 纵向)
            if path is None:
                continue
            if 微调:
                path = self.文字路径微调(path, 微调)
            paths.append(path)

        return paths

    def 文字路径微调(self, 路径集, 微调):
        x, y = 微调
        # MVQHL
        微调后路径集合 = []
        for 点命令 in 路径集:
            if 点命令[0] in ["M", "L"]:
                微调后路径集合.append((点命令[0], 点命令[1] + x, 点命令[2] + y))
            elif 点命令[0] in ["H"]:
                微调后路径集合.append((点命令[0], 点命令[1] + x))
            elif 点命令[0] in ["V"]:
                微调后路径集合.append((点命令[0], 点命令[1] + y))
            elif 点命令[0] in ["Q"]:
                微调后路径集合.append((点命令[0], 点命令[1] + x, 点命令[2] + y, 点命令[3] + x, 点命令[4] + y))
            elif 点命令[0] in ["Z", "z"]:
                微调后路径集合.append((点命令[0],))
            else:
                raise Exception(f"文字路径微调未处理：{点命令[0]}")

        return 微调后路径集合

    def _try_to_float(self, value):
        try:
            value = float(value)
        except Exception as e:
            return value

        return value

    def 字体范围(self):
        head = self.font['head']
        xMin, yMin, xMax, yMax = head.xMin, head.yMin, head.xMax, head.yMax

        # width, ascender, descender = head.width, self.font['OS/2'].usWinAscent, -self.font[
        #     'OS/2'].usWinDescent  # 获取字形的宽度和上沿以及下沿
        # height = ascender - descender  # 利用上沿和下沿计算字形高度
        scale = self._缩放大小()
        return scale * (xMax - xMin), scale * (yMax - yMin)

    def _缩放大小(self):
        if hasattr(self, "_scale_value"):
            return getattr(self, "_scale_value")

        head = self.font['head']
        xMin, yMin, xMax, yMax = head.xMin, head.yMin, head.xMax, head.yMax
        width = xMax - xMin
        height = yMax - yMin
        scale = self.字体标准宽度 / width * self._字体大小 / 913
        setattr(self, "_scale_value", scale)
        return scale

    def 生成字符路径(self, 字符, 索引位置, 纵向=否, 偏移X=0, 偏移Y=0):
        if 字符 not in self.char_dict:
            return None

        p = self.char_dict[字符]
        if self.debug:
            # 获取GlyphOrder节点GlyphID的id信息, 返回int型：
            print("GlyphOrder节点GlyphID的id信息", self.font.getGlyphID(p))

        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.boundsPen import BoundsPen
        head = self.font['head']
        glyphset = self.font.getGlyphSet()[p]
        glyph = self.font['glyf'][p]
        # 获取字体的基本单位

        units_per_em = self.font['head'].unitsPerEm
        width = glyphset.width
        height = glyphset.height

        # width, ascender, descender = \
        #     glyphset.width, self.font['OS/2'].usWinAscent, -self.font['OS/2'].usWinDescent  # 获取字形的宽度和上沿以及下沿
        # height = ascender - descender  # 利用上沿和下沿计算字形高度

        # xMin, yMin, xMax, yMax = glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax
        xMin, yMin, xMax, yMax = head.xMin, head.yMin, head.xMax, head.yMax

        width = xMax - xMin
        height = yMax - yMin

        scale = self._缩放大小()
        微调 = 0.9322  # 参考字体：小篆体.ttf
        if 纵向:
            位移y = 索引位置 * (scale * (yMax - yMin) + self._字符间距) * 微调 + 偏移Y
            位移x = 0
        else:
            位移x = 索引位置 * (scale * (xMax - xMin) + self._字符间距) * 微调 + 偏移X
            位移y = 0

        # xMin = ascender
        # yMax = height
        # yMin = 0
        glyph_set = self.font.getGlyphSet()
        pen = SVGPathPen(glyphSet=glyph_set)
        glyphset.draw(pen)

        # bpen = BoundsPen(None)
        # glyphset.draw(bpen)
        # left, bottom, right, top = bpen.bounds
        # # commands = pen.getCommands()
        # xMin = left
        # yMax = top
        # yMin = bottom
        commands = pen._commands
        path_cmds = []
        xMin = 0
        yMin = 0
        last_x, last_y = None, None
        stroke_width = self._字体大小 / 600
        定位圆半径 = self._字体大小 / 150
        调试元素列表 = []
        first_point = True
        for command in commands:
            cmd_flag = command[0]
            cs = command[1:].replace(" ", ",").split(",")
            cs = [cmd_flag] + [self._try_to_float(c) for c in cs]
            stroke_style = None

            坐标点填充色 = 颜色.红色 if first_point else 颜色.透明
            first_point = False
            if cmd_flag in ["m", "M", "l", "L"]:
                x_, y_ = scale * (cs[1] - xMin) + 位移x, scale * (yMax - cs[2] - yMin) + 位移y
                cs = (cs[0], x_, y_)
                last_x, last_y = x_, y_
            elif cmd_flag in ["q", "Q"]:
                x1_, y1_ = scale * (cs[1] - xMin) + 位移x, scale * (yMax - cs[2] - yMin) + 位移y
                x_, y_ = scale * (cs[3] - xMin) + 位移x, scale * (yMax - cs[4] - yMin) + 位移y
                cs = (cs[0], x1_, y1_, x_, y_)
                stroke_style = f"{stroke_width},{stroke_width}"
                if self.debug:
                    控制点 = self.高清图.画矩形(x=x1_ - 定位圆半径 / 2, y=y1_ - 定位圆半径 / 2, 宽=定位圆半径, 高=定位圆半径,
                                       描边宽度=stroke_width / 2, 描边颜色=颜色.黑色, 填充颜色=颜色.绿色).填充透明度(0.5)
                    连接线 = self.高清图.连线(路径点列表=[(x1_, y1_), (x_, y_)],
                                      描边宽度=stroke_width / 2, 描边颜色=颜色.绿色, 描边样式=stroke_style)
                    调试元素列表.append(控制点)
                    调试元素列表.append(连接线)
                    # if self.平移x != 0 or self.平移y != 0:
                    #     控制点.平移(self.平移x, self.平移y)

                last_x, last_y = x_, y_
            elif cmd_flag in ["v", "V"]:
                y_ = scale * (yMax - cs[1] - yMin) + 位移y
                cs = (cs[0], y_)
                last_y = y_
            elif cmd_flag in ["h", "H"]:
                x_ = scale * (cs[1] - xMin) + 位移x
                cs = (cs[0], x_)
                last_x = x_
            elif cmd_flag in ["z", "Z"]:
                cs = (cs[0],)
                first_point = True
            elif cmd_flag in [" "]:
                x_, y_ = scale * (cs[1] - xMin) + 位移x, scale * (yMax - cs[2] - yMin) + 位移y
                cs = ("L", x_, y_)
                last_x, last_y = x_, y_
            else:
                raise Exception(f"{cmd_flag}未处理")

            if self.debug:
                定位圆 = self.高清图.画圆(x=last_x, y=last_y, 半径=定位圆半径, 描边宽度=stroke_width, 描边样式=stroke_style,
                                  填充颜色=坐标点填充色)
                调试元素列表.append(定位圆)
                # if self.平移x != 0 or self.平移y != 0:
                #     定位圆.平移(self.平移x, self.平移y)

            path_cmds.append(tuple(cs))

        if len(调试元素列表) > 0:
            调试元素组 = self.高清图.创建组合(元素列表=调试元素列表)
            if self.平移x != 0 or self.平移y != 0:
                调试元素组.平移(self.平移x, self.平移y)

        return path_cmds


def 画图测试():
    import matplotlib.pyplot as plt
    font_file = r"C:\Windows\Fonts\simhei.ttf"
    font_file = r"G:\works\gitcode\code_painter\字体\小篆体.ttf"
    文字路径 = 字体文本路径工具(font_file)
    字符串轮廓 = 文字路径.获取字符串轮廓("魏刚")

    for 字符轮廓 in 字符串轮廓:
        for 轮廓 in 字符轮廓:
            轮廓 = 轮廓 + 轮廓[0:]  # 闭合
            x_coords = [point[0] for point in 轮廓]
            y_coords = [point[1] for point in 轮廓]
            # x_endPts = [num for num in 轮廓 if num % 2 == 0]
            # y_endPts = [points[pi][1] for pi in endPts]

            colors = ['blue' if flag == 1 else 'green' for x, y, flag in 轮廓]
            plt.plot(x_coords, y_coords, marker='')
            plt.scatter([x_coords[0]], [y_coords[0]], c="red", marker="*", s=200)
            plt.scatter(x_coords, y_coords, c=colors)

        # 设置坐标轴标签
        plt.xlabel('X')
        plt.ylabel('Y')

        # 显示图形
        plt.show()


def 神笔绘图板测试():
    class 路径测试(神笔绘图板):
        """
        将图像进行变形，平铺在桌面或者地板上，可以看到的立体画
        """

        def __init__(self, 文件路径):
            宽, 高 = 纸张大小.A4_纵向(1)
            super(路径测试, self).__init__(作品文件路径=文件路径, 宽=宽 * 2, 高=高 * 2)

        def 创作(self):
            self.显示图框()
            # self.显示网格()

            from 神笔码靓.神笔库.路径工具集 import 字体文本路径工具
            font_file = r"C:\Windows\Fonts\STSONG.TTF"
            font_file = r"C:\Windows\Fonts\simhei.ttf"
            font_file = r"C:\Windows\Fonts\FZYTK.TTF"
            # font_file = 字体文件目录("小篆体.ttf")
            # font_file = 字体文件目录("甲骨文.ttf")

            # font_file = 系统字体.微软雅黑
            文字路径 = 字体文本路径工具(font_file)
            文字样例 = "刚"
            文字样例 = "魏"
            文字样例 = "家"
            文字样例 = "国"
            # 文字样例 = "一"
            文字样例 = "刚一二国家魏"

            字符串路径 = 文字路径.生成字符串路径(文字样例)

            宽, 高 = 文字路径.字体范围()
            self.画矩形(x=0, y=0, 宽=宽, 高=高, 描边宽度=10, 描边颜色=颜色.红色)
            for 字符路径 in 字符串路径:
                self.连线(路径点列表=字符路径, 描边宽度=0.5, 描边颜色=颜色.红色)  # .缩放(0.5)

    神笔 = 路径测试(文件路径="文字路径测试.svg")
    神笔.完成()


def 图片轮廓转路径测试():
    输入图片 = 资源库目录('图片/头像.jpg')
    # print(os.path.exists(input_image_path))

    from 神笔码靓.神笔库 import 神笔绘图板

    神笔 = 神笔绘图板("头像.svg")
    for 路径 in 图片轮廓转路径(输入图片):
        神笔.连线(路径点列表=路径)
    神笔.完成()

class 布尔运算:
    def __init__(self, 最小采样点数=20, 最大采样点数=200, 曲线近似误差阈值=0.1,
                 数值容差=1e-8, 是否几何简化=True, 几何简化容差值=1e-6, buffer操作的分辨率=4):
        """
        初始化PathBoolean实例，设置优化参数

        参数:
            min_samples: 最小采样点数
            max_samples: 最大采样点数
            error_threshold: 曲线近似误差阈值
            tolerance: 数值容差
            simplify: 是否执行几何简化
            simplify_tolerance: 几何简化容差值
            buffer_resolution: buffer操作的分辨率
        """
        self.min_samples = 最小采样点数
        self.max_samples = 最大采样点数
        self.error_threshold = 曲线近似误差阈值
        self.tolerance = 数值容差
        self.simplify = 是否几何简化
        self.simplify_tolerance = 几何简化容差值
        self.buffer_resolution = buffer操作的分辨率

    def path_to_polygon(self, path):
        """将 SVG 路径转换为 Shapely 多边形，使用自适应采样"""
        points = []

        for segment in path:
            if isinstance(segment, Line):
                # 直线段只需两个点
                points.append((segment.start.real, segment.start.imag))
                points.append((segment.end.real, segment.end.imag))
            else:
                # 对曲线段使用自适应采样
                sampled_points = self._adaptive_sample_segment(segment)
                points.extend(sampled_points)

        # 处理空路径
        if not points:
            return None

        # 确保路径闭合
        if points and points[0] != points[-1]:
            points.append(points[0])

        # 创建多边形并处理可能的自相交
        try:
            polygon = Polygon(points)
            if not polygon.is_valid:
                polygon = make_valid(polygon)

            # 应用几何简化
            if self.simplify:
                polygon = polygon.simplify(self.simplify_tolerance)

            # 使用buffer操作消除小误差
            return polygon.buffer(0, resolution=self.buffer_resolution)
        except Exception as e:
            print(f"创建多边形失败: {e}")
            return None

    def _adaptive_sample_segment(self, segment):
        """对曲线段进行自适应采样，根据曲率动态调整采样点数量"""
        # 初始采样点数
        samples = self.min_samples
        points = [segment.point(t / samples) for t in range(samples + 1)]
        points = [(p.real, p.imag) for p in points]

        # 计算曲线的总长度，用于估计复杂度
        length = segment.length()

        # 对于复杂曲线增加采样点
        if isinstance(segment, CubicBezier):
            # 估计贝塞尔曲线的复杂度
            control_points = [
                (segment.start.real, segment.start.imag),
                (segment.control1.real, segment.control1.imag),
                (segment.control2.real, segment.control2.imag),
                (segment.end.real, segment.end.imag)
            ]

            # 计算控制点形成的多边形面积
            area = 0.0
            for i in range(4):
                x1, y1 = control_points[i]
                x2, y2 = control_points[(i + 1) % 4]
                area += (x1 * y2 - x2 * y1)

            area = abs(area) / 2.0

            # 如果面积较大或长度较长，增加采样点
            if area > 1.0 or length > 10.0:
                samples = min(int(samples * (1 + math.sqrt(area / 10) + length / 50)), self.max_samples)
                points = [segment.point(t / samples) for t in range(samples + 1)]
                points = [(p.real, p.imag) for p in points]

        return points

    def polygon_to_path(self, geometry):
        """将 Shapely 几何对象转换为 SVG 路径，处理多种几何类型"""
        if geometry is None or geometry.is_empty:
            return parse_path("")

        paths = []

        # 处理不同类型的几何对象
        if isinstance(geometry, Polygon):
            paths.append(self._polygon_to_path_string(geometry))
        elif isinstance(geometry, MultiPolygon):
            for polygon in geometry.geoms:
                paths.append(self._polygon_to_path_string(polygon))
        elif isinstance(geometry, GeometryCollection):
            for geom in geometry.geoms:
                if isinstance(geom, Polygon):
                    paths.append(self._polygon_to_path_string(geom))
                elif isinstance(geom, MultiPolygon):
                    for polygon in geom.geoms:
                        paths.append(self._polygon_to_path_string(polygon))

        # 合并所有路径
        combined_path = " ".join(paths)
        return parse_path(combined_path)

    def _polygon_to_path_string(self, polygon):
        """将单个多边形转换为SVG路径字符串"""
        # 处理外部环
        exterior_coords = list(polygon.exterior.coords)
        path_str = "M " + " L ".join([f"{x:.6f} {y:.6f}" for x, y in exterior_coords]) + " Z"

        # 处理内部环（孔洞）
        for interior in polygon.interiors:
            hole_coords = list(interior.coords)
            path_str += " M " + " L ".join([f"{x:.6f} {y:.6f}" for x, y in hole_coords]) + " Z"

        return path_str

    def 并集(self, path1, path2):
        """计算两个路径的并集，使用缓存优化"""
        # 缓存多边形结果，避免重复计算
        if not hasattr(path1, '_polygon_cache'):
            path1._polygon_cache = self.path_to_polygon(path1)
        polygon1 = path1._polygon_cache

        if not hasattr(path2, '_polygon_cache'):
            path2._polygon_cache = self.path_to_polygon(path2)
        polygon2 = path2._polygon_cache

        if not polygon1 or not polygon2:
            return parse_path("")

        union_result = unary_union([polygon1, polygon2])
        return self.polygon_to_path(union_result)

    def 交集(self, path1, path2):
        """计算两个路径的交集，使用缓存优化"""
        if not hasattr(path1, '_polygon_cache'):
            path1._polygon_cache = self.path_to_polygon(path1)
        polygon1 = path1._polygon_cache

        if not hasattr(path2, '_polygon_cache'):
            path2._polygon_cache = self.path_to_polygon(path2)
        polygon2 = path2._polygon_cache

        if not polygon1 or not polygon2:
            return parse_path("")

        # 应用几何简化
        if self.simplify:
            polygon1_simplified = polygon1.simplify(self.simplify_tolerance)
            polygon2_simplified = polygon2.simplify(self.simplify_tolerance)
        else:
            polygon1_simplified = polygon1
            polygon2_simplified = polygon2

        intersection_result = polygon1_simplified.intersection(polygon2_simplified)
        return self.polygon_to_path(intersection_result)

    def 差集(self, path1, path2):
        """计算两个路径的差集，使用缓存优化"""
        if not hasattr(path1, '_polygon_cache'):
            path1._polygon_cache = self.path_to_polygon(path1)
        polygon1 = path1._polygon_cache

        if not hasattr(path2, '_polygon_cache'):
            path2._polygon_cache = self.path_to_polygon(path2)
        polygon2 = path2._polygon_cache

        if not polygon1:
            return parse_path("")
        if not polygon2:
            return path1.copy()

        # 应用几何简化
        if self.simplify:
            polygon1_simplified = polygon1.simplify(self.simplify_tolerance)
            polygon2_simplified = polygon2.simplify(self.simplify_tolerance)
        else:
            polygon1_simplified = polygon1
            polygon2_simplified = polygon2

        difference_result = polygon1_simplified.difference(polygon2_simplified)
        return self.polygon_to_path(difference_result)


if __name__ == '__main__':
    # 神笔绘图板测试()
    图片轮廓转路径测试()
