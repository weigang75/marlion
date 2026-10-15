# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os

from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *
from 神笔码靓.码靓库.共用.国家简码 import 国家简码


class 各国国旗(神笔绘图板):
    def 所有国家国旗(self):
        root = 资源库目录("图标/国旗")
        国旗信息列表 = []
        for fd in 获取目录文件列表(root):
            code = fd[:-4].lower().replace("cif", "")
            if code not in 国家简码:
                print("未找到：" + code)
                continue
            国名 = 国家简码[code]
            国旗信息列表.append((国名, fd))

        return 国旗信息列表

    def 自定义国旗(self):

        国旗信息列表 = [
            ("中国", "CifCn.svg"),
            ("俄罗斯", "CifRu.svg"),
            ("白俄罗斯", "CifBy.svg"),
            ("巴基斯坦", "CifPk.svg"),
            ("柬埔寨", "CifKh.svg"),
            ("老挝", "CifLa.svg"),
            ("塞尔维亚", "CifRs.svg"),
            ("伊朗", "CifIr.svg"),
            ("伊拉克", "CifIq.svg"),
            ("埃及", "CifEg.svg"),
            ("伊朗", "CifIr.svg"),
            ("沙特阿拉伯", "CifSa.svg"),
            ("委内瑞拉", "CifVe.svg"),
            ("埃及", "CifEg.svg"),
            ("坦桑尼亚", "CifTz.svg"),
            ("阿联酋", "CifAe.svg"),
            ("澳大利亚", "CifAu.svg"),
            ("巴西", "CifBr.svg"),
            ("法国", "CifFr.svg"),
            ("德国", "CifDe.svg"),
            ("美国", "CifUs.svg"),
            ("加拿大", "CifCa.svg"),
            ("瑞士", "CifCh.svg"),
            ("瑞典", "CifSe.svg"),
            ("坦桑尼亚", "CifTz.svg"),
            ("西班牙", "CifEs.svg"),
            ("英国", "CifGb.svg"),
            ("意大利", "CifIt.svg"),
            ("荷兰", "CifNl.svg"),
            ("印度", "CifIn.svg"),
            ("日本", "CifJp.svg"),
        ]

        return 国旗信息列表

    def 创作(self):
        # self.显示网格()
        root = 资源库目录("图标/国旗")
        width = 300
        height = 180
        row_idx, col_idx = 0, 0
        # for 国名, fd in self.所有国家国旗():
        for 国名, fd in self.自定义国旗():
            # #
            # if 国名 in ["中国", "俄罗斯", "巴基斯坦", "朝鲜", "柬埔寨", "老挝", "塞尔维亚", "白俄罗斯", "伊朗",
            #            "坦桑尼亚", "委内瑞拉", "伊拉克", "埃及", "法国", "美国", "英国", "韩国", "日本","德国",
            #            "印度","意大利","加拿大","沙特阿拉伯","沙特","西班牙","阿联酋","瑞士","澳大利亚","荷兰","巴西","瑞典","","",]:
            #      print(f'("{国名}", "{fd}"),')

            f = os.path.join(root, fd)

            self.SVG贴图(x=10 + col_idx * width, y=10 + row_idx * height, 图片文件=f)
            self.写字(文字=国名, x=10 + col_idx * width + width / 2.5, y=10 + row_idx * height + height / 1.2)
            col_idx += 1

            if col_idx > 4:
                col_idx = 0
                row_idx += 1
            # break


if __name__ == '__main__':
    # 作品文件路径：保存的 SVG（矢量图）格式的文件路径名称
    # 宽: 神笔绘图板也需要设置页面的宽度
    # 高: 神笔绘图板也需要设置页面的高度
    宽, 高 = 纸张大小.A4_横向(10)
    神笔 = 各国国旗(作品文件路径="各国国旗.svg", 宽=宽, 高=高)
    神笔.完成()
