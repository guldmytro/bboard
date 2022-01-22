function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    });
});

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

// messages
$('.messages button').on('click', function(e) {
    e.preventDefault();
    $(this).parent().slideUp(100);
});

// upload test photo
$('#test-photo').on('change', function() {
    const form = $(this).closest('form');
    const url = form.attr('action');
    const token = form.find('[name="csrfmiddlewaretoken"]').val();
    $.each(this.files, function(key, value) {
        const image = new FormData();
        image.append(key, value);
        image.append('csrfmiddlewaretoken', token);
        const reader = new FileReader();
        reader.onload = function() {
            const preloadedImage = $('.preloaded-image');
            preloadedImage.attr('src', reader.result);
        };
        reader.readAsDataURL(value);
        uploadImage(url, image);
    });
});

function uploadImage(url, image, element) {
    $.ajax({
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    const percentComplete = ((evt.loaded / evt.total) * 100);
                    $(".progress span").width(percentComplete + '%');
                    if (percentComplete === 100) {
                        $(".progress").hide();
                    }
                }
            }, false);
            return xhr;
        },
        url: url,
        method: 'POST',
        data: image,
        cache: false,
        processData: false,
        contentType: false,
        beforeSend: function() {
            $(".progress").show();
        },
        success: function(res) {
            if (res.status === 'ok') {
                $('.delete-photo').addClass('active');
            }
        }
    });
}

// delete test photo
$('.delete-photo').on('click', function(e) {
    e.preventDefault();
    const btn = $(this);
    const url = btn.attr('data-url');
    $.ajax({
        url: url,
        method: 'POST',
        data: {

        },
        beforeSend: function() {
            btn.prop('disabled', true);
        },
        success: function(res) {
            btn.prop('disabled', false);
            $('.preloaded-image').removeAttr('src');
            btn.removeClass('active');
        }
    });
    
});