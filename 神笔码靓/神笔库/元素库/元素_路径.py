# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os
import svgwrite

from 神笔码靓.神笔库 import 打印红色消息
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.元素库 import 可变换元素, 元素位置信息, 样式可修改元素
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 路径元素(可变换元素, 样式可修改元素):
    _路径元素列表 = []

    def __init__(self, 高清图, 所属组: list):
        super(路径元素, self).__init__(高清图, 所属组)
        self.前路径: 路径元素 = None
        self.后路径: 路径元素 = None
        self._路径元素列表.append(self)
        self._批量坐标 = []
        self._点辅助全局开 = True
        self._点辅助字典 = {}

    def 点辅助记录点(self, 记录点ID):
        if 记录点ID in self._点辅助字典:
            return self._点辅助字典[记录点ID]
        return None

    def 寻找路径(self, 索引=None, id_=None):
        from 神笔码靓.神笔库.元素库 import 路径元素
        路径元素_: 路径元素 = self
        if 索引 is None and id_ is None:
            return 路径元素_
        elif id_ is not None:
            for 路径元素 in self._路径元素列表:
                if 路径元素.获取属性值("id_") == id_:
                    路径元素_ = 路径元素
                    break
        elif 索引 is not None:
            路径元素_ = self._路径元素列表[索引]
        return 路径元素_

    def 落笔(self, x, y=None):
        self.移动到(x, y)
        return self

    def 移动到(self, x, y=None):
        if y is None:
            x, y = x
        self.追加顶点(("M", x, y))
        self._记录当前线段数据(x1=x - 1, y1=y, x2=x, y2=y)
        return self

    # region 批量生成线
    def 坐标(self, x, y=None):
        if y is None or isinstance(x, tuple):
            self._批量坐标.append(x)
        elif x is not None and y is not None:
            self._批量坐标.append((x, y))
        else:
            raise Exception(f"坐标的数据不正确：({x},{y})")

        return self

    def 坐标缩放(self, 缩放X, 缩放Y=None, 缩放中心点=None, 重置=False):
        if 缩放Y is None:
            缩放Y = 缩放X
        if 缩放中心点 is None:
            缩放中心点 = 0j
        if 重置:
            坐标缩放 = []
        else:
            坐标缩放 = self.获取属性值("坐标缩放", [])
        坐标缩放.append((缩放X, 缩放Y, 缩放中心点))
        self.设置属性值("坐标缩放", 坐标缩放)
        return self

    def 坐标平移(self, 位移X, 位移Y=None, 重置=False):
        if 位移Y is None:
            位移Y = 位移X
        if 重置:
            坐标平移 = []
        else:
            坐标平移 = self.获取属性值("坐标平移", [])
        坐标平移.append((位移X, 位移Y))
        self.设置属性值("坐标平移", 坐标平移)
        return self

    def 坐标旋转(self, 旋转角度, 旋转中心点=None, 重置=False):
        if 旋转中心点 is not None:
            旋转中心点 = complex(旋转中心点[0], 旋转中心点[1])
        if 重置:
            坐标旋转 = []
        else:
            坐标旋转 = self.获取属性值("坐标旋转", [])
        坐标旋转.append((旋转角度, 旋转中心点))
        self.设置属性值("坐标旋转", 坐标旋转)
        return self

    # def 路径偏移(self, 偏移量):
    #     if 偏移量 == 0 or 偏移量 is None:
    #         return self
    #     self.设置属性值("路径偏移", 偏移量)
    #     return self

    def 反向路径(self, 保留=是):
        反向路径_ = self.克隆()
        if not 保留:
            self.所属组.remove(self)
        import svgpathtools
        p = 反向路径_._get_path()
        path1 = svgpathtools.Path(p)
        反向d = path1.reversed().d()
        if "点列表" in 反向路径_.元素属性:
            del 反向路径_.元素属性["点列表"]
        反向路径_.元素属性["原生path"] = 反向d
        return 反向路径_

    def _布尔运算(self, 布尔运算函数, 其他路径, 保留元素=False):
        import svgpathtools
        path1 = svgpathtools.Path(self.元素属性["原生path"])
        path2 = svgpathtools.Path(其他路径.元素属性["原生path"])
        path = 布尔运算函数(path1, path2)
        新路径 = self.高清图.路径(填充颜色=self.获取属性值("填充颜色", 颜色.透明),
                                  描边颜色=self.获取属性值("描边颜色", 颜色.黑色),
                                  透明度=self.获取属性值("透明度", 1.0),
                                  描边样式=self.获取属性值("描边样式", None),
                                  描边宽度=self.获取属性值("描边宽度", 1)).原生path(path.d())
        if not 保留元素:
            self.删除()
            其他路径.删除()
        return 新路径

    def _创建布尔运算(self, 高精度=1.0):
        from 神笔码靓.神笔库.路径工具集 import 布尔运算
        if 高精度 and 高精度 > 0.01:
            最小采样点数 = int((500 * 高精度) // 1)
            最大采样点数 = max(500, 最小采样点数 * 2)
            return 布尔运算(
                最小采样点数=最小采样点数,  # 增加最小采样点数
                最大采样点数=最大采样点数,  # 增加最大采样点数
                曲线近似误差阈值=0.01,  # 降低误差阈值
                数值容差=1e-9,  # 提高数值精度
                是否几何简化=True,  # 保持几何简化开启以处理自相交
                几何简化容差值=1e-8,  # 减小简化容差以保留细节
                buffer操作的分辨率=8  # 提高buffer分辨率
            )
        else:
            return 布尔运算()

    def 并集(self, 其他路径, 保留元素=False, 高精度=1.0):
        运算 = self._创建布尔运算(高精度=高精度)
        return self._布尔运算(运算.并集, 其他路径, 保留元素)

    def 交集(self, 其他路径, 保留元素=False, 高精度=1.0):
        运算 = self._创建布尔运算(高精度=高精度)
        return self._布尔运算(运算.交集, 其他路径, 保留元素)

    def 差集(self, 其他路径, 保留元素=False, 高精度=1.0):
        运算 = self._创建布尔运算(高精度=高精度)
        return self._布尔运算(运算.差集, 其他路径, 保留元素)

    def 坐标连直线(self):
        if len(self._批量坐标) == 0:
            return self
        for _坐标 in self._批量坐标:
            x, y = _坐标
            self.画直线(终点x=x, 终点y=y)
        self._批量坐标 = []
        return self

    # def 坐标连曲线(self):
    #     if len(self._批量坐标) == 0:
    #         return self
    #     for _坐标 in self._批量坐标:
    #         x, y = _坐标
    #
    #     self._批量坐标 = []
    #     return self

    # endregion

    # region 显示点坐标
    def _获取终点的坐标(self, 点):
        命令 = 点[0]
        if 命令 in ["M", "L", "T"]:
            return 点[1], 点[2]
        elif 命令 == "H":
            c, x = 点
            return x, None
        elif 命令 == "V":
            c, y = 点
            return None, y
        elif 命令 == "C":
            c, x1, y1, x2, y2, x, y = 点
            return x, y
        elif 命令 == "S":
            c, 终点控制点x, 终点控制点y, 终点x, 终点y = 点
            return 终点x, 终点y
        elif 命令 == "Q":
            c, x1, y1, x, y = 点
            return x, y
        elif 命令 == "A":
            c, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y = 点
            return x, y
        elif 命令 in ["z", "Z"]:
            return 0, 0
        else:
            return 0, 0

    def _坐标数(self, 坐标, 保留小数=2):
        return str(round(坐标[0], 保留小数)).rstrip("0").rstrip(".") + ", " + \
            str(round(坐标[1], 保留小数)).rstrip("0").rstrip(".")

    def _显示坐标标签(self, 坐标, 坐标偏移=None, 定位类型=定位点类型.实圆, 字体大小=12):
        x, y = 坐标
        坐标文字 = self._坐标数(坐标)
        if 坐标偏移 is None:
            坐标偏移x, 坐标偏移y = 0, 0
        else:
            坐标偏移x, 坐标偏移y = 坐标偏移
        self.高清图.显示坐标(坐标, 坐标1文字偏移=坐标偏移, 定位类型=定位类型, 字体大小=字体大小)
        # self.高清图.写字(x=x + 坐标偏移x, y=y + 坐标偏移y + 15, 文字=坐标文字)

    def _倒序查找XY(self, 点列表):
        x, y = None, None
        for i in range(-2, -len(点列表) - 1, -1):
            倒数第二点 = 点列表[i]
            x_, y_ = self._获取终点的坐标(倒数第二点)
            if x is None:
                x = x_
            if y is None:
                y = y_
            if x is None or y is None:
                continue
            else:
                break
        return x, y

    def _连辅助线(self, x1, y1, x, y, 字体大小=12):
        描边样式 = f"{round(字体大小 / 4, 2)},{round(字体大小 / 4, 2)}"
        描边宽度 = round(字体大小 / 12, 2)
        self.高清图.连直线(路径点列表=[(x, y), (x1, y1)], 描边颜色=self.高清图.辅助线颜色, 描边宽度=描边宽度,
                           描边样式=描边样式)

    def _显示点坐标_H(self, 最后点, 点列表, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        y = None
        for i in range(-2, -len(点列表), -1):
            倒数第二点 = 点列表[i]
            x, y = self._获取终点的坐标(倒数第二点)
            if y is not None:
                break

        c, x = 最后点
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)

    def _显示点坐标_L(self, 最后点, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        c, x, y = 最后点
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)

    def _显示点坐标_V(self, 最后点, 点列表, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        x = None
        for i in range(-2, -len(点列表), -1):
            倒数第二点 = 点列表[i]
            x, y = self._获取终点的坐标(倒数第二点)
            if x is not None:
                break

        c, y = 最后点
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)

    def _显示点坐标_C(self, 最后点, 点列表, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        x3, y3 = self._倒序查找XY(点列表)
        c, x1, y1, x2, y2, x, y = 最后点
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)
            self._显示坐标标签(坐标=(x1, y1), 坐标偏移=坐标偏移, 定位类型=定位点类型.空方, 字体大小=字体大小)
            self._显示坐标标签(坐标=(x2, y2), 坐标偏移=坐标偏移, 定位类型=定位点类型.实方, 字体大小=字体大小)
            self._连辅助线(x1, y1, x3, y3, 字体大小=字体大小)
            self._连辅助线(x2, y2, x, y, 字体大小=字体大小)
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)

    def _显示点坐标_S(self, 最后点, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        c, x1, y1, x, y = 最后点
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)
            self._连辅助线(x1, y1, x, y, 字体大小=字体大小)
            self._显示坐标标签(坐标=(x1, y1), 坐标偏移=坐标偏移, 定位类型=定位点类型.实方, 字体大小=字体大小)
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)

    def _显示点坐标_Q(self, 最后点, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        c, x1, y1, x, y = 最后点
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)
            self._连辅助线(x1, y1, x, y, 字体大小=字体大小)
            self._显示坐标标签(坐标=(x1, y1), 坐标偏移=坐标偏移, 定位类型=定位点类型.实方, 字体大小=字体大小)
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)

    def _显示点坐标_T(self, 最后点, 点列表, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        x1, y1 = self._倒序查找XY(点列表)
        c, x, y = 最后点
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)
            self._显示坐标标签(坐标=(x1, y1), 坐标偏移=坐标偏移, 字体大小=字体大小)
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)

    def _显示点坐标_A(self, 最后点, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        c, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y = 最后点
        if self._点辅助全局开:
            self._显示坐标标签(坐标=(x, y), 坐标偏移=坐标偏移, 字体大小=字体大小)
        if 记录点ID:
            self._点辅助字典[记录点ID] = (x, y)

    def 点辅助开关(self, 开):
        self._点辅助全局开 = 开
        return self

    def 点辅助(self, 开启=True, 坐标=True, 坐标偏移=None, 辅助线=False, 记录点ID=None, 字体大小=12):
        if not 开启 or (not self._点辅助全局开 and 记录点ID is None):
            return self
        P = self.获取属性值
        点列表 = P("点列表")
        if 点列表 is None:
            return self
        if len(点列表) == 0:
            return self

        点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)

        最后点 = 点列表[-1]

        命令 = 最后点[0]
        # ['M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'C', 'c', 'S', 's', 'Q', 'q', 'T', 't', 'A', 'a', 'Z', 'z']
        if 命令 in ["M", "L"]:
            self._显示点坐标_L(最后点, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 == "H":
            倒数第二点 = 点列表[-2]
            self._显示点坐标_H(最后点, 点列表, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 == "V":
            倒数第二点 = 点列表[-2]
            self._显示点坐标_V(最后点, 点列表, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 == "C":
            倒数第二点 = 点列表[-2]
            self._显示点坐标_C(最后点, 点列表, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 == "S":
            self._显示点坐标_S(最后点, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 == "Q":
            self._显示点坐标_Q(最后点, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 == "T":
            倒数第二点 = 点列表[-2]
            self._显示点坐标_T(最后点, 点列表, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 == "A":
            self._显示点坐标_A(最后点, 坐标=坐标, 坐标偏移=坐标偏移, 辅助线=辅助线, 记录点ID=记录点ID,
                               字体大小=字体大小)
        elif 命令 in ["z", "Z"]:
            pass
        else:
            打印红色消息(f"无法显示点坐标:{最后点}")

        return self

    # endregion

    def 闭合(self):
        self.追加顶点(("闭合",))
        # self._清除当前线段数据()
        self._记录当前线段数据(x1=-1, y1=0, x2=0, y2=0)
        return self

    def _切线(self):
        path = self._conv_svgpathtools()
        postion = 1
        # 获取路径上的点和单位切向量
        point = path.point(postion)
        tangent = path.unit_tangent(postion)

        # 设置切向量显示长度（单位切向量模长为1，需放大以便观察）
        scale = 50  # 可调整此值

        # 计算切向量终点（从路径点出发，沿切向量方向延伸）
        tangent_end = complex(
            point.real + tangent.real * scale,
            point.imag + tangent.imag * scale
        )
        # 反方向点
        tangent_end1 = complex(
            point.real - tangent.real * scale,
            point.imag - tangent.imag * scale
        )
        # 绘制路径点和切向量线段
        # 绘图板.连直线(路径点列表=[
        #     # (tangent_end1.real, tangent_end1.imag),
        #     (point.real, point.imag),  # 起点：路径上的点
        #     (tangent_end.real, tangent_end.imag)  # 终点：沿切向量方向延伸的点
        # ], 描边宽度=0.2, 描边颜色=颜色.红色)
        # print(f"单位切向量: {tangent.real},{tangent.imag}")  # 输出类似: (0.7071067811865476+0.7071067811865475j)
        # print(f"向量模长: {abs(tangent)}")  # 应等于 1.0
        return tangent_end1.real, tangent_end1.imag, point.real, point.imag

    def _获取当前线段数据(self):
        try:
            return self._切线()
        except:
            if hasattr(self, "_当前线段数据"):
                return self._当前线段数据

        return []

    # def _清除当前线段数据(self):
    #     if hasattr(self, "_当前线段数据"):
    #         delattr(self, "_当前线段数据")

    def _计算右转直线坐标(self, x1, y1, x2, y2, angle, length):
        """
        根据已知线段的端点坐标，计算偏转一定角度和长度后的新坐标点。

        参数:
        x1 (float): 线段起点的x坐标
        y1 (float): 线段起点的y坐标
        x2 (float): 线段终点的x坐标
        y2 (float): 线段终点的y坐标
        angle (float): 偏转角度，以弧度制表示
        length (float): 直线长度

        返回:
        tuple: 包含新坐标点的x坐标和y坐标的元组 (x3, y3)
        """
        # 计算原线段的长度
        original_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # 计算原线段与x轴正方向的夹角（弧度制）
        original_angle = math.atan2(y2 - y1, x2 - x1)
        # 计算偏转后的角度
        new_angle = original_angle + angle * math.pi / 180
        # 计算新坐标点的x坐标
        x3 = x2 + length * math.cos(new_angle)
        # 计算新坐标点的y坐标
        y3 = y2 + length * math.sin(new_angle)
        return x3, y3

    def _法线(self, r=0, d=1):
        path = self._conv_svgpathtools()
        postion = 1
        point = path.point(postion)
        normal = path.normal(postion)

        normal_end = complex(
            point.real + normal.real * r,
            point.imag + normal.imag * r
        )
        # 反方向点
        normal_end1 = complex(
            point.real - (normal.real * r),
            point.imag - (normal.imag * r)
        )
        if d == 1:
            return normal_end1.real, normal_end1.imag, point.real, point.imag

        return normal_end.real, normal_end.imag, point.real, point.imag

    def _calculate_arc_endpoint(self, cx, cy, sx, sy, rotation_direction, angle_degrees):
        """
        计算圆弧旋转后的终点坐标

        参数:
        cx, cy: 圆弧中心点坐标
        sx, sy: 圆弧起点坐标
        rotation_direction: 旋转方向，'clockwise' 或 'counterclockwise'
        angle_degrees: 旋转角度（度数）

        返回:
        终点坐标 (ex, ey)
        """
        # 计算起点相对于中心点的坐标
        dx = sx - cx
        dy = sy - cy

        # 计算起点到中心点的距离（半径）
        radius = math.hypot(dx, dy)

        # 计算起点的角度（相对于x轴正方向）
        start_angle = math.atan2(dy, dx)

        # 将角度从度数转换为弧度
        angle_radians = math.radians(angle_degrees)

        # 根据旋转方向调整角度
        if rotation_direction == 1:
            end_angle = start_angle + angle_radians
        else:
            end_angle = start_angle - angle_radians

        # 计算终点相对于中心点的坐标
        ex_relative = radius * math.cos(end_angle)
        ey_relative = radius * math.sin(end_angle)

        # 转换为绝对坐标
        ex = cx + ex_relative
        ey = cy + ey_relative

        return ex, ey

    def 右转弧线(self, 右转角度, 圆弧半径):
        _当前线段数据 = self._获取当前线段数据()
        if _当前线段数据 is None:
            raise Exception("上一条必须是直线")
        x1, y1, x2, y2 = _当前线段数据
        if 右转角度 > 0:
            方向 = 1
        else:
            方向 = 0
        normal_end_real, normal_end_imag, point_real, point_imag = self._法线(圆弧半径, 方向)

        endpoint = self._calculate_arc_endpoint(cx=normal_end_real, cy=normal_end_imag, sx=point_real, sy=point_imag,
                                                rotation_direction=方向, angle_degrees=abs(右转角度))
        # self.高清图.十字(x=x1, y=y1,颜色=颜色.红色)
        # self.高清图.十字(x=normal_end_real, y=normal_end_imag, 颜色=颜色.红色)
        # self.高清图.十字(x=point_real, y=point_imag, 颜色=颜色.蓝色)
        # self.高清图.十字(x=endpoint[0], y=endpoint[1], 颜色=颜色.绿色)

        self.画圆弧(圆弧半径=圆弧半径, 终点=endpoint, 圆弧方向=方向)

        return self

    def 左转弧线(self, 左转角度, 圆弧半径):
        self.右转弧线(-左转角度, 圆弧半径)
        return self

    # region 倒圆角直线
    # 向量工具方法
    def _vec_sub(self, a, b):
        return (a[0] - b[0], a[1] - b[1])

    def _vec_add(self, a, b):
        return (a[0] + b[0], a[1] + b[1])

    def _vec_mul(self, v, k):
        return (v[0] * k, v[1] * k)

    def _vec_dot(self, a, b):
        return a[0] * b[0] + a[1] * b[1]

    def _vec_cross(self, a, b):
        return a[0] * b[1] - a[1] * b[0]

    def _vec_len(self, v):
        return math.hypot(v[0], v[1])

    def _vec_normalize(self, v):
        l = self._vec_len(v)
        if l < self.eps:
            raise ValueError("零向量，三点共线无法倒角")
        return (v[0] / l, v[1] / l)

    def _line_point_project(self, line_p0, line_p1, pt):
        """点投影到直线，返回垂足（圆角切点）"""
        a = self._vec_sub(pt, line_p0)
        b = self._vec_sub(line_p1, line_p0)
        t = self._vec_dot(a, b) / self._vec_dot(b, b)
        proj = self._vec_add(line_p0, self._vec_mul(b, t))
        return proj

    def _calc_fillet_tangent(self, p0, p1, p2, r):
        """
        折线p0-p1-p2倒圆角，计算两线段切点与倒角方向
        :param p0: 线段A起点 (x,y)
        :param p1: 折角顶点 (x,y)
        :param p2: 线段B终点 (x,y)
        :param r: 倒角半径
        :return: (tangent1, tangent2, dir_flag)
            tangent1: p0-p1上切点
            tangent2: p1-p2上切点
            dir_flag: 1=内角凸倒角，-1=外侧凹倒角
        """
        if r <= self.eps:
            raise ValueError("倒角半径必须大于0")

        # 两条边向量
        v1_raw = self._vec_sub(p1, p0)
        v2_raw = self._vec_sub(p1, p2)
        u1 = self._vec_normalize(v1_raw)
        u2 = self._vec_normalize(v2_raw)

        # 夹角计算
        dot_val = self._vec_dot(u1, u2)
        dot_val = max(min(dot_val, 1.0), -1.0)
        theta = math.acos(dot_val)
        if theta < self.eps:
            raise ValueError("三点近似共线，不存在夹角，无法倒角")

        # 判断倒角朝向
        cross_val = self._vec_cross(u1, u2)
        dir_flag = 0 if cross_val > 0 else 1

        # 角平分线单位向量
        bisector = self._vec_add(u1, u2)
        u_bis = self._vec_normalize(bisector)

        # 计算圆角圆心
        dist_p1_center = r / math.sin(theta / 2)
        center = self._vec_add(p1, self._vec_mul(u_bis, -dist_p1_center))

        # 求两条边上的切点
        tan1 = self._line_point_project(p0, p1, center)
        tan2 = self._line_point_project(p1, p2, center)

        return tan1, tan2, dir_flag

    def 倒圆角直线(self, 点1, 点2, 倒角半径):
        self.eps = 1e-12
        点1x, 点1y = 点1
        点2x, 点2y = 点2

        上一个点 = self._获取上一个点的数据()
        if 上一个点 is None:
            raise Exception("倒角直线不能第一个使用")
        else:
            点0 = 上一个点
            点0x, 点0y = 上一个点

        t1, t2, direct = self._calc_fillet_tangent(点0, 点1, 点2, 倒角半径)

        self.画直线(t1)
        self.画圆弧(圆弧半径=倒角半径, 终点=t2, 圆弧方向=direct)
        self.画直线(点2)

        x1 = 点1x
        y1 = 点1y
        self._记录当前线段数据(x1=t2[0], y1=t2[1], x2=点2x, y2=点2y)

        return self

    # endregion 倒圆角直线

    def 右转直线(self, 右转角度, 直线长度):
        _当前线段数据 = self._获取当前线段数据()
        if _当前线段数据 is None:
            raise Exception("上一条必须是直线")
        x1, y1, x2, y2 = _当前线段数据
        x3, y3 = self._计算右转直线坐标(x1, y1, x2, y2, 右转角度, 直线长度)

        # A = x1, y1
        # B = x2, y2
        #
        # self.高清图.定位(A, B)

        self.画直线(x3, y3)
        return self

    def 右转移动(self, 右转角度, 直线长度):
        _当前线段数据 = self._获取当前线段数据()
        if _当前线段数据 is None:
            raise Exception("上一条必须是直线")
        x1, y1, x2, y2 = _当前线段数据
        x3, y3 = self._计算右转直线坐标(x1, y1, x2, y2, 右转角度, 直线长度)
        self.移动到(x3, y3)
        return self

    def 左转移动(self, 左转角度, 直线长度):
        self.右转移动(-左转角度, 直线长度)
        return self

    def 左转直线(self, 左转角度, 直线长度):
        self.右转直线(-左转角度, 直线长度)
        return self

    def 前进直线(self, 直线长度):
        self.右转直线(0, 直线长度)
        return self

    def 后退直线(self, 直线长度):
        self.右转直线(0, -直线长度)
        return self

    def _获取上一个点的数据(self):
        P = self.获取属性值
        点列表 = P("点列表")
        if 点列表 is None:
            return None
        if len(点列表) == 0:
            return None

        点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)

        点x, 点y = None, None
        for i in range(len(点列表) - 1, -1, -1):
            if not (点x is None and 点y is None):
                break
            点 = 点列表[i]
            # # ['M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'C', 'c', 'S', 's', 'Q', 'q', 'T', 't', 'A', 'a', 'Z', 'z']
            #
            if 点[0] in ["M", "L", "T"]:
                return 点[1], 点[2]
            # elif 点[0] == "L":
            #     return 点[1], 点[2]
            elif 点[0] == "H":
                点x = 点[1]
            elif 点[0] == "V":
                点y = 点[1]
            elif 点[0] == "S":
                # c, x1, y1, x, y
                return 点[3], 点[4]
            elif 点[0] == "C":
                # c, x1, y1, x2, y2, x, y
                return 点[5], 点[6]
            elif 点[0] == "Q":
                # c, x1, y1, x, y
                return 点[3], 点[4]
            # elif 点[0] == "T":
            #     # c, x, y
            #     return 点[1], 点[2]
            elif 点[0] == "A":
                # c, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y
                return 点[6], 点[7]
            else:
                打印红色消息(f"上一个点的数据：{点}")
                return None

        if 点x is None and 点y is None:
            return None
        return 点x, 点y

    # endregion

    # region 新路径

    def _新路径设置属性(self, 新路径):
        """
        @return:
        """
        描边宽度 = self.获取属性值("描边宽度", 1)
        新路径.描边宽度(描边宽度)
        填充颜色 = self.获取属性值("填充颜色", None)
        if 填充颜色 is not None:
            新路径.填充颜色(填充颜色)
        描边颜色 = self.获取属性值("描边颜色", None)
        if 描边颜色 is not None:
            新路径.描边颜色(描边颜色)
        透明度 = self.获取属性值("透明度", None)
        if 透明度 is not None:
            新路径.透明度(透明度)
        描边样式 = self.获取属性值("描边样式", None)
        if 描边样式 is not None:
            新路径.描边样式(描边样式)

    def 新路径(self, x=None, y=None, 描边颜色=None, 填充颜色=None, 描边宽度=None,
               透明度=None, 描边样式: str = None, id_: str = None):
        """

        @return:
        """
        上一个点的数据 = self._获取上一个点的数据()
        if 上一个点的数据 is None:
            x_, y_ = 0, 0
        else:
            x_, y_ = 上一个点的数据

        if x is None:
            x = x_
        if y is None:
            y = y_

        新路径 = 路径元素(self.高清图, self.所属组)
        新路径.设置属性值("点列表", [])
        if x is None and y is None:
            新路径.移动到(0, 0)
        elif x is None:
            新路径.移动到(0, y)
        elif y is None:
            新路径.移动到(x, 0)
        else:
            新路径.移动到(x, y)
        self._新路径设置属性(新路径)

        if 描边宽度 is not None:
            新路径.描边宽度(描边宽度)
        if 填充颜色 is not None:
            新路径.填充颜色(填充颜色)
        if 描边颜色 is not None:
            新路径.描边颜色(描边颜色)
        if 透明度 is not None:
            新路径.透明度(透明度)
        if 描边样式 is not None:
            新路径.描边样式(描边样式)
        if id_ is not None:
            新路径.设置属性值("id_", id_)

        新路径.前路径 = self
        self.后路径 = 新路径
        return 新路径

    def 新描边颜色(self, 颜色值, id_: str = None):
        新路径 = self.新路径()
        新路径.设置属性值(属性名="描边颜色", 属性值=颜色值)
        if id_ is not None:
            新路径.设置属性值("id_", id_)
        return 新路径

    def 新描边宽度(self, 宽度值, id_: str = None):
        新路径 = self.新路径()
        新路径.设置属性值(属性名="描边宽度", 属性值=宽度值)
        if id_ is not None:
            新路径.设置属性值("id_", id_)
        return 新路径

    def 新描边样式(self, 样式值, id_: str = None):
        新路径 = self.新路径()
        新路径.设置属性值(属性名="描边样式", 属性值=样式值)
        if id_ is not None:
            新路径.设置属性值("id_", id_)
        return 新路径

    # endregion

    def 画直线(self, 终点x, 终点y=None):
        if 终点y is None:
            终点x, 终点y = 终点x
        上一个点 = self._获取上一个点的数据()
        if 上一个点 is not None:
            x1, y1 = 上一个点
            self._记录当前线段数据(x1=x1, y1=y1, x2=终点x, y2=终点y)
        self.追加顶点(("L", 终点x, 终点y))
        return self

    # region 旋转直线
    def _记录当前线段数据(self, x1=None, y1=None, x2=None, y2=None):
        if hasattr(self, "_当前线段数据"):
            if x1 is not None:
                self._当前线段数据[0] = x1
            if y1 is not None:
                self._当前线段数据[1] = y1
            if x2 is not None:
                self._当前线段数据[2] = x2
            if y2 is not None:
                self._当前线段数据[3] = y2
        else:
            self._当前线段数据 = [x1, y1, x2, y2]

    def 画水平线(self, 终点x):
        上一个点 = self._获取上一个点的数据()
        if 上一个点 is not None:
            上一个点x, 上一个点y = 上一个点
            x1, y1, x2, y2 = 上一个点x, 上一个点y, 终点x, 上一个点y
            self._记录当前线段数据(x1, y1, x2, y2)
        self.追加顶点(("H", 终点x))
        return self

    def 画垂直线(self, 终点y):
        上一个点 = self._获取上一个点的数据()
        if 上一个点 is not None:
            上一个点x, 上一个点y = 上一个点
            x1, y1, x2, y2 = 上一个点x, 上一个点y, 上一个点x, 终点y
            self._记录当前线段数据(x1, y1, x2, y2)
        self.追加顶点(("V", 终点y))
        return self

    def 画曲线(self, 开始控制点: tuple[float, float], 终点控制点: tuple[float, float], 终点: tuple[float, float]):
        开始控制点x, 开始控制点y = 开始控制点
        终点控制点x, 终点控制点y = 终点控制点
        终点x, 终点y = 终点
        # self._清除当前线段数据()
        self.追加顶点(("C", 开始控制点x, 开始控制点y, 终点控制点x, 终点控制点y, 终点x, 终点y))
        self._记录当前线段数据(x1=终点控制点x, y1=终点控制点y, x2=终点x, y2=终点y)
        return self

    def 三次贝塞尔曲线(self, 开始控制点: tuple[float, float], 终点控制点: tuple[float, float],
                       终点: tuple[float, float]):
        开始控制点x, 开始控制点y = 开始控制点
        终点控制点x, 终点控制点y = 终点控制点
        终点x, 终点y = 终点
        # self._清除当前线段数据()
        self.追加顶点(("C", 开始控制点x, 开始控制点y, 终点控制点x, 终点控制点y, 终点x, 终点y))
        self._记录当前线段数据(x1=终点控制点x, y1=终点控制点y, x2=终点x, y2=终点y)
        return self

    def 平滑曲线(self, 终点控制点: tuple[float, float], 终点: tuple[float, float]):
        终点x, 终点y = 终点
        终点控制点x, 终点控制点y = 终点控制点
        # self._清除当前线段数据()
        self.追加顶点(("S", 终点控制点x, 终点控制点y, 终点x, 终点y))
        self._记录当前线段数据(x1=终点控制点x, y1=终点控制点y, x2=终点x, y2=终点y)
        return self

    def 二次贝塞尔曲线(self, 曲线控制点: tuple[float, float], 终点: tuple[float, float]):
        终点x, 终点y = 终点
        曲线控制点x, 曲线控制点y = 曲线控制点
        # self._清除当前线段数据()
        self.追加顶点(("Q", 曲线控制点x, 曲线控制点y, 终点x, 终点y))
        self._记录当前线段数据(x1=曲线控制点x, y1=曲线控制点y, x2=终点x, y2=终点y)
        return self

    def 平滑的二次贝塞尔曲线(self, 终点: tuple[float, float]):
        终点x, 终点y = 终点
        上一个点 = self._获取上一个点的数据()
        if 上一个点 is None:
            x1 = 终点x - 1
            y1 = 终点y
        else:
            x1, y1 = 上一个点
        # self._清除当前线段数据()
        self.追加顶点(("T", 终点x, 终点y))
        self._记录当前线段数据(x1=x1, y1=y1, x2=终点x, y2=终点y)
        return self

    import math

    def calculate_slope_of_elliptical_arc_point(self, x1, y1, x2, y2, rx, ry, x_axis_rotation, large_arc_flag,
                                                sweep_flag, x,
                                                y):
        """
        计算使用A命令绘制的椭圆弧上某点的斜率。

        参数:
        x1 (float): A命令椭圆弧起始点的x坐标
        y1 (float): A命令椭圆弧起始点的y坐标
        x2 (float): A命令椭圆弧终点的x坐标
        y2 (float): A命令椭圆弧终点的y坐标
        rx (float): 椭圆弧所在椭圆的x轴半径
        ry (float): 椭圆弧所在椭圆的y轴半径
        x_axis_rotation (float): A命令中的x - axis - rotation参数，旋转角度
        large_arc_flag (int): A命令中的large - arc - flag参数，大弧标志（0或1）
        sweep_flag (int): A命令中的sweep - flag参数，绘制方向标志（0或1）
        x (float): 椭圆弧上要计算斜率的点的x坐标
        y (float): 椭圆弧上要计算斜率的点的y坐标

        返回:
        float: 椭圆弧上该点的斜率，如果无法计算（例如在垂直切线情况下）返回None
        """
        import math

        # 将角度转换为弧度
        angle = math.radians(x_axis_rotation)
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        # 步骤1：将终点坐标转换到未旋转的椭圆坐标系
        dx = (x1 - x2) / 2
        dy = (y1 - y2) / 2
        x1_ = cos_angle * dx + sin_angle * dy
        y1_ = -sin_angle * dx + cos_angle * dy

        # 确保半径足够大
        rx = abs(rx)
        ry = abs(ry)
        rx_sq = rx * rx
        ry_sq = ry * ry
        x1_sq = x1_ * x1_
        y1_sq = y1_ * y1_

        # 计算椭圆中心
        radical = (rx_sq * ry_sq - rx_sq * y1_sq - ry_sq * x1_sq) / (rx_sq * y1_sq + ry_sq * x1_sq)
        if radical < 0:
            radical = 0
        radical = math.sqrt(radical)

        if large_arc_flag == sweep_flag:
            radical = -radical

        cx_ = radical * rx * y1_ / ry
        cy_ = -radical * ry * x1_ / rx

        # 将终点转换回原始坐标系
        cx = cos_angle * cx_ - sin_angle * cy_ + (x1 + x2) / 2
        cy = sin_angle * cx_ + cos_angle * cy_ + (y1 + y2) / 2

        # 计算终点相对于椭圆中心的角度
        angle_x = (x2 - cx) * cos_angle + (y2 - cy) * sin_angle
        angle_y = -(x2 - cx) * sin_angle + (y2 - cy) * cos_angle

        # 计算斜率
        try:
            slope = (-rx * angle_y) / (ry * angle_x)
            return slope
        except ZeroDivisionError:
            return None

    def 画椭圆弧(self, x圆弧半径, y圆弧半径, 终点: tuple[float, float], 圆弧方向=0, 是否大弧=False):
        # "椭圆弧线": "A",  # (rx, ry), x_axis_rotation, (large_arc_flag, sweep_flag), (x, y)
        终点x, 终点y = 终点
        if 圆弧方向 != 0:
            圆弧方向 = 1
        if 是否大弧 == True or 是否大弧 == 1:
            是否大弧 = 1
        else:
            是否大弧 = 0
        # self._清除当前线段数据()
        self.追加顶点(("A", x圆弧半径, y圆弧半径, 0, 是否大弧, 圆弧方向, 终点x, 终点y))
        last_x, last_y = self.获取上一个点的位置()
        # slope = self.calculate_slope_of_elliptical_arc_point(x1=last_x, y1=last_y, x2=终点x, y2=终点y, rx=x圆弧半径,
        #                                                      ry=y圆弧半径,
        #                                                      x_axis_rotation=0, large_arc_flag=0, sweep_flag=0, x=终点x,
        #                                                      y=终点y)
        self._记录当前线段数据(x1=终点x - 1, y1=终点y, x2=终点x, y2=终点y)
        return self

    def 画圆弧(self, 圆弧半径, 终点: tuple[float, float], 圆弧方向=0, 是否大弧=False):
        终点x, 终点y = 终点
        if 圆弧方向 != 0:
            圆弧方向 = 1
        # 起点x, 起点y = self.获取上一个点的位置()
        # self._清除当前线段数据()
        self.追加顶点(("圆弧线", 圆弧半径, 圆弧方向, 终点x, 终点y, 是否大弧))
        # last_x, last_y = self.获取上一个点的位置()
        # slope = self.calculate_slope_of_elliptical_arc_point(x1=last_x,y1=last_y,x2=终点x,y2=终点y,rx=圆弧半径,ry=圆弧半径,
        #                                                      x_axis_rotation=0,large_arc_flag=0, sweep_flag=0,x=终点x,y=终点y)
        # 斜率k可以表示为：k = (y2 - y1) / (x2 - x1)
        # slope = (终点y - 起点y) / (终点x - 起点x)
        # slope * (终点x - 起点x) - 终点y =  - 起点y
        # last_x, last_y = self.获取上一个点的位置()
        # # 起点x,起点y = last_x, last_y
        # 起点x = 终点x + 10
        # 起点y = 终点y - slope * (终点x - 起点x)
        # print(slope)
        self._记录当前线段数据(x1=终点x - 1, y1=终点y, x2=终点x, y2=终点y)
        return self

    def 画圆(self, 圆心: tuple[float, float], 圆方向=0, 起点=None):
        圆心x, 圆心y = 圆心
        if 圆方向 != 0:
            圆方向 = 1
        if 起点 is None:
            起点x, 起点y = self.获取上一个点的位置()
        else:
            起点x, 起点y = 起点
        点列表 = self.获取属性值("点列表", [])
        if len(点列表) == 0:
            self.移动到(起点x, 起点y)
        else:
            上起点x, 上起点y = self.获取上一个点的位置()
            if 上起点x != 起点x or 上起点y != 起点y:
                self.画直线(起点x, 起点y)

        终点x, 终点y = 2 * 圆心x - 起点x, 2 * 圆心y - 起点y
        圆半径 = math.sqrt((圆心x - 起点x) ** 2 + (圆心y - 起点y) ** 2)
        # self.追加顶点(("圆弧线", 圆半径, 圆方向, 终点x, 终点y))
        # self.追加顶点(("圆弧线", 圆半径, 圆方向, 起点x, 起点y))

        self.画圆弧(圆弧半径=圆半径, 终点=(终点x, 终点y), 圆弧方向=圆方向)
        self.画圆弧(圆弧半径=圆半径, 终点=(起点x, 起点y), 圆弧方向=圆方向)
        # self._清除当前线段数据()
        # self._记录当前线段数据(x1=终点x - 1, y1=终点y, x2=终点x, y2=终点y)
        return self

    def 路径缩放(self, x=1, y=1):
        """

        @param x:
        @param y:
        @return:
        """
        P = self.获取属性值
        点列表 = P("点列表")

        路径点列表 = []
        from 神笔码靓.神笔库 import 神笔绘图板工具
        点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)

        # ['M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'C', 'c', 'S', 's', 'Q', 'q', 'T', 't', 'A', 'a', 'Z', 'z']
        for 点 in 点列表:
            if 点[0] in ["M", "m", "L", "l", "T", "t"]:
                # 顶点x, 顶点y = 点[1]*x, 点[2]*y
                路径点列表.append((点[0], 点[1] * x, 点[2] * y))
            elif 点[0] in ["C", "c"]:
                # (x1, y1), (x2, y2), (x, y)
                顶点x, 顶点y = 点[5], 点[6]
                路径点列表.append((点[0], 点[1] * x, 点[2] * y, 点[3] * x, 点[4] * y, 点[5] * x, 点[6] * y))

            elif 点[0] in ["H", "h"]:
                顶点x = 点[1]
                路径点列表.append((点[0], 点[1] * x))
            elif 点[0] in ["V", "v"]:
                顶点y = 点[1]
                路径点列表.append((点[0], 点[1] * y))
            elif 点[0] in ["Q", "q", "S", "s"]:
                # (x1, y1), (x, y)
                顶点x, 顶点y = 点[3], 点[4]
                路径点列表.append((点[0], 点[1] * x, 点[2] * y, 点[3] * x, 点[4] * y))
            elif 点[0] in ["A", "a"]:
                # (rx, ry), x_axis_rotation, (large_arc_flag, sweep_flag), (x, y) =
                顶点x, 顶点y = 点[6], 点[7]
                路径点列表.append((点[0], 点[1] * x, 点[2] * y, 点[3], 点[4], 点[5], 点[6] * x, 点[7] * y))
            elif 点[0] in ["Z", "z"]:
                路径点列表.append((点[0],))
            else:
                顶点x, 顶点y = 点[0], 点[1]
                路径点列表.append((点[0] * x, 点[1] * y))

        self.设置属性值("点列表", 路径点列表)

        return self

    def 获取上一个点的位置(self):
        P = self.获取属性值
        点列表 = P("点列表")
        if len(点列表) == 0:
            return 0, 0
        last_x = None
        last_y = None
        for i in range(-1, -len(点列表), -1):
            倒数第二点 = 点列表[i]
            x, y = self._获取终点的坐标(倒数第二点)
            if x is not None:
                last_x = x
            if y is not None:
                last_y = y
            if last_x is not None and last_y is not None:
                break

        return last_x, last_y

    def 列表转方法调用(self):
        P = self.获取属性值
        点列表 = P("点列表")
        方法字典 = {
            "移动": self.移动到,
            "移动到": self.移动到,
            "平滑曲线": self.平滑曲线,
            "曲线": self.画曲线,
            "直线": self.画直线,
            "水平直线": self.画水平线,
            "水平线": self.画水平线,
            "垂直直线": self.画垂直线,
            "垂直线": self.画垂直线,
            "二次贝塞尔曲线": self.二次贝塞尔曲线,
            "平滑的二次贝塞尔曲线": self.平滑的二次贝塞尔曲线,
            "画圆弧": self.画圆弧
        }
        方法调用 = ""
        for 点命令, *参数 in 点列表:
            方法 = 方法字典.get(点命令, None)
            if 方法 is None:
                方法 = f".{点命令}()"
            else:
                params = self._get_function_params(方法)
                方法 = f". \\\n{方法.__name__}("
                pi = 0
                for name, param in params.items():
                    if "tuple" in str(param.annotation):
                        方法 += f"{name}=({参数[pi]}, {参数[pi + 1]}),"
                        pi += 1
                    else:
                        方法 += f"{name}={参数[pi]},"
                    pi += 1

            方法调用 += 方法.strip(",") + ")"
        print(方法调用)
        return self

    def _get_function_params(self, function):
        import inspect

        sig = inspect.signature(function)
        params = sig.parameters
        return params

    def 追加顶点(self, 顶点命令):
        P = self.获取属性值
        点列表 = P("点列表")
        点列表.append(顶点命令)
        return self

    def 合并路径(self, 路径元素_, 保留=否):
        元素_: 路径元素 = 路径元素_
        合并点列表 = 元素_.获取属性值("点列表")
        P = self.获取属性值
        现有点列表 = P("点列表")
        self.设置属性值("点列表", 现有点列表 + 合并点列表)
        if not 保留:
            元素_.所属组.remove(元素_)
        return self

    def 中心点计算(self, 元素位置: 元素位置信息 = None):
        from 神笔码靓.神笔库 import 多边形工具
        现有点列表 = self.获取路径点列表()
        # 元素位置.中心点 = 多边形工具.获取中心点(现有点列表)
        xmin, xmax, ymin, ymax = self.获取边界框()
        中心点 = (xmin + xmax) / 2, (ymin + ymax) / 2
        if 元素位置 is not None:
            元素位置.中心点 = 中心点
        return 中心点

    def 几何重心计算(self, 采样数=1000):
        """计算路径的几何重心"""
        import numpy as np
        # 在路径上均匀采样点
        path = self._conv_svgpathtools()
        t_values = np.linspace(0, 1, 采样数)
        points = np.array([path.point(t) for t in t_values])

        # 分离实部(x)和虚部(y)
        x = points.real
        y = points.imag

        # 计算重心
        centroid_x = np.mean(x)
        centroid_y = np.mean(y)

        return centroid_x, centroid_y

    def 路径长度(self):
        import svgpathtools
        path = svgpathtools.Path(self.获取路径d())
        return path.length()

    def 交点计算(self, 其他路径):
        if not isinstance(其他路径, 路径元素):
            return None
        import svgpathtools
        path1 = svgpathtools.Path(self.获取路径d())
        path2 = svgpathtools.Path(其他路径.获取路径d())
        intersect_path = path1.intersect(path2)
        intersections = []
        # svgpathtools.CompoundPath(merged_path)
        for (T1, seg1, t1), (T2, seg2, t2) in intersect_path:
            intersection = path1.point(T1)
            x, y = intersection.real, intersection.imag
            intersections.append((x, y))
        return intersections
        # for intersection in intersections:
        #     # self.高清图.画圆(intersection.real, intersection.imag, 半径=2, 填充颜色=颜色.红色)

    @property
    def 路径点列表(self):
        P = self.获取属性值
        点列表 = P("点列表")
        return 点列表

    # def 原生路径修正(self):
    #     self.设置属性值("原生路径修正", True)
    #     return self

    def 原生path(self, d=None):
        if d is None:
            if "原生path" in self.元素属性:
                return self.元素属性["原生path"]
            return None
        self.设置属性值(属性名="原生path", 属性值=d)
        return self

    def 追加顶点列表(self, 追加顶点列表):
        P = self.获取属性值
        点列表 = P("点列表")
        点列表 += 追加顶点列表
        return self

    def 获取元素范围(self):
        return self.获取边界框()
        # return self.获取路径点列表范围()

    # def 路径并集(self, 路径):
    #     if 路径 == self:
    #         return self
    #
    #     raise NotImplementedError("暂不支持路径并集")
    #
    #     return self
    #
    # def 路径交集(self, 路径):
    #     if 路径 == self:
    #         return self
    #     raise NotImplementedError("暂不支持路径交集")
    #     from svgpathtools import Path, parse_path
    #     if isinstance(路径, str):
    #         path2_str = 路径
    #     elif isinstance(路径, 路径元素):
    #         path2_str = 路径.获取路径d()
    #     path1_str = self.获取路径d()
    #     #
    #     # path1_obj.unite() # unite()和intersect()
    #     path1_obj = Path(path1_str).intersect(path2_str)
    #     # Path.unit_tangent()
    #     self.设置属性值("原生path", path1_obj.d())
    #     return self
    #
    # def 路径差集(self, 路径):
    #     if 路径 == self:
    #         return self
    #     from svgpathtools import Path
    #     raise NotImplementedError("暂不支持路径差集")
    #
    #     return self

    # def 路径并集(self):
    #     from svgpathtools import *
    #     pass

    def 平滑路径(self, 最大关节大小=3, 紧致度=1.99, 忽略无法修正的弯曲=False):
        平滑路径参数 = {
            "maxjointsize": 最大关节大小,
            "tightness": 紧致度,
            "ignore_unfixable_kinks": 忽略无法修正的弯曲
        }
        self.设置属性值("平滑路径", 平滑路径参数)

    def _get_path(self):
        P = self.获取属性值
        原生path = P("原生path", None)
        if 原生path is None:
            点列表 = P("点列表")
            点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)
            # d_list = 神笔绘图板工具.点列表转SVG路径(点列表)
            path = " ".join(神笔绘图板工具.点列表转SVG路径(点列表))
        else:
            path = 原生path
        return path

    def _conv_svgpathtools(self):
        from svgpathtools import parse_path
        path = self._get_path()
        path_alt = parse_path(path)
        return path_alt

    def 获取边界框(self, 新版本=True):
        path_alt = self._conv_svgpathtools()
        if 新版本:
            try:
                xmin, xmax, ymin, ymax = path_alt.bbox()
                return xmin, xmax, ymin, ymax
            except:
                return self.获取路径点列表范围()
        else:
            return self.获取路径点列表范围()

    def 获取线段点坐标(self, 线段索引, 位置):
        """
        获取路径上指定线段的指定位置的坐标
        @param 线段索引:
        @param 位置:
        @return:
        """
        path_alt = self._conv_svgpathtools()
        segment = path_alt[线段索引]
        if 位置 == 0:
            pt = segment.start
        elif 位置 == 1:
            pt = segment.end
        elif 位置 > 0 and 位置 < 1:
            pt = segment.point(位置)
        return pt.real, pt.imag

    def 获取路径点坐标(self, 位置):
        """
        获取路径上指定位置的坐标
        @param 位置:
        @return:
        """
        path_alt = self._conv_svgpathtools()
        if 位置 == 0:
            pt = path_alt.start
        elif 位置 == 1:
            pt = path_alt.end
        elif 位置 > 0 and 位置 < 1:
            pt = path_alt.point(位置)
        return pt.real, pt.imag

    def 获取路径d(self):
        import svgpathtools
        P = self.获取属性值
        原生path = P("原生path", None)
        if 原生path is not None:
            return svgpathtools.Path(原生path).d()

        点列表 = P("点列表")
        if len(点列表) == 0:
            return "M0,0 L0,0 z"
        点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)
        d_list = 神笔绘图板工具.点列表转SVG路径(点列表)
        return " ".join(d_list)

    def 位置坐标_old(self, 位置比, 段索引=-1):
        import svgpathtools
        d = self.获取路径d()
        path = svgpathtools.Path(d)
        if isinstance(位置比, list) or isinstance(位置比, tuple):
            if 段索引 >= 0:
                pos = [path[段索引].point(p) for p in 位置比]
            else:
                pos = [path.point(p) for p in 位置比]
            return [(pt.real, pt.imag) for pt in pos]
        if 段索引 >= 0:
            point = path[段索引].point(位置比)
        else:
            point = path.point(位置比)
        return point.real, point.imag

    def _计算两点距离(self, p1, p2):
        """计算两个复数坐标点之间的欧氏距离"""
        dx = p2.real - p1.real
        dy = p2.imag - p1.imag
        return math.hypot(dx, dy)

    def 路径高密度采样(self, path, 采样精度=1000):
        """
        对路径进行高密度采样，返回采样点列表和累计弧长列表
        :param path: svgpathtools.Path对象
        :return: (采样点坐标列表, 累计弧长列表)
        """
        from svgpathtools import Line, CubicBezier, QuadraticBezier, Arc
        采样点列表 = []
        累计弧长列表 = [0.0]  # 第一个点弧长为0
        # self.采样精度 = 1000  # 采样点数量，值越大精度越高（1000足够日常使用）
        总采样数 = 采样精度

        # 1. 遍历每个路径段，按段长比例分配采样点（保证采样均匀）
        各段长度 = []
        for seg in path:
            if isinstance(seg, (Line, CubicBezier, QuadraticBezier, Arc)):
                各段长度.append(seg.length())
            else:
                各段长度.append(0.0)
        总长度 = sum(各段长度)

        if 总长度 == 0:
            # 空路径返回第一个点
            if len(path) > 0:
                first_point = path[0].point(0.0)
                采样点列表.append((first_point.real, first_point.imag))
            return 采样点列表, 累计弧长列表

        # 2. 对每个段分配采样点并采样
        累计长度 = 0.0
        for 段索引, seg in enumerate(path):
            段长度 = 各段长度[段索引]
            if 段长度 == 0:
                continue

            # 按段长比例分配采样点数量
            段采样数 = max(2, int(总采样数 * (段长度 / 总长度)))
            段采样点 = []

            # 对当前段进行均匀采样（t从0到1）
            for i in range(段采样数):
                t = i / (段采样数 - 1)
                point = seg.point(t)
                段采样点.append((point.real, point.imag))

            # 计算当前段内的累计弧长并合并到总列表
            for i in range(1, len(段采样点)):
                距离 = self._计算两点距离(
                    complex(*段采样点[i - 1]),
                    complex(*段采样点[i])
                )
                累计长度 += 距离
                累计弧长列表.append(累计长度)

            # 合并采样点（避免重复添加第一个点）
            if 采样点列表:
                采样点列表.extend(段采样点[1:])
            else:
                采样点列表.extend(段采样点)

        return 采样点列表, 累计弧长列表

    def 按弧长插值找坐标(self, 采样点列表, 累计弧长列表, 目标比例):
        """
        根据采样点和累计弧长，插值计算目标比例的坐标
        :param 采样点列表: 路径采样点坐标[(x1,y1), (x2,y2), ...]
        :param 累计弧长列表: 对应采样点的累计弧长[0, l1, l2, ...]
        :param 目标比例: 0~1的浮点数
        :return: (x, y) 坐标
        """
        if not 采样点列表 or len(累计弧长列表) < 2:
            return (0.0, 0.0) if not 采样点列表 else 采样点列表[0]

        总弧长 = 累计弧长列表[-1]
        if 总弧长 == 0:
            return 采样点列表[0]

        # 计算目标弧长
        目标弧长 = 总弧长 * 目标比例

        # 边界情况：比例超过1或小于0
        if 目标弧长 <= 0:
            return 采样点列表[0]
        if 目标弧长 >= 总弧长:
            return 采样点列表[-1]

        # 找到目标弧长所在的区间
        for i in range(1, len(累计弧长列表)):
            if 累计弧长列表[i] >= 目标弧长:
                # 找到前后两个点
                前弧长 = 累计弧长列表[i - 1]
                后弧长 = 累计弧长列表[i]
                前点 = 采样点列表[i - 1]
                后点 = 采样点列表[i]

                # 计算插值比例
                插值比例 = (目标弧长 - 前弧长) / (后弧长 - 前弧长)

                # 线性插值计算坐标
                x = 前点[0] + 插值比例 * (后点[0] - 前点[0])
                y = 前点[1] + 插值比例 * (后点[1] - 前点[1])
                return (x, y)

        return 采样点列表[-1]

    def 位置坐标(self, 位置比, 段索引=-1, 采样精度=1000):
        """
        最终优化版：高密度采样+线性插值，获取路径上准确的坐标
        :param 位置比: 0~1的浮点数，或列表/元组（多个比例）
        :param 段索引: 指定路径段（-1表示整个路径）
        :return: 坐标(x,y)或坐标列表
        """
        import svgpathtools
        from svgpathtools.path import Path
        d = self.获取路径d()
        path = svgpathtools.Path(d)

        # 处理指定单段的情况
        if 段索引 >= 0 and 段索引 < len(path):
            单段路径 = Path(path[段索引])
            采样点, 累计弧长 = self.路径高密度采样(单段路径, 采样精度=采样精度)
        else:
            采样点, 累计弧长 = self.路径高密度采样(path, 采样精度=采样精度)

        # 处理多个位置比
        if isinstance(位置比, (list, tuple)):
            return [self.按弧长插值找坐标(采样点, 累计弧长, p) for p in 位置比]

        # 处理单个位置比
        return self.按弧长插值找坐标(采样点, 累计弧长, 位置比)

    def 构建SVG元素(self):
        from svgpathtools.path import scale, translate, rotate
        import svgpathtools
        path_d = self.获取路径d()
        P = self.获取属性值
        缩放列表 = P("坐标缩放", None)
        if 缩放列表 is not None:
            path_ = svgpathtools.Path(path_d)
            for 缩放 in 缩放列表:
                缩放X, 缩放Y, 缩放中心点 = 缩放
                path_ = scale(path_, 缩放X, 缩放Y, 缩放中心点)
            path_d = path_.d()

        平移列表 = P("坐标平移", None)
        if 平移列表 is not None:
            path_ = svgpathtools.Path(path_d)
            for 平移 in 平移列表:
                平移X, 平移Y = 平移
                path_ = translate(path_, complex(平移X, 平移Y))
                # path_d = translate(svgpathtools.Path(path_d), complex(平移X, 平移Y)).d()
            path_d = path_.d()

        旋转列表 = P("坐标旋转", None)
        if 旋转列表 is not None:
            path_ = svgpathtools.Path(path_d)
            for 旋转 in 旋转列表:
                旋转角度, 旋转中心点 = 旋转
                path_ = rotate(path_, 旋转角度, 旋转中心点)
                # path
            path_d = path_.d()
            # 旋转角度, 旋转中心点 = 旋转
            # if 旋转中心点 is not None:
            #     path_d = rotate(svgpathtools.Path(path_d), 旋转角度, 旋转中心点).d()
            # else:
            #     path_d = rotate(svgpathtools.Path(path_d), 旋转角度).d()
        # 路径偏移 = P("路径偏移", None)
        # if 路径偏移 is not None:
        #     import svgpathtools
        #     path_ = svgpathtools.Path(path_d)
        #     path_ = self._offset_curve(path_, 路径偏移)
        #     path_d = path_.d()

        if P("闭合", 否):
            path_d += 'Z'

        path = self.dwg.path(d=path_d,
                             shape_rendering='auto',
                             id=self.获取元素id(t="p"))

        样式可修改元素.属性修改处理(self, path)
        可变换元素.属性修改处理(self, path)
        return path

    def _offset_curve(self, path, offset_distance, steps=1000):
        """Takes in a Path object, `path`, and a distance,
        `offset_distance`, and outputs an piecewise-linear approximation
        of the 'parallel' offset curve."""
        from svgpathtools import parse_path, Line, Path, wsvg
        nls = []
        for seg in path:
            ct = 1
            for k in range(steps):
                t = k / steps
                offset_vector = offset_distance * seg.normal(t)
                nl = Line(seg.point(t), seg.point(t) + offset_vector)
                nls.append(nl)
        connect_the_dots = [Line(nls[k].end, nls[k + 1].end) for k in range(len(nls) - 1)]
        if path.isclosed():
            connect_the_dots.append(Line(nls[-1].end, nls[0].end))
        offset_path = Path(*connect_the_dots)
        return offset_path

    def _坐标缩放(self, 缩放X, 缩放Y=None, 缩放中心点=None):
        from svgpathtools.path import scale
        if 缩放Y is None:
            缩放Y = 缩放X
        path = self._conv_svgpathtools()
        if 缩放中心点 is None:
            缩放中心点 = 0j
        path = scale(path, 缩放X, 缩放Y, 缩放中心点)
        self.元素属性["原生path"] = path.d()
        return self

    def _坐标平移(self, 位移X, 位移Y=None):
        from svgpathtools.path import translate
        if 位移Y is None:
            位移Y = 位移X
        path = self._conv_svgpathtools()
        path = translate(path, complex(位移X, 位移Y))
        self.元素属性["原生path"] = path.d()
        return self

    def _坐标旋转(self, 旋转角度, 旋转中心点=None):
        from svgpathtools.path import rotate
        path = self._conv_svgpathtools()
        if 旋转中心点 is not None:
            旋转中心点 = complex(旋转中心点[0], 旋转中心点[1])
        path = rotate(path, 旋转角度, 旋转中心点)
        self.元素属性["原生path"] = path.d()
        return self

    def 复制(self) -> "路径元素":
        路径_ = 路径元素(self.高清图, self.高清图.默认组)
        for p in self.元素属性:
            路径_.设置属性值(p, self.元素属性[p])
        return 路径_

    def _构建SVG元素_delete(self):
        P = self.获取属性值
        C = self.获取颜色值

        原生path = P("原生path", None)
        if 原生path is None:
            点列表 = P("点列表")
            点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)

            if len(点列表) == 0:
                path = self.dwg.path(d="M0,0 L0,0 z",
                                     shape_rendering='auto',
                                     id=self.获取元素id(t="p"))

                样式可修改元素.属性修改处理(self, path)
                可变换元素.属性修改处理(self, path)
                return path

            fp = 点列表[0]
            if fp[0] in ["M", "m"]:
                t, x, y = fp
            elif len(fp) == 2:
                t, x, y = "M", fp[0], fp[1]
            else:
                t, x, y = "M", 0, 0
                点列表 = [(t, x, y)] + 点列表

            path = self.dwg.path(d="{}{:.2f},{:.2f} ".format(t, float(x), float(y)),
                                 shape_rendering='auto',
                                 id=self.获取元素id(t="p"))

            d_list = 神笔绘图板工具.点列表转SVG路径(点列表)

            for di in d_list[1:]:
                if di[0] == "z":
                    path.push('Z')
                    continue
                path.push(di)

            if P("闭合", 否):
                path.push('Z')

            from svgpathtools import parse_path
            path_d_str = " ".join(path.commands)
            path_d = parse_path(path_d_str)
            path = self.dwg.path(d=path_d,
                                 shape_rendering='auto',
                                 id=self.获取元素id(t="p"))

        else:
            from svgpathtools import parse_path
            原生path = parse_path(原生path).d()
            path = self.dwg.path(d=原生path,
                                 shape_rendering='auto',
                                 id=self.获取元素id(t="p"))

        样式可修改元素.属性修改处理(self, path)
        可变换元素.属性修改处理(self, path)

        return path


def 路径合并测试():
    from 神笔码靓.神笔库 import 神笔绘图板

    神笔 = 神笔绘图板(作品文件路径="路径合并.svg")
    y = 神笔.高 / 2
    圆 = 神笔.符号.圆(中心点=(神笔.宽 / 2, y + 2), 半径=6)
    神笔.符号.叉(中心点=(神笔.宽 / 2, y + 18), 线长=12).合并路径(圆, 是).落笔(100, 100). \
        画直线(50, 50).画水平线(200).画垂直线(300).平滑的二次贝塞尔曲线((100, 100)).平滑的二次贝塞尔曲线((90, 200))
    神笔.完成()


def 偏转直行():
    from 神笔码靓.神笔库 import 神笔绘图板
    神笔 = 神笔绘图板(作品文件路径="偏转直行.svg")
    路径 = 神笔.路径(id_="路径").移动到(300, 100).画垂直线(200).画直线(400, 200).画垂直线(400).画水平线(100).画直线(300,
                                                                                                                    300)
    for i in range(10):
        路径.右转直线(90, 20).左转直线(90, 20)

    路径.画垂直线(100).右转直线(45, 20).左转直线(45, 20).画直线(100, 500)  # .画圆((0,0),100)

    for i in range(10):
        路径.右转直线(-140, 20).左转直线(-140, 20)

    路径.新描边样式("3,3", id_="新路径").画直线(100, 100).寻找路径(id_="路径").画直线(0, 0)
    神笔.完成()


def 偏转直行画放射线():
    from 神笔码靓.神笔库 import 神笔绘图板
    神笔 = 神笔绘图板(作品文件路径="偏转直行画放射线.svg")
    路径 = 神笔.路径(id_="路径")

    for i in range(0, 180):
        路径 = 路径.新路径().描边宽度(0.5).移动到(300, 300).右转直线(i * 2, 50).描边颜色(颜色.随机色()). \
            右转直线(10, 10).右转直线(-10, 10)
    神笔.完成()


def 综合测试():
    from 神笔码靓.神笔库 import 神笔绘图板
    绘图板 = 神笔绘图板(作品文件路径="路径综合测试.svg")
    A = (100, 200)
    B = (400, 200)
    绘图板.路径().点辅助开关(开).移动到(A).画直线(B).点辅助(开启=否).平滑曲线(终点控制点=(110, 90),
                                                                              终点=(110, 220)).前进直线(100).点辅助(
        开启=是) \
        .画垂直线(400).点辅助(开启=是).画曲线(开始控制点=(110, 500), 终点控制点=(32, 500), 终点=(45, 600)).点辅助(
        开启=是).前进直线(20).点辅助(开启=是) \
        .二次贝塞尔曲线(曲线控制点=(100, 800), 终点=(200, 500)).点辅助(开启=是) \
        .平滑的二次贝塞尔曲线(终点=(300, 200)).点辅助(开启=是).平滑的二次贝塞尔曲线(终点=(320, 180)).点辅助(开启=是) \
        .右转直线(6, 120).点辅助(开启=是).画圆弧(3, (450, 104), 圆弧方向=1).前进直线(20)
    绘图板.完成()


def 画圆弧求斜率测试():
    from 神笔码靓.神笔库 import 神笔绘图板
    绘图板 = 神笔绘图板(作品文件路径="画圆弧求斜率测试.svg")
    A = (100, 200)
    B = (400, 200)
    绘图板.路径().点辅助开关(开).移动到(A).画直线(B).画圆弧(200, (400, 400), 圆弧方向=0).前进直线(150)

    绘图板.完成()


if __name__ == '__main__':
    # 路径合并测试()
    # 偏转直行()
    # 综合测试()
    画圆弧求斜率测试()
