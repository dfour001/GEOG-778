from math import acos, sin, cos, radians as rad

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
        self.distance = self.calculate_user_distance()
        self.geom = data['st_buffer']
        
    def calculate_user_distance(self):
        # Organize values and convert to radians
        sinLat1 = sin(rad(float(self.userLat)))
        sinLat2 = sin(rad(float(self.lat)))
        cosLat1 = cos(rad(float(self.userLat)))
        cosLat2 = cos(rad(float(self.lat)))

        lng1 = rad(float(self.userLng))
        lng2 = rad(float(self.lng))

        # Calculate d
        d = acos(sinLat1 * sinLat2 + cosLat1 * cosLat2 * cos(lng1 - lng2))

        # Find distance in miles
        mi = d * 3959

        return round(mi, 2)

    def build_html(self):
        formatClass = self.format.replace(" ", "_").replace("(", "").replace(")","") # To set the card's format for filtering
        template = f"""
        <div class='stationCard {formatClass}'>
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
                            <p class="detailsHeading">Distance:</p><p class="detailsInfo">{self.distance} mi</p>
                            <p class="detailsHeading">Licensee:</p><p class="detailsInfo">{self.licensee.title()}</p>
                            <div class="stationCard_btnMapHolder">
                                <button type="button" class="btn btn-light stationCard__btnMap" data-target="#mapModal" data-ID="{self.id}">View Map of Station</button>
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

class FilterList():
    def __init__(self, formatCounter):
        self.formatCounter = formatCounter
        self.formatList = [key for key in self.formatCounter.keys()]
        self.formatList.sort()
    
    def build_html(self):
        itemTemplate = """
        <p class="filterList__item" data-format="{formatClass}">{formatDisplay} <span class="badge badge-pill filterList__pill">{count}</span></p>
        """

        itemListHTML = """<p class="filterList__item" data-format="show_all">Show All Formats</p>"""
        for key in self.formatList:
            itemHTML = itemTemplate.replace("{formatClass}", key.replace("(", "").replace(")",""))
            itemHTML = itemHTML.replace("{formatDisplay}", key.replace("_", " "))
            itemHTML = itemHTML.replace("{count}", str(self.formatCounter[key]))
            itemListHTML += itemHTML

        return itemListHTML

if __name__ == "__main__":
    from collections import Counter
    c = Counter()
    
    c['Rock'] = 4
    c['Polka'] = 1
    c['Classic_Rock'] = 1
    c['Ragtime'] = 5
    fl = FilterList(c)
    print(c)
    print(fl.build_html())
    
        