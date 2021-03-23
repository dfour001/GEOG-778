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

    /////////////////////////
    // Set event listeners /
    ///////////////////////

    // Location form submit
    $('#formLocation').on('submit', submitLocation);

    // Use my current location
    $('#btnMyLocation').on('click', myLocation);

    // Filter button
    $('#btnFilter').on('click', function () {
        alert("This will show a list of all available formats (eg, Rock, Country, Public Radio, etc) along with the number of stations that match that format.  Clicking on a format will only show stations that match the selected format.  Only formats that are available in the selected location will be on the filter list.")
    });

    // New Location button
    $('#btnNew').on('click', newLocation);

    // About button
    $('#btnAbout').on('click', function () {
        alert("This will show a page that says a little bit about the project, where the data comes from, etc.")
    });
}


function get_stations(lat, lng) {
    // Calls the API to search for radio stations near input coordinates
    console.log('Getting radio station data for lat=' + lat + ' lng=' + lng);

    // Hide formLocation if visible
    $('#locationSetup').hide();
    $('#lblWarning').hide();

    // Show loading icon
    $('#Loading').fadeIn();

    // Load station data
    $.ajax({
        url: 'http://localhost:5000/' + lat + '/' + lng,
        dataType: 'html',
        success: function (r) {
            $('#StationList').html(r);
            $('#Loading').fadeOut();
            $('#StationList').fadeIn();
            $('.navbar').css("display", "flex").hide().fadeIn();
            
            // Add new event listeners:
            // Radio station info button
            $('.stationCard__main').on('click', stationClick);
        },
        error: function (e) {
            console.log('ugh, error');
            console.log(e);
        }
    })
}

// Location form
function submitLocation(e) {
    e.preventDefault();

    data = $('#formLocation').serializeArray();
    loc = data[0].value;

    // Get coordinates of loc from API
    let url = 'http://api.positionstack.com/v1/forward?access_key=4fc4bfdc142eea8b533f199ed953d029&query='+loc+'&limit=1';
    $.ajax({
        url: url,
        dataType: 'JSON',
        success: function(r) {
            alert('something went right');
            let data = r.data[0];
            let lat = data.latitude;
            let lng = data.longitude;
            let label = data.label;
            console.log(r);
            console.log(data);
            get_stations(lat, lng);
        },
        error: function(e) {
            alert('something went wrong');
        }
    });
}

// Use my location
function myLocation() {
    // Get user's location
    let lat, lng;
    if(!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
      } else {
        navigator.geolocation.getCurrentPosition(function (p) {
            let lat = p.coords.latitude;
            let lng = p.coords.longitude;
            get_stations(lat, lng);
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

    // Load station logo if available
    let url = 'https://publicfiles.fcc.gov/api/manager/download/entity/logo/' + id + '/fm';
    if ($('.logo-'+id).attr('src') == '') {
        $.ajax({
            url: url,
            success: function(r, s) {
                if (r.status == 'error') {
                    $('.detailsList-'+id).animate({opacity:1}, 250);
                } else {
                    $('.logo-'+id).attr('src', url);
                    $('.logo-'+id + '.stationCard__logo').animate({opacity: 1}, 250);
                    $('.logo-'+id + '.stationCard__logo--blurred').animate({opacity: 0.3}, 250);
                    $('.detailsList-'+id).animate({opacity:1}, 250);
                }
            },
            error: function() {
                console.log(':(');
            }
        })
    } else {
        console.log('lol no');
    }
}


// New location search
function newLocation() {
    console.log('newLocation');
    // Hide station list and clear resutls for next search
    $('#StationList').fadeOut();
    $('#StationList').children().remove();

    
    // Hide nav bars
    $('navbar').fadeOut();
    
    // Show search bars
    $('#locationSetup').fadeIn();
}


// Run initizlization function when the dom is ready
$(document).ready(init());
