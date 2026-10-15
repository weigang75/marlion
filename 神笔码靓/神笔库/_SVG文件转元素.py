import svgwrite
import xml.etree.ElementTree as ET

from 神笔码靓.神笔库 import 资源库目录
from 神笔码靓.神笔库.通用工具集 import *
import svgwrite
import xml.etree.ElementTree as ET


def SvgXml转元素(dwg, svg_xml, prefix=""):
    root = ET.fromstring(svg_xml)
    elements = []
    for child in root:
        fill = child.attrib.get('fill', None)
        stroke = child.attrib.get('stroke', None)
        stroke_width = child.attrib.get('stroke-width', None)
        transform = child.attrib.get('transform', None)
        class_ = child.attrib.get('class', None)
        style = child.attrib.get('style', None)
        # if transform is not None:
        #     print(transform)

        elm = None
        # 根据 XML 中的元素类型进行相应的处理和添加到 dwg 中
        if child.tag.endswith('circle'):
            cx = float(child.attrib['cx'])
            cy = float(child.attrib['cy'])
            r = float(child.attrib['r'])
            elm = dwg.circle(center=(cx, cy), r=r)

        elif child.tag.endswith('rect'):
            x = float(child.attrib['x'])
            y = float(child.attrib['y'])
            width = float(child.attrib['width'])
            height = float(child.attrib['height'])
            elm = dwg.rect(insert=(x, y), size=(width, height))
        elif child.tag.endswith('defs'):
            # 对于 defs 元素，可能需要根据具体情况处理其中的定义
            _elements = SvgXml转元素(dwg, ET.tostring(child), prefix)
            pass
        elif child.tag.endswith('style'):
            defs = dwg.defs
            import re

            def add_prefix_to_classes(style_string, prefix_):
                return re.sub(r'\.([a-zA-Z0-9-]+)', r'.' + prefix_ + r'\1', style_string)

            # defs.add(dwg.style(content=child.text.replace(".", f".{prefix}")))
            style_content = add_prefix_to_classes(child.text, prefix)
            defs.add(dwg.style(content=style_content))
            pass
        elif child.tag.endswith('path'):
            d = child.attrib['d']
            elm = dwg.path(d=d)
        elif child.tag.endswith('g'):
            gelm = dwg.g()

            _elements = SvgXml转元素(dwg, ET.tostring(child), prefix)

            for element in _elements:
                gelm.add(element)

            elm = gelm
            # elements.append(new_dwg)
        elif child.tag.endswith('ellipse'):
            cx = float(child.attrib.get('cx', 0))
            cy = float(child.attrib.get('cy', 0))
            rx = float(child.attrib.get('rx', 0))
            ry = float(child.attrib.get('ry', 0))

            elm = dwg.ellipse(center=(cx, cy), r=(rx, ry))

        elif child.tag.endswith('line'):
            x1 = float(child.attrib.get('x1', 0))
            y1 = float(child.attrib.get('y1', 0))
            x2 = float(child.attrib.get('x2', 0))
            y2 = float(child.attrib.get('y2', 0))

            elm = dwg.line(start=(x1, y1), end=(x2, y2))

        elif child.tag.endswith('title'):
            # 处理标题元素，例如设置文档标题
            title_text = child.text
            dwg.title = title_text
        elif child.tag.endswith('namedview'):
            # 对于 namedview 元素，根据具体需求决定如何处理
            pass
        else:
            print("Unsupported tag:", child.tag)

        if elm is not None:
            if fill is not None:
                elm.attribs["fill"] = fill
            if stroke is not None:
                elm.attribs["stroke"] = stroke
            if stroke_width is not None:
                elm.attribs["stroke-width"] = float(stroke_width)
            if class_ is not None:
                elm.attribs["class"] = f"{prefix}{class_}"
            if style is not None:
                elm.attribs["style"] = style
            if transform is not None:
                elm.attribs["transform"] = transform
            elements.append(elm)
    return elements


dwg = svgwrite.Drawing()


def SVG文件转元素(SVG文件, idx):
    文件名, _ = os.path.splitext(os.path.basename(SVG文件))

    with open(SVG文件, mode="r", encoding="utf-8") as f:
        svg_xml = f.read()

    elememts = SvgXml转元素(dwg, svg_xml, f"c{文件名}_")
    g = dwg.g(id=f"g{文件名}")
    for elememt in elememts:
        g.add(elememt)
    g.attribs["transform"] = f"translate({idx * 100} 0)"
    dwg.add(g)


import os

斗兽棋子目录 = 资源库目录("素材/斗兽棋")
for idx, df in 索引列举(获取目录文件列表(斗兽棋子目录)):
    文件路径 = os.path.join(斗兽棋子目录, df)
    if not 文件路径.lower().endswith(".svg"):
        continue
    SVG文件转元素(文件路径, idx)
    # with open(文件路径, mode="r", encoding="utf-8") as f:
    #     svg_xml = f.read()

    # 示例的 SVG XML 字符串
    # svg_xml = """
    # <svg width="400" height="400">
    #   <circle cx="50" cy="50" r="40" />
    #   <rect x="100" y="100" width="200" height="100" />
    # </svg>
    # """

    # elememts = convert_svg_xml_to_svgwrite_element(dwg, svg_xml, f"c{idx}_")
    # g = dwg.g()
    # for elememt in elememts:
    #     g.add(elememt)
    # g.attribs["transform"] = f"translate({idx * 100} 0)"
    # dwg.add(g)
# 保存转换后的 SVG 图像
dwg.saveas('converted_svg.svg')
