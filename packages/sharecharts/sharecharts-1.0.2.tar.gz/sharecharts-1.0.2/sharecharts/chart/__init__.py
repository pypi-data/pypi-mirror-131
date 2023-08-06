from chartspy import express, Echarts
from sharecharts.algo import trend
import pandas as pd


def chart_kline(df_source, title, mas=[5, 10, 21], log_y=True, left_padding='5%', height='800px',
                with_tds=True,
                with_trend_line=True,
                with_zone=True,
                width='100%') -> Echarts:
    """
    绘制K线趋势
    :param df_source: index datetime ['open', 'high', 'low', 'close', 'volume', 'money', 'float_share', 'total_share']
    :param title:
    :param mas:
    :param with_tds:
    :param log_y: 是否是log坐标
    :param left_padding: 5%
    :param height:
    :param width:
    :return:
    """
    overlaps = []
    df_origin = df_source.copy()
    if not {'float_share', 'total_share'}.issubset(df_origin.columns):
        df_origin['float_share'] = None
        df_origin['total_share'] = None
    df = df_origin[
        ['open', 'high', 'low', 'close', 'vol', 'amount', 'float_share', 'total_share']].copy()
    df.columns = ['open', 'high', 'low', 'close', 'volume', 'money', 'float_share', 'total_share']
    if not ("HK" in df_source['ts_code'].iloc[0]):
        df['volume'] = df['volume'] * 100
        df['money'] = df['money'] * 1000
    if pd.isna(df['float_share'].iloc[0]):
        df['float_share'] = (df['volume'].sum() / df.shape[0]) * 255
        df['total_share'] = df['float_share']

    df_tds, df_trend, df_zone = trend.calc_all(df)
    if with_tds:
        tds_up = express.mark_label_echarts(df_tds[df_tds['tds'] > 0], x='time', y='high', label='tds', title='上9')
        tds_dn = express.mark_label_echarts(df_tds[df_tds['tds'] < 0], x='time', y='low', label='tds', title='下9',
                                            label_position='bottom')
        overlaps = overlaps + [tds_up, tds_dn]
    if with_zone:
        df_zone['bars'] = df_zone['end_index'] - df_zone['start_index']
        df_zone = df_zone[df_zone['bars'] > 3]
        df_zone['label'] = "天:" + df_zone['bars'].astype(int).astype(str) + " 换:" + df_zone['turn'].astype(int).astype(
            str)
        chart_zone = express.mark_area_echarts(df_zone,
                                               x1='start_time',
                                               y1='p_low', x2='end_time', y2='p_high', label='label',
                                               label_font_size=10, fill_opacity=0.7,
                                               title="中枢")
        chart_avg = express.mark_segment_echarts(df_zone,
                                                 x1='start_time', y1='avg_price', x2='end_time',
                                                 y2='avg_price',
                                                 show_label=False, label='label', label_font_size=12,
                                                 title="成交均价")
        chart_seg = express.line_echarts(df_tds[df_tds['fractal'] != 0], x='time', y='value', title="线段")
        overlaps = overlaps + [chart_zone, chart_avg, chart_seg]
    if with_trend_line:
        df_trend['pct_change'] = (((df_trend['start_price'] - df_trend['end_price']) / df_trend[
            'start_price']).abs() * 100).round(2).astype(str) + "%"
        mark_broken = express.mark_segment_echarts(
            df_trend[(df_trend['important'] > 0) & (df_trend['broken'] == 1.0)], x1='start_time', x2='end_time',
            y1='start_price', y2='end_price', label='pct_change', line_width=3, line_type='dashed', title='逆势线',
            show_label=True,
            label_font_size=12, symbol_start='none', symbol_end='arrow', label_position="end")
        mark_not_broken = express.mark_segment_echarts(df_trend[df_trend['broken'] == 0], x1='start_time',
                                                       x2='end_time', y1='start_price', y2='end_price',
                                                       label='pct_change',
                                                       line_width=5, title='趋势线', line_type='dashed',
                                                       symbol_start='none', symbol_end='arrow', label_font_size=12,
                                                       label_position="end",
                                                       show_label=True)
        overlaps = overlaps + [mark_broken, mark_not_broken]
    chart_kline = express.candlestick_echarts(df, mas=mas, width=width, height=height, title=title.split("(")[0],
                                              left=left_padding, log_y=log_y)
    chart_final = chart_kline.overlap_series(overlaps)
    legends = chart_final.options['legend']['data']
    selected = {}
    for k in legends:
        if k in ['上9', '下9', '枢纽点']:
            selected[k] = False
        else:
            selected[k] = True
    chart_final.options['legend']['selected'] = selected
    return chart_final


__all__ = ['chart_kline']
