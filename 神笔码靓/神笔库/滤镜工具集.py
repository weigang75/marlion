# -*- coding:utf-8 -*-
# title           :
# description     :增强版滤镜工具集（支持复合滤镜，兼容旧版svgwrite，阴影颜色生效）
# author          :Python超人/三月三提供，AI增强
# date            :2024-05-01
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.神笔库.通用工具集 import 打印黄色消息
from 神笔码靓.神笔库.元素库 import 元素
from 神笔码靓.神笔库.定义集 import 颜色


def 滤镜警告(func):
    def wrapper(*args, **kwargs):
        滤镜名称 = func.__name__
        key = f"{滤镜名称}_已经警告"
        if not hasattr(滤镜工具集, key):
            消息 = f"注意：'{滤镜名称}'不支持无限高清"
            打印黄色消息(消息)
            setattr(滤镜工具集, key, True)
        return func(*args, **kwargs)

    return wrapper


class 滤镜工具集:
    """
    参考: https://www.51cto.com/article/652525.html
    <filter>标签用来定义滤镜，滤镜必须含有id属性来标识滤镜。图形元素通过filter=url(#id)来引用滤镜。
    feBlend:类似于CSS blend modes，描述了图像通过混合模式进行交互
    feComponentTransfer: 改变个人对RGBA通道的总称（如feFuncG）
    feComposite:一个原始的过滤器，定义像素图像交互方式
    feConvolveMatrix ：这个过滤器规定像素与他近邻将关闭交互（如：模糊、锐化）
    feDiffuseLighting ：定义了一个光源
    feDisplacementMap : 使用另一个输入值(in2)取代一个图像的像素值(in)
    feFlood : 完成过滤器的填充区域指定的颜色和alpha等级
    feGaussianBlur :输入的模糊值和标准值的偏差
    feImage ：使用其他的过滤器(像feBlend或feComposite)
    feMerge ： 允许异步过滤效果应用，而不是分层
    feMorphology : 削弱或扩张源图像
    feOffset ：用来创建阴影
    feSpecularLighting : 通过alpha创建凹凸贴图，又将其称之为”镜面”(Phong Reflection Model)
    feTile : 指图像如何重复填补空间
    feTurbulence : 允许创建纹理
    """

    def __init__(self, 高清图):
        from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
        self.高清图: 神笔绘图板 = 高清图

    # ---------- 内部辅助：构建复合滤镜 ----------
    def _构建复合滤镜(self, 操作列表, filter_id=None):
        """
        根据操作列表构建一个复合 <filter> 对象，返回 filter 对象。
        操作列表格式：[{'type':'blur','params':{...}, 'in':'可选', 'result':'可选'}, ...]
        """
        if filter_id is None:
            filter_id = 元素.生成元素id(t="f")
        filter_ = self.高清图.dwg.filter(id_=filter_id)
        # 扩展边界避免裁剪
        filter_.attribs['x'] = '-20%'
        filter_.attribs['y'] = '-20%'
        filter_.attribs['width'] = '140%'
        filter_.attribs['height'] = '140%'

        last_result = 'SourceGraphic'
        for idx, op in enumerate(操作列表):
            op_type = op['type']
            params = op.get('params', {})
            in_source = op.get('in', last_result)
            result_name = op.get('result', f'step_{idx}')

            if op_type == 'blur':
                filter_.feGaussianBlur(in_=in_source, stdDeviation=params['stdDeviation'], result=result_name)
            elif op_type == 'drop_shadow':
                # 手动实现彩色阴影（兼容旧版svgwrite）
                blur_name = f"{result_name}_blur"
                flood_name = f"{result_name}_flood"
                colorized_name = f"{result_name}_colorized"
                offset_name = f"{result_name}_offset"

                # 模糊
                filter_.feGaussianBlur(
                    in_=in_source,
                    stdDeviation=params.get('stdDeviation', 2),
                    result=blur_name
                )
                # 颜色填充
                filter_.feFlood(
                    result=flood_name,
                    flood_color=params.get('flood_color', '#000'),
                    flood_opacity=params.get('flood_opacity', 0.5)
                )
                # 将颜色应用到模糊阴影上（使用 in 操作）
                filter_.feComposite(
                    in_=flood_name,
                    in2=blur_name,
                    operator='in',
                    result=colorized_name
                )
                # 偏移
                filter_.feOffset(
                    in_=colorized_name,
                    dx=params.get('dx', 0),
                    dy=params.get('dy', 0),
                    result=offset_name
                )
                # 合并阴影和原始图形
                filter_.feMerge(layernames=[offset_name, in_source], result=result_name)
            elif op_type == 'color_matrix':
                filter_.feColorMatrix(
                    in_=in_source,
                    type=params.get('type', 'matrix'),
                    values=params.get('values', ''),
                    result=result_name
                )
            elif op_type == 'flood':
                filter_.feFlood(
                    result=result_name,
                    flood_color=params.get('color', '#000'),
                    flood_opacity=params.get('opacity', 1.0)
                )
            elif op_type == 'composite':
                filter_.feComposite(
                    in_=in_source,
                    in2=params.get('in2', 'SourceGraphic'),
                    operator=params.get('operator', 'over'),
                    k1=params.get('k1', 0),
                    k2=params.get('k2', 0),
                    k3=params.get('k3', 0),
                    k4=params.get('k4', 0),
                    result=result_name
                )
            elif op_type == 'merge':
                # 兼容旧版svgwrite：直接传入 layernames 列表
                inputs = params.get('inputs', [in_source])
                filter_.feMerge(layernames=inputs, result=result_name)
            elif op_type == 'offset':
                filter_.feOffset(
                    in_=in_source,
                    dx=params.get('dx', 0),
                    dy=params.get('dy', 0),
                    result=result_name
                )
            elif op_type == 'morphology':
                filter_.feMorphology(
                    in_=in_source,
                    operator=params.get('operator', 'dilate'),
                    radius=params.get('radius', 2),
                    result=result_name
                )
            elif op_type == 'turbulence':
                filter_.feTurbulence(
                    type=params.get('type', 'turbulence'),
                    baseFrequency=params.get('baseFrequency', 0.05),
                    numOctaves=params.get('numOctaves', 2),
                    result=result_name
                )
            elif op_type == 'displacement_map':
                filter_.feDisplacementMap(
                    in_=in_source,
                    in2=params.get('in2', 'SourceGraphic'),
                    scale=params.get('scale', 50),
                    xChannelSelector=params.get('xChannelSelector', 'R'),
                    yChannelSelector=params.get('yChannelSelector', 'G'),
                    result=result_name
                )
            else:
                raise ValueError(f"不支持的滤镜操作类型: {op_type}")

            last_result = result_name

        return filter_

    # ---------- 原有各滤镜方法（改为向元素的操作列表追加操作） ----------
    @滤镜警告
    def 形态(self, SVG元素, 形态操作='膨胀', 操作值='2'):
        operator = 'dilate' if 形态操作 == '膨胀' else 'erode'
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        filter_.feMorphology(in_='SourceGraphic', operator=operator, radius=操作值)
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    def 添加形态(self, 操作列表, 形态操作='膨胀', 操作值=2):
        operator = 'dilate' if 形态操作 == '膨胀' else 'erode'
        操作列表.append({'type': 'morphology', 'params': {'operator': operator, 'radius': 操作值}})
        return 操作列表

    @滤镜警告
    def 模糊(self, SVG元素, 模糊度=0):
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        filter_.feGaussianBlur(in_='SourceGraphic', stdDeviation=模糊度)
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    def 添加模糊(self, 操作列表, 模糊度=2):
        操作列表.append({'type': 'blur', 'params': {'stdDeviation': 模糊度}})
        return 操作列表

    @滤镜警告
    def 颜色滤镜(self, SVG元素, 颜色, x, y, 宽="100%", 高="100%", 透明度=0.5):
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        flood = filter_.feFlood(result="floodFill", x=x, y=y, width=宽, height=高, flood_color=颜色,
                                flood_opacity=透明度)
        k2 = 1 - 透明度
        if k2 < 0: k2 = 0
        composite = filter_.feComposite(in_="SourceGraphic", in2="floodFill",
                                        operator="arithmetic", k1="2", k2=k2, k3="0", k4="0")
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    def 添加颜色滤镜(self, 操作列表, 颜色, x=0, y=0, 宽="100%", 高="100%", 透明度=0.5):
        操作列表.append({'type': 'flood', 'params': {'color': 颜色, 'opacity': 透明度}, 'result': 'floodFill'})
        k2 = 1 - 透明度
        if k2 < 0: k2 = 0
        操作列表.append({
            'type': 'composite',
            'params': {'operator': 'arithmetic', 'k1': 2, 'k2': k2, 'k3': 0, 'k4': 0, 'in2': 'floodFill'},
            'in': 'SourceGraphic'
        })
        return 操作列表

    @滤镜警告
    def 光照(self, SVG元素, 光源位置, 光源颜色=颜色.黄色):
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        x, y, z = 光源位置
        diffuse_lighting = filter_.feDiffuseLighting(in_="SourceGraphic", result="light", lighting_color=光源颜色)
        diffuse_lighting.fePointLight(x=x, y=y, z=z)
        composite = filter_.feComposite(in_="SourceGraphic", in2="light", operator="arithmetic", k1="1", k2="0",
                                        k3="0", k4="0")
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    @滤镜警告
    def 扰动(self, SVG元素, 基频=0.05, 八度音阶数=2):
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        turbulence = filter_.feTurbulence(type="turbulence", baseFrequency=基频, numOctaves=八度音阶数,
                                          result="turbulence")
        displacement_map = filter_.feDisplacementMap(in2="turbulence", in_='SourceGraphic', scale="50",
                                                     xChannelSelector="R", yChannelSelector="G")
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    def 添加扰动(self, 操作列表, 基频=0.05, 八度音阶数=2, 缩放=50):
        操作列表.append(
            {'type': 'turbulence', 'params': {'baseFrequency': 基频, 'numOctaves': 八度音阶数}, 'result': 'turb'})
        操作列表.append({'type': 'displacement_map', 'params': {'in2': 'turb', 'scale': 缩放}})
        return 操作列表

    @滤镜警告
    def 立体阴影(self, SVG元素, 偏移=(2, 2), 阴影模糊度=2, 灯光颜色=颜色.白色, 灯光位置=(-50, -100, 200)):
        # 简化实现，略
        pass

    def 添加立体阴影(self, 操作列表, 偏移=(2, 2), 阴影模糊度=2, 灯光颜色=颜色.白色, 灯光位置=(-50, -100, 200)):
        dx, dy = 偏移
        操作列表.append({
            'type': 'drop_shadow',
            'params': {
                'dx': dx,
                'dy': dy,
                'stdDeviation': 阴影模糊度,
                'flood_color': 灯光颜色,
                'flood_opacity': 0.8
            }
        })
        return 操作列表

    @滤镜警告
    def 阴影(self, SVG元素, 偏移=(2, 2), 模糊度=2):
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        blur = filter_.feGaussianBlur(in_='SourceAlpha', stdDeviation=模糊度, result='blur')
        dx, dy = 偏移
        offsetBlur = filter_.feOffset(in_='blur', dx=dx, dy=dy, result='offsetBlur')
        filter_.feMerge(layernames=["offsetBlur", "SourceGraphic"])
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    # ---------- 关键修复：添加阴影操作时传递颜色参数 ----------
    def 添加阴影(self, 操作列表, 偏移=(2, 2), 模糊度=2, 颜色='#000', 透明度=0.5):
        dx, dy = 偏移
        操作列表.append({
            'type': 'drop_shadow',
            'params': {
                'dx': dx,
                'dy': dy,
                'stdDeviation': 模糊度,
                'flood_color': 颜色,
                'flood_opacity': 透明度
            }
        })
        return 操作列表

    @滤镜警告
    def 反色(self, SVG元素):
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        color_matrix = filter_.feColorMatrix(type='matrix',
                                             values='-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0')
        filter_.add(color_matrix)
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    def 添加反色(self, 操作列表):
        操作列表.append({
            'type': 'color_matrix',
            'params': {'type': 'matrix', 'values': '-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0'}
        })
        return 操作列表

    def 去色(self, SVG元素, 灰度转换系数列表=None):
        if 灰度转换系数列表 is None:
            灰度转换系数列表 = [0.299, 0.587, 0.114]
        total = sum(灰度转换系数列表)
        r, g, b = [c / total for c in 灰度转换系数列表]
        values = f'{r} {g} {b} 0 0 {r} {g} {b} 0 0 {r} {g} {b} 0 0 0 0 0 1 0'
        filter_ = self.高清图.dwg.filter(id_=元素.生成元素id(t='f'))
        color_matrix = filter_.feColorMatrix(type='matrix', values=values)
        filter_.add(color_matrix)
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()

    def 添加去色(self, 操作列表, 灰度系数列表=None):
        if 灰度系数列表 is None:
            灰度系数列表 = [0.299, 0.587, 0.114]
        total = sum(灰度系数列表)
        r, g, b = [c / total for c in 灰度系数列表]
        values = f'{r} {g} {b} 0 0 {r} {g} {b} 0 0 {r} {g} {b} 0 0 0 0 0 1 0'
        操作列表.append({'type': 'color_matrix', 'params': {'type': 'matrix', 'values': values}})
        return 操作列表

    # ---------- 新增常用组合（直接返回操作列表） ----------
    def 添加发光(self, 操作列表, 颜色1='#409EFF', 透明度1=0.7, 模糊1=8,
                 颜色2='#67C23A', 透明度2=0.8, 模糊2=4):
        操作列表.append({'type': 'blur', 'params': {'stdDeviation': 模糊1}, 'in': 'SourceAlpha', 'result': 'blur1'})
        操作列表.append({'type': 'flood', 'params': {'color': 颜色1, 'opacity': 透明度1}, 'result': 'color1'})
        操作列表.append(
            {'type': 'composite', 'params': {'operator': 'in', 'in2': 'blur1'}, 'in': 'color1', 'result': 'glow1'})
        操作列表.append({'type': 'blur', 'params': {'stdDeviation': 模糊2}, 'in': 'SourceAlpha', 'result': 'blur2'})
        操作列表.append({'type': 'flood', 'params': {'color': 颜色2, 'opacity': 透明度2}, 'result': 'color2'})
        操作列表.append(
            {'type': 'composite', 'params': {'operator': 'in', 'in2': 'blur2'}, 'in': 'color2', 'result': 'glow2'})
        操作列表.append({'type': 'merge', 'params': {'inputs': ['glow1', 'glow2']}, 'result': 'mergedGlow'})
        操作列表.append({'type': 'merge', 'params': {'inputs': ['mergedGlow', 'SourceGraphic']}})
        return 操作列表

    def 添加灰度阴影(self, 操作列表, 灰度系数=[0.33, 0.59, 0.11], 阴影偏移=(4, 4), 阴影模糊=6,
                     阴影颜色='#999', 阴影透明度=0.5, 整体模糊=1):
        total = sum(灰度系数)
        r, g, b = [c / total for c in 灰度系数]
        values = f'{r} {g} {b} 0 0 {r} {g} {b} 0 0 {r} {g} {b} 0 0 0 0 0 1 0'
        操作列表.append({'type': 'color_matrix', 'params': {'type': 'matrix', 'values': values}, 'result': 'grayscale'})
        dx, dy = 阴影偏移
        操作列表.append({
            'type': 'drop_shadow',
            'params': {
                'dx': dx,
                'dy': dy,
                'stdDeviation': 阴影模糊,
                'flood_color': 阴影颜色,
                'flood_opacity': 阴影透明度
            },
            'in': 'grayscale',
            'result': 'shadow'
        })
        操作列表.append({'type': 'blur', 'params': {'stdDeviation': 整体模糊}, 'in': 'shadow'})
        return 操作列表

    def 添加色外阴影(self, 操作列表, 颜色='#FF9800', 偏移=(3, 3), 模糊度=4, 透明度=1.0):
        dx, dy = 偏移
        操作列表.append({
            'type': 'drop_shadow',
            'params': {
                'dx': dx,
                'dy': dy,
                'stdDeviation': 模糊度,
                'flood_color': 颜色,
                'flood_opacity': 透明度
            }
        })
        return 操作列表

    # ---------- 核心方法：将操作列表应用到SVG元素 ----------
    def 应用滤镜列表(self, SVG元素, 操作列表):
        """
        根据操作列表构建复合滤镜并应用到SVG元素
        """
        if not 操作列表:
            return
        filter_ = self._构建复合滤镜(操作列表)
        self.高清图.dwg.defs.add(filter_)
        SVG元素['filter'] = filter_.get_funciri()
