# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2025-06-08
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
from 神笔码靓.神笔库 import 系统字体
import os
import platform
import glob
from typing import Dict, List, Optional, Union, Tuple

import os
import platform
import glob
import re
from typing import Dict, List, Optional, Union, Tuple

class 字体路径映射:
    """手动映射字体名称到文件路径的工具类"""

    # 定义字体路径映射字典 - 根据实际系统修改
    FONT_PATH_MAPPING = {
        # 中文字体
        "SimHei": r"C:\Windows\Fonts\simhei.ttf",  # 黑体
        "LiSu": r"C:\Windows\Fonts\simli.ttf",  # 隶书
        "SimSun": r"C:\Windows\Fonts\simsun.ttc",  # 宋体
        "YouYuan": r"C:\Windows\Fonts\youyuan.ttf",  # 幼圆
        "KaiTi": r"C:\Windows\Fonts\simkai.ttf",  # 楷体
        "Microsoft YaHei": r"C:\Windows\Fonts\msyh.ttc",  # 微软雅黑
        "NSimSun": r"C:\Windows\Fonts\nsimsun.ttc",  # 新宋体
        "STXihei": r"C:\Windows\Fonts\STXIHEI.TTF",  # 华文细黑
        "STZhongsong": r"C:\Windows\Fonts\STZHONGS.TTF",  # 华文中宋
        "STKaiti": r"C:\Windows\Fonts\STKAITI.TTF",  # 华文楷体
        "STFangsong": r"C:\Windows\Fonts\STFANGSO.TTF",  # 华文仿宋
        "STHupo": r"C:\Windows\Fonts\STHUPO.TTF",  # 华文琥珀
        "FangSong": r"C:\Windows\Fonts\simsun.ttc",  # 仿宋
        "STXingkai": r"C:\Windows\Fonts\STXINGKA.TTF",  # 华文行楷
        "STXinwei": r"C:\Windows\Fonts\STXINWEI.TTF",  # 华文新魏
        "DengXian": r"C:\Windows\Fonts\deng.ttf",  # 等线
        "FZShuTi": r"C:\Windows\Fonts\FZSTK.TTF",  # 方正舒体
        "FZYaoTi": r"C:\Windows\Fonts\FZYTK.TTF",  # 方正姚体

        # 英文字体
        "Arial": r"C:\Windows\Fonts\arial.ttf",
        "Arial Black": r"C:\Windows\Fonts\ariblk.ttf",
        "Bernard MT Condensed": r"C:\Windows\Fonts\BERNHC.TTF",
        "Bodoni MT Black": r"C:\Windows\Fonts\BOD_B.TTF",
        "Broadway": r"C:\Windows\Fonts\BRADHITC.TTF",
        "Bahnschrift": r"C:\Windows\Fonts\bahnschrift.ttf",
        "Bebas Neue": r"C:\Windows\Fonts\BEBASNEUE-REGULAR.TTF",
        "Calibri": r"C:\Windows\Fonts\calibri.ttf",
        "Cambria": r"C:\Windows\Fonts\cambria.ttc",
        "Courier New": r"C:\Windows\Fonts\cour.ttf",
        "Comic Sans MS": r"C:\Windows\Fonts\comic.ttf",
        "Consolas": r"C:\Windows\Fonts\consola.ttf",
        "Georgia": r"C:\Windows\Fonts\georgia.ttf",
        "Montserrat": r"C:\Windows\Fonts\MONTserrat-REGULAR.TTF",
        "Roboto": r"C:\Windows\Fonts\ROBOTO-REGULAR.TTF",
        "Segoe UI": r"C:\Windows\Fonts\segoeui.ttf",
        "Times New Roman": r"C:\Windows\Fonts\times.ttf",
        "Tahoma": r"C:\Windows\Fonts\tahoma.ttf",
        "Trebuchet MS": r"C:\Windows\Fonts\trebuc.ttf",
        "Verdana": r"C:\Windows\Fonts\verdana.ttf",
        "Wide Latin": r"C:\Windows\Fonts\LATINWD.TTF",
    }


class 字体查找器:
    """查找系统字体文件路径的工具类"""

    def __init__(self, verbose=False):
        self.system = platform.system()
        self.font_dirs = self._get_font_directories()
        self.font_extensions = ['ttf', 'ttc', 'otf', 'fon', 'fnt']
        self.verbose = verbose

    def _get_font_directories(self) -> List[str]:
        """获取不同操作系统的字体目录"""
        if self.system == 'Windows':
            return [os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')]
        elif self.system == 'Darwin':  # macOS
            return [
                '/Library/Fonts',
                os.path.expanduser('~/Library/Fonts'),
                '/System/Library/Fonts'
            ]
        else:  # Linux 及其他系统
            return [
                '/usr/share/fonts',
                '/usr/local/share/fonts',
                os.path.expanduser('~/.fonts')
            ]

    def _search_font(self, font_name: str) -> List[Tuple[str, str]]:
        """在字体目录中搜索指定名称的字体文件，返回所有匹配项"""
        matches = []

        # 生成多种可能的搜索模式
        search_patterns = self._generate_search_patterns(font_name)

        for font_dir in self.font_dirs:
            if not os.path.exists(font_dir):
                if self.verbose:
                    print(f"字体目录不存在: {font_dir}")
                continue

            for ext in self.font_extensions:
                for pattern in search_patterns:
                    # 构建通配符模式
                    glob_pattern = os.path.join(font_dir, f"{pattern}.{ext}")

                    if self.verbose:
                        print(f"搜索模式: {glob_pattern}")

                    for font_path in glob.glob(glob_pattern, recursive=True):
                        # 获取不包含路径的文件名
                        file_name = os.path.basename(font_path)
                        # 提取不带扩展名的字体名称
                        base_name = os.path.splitext(file_name)[0]

                        matches.append((base_name, font_path))

        return matches

    def _generate_search_patterns(self, font_name: str) -> List[str]:
        """生成多种可能的搜索模式"""
        # 处理带空格的字体名称
        if ' ' in font_name:
            name_parts = font_name.split()
            # 生成可能的文件名变体：用连字符、下划线或无分隔符连接各部分
            variants = [
                font_name,
                font_name.replace(' ', ''),
                font_name.replace(' ', '-'),
                font_name.replace(' ', '_'),
            ]
        else:
            variants = [font_name]

        # 为中文字体名称添加常见前缀
        if any('\u4e00' <= char <= '\u9fff' for char in font_name):
            prefixes = ['SIM', 'ST', 'FZ']
            for prefix in prefixes:
                if not font_name.startswith(prefix):
                    variants.append(prefix + font_name)

        # 生成包含"*"的通配符模式
        wildcard_patterns = []
        for variant in variants:
            wildcard_patterns.append(variant)
            wildcard_patterns.append(f"*{variant}*")
            # 处理字体粗细后缀
            if not variant.endswith(('Bold', 'Italic', 'Regular')):
                wildcard_patterns.append(f"{variant}*")

        return list(set(wildcard_patterns))  # 去重

    def _search_font_local(self, font_name: str) -> str:
        """在当前项目的字体目录中搜索指定名称的字体文件，返回所有匹配项"""
        # 获取当前项目的字体目录
        from 神笔码靓.神笔库 import 字体文件目录
        字体目录 = 字体文件目录()
        #  self.font_extensions
        for ext in self.font_extensions:
            font_file = os.path.join(字体目录, f"{font_name}.{ext}")
            if os.path.exists(font_file):
                return font_file
        return None

    def get_font_path(self, font_name: str) -> Optional[str]:
        font_file = self._search_font_local(font_name)
        if font_file:
            return font_file
        """获取指定字体名称的文件路径"""
        # 确保 font_name 是字符串类型
        if not isinstance(font_name, str):
            if self.verbose:
                print(f"警告: 字体名称 '{font_name}' 不是字符串类型，跳过查找")
            return None

        if self.verbose:
            print(f"查找字体: {font_name}")

        # 第一步：尝试自动查找
        path = self._try_auto_search(font_name)
        if path:
            if self.verbose:
                print(f"自动查找成功: {path}")
            return path

        # 第二步：尝试从字典中查找
        path = self._try_dict_lookup(font_name)
        if path:
            if self.verbose:
                print(f"字典查找成功: {path}")
            return path

        # 都没找到
        if self.verbose:
            print(f"未找到字体: {font_name}")
        return None

    def _try_auto_search(self, font_name: str) -> Optional[str]:
        """尝试自动搜索字体"""
        # 执行搜索
        matches = self._search_font(font_name)

        if self.verbose:
            print(f"找到 {len(matches)} 个匹配项")
            for match_name, match_path in matches:
                print(f"  匹配项: {match_name} - {match_path}")

        # 如果没有找到匹配项
        if not matches:
            return None

        # 选择最佳匹配项
        best_match = self._select_best_match(font_name, matches)
        return best_match[1] if best_match else None

    def _try_dict_lookup(self, font_name: str) -> Optional[str]:
        """尝试从字典中查找字体路径"""
        # 先尝试精确匹配
        path = 字体路径映射.FONT_PATH_MAPPING.get(font_name)
        if path and os.path.exists(path):
            return path

        # 尝试不区分大小写的匹配
        font_name_lower = font_name.lower()
        for name, path in 字体路径映射.FONT_PATH_MAPPING.items():
            if name.lower() == font_name_lower and os.path.exists(path):
                return path

        return None

    def _select_best_match(self, font_name: str, matches: List[Tuple[str, str]]) -> Optional[Tuple[str, str]]:
        """从多个匹配项中选择最佳匹配"""
        if not matches:
            return None

        # 精确匹配优先
        exact_matches = [m for m in matches if m[0].lower() == font_name.lower()]
        if exact_matches:
            return exact_matches[0]

        # 部分匹配，忽略大小写
        partial_matches = [m for m in matches if font_name.lower() in m[0].lower()]
        if partial_matches:
            # 选择最短的匹配（通常更可能是正确的）
            return min(partial_matches, key=lambda x: len(x[0]))

        # 如果没有部分匹配，返回第一个匹配项
        return matches[0]

    def get_all_font_paths(self) -> Dict[str, Optional[str]]:
        """获取所有预定义字体的路径"""
        font_paths = {}
        for attr_name in dir(系统字体):
            if not attr_name.startswith('__'):
                font_name = getattr(系统字体, attr_name)
                if font_name is not None:
                    font_paths[attr_name] = self.get_font_path(font_name)
        return font_paths


def main():
    """主函数，用于命令行使用"""
    # 创建字体查找器实例，启用详细模式以便调试
    finder = 字体查找器(verbose=True)

    print(f"在 {finder.system} 系统上查找字体...")
    print("=" * 50)

    all_fonts = finder.get_all_font_paths()

    # 按字体名称排序
    sorted_fonts = sorted(all_fonts.items(), key=lambda x: x[0])

    found_count = 0
    not_found_count = 0
    dict_used_count = 0

    for font_attr, font_path in sorted_fonts:
        font_name = getattr(系统字体, font_attr)

        # 跳过非字符串类型的属性
        if not isinstance(font_name, str):
            continue

        status = "找到" if font_path else "未找到"

        # 检查是否使用了字典
        used_dict = False
        if font_path:
            # 检查这个路径是否来自字典
            for dict_name, dict_path in 字体路径映射.FONT_PATH_MAPPING.items():
                if dict_path.lower() == font_path.lower():
                    used_dict = True
                    dict_used_count += 1
                    break

        dict_info = "（使用字典）" if used_dict else ""
        print(f"{font_attr}: {font_name} - {status}{dict_info}")

        if font_path:
            print(f"  路径: {font_path}")
            found_count += 1
        else:
            not_found_count += 1

        print("-" * 50)

    print(f"查找完成: 共找到 {found_count} 个字体，其中 {dict_used_count} 个是通过字典找到的")
    print(f"未找到 {not_found_count} 个字体")


if __name__ == "__main__":
    main()