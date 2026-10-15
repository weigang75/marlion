# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import re
import shutil
import os
import math
import importlib
import importlib.util
import inspect
import gc
import sys
import random
import hashlib
from 神笔码靓.神笔库.中文编程定义 import *


def 入参名称获取(func):
    def wrapper(*args, **kwargs):
        # ========== 新增：获取各级调用函数名 ==========
        # 当前帧：wrapper自身
        cur_frame = inspect.currentframe()

        # 1级上层：调用wrapper的函数（直接调用被装饰函数的函数）
        frame_1 = cur_frame.f_back
        caller_1_name = frame_1.f_code.co_name if frame_1 else "顶层调用(主程序)"

        # 2级上层：调用【1级上层函数】的外层函数（上上级）
        frame_2 = frame_1.f_back if frame_1 else None
        caller_2_name = frame_2.f_code.co_name if frame_2 else "顶层调用(主程序)"

        # 存到全局方便外部读取
        sys.modules["__main__"].一级调用函数名 = caller_1_name
        sys.modules["__main__"].二级调用函数名 = caller_2_name
        # ==========================================

        # 原有：获取入参变量名逻辑不变
        frame = frame_1  # 原逻辑使用直接调用帧，不用改动
        local_vars = frame.f_locals

        sig = inspect.signature(func)
        bound_arguments = sig.bind(*args, **kwargs).arguments

        arg_name_mapping = {}
        for param_name, param_value in bound_arguments.items():
            for var_name, var_value in local_vars.items():
                if var_value is param_value:
                    arg_name_mapping[param_name] = var_name
                    break

        sys.modules["__main__"].获取的函数入参名称 = arg_name_mapping
        return func(*args, **kwargs)

    return wrapper


def 入参名称字典():
    if "获取的函数入参名称" in sys.modules["__main__"].__dict__:
        return sys.modules["__main__"].获取的函数入参名称
    return None


# 封装读取调用函数名的工具函数，方便外部调用
def 获取调用层级函数名(层级=1):
    """
    :param 层级: 1=上一级，2=上上级
    :return: 函数名字符串
    """
    mod = sys.modules["__main__"]
    if 层级 == 1 and hasattr(mod, "一级调用函数名"):
        return mod.一级调用函数名
    elif 层级 == 2 and hasattr(mod, "二级调用函数名"):
        return mod.二级调用函数名
    return None


def 获取不带扩展名的文件名(文件路径名):
    if 为空(文件路径名):
        return ""
    name, ext_name = 分解文件名(获取文件名(文件路径名))
    return name


# def 搜索目录(目录名):
#     搜索路径 = [".", "..", "../.."]
#     for path in 搜索路径:
#         full_path = os.path.join(path, 目录名)
#         if os.path.exists(full_path):
#             return os.path.abspath(full_path)
#
#     return None

字体宽高字典 = {}


def 获取文字的宽高(字体, 字体大小, 文字):
    global 字体宽高字典
    # try:
    #     # for Python2
    #     import Tkinter
    # except ImportError:
    #     # for Python3
    import tkinter as Tkinter
    if 为空(字体):
        from 神笔码靓.神笔库 import 字体文件目录
        字体 = 字体文件目录("安卓字体.ttf")

    key = f"{字体}_{字体大小}"
    font_size = int(round(字体大小, 0))
    size_scale = 字体大小 / font_size

    if key in 字体宽高字典.keys():
        font = 字体宽高字典[key]
    else:
        import tkinter.font as tkFont
        # initialize Tk so that font metrics will work
        tk_root = Tkinter.Tk()
        font = None
        font = tkFont.Font(family=字体, size=font_size)
        assert font is not None
        字体宽高字典[key] = font

    (w, h) = (font.measure(文字), font.metrics('linespace'))
    return (w * size_scale, h * size_scale)


def 计算耗时(func):
    # import asyncio
    import time
    from asyncio.coroutines import iscoroutinefunction
    def fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'{func.__name__} 耗时：{time.perf_counter() - t:.2f} s')
        return result

    async def func_async(*args, **kwargs):
        t = time.perf_counter()
        result = await func(*args, **kwargs)
        print(f'{func.__name__} 耗时：{time.perf_counter() - t:.2f} s')
        return result

    if iscoroutinefunction(func):
        return func_async
    else:
        return fun


def 搜索目录(目录名, 文件名=None):
    搜索路径 = [".", "..", "../..", "../../.."]
    for path in 搜索路径:
        full_path = os.path.join(path, 目录名)
        if os.path.exists(full_path):
            if 文件名 is None:
                return os.path.abspath(full_path)
            else:
                return os.path.abspath(os.path.join(full_path, 文件名))

    return None


def 安全创建目录(文件名):
    dir_name = os.path.dirname(文件名)
    if 为空(dir_name):
        return
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def 安全复制文件(来源文件, 目标文件):
    try:
        shutil.copy2(来源文件, 目标文件)
        # print("文件复制成功")
    except FileNotFoundError:
        print("找不到指定的文件")
    except IsADirectoryError:
        print("目标文件是一个目录，而不是一个文件")
    except PermissionError:
        print("没有权限访问文件或目录")
    except Exception as e:
        print("发生错误：", e)


def 资源库目录(文件名=None):
    return 搜索目录(目录名="资源库", 文件名=文件名)


def 码靓库目录(文件名=None):
    return 搜索目录(目录名="码靓库", 文件名=文件名)


def 神笔库目录(文件名=None):
    return 搜索目录(目录名="神笔库", 文件名=文件名)


def 神笔模板目录(文件名=None):
    return 搜索目录(目录名="神笔模板", 文件名=文件名)


def 作品输出目录(作品文件名=None, 子目录名=None):
    if 子目录名 is not None:
        return 搜索目录(目录名="输出文件", 文件名=子目录名)
    if 作品文件名 is not None:
        作品文件名_lower = str(作品文件名).lower()
        if not any([作品文件名_lower.endswith(i) for i in [".svg", ".pdf", ".png"]]):
            作品文件名 = 作品文件名 + ".svg"
    return 搜索目录(目录名="输出文件", 文件名=作品文件名)


def 字体文件目录(文件名=None):
    return 搜索目录(目录名="字体", 文件名=文件名)


def 成果馆目录(文件名=None):
    return 搜索目录(目录名="成果馆", 文件名=文件名)


def 获取字符串哈希值(字符串):
    # 创建一个sha256哈希对象
    hash_object = hashlib.sha256()
    # 更新哈希对象以包含字符串的字节
    hash_object.update(字符串.encode('utf-8'))
    # 获取十六进制的哈希值
    hash_hex = hash_object.hexdigest()
    return hash_hex


def 获取字符串md5(字符串):
    # 创建一个md5哈希对象
    hash_object = hashlib.md5()
    # 更新哈希对象以包含字符串的字节
    hash_object.update(字符串.encode('utf-8'))
    # 获取十六进制的哈希值
    hash_hex = hash_object.hexdigest()
    return hash_hex


def 是否系统字体(字体名):
    import tkinter
    import tkinter.font as tkfont
    # root = tkinter.Tk()
    # families = tkfont.families(root)
    # print(families)
    # for family in families:
    #     print(family)
    #     with open('fonts.txt', 'a', encoding='utf-8') as f:
    #         f.write(family)
    #         f.write('\n')
    root = tkinter.Tk()
    families = tkfont.families(root)
    return 字体名 in families

    # if __name__ == '__main__':
    # print(是否为数值("12.34"), 是否为数值("12.3.4"), 是否为数值("12.34E"))

    # import tkinter.font


def 文件存在(文件路径):
    if not os.path.isabs(文件路径):
        文件路径 = os.path.abspath(文件路径)
    return os.path.exists(文件路径)


def 文件不存在(文件路径):
    return not 文件存在(文件路径)


def 报错(错误消息):
    raise Exception(错误消息)


def is_package_installed(package_name):
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def 是否安装svgwrite():
    # 使用示例
    package_name = "svgwrite"
    return is_package_installed(package_name)


def 是否安装cairosvg():
    # 使用示例
    package_name = "cairosvg"
    return is_package_installed(package_name)


# def run_in_jupyter():
#     try:
#         # 尝试获取IPython的交互式shell实例
#         shell = get_ipython().__class__.__name__
#         # print(shell)
#         if "InteractiveShell" in shell:
#             return True
#     except NameError:
#         # get_ipython()没有定义，则不在Jupyter Notebook中
#         return False
#
#     return True

def 获取字体的文件路径(字体名: str):
    root_path = 字体文件目录()
    for fd in os.listdir(root_path):
        path = os.path.join(root_path, fd)
        if os.path.isdir(path):
            continue
        if fd.lower() == 字体名.lower():
            return path
        name_split_text = os.path.splitext(fd)
        # Eot、otf、fon、font、ttf、ttc、woff
        if name_split_text[1].lower() not in [".ttf", ".ttc", ".eot", ".otf", ".fon", ".font", ".woff"]:
            continue

        if name_split_text[0].lower() == 字体名.lower():
            return path

    # import matplotlib.font_manager as fm
    # fonts = fm.findSystemFonts()
    # for font in fonts:

    return None


def 获取GB2312汉字集():
    汉字集 = []
    for i in range(0xB0, 0xF8):
        for j in range(0xA1, 0xFF):
            code = i * 256 + j
            try:
                char = code.to_bytes(2, 'big').decode('gb2312')
            except UnicodeDecodeError:
                continue
            汉字集.append(char)
    return 汉字集


ttfont_dict = {}


def 检查字是否在字体文件中(char: str, fontfile: str) -> bool:
    """判断字符是否在字体里

    Args:
        char (str): 单字符文本
        fontfile (str): 字体文件

    Returns:
        bool: 是否在字体里
    """
    # pip install -i http://mirrors.aliyun.com/pypi/simple fonttools (4.25.0)
    code = char.encode("unicode-escape").decode()
    if "\\u" in code:
        code = "uni" + code[2:].upper()
    if fontfile not in ttfont_dict.keys():
        from fontTools.ttLib import TTFont
        font = TTFont(fontfile)
        ttfont_dict[fontfile] = font
    else:
        font = ttfont_dict[fontfile]

    glyf = font["glyf"]
    if not glyf.has_key(code):
        return False
    coord = glyf[code].getCoordinates(glyf)
    return len(coord) > 0


def 批量修改文件名(指定目录, 修改后文件名="${序号}", 强制扩展名=None, 序号开始=1, 跳过规则=None):
    for fd in os.listdir(指定目录):
        if os.path.isdir(fd):
            continue

        if 跳过规则 is not None:
            if isinstance(跳过规则, str):
                if 跳过规则 in fd:
                    continue
        _, 原始扩展名 = os.path.splitext(fd)
        新文件名 = 修改后文件名.replace("${序号}", str(序号开始))
        序号开始 += 1
        if 强制扩展名:
            新文件名 = 新文件名 + "." + 强制扩展名
        else:
            新文件名 = 新文件名 + "." + 原始扩展名

        当前文件路径 = os.path.join(指定目录, fd)
        修改后文件路径 = os.path.join(指定目录, 新文件名)

        os.rename(src=当前文件路径, dst=修改后文件路径)


def 计算旋转后的坐标(旋转前原始坐标, 旋转中心点坐标, 旋转角度):
    """
    计算点 A 围绕点 O 旋转角度 K 后的新坐标

    :param 旋转前原始坐标: 点 A 的坐标 (x_A, y_A)
    :param 旋转中心点坐标: 点 O 的坐标 (x_O, y_O)
    :param K: 旋转角度（弧度）
    :return: 旋转后的新坐标 (x_A', y_A')
    """
    x_A, y_A = 旋转前原始坐标
    x_O, y_O = 旋转中心点坐标
    K = 旋转角度 * math.pi / 180
    # 计算旋转后的坐标
    x_A_new = x_O + (x_A - x_O) * math.cos(K) - (y_A - y_O) * math.sin(K)
    y_A_new = y_O + (x_A - x_O) * math.sin(K) + (y_A - y_O) * math.cos(K)

    return x_A_new, y_A_new


def 获取上下文实例对象(实例类型):
    frame = inspect.currentframe().f_back
    while frame:
        if 'self' in frame.f_locals:
            instance = frame.f_locals['self']
            if isinstance(instance, 实例类型):
                return instance
        frame = frame.f_back
    return None


def 获取文件2相对文件1的路径(文件1, 文件2):
    # import sys
    # os.path.relpath(图片文件,sys.argv[0])
    svg_dir = os.path.dirname(文件1)
    relative_path = os.path.relpath(文件2, svg_dir)
    return relative_path


def 打印红色消息(消息):
    print(f"\033[91m{消息}\033[0m")


def 打印红色消息(消息):
    print(f"\033[91m{消息}\033[0m")


def 打印绿色消息(消息):
    print(f"\033[92m{消息}\033[0m")


def 打印黄色消息(消息):
    print(f"\033[93m{消息}\033[0m")


def 打印蓝色消息(消息):
    print(f"\033[94m{消息}\033[0m")


def 打印紫色消息(消息):
    print(f"\033[95m{消息}\033[0m")


def 打印青色消息(消息):
    print(f"\033[96m{消息}\033[0m")


def 打印白色消息(消息):
    print(f"\033[97m{消息}\033[0m")


if __name__ == '__main__':
    打印红色消息("这是红色消息")
    打印绿色消息("这是绿色消息")
    打印黄色消息("这是黄色消息")
    打印蓝色消息("这是蓝色消息")
    打印紫色消息("这是紫色消息")
    打印青色消息("这是青色消息")
    打印白色消息("这是白色消息")

if __name__ == '__main2__':
    批量修改文件名(r"G:\works\gitcode\code_painter\资源库\图片\手机壁纸",
            修改后文件名="手机壁纸${序号}", 强制扩展名="jpg", 序号开始=1, 跳过规则=None)

if __name__ == '__main1__':
    # from 神笔码靓.神笔库 import *
    # print(是否系统字体("思雨手写行楷"))

    # region  ------ 字是否在字体文件中 -----------
    #
    甲骨文字体文件 = 字体文件目录("甲骨文.ttf")
    小篆体字体文件 = 字体文件目录("峄山碑篆体.ttf")
    字不在字体文件中 = []
    for 字 in 获取GB2312汉字集():
        if not 检查字是否在字体文件中(字, 甲骨文字体文件):
            字不在字体文件中.append(字)
    for 字 in 获取GB2312汉字集():
        if not 检查字是否在字体文件中(字, 小篆体字体文件):
            if 字 not in 字不在字体文件中:
                字不在字体文件中.append(字)

    print(字不在字体文件中)
    # endregion ------ 字是否在字体文件中 -----------

    print(获取字体的文件路径("甲骨文"))
