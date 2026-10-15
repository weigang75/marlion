# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import svgwrite
import xml.etree.ElementTree as ET
import os
import re

from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.通用工具集 import *


class 神笔绘图板工具:
    PATH_COMMANDS_MAPPINGS = {
        "移动": "M",  # x, y
        "移动到": "M",  # x, y
        "直线": "L",  # x, y
        "水平直线": "H",  # x
        "水平线": "H",  # x
        "垂直直线": "V",  # y
        "垂直线": "V",  # y
        "曲线": "C",  # (x1, y1), (x2, y2), (x, y)
        "平滑曲线": "S",  # (x2, y2), (x, y)
        "二次贝塞尔曲线": "Q",  # (x2, y2), (x, y)
        "平滑的二次贝塞尔曲线": "T",  # x, y
        "椭圆弧线": "A",  # (rx, ry), x_axis_rotation, (large_arc_flag, sweep_flag), (x, y)
        "关闭路径": "Z",
        "闭合路径": "Z",
        "关闭": "Z",
        "闭合": "Z",

        # 扩展支持
        "倒角": "倒角",  # 倒角长度
        "倒圆角": "倒圆角",  # 倒角半径, 方向
        "圆弧线": "圆弧线",
        # "矩形", "绘制矩形", "rect"  开始X, 开始Y, 宽度, 高度, 顺时针
    }

    @staticmethod
    def 获取SVG图片大小(SVG文件):
        # 打开SVG文件
        tree = ET.parse(SVG文件)
        root = tree.getroot()

        width = root.get('width')
        height = root.get('height')
        if width is None or height is None:
            x, y, width, height = root.get("viewBox").split(" ")
        # 尺寸单位换算公式大全
        # 1. 像素（px）与厘米（cm）的换算公式
        # 在设计中，经常需要将像素转换为厘米或将厘米转换为像素。其换算公式为：
        # 厘米 = 像素 ÷ dpi * 2.54
        # 像素 = 厘米 ÷ 2.54 * dpi
        # 其中，dpi为每英寸显示器点数，常见值为72、96、150、300等。需要根据具体情况进行判断，以得到精确的结果。
        # 2. 像素（px）与点（pt）的换算公式
        # 像素和点是两个常用的尺寸单位，它们的换算公式为：
        # 像素 = 点 ÷ 72 * dpi
        # 点 = 像素 ÷ dpi * 72
        # 其中，dpi的值与第一节中的相同。
        # 3. 英寸（in）与厘米（cm）的换算公式
        # 英寸是比较普遍的尺寸单位，而在国内，厘米也是常用的单位。其换算公式为：
        # 英寸 = 厘米 ÷ 2.54
        # 厘米 = 英寸 * 2.54
        # 4. 毫米（mm）与英寸（in）的换算公式
        # 毫米也是常用的尺寸单位之一，它与英寸的换算关系为：
        # 毫米 = 英寸 × 25.4
        # 英寸 = 毫米 ÷ 25.4
        # 5. 点（pt）与毫米（mm）的换算公式
        # 点是一种常见的排版单位，而毫米也是广泛使用的长度单位之一。它们的换算公式为：
        # 点 = 毫米 ÷ 25.4 × 72
        # 毫米 = 点 ÷ 72 × 25.4
        # 6. 厘米（cm）与磅（pt）的换算公式
        # 磅是一种在排版中比较常见的单位，那么它与厘米又该如何换算呢？其公式为：
        # 磅 = 厘米 ÷ 2.54 × 72
        # 厘米 = 磅 ÷ 72 × 2.54
        # 7. 毫米（mm）与磅（pt）的换算公式
        # 之前提到，毫米是可以用作长度单位的。它与磅的换算关系为：
        # 磅 = 毫米 ÷ 25.4 × 72
        # 毫米 = 磅 ÷ 72 × 25.4
        # 8. 像素（px）、点（pt）和磅（pt）之间的换算公式
        # 在数字排版时，常常需要将其它尺寸单位转换为像素、点或磅等单位。它们之间的换算公式如下所示：
        # 1像素(px) = 1点(pt) = 0.75磅   像素 = 点 ÷ 72 * dpi
        if width.endswith("pt"):
            # 1像素=0.75pt = 0.2645833333333333mm = 0.02645833333333333cm = 1REM
            width = float(width.strip('pt')) / 0.75
            height = float(height.strip('pt')) / 0.75
        # 增加其他的单位和px换算的代码 1in = 2.54cm = 25.4 mm = 72pt = 6pc
        # elif width.endswith("cm"):  # 以下代码AI生成，需要验证
        #     width = float(width.strip('cm'))*2.54
        #     height = float(height.strip('cm'))*2.54
        # elif width.endswith("mm"):
        #     width = float(width.strip('mm'))*2.54
        #     height = float(height.strip('mm'))*2.54
        # elif width.endswith("in"):
        #     width = float(width.strip('in'))*2.54*72
        #     height = float(height.strip('in'))*2.54*72
        # elif width.endswith("pc"):
        #     width = float(width.strip('pc'))*2.54*12
        #     height = float(height.strip('pc'))*2.54*12
        elif width.endswith("px"):
            width = float(width.strip('px'))
            height = float(height.strip('px'))
        else:
            width = float(width)
            height = float(height)

        return width, height

    @staticmethod
    def 缩放SVG图片_(SVG文件, 缩放=2.0, 缩放后SVG文件=None):
        tree = ET.parse(SVG文件)
        root = tree.getroot()

        if 缩放后SVG文件 is None:
            缩放后SVG文件 = SVG文件[:-4] + f"{缩放}.svg"

        # 获取SVG的宽度和高度
        width = float(root.get('width').strip('px'))
        height = float(root.get('height').strip('px'))
        # 修改SVG的缩放比例
        root.set('width', str(width * 缩放) + 'px')
        root.set('height', str(height * 缩放) + 'px')

        # 保存修改后的SVG文件
        tree.write(缩放后SVG文件)

    @staticmethod
    def 缩放SVG图片(SVG文件, 缩放, 缩放后SVG文件=None):
        if 缩放 == 1:
            svg_width, svg_height = 神笔绘图板工具.获取SVG图片大小(SVG文件)
            return SVG文件, (svg_width, svg_height)

        if 缩放后SVG文件 is None:
            缩放后SVG文件 = SVG文件[:-4] + f"{缩放}.svg"

        缩放后SVG文件, svg_size = 神笔绘图板工具._scale_svg(SVG文件, 缩放, 缩放后SVG文件)  # 放大 2 倍

        # with open(缩放后SVG文件, 'w', encoding="UTF-8") as f:
        #     f.write(scaled_svg)
        # print(缩放后SVG文件, f"已放大{缩放}倍")
        return 缩放后SVG文件, svg_size

    @staticmethod
    def 获取元素的坐标信息(对象元素):
        if hasattr(对象元素, "attribs"):
            if "x" in 对象元素.attribs:
                elm_x = float(str(对象元素['x']).strip("px"))
            else:
                elm_x = None
            if "y" in 对象元素.attribs:
                elm_y = float(str(对象元素['y']).strip("px"))
            else:
                elm_y = None
            if 'width' in 对象元素.attribs:
                elm_width = 对象元素['width']
            else:
                elm_width = None
            if 'height' in 对象元素.attribs:
                elm_height = 对象元素['height']
            else:
                elm_height = None
        else:
            elm_x, elm_y, elm_width, elm_height = None, None, None, None

        if elm_x is None or elm_y is None or elm_width is None or elm_height is None:
            if not hasattr(对象元素, "elementname"):
                return None
            _对象元素 = 对象元素
            if 对象元素.elementname == "use":
                return 神笔绘图板工具.获取元素的坐标信息(对象元素.href)
            # if 对象元素.elementname == 'symbol':
            #     return
            if _对象元素.elementname in ["g", "symbol"]:
                return 神笔绘图板工具._get_group_bbox(_对象元素)
            elif _对象元素.elementname == "path":
                return 神笔绘图板工具._get_path_bbox(_对象元素)
            elif _对象元素.elementname == "ellipse":
                return 神笔绘图板工具._get_ellipse_bbox(_对象元素)
            elif _对象元素.elementname == "circle":
                return 神笔绘图板工具._get_circle_bbox(_对象元素)
            elif _对象元素.elementname == "text":
                return 神笔绘图板工具._get_text_bbox(_对象元素)
            elif _对象元素.elementname == "use":
                return None
            else:
                raise Exception(f"elementname = {_对象元素.elementname}")
        else:
            return (elm_x, elm_y), (elm_width + elm_x, elm_height + elm_y)

    @staticmethod
    def split_decimals(num_str):
        parts = []
        dot_positions = [i for i, char in enumerate(num_str) if char == '.']
        if len(dot_positions) > 1:
            first_part = num_str[:dot_positions[0]] + '.' + num_str[dot_positions[0] + 1:dot_positions[1]]
            second_part = '0.' + num_str[dot_positions[1] + 1:]
            parts.append(first_part)
            if second_part.count('.') > 1:
                vals = 神笔绘图板工具.split_decimals(second_part)
                parts += vals
            else:
                parts.append(second_part)

        return parts

    @staticmethod
    def path_d_split(data):
        cmd_arg_num_dict = {
            "m": 2, "l": 2, "t": 2,
            "q": 4, "s": 4,
            "c": 6, "a": 7, "h": 1, "v": 1
        }

        commands = re.findall(r'[mltqscahvzMLTQSCAHVZ][^mltqscahvzMLTQSCAHVZ]*', data)
        split_commands = []
        for command in commands:
            cmd_tag = command[0]
            cmd_vals = command[1:]
            # 处理小数
            cmd_vals = cmd_vals.replace("-.", "-0.").replace(",.", ",0.").replace(" .", " 0."). \
                replace("-", " -").replace(",", " ").replace("  ", " ").replace("  ", " ")

            vals = cmd_vals.split(" ")
            vals = [v for v in vals if v != '']
            _vals = []
            for val in vals:
                if val.count('.') >= 2:
                    _vals += 神笔绘图板工具.split_decimals(val)
                else:
                    _vals.append(val)

            vals = _vals

            cmd_arg_num = cmd_arg_num_dict.get(cmd_tag.lower(), None)
            if cmd_arg_num is None:
                split_commands.append(command)
            elif len(vals) > cmd_arg_num:
                vi = 0
                for v in range(0, len(vals), cmd_arg_num):
                    cmd_text = cmd_tag
                    for i in range(cmd_arg_num):
                        try:
                            if i % 2 == 0:
                                cmd_text += f"{vals[vi]},"
                            else:
                                cmd_text += f"{vals[vi]} "
                        except Exception as e:
                            pass
                        vi += 1
                    split_commands.append(str(cmd_text).strip())
            elif len(vals) == cmd_arg_num:
                cmd_text = cmd_tag
                for i in range(cmd_arg_num):
                    if i % 2 == 0:
                        cmd_text += f"{vals[i]},"
                    else:
                        cmd_text += f"{vals[i]} "
                split_commands.append(str(cmd_text).strip())
            else:
                split_commands.append(command)

        # print(split_commands)
        return split_commands

    @staticmethod
    def _矩形转SVG绘制路径命令(命令):
        命令集 = []
        命令ID, 开始X, 开始Y, 宽度, 高度, *顺时针 = 命令
        if len(顺时针) == 0:
            顺时针 = True
        else:
            顺时针 = 顺时针[0] in ["顺时针", True]

        命令集.append(("M", 开始X, 开始Y))

        if 顺时针:
            命令集.append(("H", 开始X + 宽度))
            命令集.append(("V", 开始Y + 高度))
            命令集.append(("H", 开始X))
            命令集.append(("Z",))
        else:
            命令集.append(("V", 开始Y + 高度))
            命令集.append(("H", 开始X + 宽度))
            命令集.append(("V", 开始Y))
            命令集.append(("Z",))

        return 命令集

    @staticmethod
    def 转SVG绘制路径命令(路径点列表):

        # M = moveto 移动到指定位置
        # L = lineto 绘制直线
        # H = horizontal lineto 绘制水平直线
        # V = vertical lineto 绘制垂直直线
        # C = curveto 绘制曲线
        # S = smooth curveto 绘制平滑曲线
        # Q = quadratic Bézier curve 绘制二次贝塞尔曲线
        # T = smooth quadratic Bézier curveto 绘制平滑的二次贝塞尔曲线
        # A = elliptical Arc 绘制椭圆弧线
        # Z = closepath 关闭路径
        SVG路径点列表 = []
        for cmd_idx, cmd in enumerate(路径点列表):
            def 获取倒角的三个点():
                prev2_cmd = list(SVG路径点列表[-2])
                prev_cmd = list(SVG路径点列表[-1])
                next_cmd = list(路径点列表[cmd_idx + 1])
                return prev2_cmd, prev_cmd, next_cmd

            if isinstance(cmd, str):
                cmd_list = [cmd]
            else:
                cmd_list = list(cmd)

            if str(cmd_list[0]).lower() in ["矩形", "绘制矩形", "rect"]:
                命令集 = 神笔绘图板工具._矩形转SVG绘制路径命令(cmd_list)
                for 命令 in 命令集:
                    SVG路径点列表.append(tuple(命令))
            else:
                cmd_list[0] = 神笔绘图板工具.PATH_COMMANDS_MAPPINGS.get(cmd_list[0], cmd_list[0])
                cmd_args = cmd_list[1:]
                if cmd_list[0] in ["倒角"]:
                    倒角半径 = cmd_list[1]
                    prev2_cmd, prev_cmd, next_cmd = 获取倒角的三个点()

                    from 神笔码靓.神笔库.倒角工具集 import 计算倒圆角切点坐标
                    起点, 终点, 角度方向 = 计算倒圆角切点坐标((prev2_cmd[1], prev2_cmd[2]), (prev_cmd[1], prev_cmd[2]),
                                                              (next_cmd[1], next_cmd[2]), 倒角半径)

                    prev_cmd = prev_cmd[0], 起点.x, 起点.y
                    SVG路径点列表[-1] = prev_cmd
                    路径点列表[cmd_idx + 1] = next_cmd
                    SVG路径点列表.append(("L", 终点.x, 终点.y))

                elif cmd_list[0] in ["倒圆角"]:
                    倒角半径, *方向 = cmd_list[1:]
                    if len(方向) == 0:
                        方向 = None
                    else:
                        方向 = 方向[0]
                    prev2_cmd, prev_cmd, next_cmd = 获取倒角的三个点()

                    from 神笔码靓.神笔库.倒角工具集 import 计算倒圆角切点坐标
                    起点, 终点, 角度方向 = 计算倒圆角切点坐标((prev2_cmd[1], prev2_cmd[2]), (prev_cmd[1], prev_cmd[2]),
                                                              (next_cmd[1], next_cmd[2]), 倒角半径)

                    if 方向 is None:
                        方向 = 1 if 角度方向 else 0
                    # else:
                    #     方向 = 1

                    prev_cmd = prev_cmd[0], 起点.x, 起点.y
                    SVG路径点列表[-1] = prev_cmd
                    路径点列表[cmd_idx + 1] = next_cmd
                    是否大弧 = 0
                    SVG路径点列表.append(("A", 倒角半径, 倒角半径, 0, 是否大弧, 方向, 终点.x, 终点.y))
                elif cmd_list[0] in ["圆弧线"]:
                    if len(cmd_list[1:]) == 4:
                        倒角半径, 方向, x, y = cmd_list[1:]
                        是否大弧 = 0
                    elif len(cmd_list[1:]) == 5:
                        倒角半径, 方向, x, y, 是否大弧 = cmd_list[1:]
                        if 是否大弧 == True or 是否大弧 == 1:
                            是否大弧 = 1
                        else:
                            是否大弧 = 0
                    if 方向 != 0:
                        方向 = 1
                    SVG路径点列表.append(("A", 倒角半径, 倒角半径, 0, 是否大弧, 方向, x, y))
                else:
                    SVG路径点列表.append(tuple(cmd_list))

        return SVG路径点列表

    #
    # @staticmethod
    # def path_d_split(d):
    #     cmds = 神笔绘图板工具.split_commands_step_1(d)
    #     return 神笔绘图板工具.split_command_step_2(cmds)

    @staticmethod
    def 绝对坐标转相对坐标(path_cmds):
        # Uppercase commands indicates absolute coordinates,
        # lowercase commands indicates relative coordinates
        commands = ['M', 'L', 'H', 'V', 'C', 'S', 'Q', 'T', 'A', 'Z']
        commands_upper = [c.upper() for c in commands]
        commands_lower = [c.lower() for c in commands]
        # commands = commands_upper + commands_lower
        current_x = 0
        current_y = 0
        new_path_cmds = []
        for idx, cmd in enumerate(path_cmds):
            cmd = 神笔绘图板工具._fixed_d(cmd, idx)
            cmd_tag = cmd[0]

            if idx > 0:
                if cmd_tag in ["V"]:
                    current_y = 0
                elif cmd_tag in ["H"]:
                    current_x = 0
                elif cmd_tag in commands_upper:
                    current_x, current_y = 0, 0
            # M = moveto 移动到指定位置
            # L = lineto 绘制直线
            # H = horizontal lineto 绘制水平直线
            # V = vertical lineto 绘制垂直直线
            # C = curveto 绘制曲线
            # S = smooth curveto 绘制平滑曲线
            # Q = quadratic Bézier curve 绘制二次贝塞尔曲线
            # T = smooth quadratic Bézier curveto 绘制平滑的二次贝塞尔曲线
            # A = elliptical Arc 绘制椭圆弧线
            # Z = closepath 关闭路径
            if cmd_tag in ['M', 'm', 'L', 'l', 'T', 't']:
                x, y = map(float, cmd[1:].split(','))
                current_x = x - current_x
                current_y = y - current_y
                if idx == 0:
                    new_path_cmds.append(cmd)
                else:
                    if cmd_tag in commands_lower:
                        new_path_cmds.append(cmd)
                    else:
                        new_path_cmds.append("{}{:.2f},{:.2f}".format(cmd_tag.lower(), current_x, current_y))
                        current_x = x
                        current_y = y
            elif cmd_tag in ['Q', 'q', 'S', 's']:
                (x1, y1), (x, y) = [list(map(float, s.split(","))) for s in cmd[1:].split(" ") if s != '']
                x1 = x1 - current_x
                y1 = y1 - current_y
                current_x = x - current_x
                current_y = y - current_y
                if cmd_tag in commands_lower:
                    new_path_cmds.append(cmd)
                else:
                    new_path_cmds.append(
                        "{}{:.2f},{:.2f} {:.2f},{:.2f}".format(cmd_tag.lower(), x1, y1, current_x, current_y))
                    current_x = x
                    current_y = y
            elif cmd_tag in ['C', 'c']:
                (x1, y1), (x2, y2), (x, y) = [list(map(float, s.split(","))) for s in cmd[1:].split(" ") if s != '']
                x1 = x1 - current_x
                y1 = y1 - current_y
                x2 = x2 - current_x
                y2 = y2 - current_y
                current_x = x - current_x
                current_y = y - current_y
                if cmd_tag in commands_lower:
                    new_path_cmds.append(cmd)
                else:
                    new_path_cmds.append(
                        "{}{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}".format(cmd_tag.lower(), x1, y1, x2, y2, current_x,
                                                                             current_y))
                    current_x = x
                    current_y = y
            elif cmd_tag in ['A', 'a']:
                # raise Exception("AAAAAAAA")
                # (rx, ry), (x_axis_rotation), (large_arc_flag,sweep_flag), (x, y)
                (rx, ry), x_axis_rotation, (large_arc_flag, sweep_flag), (x, y) = [list(map(float, s.split(","))) for s
                                                                                   in cmd[1:].split(" ") if s != '']
                # # rx ry x-axis-rotation large-arc-flag sweep-flag x y)
                current_x = x - current_x
                current_y = y - current_y
                new_path_cmds.append(
                    "{}{:.2f},{:.2f} {} {},{} {:.2f},{:.2f}".format(cmd_tag.upper(), rx, ry,
                                                                    int(x_axis_rotation[0]),
                                                                    int(large_arc_flag), int(sweep_flag), current_x,
                                                                    current_y))
                # current_x = x
                # current_y = y

            elif cmd_tag in ['H', 'h']:
                x = float(cmd[1:])
                current_x = x - current_x
                if cmd_tag in commands_lower:
                    new_path_cmds.append(cmd)
                else:
                    new_path_cmds.append("{}{:.2f}".format(cmd_tag.lower(), current_x))
                    current_x = x
            elif cmd_tag in ['V', 'v']:
                y = float(cmd[1:])
                current_y = y - current_y
                if cmd_tag in commands_lower:
                    new_path_cmds.append(cmd)
                else:
                    new_path_cmds.append("{}{:.2f}".format(cmd_tag.lower(), current_y))
                    current_y = y
            elif cmd_tag in ['Z', 'z']:
                new_path_cmds.append(cmd)

        return new_path_cmds

    @staticmethod
    def _fixed_d(di, idx):
        if idx == 0:
            return di
        if not isinstance(di[0], str):
            di = tuple(["L"] + list(di))

        return di

    @staticmethod
    def _fixed_point(point, idx):
        if idx == 0:
            if point[0] in ["M", "m"]:
                return "M", point[1], point[2]
            if len(point) == 2:
                return "M", point[0], point[1]
            if len(point) == 1:
                point = point[0]
                d = point[1:].split(",")
                return point[0], float(d[0]), float(d[1])
            return "M", point[0], point[1]
        if not isinstance(point[0], str):
            point = "L", point[0], point[1]

        return point

    @staticmethod
    def 获取点列表的坐标(点列表):
        pts = []
        for idx, point in enumerate(点列表):
            point = 神笔绘图板工具._fixed_point(point, idx)
            cmd_tag = point[0].upper()
            if cmd_tag in ['M', 'm', 'L', 'l', 'T', 't']:
                pts.append((point[1], point[2]))
            elif cmd_tag in ['Q', 'q', 'S', 's']:
                if len(point) == 5:
                    x, y = point[3], point[4]
                    pts.append((x, y))
            elif cmd_tag in ['C', 'c']:
                prev_pt = 点列表[idx - 1]
                if len(点列表) < idx + 1:
                    next_pt = 点列表[idx + 1]
                    if next_pt[0] == "Z":
                        next_pt = 点列表[0]
                else:
                    next_pt = None

                if len(prev_pt) == 2:
                    prev_x, prev_y = prev_pt
                elif len(prev_pt) > 2:
                    prev_x, prev_y = prev_pt[-2], prev_pt[-1]
                else:
                    raise Exception("格式错误")

                if len(point) == 7:
                    next_x, next_y = point[5], point[6]
                elif next_pt is None:
                    next_x, next_y = None, None
                elif len(next_pt) == 2:
                    next_x, next_y = next_pt
                elif len(next_pt) > 2:
                    next_x, next_y = next_pt[1], next_pt[2]
                else:
                    raise Exception("格式错误")

                if len(point) == 5:  #
                    # pts.append((point[1], point[2], (prev_x, prev_y)))
                    pass
                    if next_x is None or next_y is None:
                        pts.append((point[3], point[4]))
                    else:
                        # pts.append((point[3], point[4], (next_x, next_y)))
                        pass

                elif len(point) == 7:  #
                    # pts.append((point[1], point[2], (prev_x, prev_y)))
                    pass
                    if next_x is None or next_y is None:
                        pts.append((point[3], point[4]))
                    else:
                        # pts.append((point[3], point[4], (next_x, next_y)))
                        pass
                    pts.append((point[5], point[6]))
            elif cmd_tag in ['A', 'a']:
                if len(point) == 8:  #
                    x, y = point[6], point[7]
                    pts.append((x, y))
            elif cmd_tag in ['H', 'h']:
                y = pts[-1][1]
                pts.append((point[1], y))
            elif cmd_tag in ['V', 'v']:
                x = pts[-1][0]
                pts.append((x, point[1]))
        return pts

    @staticmethod
    def 点列表转SVG路径(point_list):
        cmds = []
        for idx, point in enumerate(point_list):
            point = 神笔绘图板工具._fixed_point(point, idx)
            cmd_tag = point[0].upper()
            if cmd_tag in ['M', 'm', 'L', 'l', 'T', 't']:
                cmds.append("{}{:.2f},{:.2f}".format(cmd_tag.upper(), float(point[1]), float(point[2])))
            elif cmd_tag in ['Q', 'q', 'S', 's']:
                if len(point) == 3:  #
                    last_p = point_list[idx + 1]
                    x, y = last_p[0], last_p[1]
                elif len(point) == 5:  #
                    x, y = point[3], point[4]
                else:
                    raise Exception("格式错误：", point)
                cmds.append("{}{:.2f},{:.2f} {:.2f},{:.2f}".format(cmd_tag.upper(),
                                                                   float(point[1]), float(point[2]),
                                                                   float(x), float(y)))
            elif cmd_tag in ['C', 'c']:
                if len(point) == 5:  #
                    last_p = point_list[idx + 1]
                    x, y = last_p[0], last_p[1]
                elif len(point) == 7:  #
                    x, y = point[5], point[6]
                else:
                    raise Exception("格式错误：", point)
                cmds.append(
                    "{}{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}".format(cmd_tag.upper(),
                                                                         float(point[1]), float(point[2]),
                                                                         float(point[3]),
                                                                         float(point[4]),
                                                                         float(x), float(y)))
            elif cmd_tag in ['A', 'a']:
                # a 150,150 0 1,0 150,-150
                if len(point) == 6:  #
                    last_p = point_list[idx + 1]
                    x, y = last_p[0], last_p[1]
                elif len(point) == 8:  #
                    x, y = point[6], point[7]
                else:
                    raise Exception("格式错误：", point)
                # rx ry x-axis-rotation large-arc-flag sweep-flag x y)
                # {}{:.2f},{:.2f} {:.2f} {:.2f},{:.2f} {:.2f},{:.2f
                cmds.append(
                    "{}{:.2f},{:.2f} {} {},{} {:.2f},{:.2f}".format(cmd_tag.upper(), float(point[1]), float(point[2]),
                                                                    int(point[3]),
                                                                    int(point[4]), int(point[5]), float(x), float(y)))

                # raise Exception("AAAAAAAA")
            elif cmd_tag in ['H', 'h', 'V', 'v']:
                cmds.append("{}{:.2f}".format(cmd_tag.upper(), float(point[1])))
            elif cmd_tag in ['Z', 'z']:
                cmds.append("Z")

        return cmds

    @staticmethod
    def 相对坐标转绝对坐标(path_cmds):
        # Uppercase commands indicates absolute coordinates,
        # lowercase commands indicates relative coordinates
        commands = ['M', 'L', 'H', 'V', 'C', 'S', 'Q', 'T', 'A', 'Z']
        commands_upper = [c.upper() for c in commands]
        commands_lower = [c.lower() for c in commands]
        # commands = commands_upper + commands_lower
        current_x = 0
        current_y = 0
        new_path_cmds = []
        for idx, cmd in enumerate(path_cmds):
            cmd = 神笔绘图板工具._fixed_d(cmd, idx)
            cmd_tag = cmd[0]  # path_cmds[idx-1][0] in ["h","H"] and cmd_tag in ["l","L"]
            if idx > 0:
                if cmd_tag in ["V"]:
                    current_y = 0
                elif cmd_tag in ["H"]:
                    current_x = 0
                elif cmd_tag in commands_upper:
                    current_x, current_y = 0, 0
                # else:
                #     if path_cmds[idx-1][0] in ["V"]:
                #         pass
                #     elif path_cmds[idx-1][0] in ["H"]:
                #         pass
            # M = moveto
            # L = lineto
            # H = horizontal lineto
            # V = vertical lineto
            # C = curveto
            # S = smooth curveto
            # Q = quadratic Bézier curve
            # T = smooth quadratic Bézier curveto
            # A = elliptical Arc
            # Z = closepath
            if cmd_tag in ['M', 'm', 'L', 'l', 'T', 't']:
                x, y = map(float, cmd[1:].split(','))
                current_x = current_x + x
                current_y = current_y + y  # "{}{:.2f},{:.2f}".format(cmd_tag.upper(), current_x, current_y) == "L,0.67,250.38"
                new_path_cmds.append("{}{:.2f},{:.2f}".format(cmd_tag.upper(), current_x, current_y))
            elif cmd_tag in ['Q', 'q', 'S', 's']:
                (x1, y1), (x, y) = [list(map(float, s.split(","))) for s in cmd[1:].split(" ") if s != '']
                x1 = current_x + x1
                y1 = current_y + y1
                current_x = current_x + x
                current_y = current_y + y
                new_path_cmds.append(
                    "{}{:.2f},{:.2f} {:.2f},{:.2f}".format(cmd_tag.upper(), x1, y1, current_x, current_y))
            elif cmd_tag in ['C', 'c']:
                try:
                    (x1, y1), (x2, y2), (x, y) = [list(map(float, s.split(","))) for s in cmd[1:].split(" ") if s != '']
                except Exception as e:
                    pass
                x1 = current_x + x1
                y1 = current_y + y1
                x2 = current_x + x2
                y2 = current_y + y2
                current_x = current_x + x
                current_y = current_y + y
                new_path_cmds.append(
                    "{}{:.2f},{:.2f} {:.2f},{:.2f} {:.2f},{:.2f}".format(cmd_tag.upper(), x1, y1, x2, y2, current_x,
                                                                         current_y))

            elif cmd_tag in ['H', 'h']:
                x = float(str(cmd[1:]).strip(" ,"))
                current_x = current_x + x
                new_path_cmds.append("{}{:.2f}".format(cmd_tag.upper(), current_x))
            elif cmd_tag in ['V', 'v']:
                y = float(str(cmd[1:]).rstrip(" ,"))
                current_y = current_y + y
                new_path_cmds.append("{}{:.2f}".format(cmd_tag.upper(), current_y))
            elif cmd_tag in ['Z', 'z']:
                new_path_cmds.append(cmd)
            elif cmd_tag in ['A', 'a']:
                # a 40,40 0 1,0 80,0
                # rx ry x-axis-rotation large-arc-flag sweep-flag x y)
                (rx, ry), (x_axis_rotation, large_arc_flag), (sweep_flag, x), y = [list(map(float, s.split(","))) for s
                                                                                   in cmd[1:].strip(" ,").split(" ") if
                                                                                   s != '']
                x_axis_rotation = int(x_axis_rotation)
                large_arc_flag = int(large_arc_flag)
                sweep_flag = int(sweep_flag)
                y = y[0]
                # rx = current_x + rx
                # ry = current_y + ry
                current_x = current_x + x
                current_y = current_y + y
                new_path_cmds.append(
                    "{}{:.2f},{:.2f} {} {},{} {:.2f},{:.2f}".format(cmd_tag.upper(), rx, ry, x_axis_rotation,
                                                                    large_arc_flag, sweep_flag, current_x, current_y))

        return new_path_cmds

    @staticmethod
    def _get_ellipse_bbox(ellipse):
        cx, cy, rx, ry = ellipse.attribs["cx"], ellipse.attribs["cy"], ellipse.attribs["rx"], ellipse.attribs["ry"]
        # {'fill': 'url(#_右纽扣渐变)', 'alignment-baseline': 'auto', 'stroke-width': 1.0, 'stroke': 'none', 'opacity': 1.0, 'i
        # d': 'march3_pycr_el_00007', 'cx': 430.28, 'cy': 522.04, 'rx': 33.28, 'ry': 33.45}
        min_x = round(cx - rx, 2)
        max_x = round(cx + rx, 2)
        min_y = round(cy - rx, 2)
        max_y = round(cy + rx, 2)
        return (min_x, min_y), (max_x, max_y)

    @staticmethod
    def _get_circle_bbox(circle):
        cx, cy, r = circle.attribs["cx"], circle.attribs["cy"], circle.attribs["r"]
        min_x = round(cx - r, 2)
        max_x = round(cx + r, 2)
        min_y = round(cy - r, 2)
        max_y = round(cy + r, 2)
        return (min_x, min_y), (max_x, max_y)

    @staticmethod
    def _get_text_bbox(text):
        if 为空(text.text):
            return (None, None), (None, None)
        # 'font-family': '小篆体'
        # 'text-anchor': 'middle'
        # 'font-size': 40.0
        # 'alignment-baseline': 'middle'
        if "font-family" in text.attribs:
            font_family = text.attribs["font-family"]
        else:
            font_family = ""

        if "text-anchor" in text.attribs:
            text_anchor = text.attribs["text-anchor"]
        else:
            text_anchor = ""

        if "font-size" in text.attribs:
            font_size = text.attribs["font-size"]
        else:
            font_size = ""

        if "alignment-baseline" in text.attribs:
            alignment_baseline = text.attribs["alignment-baseline"]
        else:
            alignment_baseline = ""

        x, y = text.attribs["x"], text.attribs["y"]
        x, y = float(x), float(y)
        宽, 高 = 获取文字的宽高(font_family, font_size, text.text)
        w, h = 宽, 高
        if text_anchor == 文字水平基线对齐.起始点对齐:
            min_x = round(x, 2)
            max_x = round(x + w, 2)
        elif text_anchor == 文字水平基线对齐.结束点对齐:
            min_x = round(x - w, 2)
            max_x = round(x, 2)
        else:
            min_x = round(x - w / 2, 2)
            max_x = round(x + w / 2, 2)

        if alignment_baseline == 文字垂直基线对齐.顶线对齐:
            min_y = round(y, 2)
            max_y = round(y + h, 2)
        elif alignment_baseline == 文字垂直基线对齐.底线对齐:
            min_y = round(y - h, 2)
            max_y = round(y, 2)
        else:
            min_y = round(y - h / 2, 2)
            max_y = round(y + h / 2, 2)

        # min_x = round(x - w, 2)
        # max_x = round(x + w, 2)
        # min_y = round(y - h, 2)
        # max_y = round(y + h, 2)
        return (min_x, min_y), (max_x, max_y)

    @staticmethod
    def _get_path_bbox(path):
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        commands = ['M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'C', 'c', 'S', 's', 'Q', 'q', 'T', 't', 'A', 'a', 'Z', 'z']

        current_x = 0
        current_y = 0

        for idx, command in enumerate(path.commands):
            cmd_tag = command[0]

            if idx > 0:
                if cmd_tag in ["V"]:
                    current_y = 0
                elif cmd_tag in ["H"]:
                    current_x = 0
                elif cmd_tag in ["M", "L", "T", "Q", "A", "S", "Z", "C"]:
                    current_x, current_y = 0, 0

            # if idx > 0 and cmd_tag in ["M", "L", "T", "Q", "H", "V", "A", "S", "Z", "C"]:
            #     current_x, current_y = 0, 0

            if cmd_tag in commands:
                if cmd_tag in ['M', 'm', 'L', 'l', 'T', 't']:
                    x, y = map(float, command[1:].split(','))
                    # current_x = x if cmd_tag in ['M', 'm', 'L', 'l'] else current_x + x
                    # current_y = y if cmd_tag in ['M', 'm', 'L', 'l'] else current_y + y
                    current_x = current_x + x
                    current_y = current_y + y
                    min_x = min(min_x, current_x)
                    max_x = max(max_x, current_x)
                    min_y = min(min_y, current_y)
                    max_y = max(max_y, current_y)
                elif cmd_tag in ['Q', 'q', 'S', 's']:
                    (x2, y2), (x, y) = [list(map(float, s.split(","))) for s in command[1:].split(" ") if s != '']
                    x2 = current_x + x2
                    y2 = current_y + y2
                    min_x = min(min_x, x2)
                    max_x = max(max_x, x2)
                    min_y = min(min_y, y2)
                    max_y = max(max_y, y2)

                    current_x = current_x + x
                    current_y = current_y + y
                    min_x = min(min_x, current_x)
                    max_x = max(max_x, current_x)
                    min_y = min(min_y, current_y)
                    max_y = max(max_y, current_y)
                elif cmd_tag in ['C', 'c']:
                    (x1, y1), (x2, y2), (x, y) = \
                        [list(map(float, s.split(","))) for s in command[1:].split(" ") if s != '']
                    x1 = current_x + x1
                    y1 = current_y + y1
                    min_x = min(min_x, x1)
                    max_x = max(max_x, x1)
                    min_y = min(min_y, y1)
                    max_y = max(max_y, y1)

                    x2 = current_x + x2
                    y2 = current_y + y2
                    min_x = min(min_x, x2)
                    max_x = max(max_x, x2)
                    min_y = min(min_y, y2)
                    max_y = max(max_y, y2)

                    current_x = current_x + x
                    current_y = current_y + y
                    min_x = min(min_x, current_x)
                    max_x = max(max_x, current_x)
                    min_y = min(min_y, current_y)
                    max_y = max(max_y, current_y)
                elif cmd_tag in ['H', 'h']:
                    x = float(command[1:])
                    current_x = current_x + x
                    min_x = min(min_x, current_x)
                    max_x = max(max_x, current_x)
                elif cmd_tag in ['V', 'v']:
                    y = float(command[1:])
                    current_y = current_y + y
                    min_y = min(min_y, current_y)
                    max_y = max(max_y, current_y)
                elif cmd_tag in ['a', 'A']:

                    (rx, ry), x_axis_rotation, (large_arc_flag, sweep_flag), (x, y) = [list(map(float, s.split(",")))
                                                                                       for s
                                                                                       in command[1:].split(" ") if
                                                                                       s != '']
                    # rx = current_x + rx
                    # ry = current_y + ry
                    current_x = current_x + x
                    current_y = current_y + y
                    min_x = min(min_x, current_x)
                    max_x = max(max_x, current_x)
                    min_y = min(min_y, current_y)
                    max_y = max(max_y, current_y)

                else:
                    print("未处理 cmd_tag", cmd_tag)
                    pass

        width = max_x - min_x
        height = max_y - min_y

        return (min_x, min_y), (max_x, max_y)

    @staticmethod
    def _get_group_bbox(group):
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for element in group.elements:
            (_min_x, _min_y), (_max_x, _max_y) = 神笔绘图板工具.获取元素的坐标信息(element)
            if _min_x is not None:
                min_x = min(min_x, _min_x)
            if _max_x is not None:
                max_x = max(max_x, _max_x)
            if _min_y is not None:
                min_y = min(min_y, _min_y)
            if _max_y is not None:
                max_y = max(max_y, _max_y)

        # width = max_x - min_x
        # height = max_y - min_y

        return (min_x, min_y), (max_x, max_y)

    # @staticmethod
    # def _scale_path_d(d_attr, scale_factor):
    #     # 分割 d 属性中的命令和坐标
    #     commands = re.split(r'([A-Za-z])', d_attr)
    #     scaled_commands = []
    #     for i in range(len(commands)):
    #         if i % 2 == 0:  # 如果是命令（大写或小写字母）
    #             scaled_commands.append(commands[i])
    #         else:  # 如果是坐标值
    #             # 分割坐标值并用缩放因子进行缩放
    #             coords = re.findall(r'-?\d+(\.\d+)?', commands[i])
    #             scaled_coords = [str(float(c) * scale_factor) for c in coords]
    #             scaled_commands.append(' '.join(scaled_coords))
    #             # 合并回一个字符串
    #     scaled_d = ''.join(scaled_commands)
    #     return scaled_d

    @staticmethod
    def _is_number(s):
        if s.isdigit():
            return True
        elif re.match(r'^\d+\.\d+$', s) or re.match(r'^\d+\.$', s):
            return True
        else:
            return False

    @staticmethod
    def _conv_transform(t, scale_factor):
        if t.strip().startswith("rotate"):
            return 神笔绘图板工具._conv_transform_rotate(t, scale_factor)
        elif t.strip().startswith("scale"):
            return t

        return t

    @staticmethod
    def _conv_transform(t, scale_factor):
        if "rotate" in t:
            return 神笔绘图板工具._conv_transform_rotate(t, scale_factor)
        elif t.strip().startswith("scale"):
            return t

        return t

    @staticmethod
    def _conv_transform_rotate(transform, scale_factor):
        # 匹配 rotate 中的参数
        pattern = r'rotate\((.*?),\s*(.*?),\s*(.*?)\)'
        match = re.search(pattern, transform)
        x, y = match.group(2), match.group(3)
        x = 神笔绘图板工具._conv_num(str(x).strip(), scale_factor)
        y = 神笔绘图板工具._conv_num(str(y).strip(), scale_factor)
        if match:
            # 将参数替换为新的值
            new_transform = re.sub(pattern, f'rotate({match.group(1)}, {x}, {y})', transform)
            return new_transform
        else:
            return transform

    @staticmethod
    def _conv_stroke_dasharray(std, scale_factor):
        std_lis = std.split(",")
        new_std_lis = []
        for i in std_lis:
            new_std_lis.append(神笔绘图板工具._conv_num(i.strip(), scale_factor))
        return ",".join(new_std_lis)

    @staticmethod
    def _conv_path_d_2(d, scale_factor):
        if d == "":
            return ""
        perfix = ""
        if not 神笔绘图板工具._is_number(d[0]):
            perfix = d[0]
            d = d[1:]
        d_lis = d.split(",")
        val = [神笔绘图板工具._conv_num(i, scale_factor) if 神笔绘图板工具._is_number(i) else i for i in d_lis]
        val = ",".join(val)
        return perfix + val

    @staticmethod
    def _conv_path_d(d, scale_factor):
        d_lis = d.split(" ")
        val = [神笔绘图板工具._conv_num(i, scale_factor)
               if 神笔绘图板工具._is_number(i) else 神笔绘图板工具._conv_path_d_2(i, scale_factor)
               for i in d_lis]
        val = " ".join(val)
        return val

    @staticmethod
    def _conv_num(num, scale_factor):
        str_num = str(num)
        if str_num.endswith("%"):
            return str_num
        units = ["px", "em"]
        for u in units:
            if str_num.endswith(u):
                n = str(str_num).replace(u, "")
                if "." in str_num:
                    return str(round(float(n) * scale_factor, 2)) + u
                else:
                    return str(int(int(n) * scale_factor)) + u
        if "." in str_num:
            return str(round(float(num) * scale_factor, 2))
        else:
            try:
                return str(int(int(num) * scale_factor))
            except Exception as e:
                print(str(e))
        return num

    @staticmethod
    def _scale_svg(SVG文件, 缩放, 缩放后SVG文件=None):
        tree = ET.parse(SVG文件)
        root = tree.getroot()
        svg_width, svg_height = None, None

        # 定义一个函数来递归地缩放所有元素的尺寸属性和字体大小
        def scale_element(elem):
            nonlocal svg_width, svg_height
            attribs = ["width", "height", "x", "y", "font-size", "rx", "ry", "stroke-width",
                       "cx", "cy", "r",
                       "x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "x5", "y5",
                       ]  # , "dy"

            for attr in attribs:
                if elem.tag.endswith("svg"):
                    if attr == "width":
                        attr_val = elem.attrib[attr]
                        if attr_val.endswith("%"):
                            svg_width = attr_val
                        else:
                            svg_width = int(round(float(神笔绘图板工具._conv_num(attr_val, 缩放).replace("px", "")), 0))
                    elif attr == "height":
                        attr_val = elem.attrib[attr]
                        if attr_val.endswith("%"):
                            svg_width = attr_val
                        else:
                            svg_height = int(
                                round(float(神笔绘图板工具._conv_num(attr_val, 缩放).replace("px", "")), 0))

                if ":" in attr:
                    attr_n, attr_tag = attr.split(":")
                else:
                    attr_n, attr_tag = attr, None
                # print(elem.tag)
                if attr_n in elem.attrib and (attr_tag is None or elem.tag.endswith(attr_tag)):
                    elem.attrib[attr_n] = str(神笔绘图板工具._conv_num(elem.attrib[attr_n], 缩放))

            if 'd' in elem.attrib:
                if elem.tag.endswith("path"):
                    elem.attrib['d'] = 神笔绘图板工具._conv_path_d(elem.attrib['d'], 缩放)
                else:
                    pass

            if "transform" in elem.attrib:
                elem.attrib['transform'] = 神笔绘图板工具._conv_transform(elem.attrib['transform'], 缩放)

            if "stroke-dasharray" in elem.attrib:
                elem.attrib['stroke-dasharray'] = 神笔绘图板工具._conv_stroke_dasharray(elem.attrib['stroke-dasharray'],
                                                                                        缩放)

            if "points" in elem.attrib:
                elem.attrib['points'] = 神笔绘图板工具._conv_path_d(elem.attrib['points'], 缩放)

            if 'style' in elem.attrib:
                # 尝试从 style 属性中提取并缩放字体大小
                style = elem.attrib['style']
                matches = re.findall(r'font-size:(\d+(\.\d+)?)', style)
                for match in matches:
                    new_size = str(float(match) * 缩放)
                    style = style.replace(match, new_size)
                elem.attrib['style'] = style

                # 递归地处理子元素
            for child in elem:
                scale_element(child)

                # 检查并缩放根 SVG 元素的 width 和 height

        # 对所有元素进行缩放
        scale_element(root)

        # 保存修改后的SVG文件
        tree.write(缩放后SVG文件)

        return 缩放后SVG文件, (svg_width, svg_height)


if __name__ == '__main1__':
    from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板

    svg = 神笔绘图板(作品文件路径="test.svg", 宽=800, 高=500)
    svg.显示图框()
    g = svg.创建组合()
    svg.连线([(10, 10), (100, 20), (30, 50), (10, 20)], 所属分组=g)
    (min_x, min_y), (max_x, max_y) = 神笔绘图板工具.获取元素的坐标信息(g)
    svg.完成()
    print((min_x, min_y), (max_x, max_y))

if __name__ == '__main1__':
    d = ["M10,10", "l2,2", "q1,12 13,24", "L30,30", "l20,20"]
    d = 神笔绘图板工具.点列表转SVG路径([(10, 10), ("L", 20, 20)])
    print(d)
    d1 = 神笔绘图板工具.相对坐标转绝对坐标(d)
    print(d1)
    d2 = 神笔绘图板工具.绝对坐标转相对坐标(d1)
    print(d2)
    d3 = 神笔绘图板工具.相对坐标转绝对坐标(d2)
    print(d3)


def 代码生成_原始(d):
    code = """
import svgwrite
dwg = svgwrite.Drawing('generated_code.svg', profile='tiny')

"""
    for i, cmd in enumerate(神笔绘图板工具.path_d_split(d)):
        if i == 0:
            code += f'path = dwg.path(d="{cmd}")\n'
        else:
            code += f'path.push("{cmd}")\n'
    code += """
dwg.add(path)
dwg.save()"""

    print(code)


def 代码生成_转绝对坐标(d):
    # d="m28.55,281.13c-3.28-48.54-7.4-109.55,34.47-159.32,48.87-58.09,125.5-59.36,148.6-59.74,26.68-.44,91.7-1.52,134.81,43.66,39.7,41.61,37.35,97.86,34.47,166.98-2.01,48.1-5.78,116.71-52.85,180-20.05,26.96-47.47,63.82-92.68,71.23-69.33,11.37-127-55.29-144.77-75.83-53.96-62.38-59.82-134.11-62.04-166.98Z"
    code = """
import svgwrite
dwg = svgwrite.Drawing('generated_code.svg', profile='tiny')

"""
    commands = 神笔绘图板工具.path_d_split(d)
    commands = 神笔绘图板工具.相对坐标转绝对坐标(commands)
    for i, cmd in enumerate(commands):
        if i == 0:
            code += f'path = dwg.path(d="{cmd}")\n'
        else:
            code += f'path.push("{cmd}")\n'
    code += """
dwg.add(path)
dwg.save()"""

    print(code)


def 代码生成_转框架代码(d):
    code = """
from svg_to_pdf.SVG制作 import SVG制作
from svg_to_pdf.常量 import 颜色

svg = SVG制作(SVG文件="代码生成框架代码.svg", 宽=500, 高=589)
svg.贴图(x=0, y=0, 图片文件="./images/女儿国王.jpg", 缩放=1, 旋转角度=0)
svg.图框(网格线距=20, 网格颜色=颜色.红色, 网格透明度=1, 网格字体大小=9)
路径 = []
"""
    commands = 神笔绘图板工具.path_d_split(d)
    commands = 神笔绘图板工具.相对坐标转绝对坐标(commands)
    for i, cmd in enumerate(commands):
        _cmd_tag = cmd[0]
        _cmd_vals = cmd[1:].replace(",", " ")
        code += f'路径.append(("{_cmd_tag}",'
        for c in _cmd_vals.split(" "):
            code += f'{c},'
        code = code[:-1] + ")"
        code += ')\n'
    code += """
svg.连线(路径, 描边颜色="#ff0000", 填充颜色="none", 点定位=False, 点定位坐标=False)
svg.保存()"""

    print(code)


def get_style_values(style_str):
    style_dict = {}
    style_list = style_str.split(';')
    for style in style_list:
        if ':' in style:
            key, value = style.split(':')
            style_dict[key.strip()] = value.strip()
    return style_dict


# def SVG_path_____(group_name, id_index, item, pycode, TAB, style_names):
#     if group_name is None:
#         group_name = ""
#
#     if "id" not in item.attrib:
#         item_var_name = f'{group_name.replace("-", "_")}_{id_index}'
#         id_index += 1
#     else:
#         item_var_name = item.attrib["id"].replace("-", "_")
#     # print(item)
#     # item_name = item.attrib["data-name"]
#     if "style" in item.attrib:
#         item_style = item.attrib["style"]
#     else:
#         item_style = ""
#
#     if "title" in item.attrib:
#         title = item.attrib["title"]
#     elif "id" in item.attrib:
#         title = item.attrib["id"]
#     else:
#         title = ""
#
#     styles = get_style_values(item_style)
#     fill = styles["fill"] if "fill" in styles else "none"
#
#     fill, item_var_name, style_names = style_rename(fill, item_var_name, style_names)
#
#     item_var_name = title.replace(" ", "").replace("(", "_").replace(")", "_") + "_" + item_var_name.replace("CN_", "")
#
#     stroke = styles["stroke"] if "stroke" in styles else "black"
#     # 'style': 'fill: url(#_未命名的渐变_575); stroke: #000; stroke-miterlimit: 10;'
#     path_d = item.attrib["d"]
#     pycode += f"{TAB}{item_var_name}_路径点 = [\n"
#     commands = 神笔绘图板工具.path_d_split(path_d)
#     commands = 神笔绘图板工具.相对坐标转绝对坐标(commands)
#     for i, cmd in enumerate(commands):
#         _cmd_tag = cmd[0]
#         _cmd_vals = cmd[1:].replace(",", " ")
#         # pycode += f'{TAB}{item_var_name}.append(("{_cmd_tag}",'
#         pycode += f'{TAB}{TAB}("{_cmd_tag}",'
#         for c in _cmd_vals.split(" "):
#             pycode += f'{c},'
#         pycode = pycode[:-1] + ")"
#         pycode += ',\n'
#     pycode = pycode[:-1] + f']\n'
#     pycode += f'{TAB}self.连线({item_var_name}_路径点, 描边颜色="{stroke}", 填充颜色="{fill}")\n\n'
#     return id_index, pycode, style_names


def SVG_path(group_name, id_index, item, pycode, TAB, style_names):
    if group_name is None:
        group_name = ""

    if "id" not in item.attrib:
        item_var_name = f'{group_name.replace("-", "_")}_{id_index}'
        id_index += 1
    else:
        item_var_name = item.attrib["id"].replace("-", "_")
    # print(item)
    # item_name = item.attrib["data-name"]
    if "style" in item.attrib:
        item_style = item.attrib["style"]
    else:
        item_style = ""

    if "title" in item.attrib:
        title = item.attrib["title"]
    elif "id" in item.attrib:
        title = item.attrib["id"]
    else:
        title = ""

    styles = get_style_values(item_style)
    fill = styles["fill"] if "fill" in styles else "none"

    fill, item_var_name, style_names = style_rename(fill, item_var_name, style_names)

    item_var_name = title.replace(" ", "").replace("(", "_").replace(")", "_")  # + "_" +item_var_name.replace("CN_","")

    stroke = styles["stroke"] if "stroke" in styles else "black"
    # 'style': 'fill: url(#_未命名的渐变_575); stroke: #000; stroke-miterlimit: 10;'
    path_d = item.attrib["d"]
    pycode += f"{TAB}\"{item_var_name}\" : [\n"
    commands = 神笔绘图板工具.path_d_split(path_d)
    commands = 神笔绘图板工具.相对坐标转绝对坐标(commands)
    for i, cmd in enumerate(commands):
        _cmd_tag = cmd[0]
        _cmd_vals = cmd[1:].replace(",", " ")
        # pycode += f'{TAB}{item_var_name}.append(("{_cmd_tag}",'
        pycode += f'{TAB}{TAB}("{_cmd_tag}",'  # 'V954.06'  -6.18   V954.061l-6.185,-3.053
        for c in _cmd_vals.split(" "):
            pycode += f'{c},'
        pycode = pycode[:-1] + ")"
        pycode += ',\n'
    pycode = pycode[:-1] + f'],\n'

    return id_index, pycode, style_names


def style_rename(fill, item_var_name, style_names):
    if "url(#" in fill:
        old_style_name = fill[5:-1]
        if "渐变" in fill:
            suffix = "渐变"
        else:
            suffix = "样式"
        new_style_name = item_var_name + suffix
        style_names[old_style_name] = new_style_name
        fill = f"url(#{new_style_name})"
    return fill, item_var_name, style_names


def SVG_circle(group_name, id_index, item, pycode, TAB, style_names):
    if "id" not in item.attrib:
        item_var_name = f'{group_name.replace("-", "_")}_{id_index}'
        id_index += 1
    else:
        item_var_name = item.attrib["id"].replace("-", "_")

    cx, cy = item.attrib["cx"], item.attrib["cy"]
    r = item.attrib["r"]
    cx, cy = float(cx), float(cy)
    r = float(r)

    if "transform" in item.attrib:
        transform = item.attrib["transform"]
    else:
        transform = None

    item_style = item.attrib["style"]
    styles = get_style_values(item_style)
    fill = styles["fill"] if "fill" in styles else "none"

    fill, item_var_name, style_names = style_rename(fill, item_var_name, style_names)

    stroke = styles["stroke"] if "stroke" in styles else "black"
    # svg.画椭圆(x=520, y=180, 半径=(10, 20), 描边颜色=颜色.浅宝石蓝色, 填充颜色=渐变色1.颜色引用, 描边样式="5,5")
    pycode += f'{TAB}{item_var_name} = self.画圆(x={cx}, y={cy}, 半径={r}, 描边颜色="{stroke}", 填充颜色="{fill}")\n'

    if transform is not None:
        pycode += f'{TAB}{item_var_name}["transform"] = "{transform}"\n\n'
    else:
        pycode += "\n"

    return id_index, pycode, style_names


def SVG_ellipse(group_name, id_index, item, pycode, TAB, style_names):
    if "id" not in item.attrib:
        item_var_name = f'{group_name.replace("-", "_")}_{id_index}'
        id_index += 1
    else:
        item_var_name = item.attrib["id"].replace("-", "_")

    cx, cy = item.attrib["cx"], item.attrib["cy"]
    rx, ry = item.attrib["rx"], item.attrib["ry"]
    cx, cy = float(cx), float(cy)
    rx, ry = float(rx), float(ry)

    # cx="420.61" cy="236.9" rx="18.93" ry="32.57" transform="translate(-44.82 108.79) rotate(-14)" style="fill: #50dce9; stroke-width: 0px;"

    if "transform" in item.attrib:
        transform = item.attrib["transform"]
    else:
        transform = None

    item_style = item.attrib["style"]
    styles = get_style_values(item_style)
    fill = styles["fill"] if "fill" in styles else "none"

    fill, item_var_name, style_names = style_rename(fill, item_var_name, style_names)

    stroke = styles["stroke"] if "stroke" in styles else "black"
    # svg.画椭圆(x=520, y=180, 半径=(10, 20), 描边颜色=颜色.浅宝石蓝色, 填充颜色=渐变色1.颜色引用, 描边样式="5,5")
    pycode += f'{TAB}{item_var_name} = self.画椭圆(x={cx}, y={cy}, 半径=({rx}, {ry}), 描边颜色="{stroke}", 填充颜色="{fill}")\n'

    if transform is not None:
        pycode += f'{TAB}{item_var_name}["transform"] = "{transform}"\n\n'
    else:
        pycode += "\n"

    return id_index, pycode, style_names


def SVG_group(elm, pycode, fun_names, TAB, style_names):
    print("SVG_group", elm)

    if "data-name" in elm.attrib:
        group_name = elm.attrib["data-name"].replace("-", "_")  # elm.attrib["id"]

        if f"def {group_name}(self):\n" in pycode:
            return pycode, fun_names, style_names

        if group_name in fun_names:
            # print("重复方法名称", group_name)
            return pycode, fun_names, style_names

        pycode += f"def {group_name}(self):\n"
        fun_names += f"{TAB}{group_name}(高清图)\n"
    else:
        group_name = None
        # print(elm.attrib["id"], elm.attrib["data-name"])
    id_index = 0
    elm_list = list(elm.iter())
    for item in elm_list:
        if item is not elm:
            if item.tag.endswith("}path"):
                id_index, pycode, style_names = SVG_path(group_name, id_index, item, pycode, TAB, style_names)
            elif item.tag.endswith("}ellipse"):
                id_index, pycode, style_names = SVG_ellipse(group_name, id_index, item, pycode, TAB, style_names)
            elif item.tag.endswith("}circle"):
                id_index, pycode, style_names = SVG_circle(group_name, id_index, item, pycode, TAB, style_names)
            elif item.tag.endswith("}image") or item.tag.endswith("}g"):
                pass
            else:
                raise Exception("未处理 item.tag = ", item.tag)
            # elif item.tag.endswith("}g"):
            #     pycode, fun_names = SVG_group(item, pycode, fun_names, TAB)
    if id_index == 0:
        pycode += f"{TAB}pass\n\n"

    return pycode, fun_names, style_names


def SVG_defs(elm, defs, TAB, style_names):
    code = ""
    for item in elm.iter():
        if item is elm:
            continue

        if item.tag.endswith("}linearGradient"):
            id = item.attrib["id"]
            if id in style_names:
                id = style_names[id]
            x1, y1 = item.attrib["x1"], item.attrib["y1"]
            x2, y2 = item.attrib["x2"], item.attrib["y2"]
            x1, y1 = float(x1), float(y1)
            x2, y2 = float(x2), float(y2)
            stop_infos = []
            stop_list = list(item.iter())[1:]
            if len(stop_list) == 0:
                continue

            for stop_idx, stop in enumerate(stop_list):
                # {'offset': '.01', 'stop-color': '#666767'}
                if "offset" in stop.attrib:
                    offset = stop.attrib["offset"]
                else:
                    offset = "0.5"
                if "stop-color" in stop.attrib:
                    stop_color = stop.attrib["stop-color"]
                else:
                    stop_color = "none"

                if "opacity" in stop.attrib:
                    opacity = stop.attrib["opacity"]
                else:
                    opacity = 1.0

                stop_info = {"偏移": offset, "颜色": stop_color, "透明度": opacity}
                stop_infos.append(stop_info)

            start_color = stop_infos[0]["颜色"]
            start_offset = stop_infos[0]["偏移"]
            start_alpha = stop_infos[0]["透明度"]
            end_color = stop_infos[-1]["颜色"]
            end_offset = stop_infos[-1]["偏移"]
            end_alpha = stop_infos[-1]["透明度"]

            if len(stop_list) == 2:
                add_stop_color = "[]"
            else:
                code += f'{TAB}{id}中间点 = [\n'
                for stop_info in stop_infos[1:-2]:
                    if stop_info["透明度"] == 1:
                        code += f'{TAB}{TAB}{{"偏移": "{stop_info["偏移"]}", "颜色": "{stop_info["颜色"]}"}},\n'
                    else:
                        code += f'{TAB}{TAB}{{"偏移": "{stop_info["偏移"]}", "颜色": "{stop_info["颜色"]}", "透明度": {stop_info["透明度"]}}},\n'
                code += f'{TAB}]\n'
                add_stop_color = f"{id}中间点"
                # add_stop_color = "[]"

            code += f'{TAB}self.创建线性渐变色(开始位置=({x1}, {y1}), 结束位置=({x2}, {y2}), 开始颜色="{start_color}", 结束颜色="{end_color}", \n' \
                    f'{TAB}{TAB}{TAB}开始偏移="{start_offset}", 结束偏移="{end_offset}",开始透明度={start_alpha}, 结束透明度={end_alpha}, \n' \
                    f'{TAB}{TAB}{TAB}增加渐变中间点={add_stop_color},id="{id}")\n'
        elif item.tag.endswith("}stop"):
            pass
        elif item.tag.endswith("}radialGradient"):
            id = item.attrib["id"]
            if id in style_names:
                id = style_names[id]

            cx, cy = item.attrib["cx"], item.attrib["cy"]
            fx, fy = item.attrib["fx"], item.attrib["fy"]
            r = item.attrib["r"]
            cx, cy = float(cx), float(cy)
            fx, fy = float(fx), float(fy)
            渐变的焦点 = f"({fx}, {fy})"
            r = float(r)
            if "gradientTransform" in item.attrib:
                gradientTransform = item.attrib["gradientTransform"]
            else:
                gradientTransform = None

            stop_infos = []
            stop_list = list(item.iter())[1:]
            if len(stop_list) == 0:
                continue

            for stop_idx, stop in enumerate(stop_list):
                # {'offset': '.01', 'stop-color': '#666767'}
                if "offset" in stop.attrib:
                    offset = stop.attrib["offset"]
                else:
                    offset = "0.5"
                if "stop-color" in stop.attrib:
                    stop_color = stop.attrib["stop-color"]
                else:
                    stop_color = "none"

                if "opacity" in stop.attrib:
                    opacity = stop.attrib["opacity"]
                else:
                    opacity = 1.0

                stop_info = {"偏移": offset, "颜色": stop_color, "透明度": opacity}
                stop_infos.append(stop_info)

            start_color = stop_infos[0]["颜色"]
            start_offset = stop_infos[0]["偏移"]
            start_alpha = stop_infos[0]["透明度"]
            end_color = stop_infos[-1]["颜色"]
            end_offset = stop_infos[-1]["偏移"]
            end_alpha = stop_infos[-1]["透明度"]

            if len(stop_list) == 2:
                add_stop_color = "[]"
            else:
                code += f'{TAB}{id}中间点 = [\n'
                for stop_info in stop_infos[1:-2]:
                    if stop_info["透明度"] == 1:
                        code += f'{TAB}{TAB}{{"偏移": "{stop_info["偏移"]}", "颜色": "{stop_info["颜色"]}"}},\n'
                    else:
                        code += f'{TAB}{TAB}{{"偏移": "{stop_info["偏移"]}", "颜色": "{stop_info["颜色"]}", "透明度": {stop_info["透明度"]}}},\n'

                code += f'{TAB}]\n'
                add_stop_color = f"{id}中间点"
                # add_stop_color = "[]"

            if gradientTransform is None:
                code += f'{TAB}'
            else:
                code += f'{TAB}{id} = '

            code += f'self.创建径向渐变色(渐变开始中心点=({cx},{cy}), 渐变半径={r},  开始颜色="{start_color}", 结束颜色="{end_color}", \n' \
                    f'{TAB}{TAB}{TAB}开始偏移="{start_offset}", 结束偏移="{end_offset}",开始透明度={start_alpha}, 结束透明度={end_alpha}, \n' \
                    f'{TAB}{TAB}{TAB}增加渐变中间点={add_stop_color},渐变的焦点={渐变的焦点},id="{id}")\n'

            if gradientTransform is not None:
                code += f'{TAB}{id}["gradientTransform"]="{gradientTransform}"\n\n'
        else:
            print("未处理", item.tag)
            pass

    defs += code

    return defs


def 读取SVG生成代码(SVG文件, py文件):
    tree = ET.parse(SVG文件)
    root = tree.getroot()
    pycode = """# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os

from svg_to_pdf.神笔绘图板 import 神笔绘图板
from svg_to_pdf.神笔绘图板工具 import 神笔绘图板工具
from svg_to_pdf.常量 import *
from svg_to_pdf.渐变色元素 import * 


点定位 = False
点定位坐标 = False
"""
    fun_names = ""
    defs = ""
    _pycode = ""
    TAB = "    "
    style_names = {}

    for elm in root:
        if elm.tag.endswith("}g"):
            _pycode, fun_names, style_names = SVG_group(elm, _pycode, fun_names, TAB, style_names)

    for elm in root:
        if elm.tag.endswith("}defs"):
            defs = SVG_defs(elm, defs, TAB, style_names)
            #
    fun_names = f"{TAB}创建渐变色样式(高清图)\n" + fun_names
    if defs == "":
        defs = f"{TAB}pass\n"
    pycode += "def 创建渐变色样式(self):\n" + defs
    pycode += _pycode
    pycode += """
if __name__ == '__main__':
    高清图 = 神笔绘图板(作品文件路径="#{SVG文件}.svg", 宽=800, 高=800)
    # 高清图.贴图(x=-100, y=0, 图片文件="./images/超级玛丽_AI.svg", 缩放=1, 旋转角度=0)
    高清图.图框(网格线距=20, 网格颜色=颜色.红色, 网格透明度=1, 网格字体大小=9)
#{方法}
    高清图.保存() 
    """.replace("#{方法}", fun_names).replace("#{SVG文件}", py文件[:-3])

    with open(py文件, mode='w', encoding="utf-8") as f:
        f.write(pycode)
    # print(pycode)


def 下载html(url):
    import requests

    response = requests.get(url)
    filename = os.path.basename(url).replace("-", "_")

    if not filename.endswith(".html"):
        filename = filename + ".html"

    with open(filename, 'w', encoding="utf-8") as file:
        file.write(response.text)

    return filename


def 分析SVG(文件, tmp_dir_name=None):
    if tmp_dir_name is None:
        tmp_dir_name = os.path.basename(文件).replace(".html", "")
    import re
    from bs4 import BeautifulSoup

    # 读取HTML文件
    with open(文件, 'r', encoding="utf-8") as file:
        html_content = file.read()

    # 解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')
    # tmp_dir_name = "flag"
    if not os.path.exists(tmp_dir_name):
        os.makedirs(tmp_dir_name)

    # 查找所有的SVG标签
    svg_tags = soup.find_all('svg')
    c = 0
    # 遍历每个SVG标签并将其保存为SVG文件
    for i, svg_tag in enumerate(svg_tags):
        if "data-tip" not in svg_tag.parent.attrs:
            continue
        data_tip = svg_tag.parent.attrs["data-tip"].replace(":", "-")
        viewbox = svg_tag.attrs["viewbox"]
        viewboxs = viewbox.split(" ")
        width = int(viewboxs[2])
        svg_tag.attrs["width"] = viewboxs[2]
        svg_tag.attrs["height"] = viewboxs[3]
        svg_content = str(svg_tag)

        if width < 20:
            scale = 15
        elif width < 50:
            scale = 5
        elif width < 100:
            scale = 3
        elif width < 150:
            scale = 2
        else:
            scale = 0

        filename_ = f'{tmp_dir_name}/{tmp_dir_name}_{data_tip}.svg'

        if scale > 0:
            filename1 = f'{tmp_dir_name}/{tmp_dir_name}_{data_tip}_tmp.svg'
            with open(filename1, 'w', encoding="utf-8") as file:
                file.write(svg_content)
            from 神笔码靓.神笔库.cairosvg工具集 import CairoSvg工具集
            CairoSvg工具集.放大SVG(url=filename1, save_as=filename_, scale=scale)
            if os.path.exists(filename1):
                os.remove(filename1)
        else:
            with open(filename_, 'w', encoding="utf-8") as file:
                file.write(svg_content)

        c += 1

        # if c > 10:
        #     break


def svg_index_html(root_dir):
    import os
    import re

    # 获取当前目录下所有的 SVG 文件名
    svg_files = [f for f in os.listdir(root_dir) if re.match(r'.*\.svg$', f)]

    # 生成 HTML 页面
    html = '<!DOCTYPE html><html><head><style>img { width: 64px; padding:6px; }</style></head><body>'
    for svg_file in svg_files:
        html += f'<a target="_blank" href="{svg_file}"><img title="{svg_file}" src="{svg_file}"></a>'
    html += '</body></html>'

    # 将 HTML 页面保存为 index.html
    with open(os.path.join(root_dir, '_图片索引.html'), 'w') as f:
        f.write(html)


# if __name__ == '__main__':
#     from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
#
#     宽, 高 = 纸张大小.A4_横向(1)
#     神笔 = 神笔绘图板(作品文件路径="神笔绘图板倒角.svg", 宽=宽, 高=高)
#     神笔.连线(路径点列表=[("移动", 130, 100),
#                  ("直线", 200, 130),
#                  ("水平线", 200),
#                  # ("倒圆角", 40),
#                  ("倒角", 50),
#                  ("直线", 200, 240)])
#     神笔.完成()

if __name__ == '__main__':
    # filename = 下载html(url="https://yesicon.app/")
    # 分析SVG(filename)
    # 分析SVG("SVG解析.html", "boy")

    # svg_index_html(资源库目录("图标\目录"))

    # svg = 资源库目录("素材/三原色/红黄蓝三原色.svg")
    # 读取SVG生成代码(svg, "./三原色_.py")
    # exit(0)
    path_d = """
m84.26,180.74c-7.82-6.33-7.96-2.65-19.4-4.6-22.98-3.91-22.68-16.14-22.98-18.04-.51-3.3,1.95-5.09,3.93-9.97,1.47-3.64,2.03-7.47,1.94-18.71-.02-3.2,4.09-2.43,6.26-13.74.69-3.6.26-7.97,1.96-10.43,1.74-2.52-.14-5.97,1.06-6.85,3.06-2.26,8.68-.72,9.87-10.6,1.02-8.45-4.94-5.76-4.77-10.55.55-14.9-2.29-33.6-.85-46.55.36-3.27,2.95-3.6,3.23-7.23.79-10.01.37-22.46-.33-22.78-1.44-.65-1.78.58-2.22.73-1.31.46-4.6,6.38-6.21,14.55-1.55,7.84.3,11.21-1.19,17.96-2.13,9.62-5.79,28-6.89,28.17-4.21.65-16.04-1.72-21.02,2.55-3.83,3.29,1.08,3.3-4.26,9.02-1.19,1.28-6.14-.14-6.89,1.19-.72,1.27,1.43,3.23.68,4.09-.38.43-1.22-.27-2.04.17-1.26.68-.45,2.92-1.53,5.53-.95,2.3-2.24,2.15-2.55,3.49-.78,3.32,6.99,5.13,10.55,11.91,3.3,6.28,1.28,13.52.68,15.66-1.17,4.21-3.31,6.95-3.74,7.83-1.53,3.06-14.48,8.22-16.34,14.13-2.89,9.19,4.09,12.6,4.77,16.85.72,4.53,6.3,27.57,21.79,45.11,8.13,9.2,27.65,25.12,39.49,23.83,9.36-1.02,20.08-4.32,22.98-16.85,2.38-10.28,1.19-20.09-5.96-25.87Zm-47.45-66.43c-.26-.68-.33-6.05.09-8.34.52-2.85,1.46-4.51,2.6-5.83.19-.22,1.87-2.61,2.98-2.09.84.4.74,2.24.68,3.28-.14,2.57-.93,4.66-1.36,6.09-1.83,6.04-4.63,7.81-4.98,6.89Z
"""
    commands = 神笔绘图板工具.path_d_split(path_d)
    commands = 神笔绘图板工具.相对坐标转绝对坐标(commands)
    list_code = "["
    for i, cmd in enumerate(commands):
        list_code += f'("{cmd[0]}",{cmd[1:].replace(" ", ",")}), \n'
    list_code += "]"
    print(list_code)
