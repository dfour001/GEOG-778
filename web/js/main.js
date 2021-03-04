function init() {
    // Clear splashscreen after 3000 miliseconds
    setTimeout(function() {
        $('.title').removeClass('title--splashscreen');
        $('.title__mainTitle').removeClass('title__mainTitle--splashscreen');
        $('.title__subtitle').removeClass('title__subtitle--splashscreen');
        $('.warningBox').removeClass('warningBox--splashscreen');
    }, 3000);
}



// Run initizlization function when the dom is ready
$(document).ready(init());