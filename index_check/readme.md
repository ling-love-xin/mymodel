## 介绍

&emsp; 该程序主要的功能是对指标的及时性、连续性，及最大连续周期做检查(不做重点考虑)。

- 及时性：按照业务规则，基于时间戳，有无产生指标值，断定其指标的及时与否。  
例如:某指标的业务周期最小粒度为**日**的，今天必须有昨天的数据
- 连续性：按照业务规则，指标的业务日期连续与否。  
例如：某指标的日期属性为**年**，只有2012年、2013年的指标值，则判断该指标连续
- 最大连续周期数：按照业务规则，某指标在其日期属性上最大的连续日期的个数。  
例如：某指标的日期属性为**年**，其在2012、2013、2015、2016、2017、2020
有值，其最大的连续周期数为3。

### 文件夹

- 《config》为一些初始化所需资料：指标表(a_bi_indx_fact)的模型sql，检查结果表(a_bi_indx_calc_rest_qlty_analy)的模型sql，日志配置文件，数据库配置文件等等<br>
- 《code》存放代码文件夹<br/>

### 基本设计逻辑

---
1、从a_bi_indx_fact 表中读取指标的所有值 <br/>
2、根据业务规则，将指标的业务日期与一组时间序列做对比，判断其连续性<br/>
3、根据业务规则，将指标的业务日期与当前日期最对比，判断其及时性



**注**：详细流程及算法见**《指标检查程序模块介绍2.md》**



---

## 运行实例

### 无参数

    python index_check.py
    
    ## 或者 
    
    python index_check2.0.py

### 有参数

改参数为db_info.json文件中的参数，其主要作用是指定数据库服务器<br/>

```bash
python index_check.py default

## 或者 

python index_check2.0.py default
```

<br/>

## 其他说明

&emsp;&emsp;该程序必须要有biz*current.a*bi*indx*fact、biz*current.a*bi*indx*calc*rest*qlty_analy这两张表，因此在使用时需要先运行《config》目录下的两个SQL文件，才可以正常运行。<br/>

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




