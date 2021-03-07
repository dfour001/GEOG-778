function build_station_card(data) {
    let card = $('<div class="stationCard"></div>');
        let cardMain = $('<div class="stationCard__main" data-ID="' + data.id + '"></div>');
            let freq = $('<p class="stationCard__freq"><b>' + data.frequency + '</b> - ' + data.callsign + '</p>');
            let format = $('<p class="stationCard__format">' + data.format + '</p>');
            let info = $('<p class="stationCard__info">&#x25B2</p>');
        cardMain.append(freq);
        cardMain.append(format);
        cardMain.append(info);
    card.append(cardMain);
    let details = $('<div class="stationCard__details d-none" data-ID-Details="' + data.id + '"><p>[Additional]</p><p>[Data]</p><p>[About]</p><p>[This Station]</p><p>[Here]</p><button type="button" class="btn btn-light" data-toggle="modal" data-target="#modal" data-ID="' + data.id + '">View Map of Station</button></div>');
    card.append(details);
    return card
}

