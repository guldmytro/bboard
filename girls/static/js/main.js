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
    infinite: false,
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
    infinite: false,
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
    $.each(this.files, function(key, value) {
        const image = new FormData();
        console.log(key, value);
        image.append(key, value);
        const reader = new FileReader();
        reader.onload = function() {
            const preloadedImage = $('.file-wrapper_test .preloaded-image');
            preloadedImage.attr('src', reader.result);
        };
        reader.readAsDataURL(value);
        uploadImage(url, image);
    });
});

function uploadImage(url, image) {
    $.ajax({
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    const percentComplete = ((evt.loaded / evt.total) * 100);
                    $(".file-wrapper_test .progress span").width(percentComplete + '%');
                    if (percentComplete === 100) {
                        $(".file-wrapper_test .progress").hide();
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
            $(".file-wrapper_test .progress").show();
        },
        success: function(res) {
            if (res.status === 'ok') {
                $('.file-wrapper_test .delete-photo').addClass('active');
            }
        }
    });
}

// delete test photo
$('.file-wrapper_test .delete-photo').on('click', function(e) {
    e.preventDefault();
    const btn = $(this);
    const url = btn.attr('data-url');
    $.ajax({
        url: url,
        method: 'POST',
        beforeSend: function() {
            btn.prop('disabled', true);
        },
        success: function(res) {
            btn.prop('disabled', false);
            $('.file-wrapper_test .preloaded-image').removeAttr('src');
            btn.removeClass('active');
        }
    }); 
});


// upload multiple images
$('#profile-images').on('change', function() {
    const form = $(this).closest('form');
    const url = form.attr('action');
    uploadGallery(url, this.files, 0);
});

function uploadGallery(url, files, current) {
    const image = new FormData();
    image.append(0, files[current]);
    const apendedImage = appendImage(files[current]);
    const progress = apendedImage.find('.progress');
    $.ajax({
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    const percentComplete = ((evt.loaded / evt.total) * 100);
                    progress.find('span').width(percentComplete + '%');
                    if (percentComplete === 100) {
                        progress.hide();
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
            progress.show();
        },
        success: function(res) {
            apendedImage.find('.delete-photo').addClass('active');
            if (res?.status === 'forbidden') {
                apendedImage.find('.forbidden__label').show().find('span').text(res?.text);
            } else if (res?.status == 'ok' && res?.id) {
                apendedImage.find('.delete-photo').attr('data-id', res.id);
            }

            if (current < files.length - 1) {
                uploadGallery(url, files, ++current);
            }
        }
    });    
}

function appendImage(image) {
    const imageTemplate = `
        <div class="uploaded-image">
            <div class="uploaded-image__inner">
                <img>
                <div class="progress"><span></span></div>
                <button type="button" class="delete-photo">x</button>
                <span class="forbidden__label"><span><span></span> 
            </div>
        </div>
    `;
    let imageTag = $(imageTemplate);
    $('.forms-section__row_gallery').append(imageTag);
    const reader = new FileReader();
    reader.onload = function() {
        imageTag.find('img').attr('src', reader.result);
    };
    reader.readAsDataURL(image);
    return imageTag;
}

// delete image
$('.forms-section__row_gallery').on('click', '.delete-photo', function(e) {
    e.preventDefault();
    const $this = $(this);
    const imageId = $this.attr('data-id');
    const url = $('.profile-images-form').attr('data-delete');
    $.ajax({
        url: url,
        method: 'POST',
        beforeSend: function() {
            $this.prop('disabled', true);
        },
        data: {
            id: imageId
        },
        success: function(res) {
            $this.closest('.uploaded-image').remove();
        }
    }); 
});

// upload multiple videos
$('#profile-videos').on('change', function() {
    const form = $(this).closest('form');
    const url = form.attr('action');
    uploadVideo(url, this.files, 0);
});

function uploadVideo(url, files, current) {
    const image = new FormData();
    image.append(0, files[current]);
    const apendedVideo = appendVideo(files[current]);
    const progress = apendedVideo.find('.progress');
    $.ajax({
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    const percentComplete = ((evt.loaded / evt.total) * 100);
                    progress.find('span').width(percentComplete + '%');
                    if (percentComplete === 100) {
                        progress.hide();
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
            progress.show();
        },
        success: function(res) {
            if (res?.status === 'forbidden') {
                apendedVideo.find('.forbidden__label').show().find('span').text(res?.text);
            } else if (res?.status == 'ok' && res?.id) {
                apendedVideo.find('.delete-photo').addClass('active').attr('data-id', res.id);
                apendedVideo.find('video').attr('src', res?.url).attr('controls', true);
            }

            if (current < files.length - 1) {
                uploadVideo(url, files, ++current);
            }
        }
    });    
}

function appendVideo() {
    const imageTemplate = `
        <div class="uploaded-image">
            <div class="uploaded-image__inner">
                <video></video>
                <div class="progress"><span></span></div>
                <button type="button" class="delete-photo">x</button>
                <span class="forbidden__label"><span><span></span> 
            </div>
        </div>
    `;
    let imageTag = $(imageTemplate);
    $('.forms-section__row_videos').append(imageTag);
    return imageTag;
}

// delete video
$('.forms-section__row_videos').on('click', '.delete-photo', function(e) {
    e.preventDefault();
    const $this = $(this);
    const videoId = $this.attr('data-id');
    const url = $('.profile-videos-form').attr('data-delete');
    $.ajax({
        url: url,
        method: 'POST',
        beforeSend: function() {
            $this.prop('disabled', true);
        },
        data: {
            id: videoId
        },
        success: function(res) {
            $this.closest('.uploaded-image').remove();
        }
    }); 
});

// popup
const popup = $('.popup');
$('.single-add-review button').on('click', function(e) {
    e.preventDefault();
    popup.fadeIn(200);
    $('body').css('overflow', 'hidden');
});

$('.review-form__close').on('click', function(e) {
    e.preventDefault();
    popup.fadeOut(200);
    $('body').css('overflow', 'auto');
});

// send girlreview
$('.review-form').on('submit', function(e) {
    e.preventDefault();
    const btn = $(this).find('[type="submit"]');
    const url = $(this).attr('action');
    const reviewData = $(this).serialize();
    $.ajax({
        url: url,
        method: 'POST',
        data: reviewData,
        beforeSend: function() {
            btn.prop('disabled', true).text('Отправка...');
        },
        success: function(res) {
            if (res?.status === 'ok') {
                btn.text('Отправлено!');
            } else {
                btn.text('Ошибка...');
            }
        }
    });
});

// delete reviews
$('.review-item__delete').on('click', function(e) {
    e.preventDefault();
    const btn = $(this);
    const url = btn.attr('data-action');
    $.ajax({
        url: url,
        method: 'POST',
        beforeSend: function() {
            btn.prop('disabled', true);
        },
        success: function(res) {
            if (res?.status === 'ok') {
                btn.closest('.review-item').remove();
            }
        }
    });
});

// update video counter
$('.single-gallery__item video').each(function(e) {
    let triggerTime = 5;
    let fired = 0;
    const video = $(this);
    video.on('timeupdate', function() {
       const timer = video.get(0).currentTime.toFixed(2) ;
       if (timer > triggerTime) {
            if (!fired) {
                updateVideoCounter(video);
                fired = true;
            }
       }
    });
    video.on('ended', function() {
        fired = false;
    });
});

function updateVideoCounter(video) {
    const url = video.attr('data-action');
    $.ajax({
        url: url,
        method: 'POST'
    });
}

// check phone
$('.number-form').on('submit', function(e) {
    e.preventDefault();
    const form = $(this);
    const tel = form.serialize();
    const url = form.attr('action');
    const btn = form.find('[type="submit"]');
    $.ajax({
        url: url,
        method: 'POST',
        data: tel,
        beforeSend: function() {
            btn.prop('disabled', true);
        },
        success: function(res) {
            btn.prop('disabled', false);
            $('.number-check-wrapper').html(res);
        }
    });
});

// cities
const popupCities = $('.popup-cities');
$('.header-city').on('click', function(e) {
    e.preventDefault();
    popupCities.fadeIn(200);
    $('body').css('overflow', 'hidden');
});

$('.cities-form__close').on('click', function(e) {
    e.preventDefault();
    popupCities.fadeOut(200);
    $('body').css('overflow', 'auto');
});

$('.cities-item__link:not(.active)').on('click', function(e) {
    e.preventDefault();
    const btn = $(this);
    const slug = btn.attr('data-slug');
    const url = btn.attr('data-action');
    $.ajax({
        url: url,
        method: 'POST',
        data: {
            slug: slug
        },
        beforeSend: function() {
            btn.prop('disabled', true);
        },
        success: function(res) {
            $('.cities-item__link.active').removeClass('active');
            btn.addClass('active');
            const urlPieces = [location.protocol, '//', location.host, location.pathname]
            let url = urlPieces.join('')
            window.location.href = url
        }
    });
});