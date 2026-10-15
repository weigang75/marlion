# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import svgwrite
from typing import Optional, Tuple
from 神笔码靓.神笔库.动画工具集 import 缩放动画关键帧, 旋转动画关键帧, 倾斜动画关键帧, 平移动画关键帧
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.通用工具集 import *


@dataclass
class 元素位置信息:
    最小x: [float, int] = 0
    最小y: [float, int] = 0
    最大x: [float, int] = 0
    最大y: [float, int] = 0
    # 自定义的中心点
    中心点 = None

    @property
    def 中心x(self):
        if isinstance(self.中心点, tuple):
            return self.中心点[0]
        return (self.最小x + self.最大x) / 2

    @property
    def 中心y(self):
        if isinstance(self.中心点, tuple):
            return self.中心点[1]
        return (self.最小y + self.最大y) / 2

    @property
    def 宽(self):
        return self.最大x - self.最小x

    @property
    def 高(self):
        return self.最大y - self.最小y

    def __str__(self):
        return f"x:{self.最小x:.2f}~{self.最大x:.2f}  y:{self.最小y:.2f}~{self.最大y:.2f};\n" \
               f"中点:{self.中心x:.2f}, {self.中心y:.2f}  宽:{self.宽} 高:{self.高}"


class 元素:
    _id_no = 0
    元素缓存 = {}

    数值精确度 = 2
    数值精确度的属性 = ["x", "y", "cx", "cy"]

    @staticmethod
    def 元素缓存清除():
        元素.元素缓存 = {}

    # z_orders = []
    @staticmethod
    def 重置ID():
        元素._id_no = 0

    def 克隆(self):
        import copy
        新元素 = copy.deepcopy(self)
        新元素.svg_element = None
        新元素.设置id(元素.生成元素id(t="clone"))
        # 所属组 = 新元素.所属组
        # 所属组.remove(新元素)
        # 所属组.append(self)
        # self.高清图.默认组.remove(self)
        # self.高清图.默认组.append(self)
        self.高清图.默认组.append(新元素)
        return 新元素

    def 设置id(self, id_):
        if id_ is None:
            return self
        old_id = self.获取属性值("id_", None)
        if old_id is not None:
            if old_id == id_:
                return self
            if self.高清图.获取元素(old_id) == self:
                if old_id in self.高清图.元素字典:
                    del self.高清图.元素字典[old_id]
        self.设置属性值("id_", id_)
        self.高清图.元素字典[id_] = self
        return self

    def __init__(self, 高清图, 所属组: list):
        from 神笔码靓.神笔库.变换工具集 import 变换工具集
        from 神笔码靓.神笔库.样式工具集 import 样式工具集
        from 神笔码靓.神笔库.滤镜工具集 import 滤镜工具集
        from 神笔码靓.神笔库.动画工具集 import 动画工具集
        from 神笔码靓.神笔库 import 神笔绘图板

        self.svg_element = None
        self.元素属性 = {}
        self.元素附加属性 = {}
        self.元素处理列表 = []
        self.已有缓存 = 否
        self._不生成ID = False

        self.所属组 = 所属组
        self.所属组.append(self)

        self.dwg: svgwrite.Drawing = 高清图.dwg

        self.高清图: 神笔绘图板 = 高清图
        # ---------- 修改点1：实例化滤镜工具集并赋值给 self.滤镜 ----------
        self.滤镜: 滤镜工具集 = 滤镜工具集(高清图)
        self.样式: 样式工具集 = 高清图.样式
        self.变换: 变换工具集 = 高清图.变换
        self.动画: 动画工具集 = 高清图.动画

        # ---------- 新增：用于存储滤镜操作列表 ----------
        self._滤镜操作列表 = []

    def 不生成ID(self):
        self._不生成ID = True
        return self

    def 创建组合(self, class_name: str = None, style=None,
                 样式类名: str = None, 样式串: str = None, id_: str = None):
        return self.高清图.创建组合(元素列表=[self], class_name=class_name, style=class_name,
                                    样式类名=样式类名, 样式串=样式串, id_=id_)

    def 创建模板(self, class_name: str = None, style=None,
                 样式类名: str = None, 样式串: str = None, id_: str = None):
        return self.高清图.创建模板(元素列表=[self], class_name=class_name, style=class_name,
                                    样式类名=样式类名, 样式串=样式串, id_=id_)

    def 添加到列表(self, 元素列表: list):
        if self not in 元素列表:
            元素列表.append(self)
        return self

    def 置前(self):
        # self.高清图.创建组合(元素列表=[self])
        self.所属组.remove(self)
        self.所属组.append(self)
        # 元素.z_orders.append(self)
        return self

    # region 动画

    def 透明动画(self, 透明度循环集=[0.5, 1.0, 0.5], 持续时间: [float, int] = 1, 重复次数: int = None,
                 填充行为="remove", id_: str = None):
        self.元素处理预设(self.动画.透明, {
            "透明度循环集": 透明度循环集, "持续时间": 持续时间, "重复次数": 重复次数, "填充行为": 填充行为, "id_": id_
        })
        return self

    def 虚线流动画(self, 方向: int = 1, 持续时间: [float, int] = 3, 周期: [float, int] = None,
                   重复次数: int = None, 填充行为="remove", id_: str = None):
        """
        @param 方向:
        @param 持续时间:
        @param 周期:
        @param 重复次数:
        @param 填充行为:
        @return:
        """
        self.元素处理预设(self.动画.虚线流, {
            "方向": 方向, "持续时间": 持续时间, "周期": 周期, "重复次数": 重复次数, "填充行为": 填充行为, "id_": id_
        })
        return self

    # def 自旋转(self, 旋转角度: float):  不支持
    #     self.设置属性值("自旋转", 旋转角度)
    #     return self

    def 平移动画(self, 开始时间=0, 持续时间=3,
                 起点X=0, 起点Y=0, 终点X=0, 终点Y=-2000, 重复次数=None, 填充行为="freeze",
                 关键帧列表: list[平移动画关键帧] = [], id_: str = None):
        """
        [使用样例]
        from 神笔码靓.神笔库.动画工具集 import 平移动画关键帧
        关键帧列表 = 列表()
        关键帧列表.添加元素(平移动画关键帧(时间点=0, 位置X=90, 位置Y=0))
        关键帧列表.添加元素(平移动画关键帧(时间点=0.8, 位置X=20, 位置Y=10))
        关键帧列表.添加元素(平移动画关键帧(时间点=1, 位置X=90, 位置Y=30))
        :param 开始时间: 指定动画开始的时间。可以是具体的时间值，也可以是一些特殊的值如"点击"或"鼠标悬停"等。
        :param 持续时间: 指定动画的持续时间，以秒为单位。
        :param 起点X: 指定变换的起始值。
        :param 起点Y: 指定变换的起始值。
        :param 终点X: 指定变换的结束值。
        :param 终点Y: 指定变换的结束值。
        :param 重复次数: 指定动画的重复次数。可以是具体的次数，也可以是"indefinite"表示无限次
        :param 填充行为: 指定动画的填充行为。可以是"remove"表示动画结束后还原到初始状态，也可以是"freeze"表示结束后保留动画最后的状态
        :return:
        """
        self.元素处理预设(self.动画.平移, {
            "开始时间": 开始时间, "持续时间": 持续时间, "起点X": 起点X, "起点Y": 起点Y,
            "终点X": 终点X, "终点Y": 终点Y, "重复次数": 重复次数, "填充行为": 填充行为, "关键帧列表": 关键帧列表,
            "id_": id_
        })
        return self

    def 轨迹移动动画(self, 路径点列表, 开始时间=0, 持续时间=3, 重复次数=None, 旋转=None, 填充行为="remove",
                     id_: str = None):
        """
        @param 路径点列表:
        @param 开始时间:
        @param 持续时间:
        @param 重复次数:
        @param 旋转: 自动旋转(auto),自动反向旋转(auto-reverse),固定角度值(如45deg、0),相对角度值(如rotate="+90deg")
        @param 填充行为:
        @return:
        """
        self.元素处理预设(self.动画.轨迹移动, {
            "开始时间": 开始时间, "持续时间": 持续时间, "路径点列表": 路径点列表, "重复次数": 重复次数,
            "旋转": 旋转, "填充行为": 填充行为, "id_": id_
        })
        return self

    def 旋转动画(self, 开始时间=0, 持续时间=3,
                 起始角=0, 起始旋转中心点=(0, 0), 结束角=360, 结束旋转中心点=None, 重复次数=None, 填充行为="remove",
                 关键帧列表: list[旋转动画关键帧] = [], id_: str = None):
        """
        [使用样例]
        from 神笔码靓.神笔库.动画工具集 import 旋转动画关键帧
        关键帧列表 = 列表()
        关键帧列表.添加元素(旋转动画关键帧(时间点=0, 旋转角=90, 旋转中心点=(0, 0)))
        关键帧列表.添加元素(旋转动画关键帧(时间点=0.8, 旋转角=20, 旋转中心点=(0, 0)))
        关键帧列表.添加元素(旋转动画关键帧(时间点=1, 旋转角=90, 旋转中心点=(0, 0)))
        :param 开始时间:
        :param 持续时间:
        :param 起始角:
        :param 起始旋转中心点:
        :param 结束角:
        :param 结束旋转中心点:
        :param 重复次数:
        :param 填充行为:
        :param 关键帧列表:
        :return:
        """
        if 起始旋转中心点 is None:
            起始旋转中心点 = (0, 0)
        if 结束旋转中心点 is None:
            结束旋转中心点 = 起始旋转中心点
        self.元素处理预设(self.动画.旋转, {
            "开始时间": 开始时间, "持续时间": 持续时间, "起始角": 起始角, "起始旋转中心点": 起始旋转中心点,
            "结束角": 结束角, "结束旋转中心点": 结束旋转中心点, "重复次数": 重复次数, "填充行为": 填充行为,
            "关键帧列表": 关键帧列表, "id_": id_
        })
        return self

    def 加速旋转动画(
            self,
            旋转中心点: Tuple[float, float],
            加速分段数量: int = 20,
            开始时间: float = 0.0,
            开始一圈时长: float = 0.5,
            末尾段循环次数: Optional[int] = None,
            # 两种配置格式二选一：
            # 1.相对进度模式：[(进度阈值0~1, 衰减系数)] 适配任意分段【推荐默认】
            # 2.绝对序号模式：[(序号阈值, 衰减系数)] 复刻原始硬编码i判断逻辑
            加速区间配置=None,
            # 安全下限：防止持续时间过小，浏览器丢弃动画
            最小一圈时长: float = 0.001,
            id前缀=None,
            控制台输出=True
    ):
        """
        通用渐进加速旋转SVG动画，自动适配【个位数分段 / 数千超大分段】
        两种加速配置模式，按需切换，内置时长防坍缩保护

        :param 旋转中心点: 旋转圆心 (cx, cy)
        :param 加速分段数量: 动画拆分总段数，支持5 ~ 3000大范围
        :param 开始时间: 首段动画启动时刻(秒)
        :param 开始一圈时长: 初始旋转一圈耗时
        :param 末尾段循环次数: int=有限循环次数; None=SVG无限循环indefinite
        :param 加速区间配置:
            默认配置 = 自动复刻原始代码加速曲线(适配任意分段)
            【相对进度模式】示例 [(0.005,0.9), (0.015,0.95), (1.0,0.999)]
            【绝对序号模式】示例 [(10,0.9), (30,0.95), (float("inf"),0.999)]
        :param 最小一圈时长: 一圈耗时下限，避免时长趋近0导致动画失效
        """
        if 控制台输出 and id前缀:
            js_func = """
function rotateAnimListener(animId){
    const anim = document.getElementById(animId);
    // 动画【正式开始播放】触发
    anim.addEventListener('beginEvent', function(e) {
      console.log('动画启动:', e);
    });
    // 动画播放完成触发
    anim.addEventListener('endEvent', function(e) {
      console.log('动画结束:', e);
    });
}
"""
        else:
            js_func = None
        # ========== 默认配置：将原版i<10,i<30转化为相对进度，通用所有分段 ==========
        if 加速区间配置 is None:
            # 原始拐点序号：10、30，换算成相对进度
            拐点1 = 10 / 加速分段数量
            拐点2 = 30 / 加速分段数量
            加速区间配置 = [
                (拐点1, 0.9),
                (拐点2, 0.95),
                (1.00, 0.999)
            ]

        当前起始时刻 = 开始时间
        当前一圈耗时 = 开始一圈时长
        cx, cy = 旋转中心点
        js = ""
        for 分段序号 in range(加速分段数量):
            # 还原原版重复次数计算公式
            if 分段序号 >= 加速分段数量 - 1:
                本段循环 = 末尾段循环次数
            else:
                本段循环 = int((分段序号 / 500) + 1)

            if id前缀 is None:
                id_ = None
            else:
                id_ = f"旋转动画_{id前缀}_{分段序号 + 1}"

            if 控制台输出 and id前缀:
                js += f'rotateAnimListener("{id_}");\n'

            # 生成一段旋转动画
            self.旋转动画(
                开始时间=当前起始时刻,
                持续时间=当前一圈耗时,
                结束角=360,
                起始旋转中心点=(cx, cy),
                重复次数=本段循环,
                id_=id_,
            )

            # 无限循环：不再生成后续分段，直接退出
            if 本段循环 is None:
                break
            # 更新下一段起始时间
            当前起始时刻 += 当前一圈耗时 * 本段循环

            # =========自动识别配置模式：区分【进度阈值 / 绝对序号阈值】=========
            选中系数 = None
            阈值, _ = 加速区间配置[0]
            if isinstance(阈值, float) and 0 <= 阈值 <= 1.0:
                # 模式A：相对进度匹配（通用模式）
                当前进度 = 分段序号 / 加速分段数量
                for 阈值, 系数 in 加速区间配置:
                    if 当前进度 < 阈值:
                        选中系数 = 系数
                        break
            else:
                # 模式B：绝对序号匹配（兼容原版旧逻辑）
                for 阈值, 系数 in 加速区间配置:
                    if 分段序号 < 阈值:
                        选中系数 = 系数
                        break

            # 衰减时长 + 强制下限保护，解决超大分段动画提前停止的核心BUG
            当前一圈耗时 = max(当前一圈耗时 * 选中系数, 最小一圈时长)
        if 控制台输出 and id前缀:
            js = js_func + js
            self.高清图.增加JS代码(js)
        return self

    def 缩放动画(self, 开始时间=0, 持续时间=3,
                 开始缩放X=1, 开始缩放Y=1, 结束缩放X=-2, 结束缩放Y=2, 重复次数=None, 填充行为="remove",
                 关键帧列表: list[缩放动画关键帧] = [], id_: str = None):
        """
        [使用样例]
        from 神笔码靓.神笔库.动画工具集 import 缩放动画关键帧
        关键帧列表 = 列表()
        关键帧列表.添加元素(缩放动画关键帧(时间点=0, 缩放X=1, 缩放Y=2))
        关键帧列表.添加元素(缩放动画关键帧(时间点=0.8, 缩放X=2, 缩放Y=1))
        关键帧列表.添加元素(缩放动画关键帧(时间点=1, 缩放X=1, 缩放Y=2))
        :param 开始时间:
        :param 持续时间:
        :param 开始缩放X:
        :param 开始缩放Y:
        :param 结束缩放X:
        :param 结束缩放Y:
        :param 重复次数:
        :param 填充行为:
        :param 关键帧列表:
        :return:
        """
        self.元素处理预设(self.动画.缩放, {
            "开始时间": 开始时间, "持续时间": 持续时间,
            "开始缩放X": 开始缩放X, "开始缩放Y": 开始缩放Y, "结束缩放X": 结束缩放X, "结束缩放Y": 结束缩放Y,
            "重复次数": 重复次数, "填充行为": 填充行为, "关键帧列表": 关键帧列表, "id_": id_
        })
        return self

    def 倾斜X动画(self, 开始时间=0, 持续时间=3, 起始倾斜角=0, 结束倾斜角=45, 重复次数=None, 填充行为="remove",
                  关键帧列表: list[倾斜动画关键帧] = [], id_: str = None):
        """
        [使用样例]
        from 神笔码靓.神笔库.动画工具集 import 倾斜动画关键帧
        关键帧列表 = 列表()
        关键帧列表.添加元素(倾斜动画关键帧(时间点=0, 倾斜角=90))
        关键帧列表.添加元素(倾斜动画关键帧(时间点=0.8, 倾斜角=20))
        关键帧列表.添加元素(倾斜动画关键帧(时间点=1, 倾斜角=90))
        :param 开始时间:
        :param 持续时间:
        :param 起始倾斜角:
        :param 结束倾斜角:
        :param 重复次数:
        :param 填充行为:
        :param 关键帧列表:
        :return:
        """
        self.元素处理预设(self.动画.倾斜X, {
            "开始时间": 开始时间, "持续时间": 持续时间, "起始倾斜角": 起始倾斜角, "结束倾斜角": 结束倾斜角,
            "重复次数": 重复次数, "填充行为": 填充行为, "关键帧列表": 关键帧列表, "id_": id_
        })
        return self

    def 倾斜Y动画(self, 开始时间=0, 持续时间=3, 起始倾斜角=0, 结束倾斜角=45, 重复次数=None, 填充行为="remove",
                  关键帧列表: list[倾斜动画关键帧] = [], id_: str = None):
        """
        [使用样例]
        from 神笔码靓.神笔库.动画工具集 import 倾斜动画关键帧
        关键帧列表 = 列表()
        关键帧列表.添加元素(倾斜动画关键帧(时间点=0, 倾斜角=90))
        关键帧列表.添加元素(倾斜动画关键帧(时间点=0.8, 倾斜角=20))
        关键帧列表.添加元素(倾斜动画关键帧(时间点=1, 倾斜角=90))

        :param 开始时间:
        :param 持续时间:
        :param 起始倾斜角:
        :param 结束倾斜角:
        :param 重复次数:
        :param 填充行为:
        :param 关键帧列表:
        :return:
        """
        self.元素处理预设(self.动画.倾斜Y, {
            "开始时间": 开始时间, "持续时间": 持续时间, "起始倾斜角": 起始倾斜角, "结束倾斜角": 结束倾斜角,
            "重复次数": 重复次数, "填充行为": 填充行为, "关键帧列表": 关键帧列表, "id_": id_
        })
        return self

    # endregion 动画

    def 更换组(self, 组: list):
        if self.所属组 is 组:
            return

        if self.所属组 is not 空:
            self.所属组.remove(self)

        组.append(self)

    def 中心点计算(self, 元素位置: 元素位置信息):
        元素位置.中心点 = 元素位置.中心x, 元素位置.中心y
        return 元素位置.中心点

    def 获取元素范围(self):
        raise NotImplementedError("请实现 获取元素范围")

    def 获取元素列表范围(self, 属性名="元素列表"):
        P = self.获取属性值
        元素列表 = P(属性名)

        最小x = float('inf')
        最小y = float('inf')
        最大x = float('-inf')
        最大y = float('-inf')

        for 元素_ in 元素列表:
            最小x_, 最小y_, 最大x_, 最大y_ = 元素_.获取元素范围()

            if 最小x_ < 最小x:
                最小x = 最小x_

            if 最小y_ < 最小y:
                最小y = 最小y_

            if 最大x_ > 最大x:
                最大x = 最大x_

            if 最大y_ > 最大y:
                最大y = 最大y_

        return 最小x, 最小y, 最大x, 最大y

    def 获取路径点列表(self, 属性名="点列表"):
        P = self.获取属性值

        点列表 = P(属性名)
        路径点列表 = []
        from 神笔码靓.神笔库 import 神笔绘图板工具
        点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)

        # ['M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'C', 'c', 'S', 's', 'Q', 'q', 'T', 't', 'A', 'a', 'Z', 'z']
        for 点 in 点列表:
            if 点[0] in ["M", "m", "L", "l", "T", "t"]:
                顶点x, 顶点y = 点[1], 点[2]
            elif 点[0] in ["C", "c"]:
                # (x1, y1), (x2, y2), (x, y)
                顶点x, 顶点y = 点[5], 点[6]
            elif 点[0] in ["H", "h"]:
                顶点x = 点[1]
            elif 点[0] in ["V", "v"]:
                顶点y = 点[1]
            elif 点[0] in ["Q", "q", "S", "s"]:
                # (x1, y1), (x, y)
                顶点x, 顶点y = 点[3], 点[4]
            elif 点[0] in ["A", "a"]:
                # (rx, ry), x_axis_rotation, (large_arc_flag, sweep_flag), (x, y) =
                顶点x, 顶点y = 点[6], 点[7]
            elif 点[0] in ["Z", "z"]:
                pass
            else:
                顶点x, 顶点y = 点[0], 点[1]
            路径点列表.append((顶点x, 顶点y))

        return 路径点列表

    def 获取路径点列表范围(self, 属性名="点列表"):
        P = self.获取属性值

        点列表 = P(属性名)

        最小x = float('inf')
        最小y = float('inf')
        最大x = float('-inf')
        最大y = float('-inf')

        from 神笔码靓.神笔库 import 神笔绘图板工具
        点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)

        # ['M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'C', 'c', 'S', 's', 'Q', 'q', 'T', 't', 'A', 'a', 'Z', 'z']
        for 点 in 点列表:
            if 点[0] in ["M", "m", "L", "l", "T", "t"]:
                顶点x, 顶点y = 点[1], 点[2]
            elif 点[0] in ["C", "c"]:
                # (x1, y1), (x2, y2), (x, y)
                顶点x, 顶点y = 点[5], 点[6]
            elif 点[0] in ["H", "h"]:
                顶点x = 点[1]
            elif 点[0] in ["V", "v"]:
                顶点y = 点[1]
            elif 点[0] in ["Q", "q", "S", "s"]:
                # (x1, y1), (x, y)
                顶点x, 顶点y = 点[3], 点[4]
            elif 点[0] in ["A", "a"]:
                # (rx, ry), x_axis_rotation, (large_arc_flag, sweep_flag), (x, y) =
                顶点x, 顶点y = 点[6], 点[7]
            elif 点[0] in ["Z", "z"]:
                pass
            else:
                顶点x, 顶点y = 点[0], 点[1]

            if 顶点x < 最小x:
                最小x = 顶点x
            if 顶点x > 最大x:
                最大x = 顶点x
            if 顶点y < 最小y:
                最小y = 顶点y
            if 顶点y > 最大y:
                最大y = 顶点y

        return 最小x, 最小y, 最大x, 最大y

    def 获取位置信息(self) -> 元素位置信息:
        scale_x, scale_y, translate_x, translate_y = self.获取缩放平移值()
        最小x, 最小y, 最大x, 最大y = self.获取元素范围()

        元素位置_ = 元素位置信息(最小x=最小x * scale_x + translate_x, 最小y=最小y * scale_y + translate_y,
                                 最大x=最大x * scale_x + translate_x, 最大y=最大y * scale_y + translate_y)
        元素位置_.中心点 = self.中心点计算(元素位置_)
        return 元素位置_

    # region 元素属性
    def 设置属性值(self, 属性名, 属性值):
        self.元素属性[属性名] = 属性值
        return self

    def 清除属性值(self, 属性名):
        if 属性名 in self.元素属性:
            del self.元素属性[属性名]
        return self

    def 设置样式(self, 样式):
        if 为空(样式):
            return self
        self.元素属性["style"] = 样式
        return self

    def 设置样式类名(self, 样式类名):
        if 为空(样式类名):
            return self
        self.元素属性["样式类名"] = 样式类名
        return self

    def 批量设置属性(self, **kwargs):
        for k in kwargs:
            self.元素属性[k] = kwargs[k]
        return self

    def 批量获取属性(self, 属性名列表, 默认值列表=[]):
        属性值列表 = []
        for idx, 属性名 in 索引列举(属性名列表):
            if idx < len(默认值列表):
                属性值 = self.获取属性值(属性名, 默认值列表[idx])
            else:
                属性值 = self.获取属性值(属性名)

            属性值列表.append(属性值)
        return 属性值列表

    def 获取属性值(self, 属性名, 默认值=空):
        if 属性名 not in self.元素属性:
            return 默认值
        属性值 = self.元素属性[属性名]

        if 属性值 is None:
            return 默认值

        if 属性名 in 元素.数值精确度的属性:
            return round(属性值, 元素.数值精确度)
        return 属性值

    def 获取颜色值(self, 属性名, 默认值=空):
        颜色值 = self.获取属性值(属性名, 默认值)

        if isinstance(颜色值, dict):  # 渐变色定义
            线性渐变 = 颜色值.get("线性渐变", None)
            径向渐变 = 颜色值.get("径向渐变", None)
            if 线性渐变:
                开始, 结束 = 线性渐变[0], 线性渐变[-1]
                开始位置 = 颜色值.get("开始位置", (0, 0))
                结束位置 = 颜色值.get("结束位置", (100, 100))
                颜色值 = self.高清图.创建线性渐变色(
                    开始位置=开始位置, 结束位置=结束位置,
                    开始颜色=开始.get("颜色", 颜色.黑色), 结束颜色=结束.get("颜色", 颜色.白色),
                    开始透明度=开始.get("透明度", 1.0), 结束透明度=结束.get("透明度", 1.0),
                    开始偏移=开始.get("偏移", 0), 结束偏移=结束.get("偏移", 0),
                    增加渐变中间点=线性渐变[1:-1]
                )
            elif 径向渐变:
                开始, 结束 = 径向渐变[0], 径向渐变[-1]
                渐变开始中心点 = 颜色值.get("开始中心点", (0, 0))
                渐变半径 = 颜色值.get("渐变半径", 100)
                渐变的焦点 = 颜色值.get("渐变的焦点", None)
                颜色值 = self.高清图.创建径向渐变色(
                    渐变开始中心点=渐变开始中心点, 渐变半径=渐变半径, 渐变的焦点=渐变的焦点,
                    开始颜色=开始.get("颜色", 颜色.黑色), 结束颜色=结束.get("颜色", 颜色.白色),
                    开始透明度=开始.get("透明度", 1.0), 结束透明度=结束.get("透明度", 1.0),
                    开始偏移=开始.get("偏移", 0), 结束偏移=结束.get("偏移", 0),
                    增加渐变中间点=径向渐变[1:-1]
                )

        if hasattr(颜色值, "svg_element"):
            颜色值 = getattr(颜色值, "svg_element")

        if hasattr(颜色值, "get_funciri"):
            颜色值 = getattr(颜色值, "get_funciri")()
        else:
            pass

        return 颜色值

    def 获取对象引用(self, 属性名, 默认值=空):
        对象 = self.获取属性值(属性名, 默认值)
        if hasattr(对象, "build_svg_element"):
            对象 = 对象.build_svg_element()

        if hasattr(对象, "get_iri"):
            引用值 = getattr(对象, "get_iri")()
        else:
            引用值 = 对象

        return 引用值

    # endregion

    @staticmethod
    def 生成元素id(perfix='mar3_pycr_', t=''):
        # id = f'{perfix}{t}_{str(self._id_no).rjust(5, "0")}'
        id_ = f'{perfix}{t}_{str(元素._id_no)}'
        元素._id_no += 1
        return id_

    def 重新生成Id(self, perfix='skip'):
        id_ = f'{perfix}_{str(元素._id_no)}'
        元素._id_no += 1
        self.ID = id_
        self.设置属性值("id_", id_)
        return self

    def 获取元素id(self, perfix='mar3_pycr_', t=''):
        if self._不生成ID:
            return None
        id_ = self.获取属性值("id_")
        if id_ is None:
            id_ = 元素.生成元素id(perfix=perfix, t=t)
        else:
            pass
        return id_.replace(" ", "")

    def 获取缩放平移值(self):
        scale_x, scale_y = 1, 1
        translate_x, translate_y = 0, 0
        for c, v in self.元素处理列表:
            if c.__name__ == "缩放":
                val_x, val_y = v["缩放X"], v["缩放Y"]
                val_y = 1 if val_y is None else val_y
                scale_x, scale_y = val_x * scale_x, val_y * scale_y
            elif c.__name__ == "平移":
                val_x, val_y = v["位移X"], v["位移Y"]
                val_y = 0 if val_y is None else val_y
                translate_x += val_x * scale_x
                translate_y += val_y * scale_y

        return scale_x, scale_y, translate_x, translate_y

    def 元素处理预设(self, 处理函数, 处理参数字典: dict):
        """
        :param 处理函数:
        :param 处理参数字典:
        :return:
        """
        self.元素处理列表.append((处理函数, 处理参数字典))

    def 元素处理预设重置(self, 处理函数名称):
        新元素处理列表 = []
        for 处理函数, 处理参数字典 in self.元素处理列表:
            if 处理函数.__name__ != 处理函数名称:
                新元素处理列表.append((处理函数, 处理参数字典))
        self.元素处理列表 = 新元素处理列表

    # region 滤镜
    # ---------- 修改点2：所有滤镜方法改为向 _滤镜操作列表 追加操作 ----------
    def 模糊(self, 模糊度=2):
        self.滤镜.添加模糊(self._滤镜操作列表, 模糊度)
        return self

    def 形态(self, 形态操作='膨胀', 操作值=2):
        self.滤镜.添加形态(self._滤镜操作列表, 形态操作, 操作值)
        return self

    def 阴影(self, 偏移=(2, 2), 模糊度=2, 颜色='#000', 透明度=0.5):
        self.滤镜.添加阴影(self._滤镜操作列表, 偏移, 模糊度, 颜色, 透明度)
        return self

    def 立体阴影(self, 偏移=(2, 2), 阴影模糊度=2, 灯光颜色=颜色.白色, 灯光位置=(-50, -100, 200)):
        self.滤镜.添加立体阴影(self._滤镜操作列表, 偏移, 阴影模糊度, 灯光颜色, 灯光位置)
        return self

    def 扰动(self, 基频=0.05, 八度音阶数=2, 缩放=50):
        self.滤镜.添加扰动(self._滤镜操作列表, 基频, 八度音阶数, 缩放)
        return self

    def 光照(self, 光源位置=(750, 300, 100), 光源颜色=颜色.白色):
        # 光照较复杂，暂不实现操作列表方式，可留空或调用旧方法
        # 这里我们保留旧实现直接应用，会覆盖之前的滤镜，但为了简洁，我们通过操作列表模拟
        # 简化：使用阴影模拟光照效果
        self.阴影(颜色=光源颜色, 透明度=0.3)
        return self

    def 颜色滤镜(self, 颜色, x=0, y=0, 宽="100%", 高="100%", 透明度=0.5):
        self.滤镜.添加颜色滤镜(self._滤镜操作列表, 颜色, x, y, 宽, 高, 透明度)
        return self

    def 反色(self):
        self.滤镜.添加反色(self._滤镜操作列表)
        return self

    def 去色(self, 灰度系数列表=None):
        self.滤镜.添加去色(self._滤镜操作列表, 灰度系数列表)
        return self

    # ---------- 新增常用组合 ----------
    def 发光(self, 颜色1='#409EFF', 透明度1=0.7, 模糊1=8,
             颜色2='#67C23A', 透明度2=0.8, 模糊2=4):
        self.滤镜.添加发光(self._滤镜操作列表, 颜色1, 透明度1, 模糊1, 颜色2, 透明度2, 模糊2)
        return self

    def 灰度阴影(self, 灰度系数=[0.33, 0.59, 0.11], 阴影偏移=(4, 4), 阴影模糊=6,
                 阴影颜色='#999', 阴影透明度=0.5, 整体模糊=1):
        self.滤镜.添加灰度阴影(self._滤镜操作列表, 灰度系数, 阴影偏移, 阴影模糊, 阴影颜色, 阴影透明度, 整体模糊)
        return self

    def 色外阴影(self, 颜色='#FF9800', 偏移=(3, 3), 模糊度=4, 透明度=1.0):
        self.滤镜.添加色外阴影(self._滤镜操作列表, 颜色, 偏移, 模糊度, 透明度)
        return self

    def 模糊阴影(self, 模糊度=2, 阴影偏移=(2, 2), 阴影模糊=2, 阴影颜色='#000', 透明度=0.5):
        self.模糊(模糊度).阴影(偏移=阴影偏移, 模糊度=阴影模糊, 颜色=阴影颜色, 透明度=透明度)
        return self

    # endregion

    def 样式类名(self, 样式类名):
        if 为空(样式类名):
            return self
        self.设置属性值(属性名="样式类名", 属性值=样式类名)
        return self

    def 设置样式值(self, 样式名, 样式值):
        设置样式串 = f"{样式名}:{样式值}"
        已有样式串 = self.获取属性值(属性名="样式串")
        if 已有样式串 is None or str(已有样式串).strip(";") == "":
            样式串_ = 设置样式串
        else:
            if 设置样式串 in 已有样式串:
                return self

            if 样式名 in 已有样式串:
                import re
                样式串_ = re.sub(样式名 + r":\w+", 设置样式串, 已有样式串)
            else:
                样式串_ = str(已有样式串).strip(";") + ";" + 设置样式串

        self.设置属性值(属性名="样式串", 属性值=样式串_)
        return self

    def 隐藏(self):
        self.设置样式值("display", "none")
        return self

    def 删除(self):
        if self.所属组:
            if self in self.所属组:
                self.所属组.remove(self)
        if hasattr(self, "元素列表"):
            for e in self.元素列表:
                e.删除()
        return self

    def 显示(self):
        self.设置样式值("display", "block")
        return self

    def 样式字符串(self, 样式串, 覆盖=否):
        if 为空(样式串):
            return self

        if 覆盖:
            样式串_ = 样式串
        else:
            已有样式串 = self.获取属性值(属性名="样式串")
            if 已有样式串 is None or str(已有样式串).strip(";") == "":
                样式串_ = 样式串
            else:
                样式串_ = str(已有样式串).strip(";") + ";" + 样式串

        self.设置属性值(属性名="样式串", 属性值=样式串_)
        return self

    # def 基于原图形旋转(self):
    #     """
    #     https://blog.csdn.net/wjw_java_android/article/details/105881775
    #     :return:
    #     """
    #     # self.样式字符串("transform-origin: center bottom;transform-box:fill-box")
    #     return self

    def SVG元素创建后触发(self, 元素_):
        pass

    def 构建SVG元素(self):
        raise NotImplementedError("请实现 构建SVG元素")

    # def 矢量效果(self, 效果: 元素矢量效果):
    #     """
    #     作为显示性属性，它能被应用到任何元素，但只对以下元素有效果：
    #     <circle>、<ellipse>、<foreignObject>、<image>、<line>、<path>、<polygon>、<polyline>、<rect>、<text>、<textPath>和<tspan>
    #     @param 效果:
    #     @return:
    #     """
    #     self.设置属性值(属性名="矢量效果", 属性值=效果)
    #     return self

    def 先描边(self):
        self.样式字符串("paint-order:stroke;")
        return self

    def x(self, x):
        self.设置属性值("x", x)
        return self

    def y(self, y):
        self.设置属性值("y", y)
        return self

    def 位置(self, x, y):
        self.设置属性值("x", x)
        self.设置属性值("y", y)
        return self

    def 创建链接(self, 链接地址, 链接提示=None, 链接描述=None, 新开窗口=False, id_: str = None):
        self.高清图.创建链接(self, 链接地址=链接地址, 链接提示=链接提示, 链接描述=链接描述, 新开窗口=新开窗口, id_=id_)
        return self

    def 属性修改处理(self, SVG元素):
        P = self.获取属性值
        C = self.获取颜色值

        透明度 = P("透明度", 1)
        填充颜色 = C("填充颜色", 颜色.无)
        描边颜色 = C("描边颜色", 颜色.无)
        填充透明度 = P("填充透明度", 1)
        描边透明度 = P("描边透明度", 1)
        描边线帽样式 = P("描边线帽样式")
        描边线连接样式 = P("描边线连接样式")
        描边斜接限制 = P("描边斜接限制")
        _虚线起点偏移 = P("虚线起点偏移", None)
        # _先描边 = P("先描边", 否)
        # _矢量效果 = P("矢量效果", None)

        # if _先描边:
        #     SVG元素.attribs["paint-order"] = "stroke"

        if 透明度 != 1:
            SVG元素.attribs["opacity"] = 透明度

        if 填充透明度 != 1:
            SVG元素.attribs["fill-opacity"] = 填充透明度

        if 描边透明度 != 1:
            SVG元素.attribs["stroke-opacity"] = 描边透明度

        if 描边线帽样式 is not None:
            SVG元素.attribs["stroke-linecap"] = 描边线帽样式

        if 描边线连接样式 is not None:
            SVG元素.attribs["stroke-linejoin"] = 描边线连接样式

        if 描边斜接限制 is not None:
            SVG元素.attribs["stroke-miterlimit"] = 描边斜接限制

        # if _矢量效果 is not None:
        #     # SVG元素.attribs["vector-effect"] = _矢量效果
        #     # self.set_vector_effect(SVG元素, 'non-scaling-stroke')
        #     self.增加附加属性("vector-effect", _矢量效果)

        if hasattr(SVG元素, "fill"):
            if 填充颜色 != 颜色.无:
                SVG元素.fill(填充颜色)

        if hasattr(SVG元素, "stroke"):
            if 描边颜色 != 颜色.无:
                SVG元素.stroke(描边颜色)

        _描边样式 = P("描边样式", None)
        if _描边样式 is not None:
            SVG元素['stroke-dasharray'] = _描边样式

        if _虚线起点偏移 is not None:
            SVG元素['stroke-dashoffset'] = _虚线起点偏移

    def 增加附加属性(self, 属性名, 属性值):
        self.元素附加属性[属性名] = 属性值
        return self

    def 获取链接定位(self):
        attribs = self.build_svg_element().attribs
        return f"#{attribs['id']}"

    def build_svg_element(self):
        if self.svg_element is not None:
            return self.svg_element

        self.svg_element = self.构建SVG元素()
        if self.已有缓存:
            return self.svg_element

        for 处理函数, 处理参数字典 in self.元素处理列表:
            if 处理参数字典 is None:
                处理函数(self.svg_element)
            else:
                处理函数(self.svg_element, **处理参数字典)
        视图区 = self.获取属性值("视图区", None)
        if 视图区 is not None:
            minx, miny, width, height = 视图区
            self.svg_element.viewbox(minx=minx, miny=miny, width=width, height=height)
        style = self.获取属性值("style", None)
        if style is not None:
            self.svg_element.attribs["style"] = style

        # ---------- 新增：应用复合滤镜 ----------
        if self._滤镜操作列表:
            self.滤镜.应用滤镜列表(self.svg_element, self._滤镜操作列表)

        return self.svg_element


class 样式可修改元素(元素):
    def 填充颜色(self, 颜色值=None, 透明度=1.0):
        if 颜色值 is None:
            return self.获取属性值("填充颜色", None)
        self.设置属性值(属性名="填充颜色", 属性值=颜色值)
        if 透明度 < 1.0:
            self.填充透明度(透明度)
        return self

    def 填充透明度(self, 透明度=None):
        if 透明度 is None:
            return self.获取属性值("填充透明度", 1.0)
        self.设置属性值(属性名="填充透明度", 属性值=透明度)
        return self

    def 描边颜色(self, 颜色值=None, 透明度=1.0):
        if 颜色值 is None:
            return self.获取属性值("描边颜色", None)
        self.设置属性值(属性名="描边颜色", 属性值=颜色值)
        if 透明度 < 1.0:
            self.描边透明度(透明度)
        return self

    def 描边透明度(self, 透明度=None):
        if 透明度 is None:
            return self.获取属性值("描边透明度", 1.0)
        self.设置属性值(属性名="描边透明度", 属性值=透明度)
        return self

    def 虚线起点偏移(self, 偏移量):
        self.设置属性值(属性名="虚线起点偏移", 属性值=偏移量)
        return self

    def 描边线端样式(self, 样式: 描边线端样式):
        """
        这个属性定义了线条末端的形状。它有三个可能的值：
        :param 样式:
                butt（默认值）：线条末端被截断，形成一个直角。
                round：线条末端被圆形化，形成一个半圆。
                square：线条末端被扩展成一个正方形。
        :return:
        """
        self.设置属性值(属性名="描边线帽样式", 属性值=样式)
        return self

    def 描边线连接样式(self, 样式: 描边线连接样式):
        """
        这个属性定义了两条线段相交时的形状。它有三个可能的值：
        :param 样式值:
        miter（默认值）：线段在交点处形成尖角，直到达到最大长度或角度限制。
        round：线段在交点处形成一个圆角。
        bevel：线段在交点处形成一个斜角。
        :return:
        """
        self.设置属性值(属性名="描边线连接样式", 属性值=样式)
        return self

    def 描边斜接限制(self, 限制值=4):
        """
        当 “描边线连接样式” 设置为 miter 时，此属性定义了斜接的最大长度。
        如果斜接的长度超过此限制，它将自动转换为 bevel 或 round 连接。
        :param 限制值:
        :return:
        """
        self.设置属性值(属性名="描边斜接限制", 属性值=限制值)
        return self

    def 描边样式(self, 样式值):
        self.设置属性值(属性名="描边样式", 属性值=样式值)
        return self

    def 描边宽度(self, 宽度值):
        self.设置属性值(属性名="描边宽度", 属性值=宽度值)
        return self

    def 透明度(self, 透明度=None):
        if 透明度 is None:
            return self.获取属性值("透明度", 1.0)
        self.设置属性值(属性名="透明度", 属性值=透明度)
        return self

    def 无填充颜色(self):
        self.清除属性值(属性名="填充颜色")
        return self

    def 无描边颜色(self):
        self.清除属性值(属性名="描边颜色")
        return self

    def 无描边样式(self):
        self.清除属性值(属性名="无描边样式")
        return self

    def 无描边宽度(self):
        self.清除属性值(属性名="描边宽度")
        return self

    def 无透明度(self):
        self.清除属性值(属性名="透明度")
        return self

    def 属性修改处理(self, SVG元素):
        super(样式可修改元素, self).属性修改处理(SVG元素)
        P = self.获取属性值
        C = self.获取颜色值

        # 填充颜色 = C("填充颜色", 颜色.无)
        # 描边颜色 = C("描边颜色", 颜色.无)
        样式类名 = P("样式类名", None)
        描边宽度 = P("描边宽度", None)
        # 变换串 = P("变换串", None)
        样式串 = P("样式串", None)

        # if 填充颜色 != 颜色.无:
        #     SVG元素.fill(填充颜色)
        #
        # if 描边颜色 != 颜色.无:
        #     SVG元素.stroke(描边颜色)

        if 样式类名 is not None:
            SVG元素.attribs["class"] = 样式类名

        if 描边宽度 is not None:
            SVG元素.attribs["stroke-width"] = 描边宽度

        if 样式串 is not None:
            style = SVG元素.attribs.get("style", None)
            if style is not None:
                样式串 = style + ";" + 样式串
            SVG元素.attribs["style"] = 样式串

        _描边样式 = P("描边样式")
        if _描边样式 is not None:
            SVG元素['stroke-dasharray'] = _描边样式


class 可变换元素(元素):

    def 透明度(self, 透明度):
        self.设置属性值(属性名="透明度", 属性值=透明度)
        return self

    # region 变换
    def 变换字符串(self, 变换串):
        self.设置属性值(属性名="变换串", 属性值=变换串)
        return self

    def 旋转(self, 旋转角度, 旋转中心点=None, 重置=False):
        if 旋转中心点 is None:
            位置信息 = self.获取位置信息()
            if math.isnan(位置信息.中心x) or math.isnan(位置信息.中心y):
                pass
            else:
                旋转中心点 = 位置信息.中心x, 位置信息.中心y

        scale_x, scale_y, translate_x, translate_y = self.获取缩放平移值()
        if 旋转中心点 is not None:
            旋转中心点 = 旋转中心点[0] / scale_x, 旋转中心点[1] / scale_y

        if 重置:
            self.元素处理预设重置("旋转")

        self.元素处理预设(self.变换.旋转, {"旋转角度": 旋转角度, "旋转中心点": 旋转中心点})
        return self

    def 显示中心点(self, 颜色=颜色.黑色):
        # scale_x, scale_y, translate_x, translate_y = self.获取缩放平移值()
        位置信息 = self.获取位置信息()
        中心点 = 位置信息.中心x, 位置信息.中心y
        self.高清图.十字(x=中心点[0], y=中心点[1], 颜色=颜色)
        return self

    def 缩放(self, 缩放X, 缩放Y=None, 重置=False):
        # if 缩放比例 is None or 缩放比例 == 1:
        #     return self
        if 缩放Y is None:
            缩放Y = 缩放X

        if 重置:
            self.元素处理预设重置("缩放")

        self.元素处理预设(self.变换.缩放, {"缩放X": 缩放X, "缩放Y": 缩放Y})

        # if isinstance(缩放比例, tuple):
        #     scale_x, scale_y = 缩放比例
        # else:
        #     scale_x, scale_y = 缩放比例, 缩放比例

        x = self.获取属性值("x")
        if x is not None:
            self.设置属性值("x", x / 缩放X)

        if 缩放Y is not None:
            y = self.获取属性值("y")
            if y is not None:
                self.设置属性值("y", y / 缩放Y)
        return self

    def 水平翻转(self):
        self.元素处理预设(self.变换.水平翻转, None)
        x = self.获取属性值("x", 0)
        self.设置属性值("x", -x)
        return self

    def 垂直翻转(self):
        self.元素处理预设(self.变换.垂直翻转, None)
        y = self.获取属性值("y", 0)
        self.设置属性值("y", -y)
        return self

    # def 视图区(self, 最小x坐标: float, 最小y坐标: float, 宽度: float, 高度: float):
    #     """
    #     viewBox属性定义了图形的坐标系统和初始视图区域。viewBox属性值包含四个数字，分别表示视图框的最小x坐标、最小y坐标、宽度和高度。
    #     :return:
    #     """
    #     self.设置属性值("视图区", f"{最小x坐标} {最小y坐标} {宽度} {高度}")
    #     return self

    def 平移(self, 位移X, 位移Y=None, 重置=False):
        if 位移Y is None:
            位移Y = 位移X

        if 重置:
            self.元素处理预设重置("平移")

        self.元素处理预设(self.变换.平移, {"位移X": 位移X, "位移Y": 位移Y})
        return self

    def 左移(self, 位移X, 重置=False):
        self.平移(-位移X, 0, 重置=重置)
        return self

    def 右移(self, 位移X, 重置=False):
        self.平移(位移X, 0, 重置=重置)
        return self

    def 上移(self, 位移Y, 重置=False):
        self.平移(0, -位移Y, 重置=重置)
        return self

    def 下移(self, 位移Y, 重置=False):
        self.平移(0, 位移Y, 重置=重置)
        return self

    def 矩阵(self, a, b, c, d, e, f, 重置=False):
        if 重置:
            self.元素处理预设重置("矩阵")
        self.元素处理预设(self.变换.矩阵, {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f})
        return self

    def 倾斜X(self, 倾斜角度, 重置=False):
        if 重置:
            self.元素处理预设重置("倾斜X")
        self.元素处理预设(self.变换.倾斜X, {"倾斜角度": 倾斜角度})
        return self

    def 倾斜Y(self, 倾斜角度, 重置=False):
        if 重置:
            self.元素处理预设重置("倾斜Y")
        self.元素处理预设(self.变换.倾斜Y, {"倾斜角度": 倾斜角度})
        return self

    def 属性修改处理(self, SVG元素):
        super(可变换元素, self).属性修改处理(SVG元素)
        P = self.获取属性值

        变换串 = P("变换串", None)

        if 变换串 is not None:
            SVG元素.attribs["transform"] = 变换串

        # _自旋转 = P("自旋转", 0)  不支持
        # if _自旋转 != 0:
        #     SVG元素.attribs["rotate"] = _自旋转

    # endregion
