# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2024-07-06
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import os
import calendar

from 神笔码靓.神笔库.神笔绘图板 import 神笔绘图板
from 神笔码靓.神笔库.定义集 import *
from 神笔码靓.神笔库.配置 import *
from 神笔码靓.神笔库.通用工具集 import *
from 神笔码靓.码靓库.共用.国家简码 import 国家简码


class 日历制作(神笔绘图板):
    def __init__(self, 作品文件路径, 年份, 标题=None, 周日为第一天=否, 横向=否):
        if 横向:
            宽, 高 = 纸张大小.A4_横向()
            self.每行月份数 = 4
        else:
            宽, 高 = 纸张大小.A4_纵向()
            self.每行月份数 = 3

        super(日历制作, self).__init__(作品文件路径=作品文件路径, 宽=宽, 高=高)
        self.年份 = 年份
        self.横向 = 横向
        if 标题 is None:
            标题 = f"{年份}年日历"
        self.标题 = 标题
        self.firstweekday = calendar.SUNDAY if 周日为第一天 else calendar.MONDAY
        self.周日为第一天 = 周日为第一天

        self.calendar_ = calendar.TextCalendar(firstweekday=self.firstweekday)
        # print(calendar_.formatmonth(theyear=2024, themonth=1))
        # print(calendar_.formatyear(theyear=2024, w=2, l=0, c=0, m=4).replace(" ", "_"), end='')
        # print(self.formatyear(theyear, w, l, c, m), end='')
        # print(calendar_.formatmonthname(theyear=2024, themonth=12, width=10, withyear=True))
        # 年份 = 2024
        # 每行月份数 = 4
        self.calendar_lines = self.calendar_.formatyear(theyear=年份, w=2, l=0, c=0, m=self.每行月份数).split("\n")
        self.months = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        self.weeks = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

        # self.months = ["January", "April", "May",
        #                "July", "August", "September", "October", "November"]
        # self.weeks = ["Su"]
        self.周末索引列表 = []

        self.中文词典 = {
            "Su": "日", "Mo": "一", "Tu": "二", "We": "三", "Th": "四", "Fr": "五", "Sa": "六",
            "January": "1月", "February": "2月", "March": "3月", "April": "4月", "May": "5月", "June": "6月",
            "July": "7月", "August": "8月", "September": "9月", "October": "10月", "November": "11月", "December": "12月"
        }

        self.文字样式 = {
            "Su": "fill:red;font-weight:bold;", "Sa": "fill:red;font-weight:bold;",
        }

        self.文字调整 = {
            "January": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-23, 0),
            "February": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-35, 0),
            "March": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-12, 0),
            "April": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-12, 0),
            "May": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(0, 0),
            "June": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-12, 0),
            "July": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-12, 0),
            "August": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-22, 0),
            "September": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-32, 0),
            "October": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-25, 0),
            "November": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-35, 0),
            "December": lambda 文字对象, 文本, 行数, 列数, 文本类型: 文字对象.平移(-35, 0),
        }

    def _创建文本行(self, 文本行: str, 行数: int, 字体大小=12, 文本类型=None):
        if len(文本行) == 0:
            return
        if self.横向:
            上边距, 左边距 = 120, 60
            cell_width, cell_height = 11.5, 24
        else:
            上边距, 左边距 = 140, 60
            cell_width, cell_height = 10, 27

        texts = 文本行.split(" ")

        col_count = 0

        line_begin, line_end = 0, 0

        for col, text in 索引列举(texts):
            if 返回长度(text) == 0:
                continue
            col_count += 返回长度(text)  # 对文字长度进行累计
            文字样式 = self.文字样式.get(text, None)
            文字调整 = self.文字调整.get(text, None)

            col_idx = (col + col_count) // 2  # 每个单元占用2个字节，比如：Su Sa _1 31，索引值就需要除以2
            # 周日和周六为周末
            if text in ["Su", "Sa"] and col_idx not in self.周末索引列表:
                self.周末索引列表.append(col_idx)

            # 对于 "周", "天"文本行， 周日和周六为红色
            if col_idx in self.周末索引列表 and 文本类型 in ["周", "天"]:
                填充颜色 = "red"
            else:
                填充颜色 = "black"

            if 文本类型 in ["周", "月"]:
                # 翻译为中文
                text_ = self.中文词典.get(text, text)
            else:
                text_ = text

            文字 = self.写字(x=(col + col_count) * cell_width + 左边距, y=行数 * cell_height + 上边距,
                         文字=text_, 字体=系统字体.微软雅黑, 字体大小=字体大小, 填充颜色=填充颜色)

            if 文本类型 in ["周"]:
                line_y = 行数 * cell_height + 上边距 + 5
                if self.周日为第一天:
                    if text == "Su":
                        line_begin = col + col_count
                    elif text == "Sa":
                        line_end = col + col_count
                else:
                    if text == "Mo":
                        line_begin = col + col_count
                    elif text == "Su":
                        line_end = col + col_count
                if line_end > line_begin:
                    self.连直线([(line_begin * cell_width + 左边距 - 10, line_y),
                              (line_end * cell_width + 左边距 + 10, line_y)])

            if 文字样式 is not None:
                文字.设置样式(文字样式)

            if 文本类型 in ["周", "月"]:
                文字.平移(0, -10)

            if 文字调整 is not None:
                文字调整(文字对象=文字, 文本=text, 行数=行数, 列数=col, 文本类型=文本类型)

    def 写标题(self):
        self.写字(x=self.宽 / 2, y=30, 文字=self.标题, 字体大小=45, 字体=系统字体.微软雅黑, 垂直基线对齐=文字垂直基线对齐.顶线对齐)

    def 写日历(self):
        for idx, calendar_line in 索引列举(self.calendar_lines[1:]):
            items = calendar_line.split(" ")
            if any(item in self.months for item in items):
                # print("月", calendar_line)
                self._创建文本行(文本行=calendar_line, 行数=idx, 字体大小=20, 文本类型="月")
            elif any(item in self.weeks for item in items):
                # print("周", calendar_line.split("  ")[0])
                self._创建文本行(文本行=calendar_line, 行数=idx, 字体大小=14, 文本类型="周")
            elif len(calendar_line) > 0:
                # print("天", calendar_line)
                self._创建文本行(文本行=calendar_line, 行数=idx, 字体大小=14, 文本类型="天")
            else:
                # print("换行",calendar_line)
                pass

    # @计算耗时
    def 创作(self):
        self.显示图框()
        self.写标题()
        self.写日历()


if __name__ == '__main__':
    年份 = 2024
    日历 = 日历制作(作品文件路径=f"{年份}年日历.svg", 年份=年份, 周日为第一天=否, 横向=否)
    日历.完成()
    # 电子书.生成PDF()
