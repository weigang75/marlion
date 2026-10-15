# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-11
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.头像.元素神笔模板 import 头像元素神笔模板
from 神笔码靓.码靓库.头像.头像颜色定义 import 头发默认颜色列表
from 神笔码靓.神笔库 import 神笔模板, 神笔绘图板
from 神笔码靓.神笔库.线条工具集 import *
from 神笔码靓.神笔库.通用工具集 import *
import xml.etree.ElementTree as ET


def 遍历头像文件(目录):
    for fd in os.listdir(目录):
        if "SVG图片索引.svg" in fd:
            continue
        if fd.endswith("svg"):
            yield os.path.join(目录, fd)


custom_content = """
<g
   id="参考线">    <rect
   alignment-baseline="auto"
   fill="none"
   height="320"
   id="mar3_pycr_rc_0"
   stroke="black"
   stroke-width="1"
   width="320"
   x="0"
   y="0" />    <path
   d="M160.00,0.00  L160.00,320.00"
   fill="none"
   id="mar3_pycr_p_2"
   shape-rendering="auto"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1" />    <text
   alignment-baseline="middle"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_3"
   rotate="-90"
   stroke="black"
   stroke-width="0"
   text-anchor="start"
   transform="translate(-5,8) rotate(90,164.75,8.0)"
   x="160.0"
   y="0">1</text>    <rect
   alignment-baseline="auto"
   fill="none"
   height="28"
   id="mar3_pycr_rc_4"
   rx="5"
   ry="5"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1"
   width="120"
   x="100.0"
   y="148.8372093023256" />    <text
   alignment-baseline="text-before-edge"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_5"
   stroke="black"
   stroke-width="0"
   text-anchor="start"
   x="160.0"
   y="162.8372093023256">2</text>    <rect
   alignment-baseline="auto"
   fill="none"
   height="28"
   id="mar3_pycr_rc_6"
   rx="5"
   ry="5"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1"
   width="120"
   x="100.0"
   y="118.5185185185185" />    <text
   alignment-baseline="text-before-edge"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_7"
   stroke="black"
   stroke-width="0"
   text-anchor="start"
   x="160.0"
   y="132.5185185185185">3</text>    <rect
   alignment-baseline="auto"
   fill="none"
   height="28"
   id="mar3_pycr_rc_8"
   rx="5"
   ry="5"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1"
   width="35"
   x="142.5"
   y="179.7752808988764" />    <text
   alignment-baseline="text-before-edge"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_9"
   stroke="black"
   stroke-width="0"
   text-anchor="start"
   x="160.0"
   y="193.7752808988764">4</text>    <rect
   alignment-baseline="auto"
   fill="none"
   height="10"
   id="mar3_pycr_rc_10"
   rx="5"
   ry="5"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1"
   width="45"
   x="137.5"
   y="210.52631578947367" />    <text
   alignment-baseline="text-before-edge"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_11"
   stroke="black"
   stroke-width="0"
   text-anchor="start"
   x="160.0"
   y="215.52631578947367">5</text>    <path
   d="M120.00,248.06  L200.00,248.06"
   fill="none"
   id="mar3_pycr_p_12"
   shape-rendering="auto"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1" />    <text
   alignment-baseline="text-before-edge"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_13"
   stroke="black"
   stroke-width="0"
   text-anchor="start"
   x="120.0"
   y="248.06201550387595">6</text>    <ellipse
   alignment-baseline="auto"
   cx="160.0"
   cy="152.38095238095238"
   fill="none"
   id="mar3_pycr_el_14"
   rx="85"
   ry="95"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1.0" />    <text
   alignment-baseline="middle"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_15"
   stroke="black"
   stroke-width="0"
   text-anchor="middle"
   x="160.0"
   y="152.38095238095238">7</text>    <ellipse
   alignment-baseline="auto"
   cx="246.15384615384613"
   cy="168.42105263157896"
   fill="none"
   id="mar3_pycr_el_16"
   rx="20"
   ry="25"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1.0" />    <text
   alignment-baseline="middle"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_17"
   stroke="black"
   stroke-width="0"
   text-anchor="middle"
   x="246.15384615384613"
   y="168.42105263157896">8</text>    <ellipse
   alignment-baseline="auto"
   cx="74.4186046511628"
   cy="168.42105263157896"
   fill="none"
   id="mar3_pycr_el_18"
   rx="20"
   ry="25"
   stroke="black"
   stroke-dasharray="3,3"
   stroke-width="1.0" />    <text
   alignment-baseline="middle"
   fill="black"
   font-size="10"
   id="mar3_pycr_t_19"
   stroke="black"
   stroke-width="0"
   text-anchor="middle"
   x="74.4186046511628"
   y="168.42105263157896">9</text>  </g>
"""  # 将自定义字符串设置为 <g> 元素的文本内容


# def modify_svg_不要(file_path):
#     # 解析 SVG 文件
#     tree = ET.parse(file_path)
#     root = tree.getroot()
#
#     # 删除注释
#     for elem in root.iter():
#         # 查找并删除注释
#         # if isinstance(elem, ET..Comment):
#         #     root.remove(elem)
#         print(elem, type(elem))
#
#     # 去掉 height 和 width 属性
#     if 'height' in root.attrib:
#         del root.attrib['height']
#     if 'width' in root.attrib:
#         del root.attrib['width']
#
#     # 修改 viewBox 属性
#     root.attrib['viewBox'] = "0 0 320 320"
#     # 添加命名空间
#     ET.register_namespace('', 'http://www.w3.org/2000/svg')
#
#     # 创建新的 <g> 元素并添加到根节点
#     new_group = ET.Element('g', id='测试')
#
#     # 添加包含 < 和 > 的内容
#     content_with_tags = ET.Element('content')
#     content_with_tags.text = custom_content  # 直接使用包含 < 和 > 的字符串
#
#     # 将内容添加到 <g> 元素中
#     new_group.append(content_with_tags)
#
#     root.append(new_group)
#
#     # 保存修改后的 SVG 文件
#     tree.write(file_path[:-4] + "_修改.svg", encoding='utf-8', xml_declaration=True)


def modify_svg(file_path):
    # 读取原始 SVG 文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        svg_content = file.read()

    # 删除注释
    svg_content = re.sub(r'<!--.*?-->', '', svg_content, flags=re.DOTALL)

    # 替换 height 和 width 属性
    svg_content = re.sub(r' height="[^"]*"', '', svg_content)
    svg_content = re.sub(r' width="[^"]*"', '', svg_content)

    # 修改 viewBox 属性
    svg_content = re.sub(r'viewBox="[^"]*"', 'viewBox="0 0 320 320"', svg_content)

    # 添加新的 <g> 元素
    new_group = custom_content
    svg_content = svg_content.replace("</svg>", new_group + "</svg>")

    new_file_name = file_path.replace(".svg", "_修改.svg")
    # 保存修改后的 SVG 文件
    with open(new_file_name, 'w', encoding='utf-8') as file:
        file.write(svg_content)


if __name__ == '__main__':
    目录 = 资源库目录(r"素材\漫画卡通\头像\男_选")
    目录  = r"G:\works\gitcode\code_painter\资源库\素材\漫画卡通\头像\帽子"
    idx = 0
    for svg文件 in 遍历头像文件(目录):
        modify_svg(svg文件)
        idx = idx +1
        # if idx > 2:
        #     break
