$(document).ready(function () {
    let searchForm = $('.search-form');
    let searchInput = searchForm.find("[name='q']"); // input name='q'
    let searchBtn = searchForm.find("[type='submit']");
    let typingTimer;
    let typingInterval = 500; // .5 seconds

    searchInput.keyup(function (e) {
        // key released
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval);
    });

    searchInput.keydown(function (e) {
        // key pressed
        clearTimeout(typingTimer);
    });

    function displaySearch() {
        searchBtn.attr('disabled', 'true');
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching...");
    }

    function performSearch() {
        displaySearch();
        let query = searchInput.val();
        setTimeout(function () {
            window.location.href = '/search/?q=' + query;
        }, 1000);
    }

});
