from api import app, db
from flask import jsonify, render_template
import json
from api.components import StationCard

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<lat>/<lng>')
def get_statons(lat, lng):
    try:
        print(f'lat: {lat}   lng: {lng}')
        sql = f"""select s.*, sc.within_service_contour from (
        select distinct on (s.callsign)
            s.applicationid,
            s.callsign,
            s.frequency,
            f.format,
            s.city,
            s.state,
            s.dist_40dbu,
            s.id,
            s.lng, 
            s.lat,
            s.st_buffer
        from
            mv_fm_stations s
        left join formats f on s.callsign = f.callsign
        where 
            ST_Intersects(ST_Transform(ST_SetSRID(ST_Point({lng},{lat})::geometry,4326),5069), s.st_buffer)
        ) s
        left join (
        select
            sc.applicationid,
            'true' as "within_service_contour"
        from servicecontours sc
        where ST_Intersects(ST_Transform(ST_SetSRID(ST_Point({lng},{lat})::geometry,4326),5069), sc.geom)
            
        ) sc
        on s.applicationid = sc.applicationid
    order by cast(split_part(s.frequency, ' ', 1) as double precision) asc;
    """
        result = db.session.execute(sql)
        stations = [dict(r) for r in result]

        outputHTML = ''
        for station in stations:
            card = StationCard(station)
            outputHTML += card.build_html()

        return outputHTML


    except Exception as e:
        print(e)
        return {"Error": "Unable to return results"}