require('./_header');

$(function() {
  $('.nav-arrow').click(function() {
    $('html, body').animate({
      scrollTop: $('#features').offset().top
    }, 1000)
  });
});