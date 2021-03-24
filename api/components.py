class StationCard():
    def __init__(self, data, userLat, userLng):
        self.id = data['id']
        self.applicationid = data['applicationid']
        self.frequency = data['frequency']
        self.callsign = data['callsign']
        self.city = data['city']
        self.state = data['state']
        self.dist_40dbu = data['dist_40dbu']
        self.format = data['format']
        self.licensee = data['licensee']
        self.within_service_contour = data['within_service_contour']
        self.lat = data['lat']
        self.lng = data['lng']
        self.userLat = userLat
        self.userLng = userLng
        self.distance = 123
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
                <div class='row'>
                    <div class="col-6">
                        <div class='stationCard__detailsList detailsList-{self.id}'>
                            <p class="detailsHeading">City:</p><p class="detailsInfo">{self.city.title()}</p>
                            <p class="detailsHeading">State:</p><p class="detailsInfo">{self.state}</p>
                            <p class="detailsHeading">Distance:</p><p class="detailsInfo">{self.distance}</p>
                            <p class="detailsHeading">Licensee:</p><p class="detailsInfo">{self.licensee.title()}</p>
                            <div class="stationCard_btnMapHolder">
                                <button type="button" class="btn btn-light stationCard__btnMap" data-toggle="modal" data-target="#modal" data-ID="{self.id}">View Map of Station</button>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 stationCard__logoHolder">
                        <img class="logo-{self.id} stationCard__logo stationCard__logo--blurred" src=''>
                        <img class="logo-{self.id} stationCard__logo" src=''>
                    </div>
                </div>
                
                
            </div>
        </div>
        """
        return template