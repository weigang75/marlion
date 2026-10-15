# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-06
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os

from 神笔码靓.码靓库.共用.诗经集 import 三字经
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import codecs


def 获取所有GBK中文字符列表():
    gbk_chars = []

    # GBK编码的范围是从0x00到0xFF和从0xA1到0xFE
    for i in range(256):  # 0x00到0xFF
        try:
            char = codecs.decode(bytes([i]), 'gbk')
            gbk_chars.append(char)
        except UnicodeDecodeError:
            continue

    for i in range(0xA1, 0xFF):  # 0xA1到0xFE
        for j in range(0xA1, 0xFF):  # 0xA1到0xFE
            try:
                char = codecs.decode(bytes([i, j]), 'gbk')
                gbk_chars.append(char)
            except UnicodeDecodeError:
                continue

    return list(set(gbk_chars))  # 去重并返回


# 定义计算字符轮廓面积的函数
def 计算字符轮廓面积(character, font_path='msyh.ttc', font_size=100):
    # 创建一个白色背景的图像
    img = Image.new('L', (font_size, font_size), 255)
    draw = ImageDraw.Draw(img)

    # 使用指定的字体绘制字符
    font = ImageFont.truetype(font_path, font_size)
    draw.text((0, 0), character, fill=0, font=font)

    # 将图像转换为数组并计算轮廓面积
    img_array = np.array(img)
    area = np.sum(img_array == 0)  # 计算黑色像素的数量
    return area


def 是否为中文字符(char):
    # 获取字符的Unicode码点
    code_point = ord(char)
    # 判断是否在中文字符的Unicode范围内
    return (0x4E00 <= code_point <= 0x9FFF) or \
           (0x3400 <= code_point <= 0x4DBF) or \
           (0x20000 <= code_point <= 0x2A6DF) or \
           (0x2A700 <= code_point <= 0x2B73F) or \
           (0x2B740 <= code_point <= 0x2B81F) or \
           (0x2B820 <= code_point <= 0x2CEAF) or \
           (0xF900 <= code_point <= 0xFAFF) or \
           (0x2E80 <= code_point <= 0x2EFF)


def 获取字符面积排序列表():
    所有GBK中文字符列表 = 获取所有GBK中文字符列表()
    print("所有GBK中文字符列表 =", 所有GBK中文字符列表)

    所有GBK中文字符列表 = [(字符, 计算字符轮廓面积(字符)) for 字符 in 所有GBK中文字符列表]

    # 根据面积排序
    字符面积排序列表 = sorted(所有GBK中文字符列表, key=lambda x: x[1], reverse=False)
    print("字符面积排序列表 =", 字符面积排序列表)

    字符面积排序字典 = {}
    for 字符, 面积 in 字符面积排序列表:
        字符面积排序字典[字符] = round(面积 / 3272, 2)
    print("字符面积排序字典 =", 字符面积排序字典)


# 获取字符面积排序列表()

def 获取十个密度从低到高的字符列表():
    中文列表 = {"0.0": " "}  # [{"}('\u3000', ),]
    index = 0
    last_no_cn_char = ""
    from 神笔码靓.神笔库.字符串列表 import 字符面积占比排序列表
    for w, r in 字符面积占比排序列表:
        num = round(index / 10, 1)
        if str(num) in 中文列表:
            index += 1
        elif num == r:
            if 是否为中文字符(w):
                中文列表[str(r)] = w
                index += 1
            else:
                last_no_cn_char = r, w
        elif r > num:
            lr, lw = last_no_cn_char
            中文列表[str(lr)] = lw
            index += 1

    return list(中文列表.values())


# print(获取十个密度从低到高的字符列表())

def 获取十个密度从低到高的字符列表2():
    中文列表 = {}
    from 神笔码靓.神笔库.字符串列表 import 字符面积占比排序列表
    for w, r in 字符面积占比排序列表:
        str_r = str(r)
        if str_r not in 中文列表:
            中文列表[str_r] = []
        中文列表[str_r] += [w]

    return 中文列表


def 字符串去重(text):
    seen = set()  # 用于存储已经见过的字符
    result = []  # 用于存储去重后的字符

    for char in text:
        if char not in seen:  # 如果字符未被见过
            seen.add(char)  # 添加到已见集合
            result.append(char)  # 添加到结果列表

    return ''.join(result)  # 将结果列表转换为字符串


# print(获取十个密度从低到高的字符列表2())

def 字符密度排序(中文字符列表, 倒序=False):
    from 神笔码靓.神笔库.字符串列表 import 字符面积排序字典
    result = sorted(中文字符列表, key=lambda x: 字符面积排序字典[x], reverse=倒序)
    return ''.join(result)


def 打印面积密度字符字典():
    from 神笔码靓.神笔库.字符串列表 import 面积密度字符字典
    print(面积密度字符字典)
# 0.06 0.1 0.15 0.2
#  ∷♂◎±ⅹ入八火尘千水齐马旺妤想象魏鞭
# 打印面积密度字符字典()

# # 示例
# test_chars = ['汉', '字', 'a', '1', '中']
# for char in test_chars:
#     if is_chinese_char(char):
#         print(f"{char} 是中文字符")
#     else:
#         print(f"{char} 不是中文字符")


#
#
# 最大面积 = 排序后的列表[-4][1]
#
# 排序后的列表 = [(i, round(c / 最大面积, 2)) for i, c in 排序后的列表]
#
# print(排序后的列表)
