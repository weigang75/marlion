# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-10
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os.path

from 神笔码靓.神笔库 import 神笔模板, 神笔绘图板
from 神笔码靓.神笔库.线条工具集 import *
from 神笔码靓.神笔库.通用工具集 import *


class 头像元素神笔模板(神笔模板):
    头像根目录 = "素材/漫画卡通/头像"

    def 默认颜色列表(self):
        return []

    def 获取文件键(self):
        [_, ID] = self.模板ID().split(".")
        文件 = self.获取参数("文件", ID)
        if str(文件).endswith(".svg"):
            文件 = 文件[:-4]
        性别 = self.获取参数("性别", None)
        if 性别:
            return f"{性别}/{文件}"
        else:
            return 文件

    def 元素列表(self):
        [_, ID] = self.模板ID().split(".")
        文件 = self.获取参数("文件", ID + "01")
        from 神笔码靓.神笔库.元素库 import 元素
        if isinstance(文件, 元素):
            # 1、支持元素对象
            return [文件]
        else:
            if os.path.exists(文件):
                # 2、支持指定路径的 SVG 文件
                图片 = 文件
            else:
                if not str(文件).endswith(".svg"):
                    文件名 = f"{文件}.svg"
                else:
                    文件名 = 文件

                性别 = self.获取参数("性别", "")
                # 3、系统默认路径的 SVG 文件
                图片 = 资源库目录(f"{self.头像根目录}/{性别}/{文件名}")
                if not os.path.exists(图片):
                    raise Exception(f"'{文件}'暂时不支持")

            绘图板 = self.绘图板
            替换颜色 = self.获取参数("替换颜色", None)
            SVG图片 = 绘图板.SVG贴图(x=0, y=0, 图片文件=图片)
            if 替换颜色:
                if not isinstance(替换颜色, list):
                    替换颜色 = [替换颜色]
                替换前 = self.默认颜色列表()
                for i, 替换后 in enumerate(替换颜色):
                    if i >= len(替换前):
                        break
                    SVG图片.颜色替换(替换前[i].lower(), 替换后)
                    SVG图片.颜色替换(替换前[i].upper(), 替换后)

        # SVG图片 = 绘图板.导入SVG为组(x=0, y=0, SVG图片=图片)

        return [SVG图片]


if __name__ == '__main__':
    宽, 高 = 屏幕分辨率.我的手机()
    神笔 = 神笔绘图板(作品文件路径="头像_耳朵.svg")
    神笔.神笔模板("头像.耳朵").创造元素(id_="头像_耳朵")
    神笔.完成()
