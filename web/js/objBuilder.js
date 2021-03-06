function build_station_card(data) {
    let card = $('<div class="stationCard"></div>');
        let cardMain = $('<div class="stationCard__main"></div>');
            let freq = $('<p class="stationCard__freq">' + data.frequency + ' - ' + data.callsign + '</p>');
            let format = $('<p class="stationCard__format">' + data.format + '</p>');
            let info = $('<p class="stationCard__info" data-ID="' + data.id + '">&#x25B2</p>');
        cardMain.append(freq);
        cardMain.append(format);
        cardMain.append(info);
    card.append(cardMain);
    let details = $('<div class="stationCard__details d-none" data-ID-Details="' + data.id + '"><p>Additional</p><p>Data</p><p>About</p><p>This Station</p><p>Here</p><img src=img/map.jpg style="margin-left: 50%; transform: translateX(-50%);"></div>');
    card.append(details);
    
    return card
}