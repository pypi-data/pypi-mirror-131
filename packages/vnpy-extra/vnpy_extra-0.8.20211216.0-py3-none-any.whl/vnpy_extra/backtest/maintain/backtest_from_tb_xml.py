#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/12/14 11:24
@File    : backtest_from_tb_xml.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import itertools
import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from datetime import date, timedelta
from typing import Optional, Iterator
from typing import Tuple, List

from ibats_utils.decorators import get_once_call
from ibats_utils.transfer import str_2_date
from vnpy.trader.constant import Interval

from vnpy_extra.backtest import CrossLimitMethod
from vnpy_extra.backtest.commons import bulk_backtest_with_backtest_params_iter
from vnpy_extra.backtest.cta_strategy.template import CtaTemplate
from vnpy_extra.constants import BASE_POSITION, STOP_OPENING_POS_PARAM
from vnpy_extra.db.orm import StrategyInfo, StrategyBacktestStats
from vnpy_extra.db.tb.import_tb_param_xml import get_name_vt_symbol_param_list_dic_by_dir

logger = logging.getLogger(__name__)
warning_once = get_once_call(logger.warning)


def get_backtest_params_iter_from_stats_list(
        vt_symbol, param_list, start, end, strategy_cls: CtaTemplate
) -> Tuple[List[str], Iterator[Tuple[dict, list, Optional[StrategyBacktestStats]]]]:
    end = date.today() if end is None else str_2_date(end)
    start = (end - timedelta(days=365 * 5)) if start is None else str_2_date(start)
    engine_kwargs = {
        'vt_symbol': vt_symbol,
        'end': end,
        'start': start,
        'cross_limit_method': CrossLimitMethod.open_price,
        'interval': Interval.MINUTE
    }
    param_name_list = None
    param_values_list = []
    for param_dic in param_list:
        if param_name_list is None:
            param_name_list = []
            for param_name in param_dic.keys():
                if param_name in strategy_cls.parameters:
                    param_name_list.append(param_name)
                else:
                    warning_once(f"{param_name} 字段未在 {strategy_cls.__name__} 的 parameters 中定义")

        # 整理策略参数
        param_values = []
        for param_name in param_name_list:
            if param_name == BASE_POSITION:
                param_values.append(1)
            elif param_name == STOP_OPENING_POS_PARAM:
                param_values.append(0)
            else:
                param_values.append(param_dic.get(param_name, None))

        param_values_list.append(param_values)

    return param_name_list, itertools.product([engine_kwargs], param_values_list, [None])


def backtest_from_tb_xml(
        dir_path: str, start: Optional[str] = None, end: Optional[str] = None, pool_size=0,
        file_name_include_symbol=False, ignore_existed_backtest=True,
        pre_call_before_backtest=None, **kwargs):
    if pre_call_before_backtest:
        pre_call_before_backtest()

    if pool_size < 0:
        pool_size = multiprocessing.cpu_count()

    if pool_size <= 1:
        pool = None
    else:
        pool = ProcessPoolExecutor(max_workers=pool_size)

    name_vt_symbol_param_list, tot_count = get_name_vt_symbol_param_list_dic_by_dir(dir_path)

    def get_iter():
        for key, vt_symbol_param_list in name_vt_symbol_param_list.items():
            for key2, value in vt_symbol_param_list.items():
                yield key, key2, value

    logger.info(f"总计 {tot_count} 个[策略类/品种]组合将被回测")
    for num, (strategy_class_name, vt_symbol, param_list) in enumerate(get_iter(), start=1):
        try:
            strategy_cls = StrategyInfo.get_strategy_class_by_name(strategy_class_name)
            module_name = strategy_cls.__module__
        except ModuleNotFoundError:
            logger.exception(f"{strategy_class_name} 不存在，模块名称错误，忽略")
            continue
        except AttributeError:
            logger.exception(f"{strategy_class_name} 不存在，类名称错误，忽略")
            continue

        from vnpy_extra.backtest.cta_strategy.run import default_engine_param_key_func

        param_name_list, backtest_params_iter = get_backtest_params_iter_from_stats_list(
            vt_symbol, param_list, start, end, strategy_cls)
        bulk_backtest_kwargs = dict(
            strategy_cls=strategy_cls,
            multi_symbols=False,
            param_name_list=param_name_list,
            backtest_params_iter=backtest_params_iter,
            engine_param_key_func=default_engine_param_key_func,
            output_available_only=False,
            open_browser_4_charts=False,
            save_stats=True,
            enable_collect_data=False,
            output_path_has_strategy_class_name=False,
            output_separate_by_backtest_status=True,
            output_setting_json=True,
            file_name_include_symbol=file_name_include_symbol,
            pre_call_before_backtest=pre_call_before_backtest,
            ignore_existed_backtest=ignore_existed_backtest,
        )
        bulk_backtest_kwargs.update(kwargs)
        if pool_size <= 1:
            try:
                logger.info(f"{num}/{tot_count}) {strategy_class_name} on {vt_symbol} {len(param_list)} 个策略将被回测")
                bulk_backtest_with_backtest_params_iter(**bulk_backtest_kwargs)
            except:
                logging.exception("%s 追踪回测异常", strategy_cls.__name__)

        else:
            # 多进程情况下，策略类无法传递，只能通过动态获取
            bulk_backtest_kwargs.update(dict(
                strategy_cls=None,
                strategy_module_name=module_name,
                strategy_class_name=strategy_class_name
            ))
            logger.info(f"{num}/{tot_count}) {strategy_class_name} on {vt_symbol} {len(param_list)} 个策略将被多进程回测")
            pool.submit(
                bulk_backtest_with_backtest_params_iter,
                **bulk_backtest_kwargs,
            )

    if pool is not None:
        pool.shutdown(wait=True)
        logger.info(f"全部 {tot_count} 进程任务结束")


def _test_backtest_from_tb_xml():
    dir_path = r'd:\temp\RsiOnly'
    backtest_from_tb_xml(dir_path, pool_size=-1)


if __name__ == "__main__":
    pass
