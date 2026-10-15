# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os

from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板


# TODO: 以下是最简单的模板文件
class 字体查看索引页(神笔绘图板):
    页面缩放调整 = 1.0759772  # 1.0759772 < 精确值 < 1.0759773

    def find_ttf_files(self, directory):
        ttf_files = []  # 用于存储找到的 TTF 文件路径
        # 遍历目录及其子目录
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.ttf'):
                    ttf_files.append(os.path.join(root, file))  # 添加 TTF 文件的完整路径
        return ttf_files

    def 页面设置(self, 设置: 纸张设置):
        # 输出 PDF 文件，以及 页面打印，在这里设置好
        设置.上页边距 = 0
        设置.下页边距 = 0
        设置.左页边距 = 0
        设置.右页边距 = 0
        设置.页面方向 = 纸张方向.纵向
        设置.页面尺寸规格 = "A4"
        设置.页面缩放 = self.页面缩放调整
        self.最后页坐标Y = 0

    def 创作(self):
        # 注意：图框不会显示到 PDF 文件中，如果不希望SVG文件显示图框，可以注释或者删除以下代码
        self.显示图框()
        # self.显示网格(网格线距=20, 网格颜色=颜色.暗灰色, 网格透明度=1, 网格字体大小=9)
        # # TODO: 实现您的功能从这里开始
        # self.写字(x=100, y=100, 文字="制作从这里开始")
        左边距 = 30
        上边距 = 30

        # 使用示例
        directory_path =self.字体目录  # r'H:\中国大陆无版权字体'  # 替换为你实际的目录路径
        if not hasattr(self, "字体文字内容"):
            self.字体文字内容 = "神笔码靓，意如其神笔般神奇"
        ttf_files = self.find_ttf_files(directory_path)
        字体大小 = 30
        间距 = 字体大小 * 2
        row_index = 0
        for i, ttf_file in enumerate(ttf_files):
            ttf_file_name, _ = os.path.splitext(os.path.basename(ttf_file))
            # print(ttf_file)
            try:
                self.文字转路径(x=左边距, y=上边距 + 间距 * row_index,
                           文字=self.字体文字内容,
                           字体文件=ttf_file, 字体大小=字体大小).描边宽度(0.2)
                self.写字(x=左边距 + self.宽 / 1.7, y=上边距 + 间距 * row_index, 字体大小=字体大小 / 3,
                        文字=ttf_file.replace(directory_path, ""), 垂直基线对齐=文字垂直基线对齐.顶线对齐,
                        水平基线对齐=文字水平基线对齐.起始点对齐)
                row_index += 1
            except Exception as e:
                from 神笔码靓.神笔库 import 打印蓝色消息
                打印蓝色消息(str(e) + ", " + ttf_file)

        self.最后页坐标Y = 上边距 + 间距 * (row_index + 1)

    def 完成前执行(self):
        # print("最大页数", self.最大页数)
        高 = self.最后页坐标Y + 30
        self.修改绘图板大小(高=高)


# # 打印找到的 TTF 文件


if __name__ == '__main__':
    # 作品文件路径：保存的 SVG（矢量图）格式的文件路径名称
    # 宽: 神笔绘图板也需要设置页面的宽度
    # 高: 神笔绘图板也需要设置页面的高度
    宽, 高 = 纸张大小.A4_纵向(1)
    神笔 = 字体查看索引页(作品文件路径="生肖字体查看.svg", 宽=宽, 高=高)
    神笔.字体目录 = r'H:\中国大陆无版权字体'
    神笔.字体目录 = r'G:\works\gitcode\code_painter_app\字体'

    # 神笔.创作 = lambda :None
    # 神笔.完成前执行 = lambda :None
    # ttf_file = "H:\中国大陆无版权字体\包图小白体\包图小白体_猫啃网.ttf"
    # 神笔.文字转路径(x=30, y=30, 文字="代码", 字体文件=ttf_file, 字体大小=200,填充颜色=颜色.黑色)


    神笔.完成()
    # 神笔.生成PDF()

"""
D:\Anaconda3\envs\pythoncr\python.exe G:/works/gitcode/code_painter/神笔库/字体查看索引页生成.py
'NoneType' object is not subscriptable, H:\中国大陆无版权字体\文泉驿微米黑.ttf
'神', H:\中国大陆无版权字体\文泉驿点阵宋体.ttf
'神', H:\中国大陆无版权字体\问藏书房_猫啃网.ttf
Python int too large to convert to C int, H:\中国大陆无版权字体\975黑体20201014\975GothicSC-Bold.ttf
Python int too large to convert to C int, H:\中国大陆无版权字体\975黑体20201014\975GothicSC-Medium.ttf
Python int too large to convert to C int, H:\中国大陆无版权字体\975黑体20201014\975GothicSC-Regular.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\Code2003\Code2003.ttf
'神', H:\中国大陆无版权字体\叶根友微典体\叶根友微典.ttf
too much 'vmtx' table data
'神', H:\中国大陆无版权字体\字体圈欣意冠黑体\字体圈欣意LOGO体.ttf
'，', H:\中国大陆无版权字体\庞门正道真贵楷体\庞门正道真贵楷体.ttf
'，', H:\中国大陆无版权字体\摄图摩登小方体\摄图摩登小方体(免费商用).ttf
'，', H:\中国大陆无版权字体\新愚公迷茫体1.20\新愚公迷茫体.ttf
'created' timestamp seems very low; regarding as unix timestamp
The vhea.numberOfVMetrics exceeds the maxp.numGlyphs
too much 'vmtx' table data
'NoneType' object is not subscriptable, H:\中国大陆无版权字体\有字库龙藏体\有字库龙藏体.ttf
'神', H:\中国大陆无版权字体\有爱新黑_简体版\有爱新黑CN-Bold.ttf
'神', H:\中国大陆无版权字体\有爱新黑_简体版\有爱新黑CN-Light.ttf
'神', H:\中国大陆无版权字体\有爱新黑_简体版\有爱新黑CN-Medium.ttf
'神', H:\中国大陆无版权字体\有爱新黑_简体版\有爱新黑CN-Regular.ttf
'神', H:\中国大陆无版权字体\有爱黑体\有爱魔兽黑体-Bold.ttf
'神', H:\中国大陆无版权字体\有爱黑体\有爱魔兽黑体-Light.ttf
'神', H:\中国大陆无版权字体\有爱黑体\有爱魔兽黑体-Medium.ttf
'神', H:\中国大陆无版权字体\有爱黑体\有爱魔兽黑体-Regular.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\极影毁片圆1.16\极影毁片圆.ttf
'神', H:\中国大陆无版权字体\柳体\柳体.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\江城圆体3.1\江城圆体 200W.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\江城圆体3.1\江城圆体 300W.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\江城圆体3.1\江城圆体 400W.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\江城圆体3.1\江城圆体 500W.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\江城圆体3.1\江城圆体 600W.ttf
chr() arg not in range(0x110000), H:\中国大陆无版权字体\江城圆体3.1\江城圆体 700W.ttf
'码', H:\中国大陆无版权字体\澹雅明体1.00\澹雅明体A.ttf
'码', H:\中国大陆无版权字体\澹雅明体1.00\澹雅明体B.ttf
'码', H:\中国大陆无版权字体\澹雅明体1.00\澹雅明体C.ttf
'，', H:\中国大陆无版权字体\猫啃网烟波宋1.10\猫啃网烟波宋-B.ttf
'，', H:\中国大陆无版权字体\猫啃网烟波宋1.10\猫啃网烟波宋-E.ttf
'，', H:\中国大陆无版权字体\猫啃网烟波宋1.10\猫啃网烟波宋-H.ttf
'，', H:\中国大陆无版权字体\猫啃网烟波宋1.10\猫啃网烟波宋-L.ttf
'，', H:\中国大陆无版权字体\猫啃网烟波宋1.10\猫啃网烟波宋-M.ttf
'，', H:\中国大陆无版权字体\猫啃网烟波宋1.10\猫啃网烟波宋-R.ttf
'，', H:\中国大陆无版权字体\猫啃网烟波宋1.10\猫啃网烟波宋-S.ttf
'，', H:\中国大陆无版权字体\猫啃网风雅宋1.20\猫啃网风雅宋.ttf
'靓', H:\中国大陆无版权字体\站酷酷黑体\站酷酷黑体_猫啃网.ttf
'靓', H:\中国大陆无版权字体\素材集市康康体\素材集市康康体_猫啃网.ttf
'靓', H:\中国大陆无版权字体\素材集市酷方体\素材集市酷方体.ttf
'靓', H:\中国大陆无版权字体\谦度手写楷体2.20\谦度手写楷体2.20.ttf
'神', H:\中国大陆无版权字体\贤二体\贤二体_猫啃网.ttf
'神', H:\中国大陆无版权字体\途牛类圆体\途牛类圆体_猫啃网.ttf
'，', H:\中国大陆无版权字体\醍醐书体\醍醐书体A.ttf
'神', H:\中国大陆无版权字体\醍醐书体\醍醐书体B.ttf
'NoneType' object is not subscriptable, H:\中国大陆无版权字体\钟齐志莽行书\钟齐志莽行书.ttf
'NoneType' object is not subscriptable, H:\中国大陆无版权字体\钟齐流江毛草\钟齐流江毛草.ttf
'神', H:\中国大陆无版权字体\霞鹜晰黑0.201\TTF (SIL part)\LXGWclgoSILOFLpart-Book.ttf
'神', H:\中国大陆无版权字体\霞鹜晰黑0.201\TTF (SIL part)\LXGWclgoSILOFLpart-Regular.ttf
'NoneType' object is not subscriptable, H:\中国大陆无版权字体\马善政毛笔楷体\MaShanZheng-Regular.ttf
'神', H:\中国大陆无版权字体\黄令东细线体\RRPL.ttf
'神', H:\中国大陆无版权字体\黄令东齐伋体\qiji-fallback_0.0.2.ttf
'神', H:\中国大陆无版权字体\黄令东齐伋复刻\qiji-combo.ttf
神笔绘图板保存中...
神笔绘图板保存成功，保存位置： G:\works\gitcode\code_painter\输出文件\字体查看索引页.svg
已完成
完成 耗时：53.92 s

Process finished with exit code 0

"""