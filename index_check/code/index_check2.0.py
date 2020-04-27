# -*- coding: utf-8 -*-
# @Time : 2020/2/3 15:49
# @Author : ling
# @Email : ysling129@126.com
# @File : index_check2.0
# @Project : tellhow
# @description :
from datetime import datetime
from psycopg2 import extras
import psycopg2 as pg
import pandas as pd
import json
import os
import logging
from logging import config
from dateutil.relativedelta import relativedelta
logging.config.fileConfig(
    os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)),
        'config/mylog.conf'))

log = logging.getLogger("check_index")

DB_INFO = json.load(
    open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config/db_info.json'),
        encoding='utf-8'))

# conn = pg.connect(**DB_INFO["PG_CONN"]['default'])

dt_rule = {
    "0": relativedelta(days=+1),
    "1": relativedelta(weeks=+1),
    "2": relativedelta(days=+10),
    "3": relativedelta(months=+1),
    "4": relativedelta(months=+3),
    "5": relativedelta(years=+1),
}


def longestConsecutive(
        dt_list: list,
        step=relativedelta(days=+1)):
    """"
    获取最大的连续日期个数
    """
    longest_streak = 0
    num_set = set(dt_list)
    for num in num_set:
        if num - step not in num_set:
            current_num = num
            current_streak = 1

            while current_num + step in num_set:
                current_num += step
                current_streak += 1

            longest_streak = max(longest_streak, current_streak)

    return longest_streak


def data_process():
    """
    季度指标
    :return:
    """
    results = []
    fact_data = pd.read_sql(
        """select * from biz_current.a_bi_indx_fact """,
        con=conn)
    # print(data)
    data_groups = fact_data.groupby(
        ['indx_id', 'regn_cd', 'dt_attr_idtfy', 'data_src_cd'])

    for col_group, data_group in data_groups:
        latest_dt = data_group['dt'].max()
        oldest_dt = data_group['dt'].min()
        latest_indx_val = data_group[data_group['dt']
                                     == latest_dt].indx_val.values[0]
        data_group_num = data_group.shape[0]

        step = col_group[2]
        dt_list = data_group["dt"]
        latest_cont_prd_cnt = longestConsecutive(dt_list, dt_rule[step])
        compl_ind = str(1 if data_group_num == latest_dt else 0)
        ontm_ind = '0'
        if step == "0" and relativedelta(
                datetime.today(), latest_dt).days <= 1:
            ontm_ind = '1'
        elif step == "1" and relativedelta(datetime.today(), latest_dt).weeks <= 1:
            ontm_ind = '1'
        elif step == "2" and relativedelta(datetime.today(), latest_dt).days < 11:
            ontm_ind = '1'
        elif step == "3" and relativedelta(datetime.today(), latest_dt).months <= 1:
            ontm_ind = '1'
        elif step == "4" and relativedelta(datetime.today(), latest_dt).months <= 3:
            ontm_ind = '1'
        elif step == "5" and relativedelta(datetime.today(), latest_dt).years <= 1:
            ontm_ind = '1'

        result = (
            col_group[0],
            step,
            col_group[1],
            latest_dt,
            oldest_dt,
            latest_indx_val,
            latest_cont_prd_cnt,
            compl_ind,
            ontm_ind,
            col_group[3],
            datetime.today()
        )
        log.info(f"{col_group[0]} 已经检查完成。")
        results.append(result)
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        conn = pg.connect(**DB_INFO["PG_CONN"]['default'])
    else:
        conn = pg.connect(**DB_INFO["PG_CONN"][sys.argv[1]])

    data = data_process()
    data_sql = """
    insert into biz_current.a_bi_indx_calc_rest_qlty_analy values %s;
    """
    pg_cur = conn.cursor()
    log.info(f"清除之前检查结果")
    pg_cur.execute(
        f"""TRUNCATE table biz_current.a_bi_indx_calc_rest_qlty_analy""")
    extras.execute_values(pg_cur, data_sql, data, page_size=20000)
    conn.commit()
    conn.close()
    log.info(f"检查结果，已经写入数据库中")
