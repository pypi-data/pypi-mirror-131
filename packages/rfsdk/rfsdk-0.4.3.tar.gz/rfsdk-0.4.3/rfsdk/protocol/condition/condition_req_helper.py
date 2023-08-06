# -*- coding: utf-8 -*-

import inspect

from rfsdk.comm_utils import generate_req

from ant import encrypt_special


class InitFlag(object):
    InitFlag_Init = 0
    InitFlag_Pause = 1


class SettleFlag(object):
    SettleFlag_Undefined = 0
    SettleFlag_Init = 1
    SettleFlag_Settle = 2


# 条件单缓存信息存储
def make_condition_info(investor_key,
                        order_no,
                        instrument_id,
                        exchange_id,
                        direction,
                        comb_offset_flag,
                        order_price_type,
                        limit_price,
                        volume_total_original,
                        init_flag,
                        valid_period_count,
                        condition,
                        condition_type,
                        condition_info,
                        condition_status,
                        status_msg,
                        message,
                        insert_time,
                        activate_time,
                        modify_time,
                        end_time,
                        pause_time,
                        trigger_time,
                        trigger_hq_time,
                        trigger_tips,
                        trigger_entrust_price,
                        trigger_entrust_amount,
                        investor_id,
                        broker_id,
                        interface_type,
                        expire_date,
                        source,
                        pre_order_no,
                        trigger_price,
                        ):
    return generate_req(inspect.currentframe())


# 条件订单信息推送
def make_report(investor_key,
                order_no,
                instrument_id,
                exchange_id,
                direction,
                comb_offset_flag,
                order_price_type,
                limit_price,
                volume_total_original,
                init_flag,
                valid_period_count,
                condition,
                condition_type,
                condition_status,
                status_msg,
                message,
                insert_time,
                activate_time,
                modify_time,
                end_time,
                pause_time,
                trigger_time,
                trigger_hq_time,
                trigger_tips,
                trigger_entrust_price,
                trigger_entrust_amount,
                investor_id,
                broker_id,
                interface_type,
                expire_date,
                source,
                pre_order_no,
                trigger_price,
                ):
    return generate_req(inspect.currentframe())


# 创建条件单请求
def make_insert_req(investor_key,
                    instrument_id,
                    exchange_id,
                    direction,
                    comb_offset_flag,
                    order_price_type,
                    limit_price,
                    volume_total_original,
                    init_flag,
                    valid_period_count,
                    condition,
                    condition_type,
                    condition_info,
                    investor_id,
                    broker_id,
                    interface_type,
                    source,
                    pre_order_no,
                    ):
    return generate_req(inspect.currentframe())


# 条件单创建应答
def make_insert_rsp(result):
    return generate_req(inspect.currentframe())


# 条件单修改请求
def make_modify_req(investor_key,
                    order_no,
                    init_flag,
                    order_price_type,
                    limit_price,
                    volume_total_original,
                    valid_period_count,
                    condition,
                    condition_type,
                    condition_info,
                    investor_id,
                    direction,
                    comb_offset_flag,
                    source,
                    pre_order_no,
                    modify_preorder_no):
    return generate_req(inspect.currentframe())


# 条件单修改应答
def make_modify_rsp(result):
    return generate_req(inspect.currentframe())


# 条件单暂停请求
def make_pause_req(investor_key,
                   order_no,
                   investor_id,
                   source):
    return generate_req(inspect.currentframe())

    # 条件单暂停应答


def make_pause_rsp(result):
    return generate_req(inspect.currentframe())


# 条件单启动请求
def make_activate_req(investor_key,
                      order_no,
                      investor_id,
                      source):
    return generate_req(inspect.currentframe())


# 条件单启动应答
def make_activate_rsp(result):
    return generate_req(inspect.currentframe())


# 条件单删除请求
def make_delete_req(investor_key,
                    order_no,
                    investor_id,
                    source):
    return generate_req(inspect.currentframe())


# 条件单删除应答
def make_delete_rsp(result):
    return generate_req(inspect.currentframe())


# 条件单取消请求
def make_cancel_req(investor_key,
                    order_no,
                    investor_id,
                    source):
    return generate_req(inspect.currentframe())


# 条件单取消应答
def make_cancel_rsp(result):
    return generate_req(inspect.currentframe())


# 条件单查询/批量查询
def make_query_req(investor_key,
                   order_no,
                   start_date,
                   end_date,
                   condition_type,
                   condition_status,
                   investor_id,
                   broker_id,
                   interface_type,
                   begin_time,
                   end_time
                   ):
    return generate_req(inspect.currentframe())


# 条件单查询应答
def make_query_rsp(result):
    return generate_req(inspect.currentframe())


# 批量条件单查询应答
def make_multi_query_rsp(result):
    return generate_req(inspect.currentframe())


# 委托回报后推送委托与条件单的对应关系
def make_condition_push(investor_key,
                        condition_no,
                        instrument_id,
                        exchange_id,
                        trading_day,
                        order_sys_id,
                        direction):
    return generate_req(inspect.currentframe())


# 日初日终 请求
def make_condition_settle(type):
    return generate_req(inspect.currentframe())


# 日初日终 请求
def make_condition_settle_rsp(type):
    return generate_req(inspect.currentframe())


# 条件单实时触发价推送
def make_trigger_info(investor_key,
                      order_no,
                      trigger_price):
    return generate_req(inspect.currentframe())


# 查询合约信息
def make_instrument_info(instrument_id,
                         expire_date):
    return generate_req(inspect.currentframe())


# 查询合约返回
def make_instrument_info_list(result):
    return generate_req(inspect.currentframe())
