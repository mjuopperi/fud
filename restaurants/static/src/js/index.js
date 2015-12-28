require('./_header');

function setMobileMargins() {
  var header = $('header');
  var heading = $('#header').find('h1:first-of-type');
  var arrow = $('.nav-arrow');

  var halfHeight = ($(window).height() - heading.height() - header.height()) / 2;
  var headingMarginTop = halfHeight * 0.8;
  var headingMarginBottom = halfHeight - 1.5 * arrow.height();
  var arrowMarginBottom = $(window).height() - heading.height() - headingMarginTop - headingMarginBottom - arrow.height();

  heading.css('margin-top', headingMarginTop);
  heading.css('margin-bottom', headingMarginBottom);
  arrow.css('margin-bottom', arrowMarginBottom);
}


$(function() {
  $('.nav-arrow').click(function() {
    $('html, body').animate({
      scrollTop: $('#features').offset().top
    }, 1000)
  });
  if ($(window).width() < 600) setMobileMargins();
});