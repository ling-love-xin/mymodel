# -*- encoding: utf-8 -*-
"""
@File    : get_init.py
@Time    : 2020/4/30 17:22
@Author  : ling
@Email   :
@Software: PyCharm
@Content :
"""

import os
import json
import psycopg2
import argparse

base_path = os.path.dirname(os.path.dirname(__file__))
DB_INFO = json.load(
    open(
        os.path.join(
            base_path,
            'config/db_info.json'),
        encoding='utf-8'))


def get_sql():
    files_path = []
    path = os.path.join(base_path, 'config')
    for root, dirs, dir_files in os.walk(path):
        for dir_file in dir_files:
            if dir_file.split('.')[-1] == 'sql':
                files_path.append(os.path.join(root, dir_file))
            else:
                pass
    return files_path


if __name__ == '__main__':
    # try:
    parser = argparse.ArgumentParser(description='执行sql的一下参数介绍')
    parser.add_argument(
        "-s",
        dest="schema",
        default='mgmt_etl',
        type=str,
        help='所在的schema')
    parser.add_argument(
        "-l",
        dest="dblink",
        type=str,
        default='default',
        help='输入配置文件db_info的key值，默认为default')

    args = parser.parse_args()

    # print(args)
    db_info = DB_INFO[args.dblink]
    db_info['schema'] = args.schema
    pg_conn = psycopg2.connect(dbname=db_info['dbname'],
                               user=db_info['user'],
                               password=db_info['password'],
                               host=db_info['host'],
                               port=db_info['port'])
    pg_cur = pg_conn.cursor()
    files = get_sql()
    for file in files:
        f = open(file, 'r', encoding='utf8')
        sql = f.read().replace("mgmt_etl", db_info['schema'])
        try:
            pg_cur.execute(sql)
        except Exception as e:
            print(e)

    pg_conn.commit()
    pg_conn.close()

    #     data = pd.read_sql(args.sql, con=pg_conn)
    #     pg_conn.close()
    #     if args.out_type == 'console':
    #         print(data)
    #     elif args.out_type == 'csv':
    #         import datetime
    #         print(data)
    #         data.to_csv(
    #             os.path.join(
    #                 os.getcwd(),
    #                 datetime.datetime.today().strftime('%y%m%d%H%M%S') +
    #                 '.csv'),
    #             encoding='utf8', index=False)
    #         print(os.path.join(
    #             os.getcwd(),
    #             datetime.datetime.today().strftime('%y%m%d%H%M%S') +
    #             '.csv'))
    # except IndexError as e:
    #     print(e)
    #     print('未输入参数或者，输入形式不对，实例：\npython exec_sql -s "select 1;"')
    #     exit(1)
