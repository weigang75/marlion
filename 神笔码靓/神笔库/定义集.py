# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import math
import random
from enum import Enum
from dataclasses import dataclass
from 神笔码靓.神笔库.通用工具集 import 是否为数值, 是否系统字体


class 颜色:
    _颜色字典 = {
        "黑色": ("black", "#000000"),
        "海军色": ("navy", "#000080"),
        "暗蓝色": ("darkblue", "#00008b"),
        "中兰色": ("mediumblue", "#0000cd"),
        "蓝色": ("blue", "#0000ff"),
        "暗绿色": ("darkgreen", "#006400"),
        "绿色": ("green", "#008000"),
        "水鸭色": ("teal", "#008080"),
        "暗青色": ("darkcyan", "#008b8b"),
        "深天蓝色": ("deepskyblue", "#00bfff"),
        "暗宝石绿": ("darkturquoise", "#00ced1"),
        "中春绿色": ("mediumspringgreen", "#00fa9a"),
        "酸橙色": ("lime", "#00ff00"),
        "春绿色": ("springgreen", "#00ff7f"),
        "浅绿色": ("aqua", "#00ffff"),
        "中灰兰色": ("midnightblue", "#191970"),
        "闪兰色": ("dodgerblue", "#1e90ff"),
        "亮海蓝色": ("lightseagreen", "#20b2aa"),
        # "亮海蓝色": ("#00799E", "#00799E"),
        "森林绿": ("forestgreen", "#228b22"),
        "海绿色": ("seagreen", "#2e8b57"),
        "暗瓦灰色": ("darkslategray", "#2f4f4f"),
        "橙绿色": ("limegreen", "#32cd32"),
        "中海蓝": ("mediumseagreen", "#3cb371"),
        "青绿色": ("turquoise", "#40e0d0"),
        "皇家蓝": ("royalblue", "#4169e1"),
        "钢兰色": ("steelblue", "#4682b4"),
        "暗灰蓝色": ("darkslateblue", "#483d8b"),
        "中绿宝石": ("mediumturquoise", "#48d1cc"),
        "靛青色": ("indigo", "#4b0082"),
        "青色": ("cyan", "#00ffff"),
        "暗橄榄绿": ("darkolivegreen", "#556b2f"),
        "军兰色": ("cadetblue", "#5f9ea0"),
        "菊兰色": ("cornflowerblue", "#6495ed"),
        "中绿色": ("mediumaquamarine", "#66cdaa"),
        "暗灰色": ("dimgray", "#696969"),
        "石蓝色": ("slateblue", "#6a5acd"),
        "深绿褐色": ("olivedrab", "#6b8e23"),
        "灰石色": ("slategray", "#708090"),
        "亮蓝灰": ("lightslategray", "#778899"),
        "中暗蓝色": ("mediumslateblue", "#7b68ee"),
        "草绿色": ("lawngreen", "#7cfc00"),
        "黄绿色": ("chartreuse", "#7fff00"),
        "碧绿色": ("aquamarine", "#7fffd4"),
        "粟色": ("maroon", "#800000"),
        "紫色": ("purple", "#800080"),
        "橄榄色": ("olive", "#808000"),
        "灰色": ("gray", "#808080"),
        "天蓝色": ("skyblue", "#87ceeb"),
        "亮天蓝色": ("lightskyblue", "#87cefa"),
        "紫罗兰蓝色": ("blueviolet", "#8a2be2"),
        "暗红色": ("darkred", "#8b0000"),
        "暗洋红": ("darkmagenta", "#8b008b"),
        "重褐色": ("saddlebrown", "#8b4513"),
        "暗海兰色": ("darkseagreen", "#8fbc8f"),
        "亮绿色": ("lightgreen", "#90ee90"),
        "中紫色": ("mediumpurple", "#9370db"),
        "暗紫罗兰色": ("darkviolet", "#9400d3"),
        "苍绿色": ("palegreen", "#98fb98"),
        "暗紫色": ("darkorchid", "#9932cc"),
        "赭色": ("sienna", "#a0522d"),
        "褐色": ("brown", "#a52a2a"),
        "深灰色": ("darkgray", "#a9a9a9"),
        "亮蓝色": ("lightblue", "#add8e6"),
        "绿黄色": ("greenyellow", "#adff2f"),
        "苍宝石绿": ("paleturquoise", "#afeeee"),
        "亮钢兰色": ("lightsteelblue", "#b0c4de"),
        "粉蓝色": ("powderblue", "#b0e0e6"),
        "火砖色": ("firebrick", "#b22222"),
        "暗金黄色": ("darkgoldenrod", "#b8860b"),
        "中粉紫色": ("mediumorchid", "#ba55d3"),
        "褐玫瑰红": ("rosybrown", "#bc8f8f"),
        "暗黄褐色": ("darkkhaki", "#bdb76b"),
        "银色": ("silver", "#c0c0c0"),
        "中紫罗兰色": ("mediumvioletred", "#c71585"),
        "印第安红": ("indianred", "#cd5c5c"),
        "秘鲁色": ("peru", "#cd853f"),
        "巧可力色": ("chocolate", "#d2691e"),
        "茶色": ("tan", "#d2b48c"),
        "亮灰色": ("lightgray", "#d3d3d3"),
        "蓟色": ("thistle", "#d8bfd8"),
        "淡紫色": ("orchid", "#da70d6"),
        "金麒麟色": ("goldenrod", "#daa520"),
        "苍紫罗兰色": ("palevioletred", "#db7093"),
        "暗深红色": ("crimson", "#dc143c"),
        "淡灰色": ("gainsboro", "#dcdcdc"),
        "洋李色": ("plum", "#dda0dd"),
        "实木色": ("burlywood", "#deb887"),
        "亮青色": ("lightcyan", "#e0ffff"),
        "薰衣草": ("lavender", "#e6e6fa"),
        "暗肉色": ("darksalmon", "#e9967a"),
        "紫罗兰色": ("violet", "#ee82ee"),
        "苍麒麟色": ("palegoldenrod", "#eee8aa"),
        "亮珊瑚色": ("lightcoral", "#f08080"),
        "黄褐色": ("khaki", "#f0e68c"),
        "艾利斯兰": ("aliceblue", "#f0f8ff"),
        "蜜色": ("honeydew", "#f0fff0"),
        "蔚蓝色": ("azure", "#f0ffff"),
        "沙褐色": ("sandybrown", "#f4a460"),
        "浅黄色": ("wheat", "#f5deb3"),
        "米色": ("beige", "#f5f5dc"),
        "烟白色": ("whitesmoke", "#f5f5f5"),
        "薄荷色": ("mintcream", "#f5fffa"),
        "幽灵白": ("ghostwhite", "#f8f8ff"),
        "鲜肉色": ("salmon", "#fa8072"),
        "古董白": ("antiquewhite", "#faebd7"),
        "亚麻色": ("linen", "#faf0e6"),
        "亮金黄色": ("lightgoldenrodyellow", "#fafad2"),
        "老花色": ("oldlace", "#fdf5e6"),
        "红色": ("red", "#ff0000"),
        "紫红色": ("fuchsia", "#ff00ff"),
        "深粉红色": ("deeppink", "#ff1493"),
        "红橙色": ("orangered", "#ff4500"),
        "西红柿色": ("tomato", "#ff6347"),
        "热粉红色": ("hotpink", "#ff69b4"),
        "珊瑚色": ("coral", "#ff7f50"),
        "暗桔黄色": ("darkorange", "#ff8c00"),
        "亮肉色": ("lightsalmon", "#ffa07a"),
        "橙色": ("orange", "#ffa500"),
        "亮粉红色": ("lightpink", "#ffb6c1"),
        "粉红色": ("pink", "#ffc0cb"),
        "金色": ("gold", "#ffd700"),
        "桃色": ("peachpuff", "#ffdab9"),
        "纳瓦白": ("navajowhite", "#ffdead"),
        "鹿皮色": ("moccasin", "#ffe4b5"),
        "桔黄色": ("bisque", "#ffe4c4"),
        "浅玫瑰色": ("mistyrose", "#ffe4e1"),
        "白杏色": ("blanchedalmond", "#ffebcd"),
        "番木色": ("papayawhip", "#ffefd5"),
        "淡紫红": ("lavenderblush", "#fff0f5"),
        "海贝色": ("seashell", "#fff5ee"),
        "米绸色": ("cornsilk", "#fff8dc"),
        "柠檬绸色": ("lemonchiffon", "#fffacd"),
        "花白色": ("floralwhite", "#fffaf0"),
        "雪白色": ("snow", "#fffafa"),
        "黄色": ("yellow", "#ffff00"),
        "亮黄色": ("lightyellow", "#ffffe0"),
        "象牙色": ("ivory", "#fffff0"),
        "白色": ("white", "#ffffff"),

    }
    无 = ""
    透明 = "none"
    黑色 = "black"
    海军色 = "navy"
    暗蓝色 = "darkblue"
    中兰色 = "mediumblue"
    蓝色 = "blue"
    暗绿色 = "darkgreen"
    绿色 = "green"
    水鸭色 = "teal"
    暗青色 = "darkcyan"
    深天蓝色 = "deepskyblue"
    暗宝石绿 = "darkturquoise"
    中春绿色 = "mediumspringgreen"
    酸橙色 = "lime"
    春绿色 = "springgreen"
    浅绿色 = "aqua"
    中灰兰色 = "midnightblue"
    闪兰色 = "dodgerblue"
    亮海蓝色 = "lightseagreen"
    海蓝色 = "#00799E"
    森林绿 = "forestgreen"
    海绿色 = "seagreen"
    暗瓦灰色 = "darkslategray"
    橙绿色 = "limegreen"
    中海蓝 = "mediumseagreen"
    青绿色 = "turquoise"
    皇家蓝 = "royalblue"
    钢兰色 = "steelblue"
    暗灰蓝色 = "darkslateblue"
    中绿宝石 = "mediumturquoise"
    靛青色 = "indigo"
    青色 = "cyan"
    暗橄榄绿 = "darkolivegreen"
    军兰色 = "cadetblue"
    菊兰色 = "cornflowerblue"
    中绿色 = "mediumaquamarine"
    暗灰色 = "dimgray"
    石蓝色 = "slateblue"
    深绿褐色 = "olivedrab"
    灰石色 = "slategray"
    亮蓝灰 = "lightslategray"
    中暗蓝色 = "mediumslateblue"
    草绿色 = "lawngreen"
    黄绿色 = "chartreuse"
    碧绿色 = "aquamarine"
    粟色 = "maroon"
    紫色 = "purple"
    橄榄色 = "olive"
    灰色 = "gray"
    天蓝色 = "skyblue"
    亮天蓝色 = "lightskyblue"
    紫罗兰蓝色 = "blueviolet"
    暗红色 = "darkred"
    暗洋红 = "darkmagenta"
    重褐色 = "saddlebrown"
    暗海兰色 = "darkseagreen"
    亮绿色 = "lightgreen"
    中紫色 = "mediumpurple"
    暗紫罗兰色 = "darkviolet"
    苍绿色 = "palegreen"
    暗紫色 = "darkorchid"
    赭色 = "sienna"
    褐色 = "brown"
    深灰色 = "darkgray"
    亮蓝色 = "lightblue"
    绿黄色 = "greenyellow"
    苍宝石绿 = "paleturquoise"
    亮钢兰色 = "lightsteelblue"
    粉蓝色 = "powderblue"
    火砖色 = "firebrick"
    暗金黄色 = "darkgoldenrod"
    中粉紫色 = "mediumorchid"
    褐玫瑰红 = "rosybrown"
    暗黄褐色 = "darkkhaki"
    银色 = "silver"
    中紫罗兰色 = "mediumvioletred"
    印第安红 = "indianred"
    秘鲁色 = "peru"
    巧可力色 = "chocolate"
    茶色 = "tan"
    亮灰色 = "lightgray"
    蓟色 = "thistle"
    淡紫色 = "orchid"
    金麒麟色 = "goldenrod"
    苍紫罗兰色 = "palevioletred"
    暗深红色 = "crimson"
    淡灰色 = "gainsboro"
    洋李色 = "plum"
    实木色 = "burlywood"
    亮青色 = "lightcyan"
    薰衣草 = "lavender"
    暗肉色 = "darksalmon"
    紫罗兰色 = "violet"
    苍麒麟色 = "palegoldenrod"
    亮珊瑚色 = "lightcoral"
    黄褐色 = "khaki"
    艾利斯兰 = "aliceblue"
    蜜色 = "honeydew"
    蔚蓝色 = "azure"
    沙褐色 = "sandybrown"
    浅黄色 = "wheat"
    米色 = "beige"
    烟白色 = "whitesmoke"
    薄荷色 = "mintcream"
    幽灵白 = "ghostwhite"
    鲜肉色 = "salmon"
    古董白 = "antiquewhite"
    亚麻色 = "linen"
    亮金黄色 = "lightgoldenrodyellow"
    老花色 = "oldlace"
    红色 = "red"
    紫红色 = "fuchsia"
    深粉红色 = "deeppink"
    红橙色 = "orangered"
    西红柿色 = "tomato"
    热粉红色 = "hotpink"
    珊瑚色 = "coral"
    暗桔黄色 = "darkorange"
    亮肉色 = "lightsalmon"
    橙色 = "orange"
    亮粉红色 = "lightpink"
    粉红色 = "pink"
    金色 = "gold"
    桃色 = "peachpuff"
    纳瓦白 = "navajowhite"
    鹿皮色 = "moccasin"
    桔黄色 = "bisque"
    浅玫瑰色 = "mistyrose"
    白杏色 = "blanchedalmond"
    番木色 = "papayawhip"
    淡紫红 = "lavenderblush"
    海贝色 = "seashell"
    米绸色 = "cornsilk"
    柠檬绸色 = "lemonchiffon"
    花白色 = "floralwhite"
    雪白色 = "snow"
    黄色 = "yellow"
    亮黄色 = "lightyellow"
    象牙色 = "ivory"
    白色 = "white"

    @staticmethod
    def 随机色():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    @staticmethod
    def 反色(颜色值):
        # from 神笔码靓.神笔库.定义集 import 颜色
        if not str(颜色值).startswith("#"):
            颜色值 = 颜色.转16进制颜色(颜色值)
        # 在这里用 python 代码实现, 将 颜色值 格式为: #D75D72 进行颜色加深
        # 将十六进制颜色值转换为 RGB
        r = int(颜色值[1:3], 16)
        g = int(颜色值[3:5], 16)
        b = int(颜色值[5:7], 16)

        # 根据加深程度调整颜色
        r = 255 - r
        g = 255 - g
        b = 255 - b

        # 将 RGB 值转换回十六进制格式
        return f'#{r:02X}{g:02X}{b:02X}'

    @staticmethod
    def RGB(R=None, G=None, B=None):
        """
        实现 RGB 颜色
        返回格式为 #rrggbb
        :param R:
        :param G:
        :param B:
        :return:
        """
        if not 是否为数值(R):
            颜色名称 = R
            if 颜色名称 is not None:
                if 颜色名称 in 颜色._颜色字典:
                    return 颜色._颜色字典[颜色名称][1]
        else:
            if R is None or G is None or G is None:
                return None
            return "#{:02x}{:02x}{:02x}".format(R, G, B)

    @staticmethod
    def 英文名(颜色名称):
        if 颜色名称 in 颜色._颜色字典:
            return 颜色._颜色字典[颜色名称][0]
        return None

    @staticmethod
    def 转16进制颜色(英文颜色名):
        if 英文颜色名 is None:
            return None

        if 英文颜色名 in 颜色._颜色字典:
            return 颜色._颜色字典[英文颜色名][1]

        if not hasattr(颜色, "_英文颜色字典"):
            _英文颜色字典 = {}
            for 中文 in 颜色._颜色字典.keys():
                英文, 颜色值 = 颜色._颜色字典[中文]
                _英文颜色字典[英文] = (中文, 颜色值)
            setattr(颜色, "_英文颜色字典", _英文颜色字典)

        _英文颜色字典 = getattr(颜色, "_英文颜色字典")
        if 英文颜色名 in 颜色._英文颜色字典:
            return 颜色._英文颜色字典[英文颜色名][1]

        return 英文颜色名

    @staticmethod
    def 十六进制转RGB(hex_color):
        """将16进制颜色值转换为RGB元组"""
        if not hex_color:
            return (0, 0, 0)

        # 去除可能的前缀
        hex_color = hex_color.lstrip('#')

        # 处理3位和6位格式
        if len(hex_color) == 3:
            hex_color = ''.join([c * 2 for c in hex_color])

        if len(hex_color) != 6:
            return (0, 0, 0)

        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        except ValueError:
            return (0, 0, 0)

    @staticmethod
    def RGB转十六进制(rgb):
        """将RGB元组转换为16进制颜色值"""
        r, g, b = rgb
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def 多色相加(颜色集合, 保留透明度=False):
        """
        将多个颜色连续相加

        参数:
            颜色集合: 包含多个颜色的列表，可以是16进制颜色值或英文颜色名
            保留透明度: 是否保留透明度信息

        返回:
            相加后的16进制颜色值
        """
        if 颜色集合 is None:
            return None
        if len(颜色集合) == 0:
            return None
        elif len(颜色集合) == 1:
            # 单个颜色直接返回
            颜色值 = 颜色集合[0]
            return 颜色.转16进制颜色(颜色值) if isinstance(颜色值, str) else 颜色值

        # 初始化结果为第一个颜色
        result = 颜色集合[0]

        # 依次将后续颜色相加
        for color in 颜色集合[1:]:
            result = 颜色.颜色相加(result, color, 保留透明度)

        return result

    @staticmethod
    def 颜色相加(颜色1, 颜色2, 保留透明度=False):
        """
        将两种颜色相加

        参数:
            颜色1: 可以是16进制颜色值或英文颜色名
            颜色2: 可以是16进制颜色值或英文颜色名
            保留透明度: 是否保留透明度信息

        返回:
            相加后的16进制颜色值
        """
        # 转换颜色为16进制
        hex1 = 颜色.转16进制颜色(颜色1) if isinstance(颜色1, str) else 颜色1
        hex2 = 颜色.转16进制颜色(颜色2) if isinstance(颜色2, str) else 颜色2

        # 转换为RGB
        rgb1 = 颜色.十六进制转RGB(hex1)
        rgb2 = 颜色.十六进制转RGB(hex2)

        # 颜色相加（各分量相加并限制在0-255范围内）
        r = min(rgb1[0] + rgb2[0], 255)
        g = min(rgb1[1] + rgb2[1], 255)
        b = min(rgb1[2] + rgb2[2], 255)

        # 处理透明度（如果有）
        if 保留透明度 and len(rgb1) == 4 and len(rgb2) == 4:
            a = min(rgb1[3] + rgb2[3], 255)
            return 颜色.RGB转十六进制((r, g, b, a))

        return 颜色.RGB转十六进制((r, g, b))

    @staticmethod
    def 颜色叠加(底层颜色, 顶层颜色, 透明度=0.5):
        """
        按透明度叠加两种颜色

        参数:
            底层颜色: 可以是16进制颜色值或英文颜色名
            顶层颜色: 可以是16进制颜色值或英文颜色名
            透明度: 顶层颜色的透明度(0.0-1.0)

        返回:
            叠加后的16进制颜色值
        """
        # 转换颜色为16进制
        hex1 = 颜色.转16进制颜色(底层颜色) if isinstance(底层颜色, str) else 底层颜色
        hex2 = 颜色.转16进制颜色(顶层颜色) if isinstance(顶层颜色, str) else 顶层颜色

        # 转换为RGB
        rgb1 = 颜色.十六进制转RGB(hex1)
        rgb2 = 颜色.十六进制转RGB(hex2)

        # 按透明度叠加
        alpha = min(max(透明度, 0.0), 1.0)
        r = int(rgb1[0] * (1 - alpha) + rgb2[0] * alpha)
        g = int(rgb1[1] * (1 - alpha) + rgb2[1] * alpha)
        b = int(rgb1[2] * (1 - alpha) + rgb2[2] * alpha)

        return 颜色.RGB转十六进制((r, g, b))

    @staticmethod
    def 多色叠加(颜色列表, 透明度列表=None):
        """
        按顺序叠加多个颜色

        参数:
            颜色列表: 包含多个颜色的列表，可以是16进制颜色值或英文颜色名
            透明度列表: 对应每个颜色的透明度列表(0.0-1.0)，默认全为1.0

        返回:
            叠加后的16进制颜色值
        """
        if not 颜色列表:
            return None

        # 处理单个颜色的情况
        if len(颜色列表) == 1:
            return 颜色.转16进制颜色(颜色列表[0]) if isinstance(颜色列表[0], str) else 颜色列表[0]

        # 初始化透明度列表
        if 透明度列表 is None:
            透明度列表 = [0.5] * len(颜色列表)
        else:
            # 确保透明度列表长度与颜色列表一致
            透明度列表 = 透明度列表 + [1.0] * (len(颜色列表) - len(透明度列表))
            透明度列表 = 透明度列表[:len(颜色列表)]  # 截断到颜色列表长度

        # 从底层颜色开始，依次叠加后续颜色
        result = 颜色列表[0]

        for i in range(1, len(颜色列表)):
            result = 颜色.颜色叠加(result, 颜色列表[i], 透明度列表[i])

        return result

    @staticmethod
    def 颜色变深(颜色值, 加深程度=0.08):
        # from 神笔码靓.神笔库.定义集 import 颜色
        if not str(颜色值).startswith("#"):
            颜色值 = 颜色.转16进制颜色(颜色值)
        # 在这里用 python 代码实现, 将 颜色值 格式为: #D75D72 进行颜色加深
        # 将十六进制颜色值转换为 RGB
        r = int(颜色值[1:3], 16)
        g = int(颜色值[3:5], 16)
        b = int(颜色值[5:7], 16)

        # 根据加深程度调整颜色
        r = max(0, int(r * (1 - 加深程度)))
        g = max(0, int(g * (1 - 加深程度)))
        b = max(0, int(b * (1 - 加深程度)))

        # 将 RGB 值转换回十六进制格式
        return f'#{r:02X}{g:02X}{b:02X}'

    @staticmethod
    def 颜色变浅(颜色值, 变浅程度=0.08):
        # from 神笔码靓.神笔库.定义集 import 颜色
        if not str(颜色值).startswith("#"):
            颜色值 = 颜色.转16进制颜色(颜色值)
        # 将十六进制颜色值转换为 RGB
        r = int(颜色值[1:3], 16)
        g = int(颜色值[3:5], 16)
        b = int(颜色值[5:7], 16)
        # 根据变浅程度调整颜色
        r = min(255, int(r / (1 - 变浅程度)))
        g = min(255, int(g / (1 - 变浅程度)))
        b = min(255, int(b / (1 - 变浅程度)))
        # 将 RGB 值转换回十六进制格式
        return f'#{r:02X}{g:02X}{b:02X}'


class 粉笔色:
    白色 = 颜色.白色
    红色 = "#F98A88"
    桃红 = "#FFABD2"
    黄色 = "#FFF000"  # "#FFE779"
    草绿 = "#D3E6A7"
    绿色 = "#BDEBD0"
    青绿 = "#408A76"
    浅蓝 = "#ADD2FA"
    蓝色 = "#A8CCF5"
    深蓝 = "#66C5FB"
    橙色 = "#FDC799"
    粉色 = "#FCB5DF"
    紫色 = "#E4B6FF"

    @staticmethod
    def 粉笔色列表():
        return [粉笔色.白色, 粉笔色.红色, 粉笔色.桃红, 粉笔色.黄色, 粉笔色.草绿, 粉笔色.绿色, 粉笔色.青绿,
                粉笔色.浅蓝, 粉笔色.蓝色, 粉笔色.深蓝, 粉笔色.橙色, 粉笔色.粉色, 粉笔色.紫色]


class 颜色方案:
    # 彩虹色
    彩虹色1 = [颜色.红色, 颜色.橙色, 颜色.黄色, 颜色.绿色, 颜色.青色, 颜色.蓝色, 颜色.紫色]
    彩虹色2 = ["#FF0000", "#FF6D00", "#FFFF00", "#59FB46", "#59D5EF", "#5E7EF7", "#B359F6"]
    # 1. 经典三原色
    经典三原色 = ["#FF0000", "#00FF00", "#0000FF"]
    # 2. 温暖大地色
    温暖大地色 = ["#D2691E", "#8B4513", "#A0522D", "#F4A460", "#DEB887"]
    # 3. 清新天空色
    清新天空色 = ["#87CEEB", "#4682B4", "#B0E0E6", "#E0FFFF", "#AFEEEE"]
    # 4. 浪漫粉紫色系
    浪漫粉紫色系 = ["#FFC0CB", "#FF69B4", "#DA70D6", "#9370DB", "#8A2BE2", "#4B0082"]
    # 5. 深邃海洋蓝
    深邃海洋蓝 = ["#000080", "#0000CD", "#1E90FF", "#4169E1", "#6495ED"]
    # 6. 金秋丰收色
    金秋丰收色 = ["#FFD700", "#DAA520", "#B8860B", "#CD853F", "#FFA500"]
    # 7. 森林之绿
    森林之绿 = ["#228B22", "#32CD32", "#006400", "#008000", "#2E8B57", "#3CB371"]
    # 8. 活力橙黄色系
    活力橙黄色系 = ["#FFA07A", "#FF7F50", "#FF6347", "#FF4500", "#FFDAB9", "#FFFF00"]
    # 9. 优雅黑白灰
    优雅黑白灰 = ["#FFFFFF", "#000000", "#D3D3D3", "#C0C0C0", "#A9A9A9"]
    # 10. 神秘夜空色
    神秘夜空色 = ["#000000", "#191970", "#4682B4", "#6495ED", "#87CEFA"]
    # 11. 梦幻彩虹色
    梦幻彩虹色 = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
    # 12. 复古棕色系
    复古棕色系 = ["#8B4513", "#A0522D", "#BC8F8F", "#D2691E", "#F4A460", "#FFA07A"]
    # 13. 宁静湖蓝色
    宁静湖蓝色 = ["#00FFFF", "#40E0D0", "#7FFFD4", "#48D1CC", "#00CED1"]
    # 14. 春日樱花色
    春日樱花色 = ["#FFB6C1", "#FFC0CB", "#FFD1DC", "#FFE1E6", "#FFF5EE"]
    # 15. 沙漠驼色系
    沙漠驼色系 = ["#F5DEB3", "#FFDEAD", "#D2B48C", "#DEB887", "#CD853F", "#B8860B"]
    # 16. 时尚酷黑色系
    时尚酷黑色系 = ["#000000", "#2F4F4F", "#483D8B", "#696969", "#808080"]
    # 17. 青花瓷色系
    青花瓷色系 = ["#000080", "#0000CD", "#4169E1", "#6495ED", "#87CEEB", "#B0E0E6", "#FFFFFF"]
    # 18. 田园草绿色
    田园草绿色 = ["#98FB98", "#90EE90", "#7CFC00", "#32CD32", "#228B22"]
    # 19. 霓虹荧光色
    霓虹荧光色 = ["#FF00FF", "#FF6D00", "#00FF00", "#00FFFF", "#8B0082"]
    # 20. 冰雪冷白色
    冰雪冷白色 = ["#F0FFFF", "#E0FFFF", "#AFEEEE", "#DCDCDC", "#C0C0C0"]
    # 多彩颜色
    # 1. 彩虹梦境
    彩虹梦境 = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]
    # 2. 翠韵山林
    翠韵山林 = ["#006400", "#228B22", "#32CD32", "#66CD00", "#7CFC00", "#8FBC8F", "#9ACD32"]
    # 3. 暖调黄昏
    暖调黄昏 = ["#FFA07A", "#FF7F50", "#FF6347", "#FF4500", "#DAA520", "#B8860B", "#CD853F"]
    # 4. 粉樱甜香
    粉樱甜香 = ["#FFB6C1", "#FFC0CB", "#FFD1DC", "#FFE1E6", "#FFEFD5", "#FFF5EE", "#FFFFFF"]
    # 5. 幽蓝深境
    幽蓝深境 = ["#000080", "#0000CD", "#1E90FF", "#4169E1", "#6495ED", "#87CEEB", "#B0E0E6"]
    # 6. 复古棕雅
    复古棕雅 = ["#8B4513", "#A0522D", "#BC8F8F", "#D2691E", "#F4A460", "#FFA07A", "#FFDAB9"]
    # 7. 活力盛绽
    活力盛绽 = ["#FF4500", "#FF6347", "#FF7F50", "#FFA07A", "#FFB6C1", "#FFDAB9", "#FFFF00"]
    # 8. 碧海情天
    碧海情天 = ["#00FFFF", "#40E0D0", "#66CDAA", "#87CEEB", "#98FB98", "#B0E0E6", "#E0FFFF"]
    # 9. 紫韵幽梦
    紫韵幽梦 = ["#8A2BE2", "#9370DB", "#C71585", "#FF1493", "#FF69B4", "#FFC0CB", "#FFFFFF"]
    # 10. 幻彩霓虹
    幻彩霓虹 = ["#FF00FF", "#FF6D00", "#00FF00", "#00FFFF", "#8B0082", "#FF0000", "#0000FF"]
    # 11. 金秋华彩
    金秋华彩 = ["#DAA520", "#FFD700", "#FFA500", "#FF8C00", "#FF7F50", "#FF6347", "#FF4500"]
    # 12. 静谧湖蓝
    静谧湖蓝 = ["#00FFFF", "#AFEEEE", "#7FFFD4", "#40E0D0", "#48D1CC", "#00CED1", "#008080"]
    # 13. 时尚酷灰
    时尚酷灰 = ["#D3D3D3", "#C0C0C0", "#A9A9A9", "#808080", "#696969", "#555555", "#404040"]
    # 14. 童话绮丽
    童话绮丽 = ["#FFE4E1", "#FFB6C1", "#FF69B4", "#FF1493", "#C71585", "#9370DB", "#8A2BE2"]
    # 15. 大漠孤烟
    大漠孤烟 = ["#F5DEB3", "#FFDEAD", "#D2B48C", "#DEB887", "#CD853F", "#B8860B", "#8B4513"]
    # 16. 星夜流光
    星夜流光 = ["#000000", "#191970", "#2F4F4F", "#4682B4", "#6495ED", "#87CEFA", "#B0C4DE"]
    # 17. 青花雅韵
    青花雅韵 = ["#000080", "#0000CD", "#4169E1", "#6495ED", "#87CEEB", "#B0E0E6", "#FFFFFF"]
    # 18. 田园牧歌
    田园牧歌 = ["#98FB98", "#90EE90", "#7CFC00", "#32CD32", "#228B22", "#00FF00", "#008000"]
    # 19. 冰原雪韵
    冰原雪韵 = ["#F0FFFF", "#E0FFFF", "#AFEEEE", "#7FFFD4", "#40E0D0", "#48D1CC", "#00CED1"]
    # 20. 神秘雨林
    神秘雨林 = ["#006400", "#008000", "#2E8B57", "#3CB371", "#556B2F", "#6B8E23", "#808000"]

    @staticmethod
    def 循环颜色集(索引, 颜色集: list):
        return 颜色集[索引 % len(颜色集)]


class 系统字体:
    默认 = None
    黑体 = "SimHei"
    隶书 = "LiSu"
    宋体 = "SimSun"
    幼圆 = "YouYuan"
    楷体 = "KaiTi"
    微软雅黑 = "Microsoft YaHei"
    微软雅黑轻体 = "Microsoft YaHei Light"
    新宋体 = "NSimSun"
    华文细黑 = "STXihei"
    华文中宋 = "STZhongsong"
    华文楷体 = "STKaiti"
    华文仿宋 = "STFangsong"
    华文琥珀 = "STHupo"
    仿宋 = "FangSong"
    华文行楷 = "STXingkai"
    华文新魏 = "STXinwei"
    等线 = "DengXian"
    方正舒体 = "FZShuTi"
    方正姚体 = "FZYaoTi"

    Arial = "Arial"
    ArialBlack = "Arial Black"
    BernardMTCondensed = "Bernard MT Condensed"
    BodoniMTBlack = "Bodoni MT Black"
    Broadway = "Broadway"
    Bahnschrift = "Bahnschrift"
    BebasNeue = "Bebas Neue"
    Calibri = "Calibri"
    Cambria = "Cambria"
    CourierNew = "Courier New"
    ComicSansMS = "Comic Sans MS"
    Consolas = "Consolas"
    Georgia = "Georgia"
    Montserrat = "Montserrat"
    Roboto = "Roboto"
    SegoeUI = "Segoe UI"
    TimesNewRoman = "Times New Roman"
    Tahoma = "Tahoma"
    TrebuchetMS = "Trebuchet MS"
    Verdana = "Verdana"
    WideLatin = "Wide Latin"

    @staticmethod
    def 是否系统字体(字体名):
        return 是否系统字体(字体名)
        # for item in 系统字体.__dict__:
        #     if str(item).startswith("__"):
        #         continue
        #     font_name = getattr(系统字体, item)
        #     if 字体名 == font_name:
        #         return True
        #     # print(item)
        # return False

    @staticmethod
    def 中文名(字体名):
        for item in 系统字体.__dict__:
            if str(item).startswith("__"):
                continue
            font_name = getattr(系统字体, item)
            if 字体名 == font_name:
                return item
            # print(item)
        return 字体名


class 元素矢量效果:
    """
    none：默认值，表示不应用任何矢量效果。
non-scaling-stroke：保持笔触宽度不变，不受元素缩放的影响。这是解决SVG缩放时边框宽度变化问题的利器。
non-scaling-size：保持元素及其后代使用的用户坐标系的比例不变。
non-rotation：抑制元素及其后代用户坐标系的旋转和倾斜。
fixed-position：固定元素及其后代用户坐标系的位置。
    """
    无 = "none"
    边宽非缩放 = "non-scaling-stroke"
    大小非缩放 = "non-scaling-size"
    非旋转 = "non-rotation"
    固定位置 = "fixed-position"


class 屏幕分辨率:
    @staticmethod
    def 手机():
        """
        序号	分辨率	也被称为	常见机型
 720 x 1280	HD	    这种分辨率多用于个别入门级和中档手机上
 720 x 1440		    这是一种新兴的分辨率，目前许多入门级和中档手机使用
 750 x 1334		    这是iPhone 6、6s、7和8的常见分辨率
1080 x 1920	Full HD	这是目前最常见的分辨率，大多数中高档手机都采用这种分辨率
1125 x 2436		    这是iPhone X的分辨率，也是目前最高的iPhone屏幕分辨率
1440 x 2560	Quad HD 或者2K这种高分辨率多被用于高端手机上，如三星Galaxy S8和Note 8等机型
        :return:
        """
        return 1080, 2376

    @staticmethod
    def 华为畅享60X():
        return 1080, 2376

    @staticmethod
    def 华为畅享70Pro():
        return 1080, 2388  # FHD

    @staticmethod
    def 华为Nova12():
        return 1084, 2412  # FHD

    @staticmethod
    def 华为Mate50():
        return 1224, 2700  # FHD

    @staticmethod
    def 华为Pura70():
        return 1256, 2760

    @staticmethod
    def 我的手机():
        return 1080, 2376
        # return 1080, 2250


class 纸张大小:
    """
    办公常用为 A4 纸，其他纸张大小自行补充
    """
    # A4打印调整
    SCALE_FACTOR = 3.68

    @staticmethod
    def A3_横向(纸张数=1):
        # # 420mm×297mm
        return 420 * 纸张大小.SCALE_FACTOR, 297 * 纸张大小.SCALE_FACTOR * 纸张数

    @staticmethod
    def A3_纵向(纸张数=1):
        return 297 * 纸张大小.SCALE_FACTOR, 420 * 纸张大小.SCALE_FACTOR * 纸张数

    @staticmethod
    def A4_横向(纸张数=1):
        # A4规格为21*29.7cm（210mm×297mm）
        return 297 * 纸张大小.SCALE_FACTOR, 210 * 纸张大小.SCALE_FACTOR * 纸张数

    @staticmethod
    def A4_纵向(纸张数=1):
        return 210 * 纸张大小.SCALE_FACTOR, 297 * 纸张大小.SCALE_FACTOR * 纸张数

    @staticmethod
    def A5_横向(纸张数=1):
        # A5规格为 21*14.8cm（210mm×148mm）
        return 210 * 纸张大小.SCALE_FACTOR, 148 * 纸张大小.SCALE_FACTOR * 纸张数

    @staticmethod
    def A5_纵向(纸张数=1):
        return 148 * 纸张大小.SCALE_FACTOR, 210 * 纸张大小.SCALE_FACTOR * 纸张数

class 纸张方向:
    自动识别 = None
    横向 = True
    纵向 = False


#  `text_anchor`  参数用于控制水平对齐方式，可选的参数值有：
# -  `"start"` ：左对齐 在神笔绘图板写字
# -  `"middle"` ：居中对齐
# -  `"end"` ：右对齐
class 文字水平基线对齐:
    起始点对齐 = "start"
    中点对齐 = "middle"
    结束点对齐 = "end"


class 箭头样式:
    实心 = "实心"
    空心 = "空心"
    倒钩 = "倒钩"


class 描边线连接样式:
    #  arcs | bevel |miter | miter-clip | round
    # 弧形连接（此值在SVG 1.2规范中被引入，但未在所有实现中广泛支持）
    # 弧形连接 = "arcs"
    #  miter（默认值）：线段在交点处形成尖角，直到达到最大长度或角度限制。
    尖角连接 = "miter"
    # 尖角剪切连接（超过miterlimit的部分将被剪切）
    # 尖角剪切连接 = "miter-clip"
    #  段在交点处形成一个圆角。
    圆角连接 = "round"
    #  线段在交点处形成一个斜角。
    斜角连接 = "bevel"


class 描边线端样式:
    # butt（默认值）：线条末端被截断，形成一个直角。  butt | round | square | inherit
    直角 = "butt"
    # round：线条末端被圆形化，形成一个半圆。
    半圆 = "round"
    # square：线条末端被扩展成一个正方形。
    正方形 = "square"


class 图像渲染设置:
    # image-rendering
    自动 = "auto"
    平滑 = "smooth"
    高质量 = "high-quality"
    清晰边缘 = "crisp-edges"
    像素化 = "pixelated"
    优化质量 = "optimizeQuality"
    webkit优化对比度 = "-webkit-optimize-contrast"


class 定位点类型:
    十字 = "十字"
    空圆 = "空圆"
    实圆 = "实圆"
    空方 = "空方"
    实方 = "实方"


#  `alignment_baseline`
# auto | baseline | before-edge | text-before-edge | middle | central | after-edge | text-after-edge
# | ideographic | alphabetic | hanging | mathematical | inherit
class 文字垂直基线对齐:
    底线对齐 = "text-after-edge"
    中线对齐 = "middle"
    顶线对齐 = "text-before-edge"


是 = True
否 = False
空 = None
无 = None
开 = True
关 = False

全角空格 = "　"


class 网格重复类型:
    普通网格 = 0
    砖型交错 = 1
    竖砖交错 = 2


class 空间坐标系单位:
    用户空间 = "userSpaceOnUse"
    物体边界 = "objectBoundingBox"


@dataclass
class 纸张设置:
    上页边距: [str, float, int] = 0
    下页边距: [str, float, int] = 0
    左页边距: [str, float, int] = 0
    右页边距: [str, float, int] = 0
    页面方向: bool = 纸张方向.自动识别
    页面尺寸规格: str = "A4"
    页面缩放: float = 1.0


class PDF生成方式:
    自动 = 0
    谷歌浏览器 = 1
    cairosvg = 2


class PNG生成方式:
    自动 = 0
    cairosvg = 1
    谷歌浏览器 = 2
    # StirlingPDF = 2


class DOCX生成方式:
    自动 = 0
    pdf2docx = 1
    aspose_words = 2


class 单例模式:
    """
    单例模式类
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(单例模式, cls).__new__(cls)
        return cls._instance


if __name__ == '__main__':
    # print(纸张大小.A1纸_横向())
    print(颜色.RGB("灰色"), 颜色.英文名("黑色"))
