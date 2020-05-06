## 介绍

&emsp;&emsp;该程序的主要目的是根据业务需求，将不符合需求的信息查询并记录下来。用于描述该表的部分情况，也可成为质量检查。该程序涉及到三张表，其**E-R**图如下：<br/>

![质量检查ER图](img/%E8%B4%A8%E9%87%8F%E6%A3%80%E6%9F%A5.png)<br/>

&emsp;&emsp;程序的主要功能是执行配置表中的有效检核SQL，并将结果导入到检核结果表中。<br/>

## 程序环境：

Python3.7

- panda模块

- psycopg2模块

Postgresql10.0 中上述三张表

- 数据质量检核结果表(dqc_data_qlty_tsk_rest)<br/>
- 数据质量检核任务配置表(dqc_data_qlty_tsk_cfg)<br/>
- 数据质量检核规则表(dqc_data_qlty_rule)<br/>

## 文件夹

- 《config》为一些初始化所需资料：指标表(a_bi_indx_fact)的模型sql，检查结果表(a_bi_indx_calc_rest_qlty_analy)的模型sql，日志配置文件，数据库配置文件等等
- 《code》存放代码文件夹，里面含有单独的组件脚本
  - get_init.py
  - exc_sql.py
  - rule_exec.py
- 《img》存放的文中所需的图片。

## 基本设计逻辑

---

1、从dqc_data_qlty_tsk_cfg表中获取检核SQL<br/>
2、将结果集到dataframe中，利用其有关的函数及性质，获取自己想要个的属性<br/>
3、将加工处理的结果导入到表dqc_data_qlty_tsk_rest中

**注**：详细流程及算法见**《数据检查模块介绍.md》**



## 使用方法







## 运行实例









## 其他说明

### 配置文件介绍

**db_info.json**文件

```json
{

    "PG_CONN": {
        "default": {
            "port": 5432,
            "user": "postgres",
            "host": "10.10.10.31",
            "password": "tellhow123",
            "dbname": "bj_tz_ldjsc1.1"
        },
        "default_comment": "通州项目的数据连接信息",
        "PG_DB": {
            "port": 5432,
            "user": "postgres",
            "host": "xxx.xxx.xxx.xxx",
            "password": "******",
            "dbname": "postgres"
        },
        "PG_DB_comment": "XXXX数据"
    },

    "MySql_CONN": {
        "default": {
            "port": 3306,
            "user": "root",
            "host": "10.10.10.31",
            "password": "tellhow123",
            "database": "bj_tz_ldjsc1.1"
        },
        "default_comment": "通州项目的数据连接信息"
    }
}
```


上述的配置仅仅是表示一个数据库的连接信息。<br/>

**mylog.conf**文件

```ini
[loggers]
keys=root, check_index

[handlers]
keys=fileHandler, consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_check_index]
level=INFO
handlers=fileHandler, consoleHandler
qualname=check_index
propagate=0


[handler_consoleHandler]
class=StreamHandler
args=(sys.stdout,)
level=DEBUG
formatter=simpleFormatter

[handler_fileHandler]
class=handlers.TimedRotatingFileHandler
args=(os.path.abspath(os.getcwd()+'/log/my.out'), 'M', 1, 0, "UTF-8", True)
handlers.TimedRotatingFileHandler.suffix="%Y-%m-%d_%H-%M.log"
level=INFO
formatter=simpleFormatter


[formatter_simpleFormatter]
format=%(asctime)s | %(filename)s | [%(levelname)s] | %(message)-20s
datefmt=%Y-%m-%d %H:%M:%S

```

<br/>

&emsp;&emsp;上述的配置日志信息显示，loggers为check_index的日志为滚动日志，根据参数`args=os.path.abspath(os.getcwd()+'/log/my.out'), 'M', 1, 0, "UTF-8", True)`可以确定，其日志文件在运行命令出下的log文件下，`M`参数表示滚动日志是按照每分钟切割形成日志文件的。

