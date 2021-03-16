class StationCard():
    def __init__(self, data):
        self.id = data['id']
        self.applicationid = data['applicationid']
        self.frequency = data['frequency']
        self.callsign = data['callsign']
        self.city = data['city']
        self.state = data['state']
        self.dist_40dbu = data['dist_40dbu']
        self.format = data['format']
        self.within_service_contour = data['within_service_contour']
        self.lat = data['lat']
        self.lng = data['lng']
        self.geom = data['st_buffer']
        
    def build_html(self):
        template = f"""
        <div class='stationCard'>
            <div class='stationCard__main' data-ID="{self.id}">
                <p class='stationCard__freq'><b>{self.frequency}</b> - {self.callsign}</p>
                <p class='stationCard__format'>{self.format}</p>
                <p class="stationCard__info">&#x25B2</p>
            </div>
            <div class="stationCard__details d-none" data-ID-Details="{self.id}">
                <p>[HA]</p>
                <p>[HA]</p>
                <p>[HA]</p>
                <p>[!]</p>
                <p>[!]</p>
                <button type="button" class="btn btn-light" data-toggle="modal" data-target="#modal" data-ID="{self.id}">View Map of Station</button>
            </div>
        </div>
        """
        return template