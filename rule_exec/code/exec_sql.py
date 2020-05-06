# -*- coding: utf-8 -*-
# @Time : 2019/12/20 14:58
# @Author : ling
# @Email : ysling129@126.com
# @File : check_time
# @Project : tellhow
# @description :

import argparse
import os
import json
import psycopg2 as pg
import pandas as pd

DB_INFO = json.load(
    open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config/db_info.json'),
        encoding='utf-8'))


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='执行sql的一下参数介绍')
        parser.add_argument(
            "-s",
            dest="sql",
            required=True,
            type=str,
            help='输入一个sql，并用双引号引住\t例：\npython exec_sql -s "select 1;"')
        parser.add_argument(
            "-l",
            dest="dblink",
            # required=True,
            type=str,
            default='default',
            help='输入配置文件db_info的key值，默认为default')
        parser.add_argument(
            '-o',
            dest='out_type',
            type=str,
            default='console',
            help="仅仅可以输入，console、csv常用的格式",
            choices=['console', 'csv', ])

        args = parser.parse_args()
        # print(args)
        db_info = DB_INFO[args.dblink]
        pg_conn = pg.connect(dbname=db_info['dbname'],
                             user=db_info['user'],
                             password=db_info['password'],
                             host=db_info['host'],
                             port=db_info['port'])

        data = pd.read_sql(args.sql, con=pg_conn)
        pg_conn.close()
        if args.out_type == 'console':
            print(data)
        elif args.out_type == 'csv':
            import datetime
            print(data)
            data.to_csv(
                os.path.join(
                    os.getcwd(),
                    datetime.datetime.today().strftime('%y%m%d%H%M%S') +
                    '.csv'),
                encoding='utf8',index=False)
            print(os.path.join(
                    os.getcwd(),
                    datetime.datetime.today().strftime('%y%m%d%H%M%S') +
                    '.csv'))
    except IndexError as e:
        print(e)
        print('未输入参数或者，输入形式不对，实例：\npython exec_sql -s "select 1;"')
        exit(1)

