-- 此为postgresql10的sql,在语法上可能与其他版本有些许的差别，若是报错，请仔细检查sql语句



--基础信息指标结果



CREATE TABLE biz_current.a_bi_indx_fact (
	indx_id varchar(30) NOT NULL, -- 指标编号
	dt_attr_idtfy bpchar(1) NOT NULL, -- 日期属性标识：0-日,1-周,2-旬,3-月,4-季,5-年
	dt date NOT NULL, -- 日期
	regn_cd varchar(12) NOT NULL, -- 区域代码
	indx_val numeric(36,18) NULL, -- 指标值
	data_src_cd bpchar(7) NULL, -- 数据来源代码
	etl_tmstp timestamp NULL, -- 加载时间戳
	CONSTRAINT a_bi_indx_fact_pkey PRIMARY KEY (indx_id, dt_attr_idtfy, dt, regn_cd)
);

-- table comment

COMMENT ON TABLE biz_current.a_bi_indx_fact is '基础信息指标结果';

-- Column comments

COMMENT ON COLUMN biz_current.a_bi_indx_fact.indx_id IS '指标编号';
COMMENT ON COLUMN biz_current.a_bi_indx_fact.dt_attr_idtfy IS '日期属性标识：0-日,1-周,2-旬,3-月,4-季,5-年';
COMMENT ON COLUMN biz_current.a_bi_indx_fact.dt IS '日期';
COMMENT ON COLUMN biz_current.a_bi_indx_fact.regn_cd IS '区域代码';
COMMENT ON COLUMN biz_current.a_bi_indx_fact.indx_val IS '指标值';
COMMENT ON COLUMN biz_current.a_bi_indx_fact.data_src_cd IS '数据来源代码';
COMMENT ON COLUMN biz_current.a_bi_indx_fact.etl_tmstp IS '加载时间戳';
