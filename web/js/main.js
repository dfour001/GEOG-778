function init() {
    // Clear splashscreen after 3000 miliseconds
    setTimeout(function() {
        $('.title').removeClass('title--splashscreen');
        $('.title__mainTitle').removeClass('title__mainTitle--splashscreen');
        $('.title__subtitle').removeClass('title__subtitle--splashscreen');
        $('.warningBox').removeClass('warningBox--splashscreen');
        
        // Display location setup
        //$('#locationSetup').removeClass('d-none');
        $('#locationSetup').fadeIn();
    }, 3000);
    
    /////////////////////////
    // Set event listeners /
    ///////////////////////
    
    // Location form submit
    $('#formLocation').on('submit', submitLocation);
    
    // Use my current location
    $('#btnMyLocation').on('click', myLocation);
}


function get_stations(lat, lng) {
    // Calls the API to search for radio stations near input coordinates
    console.log('Getting radio station data for lat=' + lat + ' lng=' + lng);
    
    // Hide formLocation if visible
    $('#locationSetup').hide();
    
    // Show loading icon
    $('#Loading').fadeIn();
    
    // Load station data
    $.ajax({
        url: 'test.json',
        dataType: 'json',
        success: function(r) {
            console.log(r);
            // Pause to simulate loading data during test
            setTimeout(function(){$('#Loading').fadeOut();}, 3000);
            //$('#Loading').fadeOut();
        },
        error: function(e) {
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
    
    
    // Get stations from the api
    get_stations(0, 0);
}

// Use my location
function myLocation() {
    // Get user's location
    
    
    // Get stations from the api
    get_stations(0, 0);
}




// Run initizlization function when the dom is ready
$(document).ready(init());