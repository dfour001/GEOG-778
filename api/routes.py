from api import app, db
from flask import jsonify, render_template
import json
from api.components import StationCard, FilterList
from collections import Counter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<id>')
def get_station_map_data(id):
    """ Given a station id, this will return geojson for the transmitter location,
        the estimated range, and the service contour. """
    
    # try:
    sql = f"""select 
                applicationid,
                callsign,
                frequency,
                city,
                state,
                lat,
                lng,
                ST_AsGeoJSON(ST_POINT(lng, lat)) as transmitter_geom,
                ST_AsGeoJSON(ST_Transform(St_buffer, 4326)) as estimated_range_geom,
                ST_AsGeoJSON(ST_Transform(service_contour, 4326)) as service_contour_geom
            from mv_fm_stations
            where id = '{id}'
            limit 1;"""

    result = db.session.execute(sql)
    data = [dict(r) for r in result][0]
    
    # Build geojson features using returned geojson geometries
    data['transmitter'] = {
        "type": "Feature",
        "geometry": json.loads(data['transmitter_geom'])
    }

    data['service_contour'] = {
        "type": "Feature",
        "geometry": json.loads(data['service_contour_geom'])
    }

    data['estimated_range'] = {
        "type": "Feature",
        "geometry": json.loads(data['estimated_range_geom'])
    }
    
    output = {'data': data}

    return output

    # except Exception as e:
    #     print(e)
    #     return {"Error": "Unable to return results"}

@app.route('/<lat>/<lng>')
def get_statons(lat, lng):
    """ Given a latitude and longitude, this will return the html for the stations
        list as well as the html for the filter modal. """
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


    except Exception as e:
        print(e)
        return {"Error": "Unable to return results"}