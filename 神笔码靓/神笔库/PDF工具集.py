# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-06-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os
from 神笔码靓.神笔库.通用工具集 import *
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *


class PDF工具集:

    @staticmethod
    def 图片剪切(图片文件, 缩放, 裁剪大小):
        from PIL import Image
        前图片文件 = 图片文件[:-4] + "_前." + 图片文件[-3:]
        if os.path.exists(前图片文件):
            os.remove(前图片文件)
        os.rename(图片文件, 前图片文件)
        # 打开原始图片
        image = Image.open(前图片文件)
        original_width, original_height = image.size
        crop_width, crop_height = 裁剪大小
        crop_width, crop_height = crop_width * 缩放, crop_height * 缩放
        # 获取原始图片的宽度和高度

        # 判断要剪切的宽高是否超出原始图片尺寸
        if crop_width > original_width:
            crop_width = original_width
        if crop_height > original_height:
            crop_height = original_height

        if crop_height == original_height and crop_width == original_width:
            # image.save(图片文件)
            image.close()
            os.rename(前图片文件, 图片文件)
            return 图片文件
        # 进行剪切操作，按照左上角保留指定宽高的区域
        cropped_image = image.crop((0, 0, crop_width, crop_height))
        # 保存剪切后的图片
        cropped_image.save(图片文件)

        os.remove(前图片文件)
        return 图片文件

    @staticmethod
    def 转为PNG(SVG文件, 保存为PNG, 缩放=1, 窗口大小=None, 裁剪大小=None):
        chrome_path = os.path.abspath(谷歌浏览器根目录)
        if os.path.exists(chrome_path):
            os.environ["PATH"] = os.environ["PATH"] + r";" + chrome_path
        else:
            raise Exception("请在 配置.py 文件中设置谷歌浏览器的路径")

        url = os.path.abspath(SVG文件)
        save_as = os.path.abspath(保存为PNG)

        if not os.path.exists(url):
            raise Exception("文件不存在", url)

        # url = "file:///G:/works/gitcode/code_painter/神笔库/SVG缩放.html?三国象棋_彩版.svg"
        # --print-to-pdf-no-header
        # window_size = "--window-size=1412,1732"
        if 缩放 == 1:
            scale = ""
        else:
            scale = f"--force-device-scale-factor={缩放}"
        if 窗口大小 is None:
            window_size = ""
        else:
            width, height = 窗口大小
            window_size = f"--window-size={width},{height}"
        cmd = f'{谷歌浏览器执行文件} --headless --no-sandbox --disable-gpu {window_size} {scale} ' \
              f'--hide-scrollbars --screenshot="{save_as}" "{url}"'
        # 参考：https://peter.sh/experiments/chromium-command-line-switches
        # # --start-fullscreen  --start-maximized  --disable-overscroll-edge-effect
        code = os.system(cmd)
        print(cmd)
        if code == 0:
            if 裁剪大小:
                PDF工具集.图片剪切(图片文件=保存为PNG, 缩放=缩放, 裁剪大小=裁剪大小)
            print("PNG生成成功，保存位置：", 保存为PNG)
        else:
            print("PNG生成失败，chrome 返回码 =", code)
        return 保存为PNG

    @staticmethod
    def 转为PDF(SVG文件, 保存为PDF):
        # import os
        import subprocess  # 新增：用subprocess替代os.system，捕获输出
        chrome_path = os.path.abspath(谷歌浏览器根目录)
        if os.path.exists(chrome_path):
            os.environ["PATH"] = os.environ["PATH"] + r";" + chrome_path
        else:
            raise Exception("请在 配置.py 文件中设置谷歌浏览器的路径")

        url = os.path.abspath(SVG文件)
        save_as = os.path.abspath(保存为PDF)

        if not os.path.exists(url):
            raise Exception("文件不存在", url)

        # --print-to-pdf-no-header
        cmd = f'{谷歌浏览器执行文件} --headless --no-sandbox --disable-gpu --print-to-pdf="{save_as}" "{url}"'

        # ========== 核心修改：替换os.system，捕获并处理Chrome输出 ==========
        # 方式1：隐藏Chrome的乱码输出（推荐，最简）
        try:
            # 执行命令，将Chrome的stdout/stderr重定向到空设备，不打印乱码
            code = subprocess.call(
                cmd,
                stdout=subprocess.DEVNULL,  # 屏蔽标准输出（Chrome的乱码日志）
                stderr=subprocess.DEVNULL  # 屏蔽错误输出（如有）
            )
        except Exception as e:
            print("执行Chrome命令出错：", str(e))
            code = -1
        # =================================================================

        if code == 0:
            print("PDF生成成功，保存位置：", 保存为PDF)
        else:
            print("PDF生成失败，chrome 返回码 =", code)
        return 保存为PDF

    # @staticmethod
    # def 转为PDF(SVG文件, 保存为PDF):
    #     chrome_path = os.path.abspath(谷歌浏览器根目录)
    #     if os.path.exists(chrome_path):
    #         os.environ["PATH"] = os.environ["PATH"] + r";" + chrome_path
    #     else:
    #         raise Exception("请在 配置.py 文件中设置谷歌浏览器的路径")
    #
    #     url = os.path.abspath(SVG文件)
    #     save_as = os.path.abspath(保存为PDF)
    #
    #     if not os.path.exists(url):
    #         raise Exception("文件不存在", url)
    #
    #     # --print-to-pdf-no-header
    #     cmd = f'{谷歌浏览器执行文件} --headless --no-sandbox --disable-gpu --print-to-pdf="{save_as}" "{url}"'
    #     code = os.system(cmd)
    #     if code == 0:
    #         print("PDF生成成功，保存位置：", 保存为PDF)
    #     else:
    #         print("PDF生成失败，chrome 返回码 =", code)
    #     return 保存为PDF

    # https://cloud.tencent.com.cn/developer/information/%E4%BD%BF%E7%94%A8chrome%20headless%E9%80%89%E9%A1%B9%E6%89%93%E5%8D%B0%E5%88%B0pdf%E7%9A%84%E5%85%B6%E4%BB%96%E9%80%89%E9%A1%B9-salon
    # 使用Chrome Headless选项打印到PDF的其他选项包括：
    #
    # 1.页面大小和方向：可以通过设置--print-paper-size参数来指定页面的大小，
    #   例如--print-paper-size=A4。可以通过设置--print-orientation参数来指定页面的方向，例如--print-orientation=landscape。
    # 2.边距设置：可以通过设置--margin-top、--margin-bottom、--margin-left和--margin-right参数来调整页面的边距大小，
    #   例如--margin-top=10mm。
    # 3.页面缩放：可以通过设置--print-scale参数来调整页面的缩放比例，
    #   例如--print-scale=0.8。
    # 4.头部和尾部内容：可以通过设置--header-template和--footer-template参数来添加自定义的头部和尾部内容，
    #   例如--header-template=file:///path/to/header.html。
    # 5.打印背景图像：可以通过设置--print-background参数来决定是否打印页面的背景图像，
    #   例如--print-background=false。
    # 6.忽略CSS样式：可以通过设置--disable-css-media参数来禁用页面中的CSS样式，
    #   例如--disable-css-media。
    # 7.禁用JavaScript：可以通过设置--disable-javascript参数来禁用页面中的JavaScript脚本，
    #   例如--disable-javascript。
    # 8.设置页面的等待时间：可以通过设置--virtual-time-budget参数来指定页面的加载等待时间，
    #   例如--virtual-time-budget=5000。
    # 9.自定义页面内容：可以通过设置--custom-header参数来添加自定义的HTTP头部信息，
    #   例如--custom-header=Authorization: Bearer token。
    # 10.保存PDF文件：可以通过设置--print-to-pdf参数来保存PDF文件，
    #   例如--print-to-pdf=/path/to/output.pdf。

    # 开发者模式
    # --disable-extensions：启动 Chrome 时禁用所有扩展程序。
    # --enable-automation：允许自动化脚本控制浏览器。
    # --headless：在无头模式下启动 Chrome，没有图形用户界面。
    # --no-sandbox：绕过 Chrome 的沙盒模式，这通常用于开发和测试，但不推荐在生产环境中使用。
    # --remote-debugging-port=<port>：启动远程调试服务器，指定端口。
    # --user-data-dir=<path>：指定用户数据目录，用于隔离不同的配置和数据。
    # 启动选项
    # --start-maximized：启动时最大化浏览器窗口。
    # --start-fullscreen：启动时全屏显示浏览器窗口。
    # --incognito：以无痕模式启动浏览器。
    # --new-window：打开新的浏览器窗口。
    # --new-tab：打开新的浏览器标签页。
    # 调试和分析
    # --dump-dom：在启动时将页面 DOM 结构输出到控制台。
    # --js-flags="--expose-gc"：启动时启用垃圾收集器暴露。
    # --preserve-log：保留日志文件，即使它们没有被查看过。
    # --use-mock-keychain：启动时使用模拟的密钥链。
    # --window-size=<width>x<height>：启动时设置浏览器窗口大小。
    # 性能和内存
    # --disk-cache-size=<size>：设置磁盘缓存大小。
    # --disable-gpu：禁用 GPU 加速，这可能有助于解决与硬件加速相关的性能问题。
    # --disable-dev-shm-usage：禁用共享内存，这在某些情况下可以避免内存不足的错误。
    # --mute-audio：启动时静音音频。
    # --no-sandbox：绕过 Chrome 的沙盒模式（仅限开发者，不推荐在生产环境中使用）。
    # --single-process：以单进程模式启动 Chrome。
    # 网络
    # --proxy-server=<proxy-server>：设置代理服务器地址。
    # --no-proxy：不通过代理访问指定的网址。
    # --use-fake-ui-for-media-stream：使用模拟的用户界面来捕获媒体流。
    # 实验性功能
    # --enable-blink-features=<feature>：启用 Blink 引擎的实验性功能。
    # --enable-experimental-web-platform-features：启用实验性的 Web 平台功能。

    @staticmethod
    def 转为PDF2(SVG文件, 保存为PDF):
        import subprocess
        import logging

        chrome_path = os.path.abspath(谷歌浏览器根目录)
        if os.path.exists(chrome_path):
            os.environ["PATH"] = os.environ["PATH"] + r";" + chrome_path
        else:
            raise Exception("请在 配置.py 文件中设置谷歌浏览器的路径")

        url = os.path.abspath(SVG文件)
        save_as = os.path.abspath(保存为PDF)

        if not os.path.exists(url):
            raise Exception("文件不存在", url)

        logging.basicConfig(filename='command_log.txt', level=logging.INFO)

        def run_command(command):
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                logging.info(f"Command: {command}\nOutput: {result.stdout}\nError: {result.stderr}")
                return result.stdout
            except Exception as e:
                logging.error(f"Error running command {command}: {e}")
                return None

        # 示例命令
        command_to_run = f'{谷歌浏览器执行文件} --headless --no-sandbox --disable-gpu --print-to-pdf="{save_as}" "{url}"'
        output = run_command(command_to_run)
        if output:
            print(output)

    @staticmethod
    def PDF转PNG服务(PDF文件, 保存目录=None, 多张图片=是, dpi=300):
        # Stirling-PDF.exe
        import requests
        import urllib.parse
        import zipfile

        url = 'http://localhost:8080/api/v1/convert/pdf/img'
        input_file_name = os.path.basename(PDF文件)
        files = {
            'fileInput': (input_file_name, open(PDF文件, 'rb'), 'application/pdf')
        }
        if 多张图片:
            图像结果类型 = "multiple"
        else:
            图像结果类型 = "single"

        颜色类型 = "color"  # color greyscale blackwhite

        data = {
            'imageFormat': 'png',  # png jpeg jpg gif
            'singleOrMultiple': 图像结果类型,  # multiple single
            'colorType': 颜色类型,
            'dpi': dpi
        }

        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            # Decode the filename from URL encoding
            filename = urllib.parse.unquote(response.headers['content-disposition'].split('=')[-1])
            filename = filename.strip('"')
            if 多张图片:
                filename = os.path.join(作品输出目录(), "temp", filename)
                filename = os.path.normpath(filename)
                安全创建目录(filename)

                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"File '{filename}' saved successfully.")
                # extract_folder = os.path.dirname(filename)
                if 保存目录 is None:
                    extract_folder = os.path.splitext(filename)[0]
                else:
                    extract_folder = os.path.normpath(保存目录)

                # 创建一个解压缩对象
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    # 解压缩所有文件到指定目标文件夹
                    zip_ref.extractall(extract_folder)

                print(f"Zip文件 '{filename}' 已成功解压缩到文件夹 '{extract_folder}' 中。")
                os.remove(filename)
            else:
                if 保存目录 is not None:
                    filename = os.path.join(保存目录, filename)
                else:
                    filename = os.path.join(作品输出目录(), "temp", filename)
                filename = os.path.normpath(filename)
                with open(filename, 'wb') as f:
                    f.write(response.content)

                return filename
        else:
            print("Failed to download the file.")


if __name__ == '__main__':
    # PDF工具集.转为PDF(r"../输出文件/神笔绘图板样例.svg", "../输出文件/十二面体展开图.pdf")

    # 成果馆目录("生活娱乐/飞行棋.pdf")
    # 作品输出目录("足球展开图_纹理4.pdf")
    PDF工具集.PDF转PNG服务(PDF文件=成果馆目录("学习/篆体甲骨文字典.pdf"), 多张图片=是,
                           保存目录=作品输出目录(子目录名="篆体甲骨文字典"))
