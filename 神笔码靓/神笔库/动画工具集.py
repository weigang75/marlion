# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from dataclasses import dataclass


@dataclass
class 动画关键帧:
    时间点: [float, int] = 0


@dataclass
class 缩放动画关键帧(动画关键帧):
    缩放X: [float, int] = 1
    缩放Y: [float, int] = 1


@dataclass
class 平移动画关键帧(动画关键帧):
    位置X: [float, int] = 0
    位置Y: [float, int] = 0


@dataclass
class 倾斜动画关键帧(动画关键帧):
    倾斜角: [float, int] = 10


@dataclass
class 旋转动画关键帧(动画关键帧):
    旋转角: [float, int] = 0
    旋转中心点: tuple[[float, int], [float, int]] = (0, 0)


class 动画工具集:

    def __init__(self, 高清图=None):
        from 神笔码靓.神笔库 import 神笔绘图板
        self.高清图: 神笔绘图板 = 高清图
        self.dwg = 高清图.dwg

    #     def 矩阵(self, SVG元素, a, b, c, d, e, f):
    #         """
    # matrix(sx,0,0,sy,TranslateX,TranslateY)
    # matrix(cos(a), sin(a), -sin(a), cos(a), TranslateX,TranslateY)
    # matrix(1, skewY=tan(a), skewX=tan(a), 1, TranslateX,TranslateY)
    #
    # 对应矩阵：
    # a  c  e
    # b  d  f
    # 0  0  1
    #
    # 1.Translate(tx, ty)
    #     矩阵：
    #     1  0  tx
    #     0  1  ty
    #     0  0  1
    #     写法：matrix(1,0,0,1,tx,ty)
    #
    # 2.Scale(sx, sy)
    #     矩阵：
    #     sx  0  0
    #     0  sy  0
    #     0   0  1
    #     写法：matrix(sx,0,0,sy,0,0)
    #
    # 3.Rotate(a)
    #     矩阵：
    #     cos(a)  -sin(a)  0
    #     sin(a)   cos(a)  0
    #     0        0       1
    #     写法：matrix(cos(a), sin(a), -sin(a), cos(a), 0, 0)
    #
    #   3+.Rotate(a, cx, cy)
    #     cos(a)  -sin(a)  -cx × cos(a) + cy × sin(a) + cx
    #     sin(a)   cos(a)  -cx × sin(a) - cy × cos(a) + cy
    #     0        0       1
    #     写法：
    #     matrix(cos(a), sin(a), -sin(a), cos(a), -cx × cos(a) + cy × sin(a) + cx + tx, -cx × sin(a) - cy × cos(a) + cy + ty)
    #
    # 4.skew(skewX, skewY)
    #   4.1 skewX
    #     矩阵：
    #     1  tan(a)  0
    #     0     1      0
    #     0     0      1
    #     写法：matrix(1, 0, tan(a), 1, 0, 0)
    #
    #   4.2 skewY
    #     矩阵：
    #     1         0     0
    #     tan(a)    1     0
    #     0         0     1
    #     写法：matrix(1, tan(a), 0, 1, 0, 0)
    #
    # 5.如果你的使用包含旋转，缩放，平移等多种
    #     例如：
    #     <g transform="translate(20, 50) scale(1, 1) rotate(-30 10 25)">
    #     对应矩阵：
    #     cos(a)  -sin(a)  -cx × cos(a) + cy × sin(a) + cx + tx
    #     sin(a)   cos(a)  -cx × sin(a) - cy × cos(a) + cy + ty
    #     0        0       1
    #     此处scale为1，因此不考虑。写法为：
    #     matrix(cos(a), sin(a), -sin(a), cos(a), -cx × cos(a) + cy × sin(a) + cx + tx, -cx × sin(a) - cy × cos(a) + cy + ty)
    #     结果为： matrix(0.866, -0.5 0.5 0.866 8.84 58.35).
    #
    #         :param SVG元素:
    #         :param a:
    #         :param b:
    #         :param c:
    #         :param d:
    #         :param e:
    #         :param f:
    #         :return:
    #         """
    #         SVG元素.matrix(a, b, c, d, e, f)
    #

    """
    可以加入关键帧
     <animateTransform xlink:href="#frame" attributeName="transform" type="rotate" begin="0s" dur="3s"
                      values="0 150 150; 0 150 150; 180 150 150" keyTimes="0; 0.8; 1"
                      repeatCount="indefinite"></animateTransform>

                      values="0 150; 100 150; 180 150" keyTimes="0; 0.8; 1"
    """

    def 透明(self, SVG元素, 透明度循环集=[0.5, 1.0, 0.5], 持续时间: [float, int] = 1, 重复次数: int = None,
             填充行为="remove", id_: str = None):
        if 重复次数 is None:
            重复次数 = "indefinite"
        if 透明度循环集 is None:
            透明度循环集 = [0, 1.0, 0]
        animation = self.dwg.animate(attributeName="opacity", dur=f"{持续时间}s",
                                     fill=填充行为, values=透明度循环集, repeatCount=重复次数)
        if id_ is not None:
            animation.attribs["id"] = id_
        SVG元素.add(animation)

    def 虚线流(self, SVG元素, 方向: int = 1, 持续时间: [float, int] = 3, 周期: [float, int] = None,
               重复次数: int = None, 填充行为="remove", id_: str = None):
        stroke_dasharray = SVG元素.attribs.get("stroke-dasharray", None)
        if stroke_dasharray is None:
            return
        if 方向 == 0:
            方向 = -1
        if 方向 is None:
            方向 = 1
        方向 = 方向 / abs(方向)
        if 周期 is None:
            stroke_dasharray = stroke_dasharray.replace(",", " ")
            num_cnt = 0
            cnt = 0
            for num in stroke_dasharray.split(" "):
                if str(num).strip() == "":
                    continue
                num_cnt += float(num)
                cnt += 1
            if cnt % 2 == 0:
                周期 = num_cnt
            else:
                周期 = num_cnt * 2

        if 重复次数 is None:
            重复次数 = "indefinite"

        animation = self.dwg.animate(attributeName="stroke-dashoffset", from_="0", dur=f"{持续时间}s",
                                     fill=填充行为, to=f"{(方向 * 周期)}", repeatCount=重复次数)
        if id_ is not None:
            animation.attribs["id"] = id_
        SVG元素.add(animation)

    def 缩放(self, SVG元素, 开始时间=0, 持续时间=3,
             开始缩放X=1, 开始缩放Y=1, 结束缩放X=-2, 结束缩放Y=2, 重复次数=None, 填充行为="remove",
             关键帧列表: list[缩放动画关键帧] = [], id_: str = None):
        """
        <animateTransform xmlns="http://www.w3.org/2000/svg" attributeName="transform" begin="0s" dur="3s" from="1,1" repeatCount="indefinite" to="-2,2" type="scale" values="1 2; 2 1; 1 -1" keyTimes="0; 0.8; 1"/>
        <animateTransform xmlns="http://www.w3.org/2000/svg" attributeName="transform" begin="0s" dur="3s" fill="remove" from="1,1" keyTimes="1; 2" repeatCount="indefinite" to="-2,2" type="scale" values="1.5 0.5; 0.5 1.5"/>
        :param SVG元素:
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
        if 重复次数 is None:
            重复次数 = "indefinite"
        animation = self.dwg.animateTransform(begin=f"{开始时间}s", dur=f"{持续时间}s", transform="scale",
                                              fill=填充行为,
                                              from_=f"{开始缩放X},{开始缩放Y}", to=f"{结束缩放X},{结束缩放Y}",
                                              repeatCount=重复次数)
        if id_ is not None:
            animation.attribs["id"] = id_

        animation.attribs["attributeName"] = "transform"

        keyTimes = []
        values = []

        if len(关键帧列表) > 0:
            keyTimes.append("0")
            values.append(f"{开始缩放X} {开始缩放Y}")

        for 关键帧 in 关键帧列表:
            keyTimes.append(str(关键帧.时间点))
            values.append(f"{关键帧.缩放X} {关键帧.缩放Y}")

        if len(关键帧列表) > 0:
            keyTimes.append("1")
            values.append(f"{结束缩放X} {结束缩放Y}")

        if len(keyTimes) > 0:
            animation.attribs["keyTimes"] = ";".join(keyTimes)
        if len(values) > 0:
            animation.attribs["values"] = ";".join(values)

        SVG元素.add(animation)

    #
    #     def 垂直翻转(self, SVG元素):
    #         SVG元素.scale((-1, 1))
    #
    #     def 水平翻转(self, SVG元素):
    #         SVG元素.scale((1, -1))

    def 轨迹移动(self, SVG元素, 路径点列表, 开始时间=0, 持续时间=3, 重复次数=None, 旋转=None, 填充行为="remove",
                 id_: str = None):
        """

        @param SVG元素:
        @param 路径点列表:
        @param 开始时间:
        @param 持续时间:
        @param 重复次数:
        @param 旋转: 自动旋转(auto),自动反向旋转(auto-reverse),固定角度值(如45deg、0),相对角度值(如rotate="+90deg")
        @param 填充行为:
        @return:
        """
        # <!--轨迹-->
        # <path d="M10,50 q60,50 100,0 q60,-50 100,0" stroke="black" stroke-width="2" />
        # 参考：https://www.zhangxinxu.com/wordpress/2014/08/so-powerful-svg-smil-animation/
        # <g>
        # <!-- Rick 飞船 svg-->
        # <animateMotion path="M10,50 q60,50 100,0 q60,-50 100,0" begin="0s"
        # dur="10s" repeatCount="indefinite" />

        from 神笔码靓.神笔库 import 神笔绘图板工具
        from 神笔码靓.神笔库.元素库 import 路径元素
        原生path = None
        if isinstance(路径点列表, 路径元素):
            路径元素_: 路径元素 = 路径点列表
            原生path = 路径元素_.原生path()
            if 原生path is None:
                点列表 = 路径点列表.路径点列表
            else:
                pass
        else:
            点列表 = 路径点列表
            路径元素_ = None

        if 原生path is None:
            点列表 = 神笔绘图板工具.转SVG绘制路径命令(点列表)
            路径 = 神笔绘图板工具.点列表转SVG路径(点列表)
            path = "".join(路径)
        else:
            path = 原生path

        if 重复次数 is None:
            重复次数 = "indefinite"
        if 旋转 is None:
            旋转 = "auto"
        旋转 = str(旋转).lower()
        animation = self.dwg.animateMotion(path=path, fill=填充行为,
                                           begin=f"{开始时间}s", dur=f"{持续时间}s", repeatCount=重复次数, rotate=旋转)
        if id_ is not None:
            animation.attribs["id"] = id_
        if 路径元素_ is not None:
            svg_path = 路径元素_.构建SVG元素()
            if "transform" in svg_path.attribs:
                animation.attribs["transform"] = svg_path.attribs["transform"]

        SVG元素.add(animation)

    def 平移(self, SVG元素, 开始时间=0, 持续时间=3, 起点X=0, 起点Y=0, 终点X=0, 终点Y=-2000, 重复次数=None,
             填充行为="remove",
             关键帧列表: list[平移动画关键帧] = [], id_: str = None):
        """

        :param SVG元素:
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
        if 重复次数 is None:
            重复次数 = "indefinite"
        animation = self.dwg.animateTransform(begin=f"{开始时间}s", dur=f"{持续时间}s", transform="translate",
                                              fill=填充行为,
                                              from_=f"{起点X},{起点Y}", to=f"{终点X},{终点Y}", repeatCount=重复次数)
        if id_ is not None:
            animation.attribs["id"] = id_

        animation.attribs["attributeName"] = "transform"

        keyTimes = []
        values = []

        if len(关键帧列表) > 0:
            keyTimes.append("0")
            values.append(f"{起点X} {起点Y}")

        for 关键帧 in 关键帧列表:
            keyTimes.append(str(关键帧.时间点))
            values.append(f"{关键帧.位置X} {关键帧.位置Y}")

        if len(关键帧列表) > 0:
            keyTimes.append("1")
            values.append(f"{终点X} {终点Y}")

        if len(keyTimes) > 0:
            animation.attribs["keyTimes"] = ";".join(keyTimes)
        if len(values) > 0:
            animation.attribs["values"] = ";".join(values)

        SVG元素.add(animation)

    def 倾斜X(self, SVG元素, 开始时间=0, 持续时间=3, 起始倾斜角=0, 结束倾斜角=45, 重复次数=None, 填充行为="remove",
              关键帧列表: list[倾斜动画关键帧] = [], id_: str = None):
        """

        :param SVG元素:
        :param 开始时间:
        :param 持续时间:
        :param 起始倾斜角:
        :param 结束倾斜角:
        :param 重复次数:
        :param 填充行为:
        :return:
        """
        if 重复次数 is None:
            重复次数 = "indefinite"
        animation = self.dwg.animateTransform(begin=f"{开始时间}s", dur=f"{持续时间}s", transform="skewX",
                                              fill=填充行为,
                                              from_=f"{起始倾斜角}",
                                              to=f"{结束倾斜角}",
                                              repeatCount=重复次数)
        if id_ is not None:
            animation.attribs["id"] = id_
        animation.attribs["attributeName"] = "transform"

        keyTimes = []
        values = []

        if len(关键帧列表) > 0:
            keyTimes.append("0")
            values.append(f"{起始倾斜角}")

        for 关键帧 in 关键帧列表:
            keyTimes.append(str(关键帧.时间点))
            values.append(f"{关键帧.倾斜角}")

        if len(关键帧列表) > 0:
            keyTimes.append("1")
            values.append(f"{结束倾斜角}")

        if len(keyTimes) > 0:
            animation.attribs["keyTimes"] = ";".join(keyTimes)
        if len(values) > 0:
            animation.attribs["values"] = ";".join(values)

        SVG元素.add(animation)

    def 倾斜Y(self, SVG元素, 开始时间=0, 持续时间=3, 起始倾斜角=0, 结束倾斜角=45, 重复次数=None, 填充行为="remove",
              关键帧列表: list[倾斜动画关键帧] = [], id_: str = None):
        """

        :param SVG元素:
        :param 开始时间:
        :param 持续时间:
        :param 起始倾斜角:
        :param 结束倾斜角:
        :param 重复次数:
        :param 填充行为:
        :return:
        """
        if 重复次数 is None:
            重复次数 = "indefinite"
        animation = self.dwg.animateTransform(begin=f"{开始时间}s", dur=f"{持续时间}s", transform="skewY",
                                              fill=填充行为,
                                              from_=f"{起始倾斜角}",
                                              to=f"{结束倾斜角}",
                                              repeatCount=重复次数)
        if id_ is not None:
            animation.attribs["id"] = id_
        animation.attribs["attributeName"] = "transform"
        keyTimes = []
        values = []

        if len(关键帧列表) > 0:
            keyTimes.append("0")
            values.append(f"{起始倾斜角}")

        for 关键帧 in 关键帧列表:
            keyTimes.append(str(关键帧.时间点))
            values.append(f"{关键帧.倾斜角}")

        if len(关键帧列表) > 0:
            keyTimes.append("1")
            values.append(f"{结束倾斜角}")

        if len(keyTimes) > 0:
            animation.attribs["keyTimes"] = ";".join(keyTimes)
        if len(values) > 0:
            animation.attribs["values"] = ";".join(values)
        SVG元素.add(animation)

    def 旋转(self, SVG元素, 开始时间=0, 持续时间=3,
             起始角=0, 起始旋转中心点=(0, 0), 结束角=90, 结束旋转中心点=(0, 0), 重复次数=None, 填充行为="remove",
             关键帧列表: list[旋转动画关键帧] = [], id_: str = None):
        """

        :param SVG元素:
        :param 开始时间:
        :param 持续时间:
        :param 起始角:
        :param 起始旋转中心点:
        :param 结束角:
        :param 结束旋转中心点:
        :param 重复次数:
        :param 填充行为:
        :return:
        """
        if 重复次数 is None:
            重复次数 = "indefinite"
        animation = self.dwg.animateTransform(begin=f"{开始时间}s", dur=f"{持续时间}s", transform="rotate",
                                              fill=填充行为,
                                              from_=f"{起始角} {起始旋转中心点[0]} {起始旋转中心点[1]}",
                                              to=f"{结束角} {结束旋转中心点[0]} {结束旋转中心点[1]}",
                                              repeatCount=重复次数)
        if id_ is not None:
            animation.attribs["id"] = id_
        animation.attribs["attributeName"] = "transform"
        keyTimes = []
        values = []

        if len(关键帧列表) > 0:
            keyTimes.append("0")
            values.append(f"{起始角} {起始旋转中心点[0]} {起始旋转中心点[1]}")

        for 关键帧 in 关键帧列表:
            keyTimes.append(str(关键帧.时间点))
            values.append(f"{关键帧.旋转角} {关键帧.旋转中心点[0]} {关键帧.旋转中心点[1]}")

        if len(关键帧列表) > 0:
            keyTimes.append("1")
            values.append(f"{结束角} {结束旋转中心点[0]} {结束旋转中心点[1]}")

        if len(keyTimes) > 0:
            animation.attribs["keyTimes"] = ";".join(keyTimes)
        if len(values) > 0:
            animation.attribs["values"] = ";".join(values)
        SVG元素.add(animation)
