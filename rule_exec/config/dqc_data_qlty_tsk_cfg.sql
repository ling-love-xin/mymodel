-- Drop table

-- DROP TABLE mgmt_etl.dqc_data_qlty_tsk_cfg;

CREATE TABLE mgmt_etl.dqc_data_qlty_tsk_cfg (
	chk_id serial NOT NULL, -- 检核ID
	rule_id serial NOT NULL, -- 规则ID
	rule_ctgy_cd varchar(20) NULL, -- 规则类别代码
	rule_ctgy_nm varchar(200) NULL, -- 规则类别名称
	rule_typ_cd varchar(20) NULL, -- 规则类型代码
	rule_typ_nm varchar(200) NULL, -- 规则类型名称
	chk_db_obj_en_nm varchar(100) NULL, -- 检核库对象英文名称
	chk_db_obj_cn_nm varchar(200) NULL, -- 检核库对象中文名称
	chk_obj_en_nm varchar(200) NULL, -- 检核对象英文名称
	chk_obj_cn_nm varchar(200) NULL, -- 检核对象中文名称
	chk_fld_en_nm text NULL, -- 检核字段英文名称
	chk_fld_cn_nm text NULL, -- 检核字段中文名称
	belg_usg_idtfy varchar(2) NULL, -- 所属用途标识
	chk_sql text NULL, -- 检核SQL
	discard_ind bpchar(1) NULL, -- 废弃标志
	infl_degr_comnt varchar(20) NULL, -- 影响程度说明
	db_id int8 NULL, -- 数据库ID
	chk_desc text NULL, -- 检核描述
	setup_tmstp timestamp NULL, -- 创建时间戳
	upd_tmstp timestamp NULL, -- 更新时间戳
	CONSTRAINT dqc_data_qlty_tsk_cfg_pkey PRIMARY KEY (chk_id),
	CONSTRAINT dqc_data_qlty_tsk_cfg_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES mgmt_etl.dqc_data_qlty_rule(rule_id)
);

-- comments

COMMENT ON TABLE mgmt_etl.dqc_data_qlty_tsk_cfg IS '数据质量检核任务配置表';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_id IS '检核ID';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.rule_id IS '规则ID';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.rule_ctgy_cd IS '规则类别代码';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.rule_ctgy_nm IS '规则类别名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.rule_typ_cd IS '规则类型代码';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.rule_typ_nm IS '规则类型名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_db_obj_en_nm IS '检核库对象英文名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_db_obj_cn_nm IS '检核库对象中文名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_obj_en_nm IS '检核对象英文名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_obj_cn_nm IS '检核对象中文名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_fld_en_nm IS '检核字段英文名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_fld_cn_nm IS '检核字段中文名称';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.belg_usg_idtfy IS '所属用途标识';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_sql IS '检核SQL';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.discard_ind IS '废弃标志';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.infl_degr_comnt IS '影响程度说明';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.db_id IS '数据库ID';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.chk_desc IS '检核描述';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.setup_tmstp IS '创建时间戳';
COMMENT ON COLUMN mgmt_etl.dqc_data_qlty_tsk_cfg.upd_tmstp IS '更新时间戳';
