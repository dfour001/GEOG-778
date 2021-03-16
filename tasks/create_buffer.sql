drop materialized view if exists mv_fm_stations;

create materialized view mv_fm_stations as (
select
	s.applicationid,
	s.callsign,
	s.frequency,
	f.format,
	s.city,
	s.state,
	s.dist_40dbu,
	s.id,
	(s.lngd+(s.lngm/60)+(s.lngs/3600))*-1 as lng, 
	s.latd+(s.latm/60)+(s.lats/3600) as lat,
	ST_BUFFER(ST_Transform(ST_SetSRID(ST_POINT((s.lngd+(s.lngm/60)+(s.lngs/3600))*-1, (s.latd+(s.latm/60)+(s.lats/3600))), 4326),5069 ) , s.dist_40dBu*1000*0.75)
from 
	stations s,
	formats f
where lngd < 360 and s.callsign = f.callsign);