# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-17
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import svgwrite

from 神笔码靓.神笔库.元素库 import 元素模板, 元素组
from 神笔码靓.神笔库.动画工具集 import 缩放动画关键帧, 旋转动画关键帧, 倾斜动画关键帧, 平移动画关键帧
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.通用工具集 import *


class 可操作元素集合(列表):
    def __init__(self, 绘图板, seq=()):
        # # def __init__(self, seq=())
        # list.__init__(self, seq=seq)
        from 神笔码靓.神笔库 import 神笔绘图板
        self.绘图板: 神笔绘图板 = 绘图板

    def 元素类型列表(self):
        from 神笔码靓.神笔库.元素库 import 元素
        for item in self:
            if isinstance(item, 元素):
                yield item

    def 添加到列表(self, 元素列表: list):
        for item in self.元素类型列表():
            item.添加到列表(元素列表)
        return self

    def _操作(self, *args, **kwargs):
        操作名 = kwargs["操作名"]
        del kwargs["操作名"]
        for item in self.元素类型列表():
            if hasattr(item, 操作名):
                funs = getattr(item, 操作名)
                if callable(funs):
                    funs(*args, **kwargs)
        return self

    def __getattr__(self, name):
        # name 是方法名
        def method(*args, **kwargs):
            # print(f"调用的方法名: {name}")
            # print(f"参数: {args}, 关键字参数: {kwargs}")
            kwargs["操作名"]=name
            self._操作(*args, **kwargs)
            return self

        return method

    # def __getattr__(self, item):
    #     self._操作(操作名=item, 透明度=透明度)
    #     return super().__getattr__(item)

    #
    # def 平移2(self, 位移X, 位移Y=None):
    #     for item in self.元素类型列表():
    #         if hasattr(item, "平移"):
    #             funs = getattr(item, "平移")
    #             if callable(funs):
    #                 funs(位移X, 位移Y)
    #     return self

    def 平移(self, 位移X, 位移Y=None):
        self._操作(操作名="平移", 位移X=位移X, 位移Y=位移Y)
        return self

    # def 透明度(self, 透明度=1):
    #     self._操作(操作名="透明度", 透明度=透明度)
    #     return self

    def 合并为模板(self, id_: str = None, class_name: str = None, style: str = None,
              样式类名: str = None, 样式串: str = None, ) -> 元素模板:
        元素列表 = 列表()
        self.添加到列表(元素列表)
        return self.绘图板.创建模板(元素列表=元素列表, id_=id_, class_name=class_name, style=style,
                             样式类名=样式类名, 样式串=样式串)

    def 合并为组(self, class_name: str = None, style=None, 样式类名: str = None,
             样式串: str = None, id_: str = None, 追加元素=None) -> 元素组:
        from 神笔码靓.神笔库.元素库 import 元素
        元素列表 = 列表()
        self.添加到列表(元素列表)

        if isinstance(追加元素, 元素):
            追加元素.添加到列表(元素列表)
        elif isinstance(追加元素, list):
            for 元素_ in 追加元素:
                if isinstance(元素_, 元素):
                    元素_.添加到列表(元素列表)

        return self.绘图板.创建组合(元素列表=元素列表, class_name=class_name, style=style,
                             样式类名=样式类名, 样式串=样式串, id_=id_)
