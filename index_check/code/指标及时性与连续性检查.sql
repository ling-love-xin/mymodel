-- 此为postgresql10的sql,在语法上可能与其他版本有些许的差别，若是报错，请仔细检查sql语句

select
distinct
	indx_id,
	dt_attr_idtfy,
--	dt,
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
		when dt_attr_idtfy = '3' then (date_part('year', age(dt_max, dt_min))* 12 + date_part('month', age(dt_max, dt_min)) = indx_count-1)::int
		when dt_attr_idtfy = '4' then ((date_part('year', age(dt_max, dt_min))* 12 + date_part('month', age(dt_max, dt_min)))/ 3 = indx_count-1)::int
		when dt_attr_idtfy = '5' then (date_part('year', age(dt_max, dt_min))= indx_count-1)::int
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
