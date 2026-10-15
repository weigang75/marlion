# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人/三月三提供
# date            :2026-06-19
# link            :https://gitee.com/march3
# python_version  :3.9
# ==============================================================================
import math
from typing import List, Tuple, Dict

CmdItem = Tuple
ProvRawData = List[CmdItem]
MapRaw = Dict[str, ProvRawData]
Polygon = List[Tuple[float, float]]


def point_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def round_coords_poly(poly: Polygon, decimal: int) -> Polygon:
    return [(round(x, decimal), round(y, decimal)) for x, y in poly]


# 仅距离过滤简化，无道格拉斯，小岛不变形
def distance_filter_poly(poly: Polygon, min_gap: float) -> Polygon:
    if len(poly) <= 2:
        return poly.copy()
    res = [poly[0]]
    last_keep = poly[0]
    for pt in poly[1:]:
        if point_distance(pt, last_keep) >= min_gap:
            res.append(pt)
            last_keep = pt
    return res


# 解析 L/H/V 转坐标列表
def convert_mid_cmds_to_poly(mid_cmds: List[CmdItem], start_x: float, start_y: float) -> Polygon:
    cx, cy = start_x, start_y
    poly = [(cx, cy)]
    for cmd in mid_cmds:
        tag = cmd[0]
        if tag == "L":
            cx, cy = cmd[1], cmd[2]
            poly.append((cx, cy))
        elif tag == "H":
            cx = cmd[1]
            poly.append((cx, cy))
        elif tag == "V":
            cy = cmd[1]
            poly.append((cx, cy))
    return poly


# 坐标转回标准 L 指令
def poly_to_L_cmds(poly: Polygon) -> List[CmdItem]:
    cmds = []
    for x, y in poly[1:]:
        cmds.append(("L", x, y))
    return cmds


# 单独处理一段 M ... L/H/V ... z
def process_single_block(block: List[CmdItem], coord_decimal: int, min_point_gap: float) -> List[CmdItem]:
    m_cmd = block[0]
    z_cmd = block[-1]
    mid_cmds = block[1:-1]
    _, mx, my = m_cmd

    raw_poly = convert_mid_cmds_to_poly(mid_cmds, mx, my)
    poly_rounded = round_coords_poly(raw_poly, coord_decimal)
    simple_poly = distance_filter_poly(poly_rounded, min_point_gap)

    new_mid = poly_to_L_cmds(simple_poly)
    new_block = [m_cmd]
    new_block.extend(new_mid)
    new_block.append(z_cmd)
    return new_block


# 对外函数名固定 unify_all_borders，旧参数全部保留兼容（sample_count/match_tol 占位无逻辑）
def unify_all_borders(
        map_raw: MapRaw,
        sample_count: int = 12,
        match_tol: float = 0.3,
        coord_decimal: int = 0,
        simplify_tol: float = 1.0,
        unhandle_prov_names: List[str] = ["澳门", "香港", "台湾", "海南"]
) -> MapRaw:
    output_map: MapRaw = {}
    for prov_name, full_cmds in map_raw.items():
        final_cmds = []
        ptr = 0
        total = len(full_cmds)
        while ptr < total:
            cur_cmd = full_cmds[ptr]
            if prov_name in unhandle_prov_names:
                final_cmds.append(cur_cmd)
                ptr += 1
                continue
            # 非M开头的杂指令原样保留
            if cur_cmd[0] != "M":
                final_cmds.append(cur_cmd)
                ptr += 1
                continue
            # 找到本段结尾 z
            block_start = ptr
            block_end = None
            for i in range(ptr, total):
                if full_cmds[i][0].lower() == "z":
                    block_end = i
                    break
            # 找不到闭合z，剩余全部原样保留
            if block_end is None:
                final_cmds.extend(full_cmds[ptr:])
                break
            # 截取完整 M ~ z 区块处理
            one_block = full_cmds[block_start:block_end + 1]
            processed_block = process_single_block(one_block, coord_decimal, simplify_tol)
            final_cmds.extend(processed_block)
            ptr = block_end + 1
        output_map[prov_name] = final_cmds
    return output_map


统一全部边界 = unify_all_borders


def 获取省中心坐标数据(完整地图数据, 保留小数点=2):
    """
    根据原始地图路径数据，计算每个省份几何包围盒中心点
    :param 完整地图数据: dict, {省名: [(M,x,y),(L,...),("z",)]}
    :return: dict {省名: (中心x, 中心y)}
    """
    center_result = {}

    # 单段M~z提取全部坐标点
    def extract_block_points(block_cmds):
        m_cmd = block_cmds[0]
        _, start_x, start_y = m_cmd
        cx, cy = start_x, start_y
        pts = [(cx, cy)]
        for cmd in block_cmds[1:-1]:
            tag = cmd[0]
            if tag == "L":
                cx, cy = cmd[1], cmd[2]
                pts.append((cx, cy))
            elif tag == "H":
                cx = cmd[1]
                pts.append((cx, cy))
            elif tag == "V":
                cy = cmd[1]
                pts.append((cx, cy))
        return pts

    # 遍历每个省份
    for 省名, cmd_list in 完整地图数据.items():
        all_points = []
        ptr = 0
        total_len = len(cmd_list)
        while ptr < total_len:
            cur = cmd_list[ptr]
            if cur[0] != "M":
                ptr += 1
                continue
            # 找到本段闭合z
            end_idx = None
            for i in range(ptr, total_len):
                if cmd_list[i][0].lower() == "z":
                    end_idx = i
                    break
            if end_idx is None:
                break
            one_block = cmd_list[ptr:end_idx + 1]
            block_pts = extract_block_points(one_block)
            all_points.extend(block_pts)
            ptr = end_idx + 1

        if not all_points:
            # 无坐标时占位(0,0)
            center_result[省名] = (0.0, 0.0)
            continue
        # 计算包围盒 min/max
        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        # 包围盒中心
        mid_x = round((min_x + max_x) / 2.0, 保留小数点)
        mid_y = round((min_y + max_y) / 2.0, 保留小数点)
        center_result[省名] = (mid_x, mid_y)
    return center_result
