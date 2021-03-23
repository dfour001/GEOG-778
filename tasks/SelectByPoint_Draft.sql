select s.*, sc.within_service_contour from (
	select distinct on (s.callsign)
		s.applicationid,
		s.callsign,
		s.frequency,
		f.format,
		s.city,
		s.state,
		s.licensee,
		s.dist_40dbu,
		s.id,
		s.lng, 
		s.lat,
		s.st_buffer
	from
		mv_fm_stations s
	left join formats f on s.callsign = f.callsign
	where 
		ST_Intersects(ST_Transform(ST_SetSRID(ST_Point(-77.53,37.56)::geometry,4326),5069), s.st_buffer)
	) s
	left join (
	select
		sc.applicationid,
		'true' as "within_service_contour"
	from servicecontours sc
	where ST_Intersects(ST_Transform(ST_SetSRID(ST_Point(-77.53,37.56)::geometry,4326),5069), sc.geom)
		
	) sc
	on s.applicationid = sc.applicationid
order by cast(split_part(s.frequency, ' ', 1) as double precision) asc;
