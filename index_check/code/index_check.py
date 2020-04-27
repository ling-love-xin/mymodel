# -*- coding: utf-8 -*-
# @Time : 2020/1/8 13:52
# @Author : ling
# @Email : ysling129@126.com
# @File : index_exec
# @Project : tellhow
# @description : 检查指标的连续性和及时性（sql完成的），指标的最新连续周期数

from datetime import datetime
from psycopg2 import extras
import psycopg2 as pg
import pandas as pd
import json
import os
from dateutil.relativedelta import relativedelta

DB_INFO = json.load(
    open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config/db_info.json'),
        encoding='utf-8'))

sql = """select
distinct
	indx_id,
	dt_attr_idtfy,
--	dt,
    1 latest_cont_prd_cnt,
	regn_cd,
--	indx_val,
	data_src_cd,
	dt_min,
	dt_max,
--	indx_count,
	first_val,
	case
		when dt_attr_idtfy = '0' then (dt_max-dt_min = indx_count-1)::int
		when dt_attr_idtfy = '1' then null
		when dt_attr_idtfy = '2' then null
		when dt_attr_idtfy = '3' then (date_part('year', age(now()+ '-1 month', dt_min))* 12 + date_part('month', age(now()+ '-1 month', dt_min)) = indx_count-1)::int
		when dt_attr_idtfy = '4' then ((date_part('year', age(now()+ '-1 month', dt_min))* 12 + date_part('month', age(now()+ '-1 month', dt_min)))/ 3 = indx_count-1)::int
		when dt_attr_idtfy = '5' then (date_part('year', age(now()+ '-1 month', dt_min))= indx_count-1)::int
		else null
end is_continuous,
	case
		when dt_attr_idtfy = '0' then (now()::date-dt_max::date = 1 )::int
		when dt_attr_idtfy = '1' then null
		when dt_attr_idtfy = '2' then null
		when dt_attr_idtfy = '3' then (date_trunc('month', now()+ '-1 month')= dt_max::date)::int
		when dt_attr_idtfy = '4' then (date_trunc('quarter', now()+ '-3 month')= dt_max::date)::int
		when dt_attr_idtfy = '5' then (date_trunc('year', now()+ '-1 year')= dt_max::date)::int
		else null
end timeliness
from
	(
	select
		indx_id,
		dt_attr_idtfy,
		dt,
		regn_cd,
		indx_val,
		data_src_cd,
		min(dt)over(partition by indx_id,
		regn_cd,
		dt_attr_idtfy) dt_min,
		max(dt)over(partition by indx_id,
		regn_cd,
		dt_attr_idtfy) dt_max,
		count(*) over(partition by indx_id,
		regn_cd,
		dt_attr_idtfy) indx_count,
		first_value(indx_val)over(partition by indx_id,
		regn_cd,
		dt_attr_idtfy
	order by
		dt desc ) first_val
	from
		biz_current.a_bi_indx_fact ) tab;
"""

conn = pg.connect(**DB_INFO["PG_CONN"]['default'])
result_data = pd.read_sql(
    sql,
    con=conn)


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


def get_latest_cont_prd_cnt(row: pd.Series):
    """
    获取最新连续周期数
    :param row:
    :return:
    """
    refer_Sql = f"""
    select dt from biz_current.a_bi_indx_fact
    where indx_id = '{row.indx_id}'
    and dt_attr_idtfy = '{row.dt_attr_idtfy}'
    and regn_cd='{row.regn_cd}'
    """
    refer_data = pd.read_sql(refer_Sql, con=conn)

    return longestConsecutive(refer_data.dt, dt_rule[row.dt_attr_idtfy])


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        conn = pg.connect(**DB_INFO["PG_CONN"]['default'])
    else:
        conn = pg.connect(**DB_INFO["PG_CONN"][sys.argv[1]])

    result_data = pd.read_sql(
            sql,
            con=conn)

    values = []
    today = datetime.now().strftime('%Y-%m-%d')
    for index, row in result_data.iterrows():
        latest_cont_prd_cnt = get_latest_cont_prd_cnt(row)
        value = (
            row.indx_id,
            row.dt_attr_idtfy,
            row.regn_cd,
            row.dt_max,
            row.dt_min,
            row.first_val,
            latest_cont_prd_cnt,
            row.is_continuous,
            row.timeliness,
            row.data_src_cd,
            datetime.now(),
        )
        values.append(value)
    data_sql = """
    insert into biz_current.a_bi_indx_calc_rest_qlty_analy values %s;
    """
    pg_cur = conn.cursor()
    pg_cur.execute(
        f"""TRUNCATE table biz_current.a_bi_indx_calc_rest_qlty_analy""")
    extras.execute_values(pg_cur, data_sql, values, page_size=len(values))
    conn.commit()
    conn.close()
