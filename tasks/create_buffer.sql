drop table if exists testStation;

create table testStation as (
select
	frequency,
	callsign, 
	(lngd+(lngm/60)+(lngs/3600))*-1 as lng, 
	latd+(latm/60)+(lats/3600) as lat,
	ST_BUFFER(ST_Transform(ST_SetSRID(ST_POINT((lngd+(lngm/60)+(lngs/3600))*-1, (latd+(latm/60)+(lats/3600))), 4326),5069 ) , dist_40dBu*1000)
from stations);