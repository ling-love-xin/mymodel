-- 此为postgresql10的sql,在语法上可能与其他版本有些许的差别，若是报错，请仔细检查sql语句


-- 指标计算结果质量分析

CREATE TABLE biz_current.a_bi_indx_calc_rest_qlty_analy (
	indx_id varchar(30) NOT NULL, -- 指标编号
	dt_attr_idtfy bpchar(1) NOT NULL, -- 日期属性标识
	regn_cd varchar(12) NOT NULL, -- 区域代码
	latest_dt date NULL, -- 最新日期
	oldest_dt date NULL, -- 最旧日期
	latest_indx_val numeric(36,18) NULL, -- 最新指标值
	latest_cont_prd_cnt int4 NULL, -- 最新连续周期数
	compl_ind bpchar(1) NULL, -- 完整性标志
	ontm_ind bpchar(1) NULL, -- 及时性标志
	data_src_cd bpchar(7) NULL, -- 数据来源代码
	etl_tmstp timestamp NULL, -- 加载时间戳
	CONSTRAINT a_bi_indx_calc_rest_qlty_analy_pkey1 PRIMARY KEY (indx_id, dt_attr_idtfy, regn_cd)
);

-- table comment

COMMENT ON TABLE biz_current.a_bi_indx_calc_rest_qlty_analy is '指标计算结果质量分析';



-- Column comments

COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.indx_id IS '指标编号';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.dt_attr_idtfy IS '日期属性标识';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.regn_cd IS '区域代码';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.latest_dt IS '最新日期';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.oldest_dt IS '最旧日期';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.latest_indx_val IS '最新指标值';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.latest_cont_prd_cnt IS '最新连续周期数';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.compl_ind IS '完整性标志';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.ontm_ind IS '及时性标志';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.data_src_cd IS '数据来源代码';
COMMENT ON COLUMN biz_current.a_bi_indx_calc_rest_qlty_analy.etl_tmstp IS '加载时间戳';