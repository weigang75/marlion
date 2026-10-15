# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import math


class 多边形工具:
    @staticmethod
    def 顶点数去重(顶点):
        """

        :param 顶点:
        :return:
        """
        pt_s, pt_e = 顶点[0], 顶点[-1]
        if pt_s[0] == pt_e[0] and pt_s[1] == pt_e[1]:
            顶点 = 顶点[:-1]
        return 顶点

    @staticmethod
    def 获取顶点数(顶点):
        """

        :param 顶点:
        :return:
        """
        顶点 = 多边形工具.顶点数去重(顶点)
        p_num = len(顶点)
        return p_num

    @staticmethod
    def 获取中心点(顶点):
        """
        找中心点
        :param 顶点:
        :return:
        """
        p_num = 多边形工具.获取顶点数(顶点)

        x = sum(point[0] for point in 顶点) / p_num
        y = sum(point[1] for point in 顶点) / p_num

        return x, y

    @staticmethod
    def 获取形状起始点(顶点):
        """
        找中心点
        :param 顶点:
        :return:
        """
        p_num = 多边形工具.获取顶点数(顶点)

        x = min(point[0] for point in 顶点)
        y = min(point[1] for point in 顶点)

        return x, y

    @staticmethod
    def 获取形状结束点(顶点):
        """
        找中心点
        :param 顶点:
        :return:
        """
        p_num = 多边形工具.获取顶点数(顶点)

        x = max(point[0] for point in 顶点)
        y = max(point[1] for point in 顶点)

        return x, y

    # @staticmethod
    # def 计算下个顶点(顶点1, 顶点2, 形状的顶点总数, 方向=1):
    #     x1, y1 = 顶点1
    #     x2, y2 = 顶点2
    #     # Calculate distance between two points
    #     distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #     # Calculate angle between two points
    #     angle = math.atan2(y2 - y1, x2 - x1)
    #     angle = angle + 2 * math.pi / 形状的顶点总数
    #     # print(angle)
    #     # Calculate coordinates of the other three vertices
    #     x3 = x2 + distance * math.cos(angle * 方向)
    #     y3 = y2 + distance * math.sin(angle * 方向)
    #
    #     return x3, y3

    @staticmethod
    def 计算下个顶点(顶点1, 顶点2, 形状的顶点总数, 方向=1):
        if 方向 >= 0:
            方向 = 1
        else:
            方向 = -1
        x1, y1 = 顶点1
        x2, y2 = 顶点2
        # Calculate distance between two points
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Calculate angle between two points
        angle = math.atan2(y2 - y1, x2 - x1)
        angle += 方向 * 2 * math.pi / 形状的顶点总数
        # Calculate coordinates of the other three vertices
        x3 = x2 + distance * math.cos(angle)
        y3 = y2 + distance * math.sin(angle)
        return x3, y3

    @staticmethod
    def 计算缩放顶点(顶点, 缩放):
        if 缩放 == 1:
            return 顶点
        # 计算多边形的中心点
        center_x = sum([vertex[0] for vertex in 顶点]) / len(顶点)
        center_y = sum([vertex[1] for vertex in 顶点]) / len(顶点)

        # 将多边形平移到原点
        translated_vertices = [(vertex[0] - center_x, vertex[1] - center_y) for vertex in 顶点]

        # 缩放多边形
        scaled_vertices = [(vertex[0] * 缩放, vertex[1] * 缩放) for vertex in translated_vertices]

        # 将多边形平移回原来的位置
        final_vertices = [(vertex[0] + center_x, vertex[1] + center_y) for vertex in scaled_vertices]
        if len(顶点) != len(final_vertices):
            final_vertices += (final_vertices[-1][0], final_vertices[-1][1])
        return final_vertices

    @staticmethod
    def 找点(当前点, 角度, 距离):
        x_a, y_a = 当前点
        # 将角度从度转换为弧度
        angle_rad = -math.radians(角度)

        # 使用极坐标到直角坐标的转换公式
        x_b = x_a + 距离 * math.cos(angle_rad)
        y_b = y_a + 距离 * math.sin(angle_rad)

        # 返回点B的坐标
        return x_b, y_b

    @staticmethod
    def 找多边形的顶点(顶点A, 顶点B, 顶点总数, 方向=-1):
        if 顶点总数 < 3:
            err_msg = "顶点总数，必须大于等于3"
            raise Exception(err_msg)
        p1, p2 = 顶点A, 顶点B
        pts = [p1, p2]
        for i in range(顶点总数 - 2):
            p3 = 多边形工具.计算下个顶点(p1, p2, 顶点总数, 方向=方向)
            pts.append(p3)
            p1, p2 = p2, p3
        return pts

    @staticmethod
    def 根据正多边形边长计算外接圆半径(边长: float, n: int):
        """
        根据正多边形的边长和边数计算边到中心的距离（外接圆半径）。
        @param 边长: 正多边形的边长
        @param n: 正多边形的边数
        @return: 边到中心的距离（外接圆半径）
        """
        return 边长 / (2 * math.sin(math.pi / n))

    @staticmethod
    def 根据正多边形内接圆半径计算边长(内接圆半径, n):
        """
        根据正多边形内接圆半径和边数计算边长
        @param 内接圆半径:  正多边形内接圆半径，正多边形的边到中心的距离
        @param n: 正多边形的边数
        @return: 正多边形的边长
        """
        central_angle = 2 * math.pi / n  # 中心角（弧度制）
        return 2 * 内接圆半径 * math.tan(central_angle / 2)

    @staticmethod
    def 根据正多边形外接圆半径计算边长(外接圆半径: float, n: int):
        """
        根据正多边形的边到中心的距离（外接圆半径）和边数计算边长。
        @param 外接圆半径: 正多边形外接圆半径，正多边形的角到中心的距离
        @param n: 正多边形的边数
        @return: 正多边形的边长
        """
        return 2 * 外接圆半径 * math.sin(math.pi / n)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6, 8), dpi=400)
    点1 = (0, 0)
    角度 = 108
    距离 = 50
    # 点2 = 多边形工具.找点(点1, 角度, 距离)

    点2 = 多边形工具.找点(点1, 角度, 距离)

    # plt.plot([点1[0], 点3[0]], [点1[1], 点3[1]], 'b-')
    #
    # plt.plot([点1[0], 点2[0]], [点1[1], 点2[1]], 'r-')
    # 顶点总数 = 12
    # 点3 = 多边形工具.计算下个顶点(点1, 点2, 顶点总数)
    # 点4 = 多边形工具.计算下个顶点(点2, 点3, 顶点总数)
    # 点5 = 多边形工具.计算下个顶点(点3, 点4, 顶点总数)
    # 点6 = 多边形工具.计算下个顶点(点4, 点5, 顶点总数)
    pts = 多边形工具.找多边形的顶点(点1, 点2, 5)
    x, y = zip(*pts)
    plt.plot(x, y, 'b-')

    # print(点2, 点3)

    # 设置坐标轴范围，确保五边形完全可见
    plt.xlim(-100, 210)
    plt.ylim(-100, 297)
    # 设置坐标轴为等比例，这样五边形看起来就不会是椭圆形
    plt.gca().set_aspect('equal', adjustable='box')
    # 显示图形
    plt.show()
