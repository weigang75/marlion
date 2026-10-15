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
from PIL import Image

from 神笔码靓.神笔库 import 打印黄色消息
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.元素库 import 可变换元素, 样式可修改元素, 元素位置信息
from 神笔码靓.神笔库.神笔绘图板工具 import 神笔绘图板工具


class 图元素(可变换元素, 样式可修改元素):

    def 数据处理(self, 回调函数):
        数据处理回调函数列表 = self.获取属性值("数据处理回调函数列表", 空)
        if 数据处理回调函数列表 is 空:
            self.设置属性值("数据处理回调函数列表", [])
            数据处理回调函数列表 = self.获取属性值("数据处理回调函数列表", 空)

        数据处理回调函数列表.append(回调函数)

    def 获取远程图片(self, 图片链接, 保存路径=None):
        图片文件名 = getattr(self, "__图片文件名__", None)
        if 图片文件名 is not None:
            if os.path.exists(图片文件名):
                return 图片文件名
        import urllib.request
        from 神笔码靓.神笔库.通用工具集 import 资源库目录
        # 获取图片链接 的 md5
        import hashlib
        md5 = hashlib.md5()
        md5.update(图片链接.encode('utf-8'))
        md5_str = md5.hexdigest()
        if 保存路径 is None:
            保存路径 = 资源库目录("图片/临时文件")
        # 如果保存路径不存在，则创建
        if not os.path.exists(保存路径):
            os.makedirs(保存路径)
        # 获取图片链接的content-type
        content_type = urllib.request.urlopen(图片链接).info().get('Content-Type')
        if content_type.startswith("image/svg+xml"):
            图片扩展名 = ".svg"
        elif content_type.startswith("image/png"):
            图片扩展名 = ".png"
        elif content_type.startswith("image/jpg"):
            图片扩展名 = ".jpg"
        elif content_type.startswith("image/jpeg"):
            图片扩展名 = ".jpeg"
        elif content_type.startswith("image/gif"):
            图片扩展名 = ".gif"
        elif content_type.startswith("image/webp"):
            图片扩展名 = ".webp"
        else:
            raise Exception("图片格式不支持")

        图片文件 = os.path.join(保存路径, md5_str + 图片扩展名)
        setattr(self, "__图片文件名__", 图片文件)
        # 如果文件存在
        if os.path.exists(图片文件):
            return 图片文件
        # 下载图片，保存在本地
        urllib.request.urlretrieve(图片链接, 图片文件)

        return 图片文件

    def 获取图片真实宽高(self):
        图片文件 = self.获取图片文件()
        if str(图片文件).endswith(".svg"):
            宽, 高 = 神笔绘图板工具.获取SVG图片大小(图片文件)
        else:
            image = Image.open(图片文件)
            宽, 高 = image.size
            if self.高清图.开启警告:
                打印黄色消息(f"注意：图片'{图片文件}'不支持无限高清")
        return 宽, 高

    def 获取图片宽高(self):

        if hasattr(self, "_图片宽高"):
            return getattr(self, "_图片宽高")

        P = self.获取属性值

        宽 = P("宽", None)
        高 = P("高", None)

        if 宽 is None or 高 is None:
            宽, 高 = self.获取图片真实宽高()
            # scale_x, scale_y = self.获取缩放值()
            # 宽, 高 = 宽 * scale_x, 高 * scale_y

        setattr(self, "_图片宽高", (宽, 高))

        return 宽, 高

    def 获取元素范围(self):
        P = self.获取属性值
        宽, 高 = self.获取图片宽高()
        x, y = P("x"), P("y")

        最小x = x
        最小y = y
        最大x = x + 宽
        最大y = y + 高

        return 最小x, 最小y, 最大x, 最大y

    def 获取PIL图片文件(self, 图片数据, 保存路径=None):
        import io
        import PIL.Image
        from 神笔码靓.神笔库.通用工具集 import 资源库目录
        if 保存路径 is None:
            保存路径 = 资源库目录("图片/临时文件")
        import hashlib
        md5 = hashlib.md5()
        md5.update(图片数据.tobytes())
        md5_str = md5.hexdigest()

        if not os.path.exists(保存路径):
            os.makedirs(保存路径)
        图片文件 = os.path.join(保存路径, f"{md5_str}.jpg")
        图片数据.save(图片文件)
        return 图片文件

    def 获取图片文件(self):
        import PIL.Image
        P = self.获取属性值
        图片文件 = P("图片文件")
        if str(图片文件).startswith("http"):
            图片文件 = self.获取远程图片(图片链接=图片文件)
        elif isinstance(图片文件, PIL.Image.Image):
            图片文件 = self.获取PIL图片文件(图片数据=图片文件)
        return 图片文件

    def 渲染设置(self, 设置):
        self.设置样式值("image-rendering", 设置)
        return self

    def 外联图片(self, 是否外联=True):
        self.设置属性值("是否外联图片", 是否外联)
        return self

    def 构建SVG元素(self):
        P = self.获取属性值
        C = self.获取颜色值
        图片文件 = self.获取图片文件()
        # 宽, 高 = self.获取图片宽高()
        是否外联图片 = P("是否外联图片", None)

        if self.高清图.外联图片贴图 or 是否外联图片 == True:
            from 神笔码靓.神笔库.通用工具集 import 获取文件2相对文件1的路径
            xlink_href = 获取文件2相对文件1的路径(文件1=self.高清图.高清文件路径, 文件2=图片文件)
        else:
            import base64
            key = str(self.元素属性)
            if key in self.元素缓存.keys():
                # print(key)
                self.已有缓存 = 是
                return self.元素缓存[key]

            数据处理回调函数 = P("数据处理回调函数", None)

            if str(图片文件).startswith("data:image"):
                # 去除"data:image/..."前缀
                data = 图片文件.split(",")[1]
                # 将base64编码的数据解码为字节
                image_data = base64.b64decode(data)
                encoded_image = 图片文件
            else:
                encoded_image = None
                with open(图片文件, 'rb') as image_file:
                    image_data = image_file.read()

            数据处理回调函数列表 = self.获取属性值("数据处理回调函数列表", 空)
            if 数据处理回调函数列表 is not 空:
                for 数据处理回调函数 in 数据处理回调函数列表:
                    if callable(数据处理回调函数):
                        image_data = 数据处理回调函数(image_data)

            if encoded_image is None:
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                if str(图片文件).endswith(".svg"):
                    encoded_image = "data:image/svg+xml;base64," + encoded_image
                elif str(图片文件).endswith(".png"):
                    encoded_image = "data:image/png;base64," + encoded_image
                elif str(图片文件).endswith(".jpg"):
                    encoded_image = "data:image/jpg;base64," + encoded_image
                elif str(图片文件).endswith(".jpeg"):
                    encoded_image = "data:image/jpeg;base64," + encoded_image
                elif str(图片文件).endswith(".gif"):
                    encoded_image = "data:image/gif;base64," + encoded_image
                elif str(图片文件).endswith(".webp"):
                    encoded_image = "data:image/webp;base64," + encoded_image
                else:
                    raise Exception("图片格式不支持")

            xlink_href = encoded_image

        img = self.dwg.image(xlink_href, insert=(P("x"), P("y")),
                             # opacity=P("透明度", 1.0),
                             alignment_baseline="middle",
                             id=self.获取元素id(t="im"))
        宽_ = P("宽", None)
        高_ = P("高", None)

        if 宽_ is not None or 高_ is not None:
            if 高_ is None:
                图宽, 图高 = self.获取图片宽高()
                高_ = round(图高 / 图宽 * 宽_, 2)
            elif 宽_ is None:
                图宽, 图高 = self.获取图片宽高()
                宽_ = round(图宽 / 图高 * 高_, 2)

        if 宽_ is not None:
            img.attribs["width"] = 宽_
        if 高_ is not None:
            img.attribs["height"] = 高_

        self.属性修改处理(img)

        if self.高清图.外联图片贴图 or 是否外联图片 == True:
            pass
        else:
            self.元素缓存[key] = img

        return img
