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

生成随机数 = random.random
生成范围内随机数 = random.uniform
获取范围内随机整数 = random.randint
获取随机元素 = random.choice
打乱顺序 = random.shuffle
获取定长片段 = random.sample

真 = True
假 = False
空 = None
# 打印 = print
输入 = input

# 数值相关
绝对值 = abs
幂值 = pow
幂运算 = pow
四舍五入值 = round
商和余数 = divmod
复数 = complex
转整数 = int
转浮点数 = float
表达式取值 = eval
# 比较大小=cmp(x,y)

# 转换
转布尔值 = bool
转字节可变数组 = bytearray
转不可变字节数组 = bytearray
转内存查看对象 = memoryview
转二进制 = bin
转八进制 = oct
转十六进制 = hex
字符转统一码 = ord
统一码转字符 = chr

# 序列相关
返回长度 = len
返回最大值 = max
返回最小值 = min
求和 = sum
返回排序后列表 = sorted
返回反转后序列 = reversed
范围 = range
迭代器 = iter
切片器 = slice
映射器 = map
过滤器 = filter
下一个 = next
枚举 = enumerate
索引列举 = enumerate
打包 = zip
是否全为真 = all
是否某项为真 = any

def 索引范围(*args):
    """
    索引范围(stop) -> 索引范围 object
    索引范围(start, stop[, step]) -> 索引范围 object
    @return:
    """
    return enumerate(range(*args))

# class相关
是否是后者的子类 = issubclass


def 对象是后者的子类(对象, 类型):
    return issubclass(对象, 类型)


def 对象不是后者的子类(对象, 类型):
    return not issubclass(对象, 类型)


是否为此种类型 = isinstance


def 对象是此种类型(对象, 类型):
    return isinstance(对象, 类型)


def 对象不是此种类型(对象, 类型):
    return not isinstance(对象, 类型)


返回数据类型 = type
对象是否包含属性 = hasattr  # 对象是类的实例?
获取对象的属性值 = getattr
设置对象的属性值 = setattr
删除对象的某属性 = delattr
是否可调用 = callable

# 打开文件 = open

英文关键字 = ['and', 'or', 'not', 'is', 'in', 'if', 'else', 'elif', 'assert'
    , 'while', 'break', 'for', 'continue', 'pass', 'del']
英文关键字2 = ['try', 'except', 'finally', 'raise', 'lambda', 'global', 'nonlocal', 'lambda']


def 打印(*内容: object, 分隔符: str = ' ', 结束: str = '\n', 输出到文件=sys.stdout) -> None:
    print(*内容, sep=分隔符, end=结束, file=输出到文件)


def 打开文本文件(文件名, 模式: str, 编码='utf-8'):
    '''
    模式: 'r'只读，'w'可写，'a'追加，'wb'二进制写入。。。

    举例：【 with 打开文件('txt.txt', 'r') as 文件: 】
    '''
    模式 = 模式.replace("二进制写", "wb").replace("读", "r").replace("写", "w").replace("追加", "a")
    return open(文件名, 模式, encoding=编码)


def 读取文本文件(文件名, 编码='utf-8'):
    '''
    模式: 'r'只读，'w'可写，'a'追加，'wb'二进制写入。。。

    举例：【 with 打开文件('txt.txt', 'r') as 文件: 】
    '''
    return open(文件名, "r", encoding=编码)


# def 读取文件内容(文件):
#     return 文件.read()

class 整数(int):
    pass


class 浮点数(float):
    pass


class 字符串(str):
    首字母转大写 = str.capitalize
    全转小写字母 = str.lower
    全转大写字母 = str.upper
    大小写切换 = str.swapcase
    去空格_左端 = str.lstrip
    去空格_右端 = str.rstrip
    去空格_左右两端 = str.strip
    统计字符出现次数 = str.count
    是否以子串结束 = str.endswith
    是否以子串开头 = str.startswith
    是否只包含空格 = str.isspace
    是否只包含数字字符包括汉字数字 = str.isnumeric
    是否只包含数字字符 = str.isdigit
    是否只包含字母字符 = str.isalpha
    指定宽度返回左对齐 = str.ljust
    指定宽度返回右对齐 = str.rjust

    # 用子串分割成三元组 = str.partition
    # 用子串分割成三元组从右侧 = str.rpartition
    按行数分割成列表 = str.splitlines
    格式化 = format
    合并序列中的字符串 = str.join

    def 查找子串位置(self, 子串: str):
        # 找不到会返回-1
        return str.find(self, 子串)

    def 查找子串位置从后面(self, 子串: str):
        # 找不到会返回-1
        return str.rfind(self, 子串)

    def 字符串替换(self, 被替换: str, 替换成: str):
        return self.replace(被替换, 替换成)

    def 字符串分割成列表(self, 分割符: str = ' '):
        return 列表(self.split(分割符))


class 列表(list):
    列表反转 = list.reverse  # 参数不能中文提示，无需参数的使用这种

    def 列表排序(self, 比较元素=None, 是否降序=False):
        self.sort(key=比较元素, reverse=是否降序)

    def 添加元素(self, 新元素):
        return self.append(新元素)

    def 列表扩展(self, 新增序列):
        return self.extend(新增序列)

    def 插入元素(self, 位置, 新增元素):
        return self.insert(位置, 新增元素)

    def 删除某元素(self, 元素):
        # 删除列表中某个元素的第一个匹配项
        return self.remove(元素)

    def 删除末尾元素(self, 序号=-1):
        # 删除列表中后面的1个元素,默认最后1个
        return self.pop(序号)

    def 统计元素出现次数(self, 元素) -> int:
        return self.count(元素)

    def 查找元素位置(self, 元素) -> int:
        # 查找元素中列表中第一次出现的位置,找不到会抛出异常ValueError: x is not in list,建议先判断 x in list
        return self.index(元素)

    def 神笔绘图板(self, 绘图板):
        from 神笔码靓.神笔库 import 神笔绘图板
        self.绘图板: 神笔绘图板 = 绘图板

    def 创建组合(self, class_name: str = None, style=None,
             样式类名: str = None, 样式串: str = None, id_: str = None):
        from 神笔码靓.神笔库 import 神笔绘图板
        if hasattr(self, "绘图板"):
            神笔: 神笔绘图板 = self.绘图板
        else:
            from 神笔码靓.神笔库 import 获取上下文实例对象
            神笔: 神笔绘图板 = 获取上下文实例对象(神笔绘图板)
        if 神笔 is None:
            err_msg = "需要调用：列表.神笔绘图板(神笔绘图板实例),给列表对象实例指定神笔绘图板。"
            raise Exception(err_msg)
        return 神笔.创建组合(元素列表=self, class_name=class_name, style=class_name,
                       样式类名=样式类名, 样式串=样式串, id_=id_)

    def 创建模板(self, class_name: str = None, style=None,
             样式类名: str = None, 样式串: str = None, id_: str = None):
        from 神笔码靓.神笔库 import 神笔绘图板
        if hasattr(self, "绘图板"):
            神笔: 神笔绘图板 = self.绘图板
        else:
            from 神笔码靓.神笔库 import 获取上下文实例对象
            神笔: 神笔绘图板 = 获取上下文实例对象(神笔绘图板)
        if 神笔 is None:
            err_msg = "需要调用：列表.神笔绘图板(神笔绘图板实例),给列表对象实例指定神笔绘图板。"
            raise Exception(err_msg)
        return 神笔.创建模板(元素列表=self, class_name=class_name, style=class_name,
                       样式类名=样式类名, 样式串=样式串, id_=id_)


class 元组(tuple):
    def 统计元素出现次数(self, 元素) -> int:
        return self.count(元素)

    def 查找元素位置(self, 元素) -> int:
        # 查找元素中元组中第一次出现的位置,找不到会抛出异常ValueError: x is not in list,建议先判断 x in list
        return self.index(元素)


class 字典(dict):
    以序列元素为键创建字典 = dict.fromkeys
    返回字典的所有键 = dict.keys
    返回字典的所有值 = dict.values
    返回键值对二元组 = dict.items
    返回指定键的值 = dict.get
    返回指定键的值_无则添加 = dict.setdefault
    删除键值并返回值 = dict.pop
    随机删除并返回键值 = dict.popitem
    清空字典 = dict.clear
    复制字典 = dict.copy
    更新字典同键部分 = dict.update


def 以序列元素为键创建字典(序列, 默认值=None) -> 字典:
    return 字典(dict.fromkeys(序列, 默认值))


class 集合(set):
    添加元素 = set.add
    有新值则更新集合 = set.update
    删除存在的元素 = set.remove
    删除元素 = set.discard
    随机删除1个元素 = set.pop
    返回交集 = set.intersection
    删除交集之外元素 = set.intersection_update
    返回差集 = set.difference
    删除差集之外元素 = set.difference_update
    返回异或 = set.symmetric_difference
    删除异或之外元素 = set.symmetric_difference_update
    是否被包含 = set.issubset
    是否包含子集 = set.issuperset
    是否不相交 = set.isdisjoint


def 是否为数值(文本):
    s = str(文本)
    if s.isdigit():
        return True
    elif re.match(r'^\d+\.\d+$', s) or re.match(r'^\d+\.$', s):
        return True
    else:
        return False


def 取最小数(*数字):
    return min(数字)


def 取最大数(*数字):
    return max(数字)


def 为空(字符串):
    if 字符串 is None:
        return True
    if isinstance(字符串, list):
        return len(字符串) == 0

    if str(字符串).strip() == "":
        return True
    return False


def 不为空(字符串):
    return not 为空(字符串)


连接路径 = os.path.join
获取文件名 = os.path.basename
分解文件名 = os.path.splitext
路径是否存在 = os.path.exists
是否绝对路径 = os.path.isabs
是否为目录 = os.path.isdir
是否为文件 = os.path.isfile

获取目录文件列表 = os.listdir


def 获取文件路径的文件名和扩展名(文件路径):
    return os.path.splitext(os.path.basename(文件路径))

# def 循环(循环体, 循环逻辑代码):
#     for i in 循环体:
#         循环逻辑代码(i)
#
#
# if __name__ == '__main__':
#     循环([1, 2, 3], 循环逻辑代码=lambda i: 打印(i))
#
# if __name__ == '__main__':
#    打印(获取文件路径的文件名和扩展名("c:/aaaa/bbb.txt"))
