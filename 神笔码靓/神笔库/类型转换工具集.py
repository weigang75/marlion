# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================


class 类型转换工具集:

    @staticmethod
    def 转浮点型(val, 默认值=None):
        return 类型转换工具集.转类型(float, val, 默认值)

    @staticmethod
    def 转整型(val, 默认值=None):
        return 类型转换工具集.转类型(int, val, 默认值)

    @staticmethod
    def 转布尔型(val, 默认值=None):
        return 类型转换工具集.转类型(bool, val, 默认值)

    @staticmethod
    def 转类型(type_, val, 默认值=None):
        try:
            return type_(val)
        except Exception as e:
            return 默认值
