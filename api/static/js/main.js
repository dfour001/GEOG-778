var map;
var userLat;
var userLng;

function init() {
    // Clear splashscreen after 3000 miliseconds
    setTimeout(function () {
        $('.title').removeClass('title--splashscreen');
        $('.title__mainTitle').removeClass('title__mainTitle--splashscreen');
        $('.title__subtitle').removeClass('title__subtitle--splashscreen');
        $('.navBox').removeClass('warningBox--splashscreen');

        // Display location setup
        //$('#locationSetup').removeClass('d-none');
        $('#locationSetup').fadeIn();
    }, 2000);

    ////////////////////////
    // Start Leaflet Map //
    //////////////////////
    map = L.map('map').setView([51.505, -0.09], 13);
    // var basemap = new L.StamenTileLayer("terrain");
    var basemap = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
	maxZoom: 20,
	attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
});
    map.addLayer(basemap);
    map.addControl(new LegendControl());

    // Add legend tooltips
    $(function(){
        $('[data-toggle="tooltip"]').tooltip();
    });
    
    // Legend Collapse Button
    $('.collapseAction').on('click', function () {
        let legendState = $('#btnCollapse').attr('data-status');
        if (legendState == "open") {
            // Collapse the legend
            $('#btnCollapse').attr('data-status', 'closed');
            $('#btnCollapse').attr('src', legendOpenPNG);
            $('#legend-body').addClass('legend-hide');
        } else {
            $('#btnCollapse').attr('data-status', 'open');
            $('#btnCollapse').attr('src', legendClosePNG);
            $('#legend-body').removeClass('legend-hide');
        }
    });

    /////////////////////////
    // Set event listeners /
    ///////////////////////

    // Location form submit
    $('#formLocation').on('submit', submitLocation);

    // Use my current location
    $('#btnMyLocation').on('click', myLocation);

    // Filter button
    $('#btnFilter').on('click', function () {
        $('#filterModal').modal('show');
    });

    // New Location button
    $('#btnNew').on('click', newLocation);

    // About button
    $('#btnAbout').on('click', function () {
        $('#aboutModal').modal('show');
        // alert('test');
    });

    // Reset map on map modal close
    $('#mapModal').on('hidden.bs.modal', function () {
        // Remove all layers from map
        map.eachLayer(function(l) {
            if (l instanceof L.FeatureGroup || l instanceof L.Marker) {
                map.removeLayer(l);
                console.log('removed');
            }
        });

        // Reset loading icon
        $('#MapLoading').show();
    });
}


function get_stations(lat, lng, locality="") {
    // Calls the API to search for radio stations near input coordinates
    console.log('Getting radio station data for lat=' + lat + ' lng=' + lng);
    console.log('in ' + locality);
    // Hide formLocation if visible
    $('#locationSetup').hide();
    $('#lblWarning').hide();

    // Show loading icon
    $('#Loading').fadeIn();

    // Load station data
    $.ajax({
        url: lat + '/' + lng,
        dataType: 'json',
        success: function (r) {
            console.log(r);
            let stationsHTML = r.stationsHTML;
            let filterHTML = r.filterHTML;
            // Set HTML from api return
            $('#StationList').html(stationsHTML);
            $('#FilterList').html(filterHTML)

            // Adjust display of UI
            $('#Loading').fadeOut();
            $('#StationList').fadeIn();
            $('.navbar').css("display", "flex").hide().fadeIn();
            $('.currentLocation--white').html(locality);
            $('#CurrentLocation').fadeIn()
            
            // Add new event listeners:
            // Radio station info button
            $('.stationCard__main').on('click', stationClick);

            // Filter List Item
            $('.filterList__item').on('click', filterItemClick);

            // Update Map Modal
            $('.stationCard__btnMap').on('click', openMapModal);
        },
        error: function (e) {
            console.log('ugh, error');
            console.log(e);
        }
    })
}

// Open Map Modal, call API for data, and display in leaflet map
function openMapModal(e) {
    let id = $(this).data('id');
    $('#mapModal').modal('show');

    // Fix issue with map size within modal
    setTimeout(function() {
        
        $.ajax({
            url: id,
            success: function(r) {
                let data = r.data;
    
                // Update map title
                $('#mapModalTitle').html('<h4>Map of ' + data.callsign + '</h4><p>' + data.city + ', ' + data.state + '</p>');

                // Add layers to map
                let transmitterIcon = L.icon({
                    iconUrl: radioMarkerPNG,
                    iconSize: [45,45],
                    iconAnchor: [22,22]
                });

                let transmitter = L.geoJSON(data.transmitter, {
                    pointToLayer: function(f, latlng) {
                        return (L.marker(latlng, {icon: transmitterIcon, interactive: false}))
                    },
                    interactive: false
                }).addTo(map);

                let serviceContour = L.geoJSON(data.service_contour, {
                    style: function(f) {
                        return {
                            color: '#35dc35',
                            storke: '#35dc35'
                        }
                    },
                    interactive: false
                }).addTo(map);

                let estimatedRange = L.geoJSON(data.estimated_range, {
                    style: function(f) {
                        return {
                            color: '#fbfd6b',
                            stroke: '#fbfd6b'
                        }
                    },
                    interactive: false
                }).addTo(map);

                let userLocation = L.marker([userLat, userLng], {interactive: false}).addTo(map);
    
                // Zoom map to estimatedRange layer
                $('#map').show();
                map.invalidateSize();
                map.fitBounds(estimatedRange.getBounds());

                // Hide loading icon
                $('#MapLoading').fadeOut();
                
                
            }
        })
    }, 500);

    
}

// Location search form
function submitLocation(e) {
    e.preventDefault();

    data = $('#formLocation').serializeArray();
    loc = data[0].value;

    // Get coordinates of loc from API
    // let url = 'http://api.positionstack.com/v1/forward?access_key=4fc4bfdc142eea8b533f199ed953d029&query='+loc+'&limit=1';
    // Switching to geocodio api
    let url = 'https://api.geocod.io/v1.6/geocode?api_key=228038a8bc60b30b600627abb0bbeda070370bb&q='+loc+'&limit=1';
    $.ajax({
        url: url,
        dataType: 'JSON',
        success: function(r) {
            console.log(r)
            let data = r;
            let lat = data.results[0].location.lat
            let lng = data.results[0].location.lng;
            let locality = data.input.formatted_address;
            get_stations(lat, lng, locality);

            // Set global vars for tracking in map
            userLat = lat;
            userLng = lng;
        },
        error: function(e) {
            alert('something went wrong');
        }
    });
}

// Use geolocation
function myLocation() {
    // Get user's location
    let lat, lng;
    if(!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
      } else {
        navigator.geolocation.getCurrentPosition(function (p) {
            let lat = p.coords.latitude;
            let lng = p.coords.longitude;
            // let url = "http://api.positionstack.com/v1/reverse?access_key=4fc4bfdc142eea8b533f199ed953d029&query=" + lat + "," + lng+"&limit=1";
            // Switching to geocodio
            let url = 'https://api.geocod.io/v1.6/reverse?q='+lat+','+lng+'&api_key=228038a8bc60b30b600627abb0bbeda070370bb&limit=1';
            $.get({
                url: url,
                dataType: "JSON",
                success: function(r) {
                    console.log(r);
                    let data = r;
                    let locality = data.results[0].address_components.city + ', ' + data.results[0].address_components.state;
                    get_stations(lat, lng, locality);

                    // Set global vars for tracking in map
                    userLat = lat;
                    userLng = lng;
                },
                error: function() {
                    console.log('error');
                }
            });
            // get_stations(lat, lng);
            // $('.title__mainTitle').html("Stations near " + lat.toFixed(2) + "," + lng.toFixed(2));
        }, function() {
            alert("Unable to find your current location.  Try searching by text.");
        });
      }
}


// Info button in station card
function stationClick(e) {
    // Station id
    let id = $(this).data('id');

    // Open station details
    $('.stationCard__info', this).toggleClass('stationCard__info--active')
    $('[data-ID-Details = "' + id + '"]').toggleClass('d-none');
    $('.detailsList-'+id).animate({opacity:1}, 250);
    // Load station logo if available
    let url = 'https://publicfiles.fcc.gov/api/manager/download/entity/logo/' + id + '/fm';
    if ($('.logo-'+id).attr('src') == '') {
        $.ajax({
            url: url,
            success: function(r, s) {
                if (r.status != 'error') {
                    $('.logo-'+id).attr('src', url);
                    $('.logo-'+id + '.stationCard__logo').animate({opacity: 1}, 750);
                    $('.logo-'+id + '.stationCard__logo--blurred').animate({opacity: 0.3}, 750);
                    $('.detailsList-'+id).animate({opacity:1}, 250);
                }
            },
            error: function() {
                console.log(':(');
            }
        })
    } else {
        console.log('No logo to load');
    }
}

// Filter Item List Click
function filterItemClick(e) {
    let filterFormat = $(this).data('format');

    // Hide and show appropriate stations
    if (filterFormat == 'show_all') {
        $('.stationCard').fadeOut();
        setTimeout(function() {$('.stationCard').fadeIn();}, 600);  
    }
    $('.stationCard').fadeOut();
    setTimeout(function() {$('.' + filterFormat).fadeIn();}, 600);     

    // Close filter modal
    $('#filterModal').modal('hide');
    console.log('.' + filterFormat);
}


// New location search
function newLocation() {
    console.log('newLocation');
    // Hide station list and clear resutls for next search
    $('#StationList').fadeOut();
    $('#StationList').children().remove();
    $('#CurrentLocation').fadeOut();

    
    // Hide nav bars
    $('navbar').fadeOut();
    
    // Show search bars
    $('#locationSetup').fadeIn();
}


// Run initizlization function when the dom is ready
$(document).ready(init());
