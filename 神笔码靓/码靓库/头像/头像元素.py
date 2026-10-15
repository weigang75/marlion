# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-08-13
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.码靓库.头像.头像颜色定义 import 常见发色
from 神笔码靓.神笔库 import 列表
from 神笔码靓.神笔库.元素库 import 元素, 复用元素, 元素模板, 元素组
from 神笔码靓.神笔库.定义集 import *


class 头像元素:
    def __init__(self, 绘图板, 部件配置):
        from 神笔码靓.码靓库.头像.头像模板生成器 import 头像模板生成器
        from 神笔码靓.码靓库.头像.头像文件定义 import 头像部件配置

        self.绘图板 = 绘图板
        self.头像生成器 = 头像模板生成器(绘图板)
        self.部件配置: 头像部件配置 = 部件配置
        self._微调字典调用 = {}
        self._信息 = None

    def _微调字典(self, 函数, 参数, 参数值):
        if 函数 not in self._微调字典调用.keys():
            self._微调字典调用[函数] = {}
        self._微调字典调用[函数][参数] = 参数值

    def 创建(self) -> 复用元素:
        头像 = self.创建模板().创造元素()
        if self._信息:
            self._信息.置前()
        return 头像

    def 创建模板(self) -> 元素模板:
        for 函数 in self._微调字典调用:
            参数 = self._微调字典调用[函数]
            函数(**参数)

        头像模板 = self.头像生成器.创造头像模板(部件配置=self.部件配置)
        if self._信息:
            头像模板.获取属性值("元素列表").append(self._信息)
            # self._信息.所属组.remove(self._信息)
        return 头像模板

    def 显示信息(self, 显示部件=None, 信息下移=240) -> 元素组:
        绘图板 = self.绘图板
        部件配置 = self.部件配置
        x = 0
        y = 0

        头发 = 部件配置.头发
        面部 = 部件配置.面部
        眼睛 = 部件配置.眼睛
        嘴巴 = 部件配置.嘴巴
        眉毛 = 部件配置.眉毛
        胡须 = 部件配置.胡须
        帽子 = 部件配置.帽子
        鼻子 = 部件配置.鼻子
        上身 = 部件配置.上身
        眼镜 = 部件配置.眼镜
        头发颜色 = 部件配置.头发颜色
        胡须颜色 = 部件配置.胡须颜色
        眉毛颜色 = 部件配置.眉毛颜色

        发色名 = 常见发色.获取发色名(部件配置.头发颜色)
        信息元素列表 = 列表()

        if 显示部件:
            矩形宽 = 80
            绘图板.画矩形(x=x + 160 - 矩形宽 / 2, y=y + 50 + 信息下移,
                    宽=矩形宽, 高=22, 圆角半径=5, 填充颜色=颜色.白色).透明度(0.8).添加到列表(信息元素列表)
            绘图板.写字(x=x, y=y + 信息下移, 文字=f"{eval(显示部件)}", 字体大小=13,
                   垂直基线对齐=文字垂直基线对齐.顶线对齐, 水平基线对齐=文字水平基线对齐.中点对齐).平移(160, 50).添加到列表(信息元素列表)
        else:
            矩形宽 = 280
            绘图板.画矩形(x=x + 160 - 矩形宽 / 2, y=y + 50 + 信息下移,
                    宽=矩形宽, 高=40, 圆角半径=5, 填充颜色=颜色.白色).透明度(0.8).添加到列表(信息元素列表)
            文字 = f"{头发},{面部},{眼睛},{嘴巴}"
            绘图板.写字(x=x, y=y + 信息下移, 文字=文字, 字体大小=13,
                   垂直基线对齐=文字垂直基线对齐.顶线对齐, 水平基线对齐=文字水平基线对齐.中点对齐).平移(160, 50).添加到列表(信息元素列表)
            文字 = f"{眉毛},{鼻子},{上身}{'' if 眼镜 is None else ',' + 眼镜}"
            绘图板.写字(x=x, y=y + 20 + 信息下移, 文字=文字, 字体大小=13,
                   垂直基线对齐=文字垂直基线对齐.顶线对齐, 水平基线对齐=文字水平基线对齐.中点对齐).平移(160, 50).添加到列表(信息元素列表)
        self._信息 = 绘图板.创建组合(元素列表=信息元素列表)
        return self

    def 面部(self, 面部文件):
        if isinstance(面部文件, int):
            面部文件 = f"面部{str(面部文件).rjust(2, '0')}"
        self.部件配置.面部 = 面部文件
        return self

    def 肤色(self, 肤色):
        self.部件配置.肤色 = 肤色
        return self

    def 眼睛(self, 眼睛文件):
        if isinstance(眼睛文件, int):
            眼睛文件 = f"眼睛{str(眼睛文件).rjust(2, '0')}"
        self.部件配置.眼睛 = 眼睛文件
        return self

    def 鼻子(self, 鼻子文件):
        if isinstance(鼻子文件, int):
            鼻子文件 = f"鼻子{str(鼻子文件).rjust(2, '0')}"
        self.部件配置.鼻子 = 鼻子文件
        return self

    def 耳朵(self, 耳朵文件):
        if isinstance(耳朵文件, int):
            耳朵文件 = f"耳朵{str(耳朵文件).rjust(2, '0')}"
        self.部件配置.耳朵 = 耳朵文件
        return self

    def 嘴巴(self, 嘴巴文件):
        if isinstance(嘴巴文件, int):
            嘴巴文件 = f"嘴巴{str(嘴巴文件).rjust(2, '0')}"
        self.部件配置.嘴巴 = 嘴巴文件
        return self

    def 胡须(self, 胡须文件):
        if isinstance(胡须文件, int):
            胡须文件 = f"胡须{str(胡须文件).rjust(2, '0')}"
        self.部件配置.胡须 = 胡须文件
        return self

    def 胡须颜色(self, 胡须颜色):
        self.部件配置.胡须颜色 = 胡须颜色
        return self

    def 头发(self, 头发文件):
        if isinstance(头发文件, int):
            头发文件 = f"头发{str(头发文件).rjust(2, '0')}"
        self.部件配置.头发 = 头发文件
        return self

    def 无发(self):
        self.部件配置.头发 = None
        return self

    def 头发颜色(self, 头发颜色):
        self.部件配置.头发颜色 = 头发颜色
        return self

    def 眉毛(self, 眉毛文件):
        if isinstance(眉毛文件, int):
            眉毛文件 = f"眉毛{str(眉毛文件).rjust(2, '0')}"
        self.部件配置.眉毛 = 眉毛文件
        return self

    def 眉毛颜色(self, 眉毛颜色):
        self.部件配置.眉毛颜色 = 眉毛颜色
        return self

    def 毛发颜色(self, 毛发颜色):
        self.部件配置.眉毛颜色 = 毛发颜色
        self.部件配置.头发颜色 = 毛发颜色
        self.部件配置.胡须颜色 = 毛发颜色
        return self

    def 上身(self, 上身文件):
        if isinstance(上身文件, int):
            上身文件 = f"上身{str(上身文件).rjust(2, '0')}"
        self.部件配置.上身 = 上身文件
        return self

    def 眼镜(self, 眼镜文件):
        if isinstance(眼镜文件, int):
            眼镜文件 = f"眼镜{str(眼镜文件).rjust(2, '0')}"
        self.部件配置.眼镜 = 眼镜文件
        return self

    def 帽子(self, 帽子文件):
        if isinstance(帽子文件, int):
            帽子文件 = f"帽子{str(帽子文件).rjust(2, '0')}"
        self.部件配置.帽子 = 帽子文件
        return self

    def 派对眼罩(self, 派对眼罩文件):
        if isinstance(派对眼罩文件, int):
            派对眼罩文件 = f"派对眼罩{str(派对眼罩文件).rjust(2, '0')}"
        self.部件配置.眼镜 = 派对眼罩文件
        return self

    def 眼镜在头发前(self):
        self.部件配置.眼镜在头发前 = 是
        return self

    def 显示边框(self):
        self.部件配置.显示边框 = 是
        return self

    # def 微调鼻子(self, 上下=0, 左右=0, 旋转=0, 缩放: [float, tuple[float, float]] = 1,
    #          水平翻转: bool = 否, 垂直翻转: bool = 否):
    #     self.部件配置.微调鼻子(上下=上下, 左右=左右, 旋转=旋转, 缩放=缩放, 水平翻转=水平翻转, 垂直翻转=垂直翻转)
    #     return self

    def 眼睛上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调眼睛, "上下", 位移比)
        return self

    def 眼睛左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调眼睛, "左右", 位移比)
        return self

    def 眼睛旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调眼睛, "旋转", 角度)
        return self

    def 眼睛缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调眼睛, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 眼睛垂直翻转(self):
        self._微调字典(self.部件配置.微调眼睛, "垂直翻转", 是)
        return self

    def 眼睛水平翻转(self):
        self._微调字典(self.部件配置.微调眼睛, "水平翻转", 是)
        return self

    def 微调眼睛(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调眼睛, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调眼睛, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调眼睛, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调眼睛, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调眼睛, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调眼睛, "垂直翻转", True)

    def 鼻子上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调鼻子, "上下", 位移比)
        return self

    def 鼻子左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调鼻子, "左右", 位移比)
        return self

    def 鼻子旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调鼻子, "旋转", 角度)
        return self

    def 鼻子缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调鼻子, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 鼻子垂直翻转(self):
        self._微调字典(self.部件配置.微调鼻子, "垂直翻转", 是)
        return self

    def 鼻子水平翻转(self):
        self._微调字典(self.部件配置.微调鼻子, "水平翻转", 是)
        return self

    def 微调鼻子(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调鼻子, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调鼻子, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调鼻子, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调鼻子, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调鼻子, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调鼻子, "垂直翻转", True)
        return self

    def 眉毛上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调眉毛, "上下", 位移比)
        return self

    def 眉毛左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调眉毛, "左右", 位移比)
        return self

    def 眉毛旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调眉毛, "旋转", 角度)
        return self

    def 眉毛缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调眉毛, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 眉毛垂直翻转(self):
        self._微调字典(self.部件配置.微调眉毛, "垂直翻转", 是)
        return self

    def 眉毛水平翻转(self):
        self._微调字典(self.部件配置.微调眉毛, "水平翻转", 是)
        return self

    def 微调眉毛(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调眉毛, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调眉毛, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调眉毛, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调眉毛, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调眉毛, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调眉毛, "垂直翻转", True)

    def 上身上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调上身, "上下", 位移比)
        return self

    def 上身左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调上身, "左右", 位移比)
        return self

    def 上身旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调上身, "旋转", 角度)
        return self

    def 上身缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调上身, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 上身垂直翻转(self):
        self._微调字典(self.部件配置.微调上身, "垂直翻转", 是)
        return self

    def 上身水平翻转(self):
        self._微调字典(self.部件配置.微调上身, "水平翻转", 是)
        return self

    def 微调上身(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调上身, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调上身, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调上身, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调上身, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调上身, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调上身, "垂直翻转", True)

    def 胡须上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调胡须, "上下", 位移比)
        return self

    def 胡须左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调胡须, "左右", 位移比)
        return self

    def 胡须旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调胡须, "旋转", 角度)
        return self

    def 胡须缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调胡须, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 胡须垂直翻转(self):
        self._微调字典(self.部件配置.微调胡须, "垂直翻转", 是)
        return self

    def 胡须水平翻转(self):
        self._微调字典(self.部件配置.微调胡须, "水平翻转", 是)
        return self

    def 微调胡须(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调胡须, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调胡须, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调胡须, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调胡须, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调胡须, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调胡须, "垂直翻转", True)

    def 耳朵上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调耳朵, "上下", 位移比)
        return self

    def 耳朵左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调耳朵, "左右", 位移比)
        return self

    def 耳朵旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调耳朵, "旋转", 角度)
        return self

    def 耳朵缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调耳朵, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 耳朵垂直翻转(self):
        self._微调字典(self.部件配置.微调耳朵, "垂直翻转", 是)
        return self

    def 耳朵水平翻转(self):
        self._微调字典(self.部件配置.微调耳朵, "水平翻转", 是)
        return self

    def 微调耳朵(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调耳朵, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调耳朵, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调耳朵, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调耳朵, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调耳朵, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调耳朵, "垂直翻转", True)

    def 面部上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调面部, "上下", 位移比)
        return self

    def 面部左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调面部, "左右", 位移比)
        return self

    def 面部旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调面部, "旋转", 角度)
        return self

    def 面部缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调面部, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 面部垂直翻转(self):
        self._微调字典(self.部件配置.微调面部, "垂直翻转", 是)
        return self

    def 面部水平翻转(self):
        self._微调字典(self.部件配置.微调面部, "水平翻转", 是)
        return self

    def 微调面部(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调面部, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调面部, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调面部, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调面部, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调面部, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调面部, "垂直翻转", True)

    def 头发上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调头发, "上下", 位移比)
        return self

    def 头发左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调头发, "左右", 位移比)
        return self

    def 头发旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调头发, "旋转", 角度)
        return self

    def 头发缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调头发, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 头发垂直翻转(self):
        self._微调字典(self.部件配置.微调头发, "垂直翻转", 是)
        return self

    def 头发水平翻转(self):
        self._微调字典(self.部件配置.微调头发, "水平翻转", 是)
        return self

    def 微调头发(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调头发, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调头发, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调头发, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调头发, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调头发, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调头发, "垂直翻转", True)

        return self

    def 嘴巴上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调嘴巴, "上下", 位移比)
        return self

    def 嘴巴左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调嘴巴, "左右", 位移比)
        return self

    def 嘴巴旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调嘴巴, "旋转", 角度)
        return self

    def 嘴巴缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调嘴巴, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 嘴巴垂直翻转(self):
        self._微调字典(self.部件配置.微调嘴巴, "垂直翻转", 是)
        return self

    def 嘴巴水平翻转(self):
        self._微调字典(self.部件配置.微调嘴巴, "水平翻转", 是)
        return self

    def 微调嘴巴(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调嘴巴, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调嘴巴, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调嘴巴, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调嘴巴, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调嘴巴, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调嘴巴, "垂直翻转", True)

    def 眼镜上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调眼镜, "上下", 位移比)
        return self

    def 眼镜左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调眼镜, "左右", 位移比)
        return self

    def 眼镜旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调眼镜, "旋转", 角度)
        return self

    def 眼镜缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调眼镜, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 眼镜垂直翻转(self):
        self._微调字典(self.部件配置.微调眼镜, "垂直翻转", 是)
        return self

    def 眼镜水平翻转(self):
        self._微调字典(self.部件配置.微调眼镜, "水平翻转", 是)
        return self

    def 微调眼镜(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调眼镜, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调眼镜, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调眼镜, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调眼镜, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调眼镜, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调眼镜, "垂直翻转", True)

    def 帽子上下移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调帽子, "上下", 位移比)
        return self

    def 帽子左右移动(self, 位移比: float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调帽子, "左右", 位移比)
        return self

    def 帽子旋转(self, 角度: float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调帽子, "旋转", 角度)
        return self

    def 帽子缩放(self, X缩放倍数: float = 1.0, Y缩放倍数: float = 1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调帽子, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def 帽子垂直翻转(self):
        self._微调字典(self.部件配置.微调帽子, "垂直翻转", 是)
        return self

    def 帽子水平翻转(self):
        self._微调字典(self.部件配置.微调帽子, "水平翻转", 是)
        return self

    def 微调帽子(self, 上下: float = 0, 左右: float = 0, 旋转: float = 0, 缩放: [float, tuple[float, float]] = 1,
             水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调帽子, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调帽子, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调帽子, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调帽子, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调帽子, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调帽子, "垂直翻转", True)


def 代码生成(文件名):
    template = f"""
    def {文件名}上下移动(self, 位移比:float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调{文件名}, "上下", 位移比)
        return self

    def {文件名}左右移动(self, 位移比:float):
        if 位移比 != 0:
            self._微调字典(self.部件配置.微调{文件名}, "左右", 位移比)
        return self

    def {文件名}旋转(self, 角度:float):
        if 角度 != 0:
            self._微调字典(self.部件配置.微调{文件名}, "旋转", 角度)
        return self

    def {文件名}缩放(self, X缩放倍数: float=1.0, Y缩放倍数: float=1.0):
        if X缩放倍数 != 1 or Y缩放倍数 != 1:
            self._微调字典(self.部件配置.微调{文件名}, "缩放", (X缩放倍数, Y缩放倍数))
        return self

    def {文件名}垂直翻转(self):
        self._微调字典(self.部件配置.微调{文件名}, "垂直翻转", 是)
        return self

    def {文件名}水平翻转(self):
        self._微调字典(self.部件配置.微调{文件名}, "水平翻转", 是)
        return self

    def 微调{文件名}(self, 上下:float=0, 左右:float=0, 旋转:float=0, 缩放: [float, tuple[float, float]] = 1,
                水平翻转: bool = 否, 垂直翻转: bool = 否):
        if 上下 != 0:
            self._微调字典(self.部件配置.微调{文件名}, "上下", 上下)
        if 左右 != 0:
            self._微调字典(self.部件配置.微调{文件名}, "左右", 左右)
        if 旋转 != 0:
            self._微调字典(self.部件配置.微调{文件名}, "旋转", 旋转)
        if 缩放 != 1:
            self._微调字典(self.部件配置.微调{文件名}, "缩放", 缩放)
        if 水平翻转:
            self._微调字典(self.部件配置.微调{文件名}, "水平翻转", True)
        if 垂直翻转:
            self._微调字典(self.部件配置.微调{文件名}, "垂直翻转", True)
"""
    print(template)


if __name__ == '__main__':
    for 文件名 in ["眼睛", "鼻子", "眉毛", "上身", "胡须", "耳朵", "面部", "头发", "嘴巴", "眼镜", "帽子"]:
        代码生成(文件名)
