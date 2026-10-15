# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from tkinter import Tk, Canvas, Label, Entry, Button, Frame, LEFT, RIGHT, TOP, BOTTOM
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
# import pyperclip
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw


class ImageSelector:
    def __init__(self, master, 加载图片按钮=False):
        self.master = master
        master.title("图片区域选择器")
        # master.attributes('-fullscreen', True)
        # 将窗口状态设置为最大化
        # master.state('zoomed')
        # 设置 master的位置
        # master.geometry("360x260+0+0")
        # 获取屏幕的宽度和高度
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # 计算右边一半屏幕的宽度和高度
        window_width = screen_width // 2
        window_height = screen_height

        # 计算窗口的起始位置（x 坐标为屏幕宽度的一半）
        x_position = screen_width // 2
        y_position = 50

        # 设置窗口的位置和大小
        master.geometry(f"{window_width}x{window_height - y_position}+{x_position}+{y_position}")

        # 用于存储原始图片和显示的图片对象
        self.original_image = None
        self.display_image = None

        # 用于记录选择区域的起始坐标和当前坐标
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        # 创建画布用于显示图片
        self.canvas = Canvas(master, width=500, height=400)
        self.canvas.pack(padx=5, pady=5)

        # 创建一个框架用于横向排列加载图片按钮和区域信息文本框等
        self.control_frame = Frame(master)
        self.control_frame.config(borderwidth=2, relief=tk.GROOVE, padx=20, pady=5)
        self.control_frame.pack()

        # 创建按钮用于加载图片并添加到框架中
        if 加载图片按钮:
            self.load_button = Button(self.control_frame, text="加载图片", command=self.load_image)
            self.load_button.pack(side=LEFT)

        # 创建文本框用于显示区域信息并添加到框架中
        self.x_label = Label(self.control_frame, text="X坐标")
        self.x_label.pack(side=LEFT)
        self.x_entry = Entry(self.control_frame, width=10)
        self.x_entry.pack(side=LEFT)

        self.y_label = Label(self.control_frame, text=" Y坐标")
        self.y_label.pack(side=LEFT)
        self.y_entry = Entry(self.control_frame, width=10)
        self.y_entry.pack(side=LEFT)

        self.width_label = Label(self.control_frame, text=" 宽度")
        self.width_label.pack(side=LEFT)
        self.width_entry = Entry(self.control_frame, width=10)
        self.width_entry.pack(side=LEFT)

        self.height_label = Label(self.control_frame, text=" 高度")
        self.height_label.pack(side=LEFT)
        self.height_entry = Entry(self.control_frame, width=10)
        self.height_entry.pack(side=LEFT)

        # 创建复制到剪切板按钮
        self.copy_button = Button(self.control_frame, text="复制到剪切板", command=self.copy_to_clipboard)
        self.copy_button.pack(side=LEFT)
        # 增加一个间隔
        self.space_label = Label(self.control_frame, text="  ")
        self.space_label.pack(side=LEFT)

        self.ok_button = Button(self.control_frame, text="确定", command=self.on_ok, width=8)
        self.ok_button.pack(side=LEFT)

        # 绑定窗口关闭协议，当点击关闭按钮时触发on_close函数
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        # 绑定鼠标事件到画布上用于选择区域
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.scale_ratio = 1.0

    def on_ok(self):
        self.select_region = self.get_selected_region()
        if self.select_region is not None:
            self.master.destroy()  # 最后执行关闭窗口操作

    def on_close(self):
        self.select_region = None
        self.master.destroy()  # 最后执行关闭窗口操作

    def get_selected_region(self):
        x = self.x_entry.get()
        y = self.y_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()
        # if x == "" or y == "" or width == "" or height == "":
        #     return 0, 0, self.original_image.width, self.original_image.height
        return int(round(float(x), 0)), \
               int(round(float(y), 0)), \
               int(round(float(width), 0)), \
               int(round(float(height), 0))
        # return int(round(int(x) / self.scale_ratio, 0)), \
        #        int(round(int(y) / self.scale_ratio, 0)), \
        #        int(round(int(width) / self.scale_ratio, 0)), \
        #        int(round(int(height) / self.scale_ratio, 0))

    def load_image(self, file_path=None):
        if file_path is None:
            file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()

            width_ratio = screen_width / self.original_image.width
            height_ratio = (screen_height - 100) / self.original_image.height

            if self.original_image.width < screen_width / 2 or self.original_image.height < screen_height / 2:
                scale_ratio = round(min(width_ratio * 0.8, height_ratio * 0.8), 2)
            else:
                # 计算图片缩放比例，以适应屏幕宽度或高度（取较大的缩放比例）
                scale_ratio = min(width_ratio, height_ratio) if min(width_ratio, height_ratio) < 1 else 1

            new_width = int(self.original_image.width * scale_ratio)
            new_height = int(self.original_image.height * scale_ratio)

            self.scale_ratio = scale_ratio
            # 对图片进行缩放
            self.original_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.display_image = ImageTk.PhotoImage(self.original_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
            # 给 self.canvas 设置边框 canvas.config(borderwidth=2, relief='sunken')
            # FLAT：边框是平的，没有3D效果。
            # RAISED：边框看起来被按下了，有3D凹陷效果。
            # SUNKEN：边框看起来被按下，有3D凸起效果。
            # GROOVE：边框看起来像凹槽。
            # RIDGE：边框看起来像脊状org/python/tkinter/tkinter.html#relief。
            self.canvas.config(borderwidth=2, relief=tk.GROOVE)
            self.canvas.config(width=new_width, height=new_height)
            self.set_default_region(0, 0, self.original_image.width, self.original_image.height)

        self.图片路径 = file_path

    def set_default_region(self, x, y, width, height):
        self.x_entry.delete(0, 'end')
        self.x_entry.insert(0, int(round(x / self.scale_ratio, 0)))
        self.y_entry.delete(0, 'end')
        self.y_entry.insert(0, int(round(y / self.scale_ratio, 0)))
        self.width_entry.delete(0, 'end')
        self.width_entry.insert(0, int(round(width / self.scale_ratio)))
        self.height_entry.delete(0, 'end')
        self.height_entry.insert(0, int(round(height / self.scale_ratio, 0)))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        self.current_x = event.x
        self.current_y = event.y
        self.update_region_info()
        self.canvas.delete("rect")  # 删除之前绘制的矩形
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", tags="rect")

    def update_region_info(self):
        x = min(self.start_x, self.current_x)
        y = min(self.start_y, self.current_y)
        width = abs(self.start_x - self.current_x)
        height = abs(self.start_y - self.current_y)
        self.set_default_region(x, y, width, height)

        # self.x_entry.delete(0, 'end')
        # self.x_entry.insert(0, x)
        # self.y_entry.delete(0, 'end')
        # self.y_entry.insert(0, y)
        # self.width_entry.delete(0, 'end')
        # self.width_entry.insert(0, width)
        # self.height_entry.delete(0, 'end')
        # self.height_entry.insert(0, height)

    def copy_to_clipboard(self):
        import pyperclip
        self.select_region = self.get_selected_region()
        if self.select_region:
            x, y, width, height = self.select_region
            content = f"({x},{y},{width},{height})"
            pyperclip.copy(content)


def 获取图片选择区域(图片路径=None, 宽高比=None):
    root = Tk()
    app = ImageSelector(root)
    if 图片路径:
        app.load_image(图片路径)
    else:
        app.load_button.invoke()
        图片路径 = app.图片路径

    root.mainloop()
    # print(pyperclip.paste())
    x, y, width, height = app.select_region
    if 宽高比 is not None:
        # 保证高除以宽的比，将区域
        if width / height != 宽高比:
            if width / height > 宽高比:
                height = int(width / 宽高比)
            else:
                width = int(height * 宽高比)
    return 图片路径, (x, y, width, height)


class 图像处理工具:
    def __init__(self, 图片文件):
        self.图片文件 = 图片文件
        self._image = Image.open(图片文件).convert('RGBA')

    @property
    def 图像数据(self):
        return self._image

    @property
    def 图像像素(self, 包含透明值=False):
        """
        将图像的像素数据转换为行和列的集合。
        :return: 行和列的集合。
        """
        宽, 高 = self._image.size
        像素数据 = self._image.load()
        像素集合 = []
        for y in range(高):
            行像素 = []
            for x in range(宽):
                pixcel = 像素数据[x, y]
                if not isinstance(pixcel, tuple):
                    行像素.append(pixcel)
                elif len(pixcel) == 3:
                    r, g, b = 像素数据[x, y]
                    行像素.append((r, g, b))
                else:
                    r, g, b, a = 像素数据[x, y]
                    if 包含透明值:
                        行像素.append((r, g, b, a))
                    else:
                        行像素.append((r, g, b))
            像素集合.append(行像素)
        return 像素集合

    @property
    def 图像大小(self):
        return self._image.size

    def 裁剪(self, 裁剪坐标和尺寸=None):
        """
        裁剪图像。
        :param 裁剪坐标和尺寸: 格式为 (裁剪坐标x, 裁剪坐标y, 裁剪宽度, 裁剪高度)。
        :return:。
        """
        from 神笔码靓.神笔库.通用工具集 import 资源库目录
        if 裁剪坐标和尺寸 is None:
            import random
            tempfile = 资源库目录(f"图片/临时文件/temp_{random.randint(10000, 99999)}.png")
            self.保存(tempfile)
            图片路径, (crop_x, crop_y, crop_width, crop_height) = 获取图片选择区域(图片路径=tempfile)
            import os
            os.remove(tempfile)
        else:
            crop_x, crop_y, crop_width, crop_height = 裁剪坐标和尺寸
        self._image = self._image.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
        return self

    def 缩放(self, 缩放倍率):
        """
        缩放图像。
        :param 缩放倍率: 缩放倍率，1.0 表示原始大小，小于 1.0 会缩小，大于 1.0 会放大。
        :return:。
        """
        # 计算缩放后的尺寸
        宽, 高 = self._image.size
        新宽 = int(宽 * 缩放倍率)
        新高 = int(高 * 缩放倍率)
        # 缩放图像
        self._image = self._image.resize((新宽, 新高))
        return self

    def 旋转(self, 旋转角度):
        """
        旋转图像。
        :param 旋转角度: 旋转角度，以度为单位。
        :return:。
        """
        self._image = self._image.rotate(旋转角度)
        return self

    def 水平翻转(self):
        """
        水平翻转图像。
        :return:。
        """
        self._image = self._image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        return self

    def 垂直翻转(self):
        """
        垂直翻转图像。
        :return:。
        """
        self._image = self._image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        return self

    def 反色(self):
        """
        反色图像。
        :return:。
        """
        # 检查图像模式是否支持反转操作，如果不支持，将其转换为 RGB 模式
        if self._image.mode not in ["RGB", "L", "I", "F"]:
            self._image = self._image.convert("RGB")
        self._image = ImageOps.invert(self._image)
        return self

    def 锐化(self, 锐化倍率):
        """
        调整图像的锐化程度。
        :param 锐化倍率: 1.0 表示原始锐化程度，小于 1.0 会降低锐化程度，大于 1.0 会增加锐化程度。
        :return:。
        """
        # 创建锐化增强器
        enhancer = ImageEnhance.Sharpness(self._image)
        # 应用锐化增强
        self._image = enhancer.enhance(锐化倍率)
        return self

    def 保存(self, 保存路径):
        """
        保存图像。
        :param 保存路径: 保存路径。
        :return:。
        """
        self._image.save(保存路径)
        return self

    def 高斯模糊(self, 模糊半径=7):
        """
        高斯模糊
        @param radius:  写中文注释：
        @return:
        """
        # 创建模糊增强器
        # 数据增强方法8：高斯模糊
        self._image = self._image.filter(ImageFilter.GaussianBlur(radius=模糊半径))
        return self

    def 饱和度调整(self, 颜色倍率):
        """

        调整图像的颜色。
        :param 颜色倍率: 1.0 表示原始颜色，小于 1.0 会降低颜色，大于 1.0 会增加颜色。
        :return:。
        """
        # 创建颜色增强器
        enhancer = ImageEnhance.Color(self._image)
        # 应用颜色增强
        self._image = enhancer.enhance(颜色倍率)
        return self

    def 对比度调整(self, 对比度倍率):
        """
        调整图像的对比度。
        :param 对比度倍率: 1.0 表示原始对比度，小于 1.0 会降低对比度，大于 1.0 会增加对比度。
        :return:。
        """
        # 创建对比度增强器
        enhancer = ImageEnhance.Contrast(self._image)

        # 应用对比度增强
        self._image = enhancer.enhance(对比度倍率)

        return self

    def 灰色(self):
        # 转换为灰度图
        self._image = self._image.convert('L')
        return self

    def 亮度调整(self, 亮度倍率):
        # 调整图片亮度
        enhancer = ImageEnhance.Brightness(self._image)
        self._image = enhancer.enhance(亮度倍率)
        return self

    def 透明默认色(self, 颜色值):
        """
        设置PNG透明的默认颜色为白色。
        :return:。
        """
        from 神笔码靓.神笔库.定义集 import 颜色
        if self._image.mode == 'RGBA':
            颜色值 = 颜色.转16进制颜色(颜色值)
            r = int(颜色值[1:3], 16)
            g = int(颜色值[3:5], 16)
            b = int(颜色值[5:7], 16)
            # 创建一个新的图像，将透明部分设置为白色
            new_image = Image.new('RGBA', self._image.size, (r, g, b, 255))
            # 将原始图像与新图像进行合成
            self._image = Image.alpha_composite(new_image, self._image)

        return self

    def 缩略图(self, 缩放比例=None, 宽=None, 高=None):
        if 缩放比例 is None:
            if 宽 is None and 高 is None:
                raise ValueError("至少提供一个缩放比例、宽或高参数")

        if 缩放比例 is not None:
            宽 = int(self._image.width * 缩放比例)
            高 = int(self._image.height * 缩放比例)
        else:
            if 宽 is None:
                宽 = int(self._image.width * (高 / self._image.height))
            if 高 is None:
                高 = int(self._image.height * (宽 / self._image.width))

        self._image.thumbnail((宽, 高))
        return self


if __name__ == '__main__':
    from 神笔码靓.神笔库 import 神笔绘图板, 资源库目录, 图像渲染设置, 颜色

    作品文件路径 = "demo.svg"
    绘图板宽, 绘图板高 = 1000, 1000
    绘图板 = 神笔绘图板(作品文件路径=作品文件路径, 宽=绘图板宽, 高=绘图板高)
    # 绘图从这里开始 高斯模糊
    # ----------------------------------------------------------------------
    图像处理 = 图像处理工具(资源库目录("图片/Python超人.png"))
    # 图像处理.缩略图(宽=20).透明默认色(颜色.白色)
    图像处理.透明默认色(颜色.黄色).高斯模糊(1)
    绘图板.贴图(图片文件=图像处理.图像数据, 高=500, 宽=500).渲染设置(图像渲染设置.像素化)
    # print(图像处理.图像像素())
    # ----------------------------------------------------------------------
    # 绘图完成
    绘图板.完成()
