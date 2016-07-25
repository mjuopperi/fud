var header = require('./_header');
var util = require('./_util');
var uiUtil = require('./_uiUtil');
var restaurantTemplate = require('./templates/restaurant.html');
var restaurantAdminTemplate = require('./templates/restaurantAdmin.html');
var mapTemplate = require('./templates/map.html');

const apiUrl = util.getApiUrl();
const subdomain = util.getSubdomain();

const errorTexts = {
  default: 'Something went wrong. Please try again.'
};

var restaurant;
var editing = false;

function toggleFormFields(form) {
  form.find('input').each(function() {
    $(this).prop('disabled', function(i, disabled) { return !disabled; });
  });
  form.find('.change').toggle();
  form.find('.cancel, .save, .extra').toggleClass('hidden');
  var firstInput = form.find('input').first();
  firstInput.focus().val(firstInput.val());
}

function toggleForm(e) {
  toggleFormFields($(e.target).closest('.input-container'));
}

function adjustInputWidth(e) {
  var target = $(e.target).is('input') ? $(e.target) : $(this);
  var hiddenSpan = $('<span>', {
    class: 'hidden-span',
    style: 'font-size: ' + target.css('font-size') + ';' +
           'font-family: ' + target.css('font-family')
  });
  hiddenSpan.text(target.val()).appendTo('body');
  target.width(hiddenSpan.width() + parseInt(target.css('font-size')));
  hiddenSpan.remove();
}

function updateRestaurantRequest() {
  return $.ajax({
    type: 'PUT',
    url: apiUrl + '/restaurants/' + subdomain,
    data: restaurant,
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function shouldUpdateMap(fieldName) {
  return fieldName === 'address' || fieldName === 'city';
}

function updateRestaurant(e) {
  e.preventDefault();
  var form = $(e.target).parent().parent();
  var updateMap = false;
  uiUtil.showProgressIndicator($(e.target));
    form.find('input').each(function() {
      updateMap = shouldUpdateMap($(this).attr('name')); 
      restaurant[$(this).attr('name')] = $(this).val();
  });
    updateRestaurantRequest()
    .done(function() { handleSuccess(form, updateMap) })
    .fail(function() { handleErrors(form) })
    .always(function() { uiUtil.hideProgressIndicator($(e.target)) });
}
function handleSuccess(form, updateMap) {
  toggleFormFields(form);
  uiUtil.showSuccesIndicator(form);
  if (updateMap) renderMap();
}
function handleErrors(form) {
  }

function getRestaurantInfo() {
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/restaurants/' + subdomain
  });
}

function init() {
  getRestaurantInfo().then(function(data) {
    restaurant = data;
    renderRestaurant(restaurantTemplate);
  });
}

function renderRestaurant(templateFile) {
  var template = _.template(templateFile);
  $('.content').html(template({
    restaurant: restaurant,
    googleMapsApiKey: googleMapsApiKey
  })).find('input').each(adjustInputWidth);
}

function renderMap() {
  var template = _.template(mapTemplate);
  $('.content').find('.map').html(template({
    restaurant: restaurant,
    googleMapsApiKey: googleMapsApiKey
  })).find('input').each(adjustInputWidth);
}

function toggleMode() {
  if (editing) {
    renderRestaurant(restaurantTemplate);
    $(this).text('Edit page');
  }
  else {
    renderRestaurant(restaurantAdminTemplate);
    $(this).text('View page');
  }
  editing = !editing;
}

$(function() {
  $('.content')
    .on('click', 'button.change, button.cancel', toggleForm)
    .on('click', 'button.save', updateRestaurant)
    .on('keyup keydown blur update', 'input', adjustInputWidth);
  $('.switch-mode').click(toggleMode);
  init();
});