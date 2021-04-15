from api import app, db
from flask import jsonify, render_template
import json
from api.components import StationCard, FilterList
from collections import Counter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<lat>/<lng>')
def get_statons(lat, lng):
    # try:
        print(f'lat: {lat}   lng: {lng}')
        sql = f"""select s.*, sc.within_service_contour from (
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

        # Format counter for filter. Used as input for creating FilterList
        formatCounter = Counter()

        stationsHTML = ''
        for station in stations:
            card = StationCard(station, lat, lng)
            stationsHTML += card.build_html()
            formatCounter[station["format"].replace(' ', '_')] += 1

        filterList = FilterList(formatCounter)
        filterHTML = filterList.build_html()

        output = {
            "stationsHTML": stationsHTML,
            "filterHTML": filterHTML
        }
        return output


    # except Exception as e:
    #     print(e)
    #     return {"Error": "Unable to return results"}