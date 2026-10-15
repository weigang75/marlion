# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
# 生成神笔绘图板文档： python -m pydoc -w 神笔库.神笔绘图板
import os
import svgwrite
from typing import Union, Tuple
import numpy as np
from 神笔码靓.神笔库.元素库.可操作元素集合 import 可操作元素集合
from 神笔码靓.神笔库 import 神笔绘图板工具, N角星路径, N边形路径, 爱心路径, 菱型路径
from 神笔码靓.神笔库.cairosvg工具集 import CairoSvg工具集
from 神笔码靓.神笔库.元素重复工具集 import 元素重复工具集
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.通用工具集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.元素库 import *
from 神笔码靓.神笔库.PDF工具集 import PDF工具集


class 神笔绘图板:
    """
    制作神笔绘图板（矢量图）的工具
    """

    def __init__(self, 作品文件路径: str, 宽=None, 高=None, 视图区=None):
        """
        初始化
        :param 作品文件路径: 保存的SVG无限高清文件路径名称
        :param 宽: 神笔绘图板的宽度
        :param 高: 神笔绘图板的高度
        """
        self.缓存 = {}
        self.开启警告 = 是
        if 高 is None:
            高 = 1000
        if 宽 is None:
            宽 = 1000
        if not 作品文件路径.lower().endswith(".svg"):
            作品文件路径 = 作品文件路径 + ".svg"

        if not os.path.isabs(作品文件路径):
            输出目录 = 作品输出目录()
            if 输出目录 is None:
                err_msg = "请手动创建一个名为'输出文件'的目录。"
                raise Exception(err_msg)
            作品文件路径 = os.path.join(输出目录, 作品文件路径)

        self.高清文件路径 = 作品文件路径
        self.dwg = svgwrite.Drawing(self.高清文件路径, profile='full')
        title = os.path.splitext(os.path.basename(作品文件路径))[0]
        desc = "本文件由《神笔码靓》工具生成，版权归《Python超人/三月三》所有。未经许可，禁止商业使用。" \
               " https://gitcode.net/pythoncr  https://gitee.com/pythoncr"
        self.dwg.set_desc(title=title, desc=desc)
        if 宽 is not None:
            self.dwg['width'] = 宽
        if 高 is not None:
            self.dwg['height'] = 高
        self.dwg.width_ = 宽
        self.dwg.height_ = 高
        self.宽, self.高 = 宽, 高
        self.dwg['xmlns'] = 'http://www.w3.org/2000/svg'
        self.dwg['version'] = '1.1'
        self.dwg['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'
        # self.dwg['viewBox'] = f"0 0 {宽} {高}"
        if 视图区 is not None:
            self.dwg['viewBox'] = 视图区
        self._id_no = 0
        元素.重置ID()
        元素.元素缓存清除()
        self.默认组 = []
        self.调试组 = []
        self.configs = {}
        self.已加载字体 = {}

        self.外联图片贴图 = 否
        self.辅助线颜色 = 颜色.黑色
        self.元素字典 = {}

        from 神笔码靓.神笔库.变换工具集 import 变换工具集
        from 神笔码靓.神笔库.样式工具集 import 样式工具集
        from 神笔码靓.神笔库.滤镜工具集 import 滤镜工具集
        from 神笔码靓.神笔库.动画工具集 import 动画工具集
        from 神笔码靓.神笔库.消息框工具集 import 消息框工具集
        from 神笔码靓.神笔库.符号工具集 import 符号工具集
        from 神笔码靓.神笔库.印章工具集 import 印章工具集
        from 神笔码靓.神笔库.元素排列工具集 import 元素排列工具集

        self.滤镜 = 滤镜工具集(self)
        self.样式 = 样式工具集(self)
        self.变换 = 变换工具集(self)
        self.动画 = 动画工具集(self)
        self.消息框 = 消息框工具集(self)
        self.重复 = 元素重复工具集(self)
        self.符号 = 符号工具集(self)
        self.印章 = 印章工具集(self)
        self.排列 = 元素排列工具集(self)

        self._复用模板支持 = {}
        self.jscripts = []

    def _gen_id(self, perfix):
        _id = f"{perfix}_{self._id_no}"
        self._id_no += 1
        return _id

    def 获取元素(self, id_):
        return self.元素字典.get(id_, None)

    def _注册元素到字典(self, id_, 元素):
        if id_ is None:
            return
        self.元素字典[id_] = 元素

    # region 配置/设置
    def 页面设置(self, 设置: 纸张设置):
        """

        :param 设置:
        :return:
        """
        pass

    def 增加配置项(self, 配置名称: str, 配置数据):
        """

        :param 配置名称:
        :param 配置数据:
        :return:
        """
        self.configs[配置名称] = 配置数据

    def 获取配置项(self, 配置名称: str):
        """

        :param 配置名称:
        :return:
        """
        if 配置名称 in self.configs:
            return self.configs[配置名称]
        return None

    # endregion

    # region 裁剪/遮罩
    def 遮罩(self, 遮罩元素_: 元素, 被遮元素: [元素, list[元素]] = None,
             遮罩单位=None, 遮罩内容单位=None, id_: str = None) -> 遮罩元素:
        """

        @param 遮罩元素_:
        @param 被遮元素:
        @param 遮罩单位: 默认：空间坐标系单位.物体边界
        @param 遮罩内容单位: 默认：空间坐标系单位.用户空间
        @param id_:
        @return:
        """
        _元素 = 遮罩元素(self, self.默认组)
        if hasattr(遮罩元素_, "删除"):
            遮罩元素_.删除()
        _元素.批量设置属性(遮罩元素=遮罩元素_, 被遮元素=被遮元素, 遮罩单位=遮罩单位, 遮罩内容单位=遮罩内容单位, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 圆形裁剪(self, x: float, y: float, 半径: float, 被裁元素: 元素 = None,
                 裁剪路径单位=None, id_: str = None) -> 裁剪元素:
        """

        @param x:
        @param y:
        @param 半径:
        @param 被裁元素:
        @param 裁剪路径单位: 默认：空间坐标系单位.用户空间
        @param id_:
        @return:
        """
        _裁剪元素 = self.画圆(x=x, y=y, 半径=半径)
        _元素 = self.裁剪(裁剪元素_=_裁剪元素, 被裁元素=被裁元素, 裁剪路径单位=裁剪路径单位, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 矩形裁剪(self, x: float, y: float, 宽: float, 高: float, 被裁元素: 元素 = None,
                 裁剪路径单位=None, id_: str = None) -> 裁剪元素:
        """

        @param x:
        @param y:
        @param 宽:
        @param 高:
        @param 被裁元素:
        @param 裁剪路径单位: 默认：空间坐标系单位.用户空间
        @param id_:
        @return:
        """
        _裁剪元素 = self.画矩形(x=x, y=y, 宽=宽, 高=高)
        _元素 = self.裁剪(裁剪元素_=_裁剪元素, 被裁元素=被裁元素, 裁剪路径单位=裁剪路径单位, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 裁剪(self, 裁剪元素_: 元素, 被裁元素: 元素 = None, 裁剪路径单位=None, id_: str = None) -> 裁剪元素:
        """

        @param 裁剪元素_:
        @param 被裁元素:
        @param 裁剪路径单位: 默认：空间坐标系单位.用户空间
        @param id_:
        @return:
        """
        _元素 = 裁剪元素(self, self.默认组)
        if hasattr(裁剪元素_, "删除"):
            裁剪元素_.删除()
        _元素.批量设置属性(裁剪元素=裁剪元素_, 被裁元素=被裁元素, 裁剪路径单位=裁剪路径单位, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    # endregion

    # region 调试用

    def 测距(self, 点1, 点2, 测距颜色=None, 标签字体大小=16, 标签偏移=None, 标签引线位置=0.5,
             背景圆角半径=5, 背景透明度=0.3, 背景色=None, 线条宽度=3, 线条样式=None, 保留小数位=2):
        if 测距颜色 is None:
            测距颜色 = self.辅助线颜色

        def calculate_distance_and_center():
            """
            计算两点之间的距离以及两点的中心点坐标。

            参数:
            x1 (float): 第一个点的x坐标
            y1 (float): 第一个点的y坐标
            x2 (float): 第二个点的x坐标
            y2 (float): 第二个点的y坐标

            返回:
            tuple: 包含两点距离 (distance)、中心点的x坐标 (center_x) 和中心点的y坐标 (center_y) 的元组
            """
            x1, y1 = 点1
            x2, y2 = 点2
            # 计算两点之间的距离，使用两点间距离公式：√[(x2 - x1)² + (y2 - y1)²]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            # 计算中心点的x坐标，即两点x坐标的平均值
            center_x = (x1 + x2) / 2
            # 计算中心点的y坐标，即两点y坐标的平均值
            center_y = (y1 + y2) / 2
            return distance, center_x, center_y

        self.连直线(路径点列表=[点1, 点2], 描边颜色=测距颜色, 描边样式=线条样式, 描边宽度=线条宽度)
        distance, center_x, center_y = calculate_distance_and_center()
        标签文字 = str(round(distance, 保留小数位))
        标签元素列表 = 可操作元素集合(self)

        矩形宽, 矩形高 = len(标签文字) * 标签字体大小 * 0.6, 标签字体大小 * 1.5
        if 背景色 is None:
            背景色 = 颜色.反色(测距颜色)
        self.画矩形(x=center_x - 矩形宽 / 2, y=center_y - 矩形高 / 2, 宽=矩形宽, 高=矩形高,
                    描边颜色=测距颜色,
                    填充颜色=背景色, 圆角半径=背景圆角半径).透明度(背景透明度).添加到列表(标签元素列表)
        self.写字(x=center_x, y=center_y, 文字=标签文字, 填充颜色=测距颜色, 字体大小=标签字体大小).添加到列表(
            标签元素列表)

        if 标签偏移:
            x1, y1 = 点1
            x2, y2 = 点2
            dx = x2 - x1
            # 计算线段在y方向上的长度分量
            dy = y2 - y1
            # 根据70%的比例计算在x方向上的偏移量
            offset_x = dx * 标签引线位置
            # 根据70%的比例计算在y方向上的偏移量
            offset_y = dy * 标签引线位置

            # 计算所求位置的x坐标
            c_x = x1 + offset_x
            # 计算所求位置的y坐标
            c_y = y1 + offset_y
            self.连直线(路径点列表=[(c_x, c_y),
                                    ((center_x + 标签偏移[0], center_y + 标签偏移[1]))],
                        描边颜色=测距颜色, 描边样式="2,2")
            self.画圆(x=c_x, y=c_y, 半径=3, 填充颜色=测距颜色)
            标签元素列表.创建组合().平移(*标签偏移)

    def 显示辅助线(self, 线条颜色=None, 线条宽=1, 显示网格=False, 调试组=False):
        if 线条颜色 is None:
            线条颜色 = self.辅助线颜色
        定位线条 = self.连线(描边颜色=线条颜色, 描边宽度=线条宽)
        定位线条.移动到(0, 0).画水平线(self.宽).画垂直线(self.高).画水平线(0).闭合()
        定位线条.移动到(0, self.高 / 2).画水平线(self.宽)
        定位线条.移动到(self.宽 / 2, 0).画垂直线(self.高)

        if 显示网格:
            self.显示网格(文字描边宽度=0, 网格颜色=线条颜色, 网格透明度=0.8, 调试组=调试组)

        if 调试组:
            定位线条.添加到列表(self.调试组)
        # self.十字(x=self.宽 / 2, y=self.高 / 2, 宽度=self.宽, 高度=self.高, 颜色=颜色)
        # self.十字(x=self.宽, y=self.高, 宽度=100, 高度=100, 颜色=颜色).添加到列表(self.调试组)
        # self.十字(x=0, y=0, 宽度=100, 高度=100, 颜色=颜色).添加到列表(self.调试组)

    def _set_filter(self, SVG元素, filter_name, get_filter_fun):
        if not hasattr(self, filter_name):
            dwg = self.dwg
            filter_ = get_filter_fun()
            # 将滤镜添加到SVG定义中
            dwg.defs.add(filter_)
            setattr(self, filter_name, filter_)
        else:
            filter_ = getattr(self, filter_name)

        SVG元素["filter"] = filter_.get_funciri()

    def _text_to_debug(self, t, x: float, y: float, color: str, font_size: float, text_anchor: str,
                       opacity: float, alignment_baseline=文字垂直基线对齐.中线对齐, 文字描边颜色=None,
                       文字描边宽度=None,
                       调试组=True):
        """

        :param t:
        :param x:
        :param y:
        :param color:
        :param font_size:
        :param text_anchor:
        :param opacity:
        :return:
        """
        text = self.dwg.text(str(t), insert=(x, y), fill=color,
                             font_size=font_size,
                             style="paint-order: stroke;",
                             text_anchor=text_anchor,
                             alignment_baseline=alignment_baseline,
                             font_family=系统字体.Arial, opacity=opacity)

        # bg_text = self.dwg.text(str(t), insert=(x, y), fill="white",
        #                         font_size=font_size,
        #                         text_anchor=text_anchor,
        #                         alignment_baseline=alignment_baseline,
        #                         font_family=系统字体.Arial, opacity=opacity)
        if 文字描边宽度 is None:
            文字描边宽度 = 1

        if 文字描边宽度 > 0:
            # bg_text = self.dwg.use(href=text)
            if 文字描边颜色 is None:
                text.stroke("white")
                # text.fill("white")
            else:
                text.stroke(文字描边颜色)
                # text.fill(文字描边颜色)

            if 文字描边宽度 is not None:
                text.attribs["stroke-width"] = 文字描边宽度
        # else:
        #     bg_text = None
        #
        # filter_name = f"morphology_dilate_0.2"
        #
        # def get_filter_fun():
        #     filter_ = self.dwg.filter()
        #     morphology = filter_.feMorphology(in_='SourceGraphic', operator='dilate', radius=0.2)
        #     return filter_
        #
        # if bg_text:
        #     self._set_filter(bg_text, filter_name, get_filter_fun)

        # SourceGraphic | SourceAlpha | BackgroundImage | BackgroundAlpha | FillPaint | StrokePaint
        # normal — 正常
        # multiply — 正片叠底
        # screen — 滤色
        # darken — 变暗
        # lighten— 变亮
        # SourceGraphic——此关键字代表初始输入到<filter>元素中的图形元素。
        # SourceAlpha——此关键字代表初始输入到<filter>元素中的图形元素。除了只使用alpha通道之外，
        #   SourceAlpha其他规则与SourceGraphic都是一样的。
        # BackgroundImage——该关键字代表<filter>调用该元素时过滤区域下的SVG文档的图像快照。
        #   BackgroundAlpha ——除了了只使用alpha通道之外，其他规则与BackgroundImage相同。
        # FillPaint——此关键字表示过滤器效果的目标元素上的fill属性的值。在很多情况下，FillPaint在任何地方都是不透明的，
        #   但是如果一个形状是用渐变或者图案（其本身包括透明或者半透明的部分）来绘制的话，情况就不一样了。
        # StrokePaint——此关键字表示过滤器效果的目标元素上的stroke属性值。在很多情况下，它们在StrokePaint任何地方都是不透明的，
        #   但是如果一个形状是用渐变或图案（其本身包括透明或半透明的部分）进行绘制，则可能不是这种情况。

        # filter2 = self.dwg.filter()
        # filter2.feBlend(in_='SourceGraphic', in2='FillPaint', mode='multiply')
        # text["filter"] = filter2.get_funciri()

        # # 将feMorphology滤镜应用到红色圆形上
        # bg_text["filter"] = filter_.get_funciri()
        #
        # # 将feMorphology滤镜添加到画布
        # self.dwg.defs.add(filter_)
        if 调试组:
            # if bg_text:
            #     self.调试组.append(bg_text)
            self.调试组.append(text)
        else:
            # if bg_text:
            #     self.默认组.append(bg_text)
            self.默认组.append(text)

    def _path_to_debug(self, path_d: str, color: str, stroke_dasharray: str, opacity: float, 调试组=True):
        """

        :param path_d:
        :param color:
        :param stroke_dasharray:
        :param opacity:
        :return:
        """
        path = self.dwg.path(d=path_d,
                             stroke=color, fill="none", stroke_width=0.2, stroke_dasharray=stroke_dasharray,
                             opacity=opacity)
        if 调试组:
            self.调试组.append(path)
        else:
            self.默认组.append(path)

    def 显示网格(self, 网格线距: int = 20, 网格颜色: str = None, 网格透明度: float = 0.8, 文字描边颜色=None,
                 文字描边宽度=None, 网格字体大小: float = 16, 线条样式: str = "3,2", 更多刻度值=False, 调试组=True):
        """

        :param 网格线距:
        :param 网格颜色:
        :param 网格透明度:
        :param 文字描边颜色:
        :param 文字描边宽度:
        :param 网格字体大小:
        :param 线条样式:
        :param 更多刻度值:
        :param 调试组:
        :return:
        """
        if 网格颜色 is None:
            网格颜色 = self.辅助线颜色

        if 网格线距 is not None:
            w, h = int(self.dwg.width_), int(self.dwg.height_)
            path_d = ""
            网格高阈值 = 300
            center_y, center_y_min, center_y_max = h / 2, h, 0
            for yi in range(网格线距, h, 网格线距):
                path_d += "M{:.2f},{:.2f}L{:.2f},{:.2f}".format(0, yi, w, yi)
                if (yi / 网格线距) % 2 == 0:
                    continue

                if yi < center_y and yi > center_y_max:
                    center_y_max = yi
                if yi > center_y and yi < center_y_min:
                    center_y_min = yi

                self._text_to_debug(t=yi, x=网格字体大小 / 2, y=yi, color=网格颜色, font_size=网格字体大小,
                                    text_anchor=文字水平基线对齐.起始点对齐, opacity=网格透明度,
                                    文字描边颜色=文字描边颜色, 文字描边宽度=文字描边宽度, 调试组=调试组)

                if (self.宽 > 网格高阈值 * 1.77) and 更多刻度值:
                    self._text_to_debug(t=yi, x=w - 网格字体大小 / 2, y=yi, color=网格颜色, font_size=网格字体大小,
                                        text_anchor=文字水平基线对齐.结束点对齐, opacity=网格透明度,
                                        文字描边颜色=文字描边颜色, 文字描边宽度=文字描边宽度, 调试组=调试组)

                if (self.宽 > 网格高阈值 * 1.77 * 2) and 更多刻度值:
                    self._text_to_debug(t=yi, x=w / 2, y=yi, color=网格颜色, font_size=网格字体大小,
                                        text_anchor=文字水平基线对齐.结束点对齐, opacity=网格透明度,
                                        文字描边颜色=文字描边颜色, 文字描边宽度=文字描边宽度, 调试组=调试组)

            for xi in range(网格线距, w, 网格线距):
                path_d += "M{:.2f},{:.2f}L{:.2f},{:.2f}".format(xi, 0, xi, h)

                if (xi / 网格线距) % 2 == 0:
                    continue

                self._text_to_debug(t=xi, x=xi, y=网格字体大小 / 1.5, color=网格颜色, font_size=网格字体大小,
                                    text_anchor=文字水平基线对齐.中点对齐, opacity=网格透明度,
                                    文字描边颜色=文字描边颜色, 文字描边宽度=文字描边宽度, 调试组=调试组)

                if (self.高 > 网格高阈值) and 更多刻度值:
                    self._text_to_debug(t=xi, x=xi, y=h - 网格字体大小 / 1.5, color=网格颜色, font_size=网格字体大小,
                                        text_anchor=文字水平基线对齐.中点对齐, opacity=网格透明度,
                                        文字描边颜色=文字描边颜色, 文字描边宽度=文字描边宽度, 调试组=调试组)

                if (self.高 > 网格高阈值 * 2) and 更多刻度值:
                    # y_center = h / 2
                    y_center = (center_y_min + center_y_max) / 2
                    self._text_to_debug(t=xi, x=xi, y=y_center, color=网格颜色, font_size=网格字体大小,
                                        text_anchor=文字水平基线对齐.中点对齐, opacity=网格透明度,
                                        文字描边颜色=文字描边颜色, 文字描边宽度=文字描边宽度, 调试组=调试组)

            self._path_to_debug(path_d=path_d, color=网格颜色, stroke_dasharray=线条样式, opacity=网格透明度,
                                调试组=调试组)

    def 显示图框(self, 边框颜色: str = None, 边框宽度: float = 1, 调试组=True):
        """

        :param 边框颜色:
        :param 边框宽度:
        :return:
        """
        if 边框颜色 is None:
            边框颜色 = self.辅助线颜色

        if 边框宽度 is None or 边框宽度 <= 0:
            边框宽度 = 1
        rect = self.dwg.rect(insert=(0, 0), size=('100%', '100%'),
                             fill='none', stroke_width=边框宽度, stroke=边框颜色,
                             id=f'{元素.生成元素id("rc")}')
        if 调试组:
            self.调试组.append(rect)
        else:
            self.默认组.append(rect)
        return rect

    def 小数转字符串(self, 小数, 保留位数):
        小数s = str(round(小数, 保留位数))
        if "." in 小数s:
            小数s = 小数s.rstrip("0")
        if 小数s.endswith("."):
            小数s = 小数s.rstrip(".")
        return 小数s

    @入参名称获取
    def 显示坐标(self, 坐标1, 坐标2=None, 坐标3=None, 坐标4=None, 坐标5=None,
                 坐标6=None, 坐标7=None, 坐标8=None, 坐标9=None, 坐标10=None,
                 坐标11=None, 坐标12=None, 坐标13=None, 坐标14=None, 坐标15=None,
                 坐标16=None, 坐标17=None, 坐标18=None, 坐标19=None, 坐标20=None,
                 坐标1文字偏移=None, 坐标2文字偏移=None, 坐标3文字偏移=None, 坐标4文字偏移=None, 坐标5文字偏移=None,
                 坐标6文字偏移=None, 坐标7文字偏移=None, 坐标8文字偏移=None, 坐标9文字偏移=None, 坐标10文字偏移=None,
                 坐标11文字偏移=None, 坐标12文字偏移=None, 坐标13文字偏移=None, 坐标14文字偏移=None,
                 坐标15文字偏移=None,
                 坐标16文字偏移=None, 坐标17文字偏移=None, 坐标18文字偏移=None, 坐标19文字偏移=None,
                 坐标20文字偏移=None,
                 文字颜色=None, 字体大小=12, 保留小数位=2, 定位类型=定位点类型.十字) -> 元素组:
        if 文字颜色 is None:
            文字颜色 = self.辅助线颜色
        入参名称 = 入参名称字典()
        参数列表 = "["
        for i in range(1, 21):
            参数列表 += f"('坐标{i}',坐标{i}), "
        参数列表 += "]"
        定位元素列表 = 可操作元素集合(self)
        for 坐标名, 坐标值 in eval(参数列表):
            if 坐标值 is not None:
                if 坐标名 in 入参名称:
                    坐标值x = self.小数转字符串(坐标值[0], 保留小数位)  # f"{round(坐标值[0], 保留小数位)}".rstrip("0")
                    坐标值y = self.小数转字符串(坐标值[1], 保留小数位)  # f"{round(坐标值[1], 保留小数位)}".rstrip("0")
                    坐标名称 = f'({坐标值x}, {坐标值y})'
                    文字偏移 = eval(f"{坐标名}文字偏移")
                else:
                    文字偏移 = None
                    坐标名称 = None
                if 文字偏移 is None:
                    self.定位坐标(坐标=坐标值, 文字=坐标名称, 定位颜色=文字颜色,
                                  字体大小=字体大小, 定位类型=定位类型).添加到列表(定位元素列表)
                else:
                    self.定位坐标(坐标=坐标值, 文字=坐标名称, 文字偏移=文字偏移, 定位颜色=文字颜色,
                                  字体大小=字体大小, 定位类型=定位类型).添加到列表(定位元素列表)

        return 定位元素列表.创建组合()

    def 定位点(self, x: float, y: float, 定位点颜色=颜色.红色, 所属组=None, 类型=定位点类型.十字,
               字体大小=12) -> 元素组:
        """

        @param x:
        @param y:
        @param 定位点颜色:
        @param 所属组:
        @param 定位点类型: 十字 空圆 实圆 空方 实方
        @return:
        """
        定位宽 = round(字体大小 / 12 * 8)
        描边宽度 = round(字体大小 / 12, 2)
        定位半宽 = 定位宽 / 2
        # if 类型 == 定位点类型.十字:
        #     定位点元素 = self.十字(x=x, y=y, 高度=20, 宽度=20, 颜色=定位点颜色)
        if 类型 == 定位点类型.空圆:
            定位点元素 = self.画圆(x=x, y=y, 半径=定位半宽, 描边颜色=定位点颜色, 描边宽度=描边宽度)
        elif 类型 == 定位点类型.实圆:
            定位点元素 = self.画圆(x=x, y=y, 半径=定位半宽, 填充颜色=定位点颜色, 描边颜色=定位点颜色, 描边宽度=描边宽度)
        elif 类型 == 定位点类型.空方:
            定位点元素 = self.画矩形(x=x - 定位半宽, y=y - 定位半宽, 高=定位宽, 宽=定位宽, 描边颜色=定位点颜色,
                                     描边宽度=描边宽度)
        elif 类型 == 定位点类型.实方:
            定位点元素 = self.画矩形(x=x - 定位半宽, y=y - 定位半宽, 高=定位宽, 宽=定位宽, 填充颜色=定位点颜色,
                                     描边颜色=定位点颜色, 描边宽度=描边宽度)
        else:
            圆 = self.画圆(x, y, 半径=定位宽 / 4, 填充颜色=定位点颜色, 描边颜色=定位点颜色, 描边宽度=0)
            十字 = self.十字(x=x, y=y, 高度=定位宽 * 2, 宽度=定位宽 * 2, 颜色=定位点颜色, 描边宽度=描边宽度)
            定位点元素 = self.创建组合(元素列表=[圆, 十字])

        if 所属组 is not None:
            定位点元素.更换组(所属组)

        return 定位点元素

    @入参名称获取
    def 定位(self, 坐标1, 坐标2=None, 坐标3=None, 坐标4=None, 坐标5=None,
             坐标6=None, 坐标7=None, 坐标8=None, 坐标9=None, 坐标10=None,
             坐标11=None, 坐标12=None, 坐标13=None, 坐标14=None, 坐标15=None,
             坐标16=None, 坐标17=None, 坐标18=None, 坐标19=None, 坐标20=None,
             坐标21=None, 坐标22=None, 坐标23=None, 坐标24=None, 坐标25=None,
             坐标26=None, 坐标27=None, 坐标28=None, 坐标29=None, 坐标30=None,
             坐标31=None, 坐标32=None, 坐标33=None, 坐标34=None, 坐标35=None,
             坐标36=None, 坐标37=None, 坐标38=None, 坐标39=None, 坐标40=None,
             坐标41=None, 坐标42=None, 坐标43=None, 坐标44=None, 坐标45=None,
             坐标46=None, 坐标47=None, 坐标48=None, 坐标49=None, 坐标50=None,
             坐标51=None, 坐标52=None, 坐标53=None, 坐标54=None, 坐标55=None,
             坐标56=None, 坐标57=None, 坐标58=None, 坐标59=None, 坐标60=None,
             坐标61=None, 坐标62=None, 坐标63=None, 坐标64=None, 坐标65=None,
             坐标66=None, 坐标67=None, 坐标68=None, 坐标69=None, 坐标70=None,
             坐标71=None, 坐标72=None, 坐标73=None, 坐标74=None, 坐标75=None,
             坐标76=None, 坐标77=None, 坐标78=None, 坐标79=None, 坐标80=None,
             坐标81=None, 坐标82=None, 坐标83=None, 坐标84=None, 坐标85=None,
             坐标86=None, 坐标87=None, 坐标88=None, 坐标89=None, 坐标90=None,
             坐标91=None, 坐标92=None, 坐标93=None, 坐标94=None, 坐标95=None,
             坐标96=None, 坐标97=None, 坐标98=None, 坐标99=None, 坐标100=None,
             坐标1文字偏移=None, 坐标2文字偏移=None, 坐标3文字偏移=None, 坐标4文字偏移=None, 坐标5文字偏移=None,
             坐标6文字偏移=None, 坐标7文字偏移=None, 坐标8文字偏移=None, 坐标9文字偏移=None, 坐标10文字偏移=None,
             坐标11文字偏移=None, 坐标12文字偏移=None, 坐标13文字偏移=None, 坐标14文字偏移=None, 坐标15文字偏移=None,
             坐标16文字偏移=None, 坐标17文字偏移=None, 坐标18文字偏移=None, 坐标19文字偏移=None, 坐标20文字偏移=None,
             坐标21文字偏移=None, 坐标22文字偏移=None, 坐标23文字偏移=None, 坐标24文字偏移=None, 坐标25文字偏移=None,
             坐标26文字偏移=None, 坐标27文字偏移=None, 坐标28文字偏移=None, 坐标29文字偏移=None, 坐标30文字偏移=None,
             坐标31文字偏移=None, 坐标32文字偏移=None, 坐标33文字偏移=None, 坐标34文字偏移=None, 坐标35文字偏移=None,
             坐标36文字偏移=None, 坐标37文字偏移=None, 坐标38文字偏移=None, 坐标39文字偏移=None, 坐标40文字偏移=None,
             坐标41文字偏移=None, 坐标42文字偏移=None, 坐标43文字偏移=None, 坐标44文字偏移=None, 坐标45文字偏移=None,
             坐标46文字偏移=None, 坐标47文字偏移=None, 坐标48文字偏移=None, 坐标49文字偏移=None, 坐标50文字偏移=None,
             坐标51文字偏移=None, 坐标52文字偏移=None, 坐标53文字偏移=None, 坐标54文字偏移=None, 坐标55文字偏移=None,
             坐标56文字偏移=None, 坐标57文字偏移=None, 坐标58文字偏移=None, 坐标59文字偏移=None, 坐标60文字偏移=None,
             坐标61文字偏移=None, 坐标62文字偏移=None, 坐标63文字偏移=None, 坐标64文字偏移=None, 坐标65文字偏移=None,
             坐标66文字偏移=None, 坐标67文字偏移=None, 坐标68文字偏移=None, 坐标69文字偏移=None, 坐标70文字偏移=None,
             坐标71文字偏移=None, 坐标72文字偏移=None, 坐标73文字偏移=None, 坐标74文字偏移=None, 坐标75文字偏移=None,
             坐标76文字偏移=None, 坐标77文字偏移=None, 坐标78文字偏移=None, 坐标79文字偏移=None, 坐标80文字偏移=None,
             坐标81文字偏移=None, 坐标82文字偏移=None, 坐标83文字偏移=None, 坐标84文字偏移=None, 坐标85文字偏移=None,
             坐标86文字偏移=None, 坐标87文字偏移=None, 坐标88文字偏移=None, 坐标89文字偏移=None, 坐标90文字偏移=None,
             坐标91文字偏移=None, 坐标92文字偏移=None, 坐标93文字偏移=None, 坐标94文字偏移=None, 坐标95文字偏移=None,
             坐标96文字偏移=None, 坐标97文字偏移=None, 坐标98文字偏移=None, 坐标99文字偏移=None, 坐标100文字偏移=None,
             定位颜色=None, 字体大小=16, 自定义标签=None) -> 元素组:
        if 定位颜色 is None:
            定位颜色 = self.辅助线颜色
        入参名称 = 入参名称字典()
        参数列表 = "["
        for i in range(1, 101):
            参数列表 += f"('坐标{i}',坐标{i}), "
        参数列表 += "]"
        定位元素列表 = 可操作元素集合(self)
        idx = 0
        for 坐标名, 坐标值 in eval(参数列表):
            if 坐标值 is not None:
                if isinstance(自定义标签, list):
                    坐标名称 = 自定义标签[idx]
                    文字偏移 = None
                    idx += 1
                else:
                    if 坐标名 in 入参名称:
                        坐标名称 = 入参名称[坐标名]
                        文字偏移 = eval(f"{坐标名}文字偏移")
                    else:
                        文字偏移 = None
                        坐标名称 = None
                if 文字偏移 is None:
                    self.定位坐标(坐标=坐标值, 文字=坐标名称, 定位颜色=定位颜色,
                                  字体大小=字体大小).添加到列表(定位元素列表)
                else:
                    self.定位坐标(坐标=坐标值, 文字=坐标名称, 文字偏移=文字偏移,
                                  字体大小=字体大小, 定位颜色=定位颜色).添加到列表(定位元素列表)

        return 定位元素列表.创建组合()

    @入参名称获取
    def 定位坐标(self, 坐标, 定位颜色=None, 文字=None, 字体大小=16, 文字偏移=None,
                 所属组=None, 定位类型=定位点类型.十字) -> 元素组:
        if 定位颜色 is None:
            定位颜色 = self.辅助线颜色

        if 文字偏移 is None:
            文字偏移 = (3, 6)
            pp = round(字体大小 / 5, 2)
            文字偏移 = (pp, pp * 2)

        x, y = 坐标
        定位元素列表 = 可操作元素集合(self)
        定位点 = self.定位点(x=x, y=y, 定位点颜色=定位颜色, 类型=定位类型, 字体大小=字体大小).添加到列表(定位元素列表)
        if 文字 is None:
            入参名称 = 入参名称字典()
            if 入参名称 is None:
                文字 = ""
            elif "坐标" in 入参名称:
                文字 = 入参名称["坐标"]
            else:
                文字 = ""

        if len(文字) > 0:
            定位文字 = self.写字(x=x, y=y, 文字=文字, 字体大小=字体大小, 填充颜色=定位颜色,
                                 水平基线对齐=文字水平基线对齐.起始点对齐,
                                 垂直基线对齐=文字垂直基线对齐.顶线对齐).添加到列表(定位元素列表)
            if 文字偏移 is not None:
                定位文字.平移(*文字偏移)
        定位 = 定位元素列表.创建组合()
        if 所属组 is not None:
            定位.更换组(所属组)
        return 定位

    def 显示关键点(self, 关键点列表=[], 关键点颜色=颜色.黑色):
        for x, y in 关键点列表:
            十字 = self.十字(x=x, y=y, 高度=10, 宽度=10, 颜色=关键点颜色)
            self.调试组.append(十字)

    def 定位点距离(self, x1: float, y1: float, x2: float, y2: float, 颜色=颜色.黑色, 所属组=None):
        if 所属组 is None:
            所属组 = self.调试组
        self.定位点(x=x1, y=y1, 定位点颜色=颜色, 所属组=所属组)
        self.定位点(x=x2, y=y2, 定位点颜色=颜色, 所属组=所属组)
        self.连直线([(x1, y1), (x2, y2)], 描边颜色=颜色).更换组(所属组)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        dx = x2 - x1
        dy = y2 - y1
        distance = (dx ** 2 + dy ** 2) ** 0.5
        self.写字(x=cx, y=cy, 文字=str(round(distance, 2)), 填充颜色=颜色).更换组(所属组)

    # def 画点(self, x: float, y: float, 填充颜色=颜色.黑色, 大小=2, 十字=True):
    #
    #     self.画圆(x, y, 半径=大小, 填充颜色=填充颜色, 描边颜色=填充颜色, 描边宽度=0)
    #     if 十字:
    #         line1 = [(x - 大小 * 3, y), (x + 大小 * 3, y)]
    #         self.sz(line1, 填充颜色=填充颜色, 描边颜色=填充颜色)
    #         line2 = [(x, y - 大小 * 3), (x, y + 大小 * 3)]
    #         self.连直线(line2, 填充颜色=填充颜色, 描边颜色=填充颜色)
    #
    # def 画多个点(self, 点坐标列表, 填充颜色=颜色.黑色, 大小=2, 显示坐标=False):
    #     """
    #
    #     :param 点坐标列表:
    #     :param 填充颜色:
    #     :param 大小:
    #     :param 显示坐标:
    #     :return:
    #     """
    #     cx, cy = 多边形工具.获取中心点(点坐标列表)
    #     for 点坐标 in 点坐标列表:
    #         if len(点坐标) == 2:
    #             x, y = 点坐标
    #             link_to = None
    #             self.画点(x, y, 填充颜色=填充颜色, 大小=大小)
    #         else:
    #             x, y, link_to = 点坐标
    #             self.画矩形(x - 2, y - 2, 高=4, 宽=4, 描边颜色=填充颜色, 描边宽度=0.5, 填充颜色="none")
    #
    #         if 显示坐标:
    #             if x > cx:
    #                 tx = x + 5
    #             elif x < cx:
    #                 tx = x - 5
    #             else:
    #                 tx = x
    #             if y > cy:
    #                 ty = y + 5
    #             elif y < cy:
    #                 ty = y - 5
    #             else:
    #                 ty = y
    #
    #             self.写字(tx, ty, f"{x},{y}", 填充颜色=填充颜色, 字体大小=5)
    #             if link_to is not None:
    #                 link_x, link_y = link_to
    #                 self.连直线([(x, y), (link_x, link_y)], 描边颜色=填充颜色, 填充颜色='none', 描边样式="1,1", 描边宽度=0.2)

    # endregion

    def 创建链接(self, 元素对象, 链接地址, 链接提示=None, 链接描述=None, 新开窗口=False, id_: str = None) -> 链接元素:
        _元素 = 链接元素(self, self.默认组)
        _元素.批量设置属性(元素对象=元素对象, 链接地址=链接地址, 链接提示=链接提示, 链接描述=链接描述,
                           新开窗口=新开窗口, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 创建标记(self, id_: str = None) -> 标记元素:
        _元素 = 标记元素(self, self.默认组)
        _元素.批量设置属性(id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    # region 绘图方法
    # region 文字/路径
    def 路径文字(self, 路径点列表: list, 文字: str, 开始位移="50%", 字体: str = 系统字体.默认, 字体大小: float = 16,
                 字符间距: float = 0,
                 填充颜色=颜色.黑色, 描边颜色=颜色.黑色, 描边宽度: float = 0, 透明度: float = 1.0, 描边样式: str = None,
                 粗体: bool = 否, 斜体: bool = 否, 下划线: bool = 否, id_: str = None) -> 路径文字元素:
        """
        路径详情看： https://blog.csdn.net/weixin_40779234/article/details/113701444
        :param 路径点列表:
        :param 文字:
        :param 开始位移:
        :param 字体:
        :param 字体大小:
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 透明度:
        :param 描边样式:
        :param 粗体:
        :param 斜体:
        :param 下划线:
        :param 阴影:
        :param 模糊:
        :return:
        """
        _元素 = 路径文字元素(self, self.默认组)
        _元素.批量设置属性(点列表=路径点列表, 文字=文字, 开始位移=开始位移, 字体=字体, 字体大小=字体大小,
                           字符间距=字符间距,
                           填充颜色=填充颜色, 描边颜色=描边颜色, 水平基线对齐=文字水平基线对齐.中点对齐,
                           描边宽度=描边宽度, 透明度=透明度, 描边样式=描边样式, 粗体=粗体, 斜体=斜体, 下划线=下划线,
                           id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    # def 标注文字(self, 元素对象, 文字, 相对位置=(0, 0), 字体=系统字体.默认, 字体大小=16, 填充颜色=颜色.黑色, 描边颜色=颜色.黑色,
    #          描边宽度=0, 透明度=1.0, 旋转角度=0, 垂直基线对齐="middle", 水平基线对齐="middle", 描边样式=None, 模糊=0, 阴影=None,
    #          粗体=否, 斜体=否, 下划线=否) -> 文字元素:
    #
    #     (min_x, min_y), (max_x, max_y) = 神笔绘图板工具.获取元素的坐标信息(元素对象)
    #     ox, oy = min_x, min_y
    #     x, y = ox + 相对位置[0], oy + 相对位置[1]
    #     return self.写字(x, y, 文字=文字, 字体=字体, 字体大小=字体大小, 填充颜色=填充颜色, 描边颜色=描边颜色, 描边宽度=描边宽度,
    #                    透明度=透明度, 旋转角度=旋转角度, 垂直基线对齐=垂直基线对齐, 水平基线对齐=水平基线对齐, 描边样式=描边样式,
    #                    模糊=模糊, 阴影=阴影, 粗体=粗体, 斜体=斜体, 下划线=下划线)

    def _判断并加载字体(self, 字体):
        if 字体 in self.已加载字体:
            return
        self.已加载字体[字体] = True
        if not 系统字体.是否系统字体(字体):
            self.加载字体样式(字体)
            # 字体名列表 = self.样式.导入字体样式(字体)
            # if len(字体名列表) > 0:
            #     字体 = 字体文件目录(字体名列表[0])

    def 加载字体样式(self, 字体):
        字体名列表 = self.样式.导入字体样式()

    @staticmethod
    def 四舍五入(数值, 保留位数=None):
        if 保留位数 is None:
            保留位数 = 元素.数值精确度
        return round(数值, 保留位数)

    def 文字转路径(self, x: float, y: float, 文字: str, 字体文件: str = 系统字体.默认, 字体大小: float = 16,
                   填充颜色: object = 颜色.透明, 描边颜色: object = 颜色.黑色, 描边宽度: float = 1, 透明度: float = 1.0,
                   字符间距: [float, str] = 空, 纵向=否, 描边样式: object = 空, id_: str = None,
                   文字位置微调=None) -> 路径元素:
        from 神笔码靓.神笔库.路径工具集 import 字体文本路径工具

        文字 = 文字.replace("\r", "").replace("\n", "")
        平移x = 字体大小 / 1000
        平移y = 字体大小 / 6.2

        if x != 0:
            平移x += x

        if y != 0:
            平移y += y

        if "\\" in 字体文件 or "/" in 字体文件:
            pass
        else:
            字体文件_ = 字体文件目录(字体文件)
            if not os.path.exists(字体文件_):
                字体文件_ = os.path.join("c:\\windows\\fonts", 字体文件)
            字体文件 = 字体文件_

        文字路径工具 = 字体文本路径工具(self, 字体文件, 字体大小, 字符间距)
        if 平移x != 0 or 平移y != 0:
            文字路径工具.平移(平移x, 平移y)
        字符串路径点列表 = 文字路径工具.生成字符串路径(文字, 纵向, 文字位置微调)

        路径点列表 = []
        for 字符路径点列表 in 字符串路径点列表:
            路径点列表 += 字符路径点列表
        文字路径 = self.连线(路径点列表=路径点列表, 填充颜色=填充颜色, 描边颜色=描边颜色, 描边宽度=描边宽度,
                             透明度=透明度,
                             描边样式=描边样式, id_=id_)
        文字路径.设置属性值("文字", 文字)
        # if 水平基线对齐 == 文字水平基线对齐.中点对齐:
        #     平移x = -字体大小 / 2.0064  # 左->小   右->大
        # elif 水平基线对齐 == 文字水平基线对齐.起始点对齐:
        #     平移x = 字体大小 / 1000  # 左->大   右->小
        # elif 水平基线对齐 == 文字水平基线对齐.结束点对齐:
        #     平移x = -字体大小 / 1.0015  # 左->小   右->大
        # else:
        #     平移x = 0
        #
        # if 垂直基线对齐 == 文字垂直基线对齐.中线对齐:
        #     平移y = -字体大小 / 1.57819  # 上->小   下->大
        # elif 垂直基线对齐 == 文字垂直基线对齐.顶线对齐:
        #     平移y = 字体大小 / 6.2  # 上->大  下->小
        # elif 垂直基线对齐 == 文字垂直基线对齐.底线对齐:
        #     平移y = -字体大小 / 0.9628  # 上->小   下->大
        # else:
        #     平移y = 0

        # 平移x = 字体大小 / 1000
        # 平移y = 字体大小 / 6.2
        # 文字路径 = 文字路径.平移(平移x, 平移y)

        # 宽, 高 = 文字路径工具.字体范围()
        # 矩形 = self.画矩形(x=x, y=y, 宽=宽, 高=高, 描边宽度=10, 描边颜色=颜色.红色)
        # 矩形 = 矩形.平移(平移x, 平移y)

        # 字体 = os.path.splitext(os.path.basename(字体文件))[0]
        # self.写字(x=x, y=y, 文字=文字, 字体大小=字体大小, 字符间距=字符间距,
        #         垂直基线对齐=文字垂直基线对齐.顶线对齐, 水平基线对齐=文字水平基线对齐.起始点对齐, 字体=字体).透明度(0.5)

        if 平移x != 0 or 平移y != 0:
            文字路径.平移(平移x, 平移y)
        self._注册元素到字典(id_, 文字路径)
        return 文字路径

    def 写字(self, x: float, y: float, 文字: str, 字体: str = 系统字体.默认, 字体大小: float = 16, 填充颜色=颜色.黑色,
             描边颜色=颜色.黑色, 描边宽度: float = 0, 透明度: float = 1.0,
             垂直基线对齐: str = 文字垂直基线对齐.中线对齐,
             水平基线对齐: str = 文字水平基线对齐.中点对齐, 描边样式=空, 字符行间距: float = 空, 文字换行=否,
             粗体: bool = 否, 斜体: bool = 否, 下划线: bool = 否, 字符间距: float = 空, id_: str = None) -> 文字元素:
        """

        :param x:
        :param y:
        :param 文字:
        :param 字体:
        :param 字体大小:
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 透明度:
        :param 垂直基线对齐:
        :param 水平基线对齐:
        :param 描边样式:
        :param 字符行间距:
        :param 文字换行:
        :param 粗体:
        :param 斜体:
        :param 下划线:
        :param 字符间距:
        :param id_:
        :return:
        """
        if "\n" not in 文字 or 文字换行 is 否:
            _元素 = self._写字(x=x, y=y, 文字=文字, 字体=字体, 字体大小=字体大小,
                               填充颜色=填充颜色, 描边颜色=描边颜色, 描边宽度=描边宽度,
                               透明度=透明度, 垂直基线对齐=垂直基线对齐, 水平基线对齐=水平基线对齐, 描边样式=描边样式,
                               粗体=粗体, 斜体=斜体, 下划线=下划线, 字符间距=字符间距, id_=id_)
        else:
            文字列表 = 可操作元素集合(self)
            if 字符行间距 is 空:
                字符行间距 = 字体大小 * 0.15
            字符行间距 = 字体大小 + 字符行间距
            for idx, 文字_ in enumerate(文字.split("\n")):
                if id_ is not None:
                    id_n = id_ + "_" + str(idx)
                else:
                    id_n = id_
                self._写字(x=x, y=y + idx * 字符行间距, 文字=文字_, 字体=字体, 字体大小=字体大小,
                           填充颜色=填充颜色, 描边颜色=描边颜色, 描边宽度=描边宽度,
                           透明度=透明度, 垂直基线对齐=垂直基线对齐, 水平基线对齐=水平基线对齐, 描边样式=描边样式,
                           粗体=粗体, 斜体=斜体, 下划线=下划线, 字符间距=字符间距, id_=id_n).添加到列表(文字列表)
            _元素 = 文字列表
        self._注册元素到字典(id_, _元素)
        return _元素

    def _写字(self, x: float, y: float, 文字: str, 字体: str = 系统字体.默认, 字体大小: float = 16,
              填充颜色=颜色.黑色, 描边颜色=颜色.黑色, 描边宽度: float = 0,
              透明度: float = 1.0, 垂直基线对齐: str = 文字垂直基线对齐.中线对齐,
              水平基线对齐: str = 文字水平基线对齐.中点对齐, 描边样式=空,
              粗体: bool = 否, 斜体: bool = 否, 下划线: bool = 否, 字符间距: float = 空, id_: str = None) -> 文字元素:
        """

        :param x:
        :param y:
        :param 文字:
        :param 字体:
        :param 字体大小:
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 透明度:
        :param 垂直基线对齐:
        :param 水平基线对齐:
        :param 描边样式:
        :param 粗体:
        :param 斜体:
        :param 下划线:
        :param 字符间距:
        :param id_:
        :return:
        """
        if 描边样式 != 空 and 描边宽度 == 0:
            描边宽度 = 1.0

        if 字体 is not None:
            self._判断并加载字体(字体)

        _元素 = 文字元素(self, self.默认组)
        _元素.批量设置属性(x=x, y=y, 文字=文字, 字体=字体, 字体大小=字体大小, 填充颜色=填充颜色,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, 粗体=粗体, 斜体=斜体, 下划线=下划线,
                           字符间距=字符间距,
                           透明度=透明度, 垂直基线对齐=垂直基线对齐, 水平基线对齐=水平基线对齐, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 获取箭头路径(self, 开始点, 结束点, 样式=None, 箭头长度=10, 箭头角度=30, 描边宽度=1, 结束箭头=True,
                     开始箭头=True):
        arrow_length = 箭头长度
        arrow_angle = 箭头角度
        (start_x, start_y), (end_x, end_y) = 开始点, 结束点
        angle_rad = math.atan2(end_y - start_y, end_x - start_x)
        angle_deg = math.degrees(angle_rad)

        if 样式 is None:
            样式 = 箭头样式.倒钩

        if 样式 in [箭头样式.空心]:
            if 开始箭头:
                lines = [("M", start_x + (arrow_length - 描边宽度) * math.cos(math.radians(angle_deg)),
                          start_y + (arrow_length - 描边宽度) * math.sin(math.radians(angle_deg)))]
            else:
                lines = [("M", start_x, start_y)]

            if 结束箭头:
                lines += [(end_x - (arrow_length - 描边宽度) * math.cos(math.radians(angle_deg)),
                           end_y - (arrow_length - 描边宽度) * math.sin(math.radians(angle_deg)))]
            else:
                lines += [(end_x, end_y)]
        else:
            lines = [("M", start_x, start_y), (end_x, end_y)]

        arrow_dx1 = arrow_length * math.cos(math.radians(angle_deg + arrow_angle))
        arrow_dy1 = arrow_length * math.sin(math.radians(angle_deg + arrow_angle))
        arrow_dx2 = arrow_length * math.cos(math.radians(angle_deg - arrow_angle))
        arrow_dy2 = arrow_length * math.sin(math.radians(angle_deg - arrow_angle))
        arrow_lines = []

        # 结束箭头
        if 结束箭头:
            arrow_lines += [("M", end_x - arrow_dx1, end_y - arrow_dy1),
                            (end_x, end_y), (end_x - arrow_dx2, end_y - arrow_dy2)]

            if "倒钩" not in 样式:
                arrow_lines += "Z"

        # 开始箭头
        if 开始箭头:
            arrow_lines += [("M", start_x + arrow_dx1, start_y + arrow_dy1),
                            (start_x, start_y), (start_x + arrow_dx2, start_y + arrow_dy2)]

            if "倒钩" not in 样式:
                arrow_lines += "Z"

        return lines, arrow_lines

    def 箭头线(self, 开始点, 结束点, 样式=箭头样式.倒钩, 箭头长度=10, 箭头角度=25, 填充颜色=颜色.透明,
               描边宽度=1, 描边颜色=颜色.黑色, 描边样式=None, 结束箭头=True, 开始箭头=True):
        """

        :param 开始点:
        :param 结束点:
        :param 箭头样式: 倒钩、实心、空心
        :param 箭头长度:
        :param 箭头角度:
        :param 填充颜色:
        :param 描边宽度:
        :param 描边颜色:
        :param 描边样式:
        :param 结束箭头:
        :param 开始箭头:
        :return:
        """
        # https://cn.piliapp.com/symbol/arrow/
        # 箭头样式：倒钩、左倒钩、右倒钩、实心、空心
        lines, arrow_lines = self.获取箭头路径(开始点=开始点, 结束点=结束点, 样式=样式, 箭头长度=箭头长度,
                                               箭头角度=箭头角度, 描边宽度=描边宽度, 结束箭头=结束箭头,
                                               开始箭头=开始箭头)
        if 样式 in ["空心"]:
            填充颜色 = 颜色.透明
        elif 样式 in ["实心"]:
            填充颜色 = 描边颜色
        箭头线_ = 可操作元素集合(self)
        self.连直线(路径点列表=lines, 描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度,
                    描边样式=描边样式).添加到列表(箭头线_)
        if len(arrow_lines) > 0:
            self.连直线(路径点列表=arrow_lines, 描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度).添加到列表(
                箭头线_)
        return 箭头线_.创建组合()

    def 连直线(self, 路径点列表: list = [], 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
               闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param 路径点列表:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        _元素 = self.连线(路径点列表, 描边颜色, 填充颜色, 描边宽度, 闭合, 透明度, 描边样式, id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 连线_取整数(self, 路径点列表: list, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                    闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None):
        """

        :param 路径点列表:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """

        _点列表 = []
        for 点 in 路径点列表:
            _点 = []
            for v in 点:
                if isinstance(v, str):
                    _点.append(v)
                else:
                    _点.append(int(round(v, 0)))

            _点列表.append(tuple(_点))

        print(_点列表)

        _元素 = self.连线(描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度, 闭合=闭合, 透明度=透明度,
                          描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 连线_路径列表转代码(self, 路径点列表: list, 保留位数=0):
        代码 = ""  # 开始控制点: tuple[float, float], 终点控制点: tuple[float, float], 终点
        if 保留位数 == 0:
            _round = lambda x, n: int(round(x, n))
        else:
            _round = round
        for 点命令, *点数据 in 路径点列表:
            if 点命令 == "M":
                代码 += f".移动到({_round(点数据[0], 保留位数)}, {_round(点数据[1], 保留位数)})\\\n"
            elif 点命令 == "L":
                代码 += f".画直线({_round(点数据[0], 保留位数)}, {_round(点数据[1], 保留位数)})\\\n"
            elif 点命令 == "Q":
                代码 += f".二次贝塞尔曲线({_round(点数据[0], 保留位数)}, {_round(点数据[1], 保留位数)}, {_round(点数据[2], 保留位数)}, {_round(点数据[3], 保留位数)})\\\n"
            elif 点命令 == "C":
                代码 += f".画曲线(开始控制点=({_round(点数据[0], 保留位数)}, {_round(点数据[1], 保留位数)}), 终点控制点=({_round(点数据[2], 保留位数)}, {_round(点数据[3], 保留位数)}), 终点=({_round(点数据[4], 保留位数)}, {_round(点数据[5], 保留位数)}))\\\n"
            elif 点命令 == "A":
                代码 += f".画弧线({_round(点数据[0], 保留位数)}, {_round(点数据[1], 保留位数)}, {_round(点数据[2], 保留位数)}, {_round(点数据[3], 保留位数)}, {_round(点数据[4], 保留位数)}, {_round(点数据[5], 保留位数)}, {_round(点数据[6], 保留位数)})\\\n"
            elif 点命令 == "H":
                代码 += f".画水平线({_round(点数据[0], 保留位数)})\\\n"
            elif 点命令 == "V":
                代码 += f".画垂直线({_round(点数据[0], 保留位数)})\\\n"
            elif 点命令 in ("Z", "z"):
                代码 += ".闭合()\\\n"

        print(代码)

    def 连线_调整数值(self, 路径点列表: list, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                      闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None):
        """

        :param 路径点列表:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        PATH_COMMANDS = {}
        for key in 神笔绘图板工具.PATH_COMMANDS_MAPPINGS:
            val = 神笔绘图板工具.PATH_COMMANDS_MAPPINGS[key]
            if val not in PATH_COMMANDS:
                PATH_COMMANDS[val] = key

        _点列表 = []
        for 点 in 路径点列表:
            _点 = []
            for v in 点:
                if isinstance(v, str):
                    _点.append(PATH_COMMANDS.get(v, v))
                else:
                    _点.append(round(v / 3, 2))

            _点列表.append(tuple(_点))

        print(_点列表)

        _元素 = self.连线(描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度, 闭合=闭合, 透明度=透明度,
                          描边样式=描边样式, id_=id_)

        self._注册元素到字典(id_, _元素)
        return _元素

    def 画线(self, 开始位置, 结束位置, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
             闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 线元素:
        """

        :param 开始位置:
        :param 结束位置:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """

        _元素 = 线元素(self, self.默认组)

        _元素.批量设置属性(开始位置=开始位置, 结束位置=结束位置, 填充颜色=填充颜色, 透明度=透明度,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, 闭合=闭合, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 连曲线(self, 路径点列表: list = [], 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
               闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param 路径点列表:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """

        路径点列表_ = []
        tag = "T"

        def calculate_control_points(P0, P3):
            """
            计算贝塞尔曲线的控制点
            :param P0: 起点坐标 (x0, y0)
            :param P3: 终点坐标 (x3, y3)
            :return: 两个控制点的坐标 (P1, P2)
            """
            P1 = (2 * P0[0] + P3[0]) / 3, (2 * P0[1] + P3[1]) / 3
            P2 = (P0[0] + 2 * P3[0]) / 3, (P0[1] + 2 * P3[1]) / 3
            # self.十字(x=P1[0],y=P1[1])
            # self.十字(x=P2[0], y=P2[1])
            return P1, P2

        for i, 路径点 in enumerate(路径点列表):
            if len(路径点列表_) == 0:
                路径点列表_.append(("移动", 路径点[0], 路径点[1]))
                continue

            if tag == "T":  # 平滑的二次贝塞尔曲线  x, y
                路径点列表_.append((tag, 路径点[0], 路径点[1]))
            elif tag == "C":  # 曲线 (x1, y1), (x2, y2), (x, y)
                if i < len(路径点列表) - 1:
                    x3, y3 = 路径点列表[i + 1]
                    (x1, y1), (x2, y2) = calculate_control_points((路径点[0], 路径点[1]), (x3, y3))
                    路径点列表_.append((tag, x1, y1, x2, y2, 路径点[0], 路径点[1]))
                else:
                    路径点列表_.append(("L", 路径点[0], 路径点[1]))
            elif tag in ["S", "Q"]:  # 平滑曲线 二次贝塞尔曲线 (x2, y2), (x, y)
                if i < len(路径点列表) - 1:
                    x2, y2 = 路径点列表[i + 1]
                    路径点列表_.append((tag, x2, y2, 路径点[0], 路径点[1]))
                else:
                    路径点列表_.append(("L", 路径点[0], 路径点[1]))

        _元素 = self.连线(路径点列表=路径点列表_, 描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度, 闭合=闭合,
                          透明度=透明度,
                          描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 路径(self, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
             透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        @param 描边颜色:
        @param 填充颜色:
        @param 描边宽度:
        @param 透明度:
        @param 描边样式:
        @param id_:
        @return:
        """

        _元素 = self.连线(路径点列表=[], 描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度, 透明度=透明度,
                          描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 连线(self, 路径点列表: list = [], 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
             闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param 路径点列表:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        _元素 = 路径元素(self, self.默认组)

        _元素.批量设置属性(点列表=路径点列表, 填充颜色=填充颜色, 透明度=透明度,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, 闭合=闭合, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画海浪线(self, 开始位置, 结束位置, 周期数, 波幅倍数=1, 描边颜色=颜色.黑色, 填充颜色=颜色.透明,
                 描边宽度: float = 1,
                 闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, 正方向: bool = 是,
                 id_: str = None) -> 路径元素:
        """

        @param 开始位置:
        @param 结束位置:
        @param 周期数:
        @param 波幅倍数:
        @param 描边颜色:
        @param 填充颜色:
        @param 描边宽度:
        @param 闭合:
        @param 透明度:
        @param 描边样式:
        @param 正方向:
        @param id_:
        @return:
        """
        start_x, start_y = 开始位置
        end_x, end_y = 结束位置
        step_x = (end_x - start_x) / 2 / 周期数
        step_y = (end_y - start_y) / 2 / 周期数

        if 正方向:
            路径点列表 = [("M", start_x, start_y)]
            current_x = start_x
            current_y = start_y
        else:
            路径点列表 = [("M", end_x, end_y)]
            step_x = -step_x
            step_y = -step_y
            current_x = end_x
            current_y = end_y

        for i in range(周期数):
            路径点列表.append(("A", 1, 波幅倍数, 0, 0, 1, step_x * 2 + current_x, step_y * 2 + current_y))
            current_x = step_x * 2 + current_x
            current_y = step_y * 2 + current_y

        _元素 = self.连线(路径点列表=路径点列表, 描边颜色=描边颜色, 填充颜色=填充颜色,
                          描边宽度=描边宽度, 闭合=闭合, 透明度=透明度, 描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画波浪线(self, 开始位置, 结束位置, 波浪幅度, 周期数, 描边颜色=颜色.黑色, 填充颜色=颜色.透明,
                 描边宽度: float = 1,
                 闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, 正方向: bool = 是,
                 id_: str = None) -> 路径元素:
        """

        @param 开始位置:
        @param 结束位置:
        @param 波浪幅度:
        @param 周期数:
        @param 描边颜色:
        @param 填充颜色:
        @param 描边宽度:
        @param 闭合:
        @param 透明度:
        @param 描边样式:
        @param 正方向:
        @param id_:
        @return:
        """

        start_x, start_y = 开始位置
        end_x, end_y = 结束位置
        # path_data2 = f"M {start_x},{start_y}"
        路径点列表 = [("M", start_x, start_y)]
        step_x = (end_x - start_x) / 4 / 周期数
        step_y = (end_y - start_y) / 4 / 周期数

        def _find_point_O(ax, ay, bx, by, H):
            # 计算向量AB
            AB = np.array([bx - ax, by - ay])

            # 计算AB的长度
            AB_length = np.linalg.norm(AB)

            # 避免除零错误
            if AB_length == 0:
                raise ValueError("A and B are the same point")

                # 构造与AB垂直的向量（未归一化）
            # 注意：这里我们选择了AB的逆时针旋转90度的方向作为垂直方向
            normal_vector_unnormalized = np.array([-AB[1], AB[0]])

            # 对垂直向量进行归一化
            normal_vector = normal_vector_unnormalized / np.linalg.norm(normal_vector_unnormalized)

            # 计算点O的坐标
            # 这里我们取AB的中点，然后沿着normal_vector方向移动H距离
            mid_point = np.array([(ax + bx) / 2, (ay + by) / 2])
            O_point = mid_point + normal_vector * H

            return O_point[0], O_point[1]

        # 波浪幅度 = start_y - 波浪幅度
        current_x = start_x
        current_y = start_y
        for i️ in range(周期数):
            if 正方向:
                ox, oy = _find_point_O(current_x, current_y, step_x * 2 + current_x, step_y * 2 + current_y, 波浪幅度)
            else:
                ox, oy = _find_point_O(step_x * 2 + current_x, step_y * 2 + current_y, current_x, current_y, 波浪幅度)
            # path_data += f" Q{ox},{oy} {step_x * 2 + current_x},{step_y * 2 + current_y}"
            路径点列表.append(("Q", ox, oy, step_x * 2 + current_x, step_y * 2 + current_y))
            # path_data += f" Q{step_x + current_x},{波浪幅度} {step_x * 2 + current_x},{step_y * 2 + current_y}"
            # path_data += f" T{step_x * 4 + current_x},{step_y * 4 + current_y}"
            路径点列表.append(("T", step_x * 4 + current_x, step_y * 4 + current_y))
            current_x = step_x * 4 + current_x
            current_y = step_y * 4 + current_y

        _元素 = self.连线(路径点列表=路径点列表, 描边颜色=描边颜色, 填充颜色=填充颜色,
                          描边宽度=描边宽度, 闭合=闭合, 透明度=透明度, 描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 十字(self, x: float, y: float, 宽度: float = 5, 高度: float = 5, 颜色: str = 颜色.黑色,
             描边宽度: float = 1, id_: str = None) -> 路径元素:
        """

        @param x:
        @param y:
        @param 宽度:
        @param 高度:
        @param 颜色:
        @param 描边宽度:
        @param id_:
        @return:
        """
        line1 = [("M", x - 宽度 / 2, y), (x + 宽度 / 2, y), ("M", x, y - 高度 / 2), (x, y + 高度 / 2)]
        _元素 = self.连线(line1, 填充颜色=颜色, 描边颜色=颜色, 描边宽度=描边宽度)
        self._注册元素到字典(id_, _元素)
        return _元素

    def _构建水平线点列表(self, x1: float, x2: float, y1: float, y2: float = None, 数量: int = 2):
        """

        :param x1:
        :param x2:
        :param y1:
        :param y2:
        :param 数量:
        :return:
        """
        points = [("M", x1, y1), ("L", x2, y1)]
        if y2 is not None:
            if isinstance(y2, list):
                pass
            else:
                if 数量 == 2:
                    points += [("M", x1, y2), (x2, y2)]
                elif 数量 > 2:
                    y间隔 = (y2 - y1) / (数量 - 1)
                    for i in range((数量 - 1)):
                        points += [("M", x1, y1 + y间隔 * (i + 1)), ("L", x2, y1 + y间隔 * (i + 1))]
        return points

    def _构建垂直线点列表(self, y1: float, y2: float, x1: float, x2: float = None, 数量: int = 2):
        """

        :param y1:
        :param y2:
        :param x1:
        :param x2:
        :param 数量:
        :return:
        """
        points = [("M", x1, y1), ("L", x1, y2)]
        if x2 is not None:
            if isinstance(x2, list):
                for _x in x2:
                    points += [("M", _x, y1), (_x, y2)]
            else:
                if 数量 == 2:
                    points += [("M", x2, y1), (x2, y2)]
                elif 数量 > 2:
                    x间隔 = (x2 - x1) / (数量 - 1)
                    for i in range((数量 - 1)):
                        points += [("M", x1 + x间隔 * (i + 1), y1), ("L", x1 + x间隔 * (i + 1), y2)]
        return points

    def 画水平线(self, x1: float, y1: float, x2: float, y2: float = None, 数量: int = 2,
                 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1, 描边样式: str = None,
                 透明度: float = 1.0, id_: str = None) -> 路径元素:
        """

        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param 数量:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """
        points = self._构建水平线点列表(x1, x2, y1, y2, 数量)
        _元素 = self.连直线(points, 描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度,
                            透明度=透明度, 描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画垂直线(self, y1: float, y2: float, x1: float, x2: float = None, 数量: int = 2,
                 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1, 描边样式: str = None,
                 透明度: float = 1.0, id_: str = None) -> 路径元素:
        """

        :param y1:
        :param y2:
        :param x1:
        :param x2:
        :param 数量:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """
        points = self._构建垂直线点列表(y1, y2, x1, x2, 数量)
        _元素 = self.连直线(points, 描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度, 透明度=透明度,
                            描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画表格(self, x: float, y: float, 列宽: [list, float], 行高: [list, float], 行数: int, 列数: int = 1,
               描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1, 描边样式=None,
               透明度: float = 1.0, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 列宽:
        :param 行高:
        :param 行数:
        :param 列数:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """

        if isinstance(列宽, list):
            列宽集合 = 列宽
        else:
            列宽集合 = [列宽] * 列数

        if isinstance(行高, list):
            行高集合 = 行高
        else:
            行高集合 = [行高] * 行数

        x2 = sum(列宽集合) + x
        y2 = sum(行高集合) + y

        # points_h = self._构建水平线点列表(x1=x, x2=x2, y1=y, y2=y2, 数量=行数 + 1)
        points_h = []
        points_h += [("M", x, y), ("L", x2, y)]
        row_y_count = y

        for row_idx, 行高 in 索引列举(行高集合):
            row_y_count += 行高
            points_h += [("M", x, row_y_count), ("L", x2, row_y_count)]

        points_v = []
        points_v += [("M", x, y), ("L", x, y2)]
        col_x_count = x

        for col_idx, 列宽 in 索引列举(列宽集合):
            col_x_count += 列宽
            points_v += [("M", col_x_count, y), ("L", col_x_count, y2)]

        points = points_h + points_v
        _元素 = self.连直线(points, 描边颜色=描边颜色, 填充颜色=填充颜色, 描边宽度=描边宽度, 透明度=透明度,
                            描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    # endregion

    # region 形状
    def 矩形背景(self, 填充颜色, 透明度: float = 1.0, id_: str = None) -> 矩形元素:
        """

        @param 填充颜色:
        @param 透明度:
        @param id_:
        @return:
        """
        _元素 = self.画矩形(x=0, y=0, 宽=self.宽, 高=self.高,
                            填充颜色=填充颜色, 描边宽度=0, 透明度=透明度, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画矩形(self, x: float, y: float, 宽: float, 高: float, 圆角半径: float = None,
               填充颜色=颜色.透明, 描边颜色=颜色.黑色, 描边宽度: float = 1, 描边样式: str = None,
               透明度: float = 1.0, id_: str = None) -> 矩形元素:
        """

        :param x:
        :param y:
        :param 宽:
        :param 高:
        :param 圆角半径:
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """
        _元素 = 矩形元素(self, self.默认组)
        _元素.批量设置属性(x=x, y=y, 宽=宽, 高=高, 填充颜色=填充颜色, 透明度=透明度,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, 圆角半径=圆角半径, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画圆(self, x: float, y: float, 半径: float, 填充颜色=颜色.透明,
             描边颜色=颜色.黑色, 描边宽度: float = 1.0, 描边样式: str = None,
             透明度: float = 1.0, id_: str = None) -> 圆元素:
        """

        :param x:
        :param y:
        :param 半径:
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """
        _元素 = 圆元素(self, self.默认组)
        _元素.批量设置属性(x=x, y=y, 半径=半径, 填充颜色=填充颜色, 透明度=透明度,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画椭圆(self, x: float, y: float, 半径: Union[float, Tuple[float, float]],
               填充颜色=颜色.透明, 描边颜色=颜色.黑色, 描边宽度: float = 1.0, 描边样式: str = None,
               透明度: float = 1.0, id_: str = None) -> 椭圆元素:
        """

        :param x:
        :param y:
        :param 半径: 格式为 x轴向半径 和 y轴向半径 (rx, ry)
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """
        _元素 = 椭圆元素(self, self.默认组)
        if isinstance(半径, tuple):
            rx, ry = 半径
        else:
            rx, ry = 半径, 半径

        _元素.批量设置属性(x=x, y=y, rx=rx, ry=ry, 填充颜色=填充颜色, 透明度=透明度,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画爱心(self, x: float, y: float, 半径大小, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
               闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        _元素 = self.连线(路径点列表=爱心路径(x=x, y=y, 半径大小=半径大小),
                          描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                          描边宽度=描边宽度,
                          描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画菱型(self, x: float, y: float, 半径, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
               闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        _元素 = self.连线(路径点列表=菱型路径(x=x, y=y, 半径=半径),
                          描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                          描边宽度=描边宽度,
                          描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画折线(self, 顶点列表: list, 填充颜色=颜色.透明, 描边颜色=颜色.黑色, 描边宽度: float = 1, 描边样式: str = None,
               透明度: float = 1.0, id_: str = None) -> 折线元素:
        """

        :param 顶点列表:
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """
        _元素 = 折线元素(self, self.默认组)
        _元素.批量设置属性(顶点列表=顶点列表, 填充颜色=填充颜色, 透明度=透明度,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画多边形(self, 顶点列表: list, 填充颜色=颜色.透明, 描边颜色=颜色.黑色, 描边宽度: float = 1,
                 描边样式: str = None,
                 透明度: float = 1.0, id_: str = None) -> 多边形元素:
        """

        :param 顶点列表:
        :param 填充颜色:
        :param 描边颜色:
        :param 描边宽度:
        :param 描边样式:
        :param 透明度:
        :param id_:
        :return:
        """
        _元素 = 多边形元素(self, self.默认组)
        _元素.批量设置属性(顶点列表=顶点列表, 填充颜色=填充颜色, 透明度=透明度,
                           描边颜色=描边颜色, 描边宽度=描边宽度, 描边样式=描边样式, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 画正N边形(self, x: float, y: float, 半径大小, N, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                  闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param N:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N边形路径(x=x, y=y, 半径大小=半径大小, n=N),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画正三边形(self, x: float, y: float, 半径大小, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                   闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N边形路径(x=x, y=y, 半径大小=半径大小, n=3),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画正四边形(self, x: float, y: float, 半径大小, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                   闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N边形路径(x=x, y=y, 半径大小=半径大小, n=4, 旋转角度=45),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画正方形(self, x: float, y: float, 边长, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                 闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 大小:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        半径大小 = 边长 / math.sqrt(2)
        return self.连线(路径点列表=N边形路径(x=x, y=y, 半径大小=半径大小, n=4, 旋转角度=45),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画正五边形(self, x: float, y: float, 半径大小, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                   闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N边形路径(x=x, y=y, 半径大小=半径大小, n=5),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画正六边形(self, x: float, y: float, 半径大小, 描边颜色=颜色.黑色, 填充颜色=颜色.透明, 描边宽度: float = 1,
                   闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N边形路径(x=x, y=y, 半径大小=半径大小, n=6, 旋转角度=30),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画N角星(self, x: float, y: float, 半径大小, N, 内角点占比=0.382, 描边颜色=颜色.黑色, 填充颜色=颜色.透明,
                描边宽度: float = 1,
                闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param N:
        :param 内角点占比:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N角星路径(x=x, y=y, 半径大小=半径大小, n=N, 内角点占比=内角点占比),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画三角星(self, x: float, y: float, 半径大小, 内角点占比=0.3, 描边颜色=颜色.黑色, 填充颜色=颜色.透明,
                 描边宽度: float = 1,
                 闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 内角点占比:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N角星路径(x=x, y=y, 半径大小=半径大小, n=3, 内角点占比=内角点占比),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画四角星(self, x: float, y: float, 半径大小, 内角点占比=0.35, 描边颜色=颜色.黑色, 填充颜色=颜色.透明,
                 描边宽度: float = 1,
                 闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 内角点占比:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N角星路径(x=x, y=y, 半径大小=半径大小, n=4, 内角点占比=内角点占比),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画五角星(self, x: float, y: float, 半径大小, 内角点占比=0.382, 描边颜色=颜色.黑色, 填充颜色=颜色.透明,
                 描边宽度: float = 1,
                 闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 内角点占比:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N角星路径(x=x, y=y, 半径大小=半径大小, n=5, 内角点占比=内角点占比),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    def 画六角星(self, x: float, y: float, 半径大小, 内角点占比=0.6, 描边颜色=颜色.黑色, 填充颜色=颜色.透明,
                 描边宽度: float = 1,
                 闭合: bool = 否, 透明度: float = 1.0, 描边样式: str = None, id_: str = None) -> 路径元素:
        """

        :param x:
        :param y:
        :param 半径大小:
        :param 内角点占比:
        :param 描边颜色:
        :param 填充颜色:
        :param 描边宽度:
        :param 闭合:
        :param 透明度:
        :param 描边样式:
        :param id_:
        :return:
        """
        return self.连线(路径点列表=N角星路径(x=x, y=y, 半径大小=半径大小, n=6, 内角点占比=内角点占比),
                         描边颜色=描边颜色, 填充颜色=填充颜色, 闭合=闭合, 透明度=透明度,
                         描边宽度=描边宽度,
                         描边样式=描边样式, id_=id_)

    # endregion

    # region 图片
    def SVG贴图(self, 图片文件: str, x: float = 0, y: float = 0, 宽: float = None, 高: float = None,
                透明度: float = 1.0, id_: str = None) -> SVG图元素:
        """

        :param 图片文件:
        :param x:
        :param y:
        :param 宽:
        :param 高:
        :param 透明度:
        :param id_:
        :return:
        """
        _元素 = SVG图元素(self, self.默认组)
        _元素.批量设置属性(图片文件=图片文件, x=x, 透明度=透明度, y=y, 宽=宽, 高=高, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    def 导入SVG为组(self, SVG图片, x=0, y=0, 缩放=None, 修正原生路径=否) -> 元素组:
        from 神笔码靓.神笔库.SVG文件转元素 import SVG文件转元素工具
        elememts = SVG文件转元素工具(self).SVG文件转元素(SVG图片)
        if 修正原生路径:
            for elememt in elememts:
                if isinstance(elememt, 路径元素):
                    elememt.原生路径修正()

        图片名, _ = os.path.splitext(os.path.basename(SVG图片))
        组合 = self.创建组合(元素列表=elememts, id_=f"{self._gen_id(图片名)}")
        if x != 0 or y != 0:
            组合 = 组合.平移(x, y)
        if 缩放 is not None:
            if isinstance(缩放, tuple):
                组合 = 组合.缩放(缩放[0], 缩放[1])
            else:
                组合 = 组合.缩放(缩放)
        return 组合

    def 导入SVG为模板(self, SVG图片, x=0, y=0, 缩放=None, 修正原生路径=否) -> 元素模板:
        g = self.导入SVG为组(SVG图片, x, y, 缩放, 修正原生路径)
        return self.创建模板(元素列表=[g])

    def 贴图(self, 图片文件: [str, object], x: float = 0, y: float = 0, 宽: float = None, 高: float = None,
             透明度: float = 1.0, id_: str = None) -> 图元素:
        """

        :param 图片文件:
        :param x:
        :param y:
        :param 宽:
        :param 高:
        :param 透明度:
        :param id_:
        :return:
        """
        _元素 = 图元素(self, self.默认组)
        _元素.批量设置属性(图片文件=图片文件, x=x, 透明度=透明度, y=y, 宽=宽, 高=高, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    # endregion

    # region 模板/组合/图案/克隆
    def _加载神笔模板(self, 搜索目录, 神笔模板列表=[]):
        if 搜索目录 is None:
            return 神笔模板列表

        from 神笔码靓.神笔库 import 神笔模板
        from pathlib import Path
        # 获取当前脚本所在的目录
        current_path = Path(__file__).resolve().parent.parent

        # 获取当前脚本所在的项目根目录
        root_path = current_path.parent

        for fd in 获取目录文件列表(搜索目录):
            if fd.startswith("__"):
                continue
            full_apth = os.path.join(搜索目录, fd)
            if os.path.isdir(full_apth):
                self._加载神笔模板(full_apth, 神笔模板列表)
                continue
            if fd.endswith(".py") and "神笔模板" in fd and not fd.startswith("__"):
                # if fd.endswith(".py") and not fd.startswith("__"):
                module_name = fd[:-3]
                try:
                    搜索目录_ = os.path.relpath(搜索目录, root_path)
                except Exception as e:
                    搜索目录_ = "神笔模板"

                module_name = 搜索目录_.replace("../", "").replace("/", ".").replace("\\", ".") + "." + module_name
                try:
                    module = importlib.import_module(module_name)
                    for name, obj in module.__dict__.items():
                        if isinstance(obj, type) and issubclass(obj, 神笔模板) and obj != 神笔模板:
                            _instance = obj(self)
                            _模板ID = _instance.模板ID()
                            神笔模板列表.append((_模板ID, _instance))
                except Exception as e:
                    print(e)

        return 神笔模板列表

    def _加载复用模板支持(self):
        _码靓库目录 = 码靓库目录()
        _神笔库目录 = 神笔库目录()
        _神笔模板目录 = 神笔模板目录()

        from pathlib import Path
        current_path = Path(__file__).resolve().parent.parent

        if _码靓库目录 is None:
            _码靓库目录 = os.path.join(current_path, "码靓库")

        if _神笔库目录 is None:
            _神笔库目录 = os.path.join(current_path, "神笔库")

        _加载神笔模板 = []
        _加载神笔模板 = self._加载神笔模板(_神笔库目录, 神笔模板列表=_加载神笔模板)
        _加载神笔模板 = self._加载神笔模板(_码靓库目录, 神笔模板列表=_加载神笔模板)
        _加载神笔模板 = self._加载神笔模板(_神笔模板目录, 神笔模板列表=_加载神笔模板)

        for 模板ID, 实例 in _加载神笔模板:
            if 模板ID is None:
                continue
            if 模板ID in self._复用模板支持.keys():
                raise Exception(f"模板ID“{模板ID}”重复了")

            self._复用模板支持[模板ID] = 实例

    def __getitem__(self, 模板ID):
        return self.神笔模板(模板ID=模板ID)

    def 神笔模板(self, 模板ID=None, **kwargs) -> 元素模板:
        if len(self._复用模板支持) == 0:
            self._加载复用模板支持()

        err_msg = "支持的模板ID有：%s" % (", ".join(self._复用模板支持.keys()))

        if 模板ID is None:
            raise Exception(err_msg)

        if 模板ID not in self._复用模板支持.keys():
            raise Exception(f"模板ID“{模板ID}”不存在。{err_msg}")

        key = (f"神笔模板_{模板ID}_") + str(kwargs)
        if key in self.缓存:
            return self.缓存[key]

        _模板对象支持 = self._复用模板支持[模板ID]
        _模板对象支持.模板参数(**kwargs)
        _模板对象支持.初始化()
        _模板元素列表 = _模板对象支持.获取元素列表()
        if _模板元素列表 is None or not isinstance(_模板元素列表, list):
            return None
        if len(_模板元素列表) == 0:
            return None
        _模板对象支持.模板创建前()
        模板_ = self.创建模板(元素列表=_模板元素列表, id_=_模板对象支持.id_())
        setattr(模板_, "神笔模板返回值", _模板对象支持.返回值)
        _模板对象支持.模板创建后(模板_)
        self.缓存[key] = 模板_
        return 模板_

    def 创建模板(self, id_: str = None, class_name: str = None, style: str = None,
                 样式类名: str = None, 样式串: str = None, 元素列表: list = []) -> 元素模板:
        """

        :param id:
        :param class_name:
        :param style:
        :param 元素列表:
        :return:
        """
        _元素组 = 元素模板(self, self.默认组)
        _元素组.批量设置属性(元素列表=元素列表, class_name=class_name, style=style,
                             样式类名=样式类名, 样式串=样式串, id_=id_)
        self._注册元素到字典(id_, _元素组)
        return _元素组

    def 创建组合(self, class_name: str = None, style=None, 元素列表: list = [],
                 样式类名: str = None, 样式串: str = None, id_: str = None) -> 元素组:
        """

        :param class_name:
        :param style:
        :param 元素列表:
        :param id_:
        :return:
        """
        _元素组 = 元素组(self, self.默认组)
        _元素组.批量设置属性(元素列表=元素列表, class_name=class_name, style=style,
                             样式类名=样式类名, 样式串=样式串, id_=id_)
        self._注册元素到字典(id_, _元素组)
        return _元素组

    def 创建图案(self, x: float, y: float, 宽: float, 高: float, class_name: str = None,
                 元素列表: list = [], id_: str = None) -> 元素图案:
        """

        :param x:
        :param y:
        :param 宽:
        :param 高:
        :param class_name:
        :param 元素列表:
        :param id_:
        :return:
        """
        _元素组 = 元素图案(self, self.默认组)
        _元素组.批量设置属性(元素列表=元素列表, x=x, y=y, 宽=宽, 高=高, class_name=class_name, id_=id_)
        self._注册元素到字典(id_, _元素组)
        return _元素组

    def 复制元素(self, 对象元素: 元素, x: float = None, y: float = None, 透明度: float = 1.0,
                 id_: str = None) -> 复用元素:
        """

        :param 对象元素:
        :param x:
        :param y:
        :param 透明度:
        :param id_:
        :return:
        """
        if x is None:
            x = 0
        if y is None:
            y = 0
        _元素 = 复用元素(self, self.默认组)
        _元素.批量设置属性(对象元素=对象元素, x=x, 透明度=透明度, y=y, id_=id_)
        self._注册元素到字典(id_, _元素)
        return _元素

    # region 元素排列

    def 水平排列(self, 元素集合, 元素间距: float) -> 可操作元素集合:
        """

        @param 元素集合:
        @param 元素间距:
        @return:
        """
        return self.排列.水平排列(元素集合=元素集合, 元素间距=元素间距)

    def 垂直排列(self, 元素集合, 元素间距: float) -> 可操作元素集合:
        """

        @param 元素集合:
        @param 元素间距:
        @return:
        """
        return self.排列.垂直排列(元素集合=元素集合, 元素间距=元素间距)

    def 网格水平排列(self, 元素集合, 最大列数, 列间距: float, 行间距: float) -> 可操作元素集合:
        """

        @param 元素集合:
        @param 最大列数:
        @param 列间距:
        @param 行间距:
        @return:
        """
        return self.排列.网格水平排列(元素集合=元素集合, 最大列数=最大列数, 列间距=列间距, 行间距=行间距)

    def 网格垂直排列(self, 元素集合, 最大行数, 行间距: float, 列间距: float) -> 可操作元素集合:
        """

        @param 元素集合:
        @param 最大行数:
        @param 行间距:
        @param 列间距:
        @return:
        """
        return self.排列.网格垂直排列(元素集合=元素集合, 最大行数=最大行数, 行间距=行间距, 列间距=列间距)

    def 环绕排列(self, 元素集合, 环绕中心点: tuple[float, float] = None, 间距角: float = None,
                 顺时针: bool = 是, 元素跟随旋转: bool = 是) -> 可操作元素集合:
        """

        @param 元素集合:
        @param 环绕中心点:
        @param 间距角:
        @param 顺时针:
        @param 元素跟随旋转:
        @return:
        """

        return self.排列.环绕排列(元素集合=元素集合, 环绕中心点=环绕中心点, 间距角=间距角,
                                  顺时针=顺时针, 元素跟随旋转=元素跟随旋转)

    # endregion

    # region 元素重复
    def 环绕重复(self, 重复元素, 重复数量: int, 环绕中心点: tuple[float, float] = None, 间距角: float = None,
                 顺时针: bool = 是, 元素跟随旋转: bool = 是, 元素创造前回调=None,
                 元素创造后回调=None) -> 可操作元素集合:
        """

        @param 重复元素: 元素类型、列表类型 或 函数
        @param 重复数量:
        @param 环绕中心点:
        @param 间距角:
        @param 顺时针:
        @param 元素跟随旋转:
        @param 元素创造前回调:
        @param 元素创造后回调:
        @return:
        """
        return self.重复.环绕重复(重复元素=重复元素, 重复数量=重复数量, 环绕中心点=环绕中心点, 间距角=间距角,
                                  顺时针=顺时针, 元素跟随旋转=元素跟随旋转, 元素创造前回调=元素创造前回调,
                                  元素创造后回调=元素创造后回调)

    def 网格重复(self, 重复元素, 重复列数, 列间距: float, 重复行数, 行间距: float,
                 网格类型: 网格重复类型 = None) -> 可操作元素集合:
        """

        @param 重复元素: 元素类型、列表类型 或 函数
        @param 重复列数:
        @param 列间距:
        @param 重复行数:
        @param 行间距:
        @param 网格类型:
        @return:
        """
        return self.重复.网格重复(重复元素=重复元素, 重复列数=重复列数, 列间距=列间距,
                                  重复行数=重复行数, 行间距=行间距, 网格类型=网格类型)

    def 垂直方向重复(self, 重复元素, 重复数量: int, 元素间距: float, 上中下="中", 中间空着=否) -> 可操作元素集合:
        """

        @param 重复元素: 元素类型、列表类型 或 函数
        @param 重复数量:
        @param 元素间距:
        @param 上中下:
        @param 中间空着:
        @return:
        """
        return self.重复.垂直方向重复(重复元素=重复元素, 重复数量=重复数量, 元素间距=元素间距, 上中下=上中下,
                                      中间空着=中间空着)

    def 水平方向重复(self, 重复元素, 重复数量: int, 元素间距: float, 左中右="中", 中间空着=否) -> 可操作元素集合:
        """

        @param 重复元素: 元素类型、列表类型 或 函数
        @param 重复数量:
        @param 元素间距:
        @param 左中右:
        @param 中间空着:
        @return:
        """
        return self.重复.水平方向重复(重复元素=重复元素, 重复数量=重复数量, 元素间距=元素间距, 左中右=左中右,
                                      中间空着=中间空着)

    # endregion
    # endregion
    # endregion

    # region 脚本支持
    def 增加JS代码(self, JS代码):
        self.jscripts.append(JS代码)

    def 处理JavaScript(self):
        from svgwrite import container
        for js in self.jscripts:
            script = container.Script(content=js)
            self.dwg.add(script)

    # endregion

    # region 样式
    def 设置背景色(self, 背景色):
        if 背景色 != 颜色.白色:
            if "style" in self.dwg.attribs:
                style = self.dwg.attribs["style"]
            else:
                style = ""
            self.dwg.attribs["style"] = f"background-color: {背景色};" + style

    def 创建线性渐变色(self, 开始位置, 结束位置, 开始颜色, 结束颜色,
                       开始偏移='0%', 结束偏移='100%',
                       开始透明度=1.0, 结束透明度=1.0, 增加渐变中间点: list = [], id_: str = None) -> 线性渐变色:
        """

        :param 开始位置:
        :param 结束位置:
        :param 开始颜色:
        :param 结束颜色:
        :param 开始偏移:
        :param 结束偏移:
        :param 开始透明度:
        :param 结束透明度:
        :param 增加渐变中间点:
        :param id_:
        :return:
        """
        return self.样式.创建线性渐变色(开始位置, 结束位置, 开始颜色, 结束颜色,
                                        开始偏移=开始偏移, 结束偏移=结束偏移,
                                        开始透明度=开始透明度, 结束透明度=结束透明度, 增加渐变中间点=增加渐变中间点,
                                        id_=id_)

    def 创建径向渐变色(self, 渐变开始中心点, 渐变半径, 开始颜色, 结束颜色,
                       开始偏移='0%', 结束偏移='100%',
                       开始透明度=1.0, 结束透明度=1.0, 渐变的焦点=None,
                       增加渐变中间点: list = [], id_: str = None
                       # , 旋转角度=0, 缩放=1, 平移=None

                       ) -> 径向渐变色:
        """

        :param 渐变开始中心点:
        :param 渐变半径:
        :param 开始颜色:
        :param 结束颜色:
        :param 开始偏移:
        :param 结束偏移:
        :param 开始透明度:
        :param 结束透明度:
        :param 渐变的焦点:
        :param 增加渐变中间点:
        :param id_:
        :param 旋转角度:
        :param 缩放:
        :param 平移:
        :return:
        """

        return self.样式.创建径向渐变色(渐变开始中心点, 渐变半径, 开始颜色, 结束颜色,
                                        开始偏移=开始偏移, 结束偏移=结束偏移,
                                        开始透明度=开始透明度, 结束透明度=结束透明度, 渐变的焦点=渐变的焦点,
                                        增加渐变中间点=增加渐变中间点, id_=id_
                                        # , 旋转角度=旋转角度, 缩放=缩放, 平移=平移
                                        )

    def 彩虹渐变点(self, 关键点偏移=None, 关键点透明度=None, 彩虹七色=None):
        """

        :param 关键点偏移: 关键点个数只支持 1、2、3、7，请参照：<br>
                 0.5<br>
        ──────────┴──────────  一个关键点（0.5:中间位置的偏移）<br>
            0.1      0.9<br>
        ─────┴────────┴──────  两个关键点（0.1:开始偏移,中间位置固定为 0.5, 0.9:结束偏移）<br>
        0.1      0.5       0.9<br>
        ┴─────────┴─────────┴  三个关键点（0.1:开始偏移,0.5:中间位置偏移, 0.9:结束偏移）<br>
        0.1               0.9<br>
        ┴──┴──┴──┴──┴──┴──┴    七个关键点（彩虹7种颜色的偏移，红橙黄绿青蓝紫，0.1:红色偏移, 0.9:紫色偏移）<br>
        :param 关键点透明度: 透明度个数只支持 1、2、3、7，请参照：<br>
        0.5      0.5       0.5<br>
        └─────────┴─────────┘  一个值: 全部透明度为0.5<br>
        0.1      0.5       1.0<br>
        └─────────┴─────────┘  两个值: 决定开始透明度值和结束透明度，中间的透明度线性平分<br>
        0.1      0.5       1.0<br>
        └─────────┴─────────┘  三个值: 决定开始透、中间、结束透明度，中间的透明度线性平分<br>
        0.1                0.9<br>
        └──┴───┴──┴──┴──┴───┘  七个值（彩虹7种颜色的透明度，红橙黄绿青蓝紫，0.1:红色透明度, 0.9:紫色透明度）<br>
        :param 彩虹七色: 自定义彩虹的7种颜色
        :return:
        """
        return self.样式.彩虹渐变点(关键点偏移, 关键点透明度, 彩虹七色=彩虹七色)

    def 创建彩虹线性渐变色(self, 开始位置, 结束位置, id_: str = None,
                           关键点偏移=None, 关键点透明度=None, 彩虹七色=None) -> 线性渐变色:
        """

        :param 开始位置:
        :param 结束位置:
        :param id_:
        :param 关键点偏移: 关键点个数只支持 1、2、3、7，请参照：<br>
                 0.5<br>
        ──────────┴──────────  一个关键点（0.5:中间位置的偏移）<br>
            0.1      0.9<br>
        ─────┴────────┴──────  两个关键点（0.1:开始偏移,中间位置固定为 0.5, 0.9:结束偏移）<br>
        0.1      0.5       0.9<br>
        ┴─────────┴─────────┴  三个关键点（0.1:开始偏移,0.5:中间位置偏移, 0.9:结束偏移）<br>
        0.1               0.9<br>
        ┴──┴──┴──┴──┴──┴──┴    七个关键点（彩虹7种颜色的偏移，红橙黄绿青蓝紫，0.1:红色偏移, 0.9:紫色偏移）<br>
        :param 关键点透明度: 透明度个数只支持 1、2、3、7，请参照：<br>
        0.5      0.5       0.5<br>
        └─────────┴─────────┘  一个值: 全部透明度为0.5<br>
        0.1      0.5       1.0<br>
        └─────────┴─────────┘  两个值: 决定开始透明度值和结束透明度，中间的透明度线性平分<br>
        0.1      0.5       1.0<br>
        └─────────┴─────────┘  三个值: 决定开始透、中间、结束透明度，中间的透明度线性平分<br>
        0.1                0.9<br>
        └──┴───┴──┴──┴──┴───┘  七个值（彩虹7种颜色的透明度，红橙黄绿青蓝紫，0.1:红色透明度, 0.9:紫色透明度）<br>
        :param 彩虹七色: 自定义彩虹的7种颜色
        :return:
        """
        彩虹渐变点 = self.彩虹渐变点(关键点偏移, 关键点透明度, 彩虹七色=彩虹七色)

        开始颜色 = 彩虹渐变点[0]["颜色"]
        结束颜色 = 彩虹渐变点[-1]["颜色"]
        开始偏移 = 彩虹渐变点[0]["偏移"]
        结束偏移 = 彩虹渐变点[-1]["偏移"]
        开始透明度 = 彩虹渐变点[0].get("透明度", 1.0)
        结束透明度 = 彩虹渐变点[-1].get("透明度", 1.0)

        return self.创建线性渐变色(开始位置=开始位置, 结束位置=结束位置, 开始颜色=开始颜色, 结束颜色=结束颜色,
                                   开始偏移=开始偏移, 结束偏移=结束偏移, 开始透明度=开始透明度, 结束透明度=结束透明度,
                                   增加渐变中间点=彩虹渐变点[1:-1], id_=id_)

    def 创建彩虹径向渐变色(self, 渐变开始中心点, 渐变半径,
                           渐变的焦点=None, id_: str = None, 关键点偏移=None, 关键点透明度=None, 彩虹七色=None):
        """

        :param 渐变开始中心点:
        :param 渐变半径:
        :param 渐变的焦点:
        :param id_:
              :param 关键点偏移: 关键点个数只支持 1、2、3、7，请参照：<br>
                 0.5<br>
        ──────────┴──────────  一个关键点（0.5:中间位置的偏移）<br>
            0.1      0.9<br>
        ─────┴────────┴──────  两个关键点（0.1:开始偏移,中间位置固定为 0.5, 0.9:结束偏移）<br>
        0.1      0.5       0.9<br>
        ┴─────────┴─────────┴  三个关键点（0.1:开始偏移,0.5:中间位置偏移, 0.9:结束偏移）<br>
        0.1               0.9<br>
        ┴──┴──┴──┴──┴──┴──┴    七个关键点（彩虹7种颜色的偏移，红橙黄绿青蓝紫，0.1:红色偏移, 0.9:紫色偏移）<br>
        :param 关键点透明度: 透明度个数只支持 1、2、3、7，请参照：<br>
        0.5      0.5       0.5<br>
        └─────────┴─────────┘  一个值: 全部透明度为0.5<br>
        0.1      0.5       1.0<br>
        └─────────┴─────────┘  两个值: 决定开始透明度值和结束透明度，中间的透明度线性平分<br>
        0.1      0.5       1.0<br>
        └─────────┴─────────┘  三个值: 决定开始透、中间、结束透明度，中间的透明度线性平分<br>
        0.1                0.9<br>
        └──┴───┴──┴──┴──┴───┘  七个值（彩虹7种颜色的透明度，红橙黄绿青蓝紫，0.1:红色透明度, 0.9:紫色透明度）<br>
        :param 彩虹七色: 自定义彩虹的7种颜色
        :return:
        """
        彩虹渐变点 = self.彩虹渐变点(关键点偏移, 关键点透明度, 彩虹七色=彩虹七色)

        开始颜色 = 彩虹渐变点[0]["颜色"]
        结束颜色 = 彩虹渐变点[6]["颜色"]
        开始偏移 = 彩虹渐变点[0]["偏移"]
        结束偏移 = 彩虹渐变点[6]["偏移"]
        开始透明度 = 彩虹渐变点[0].get("透明度", 1.0)
        结束透明度 = 彩虹渐变点[6].get("透明度", 1.0)

        return self.创建径向渐变色(渐变开始中心点=渐变开始中心点, 渐变半径=渐变半径, 开始颜色=开始颜色,
                                   结束颜色=结束颜色,
                                   开始偏移=开始偏移, 结束偏移=结束偏移, 开始透明度=开始透明度, 结束透明度=结束透明度,
                                   渐变的焦点=渐变的焦点,
                                   增加渐变中间点=彩虹渐变点[1:6], id_=id_)

    def 创建黄金线性渐变色(self, 开始位置=(0, 0), 结束位置=(640, 640),
                           黄金色1="#DFB802", 黄金色2="#FFF6CD", 变化频率=20) -> 线性渐变色:
        """

        :param 开始位置:
        :param 结束位置:
        :param 黄金色1:
        :param 黄金色2:
        :param 变化频率:
        :return:
        """
        # 黄金色 "#DFB802", "#FEEEA1"
        # 黄金色 "#FFD200", "#813919"
        # 黄金色 "#DFB802", "#FFF6CD"

        黄金渐变中间点 = []
        循环 = 变化频率
        for i in range(1, 循环):
            黄金色 = 黄金色1 if i % 2 == 0 else 黄金色2
            黄金渐变中间点.append({"偏移": f"{i * round(100 / 循环, 1)}%", "颜色": 黄金色, "透明度": 1})

        黄金渐变色 = self.创建线性渐变色(开始颜色=黄金色1, 结束颜色=黄金色1,
                                         开始位置=开始位置,
                                         结束位置=结束位置,
                                         开始透明度=1, 结束透明度=1, 增加渐变中间点=黄金渐变中间点)
        return 黄金渐变色

    # endregion

    def 修改绘图板大小(self, 宽=None, 高=None):
        if 宽 is not None:
            self.dwg.attribs["width"] = 宽
        if 高 is not None:
            self.dwg.attribs["height"] = 高

    def 写网址信息(self, x, y, 字体大小, 填充颜色=颜色.黑色, 水平基线对齐=文字水平基线对齐.结束点对齐):
        return self.写字(x=x, y=y,
                         # 文字="https://gitcode.net/pythoncr",
                         文字="https://gitee.com/pythoncr",
                         水平基线对齐=水平基线对齐,
                         字体=系统字体.Verdana, 字体大小=字体大小, 填充颜色=填充颜色, 透明度=0.7)

    def 写软件信息(self, x, y, 字体大小, 填充颜色=颜色.黑色, 水平基线对齐=文字水平基线对齐.结束点对齐, 是否转路径=否):
        if 是否转路径:
            return self.文字转路径(x=x, y=y, 文字="神笔码靓", 字体大小=字体大小, 字体文件=字体文件目录("小篆体.ttf"),
                                   填充颜色=填充颜色, 透明度=0.7, 描边宽度=0).平移(0, -字体大小 * 0.75)
        else:
            return self.写字(x=x, y=y, 文字="神笔码靓", 字体大小=字体大小, 字体="小篆体",
                             水平基线对齐=水平基线对齐,
                             填充颜色=填充颜色, 透明度=0.7)

    def 作者印章(self, 印章颜色=None, 是否转路径=否):
        from 神笔码靓.神笔库 import 版权印章路径
        外框路径 = 版权印章路径()

        if 印章颜色 is None:
            印章颜色 = "#E62828"

        外框 = self.连线(路径点列表=外框路径, 描边颜色=印章颜色, 描边宽度=13)

        if 是否转路径:
            作者网名 = self.文字转路径(x=36, y=-5, 文字="三月三", 字体大小=120, 字体文件="小篆体.ttf",
                                       纵向=是, 字符间距=-20, 填充颜色=印章颜色, 描边颜色=印章颜色, 描边宽度=5).缩放(
                1.7, 1)
        else:
            作者网名 = self.写字(x=100, y=100, 文字="三月三", 字体大小=126, 字体="小篆体",
                                 填充颜色=印章颜色).字符间距(-10).粗体().旋转(90).字旋转(-90).平移(196, 10).缩放(1, 1.5)

        return self.创建组合(元素列表=[外框, 作者网名])

    def 作者葫芦印章(self, 作者="三月三", 印章颜色=None):
        return self.印章.葫芦形(文字=作者, 描边颜色=印章颜色).创建组合()

    def 作者竖版印章(self, 作者="三月三", 印章颜色=None):
        return self.印章.竖版印章(文字=作者, 描边颜色=印章颜色).创建组合()

    def 完成前执行(self):
        """

        :return:
        """
        pass

    def 创作前执行(self):
        """

        :return:
        """
        pass

    def 修改文件名(self, 原始文件名: str):
        """

        :param 原始文件名:
        :return:
        """
        return None

    def 完成后执行(self):
        """

        :return:
        """
        pass

    def 创作(self):
        """

        :return:
        """
        pass

    def 写入Z顺序(self):
        from xml.etree import ElementTree as ET
        # 解析SVG文件
        tree = ET.parse(self.高清文件路径)
        root = tree.getroot()
        # 注册命名空间
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        # 初始化z_idx值
        z_idx = 0

        # 遍历所有元素并添加z_idx属性
        for element in root:
            if element.tag.split("}")[1] in ["path", "circle", "rect", "text", "image", "use", "ellipse", "line", "",
                                             "", "", ""]:
                element.attrib["z_index"] = str(z_idx)
                z_idx += 1

        # 保存修改后的SVG文件
        tree.write(self.高清文件路径[:-4] + ".zindex.svg", encoding='utf-8', xml_declaration=True)

    def _构建SVG元素(self):
        """

        :return:
        """
        处理组 = []

        for g in self.默认组:
            处理组.append(g)

        exclude_elements = []
        svg_elements = []

        def 移除重复的SVG元素(element_):
            """
            一旦成为 遮罩元素, 裁剪元素，则移除掉其他组里面的重复元素
            :param elem:
            :return:
            """
            nonlocal 处理组, exclude_elements, svg_elements
            if element_ is None:
                return

            if not isinstance(element_, list):
                elements = [element_]
            else:
                elements = element_

            for elem in elements:
                svg_element_ = elem.build_svg_element()
                if elem not in exclude_elements:
                    exclude_elements.append(elem)
                if svg_element_ not in exclude_elements:
                    exclude_elements.append(svg_element_)

                for g in [svg_elements]:
                    if svg_element_ in g:
                        g.remove(svg_element_)

                for g in [self.默认组, 处理组]:
                    if elem in g:
                        g.remove(elem)

        for _元素 in 处理组:
            if isinstance(_元素, 遮罩元素):
                遮罩元素_ = _元素.获取属性值("遮罩元素")
                移除重复的SVG元素(遮罩元素_)

            if isinstance(_元素, 裁剪元素):
                裁剪元素_ = _元素.获取属性值("裁剪元素")
                移除重复的SVG元素(裁剪元素_)
            if hasattr(_元素, "build_svg_element"):
                svg_element = _元素.build_svg_element()
            else:
                svg_element = _元素
            if not isinstance(svg_element, list):
                svg_element = [svg_element]
            for e in svg_element:
                if e not in exclude_elements:
                    svg_elements.append(e)

        added_ids = []

        def exists_id(svg_element):
            """
            主要是去掉相同的元素，但是有问题，暂时保留
            """
            id_ = svg_element.attribs["id"]
            if id_ in added_ids:
                return True

            for element in svg_element.elements:
                if exists_id(element):
                    return True

            added_ids.append(id_)
            return False

        for _元素 in self.默认组:
            if hasattr(_元素, "build_svg_element"):
                svg_element = _元素.build_svg_element()
            else:
                svg_element = _元素
            if not isinstance(svg_element, list):
                svg_element = [svg_element]

            for e in svg_element:
                # if exists_id(e):
                #     continue
                self.dwg.add(e)

        for _元素 in 处理组:
            if hasattr(_元素, "SVG元素创建后触发"):
                _元素.SVG元素创建后触发(_元素)

        self.处理JavaScript()

    def 元素构建完成(self):
        pass

    @计算耗时
    def 完成(self):
        """
        保存神笔绘图板
        :return:
        """
        设置 = 纸张设置()

        self.页面设置(设置)

        if 设置.页面方向 is None:
            设置.页面方向 = self.dwg.width_ / self.dwg.height_ > 1

        页边距 = f"{设置.上页边距} {设置.右页边距} {设置.下页边距} {设置.左页边距}"

        self.样式.设置页面样式(页边距=页边距, 页面尺寸规格=设置.页面尺寸规格, 页面缩放=设置.页面缩放,
                               页面方向=设置.页面方向)

        self.创作前执行()
        self.创作()
        self.完成前执行()

        self.样式.完成前定义样式()

        self._构建SVG元素()

        self.元素构建完成()

        修改后的文件名 = self.修改文件名(self.dwg.filename)
        if 修改后的文件名 is not None:
            if isinstance(修改后的文件名, str):
                self.dwg.filename = 修改后的文件名
            elif isinstance(修改后的文件名, list):
                filename = self.dwg.filename
                for o, t in 修改后的文件名:
                    filename = filename.replace(o, t)
                self.dwg.filename = filename
            elif isinstance(修改后的文件名, tuple):
                filename = self.dwg.filename
                o, t = 修改后的文件名
                filename = filename.replace(o, t)
                self.dwg.filename = filename
        self.高清文件路径 = self.dwg.filename

        # 如果要输出PDF文件，则需要将一些调式用的元素过滤掉，先生成一个临时高清图片用于生成PDF，再生成一个真实高清图片
        self._生成PDF准备()

        # 增加调试组中的元素
        if len(self.调试组) > 0:
            debug_g = self.dwg.g(id="debug_group")
            self.dwg.add(debug_g)
            for el in self.调试组:
                if isinstance(el, 元素):
                    el = el.build_svg_element()
                debug_g.add(el)

        print("神笔绘图板保存中...")
        安全创建目录(self.高清文件路径)

        # for e in 元素.z_orders:
        #     self.dwg.add(e.svg_element)
        if os.path.exists(self.高清文件路径):
            os.remove(self.高清文件路径)

        self.dwg.save(pretty=True)
        svg_file_path = os.path.abspath(self.高清文件路径)
        print("神笔绘图板保存成功，保存位置：", svg_file_path)

        self.完成后执行()

        print("已完成")

    # def open_svg_in_browser(self, svg_file):
    #     import webbrowser
    #     html_file = "svg_display.html"
    #     with open(html_file, "r") as file:
    #         html_content = file.read()
    #     html_content = html_content.replace("your_svg_file.svg", svg_file)
    #     with open(html_file, "w") as file:
    #         file.write(html_content)
    #     webbrowser.open("file://" + os.path.realpath(html_file))

    def _获取临时文件名(self):
        临时目录名 = os.path.dirname(self.高清文件路径)
        临时文件名 = os.path.basename(self.高清文件路径)[:-4] + ".tmp.svg"
        临时高清文件路径 = os.path.join(临时目录名, 临时文件名)
        临时高清文件路径 = os.path.normpath(临时高清文件路径)
        安全创建目录(临时高清文件路径)
        return 临时高清文件路径

    def _生成PDF准备(self):
        """
        生成PDF的准备工作，保证生成的PDF文件中去除调试组中元素（self.debug_group）
        :return:
        """
        # 调试组中存在元素，则执行
        if len(self.调试组) > 0:
            # 先生成一个临时高清图片用于生成PDF
            self.dwg.save()
            # 为了避免覆盖，改名为临时高清文件路径
            self.临时高清文件路径 = self._获取临时文件名()
            # 删除之前生成的临时文件
            if os.path.exists(self.临时高清文件路径):
                os.remove(self.临时高清文件路径)

            os.rename(self.高清文件路径, self.临时高清文件路径)

    def _获取PDF生成方式(self):
        if 谷歌浏览器是否有效():
            return PDF生成方式.谷歌浏览器

        if 是否安装cairosvg():
            return PDF生成方式.cairosvg

        msg = "生成PDF需要:安装谷歌浏览器并配置 或者 安装 cairosvg 包"
        raise Exception(msg)

    @计算耗时
    def 生成PDF(self, 生成方式=PDF生成方式.谷歌浏览器):
        """

        :return:
        """

        if PDF生成方式.自动 == 生成方式:
            生成方式 = self._获取PDF生成方式()

        # 存在临时高清文件路径，则优先使用
        if hasattr(self, "临时高清文件路径"):
            原始文件路径 = self.临时高清文件路径
        else:
            原始文件路径 = self.高清文件路径
        文件名 = 获取文件名(self.高清文件路径)
        输出文件名 = 连接路径(作品输出目录(), 文件名[:-4])
        print("PDF文件生成中...")
        if 生成方式 == PDF生成方式.谷歌浏览器:
            PDF工具集.转为PDF(原始文件路径, f"{输出文件名}.pdf")
        elif 生成方式 == PDF生成方式.cairosvg:
            CairoSvg工具集.转为PDF(原始文件路径, f"{输出文件名}.pdf")
        else:
            raise Exception(f"生成PDF不支持{生成方式}")

        self._删除临时高清文件路径()
        self.PDF文件路径 = f"{输出文件名}.pdf"
        print("PDF文件路径 ->", self.PDF文件路径)
        return self.PDF文件路径

    def 生成DOCX(self, 生成方式=DOCX生成方式.pdf2docx):
        """

        @param 生成方式:
        @return:
        """

        if not hasattr(self, "PDF文件路径"):
            self.生成PDF()

        if 生成方式 == DOCX生成方式.自动:
            生成方式 = DOCX生成方式.pdf2docx

        pdf_file = self.PDF文件路径
        docx_file = pdf_file[:-4] + ".docx"
        self.DOCX文件路径 = docx_file
        if 生成方式 == DOCX生成方式.pdf2docx:
            from pdf2docx import parse
            parse(pdf_file, docx_file)
        elif 生成方式 == DOCX生成方式.aspose_words:
            import aspose.words as aw
            doc = aw.Document(pdf_file)
            doc.save(docx_file)
        else:
            raise Exception(f"生成DOCX不支持{生成方式}")

        print("DOCX文件路径 ->", self.DOCX文件路径)
        return self.DOCX文件路径

    def 生成图片(self, 生成方式=PNG生成方式.谷歌浏览器, 缩放=3, 图片格式=None):
        if 图片格式 is None:
            图片格式 = "png"

        if 图片格式.lower() in ["png", ".png"]:
            self.生成PNG(生成方式=生成方式, 缩放=缩放)
        else:
            raise Exception(f"图片格式暂时不支持{图片格式}")

    @计算耗时
    def 生成PNG(self, 生成方式=PNG生成方式.谷歌浏览器, 缩放=3, 输出文件名=None, 输出文件覆盖=True, 窗口大小=None):
        """

        :param 生成方式:
        :return:
        """
        from PIL import Image

        # Set a new higher limit (e.g., doubling the default)
        # 解决报警：DecompressionBombWarning: Image size (118368000 pixels) exceeds limit of 89478485 pixels, could be decompression bomb DOS attack.
        Image.MAX_IMAGE_PIXELS = 2 * 89478485
        if 输出文件名 is None:
            文件名 = 获取文件名(self.高清文件路径)
            输出文件名 = 连接路径(作品输出目录(), 文件名[:-4])
        if not 输出文件覆盖:
            文件名序号 = 1
            while os.path.exists(f"{输出文件名}.png"):
                输出文件名 = f"{输出文件名}_{文件名序号}"
                文件名序号 += 1

        if 生成方式 == PNG生成方式.自动:
            生成方式 = PNG生成方式.谷歌浏览器

        print("PNG图片生成中...")
        if 生成方式 == PNG生成方式.cairosvg:
            CairoSvg工具集.转为PNG(self.高清文件路径, f"{输出文件名}.png", 缩放=缩放)
        elif 生成方式 == PNG生成方式.谷歌浏览器:
            # if 窗口大小调整 is None:
            #     win_w, win_h = 0, 0
            # else:
            #     win_w, win_h = 窗口大小调整
            # window_size = int(self.宽) + win_w, int(self.高) + win_h
            # 当前宽 = self.dwg.attribs["width"]
            # 当前高 = self.dwg.attribs["height"]
            # if 当前宽 != window_size[0] or 当前高 != window_size[1]:
            #     裁剪大小 = 当前宽, 当前高
            # else:
            #     裁剪大小 = None
            if 窗口大小 is None:
                当前宽 = self.dwg.attribs["width"]
                当前高 = self.dwg.attribs["height"]
                window_size = 当前宽, 当前高
            else:
                window_size = 窗口大小
            PDF工具集.转为PNG(self.高清文件路径, f"{输出文件名}.png", 缩放=缩放,
                              窗口大小=window_size, 裁剪大小=None)
            # if 缩放 != 1:
            #     print(f"谷歌浏览器生成的PNG不支持缩放={缩放}")
        else:
            raise Exception(f"生成PNG不支持{生成方式}")
        # else:
        #     pdf文件 = self.生成PDF()
        #     # f"{输出文件名}.png"
        #     PDF工具集.PDF转PNG服务(PDF文件=pdf文件, 保存目录=作品输出目录(), 多张图片=否, dpi=300)
        self.PNG文件路径 = f"{输出文件名}.png"
        print("PNG文件路径 ->", self.PNG文件路径)
        return self.PNG文件路径

    def _删除临时高清文件路径(self):
        if hasattr(self, "临时高清文件路径"):
            if os.path.exists(self.临时高清文件路径):
                # 删除临时文件
                os.remove(self.临时高清文件路径)
            delattr(self, "临时高清文件路径")

    def __del__(self):
        self._删除临时高清文件路径()


if __name__ == '__main__':
    神笔 = 神笔绘图板(作品文件路径="../输出文件/路径测试.svg", 宽=800, 高=800)
    路径 = 神笔.路径()
    p1 = (100, 200)
    p2 = (200, 300)
    p3 = (350, 400)
    p4 = (400, 200)

    # .倒角直线(点1, 点2, 倒角半径)
    路径.移动到(100, 100).画直线(p1).画直线(p2).画直线(p3).画直线(p4)
    路径.移动到(100, 100).倒圆角直线(p1, p2, 40).倒圆角直线(p3, p4, 40)
    神笔.完成()

if __name__ == '__main2__':
    import ast
    import inspect

    methods = inspect.getmembers(神笔绘图板, predicate=inspect.isfunction)

    for method_name, method in methods:
        if method_name.startswith("_"):
            continue
        docstring = method.__doc__
        params = inspect.signature(method).parameters
        print(f"Method Name: {method_name}")
        print(f"Docstring: {docstring}")
        print(f"Parameters: {params}")

    # def extract_class_info(file_path):
    #     with open(file_path, "r", encoding="utf-8") as file:
    #         code = file.read()
    #     tree = ast.parse(code)
    #     class_info = []
    #
    #     for node in ast.walk(tree):
    #         if isinstance(node, ast.ClassDef):
    #             class_name = node.name
    #             methods = []
    #             for sub_node in node.body:
    #                 if isinstance(sub_node, ast.FunctionDef):
    #                     method_name = sub_node.name
    #                     if method_name.startswith("_"):
    #                         continue
    #                     docstring = ast.get_docstring(sub_node)
    #                     methods.append((method_name, docstring))
    #             class_info.append((class_name, methods))
    #
    #     return class_info
    #
    #
    # # 示例用法
    # file_path = "神笔绘图板.py"  # 替换为你要分析的Python文件路径
    # class_info = extract_class_info(file_path)
    # for class_name, methods in class_info:
    #     print(f"类名： {class_name}")
    #     for method_name, docstring in methods:
    #         print(f"  方法名： {method_name}")
    #         if docstring:
    #             print(f"    文档字符串： {docstring}")

if __name__ == '__main2__':
    神笔 = 神笔绘图板(作品文件路径="../输出文件/神笔模板支持.svg", 宽=800, 高=800)
    超级玛丽模板 = 神笔.神笔模板("超级玛丽")
    超级玛丽 = 神笔.复制元素(超级玛丽模板, x=0, y=0, id_="超级玛丽")
    # # 在超级玛丽的眼中克隆一个和自己一样的小超级玛丽
    小玛丽 = 神笔.复制元素(超级玛丽模板, x=416.3, y=224.3, id_="小玛丽").缩放(0.003)
    超小玛丽 = 神笔.复制元素(超级玛丽模板, x=418.3, y=224.3, id_="超小玛丽").缩放(0.0001).垂直翻转()
    神笔.完成()

if __name__ == '__main1__':
    神笔 = 神笔绘图板(作品文件路径="../输出文件/神笔绘图板样例.svg", 宽=800, 高=500)
    神笔.显示图框()
    #
    矩形 = 神笔.画矩形(x=220, y=10, 宽=200, 高=100, 描边颜色=颜色.黑色, 圆角半径=10, 描边样式="5,5")

    神笔.写字(x=320, y=55, 文字="矩形水印", 字体大小=30, 填充颜色=颜色.黑色, 粗体=是, 斜体=是, 下划线=是,
              字体=系统字体.华文新魏, 透明度=1).缩放(1)
    # 高清图.写字(x=320, y=55, 文字="矩形水印", 字体大小=30, 填充颜色=颜色.红色,
    #        字体=系统字体.华文新魏, 透明度=1).缩放(1).倾斜X(80)
    # .旋转(90, (320, 55)).字旋转(-90).缩放(0.5).垂直翻转()

    #
    增加渐变中间点 = [{"偏移": "70%", "颜色": 颜色.橙色, "透明度": 1.0}]
    增加渐变中间点 = [{"偏移": "80%", "颜色": 颜色.黄色, "透明度": 1.0}]
    渐变色2 = 神笔.样式.创建线性渐变色(开始位置=(10, 10), 结束位置=(10, 100), 开始颜色=颜色.红色, 结束颜色=颜色.绿色,
                                       增加渐变中间点=增加渐变中间点)
    神笔.连线(路径点列表=[(10, 10), (10, 100), ("T", 50, 120), ("V", 120), (100, 100), (100, 10)], 闭合=True,
              填充颜色=渐变色2)

    #
    神笔.连直线(路径点列表=[(110, 10), (110, 100), (150, 120), (200, 100), (200, 10)], 闭合=是, 描边样式="5,5")
    #
    神笔.画多边形(顶点列表=[(10, 130), (140, 130), (140, 200), (10, 200)])
    for x, y in [(10, 130), (140, 130), (140, 200), (10, 200)]:
        神笔.画圆(x=x, y=y, 半径=10, 描边颜色=颜色.蓝色)
    #
    渐变色1 = 神笔.样式.创建径向渐变色(渐变开始中心点=(520, 180), 渐变半径=40, 开始颜色=颜色.红色, 结束颜色=颜色.橙色)
    _圆 = 神笔.画圆(x=520, y=180, 半径=50, 描边颜色=颜色.中绿宝石, 填充颜色=渐变色1, 描边样式="5,5")
    #
    _椭圆 = 神笔.画椭圆(x=520, y=180, 半径=(10, 20), 描边颜色=颜色.中绿宝石, 填充颜色="red", 描边样式="5,5")
    a = 神笔.创建组合(元素列表=[_圆, _椭圆])

    神笔.复制元素(对象元素=a, x=30, y=10)

    #
    神笔.写字(x=520, y=180, 文字="圆圈", 字体大小=30, 填充颜色=颜色.黑色, 字体=系统字体.华文行楷)
    神笔.写字(x=520, y=180, 文字="圆圈", 字体大小=30, 填充颜色=颜色.白色, 字体=系统字体.华文行楷)

    神笔.写字(x=300, y=180, 文字="隶书空心字", 字体大小=60, 字体=系统字体.隶书, 填充颜色=颜色.白色, 描边宽度=1,
              描边样式="1,1")
    神笔.写字(x=50, y=160, 文字="旋转字", 字体大小=20, 填充颜色=颜色.RGB(255, 0, 0))
    # # svg.画圆(x=50, y=160, 半径=10, 描边颜色=颜色.浅宝石蓝色)
    #
    印章 = 神笔.贴图(x=600, y=10, 图片文件="../资源库/图片/三月三印章.png").缩放(0.25)
    b = 神笔.复制元素(x=720, y=10, 对象元素=印章).缩放(1)
    #
    # 足球纹理6 = 高清图.贴图(x=10, y=200, 图片文件="../images/创意球体/足球纹理6.svg", 缩放=0.3, 旋转角度=0)  # ,模糊=2
    # # svg.贴图(x=100, y=200, 图片文件="../images/创意球体/足球纹理6.svg", 缩放=0.3, 旋转角度=0, 水平翻转=True)
    # # svg.贴图(x=200, y=200, 图片文件="../images/创意球体/足球纹理6.svg", 缩放=0.3, 旋转角度=0, 垂直翻转=True)
    # # svg.贴图(x=300, y=200, 图片文件="../images/创意球体/足球纹理6.svg", 缩放=0.3, 旋转角度=180, 垂直翻转=True, 水平翻转=True)
    # #
    # # svg.克隆元素(x=100, y=200, 对象元素=足球纹理6, 旋转角度=10, 缩放=1, 垂直翻转=True, 水平翻转=True)
    神笔.画矩形(x=400, y=250, 高=160, 宽=230, 填充颜色=颜色.橙色)
    足球1_效果 = 神笔.贴图(x=300, y=200, 图片文件="../资源库/素材/足球.jpg").缩放(0.25)
    矩形裁剪 = 神笔.矩形裁剪(x=1490, y=840, 宽=490, 高=490, 被裁元素=足球1_效果)
    # 圆形裁剪 = 高清图.圆形裁剪(x=1730, y=1100, 半径=240, 被裁元素=足球1_效果)
    # # svg.裁剪()
    #
    # # 足球1_效果['clip-path'] = 矩形裁剪.引用
    # # 足球1_效果['clip-path'] = 圆形裁剪.引用
    #
    神笔.完成()
