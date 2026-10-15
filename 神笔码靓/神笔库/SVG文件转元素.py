# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-07-27
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import xml.etree.ElementTree as ET
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *
from 神笔码靓.神笔库.元素库 import *


class SVG文件转元素工具(单例模式):
    def __init__(self, 高清图):
        self.高清图: 神笔绘图板 = 高清图
        self.href_key = '{http://www.w3.org/1999/xlink}href'

    def _circle(self, child):
        cx = float(child.attrib['cx'])
        cy = float(child.attrib['cy'])
        r = float(child.attrib['r'])
        elm = self.高清图.画圆(x=cx, y=cy, 半径=r)
        return elm

    def _rect(self, child):
        x = float(child.attrib.get('x', 0))
        y = float(child.attrib.get('y', 0))
        width = float(child.attrib['width'])
        height = float(child.attrib['height'])
        elm = self.高清图.画矩形(x=x, y=y, 宽=width, 高=height)
        return elm

    def _style(self, child, prefix):
        defs = self.高清图.dwg.defs
        import re
        # def add_prefix_to_classes(style_string, prefix_):
        #     return re.sub(r'\.([a-zA-Z0-9-]+)', r'.' + prefix_ + r'\1', style_string)

        def add_prefix_to_classes(style_string, prefix):
            # 使用负向先行断言来确保不匹配小数点后的数字
            return re.sub(r'\.(?![0-9])([a-zA-Z0-9-]+)', r'.' + prefix + r'\1', style_string)

        # defs.add(dwg.style(content=child.text.replace(".", f".{prefix}")))
        style_content = add_prefix_to_classes(child.text, prefix)
        defs.add(self.高清图.dwg.style(content=style_content))

    def _ellipse(self, child):
        cx = float(child.attrib.get('cx', 0))
        cy = float(child.attrib.get('cy', 0))
        rx = float(child.attrib.get('rx', 0))
        ry = float(child.attrib.get('ry', 0))
        elm = self.高清图.画椭圆(x=cx, y=cy, 半径=(rx, ry))
        return elm

    def _line(self, child):
        x1 = float(child.attrib.get('x1', 0))
        y1 = float(child.attrib.get('y1', 0))
        x2 = float(child.attrib.get('x2', 0))
        y2 = float(child.attrib.get('y2', 0))
        elm = self.高清图.画线(开始位置=(x1, y1), 结束位置=(x2, y2))
        return elm

    def _text(self, child):
        rotate = child.attrib.get('rotate', None)
        x = float(child.attrib.get('x', 0))
        y = float(child.attrib.get('y', 0))
        font_size = float(child.attrib.get('font-size', 12))
        font_family = child.attrib.get('font-family', 系统字体.微软雅黑)
        alignment_baseline = child.attrib.get("alignment-baseline", "middle")
        text_anchor = child.attrib.get("text_anchor", "middle")
        # fill = child.attrib.get('fill', 'black')
        text_content = child.text
        # elements.append(
        #     dwg.text(text_content, insert=(x, y), font_size=font_size, font_family=font_family, fill=fill))
        elm = self.高清图.写字(x=x, y=y, 文字=text_content, 字体=font_family, 字体大小=font_size,
                          水平基线对齐=text_anchor, 垂直基线对齐=alignment_baseline)
        if rotate is not None:
            elm.字旋转(rotate)
        return elm

    def _use(self, child):
        id_ = child.attrib.get('id', None)
        x = float(child.attrib.get('x', 0))
        y = float(child.attrib.get('y', 0))
        alignment_baseline = child.attrib.get("alignment-baseline", None)
        href = child.attrib.get(self.href_key)
        elm = self.高清图.复制元素(对象元素=href, x=x, y=y, 透明度=1.0, id_=id_)
        return elm

    def _symbol(self, child, prefix):
        # 处理 symbol 元素
        id_ = child.attrib.get('id')
        view_box = child.attrib.get('viewBox', None)
        sub_elms = [(i, i.attrib.get(self.href_key)) for i in child]
        _elements = self.Xml转元素(ET.tostring(child), prefix)
        elm = self.高清图.创建模板(元素列表=_elements, id_=id_)
        return elm

    def _image(self, child):
        x = float(child.attrib.get('x', 0))
        y = float(child.attrib.get('y', 0))
        width = float(child.attrib.get('width', 0))
        height = float(child.attrib.get('height', 0))
        href = child.attrib.get(self.href_key)
        # elements.append(dwg.image(href=href, insert=(x, y), size=(width, height)))
        elm = self.高清图.贴图(x=x, y=y, 图片文件=href, 宽=width, 高=height)
        return elm

    def _clipPath(self, child):
        id_ = child.attrib.get('id')
        裁剪元素_ = 裁剪元素(self.高清图, self.高清图.默认组)
        裁剪元素_.设置属性值("href", child[0].attrib.get('href'))
        # self.高清图.默认组.append(裁剪元素_)
        return 裁剪元素_

    def _polygon(self, child):
        id_ = child.attrib.get('id')
        x = float(child.attrib.get('x', 0))
        y = float(child.attrib.get('y', 0))
        points = child.attrib.get('points')
        fill = child.attrib.get('fill', 'none')
        stroke_width = child.attrib.get('stroke-width', 1)
        stroke = child.attrib.get('stroke', "black")
        opacity = child.attrib.get("opacity", 1.0)
        stroke_dasharray = child.attrib.get('stroke-dasharray', None)

        points = points.replace(",", " ")
        while "  " in points:
            points = points.replace("  ", " ")

        points = points.strip().split(" ")

        if len(points) % 2 == 0:
            points = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
        else:
            print(points)
            exit(-1)

        elm = self.高清图.画多边形(顶点列表=points,
                            # 填充颜色=fill, 描边颜色=stroke, 描边宽度=stroke_width, 描边样式=stroke_dasharray, 透明度=opacity
                            )
        return elm

    def _linearGradient(self, child):
        # 处理线性渐变元素
        id_ = child.attrib.get('id')
        x1 = float(child.attrib.get('x1', 0))
        y1 = float(child.attrib.get('y1', 0))
        x2 = float(child.attrib.get('x2', 0))
        y2 = float(child.attrib.get('y2', 0))

        增加渐变中间点 = []
        for stop in child:
            offset = stop.attrib['offset']
            color = stop.attrib['stop-color']
            opacity = stop.attrib.get("opacity", 1)

            增加渐变中间点.append({"偏移": offset, "颜色": color, "透明度": opacity})
        if len(增加渐变中间点) > 1:
            开始 = 增加渐变中间点[0]
            结束 = 增加渐变中间点[-1]
            增加渐变中间点 = 增加渐变中间点[1:-1]
            渐变色 = self.高清图.创建线性渐变色(开始位置=(x1, y1), 结束位置=(x2, y2),
                                   开始颜色=开始["颜色"], 结束颜色=结束["颜色"],
                                   开始偏移=开始["偏移"], 结束偏移=结束["偏移"],
                                   开始透明度=开始["透明度"], 结束透明度=结束["透明度"],
                                   增加渐变中间点=增加渐变中间点, id_=id_)

    def _radialGradient(self, child):
        # 处理径向渐变元素
        id_ = child.attrib.get('id')
        cx = float(child.attrib.get('cx', 0))
        cy = float(child.attrib.get('cy', 0))
        r = float(child.attrib.get('r', 1))

        增加渐变中间点 = []
        for stop in child:
            offset = stop.attrib['offset']
            color = stop.attrib['stop-color']
            opacity = stop.attrib.get("opacity", 1)

            增加渐变中间点.append({"偏移": offset, "颜色": color, "透明度": opacity})
        if len(增加渐变中间点) > 1:
            开始 = 增加渐变中间点[0]
            结束 = 增加渐变中间点[-1]
            增加渐变中间点 = 增加渐变中间点[1:-1]
            渐变色 = self.高清图.创建径向渐变色(渐变开始中心点=(cx, cy), 渐变半径=r,
                                   开始颜色=开始["颜色"], 结束颜色=结束["颜色"],
                                   开始偏移=开始["偏移"], 结束偏移=结束["偏移"],
                                   开始透明度=开始["透明度"], 结束透明度=结束["透明度"],
                                   增加渐变中间点=增加渐变中间点, id_=id_)

    # region ------------------------------------------------------

    def 解析Xml元素(self, child, prefix):
        elm = None
        # 根据 XML 中的元素类型进行相应的处理和添加到 dwg 中
        if child.tag.endswith('circle'):
            elm = self._circle(child)
        elif child.tag.endswith('rect'):
            elm = self._rect(child)
        elif child.tag.endswith('defs'):
            # 对于 defs 元素，可能需要根据具体情况处理其中的定义
            _elements = self.Xml转元素(ET.tostring(child), prefix)
        elif child.tag.endswith('style'):
            self._style(child, prefix)
        elif child.tag.endswith('path'):
            path_d = child.attrib['d']
            # path_d = path_d.replace(" ", ",")
            elm = self.高清图.连线(路径点列表=[]).原生path(path_d)
        elif child.tag.endswith('g'):
            _elements = self.Xml转元素(ET.tostring(child), prefix)
            elm = self.高清图.创建组合(元素列表=_elements)
        elif child.tag.endswith('ellipse'):
            elm = self._ellipse(child)
        elif child.tag.endswith('line'):
            elm = self._line(child)
        elif child.tag.endswith('text'):
            elm = self._text(child)
        elif child.tag.endswith('use'):
            elm = self._use(child)
        elif child.tag.endswith('symbol'):
            elm = self._symbol(child, prefix)
        elif child.tag.endswith('image'):
            elm = self._image(child)
        elif child.tag.endswith('filter'):
            id_ = child.attrib.get('id')
            # print("filter",id_)
            print("滤镜未处理:", ET.tostring(child))
            # 处理 filter 的属性和子元素
            # self.滤镜
        elif child.tag.endswith('linearGradient'):
            self._linearGradient(child)
        elif child.tag.endswith('radialGradient'):
            self._radialGradient(child)
        elif child.tag.endswith('polygon'):
            elm = self._polygon(child)
        elif child.tag.endswith('clipPath'):
            elm = self._clipPath(child)
        elif child.tag.endswith('namedview'):
            pass
        elif child.tag.endswith('desc'):
            pass
        elif child.tag.endswith('title'):
            pass
        else:
            print("暂时未支持的TAG:", child.tag)

        return elm

    def Xml转元素(self, svg_xml, prefix=""):

        root = ET.fromstring(svg_xml)
        elements = []

        for child in root:
            # 获取通用属性
            fill = child.attrib.get('fill', None)
            stroke = child.attrib.get('stroke', None)
            stroke_width = child.attrib.get('stroke-width', None)
            transform = child.attrib.get('transform', None)
            class_ = child.attrib.get('class', None)
            style = child.attrib.get('style', None)
            opacity = child.attrib.get('opacity', 1)
            stroke_dasharray = child.attrib.get('stroke-dasharray', None)

            elm = self.解析Xml元素(child, prefix)

            # 如果元素不为空，则赋值通用属性
            if elm is not None:
                if fill is not None and hasattr(elm, "填充颜色"):
                    elm.填充颜色(fill)
                elif hasattr(elm, "无填充颜色"):
                    elm.无填充颜色()

                if stroke is not None and hasattr(elm, "描边颜色"):
                    elm.描边颜色(stroke)
                elif hasattr(elm, "无描边颜色"):
                    elm.无描边颜色()

                if stroke_width is not None and hasattr(elm, "描边宽度"):
                    elm.描边宽度(float(stroke_width))
                elif hasattr(elm, "无描边宽度"):
                    elm.无描边宽度()

                if opacity != 1 and hasattr(elm, "透明度"):
                    elm.透明度(float(opacity))

                if class_ is not None and hasattr(elm, "样式类名"):
                    elm.样式类名(f"{prefix}{class_}")

                if style is not None and hasattr(elm, "样式字符串"):
                    elm.样式字符串(style)

                if transform is not None and hasattr(elm, "变换字符串"):
                    elm.变换字符串(transform)

                if stroke_dasharray is not None and hasattr(elm, "描边样式"):
                    elm.描边样式(stroke_dasharray)
                elif hasattr(elm, "无描边样式"):
                    elm.无描边样式()

                elements.append(elm)
        return elements

    def SVG文件转元素(self, SVG图片):
        文件名, _ = os.path.splitext(os.path.basename(SVG图片))

        with open(SVG图片, mode="r", encoding="utf-8") as f:
            svg_xml = f.read()
        md5 = 获取字符串md5(SVG图片)
        elememts = self.Xml转元素(svg_xml, f"c{md5[:15]}_")
        return elememts

        # g = dwg.g(id=f"g{文件名}")
        # for elememt in elememts:
        #     g.add(elememt)
        # g.attribs["transform"] = f"translate({idx * 100} 0)"
        # dwg.add(g)

    # endregion --------------------------------------------------------
