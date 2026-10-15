# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os

from 神笔码靓.神笔库.定义集 import *

from 神笔码靓.神笔库.通用工具集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.元素库 import 线性渐变色, 径向渐变色


class 样式工具集:
    彩虹色1 = [颜色.红色, 颜色.橙色, 颜色.黄色, 颜色.绿色, 颜色.青色, 颜色.蓝色, 颜色.紫色]
    彩虹色2 = [颜色.红色, "#FF6D00", 颜色.黄色, "#59FB46", "#59D5EF", "#5E7EF7", "#B359F6"]

    def __init__(self, 高清图):
        from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
        self.高清图: 神笔绘图板 = 高清图
        self.dwg = 高清图.dwg
        self._loaded_fonts = {}

    def _conv_to_id(self, id_perfix, values):
        import re
        id = f"{id_perfix}_"
        for v in values:
            id += re.sub(r'[-()" .,]', '_', str(v).strip(" (),")).replace("__", "_").replace("__", "_") + "_"
        return id[:-1]

    def 设置背景色(self, 背景色):
        if 背景色 != 颜色.白色:
            if "style" in self.dwg.attribs:
                style = self.dwg.attribs["style"]
            else:
                style = ""
            self.dwg.attribs["style"] = f"background-color: {背景色};" + style

    def 导入字体样式(self):
        if hasattr(self, "_字体样式加载"):
            return
        setattr(self, "_字体样式加载", True)

        self.预设置样式('@import url("字体样式.css");', 插入到最前=是)

    def 设置字体样式(self, 字体文件):
        """
        保留
        :param 字体文件:
        :return:
        """
        if not isinstance(字体文件, list):
            字体文件 = [字体文件]

        字体名列表 = []
        font_root = 字体文件目录()
        if os.path.exists(font_root):
            for d in 获取目录文件列表(font_root):
                name_split_text = os.path.splitext(d)
                # Eot、otf、fon、font、ttf、ttc、woff
                if name_split_text[1].lower() not in [".ttf", ".ttc", ".eot", ".otf", ".fon", ".font", ".woff"]:
                    continue
                font_name = name_split_text[0]
                if font_name in self._loaded_fonts:
                    continue
                if font_name not in 字体文件:
                    continue

                self._loaded_fonts[font_name] = True

                字体名列表.append(d)

                # if run_in_jupyter():
                #     font_path = os.path.join(font_root, d).replace("\\", "/")
                # else:
                font_path = os.path.join("fonts", d).replace("\\", "/")

                output_dir = os.path.dirname(self.高清图.高清文件路径)
                output_font_dir = os.path.join(output_dir, "fonts", d)
                if not os.path.exists(output_font_dir):
                    安全创建目录(output_font_dir)
                    安全复制文件(os.path.join(font_root, d), output_font_dir)
                style = f"@font-face {{font-family: '{font_name}'; src: url('{font_path}');}}"
                # 加载字体路径文件
                self.预设置样式(style)
                # self.dwg.defs.add(self.dwg.style(style))
        return 字体名列表

    def 设置页面样式(self, 页边距="0.1cm 0 0 0.1cm", 页面尺寸规格="A4", 页面缩放=1, 页面方向=纸张方向.纵向):
        if 页边距 is None:
            页边距 = "0cm"
        if 页面缩放 is None:
            页面缩放 = ""
        else:
            页面缩放 = f"zoom: {页面缩放}"

        if 页面方向:
            页面方向 = "landscape"
        else:
            页面方向 = ""

        if 页面尺寸规格 is None:
            页面尺寸规格 = "A4"

        # 无页眉页脚
        page_margin = "0"

        media_style = f"@media print {{ @page {{ margin: {page_margin}; size: {页面尺寸规格} {页面方向};}} " \
                      f"svg {{ margin: {页边距}; {页面缩放}}} }}"

        # dwg.defs.add(dwg.style(media_style))
        self.预设置样式(样式=media_style)

    def 预设置样式(self, 样式, 插入到最前=False):
        if not hasattr(self, "dwg_styles"):
            dwg_styles = ""
        else:
            dwg_styles = getattr(self, "dwg_styles")
        if 插入到最前:
            setattr(self, "dwg_styles", 样式 + dwg_styles)
        else:
            setattr(self, "dwg_styles", dwg_styles + 样式)

    def 完成前定义样式(self):
        if hasattr(self, "dwg_styles"):
            # 将样式添加到SVG文件中
            defs = self.dwg.defs
            defs.add(self.dwg.style(content=getattr(self, "dwg_styles")))

    def 文字样式生成(self, 粗体=否, 斜体=否, 下划线=否, 字符间距=0):
        style = ""
        if 粗体:
            style = "font-weight:bold; "
        if 斜体:
            style += "font-style:italic; "
        if 下划线:
            style += "text-decoration:underline; "

        if 字符间距 != 0 and 字符间距 is not None:
            style += f"letter-spacing:{字符间距}px; "

        #  textLength="100" lengthAdjust="spacingAndGlyphs"
        # 使用时spacingAndGlyphs，整个文本元素被拉伸到文本的方向。
        # style += "width:100%;height:200%;"
        if style == "":
            style = None

        return style

    def 创建线性渐变色(self, 开始位置, 结束位置, 开始颜色, 结束颜色,
                开始偏移='0%', 结束偏移='100%',
                开始透明度=1.0, 结束透明度=1.0, 增加渐变中间点=[], id_=None) -> 线性渐变色:
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
        from svgwrite.gradients import LinearGradient
        if id_ is None:
            grad_id = self._conv_to_id("LG", [开始位置, 结束位置, 开始颜色, 结束颜色])
        else:
            grad_id = id_
        grad = LinearGradient(start=开始位置, end=结束位置, id=grad_id, gradientUnits='userSpaceOnUse')
        grad.add_stop_color(offset=开始偏移, color=开始颜色, opacity=开始透明度)
        for s in 增加渐变中间点:
            _offset = s["偏移"]
            _color = s["颜色"]
            if "透明度" in s.keys():
                _opacity = s["透明度"]
            else:
                _opacity = 1.0
            grad.add_stop_color(offset=_offset, color=_color, opacity=_opacity)
        grad.add_stop_color(offset=结束偏移, color=结束颜色, opacity=结束透明度)
        # 将渐变添加到SVG画布
        self.dwg.defs.add(grad)

        return 线性渐变色(grad)

    # def _build_gradient_transform(self, gradient_elm, 旋转角度=0, 缩放=1, 平移=None):
    #     gradientTransform = ""
    #     # translate(25.53 144.5) rotate(2.07) scale(1 .5)
    #     if 平移 is not None:
    #         x, y = 平移
    #         gradientTransform += f"translate({x} {y}) "
    #     if 旋转角度 != 0:
    #         gradientTransform += f"rotate({旋转角度}) "
    #     if 缩放 is None:
    #         缩放 = 1.0
    #
    #     if isinstance(缩放, tuple):
    #         缩放_x, 缩放_y = 缩放
    #     else:
    #         缩放_x, 缩放_y = 缩放, 缩放
    #
    #     if 缩放 != 1.0:
    #         gradientTransform += f"scale({缩放_x} {缩放_y})"
    #
    #     if len(gradientTransform) > 0:
    #         gradient_elm["gradientTransform"] = gradientTransform

    def 创建径向渐变色(self, 渐变开始中心点, 渐变半径, 开始颜色, 结束颜色,
                开始偏移='0%', 结束偏移='100%',
                开始透明度=1.0, 结束透明度=1.0, 渐变的焦点=None,
                增加渐变中间点=[], id_=None
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
        from svgwrite.gradients import RadialGradient
        if id_ is None:
            grad_id = self._conv_to_id("RG", [渐变开始中心点, 渐变半径, 开始颜色, 结束颜色])
        else:
            grad_id = id_

        if 渐变的焦点 is None:
            grad = RadialGradient((float(渐变开始中心点[0]), float(渐变开始中心点[1])), 渐变半径,
                                  id=grad_id, gradientUnits='userSpaceOnUse')
        else:
            fx, fy = 渐变的焦点
            grad = RadialGradient((float(渐变开始中心点[0]), float(渐变开始中心点[1])), 渐变半径, focal=(fx, fy),
                                  id=grad_id, gradientUnits='userSpaceOnUse')

        grad.add_stop_color(offset=开始偏移, color=开始颜色, opacity=开始透明度)
        for s in 增加渐变中间点:
            _offset = s["偏移"]
            _color = s["颜色"]
            if "透明度" in s.keys():
                _opacity = s["透明度"]
            else:
                _opacity = 1.0
            grad.add_stop_color(offset=_offset, color=_color, opacity=_opacity)
        grad.add_stop_color(offset=结束偏移, color=结束颜色, opacity=结束透明度)

        # self._build_gradient_transform(grad, 旋转角度=旋转角度, 缩放=缩放, 平移=平移)
        # 将渐变添加到SVG画布
        self.dwg.defs.add(grad)
        return 径向渐变色(grad)

    def 彩虹渐变点(self, 关键点偏移=None, 关键点透明度=None, 彩虹七色=None):
        """
                 0.5
        ──────────┴──────────  一个关键点（0.5:中间位置的偏移）
            0.1      0.9
        ─────┴────────┴──────  两个关键点（0.1:开始偏移,中间位置固定为 0.5, 0.9:结束偏移）
        0.1      0.5       0.9
        ┴─────────┴─────────┴  三个关键点（0.1:开始偏移,0.5:中间位置偏移, 0.9:结束偏移）
       0.1  0.25 0.5  0.75 0.9
        ┴────┴────┴────┴────┴  五个关键点（0.1:开始偏移, 0.9:结束偏移）
       0.1               0.9
        ┴──┴──┴──┴──┴──┴──┴    七个关键点（彩虹7种颜色的偏移，红橙黄绿青蓝紫，0.1:红色偏移, 0.9:紫色偏移）

        :param 关键点偏移: 关键点个数只支持 1、2、3、7，请参照：
                 0.5
        ──────────┴──────────  一个关键点（0.5:中间位置的偏移）
            0.1      0.9
        ─────┴────────┴──────  两个关键点（0.1:开始偏移,中间位置固定为 0.5, 0.9:结束偏移）
        0.1      0.5       0.9
        ┴─────────┴─────────┴  三个关键点（0.1:开始偏移,0.5:中间位置偏移, 0.9:结束偏移）
        0.1               0.9
        ┴──┴──┴──┴──┴──┴──┴    七个关键点（彩虹7种颜色的偏移，红橙黄绿青蓝紫，0.1:红色偏移, 0.9:紫色偏移）
        :param 关键点透明度: 透明度个数只支持 1、2、3、7，请参照：
        0.5      0.5       0.5
        └─────────┴─────────┘  一个值: 全部透明度为0.5
        0.1      0.5       1.0
        └─────────┴─────────┘  两个值: 决定开始透明度值和结束透明度，中间的透明度线性平分
        0.1      0.5       1.0
        └─────────┴─────────┘  三个值: 决定开始透、中间、结束透明度，中间的透明度线性平分
        0.1                0.9
        └──┴───┴──┴──┴──┴───┘  七个值（彩虹7种颜色的透明度，红橙黄绿青蓝紫，0.1:红色透明度, 0.9:紫色透明度）
        :param 彩虹七色: 自定义彩虹的7种颜色
        :return:
        """
        关键点偏移使用说明 = """关键点个数只支持 1、2、3、7，请参照：
         0.5
──────────┴──────────  一个关键点（0.5:中间位置的偏移）
    0.1      0.9
─────┴────────┴──────  两个关键点（0.1:开始偏移,中间位置固定为 0.5, 0.9:结束偏移）
0.1      0.5       0.9
┴─────────┴─────────┴  三个关键点（0.1:开始偏移,0.5:中间位置偏移, 0.9:结束偏移）
0.1               0.9
┴──┴──┴──┴──┴──┴──┴    七个关键点（彩虹7种颜色的偏移，红橙黄绿青蓝紫，0.1:红色偏移, 0.9:紫色偏移）
"""
        透明度使用说明 = """透明度个数只支持 1、2、3、7，请参照：
0.5      0.5       0.5
└─────────┴─────────┘  一个值: 全部透明度为0.5
0.1      0.5       1.0
└─────────┴─────────┘  两个值: 决定开始透明度值和结束透明度，中间的透明度线性平分  
0.1      0.5       1.0
└─────────┴─────────┘  三个值: 决定开始透、中间、结束透明度，中间的透明度线性平分  
0.1                0.9
└──┴───┴──┴──┴──┴───┘  七个值（彩虹7种颜色的透明度，红橙黄绿青蓝紫，0.1:红色透明度, 0.9:紫色透明度）
"""

        def 转百分比字符串(num):
            if isinstance(num, float):
                return str(round(num * 100.0, 1)) + "%"
            if isinstance(num, str):
                return num
            return str(num)

        def 转百分比数值(num):
            if isinstance(num, float):
                return num
            if isinstance(num, str):
                return float(num.replace("%", "")) / 100.0
            return float(num)

        def 中间点偏移_1(n):
            if n < 0.5:
                n16 = round(0.5 / 3 * n * 2, 3)
                n33 = round(0.5 / 3 * 2 * n * 2, 3)
                n50 = n
                r = (1 - n) / 3
                n66 = n + r
                n83 = n + 2 * r
            elif n > 0.5:
                r = n / 3
                n16 = r
                n33 = 2 * r
                n50 = n
                r = (1 - n) / 3
                n66 = n + r
                n83 = n + 2 * r
            else:
                n16, n33, n50, n66, n83 = 0.167, 0.333, 0.5, 0.667, 0.833

            # print(转百分比字符串(n16), 转百分比字符串(n33), 转百分比字符串(n50), 转百分比字符串(n66), 转百分比字符串(n83))
            中间点偏移_ = ["0%", 转百分比字符串(n16), 转百分比字符串(n33),
                      转百分比字符串(n50), 转百分比字符串(n66), 转百分比字符串(n83), "100%"]
            return 中间点偏移_

        def 中间点偏移_2(n1, n2):
            n = 0.5
            return 中间点偏移_3(n1, n, n2)

        def 中间点偏移_3(n1, n2, n3):
            n_f = n2 - n1
            n_b = n3 - n2
            r_f = n_f / 3
            r_b = n_b / 3

            n16, n33, n66, n83 = n1 + r_f, n1 + r_f * 2, n2 + r_b, n2 + r_b * 2

            中间点偏移_ = [转百分比字符串(n1), 转百分比字符串(n16), 转百分比字符串(n33),
                      转百分比字符串(n2),
                      转百分比字符串(n66), 转百分比字符串(n83), 转百分比字符串(n3)]
            return 中间点偏移_

        if 关键点偏移 is None:
            中间点偏移 = ["0%", "16.7%", "33.3%", "50%", "66.7%", "83.3%", "100%"]
        elif isinstance(关键点偏移, tuple) or isinstance(关键点偏移, list):
            if len(关键点偏移) == 1:
                n = 转百分比数值(关键点偏移[0])
                中间点偏移 = 中间点偏移_1(n)
            elif len(关键点偏移) == 2:
                n1 = 转百分比数值(关键点偏移[0])
                n2 = 转百分比数值(关键点偏移[1])
                中间点偏移 = 中间点偏移_2(n1, n2)
            elif len(关键点偏移) == 3:
                n1 = 转百分比数值(关键点偏移[0])
                n2 = 转百分比数值(关键点偏移[1])
                n3 = 转百分比数值(关键点偏移[2])
                中间点偏移 = 中间点偏移_3(n1, n2, n3)
            elif len(关键点偏移) == 7:
                中间点偏移 = [转百分比字符串(关键点偏移[0]), 转百分比字符串(关键点偏移[1]), 转百分比字符串(关键点偏移[2]),
                         转百分比字符串(关键点偏移[3]), 转百分比字符串(关键点偏移[4]), 转百分比字符串(关键点偏移[5]),
                         转百分比字符串(关键点偏移[6])]
            else:
                raise Exception(关键点偏移使用说明)
        else:
            中间点偏移 = 中间点偏移_1(转百分比数值(关键点偏移))

        if 关键点透明度 is None:
            关键点透明度 = [1.0] * 7

        if isinstance(关键点透明度, float) or isinstance(关键点透明度, int):
            关键点透明度 = [关键点透明度] * 7
        elif isinstance(关键点透明度, tuple) or isinstance(关键点透明度, list):
            if len(关键点透明度) == 1:
                关键点透明度 = [关键点透明度[0]] * 7
            elif len(关键点透明度) == 2:
                o_start = 关键点透明度[0]
                o_end = 关键点透明度[1]
                r = (o_end - o_start) / 6
                关键点透明度 = [o_start, round(o_start + r, 2), round(o_start + 2 * r, 2), round(o_start + 3 * r, 2),
                          round(o_start + 4 * r, 2), round(o_start + 5 * r, 2), o_end]
            elif len(关键点透明度) == 3:
                o_start = 关键点透明度[0]
                o_mid = 关键点透明度[1]
                o_end = 关键点透明度[2]
                r_start = (o_mid - o_start) / 3
                r_end = (o_end - o_mid) / 3

                关键点透明度 = [o_start, round(o_start + r_start, 2), round(o_start + r_start * 2, 2),
                          o_mid,
                          round(o_mid + r_end, 2), round(o_mid + r_end * 2, 2), o_end]
            elif len(关键点透明度) == 7:
                pass
            else:
                raise Exception(透明度使用说明)
        else:
            关键点透明度 = [关键点透明度] * 7

        if 彩虹七色 is None:
            彩虹七色 = self.彩虹色1

        关键渐变点 = [
            {"偏移": 中间点偏移[0], "颜色": 彩虹七色[0]},
            {"偏移": 中间点偏移[1], "颜色": 彩虹七色[1]},
            {"偏移": 中间点偏移[2], "颜色": 彩虹七色[2]},
            {"偏移": 中间点偏移[3], "颜色": 彩虹七色[3]},
            {"偏移": 中间点偏移[4], "颜色": 彩虹七色[4]},
            {"偏移": 中间点偏移[5], "颜色": 彩虹七色[5]},
            {"偏移": 中间点偏移[6], "颜色": 彩虹七色[6]},
        ]
        # print(中间点偏移)
        # print(关键点透明度)
        for i, o in 索引列举(关键点透明度):
            if o != 1.0:
                关键渐变点[i]["透明度"] = o

        # print(关键渐变点)
        return 关键渐变点


def 字体样式文件生成(目录列表):
    字体目录 = 字体文件目录()
    字体名称列表 = []
    for fd in 获取目录文件列表(字体目录):
        name_split_text = os.path.splitext(fd)
        # Eot、otf、fon、font、ttf、ttc、woff
        if name_split_text[1].lower() not in [".ttf", ".ttc", ".eot", ".otf", ".fon", ".font", ".woff"]:
            continue
        字体名称列表.append(fd)
    font_face_str = ""
    for 字体名 in 字体名称列表:
        name, f_name = os.path.splitext(字体名)
        font_face_str += "@font-face {\n" + f"	font-family: '{name}'; src: url('$相对目录$/{字体名}');\n"
        font_face_str += "}\n"
    # @font-face {
    # 	font-family: '小篆体'; src: url('../字体/小篆体.ttf');
    # }

    for d in 目录列表:
        _font_face_str = font_face_str.replace("$相对目录$", os.path.relpath(字体目录, d).replace("\\", "/"))

        css_file = os.path.join(d, "字体样式.css")

        with open(css_file, 'w', encoding="utf-8") as f:
            f.write(_font_face_str)


if __name__ == '__main__':
    字体样式文件生成([
        神笔库目录(),
        神笔库目录("html"),
        作品输出目录(),
        成果馆目录(),
        成果馆目录("地理"),
        成果馆目录("学习"),
        成果馆目录("手工"),
        成果馆目录("数学之美"),
        成果馆目录("生活娱乐"),
        成果馆目录("日历"),
        成果馆目录("日历/2022年"),
        成果馆目录("日历/2023年"),
        成果馆目录("日历/2024年"),
        成果馆目录("日历/2025年"),
        成果馆目录("绘画"),
        成果馆目录("音乐"),
    ])
