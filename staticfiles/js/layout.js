$('document').ready(function() {

    // open sidebar and show overlay when toggle is clicked
    $('#menu-toggle').click(function(e) {
        e.preventDefault();
        $('#sidebar').addClass('sidebar-toggled');
        $('.overlay').show();
    });

    // close sidebar and hide overlay when overlay is clicked
    $('.overlay').click(function(e) {
        e.preventDefault();
        $('#sidebar').removeClass('sidebar-toggled');
        $('.overlay').hide();
    });

    // on load determine if window is medium or wider and set sidebar to toggled
    // in all cases remove sidebar-initial class
    // use windowExpanded to keep track of the current state of the window
    var windowExpanded;
    if($(window).width() > 768) {
        $('#sidebar').addClass('sidebar-toggled');
        windowExpanded = true;
    }
    else {
        windowExpanded = false;
    }

    $('#sidebar').removeClass('sidebar-initial');

    // when resizing, show sidebar if window is resized to medium or wider
    // if window goes from medium or wider to smaller, close the sidebar
    // else leave everthing as is
    $(window).resize(function(e) {
        if( $(window).width() > 768) {
            $('#sidebar').addClass('sidebar-toggled');
            $('.overlay').hide();
            windowExpanded = true;
        }
        else if( windowExpanded ) {
            console.log('here');
            $('#sidebar').removeClass('sidebar-toggled');
            windowExpanded = false;
        }
    });
});
