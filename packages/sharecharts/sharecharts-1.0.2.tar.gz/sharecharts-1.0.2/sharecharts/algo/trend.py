import numpy as np
import pandas as pd
from numba import jit, float64, int64

"""
tds -> 线段 ->  中枢 
           ->  趋势

先创建对应数组
arr_price start,end
arr_seg start,end
arr_trend 
"""


def extend_arrays_if_full(arr, index):
    """
    检查各个数组，如果数组满了，移动数组里的值
    :return:
    """
    if index > arr.shape[0] - 5:
        return np.concatenate((arr, np.zeros((int(arr.shape[0] * 0.25), arr.shape[1]), dtype=np.float64)), axis=0)
    else:
        return arr


def get_arr_from_df_price(df):
    """
    准备价格数据数组
    :param df:
    :return:
    """
    df_copy = df.copy()
    df_copy['time'] = df_copy.index.astype(int) / 1000000
    arr = df_copy[['time', 'high', 'low', 'close', 'volume', 'money', 'float_share']].values
    ret = np.zeros((arr.shape[0], 11), np.float64)
    ret[:, 0:7] = arr
    ret[:, 10] = np.arange(0, ret.shape[0])
    return ret


@jit(int64[:](float64[:, :], int64, int64), cache=True)
def tds(arr: np.array, start=5, end=-1) -> np.array:
    """
    根据k线,生成tds序列以及枢纽点
    :param arr: np.array([time,high,low,close,volume,money,tds,fractal,value,idx])
    :param start: 开始计算的位置
    :param end: 结束计算的位置
    :return: np.array([time,high,low,close,volume,money,tds,fractal,value,idx])
    """
    time, high, low, clos, volume, money, float_share, tds, fractal, value, idx = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    max_idx = 0
    max_value = 0
    min_idx = 0
    min_value = 0
    end = arr.shape[0] if end == -1 else end
    for i in np.arange(start, end):
        arr[i, idx] = i
        if arr[i, clos] > arr[i - 4, clos] and arr[i - 1, clos] <= arr[i - 5, clos]:  # 正逆转
            arr[i, tds] = 1
            max_idx = i
            max_value = arr[i, high]
            if min_idx > 0:
                last_min_idx = int(min_idx)
                arr[last_min_idx, fractal] = -1
                arr[last_min_idx, value] = min_value
        elif arr[i, clos] > arr[i - 4, clos] and arr[i - 1, clos] > arr[i - 5, clos]:  # 正延续
            arr[i, tds] = arr[i - 1, tds] + 1
            if arr[i, high] > max_value:
                max_idx = i
                max_value = arr[i, high]
        elif arr[i, clos] <= arr[i - 4, clos] and arr[i - 1, clos] > arr[i - 5, clos]:  # 负逆转
            arr[i, tds] = -1
            min_idx = i
            min_value = arr[i, low]
            if max_idx > 0:
                last_max_idx = int(max_idx)
                arr[last_max_idx, fractal] = 1
                arr[last_max_idx, value] = max_value
        elif arr[i, clos] <= arr[i - 4, clos] and arr[i - 1, clos] <= arr[i - 5, clos]:  # 负延续
            arr[i, tds] = arr[i - 1, tds] - 1
            if arr[i, low] < min_value:
                min_idx = i
                min_value = arr[i, low]

    last_max_idx = int(max_idx)
    arr[last_max_idx, fractal] = 1
    arr[last_max_idx, value] = max_value

    last_min_idx = int(min_idx)
    arr[last_min_idx, fractal] = -1
    arr[last_min_idx, value] = min_value

    return np.array([last_max_idx, last_min_idx])


@jit(float64[:, :](float64[:, :]), cache=True)
def segments(arr_tds):
    """
    从TDS数组提取线段
    :param arr_tds:
    :return:
    """
    time, high, low, clos, volume, money, float_share, tds, fractal, value, idx = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    arr_fractal = arr_tds[np.abs(arr_tds[:, fractal]) > 0]
    arr_segment = np.empty((arr_fractal.shape[0] - 1, 5), np.float64)
    for i in np.arange(1, arr_fractal.shape[0]):
        arr_segment[i - 1] = np.array([arr_fractal[i - 1, value], arr_fractal[i, value], arr_fractal[i, fractal],
                                       arr_fractal[i - 1, idx],
                                       arr_fractal[i, idx]])
    return arr_segment


@jit(float64[:, :](float64[:, :], float64), cache=True)
def trends(arr_segment, filter_ratio=0.1):
    """
    :param arr_segment:np.array([start_price,end_price,cat,start_index,end_index])
    :param filter_ratio:
    :return: np.array([start_price, end_price, cat, start_index, end_index, idx, reverse_idx, broken,important])
    """
    start_price, end_price, cat, start_index, end_index, idx, reverse_idx, broken, important = 0, 1, 2, 3, 4, 5, 6, 7, 8
    ret = np.empty((arr_segment.shape[0], 9), np.float64)
    ret[0] = np.array(
        [arr_segment[0, start_price], arr_segment[0, end_price], arr_segment[0, cat], arr_segment[0, start_index],
         arr_segment[0, end_index], 0.0, 0.0, 0.0, 0.0])
    k = 1
    for i in np.arange(1, arr_segment.shape[0]):
        # 结果里还没有被打破的趋势
        not_broken = ret[np.where(ret[:k, broken] == 0.0)]
        # 比较的线段
        compare_seg = np.array(
            [arr_segment[i, start_price], arr_segment[i, end_price], arr_segment[i, cat], arr_segment[i, start_index],
             arr_segment[i, end_index], -1, not_broken[-1, idx], 0.0, 0.0])
        # 没有打破的趋势大于0,没有打破的趋势，符合区间套,后面的在前面的区间里
        if not_broken.shape[0] > 0:
            # 从后往前迭代
            for j in np.arange(not_broken.shape[0] - 1, -1, -1):
                # 如果比较的线段,跟迭代的线段方向不同，检查是否打破迭代的线段
                if compare_seg[cat] != not_broken[j, cat]:
                    is_broken = np.sign(compare_seg[cat]) == np.sign(
                        compare_seg[end_price] - not_broken[j, start_price])
                    if not is_broken:
                        # 如果没有打破,并且比较的是第一个,增加一个没有打破的线段,中断比较
                        if j == not_broken.shape[0] - 1:
                            compare_seg[idx] = k
                            ret[k] = compare_seg
                            k = k + 1
                        else:
                            # 更新比较线段的parent_idx到没有突破的迭代线段idx
                            ret[int(compare_seg[idx]), reverse_idx] = not_broken[j, idx]
                        break
                    else:
                        # 打破了这个未结束趋势,标记趋势结束
                        broken_idx = int(not_broken[j, idx])
                        ret[broken_idx, broken] = 1
                        if abs(ret[broken_idx, start_price] - ret[broken_idx, end_price]) / ret[
                            broken_idx, start_price] > filter_ratio:
                            ret[broken_idx, important] = 1
                        if j == 0 and compare_seg[idx] == -1:
                            # 初始情况,第二个线段打破了第一个线段
                            compare_seg[idx] = k
                            compare_seg[reverse_idx] = compare_seg[idx]
                            ret[k] = compare_seg
                            k = k + 1
                else:
                    # 当前比较的是同向线段
                    is_extended = np.sign(compare_seg[cat]) == np.sign(
                        compare_seg[end_price] - not_broken[j, start_price])
                    if is_extended:
                        # 迭代的同向线段,扩展终点
                        extend_idx = int(not_broken[j, idx])
                        ret[extend_idx, end_price] = compare_seg[end_price]
                        ret[extend_idx, end_index] = compare_seg[end_index]
                        # 比较的线段设置broken为1
                        ret[int(compare_seg[idx]), broken] = 1
                        # 设置比较的线段为扩展后的线段
                        compare_seg = ret[extend_idx]
                    else:
                        break

    not_broken = ret[np.where(ret[:k, broken] == 0.0)]
    for i in np.arange(0, not_broken.shape[0]):
        cur = not_broken[i]
        # 现在没有被破坏的线段标记1
        ret[int(cur[idx]), important] = 1
    return ret[:k]


@jit(float64[:](float64[:], float64[:, :], float64, float64), cache=True)
def extend_zone(arr_zone, arr_tds, quantile_low=0.15, quantile_high=0.85):
    """
    扩展zone区间，均价，累计换手率,成交量变化趋势
    :param arr_zone:
    :param arr_tds:
    :param quantile_low:
    :param quantile_high:
    :return:
    """
    zs_start_index, zs_start_price, zs_end_index, zs_end_price, zs_verify_index, zs_verify_price, zs_cat, zs_zone_high, zs_zone_low, zs_status, zs_extend_start_index, zs_extend_end_index, zs_avg_price, zs_p_low, zs_p_high, zs_turn, zs_next_index, zs_next_price, zs_volume_trend = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
    p_time, p_high, p_low, p_clos, p_volume, p_money, p_float_share = 0, 1, 2, 3, 4, 5, 6

    zs_start = int(arr_zone[zs_start_index])
    zs_end = int(arr_zone[zs_next_index])
    zs_high = max(arr_zone[zs_verify_price], arr_zone[zs_start_price])
    zs_low = min(arr_zone[zs_verify_price], arr_zone[zs_start_price])
    # 中枢前后延伸,跟中枢确认线段高低点有重合
    while min(arr_tds[zs_start][p_high], zs_high) > max(arr_tds[zs_start][p_low], zs_low) and zs_start > 0:
        zs_start = zs_start - 1
    while min(arr_tds[zs_end][p_high], zs_high) < max(arr_tds[zs_end][p_low], zs_low) and zs_end < \
            arr_tds.shape[0] - 1:
        zs_end = zs_end - 1

    zs_price = arr_tds[zs_start:zs_end]
    avg_price = np.sum(zs_price[:, p_money]) / np.sum(zs_price[:, p_volume])
    # 高低区间
    if zs_price.shape[0] > 0:
        zs_avg_price = zs_price[:, p_money] / zs_price[:, p_volume]
        zs_price_weight = np.ceil(zs_price[:, p_volume] / np.sum(zs_price[:, p_volume]) * 100).astype(np.int_)
        zs_p_r = np.repeat(zs_avg_price, zs_price_weight)
        low_high = np.quantile(zs_p_r, [quantile_low, quantile_high])
    else:
        low_high = np.array([zs_low, zs_high])
    # 换手率
    turn = np.sum(zs_price[:, p_volume] / zs_price[:, p_float_share])
    x = np.vstack((np.arange(0, zs_price.shape[0]), np.ones(zs_price.shape[0]))).T
    v_mean = np.mean(zs_price[:, p_volume])
    v_std = np.std(zs_price[:, p_volume])
    v_normal = (zs_price[:, p_volume] - v_mean) / v_std
    v_normal[np.isnan(v_normal)] = 0
    m, c = np.linalg.lstsq(x, v_normal)[0]
    # 高低点
    return np.array([arr_zone[zs_start_index], arr_zone[zs_start_price], arr_zone[zs_end_index],
                     arr_zone[zs_end_price],
                     arr_zone[zs_verify_index], arr_zone[zs_verify_price], arr_zone[zs_cat],
                     arr_zone[zs_zone_high],
                     arr_zone[zs_zone_low], arr_zone[zs_status],
                     zs_start, zs_end, avg_price, low_high[0], low_high[1], turn,
                     arr_zone[zs_next_index], arr_zone[zs_next_price], m * 1000])


@jit(float64[:, :](float64[:, :], float64[:, :], float64, float64, float64), cache=True)
def zone(arr_tds, arr_segment, min_common_ratio=0.1, quantile_low=0.15, quantile_high=0.85):
    """
     根据阈值，递归向上合并形成不同等级的线段

     :param arr_tds: tds记录
     :param arr_segment: np.array([[start_price, end_price, cat, start_index, end_index]])
     :param min_common_ratio:线段与现有中枢最小重合范围
     :param quantile_high:
     :param quantile_low:
     :return:  np.array([[start_index,start_price,end_index,end_price,zone_high,zone_low,level,status]])
     """
    xd_start_price, xd_end_price, xd_cat, xd_start_index, xd_end_index = 0, 1, 2, 3, 4  # 位置命名，方便阅读
    zs_start_index, zs_start_price, zs_end_index, zs_end_price, zs_verify_index, zs_verify_price, zs_cat, zs_zone_high, zs_zone_low, zs_status, zs_extend_start_index, zs_extend_end_index, zs_avg_price, zs_p_low, zs_p_high, zs_turn, zs_next_index, zs_next_price, zs_volume_trend = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
    default_zs_status = 0
    zs = np.empty((arr_segment.shape[0], 19), np.float64)  # 线段存放申请内存
    k = 0  # k==中枢长度
    for i in np.arange(1, arr_segment.shape[0]):
        if k > 0 and zs[k - 1, zs_status] == 0:  # 上一个中枢没有结束
            # 当前线段高低点
            max1 = max(arr_segment[i, xd_start_price], arr_segment[i, xd_end_price])
            min1 = min(arr_segment[i, xd_start_price], arr_segment[i, xd_end_price])
            # 最后一个中枢确认区间高低点
            common_high = min(max1, zs[k - 1, zs_zone_high])
            common_min = max(min1, zs[k - 1, zs_zone_low])

            min_seg_height = min((zs[k - 1, zs_zone_high] - zs[k - 1, zs_zone_low]), (max1 - min1))
            # 如果有重合,并且重合高度>指定的较短线段高度限定比例，扩展中枢
            if (common_high > common_min) and (
                    common_high - common_min) > min_seg_height * min_common_ratio:  # 当前线段跟中枢还有重合，中枢没有完成,扩展中枢到当前线段开始
                zs[k - 1, zs_end_index] = arr_segment[i, xd_start_index]
                zs[k - 1, zs_end_price] = arr_segment[i, xd_start_price]
                zs[k - 1, zs_next_index] = arr_segment[i, xd_end_index]
                zs[k - 1, zs_next_price] = arr_segment[i, xd_end_price]
                zs[k - 1, zs_zone_high] = max(arr_segment[i - 1, xd_start_price], arr_segment[i - 1, xd_end_price],
                                              zs[k - 1, zs_zone_high])
                zs[k - 1, zs_zone_low] = min(arr_segment[i - 1, xd_start_price], arr_segment[i - 1, xd_end_price],
                                             zs[k - 1, zs_zone_low])
                continue
            else:
                zs[k - 1, zs_status] = 1  # 中枢完成，检查当前线段和前两个线段是否构成新中枢
                zs[k - 1] = extend_zone(zs[k - 1], arr_tds, quantile_low, quantile_high)
        if k == 0 or zs[k - 1, zs_status] == 1:
            # 中枢起点 第一条线段终点，最后一条线段起点
            # 最近两条线段，后面的更短
            max0 = (max(arr_segment[i, xd_start_price], arr_segment[i, xd_end_price]))
            min0 = (min(arr_segment[i, xd_start_price], arr_segment[i, xd_end_price]))

            max1 = (max(arr_segment[i - 1, xd_start_price], arr_segment[i - 1, xd_end_price]))
            min1 = (min(arr_segment[i - 1, xd_start_price], arr_segment[i - 1, xd_end_price]))
            if (max1 - min1) > (max0 - min0):
                zs[k] = np.array(
                    [arr_segment[i, xd_start_index], arr_segment[i, xd_start_price],
                     arr_segment[i, xd_end_index], arr_segment[i, xd_end_price],
                     arr_segment[i, xd_end_index], arr_segment[i, xd_end_price],
                     arr_segment[i - 1, xd_cat], max(arr_segment[i, xd_start_price], arr_segment[i, xd_end_price]),
                     min(arr_segment[i, xd_start_price], arr_segment[i, xd_end_price]),
                     default_zs_status, arr_segment[i, xd_end_index], arr_segment[i, xd_end_price], 0, 0, 0, 0,
                     arr_segment[i, xd_end_index], arr_segment[i, xd_end_price], 0])
                k = k + 1
    zs[k - 1] = extend_zone(zs[k - 1], arr_tds, quantile_low, quantile_high)
    ret_left = zs[:k]
    return ret_left


def tds_array2df(arr_tds: np.array, arr_dt: np.array) -> pd.DataFrame:
    df_tds = pd.DataFrame(arr_tds,
                          columns=['time', 'high', 'low', 'close', 'volume', 'money', 'float_share', 'tds', 'fractal',
                                   'value',
                                   'idx'])
    df_tds['time'] = np.take(arr_dt, df_tds['idx'].astype(np.int32).values)
    return df_tds[['time', 'high', 'low', 'close', 'volume', 'money', 'float_share', 'tds', 'fractal', 'value',
                   'idx']]


def trends_array2df(arr_trend: np.array, arr_dt: np.array) -> pd.DataFrame:
    """
    返回中枢 [[start_index,start_price,end_index,end_price,verify_index,verify_price,cat,zone_high,zone_low,level,status]]
    :param arr_trend: np.array([start_price, end_price, cat, start_index, end_index, idx, reverse_idx, broken])
    :param arr_dt: datetime index
    :return:pd.DataFrame
    """
    df_zones = pd.DataFrame(arr_trend,
                            columns=['start_price', 'end_price', 'cat', 'start_index', 'end_index', 'idx',
                                     'reverse_idx',
                                     'broken', 'important'])
    df_zones['start_time'] = np.take(arr_dt, df_zones['start_index'].astype(np.int32).values)
    df_zones['end_time'] = np.take(arr_dt, df_zones['end_index'].astype(np.int32).values)
    return df_zones[
        ['start_index', 'start_time', 'start_price', 'end_index', 'end_time', 'end_price', 'idx', 'reverse_idx',
         'broken', 'important']]


def zones_array2df(arr_zone: np.array, arr_dt: np.array) -> pd.DataFrame:
    """
    返回中枢 [[start_index,start_price,end_index,end_price,verify_index,verify_price,cat,zone_high,zone_low,level,status]]
    :param arr_zone: zs_start_index, zs_start_price, zs_end_index, zs_end_price, zs_verify_index, zs_verify_price, zs_cat, zs_zone_high, zs_zone_low, zs_status, zs_extend_start_index, zs_extend_end_index, zs_avg_price, zs_p_low, zs_p_high, zs_turn, zs_next_index, zs_next_price, zs_volume_trend
    :param arr_dt: datetime index
    :return:pd.DataFrame
    """
    df_zones = pd.DataFrame(arr_zone, columns=['start_index', 'start_price', 'end_index', 'end_price', 'verify_index',
                                               'verify_price', 'cat', 'zone_high',
                                               'zone_low', 'status', 'extend_start_index',
                                               'extend_end_index', 'avg_price', 'p_low', 'p_high', 'turn',
                                               'next_end_index', 'next_end_price', 'volume_trend'])
    df_zones['start_time'] = np.take(arr_dt, df_zones['start_index'].astype(np.int32).values)
    df_zones['extend_start_time'] = np.take(arr_dt, df_zones['extend_start_index'].astype(np.int32).values)
    df_zones['verify_time'] = np.take(arr_dt, df_zones['verify_index'].astype(np.int32).values)
    df_zones['end_time'] = np.take(arr_dt, df_zones['end_index'].astype(np.int32).values)
    df_zones['next_end_time'] = np.take(arr_dt, df_zones['next_end_index'].astype(np.int32).values)
    df_zones['extend_end_time'] = np.take(arr_dt, df_zones['extend_end_index'].astype(np.int32).values)
    df_zones['turn'] = (df_zones['turn'] * 100).round(2)
    return df_zones[['start_index', 'start_time', 'start_price', 'end_index', 'end_time', 'end_price', 'verify_index',
                     'verify_time', 'verify_price', 'cat', 'zone_high', 'zone_low', 'status',
                     'extend_start_time', 'extend_end_time', 'avg_price', 'p_low', 'p_high', 'turn',
                     'next_end_time', 'next_end_price', 'volume_trend']]


def calc_all(df_price, trend_min_ratio=0.1, zone_min_common_ratio=0.0, zone_quantile_low=0.15, zone_quantile_high=0.85):
    arr_tds = get_arr_from_df_price(df_price)
    tds(arr_tds, 5, -1)
    arr_segment = segments(arr_tds)
    arr_trend = trends(arr_segment, trend_min_ratio)
    arr_zone = zone(arr_tds, arr_segment, min_common_ratio=zone_min_common_ratio, quantile_low=zone_quantile_low,
                    quantile_high=zone_quantile_high)
    arr_dt = df_price.index.values
    df_tds = tds_array2df(arr_tds, arr_dt)
    df_trend = trends_array2df(arr_trend, arr_dt)
    df_zone = zones_array2df(arr_zone, arr_dt)
    return df_tds, df_trend, df_zone


__all__ = ['tds', 'segments', 'zone', 'extend_zone', 'trends', 'get_arr_from_df_price', 'extend_arrays_if_full',
           'trends_array2df', 'zones_array2df', 'tds_array2df', 'calc_all']
