# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-07-15
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.生活娱乐.纸笔五子棋 import 纸笔五子棋
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *


def 读取棋谱():
    import json

    # 读取 JSON 文件
    with open('五子棋棋谱/1.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    chess_notation = data['棋谱']
    moves_list = []
    i = 0
    黑方 = True
    序号 = 1
    while i < len(chess_notation):
        move = ""
        while i < len(chess_notation) and chess_notation[i].isalpha():
            move += chess_notation[i]
            i += 1
        while i < len(chess_notation) and chess_notation[i].isdigit():
            move += chess_notation[i]
            i += 1
        if 黑方:
            步 = f"黑{序号}:{move}"
        else:
            步 = f"白{序号}:{move}"

        moves_list.append(步)

        序号 += 1
        黑方 = not 黑方
    return moves_list


if __name__ == '__main__':
    # 神笔 = 纸笔五子棋(文件路径="随身五子棋.svg")
    # 神笔.完成()
    # 神笔.生成PNG(缩放=2)
    # 神笔.生成PDF()

    神笔 = 纸笔五子棋(文件路径="随身五子棋_彩版.svg", 棋盘背景色="#F5D7A1", 棋盘格颜色="#916D3A")
    神笔.白子图片 = 资源库目录("素材/围棋/白子1.png")
    神笔.黑子图片 = 资源库目录("素材/围棋/黑子1.png")
    神笔.完成前执行 = lambda: 神笔.画对局(棋局=读取棋谱(), 记录序号=否, 显示阴影=是)
    神笔.完成()
    # 神笔.生成PNG(缩放=2)
    # 神笔.生成PDF()
