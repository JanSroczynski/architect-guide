$(function() {
    var pathname = window.location.pathname;
    var navbar_children = $('nav').children();
    if (pathname.includes("user")) {
        pathname = 'user'
    };
    navbar_children.removeClass('active')
    switch(pathname) {
        case '/':
            navbar_children.eq(0).addClass('active');
            break;
        case '/login':
            navbar_children.eq(2).addClass('active');
            break;
        case '/register':
            navbar_children.eq(3).addClass('active');
            break;
        case '/about':
            navbar_children.eq(1).addClass('active');
            break;
        case 'user':
            navbar_children.eq(2).addClass('active');
            break;
    };
});