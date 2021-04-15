select 
	applicationid,
	callsign,
	frequency,
	city,
	state,
	lat,
	lng,
	ST_Transform(St_buffer, 4326) as estimated_range,
	ST_Transform(service_contour, 4326)
from mv_fm_stations
where id = '19527'
limit 1;