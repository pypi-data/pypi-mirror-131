#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/12/14 10:25
@File    : import_tb_param_xml.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import json
import logging
import os
from collections import defaultdict
from json import JSONDecodeError
from typing import Tuple, List, Dict
from xml.etree.ElementTree import ElementTree

from vnpy.trader.constant import Exchange

from vnpy_extra.constants import INSTRUMENT_EXCHANGE_DIC
from vnpy_extra.utils.symbol import get_instrument_type

logger = logging.getLogger(__name__)


def get_name_vt_symbol_param_dic_by_xml(file_path) -> Tuple[str, str, dict]:
    tree = ElementTree(file=file_path)  # <xml.etree.ElementTree.ElementTree at 0x1c13635f28>
    return get_strategy_name_by_et(tree), get_vt_symbol_by_et(tree), get_param_dic_by_et(tree)


def get_strategy_name_by_et(tree: ElementTree) -> str:
    root = tree.getroot()  # <Element 'App' at 0x0000001C13657958>
    el = root.find('TradeUnit/Formular/F/TacticSetting/Master/NativeStrategyKey/strName')
    return el.text


def transfer_param_value(val: str):
    try:
        return json.loads(val)
    except JSONDecodeError:
        return val


def get_param_dic_by_et(tree: ElementTree) -> dict:
    root = tree.getroot()  # <Element 'App' at 0x0000001C13657958>
    param_dic = {param.get("Name"): transfer_param_value(param.get("Value")) for param in
                 root.iterfind('TradeUnit/Formular/F/TacticSetting/Parameters/Parameter')}
    return param_dic


def tb_symbol_2_symbol_exchange(tb_symbol) -> Tuple[str, Exchange]:
    instrument_type = get_instrument_type(tb_symbol)
    exchange = INSTRUMENT_EXCHANGE_DIC[instrument_type]
    return instrument_type, exchange


def get_symbol_exchange_by_et(tree: ElementTree) -> Tuple[str, Exchange]:
    root = tree.getroot()  # <Element 'App' at 0x0000001C13657958>
    el = root.find('TradeUnit/Goods/G/GoodsSetting/DataRangeSetting/DataRange/GoodsKey')
    symbol = el.get("Goods")
    return tb_symbol_2_symbol_exchange(symbol)


def tb_symbol_2_vt_symbol_exchange(tb_symbol) -> str:
    instrument_type, exchange = tb_symbol_2_symbol_exchange(tb_symbol)
    return f"{instrument_type}9999.{exchange.value}"


def get_vt_symbol_by_et(tree: ElementTree) -> str:
    root = tree.getroot()  # <Element 'App' at 0x0000001C13657958>
    el = root.find('TradeUnit/Goods/G/GoodsSetting/DataRangeSetting/DataRange/GoodsKey')
    symbol = el.get("Goods")
    return tb_symbol_2_vt_symbol_exchange(symbol)


def _test_get_param_dic_by_xml():
    file_path = r'd:\temp\RsiOnly\RsiOnly(0,20,30,0,1)_研究单元-1.xml'
    name, vt_symbol, param_dic = get_name_vt_symbol_param_dic_by_xml(file_path)
    print(name, vt_symbol, param_dic)


def get_name_vt_symbol_param_list_dic_by_dir(dir_path) -> Tuple[Dict[str, Dict[str, List[dict]]], int]:
    name_param_list_dic = defaultdict(lambda: defaultdict(list))
    tot_count = 0
    for _ in os.listdir(dir_path):
        file_path = os.path.join(dir_path, _)
        if not os.path.isfile(file_path):
            continue
        name, vt_symbol, param_dic = get_name_vt_symbol_param_dic_by_xml(file_path)
        name_param_list_dic[f"{name}Strategy"][vt_symbol].append(param_dic)
        tot_count += 1

    return name_param_list_dic, tot_count


def _test_get_name_vt_symbol_param_list_dic_by_dir():
    dir_path = r'd:\temp\RsiOnly'
    name_vt_symbol_param_list, tot_count = get_name_vt_symbol_param_list_dic_by_dir(dir_path)
    print(name_vt_symbol_param_list)


if __name__ == "__main__":
    # _test_get_param_dic_by_xml()
    _test_get_name_vt_symbol_param_list_dic_by_dir()
