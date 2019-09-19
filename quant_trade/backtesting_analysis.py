#!/usr/bin/python
# coding=utf8
import math

from .constant import *
from report_util.data_analysis_head import *

__author__ = 'Jam'
__date__ = '2018/12/6 11:30'


def get_year_yield(net_asset_value):
    benchmark_index = Environment.benchmark_index
    benchmark_timetag_to_day = [int(timetag - benchmark_index[0]) / 86400000 for timetag in benchmark_index]
    year_yield = [100 * (pow(net_asset_value[value], 252.0 / benchmark_timetag_to_day[value]) - 1) if
                  benchmark_timetag_to_day[value] > 0 else 1 for value in
                  range(len(net_asset_value))]

    return year_yield


def get_beta(benchmark_net_asset_value, strategy_net_asset_value):
    benchmark_net_asset_value_change = np.array([0]) + (
            np.array(benchmark_net_asset_value)[1:] - np.array(benchmark_net_asset_value)[:-1])
    strategy_net_asset_value_change = np.array([0]) + (
            np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
    beta_list = []
    for timetag_index in range(len(Environment.benchmark_index)):
        benchmark_net_asset_value_timetag = benchmark_net_asset_value_change[:timetag_index + 1]
        strategy_net_asset_value_timetag = strategy_net_asset_value_change[:timetag_index + 1]
        if len(benchmark_net_asset_value_timetag) > 1:
            beta = (np.cov(benchmark_net_asset_value_timetag, strategy_net_asset_value_timetag)[0, 1]) / np.var(
                benchmark_net_asset_value_timetag)
        else:
            beta = 0
        beta_list.append(beta)
    return beta_list


def get_alpha(benchmark_year_yield, strategy_year_yield, beta):
    alpha_list = []
    for i in range(len(benchmark_year_yield)):
        alpha = strategy_year_yield[i] - (3.0 + beta[i] * (benchmark_year_yield[i] - 3.0))
        alpha_list.append(alpha)
    return alpha_list


def get_volatility(strategy_net_asset_value):
    strategy_net_asset_value_change = np.array([0]) + (
            np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
    volatility_list = []
    for timetag_index in range(len(strategy_net_asset_value)):
        if timetag_index > 0:
            volatility = math.sqrt(252) * np.std(strategy_net_asset_value_change[:timetag_index + 1])
        else:
            volatility = 0
        volatility_list.append(volatility)
    return volatility_list


def get_sharp(strategy_year_yield, volatility):
    sharp_list = []
    for timetag_index in range(len(strategy_year_yield)):
        if volatility[timetag_index] > 0:
            sharp = (strategy_year_yield[timetag_index] - 3.0) / volatility[timetag_index]
        else:
            sharp = 0
        sharp_list.append(sharp)
    return sharp_list


def get_downside_risk(strategy_year_yield):
    downside_strategy_year_yield = [i if i > 3.0 else i == 0 for i in strategy_year_yield]
    downside_risk_list = []
    for timetag_index in range(len(downside_strategy_year_yield)):
        if timetag_index > 0:
            downside_risk = np.std(downside_strategy_year_yield[:timetag_index + 1])
        else:
            downside_risk = 0
        downside_risk_list.append(downside_risk)
    return downside_risk_list


def get_sortino_ratio(strategy_year_yield, downside_risk):
    sortino_ratio_list = []
    for timetag_index in range(len(Environment.benchmark_index)):
        if downside_risk[timetag_index] > 0:
            sortino_ratio = (strategy_year_yield[timetag_index] - 3.0) / downside_risk[timetag_index]
        else:
            sortino_ratio = 0
        sortino_ratio_list.append(sortino_ratio)
    return sortino_ratio_list


def get_tracking_error(benchmark_net_asset_value, strategy_net_asset_value):
    benchmark_net_asset_value_change = np.array([0]) + (
            np.array(benchmark_net_asset_value)[1:] - np.array(benchmark_net_asset_value)[:-1])
    strategy_net_asset_value_change = np.array([0]) + (
            np.array(strategy_net_asset_value)[1:] - np.array(strategy_net_asset_value)[:-1])
    benchmark_strategy_diff = benchmark_net_asset_value_change - strategy_net_asset_value_change
    # print(benchmark_strategy_diff)
    tracking_error_list = []
    for timetag_index in range(len(strategy_net_asset_value)):
        if timetag_index > 0:
            tracking_error = math.sqrt(252) * np.std(benchmark_strategy_diff[:timetag_index + 1])
        else:
            tracking_error = 0
        tracking_error_list.append(tracking_error)
    return tracking_error_list


def get_information_ratio(benchmark_year_yield, strategy_year_yield, tracking_error):
    information_ratio_list = []
    for timetag_index in range(len(strategy_year_yield)):
        if tracking_error[timetag_index] > 0:
            information_ratio = (strategy_year_yield[timetag_index] - benchmark_year_yield[timetag_index]) / \
                                tracking_error[timetag_index]
        else:
            information_ratio = 0
        information_ratio_list.append(information_ratio)
    return information_ratio_list


def get_max_drawdown(strategy_net_asset_value):
    drawdown_list = []
    for timetag_index in range(len(strategy_net_asset_value)):
        if timetag_index > 0 and max(strategy_net_asset_value[:timetag_index]):
            drawdown = 1 - strategy_net_asset_value[timetag_index] / max(strategy_net_asset_value[:timetag_index])
        else:
            drawdown = 0
        drawdown_list.append(drawdown)

    max_drawdown_list = []
    for timetag_index in range(len(drawdown_list)):
        if timetag_index > 0:
            max_drawdown = 100 * max(drawdown_list[:timetag_index + 1])
        else:
            max_drawdown = 0
        max_drawdown_list.append(max_drawdown)

    return max_drawdown_list


def main():
    print (Empty.EMPTY_STRING)
    print (Empty.EMPTY_FLOAT)
    print (Empty.EMPTY_INT)


if __name__ == "__main__":
    main()
