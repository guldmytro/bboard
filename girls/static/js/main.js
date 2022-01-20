$('.lux-slider').slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000,
    responsive: [
        {
            breakpoint: 1200,
            settings: {
                slidesToShow: 3
            }
        },
        {
            breakpoint: 992,
            settings: {
                slidesToShow: 2
            }
        },
        {
            breakpoint: 576,
            settings: {
                slidesToShow: 1
            }
        }
    ]
});

$('.single-gallery').slick({
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    asNavFor: $('.single-subgallery')
});

$('.single-subgallery').on('init', function() {
    $('.single-subgallery .slick-slide').on('click', function() {
        const index = parseInt($(this).attr('data-slick-index'));
        $('.single-gallery').slick('slickGoTo', index, false);
    });
});

$('.single-subgallery').slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: false,
    asNavFor: $('.single-gallery')
});

// mobile menu
const headerMenuBtn = $('.header-menu-btn');
const mobileMenu = $('.mobile-menu');
headerMenuBtn.on('click', function(e) {
    e.preventDefault();
    headerMenuBtn.toggleClass('active');
    mobileMenu.slideToggle(300);
});

$('.mobile-nav__item_has_children span').on('click', function(e) {
    e.preventDefault();
    const $this = $(this);
    const subMenu = $this.next('.mobile-sub-menu');
    subMenu.slideToggle(250)
});

$(window).on('resize', function(e) {
    if ($(window).width() > 991) {
        headerMenuBtn.removeClass('active');
        mobileMenu.hide();
    }
});
