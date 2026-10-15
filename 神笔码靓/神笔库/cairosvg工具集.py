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
from 神笔码靓.神笔库.配置 import *


# pip install -i https://mirrors.bfsu.edu.cn/pypi/web/simple cairosvg



class CairoSvg工具集:
    @staticmethod
    def 转为PNG(url, save_as,缩放=1):
        try:
            import cairosvg
        except Exception as e:
            raise e
        cairosvg.svg2png(url=url, write_to=save_as, dpi=96, scale=缩放)

    @staticmethod
    def 转为PDF(url, save_as):
        try:
            import cairosvg
        except Exception as e:
            raise e
        cairosvg.svg2pdf(url=url, write_to=save_as, dpi=96, scale=10)

    @staticmethod
    def 转为PS(url, save_as):
        try:
            import cairosvg
        except Exception as e:
            raise e
        cairosvg.svg2ps(url=url, write_to=save_as, dpi=96, scale=1)

    @staticmethod
    def 转为EPS(url, save_as):
        try:
            import cairosvg
        except Exception as e:
            raise e
        cairosvg.svg2eps(url=url, write_to=save_as, dpi=96, scale=10)

    @staticmethod
    def 放大SVG(url, save_as, scale=10):
        try:
            import cairosvg
        except Exception as e:
            raise e

        cairosvg.svg2svg(url=url, write_to=save_as, dpi=96, scale=scale)


def 转PNG_PDF(文件名称):
    CairoSvg工具集.转为PNG(f"../输出文件/{文件名称}.svg", f"../输出文件/{文件名称}_2.png")
    CairoSvg工具集.转为PDF(f"../输出文件/{文件名称}.svg", f"../输出文件/{文件名称}_2.pdf")
    CairoSvg工具集.转为PS(f"../输出文件/{文件名称}.svg", f"../输出文件/{文件名称}_2.ps")
    CairoSvg工具集.转为PS(f"../输出文件/{文件名称}.svg", f"../输出文件/{文件名称}_2.eps")

def to_pdf():
    # pip install i https://mirrors.bfsu.edu.cn/pypi/web/simple fpdf fpdf2
    # https://py-pdf.github.io/fpdf2/SVG.html
    # https://py-pdf.github.io/fpdf2/Tutorial-zh.html
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.image("../输出文件/钢笔字帖_床前明月光_小篆.svg")
    pdf.output("../输出文件/钢笔字帖_床前明月光_小篆.pdf")


if __name__ == '__main__':
    # 转PNG_PDF("钢笔字帖_床前明月光_小篆体")
    CairoSvg工具集.转为PNG(f"../资源库/图标/神笔码靓.svg", f"../资源库/图标/神笔码靓.png",缩放=2)
