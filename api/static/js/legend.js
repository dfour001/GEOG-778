// Legend
var LegendControl = L.Control.extend({
    options: {
        position: 'bottomright'
    },

    onAdd: function (map) {
        let container = L.DomUtil.create('div', 'legend-control-container');
        $(container).append('<div id="collapse" class="collapseAction"><b>Legend</b></div><img id="btnCollapse" src=' + legendOpenPNG + ' data-status="open" class="collapseAction">');
        
        let legendBody = '<div id="legend-body" class="legend-hide"><hr>';


        
        legendBody += '<p><div class="legend__item legend__transmitter"><img src='+radioMarkerPNG+' class="legend__img"></div> Transmitter (<a data-toggle="tooltip" data-placement="left" title="Location of the radio transmitter tower" href="#">?</a>)</p>';
        legendBody += '<p><div class="legend__item legend__serviceContour"></div> Service Contour (<a data-toggle="tooltip" data-placement="left" title="Area guaranteed by the FCC to provide service without interference" href="#">?</a>)</p>';
        legendBody += '<p><div class="legend__item legend__estimatedRange"></div> Estimated Range (<a data-toggle="tooltip" data-placement="left" title="Theoretical range of this station on a normal radio" href="#">?</a>)</p>';
        legendBody +='<p><div class="legend__item legend__userLocation"><img src='+markerIconPNG+' class="legend__img"></div> User Location (<a data-toggle="tooltip" data-placement="left" title="Location used for this search" href="#">?</a>)</p>';
        legendBody += '</div>';
        $(container).append(legendBody);
        
        return container
    }
});