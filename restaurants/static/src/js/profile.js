var header = require('./_header');
var util = require('./_util');

const apiUrl = util.getApiUrl();

const errorTexts = {
  currentPassword: 'Current password is incorrect.',
  default: 'Something went wrong. Please try again.'
};

function initPage(user) {
  $('h1.welcome').append(', ' + user.username + '!');
  $('input[name="email"]').val(user.email);
}

function renderRestaurants(restaurants) {
  $('#restaurants ul').empty();
  restaurants.results.forEach(renderRestaurant);
}

function renderRestaurant(restaurant) {
  var restaurantElem = $('<li>').append(
                         $('<a>', {
                           href: util.getRestaurantUrl(restaurant.subdomain),
                           text: restaurant.name
                         }));
  $('#restaurants ul').append(restaurantElem);
}

function restaurantsRequest() {
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/restaurants/owned/',
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function getRestaurants() {
  var request = restaurantsRequest();
  request.done(renderRestaurants)
}

function nope() {
  $('.wrapper > section').css({
    'background': 'url(http://i.giphy.com/uVM1AZwC3AxYA.gif) no-repeat center',
    'background-size': 'cover'
  });
  setTimeout(unNope, 5000)
}

function unNope() {
  $('.wrapper > section').css({
    'background': '#fff'
  });
}

function toggleFormFields(form) {
  form.find('input').each(function() {
    $(this).prop('disabled', function(i, disabled) { return !disabled; });
  });
  form.find('.cancel, .save, .extra').toggleClass('hidden');
  form.find('input').first().focus();
}

function toggleForm() {
  toggleFormFields($(this).parent());
}

function changePasswordRequest(data) {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/password/',
    data: data,
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function changeEmail(e) {
  e.preventDefault();
  nope()
}


function changePassword(e) {
  e.preventDefault();
  var request = changePasswordRequest({
    current_password: $('input[name="current-password"]').val(),
    new_password: $('input[name="new-password"]').val()
  });
  request.done(handlePasswordSuccess);
  request.fail(handlePasswordErrors);
}

function handleSuccess() {
  $('#error').hide();
  $('input.invalid').removeClass('invalid');
}

function handlePasswordSuccess() {
  handleSuccess();
  var form = $('#change-password');
  form.find('input').each(function() {
    $(this).val('');
  });
  toggleFormFields(form);
}

function handlePasswordErrors(errors) {
  if (errors.status == 400 && errors.responseJSON.current_password) {
    $('#error').find('p').text(errorTexts.currentPassword).parent().show();
    $('input[name="current-password"]').addClass('invalid');
  } else {
    $('#error').find('p').text(errorTexts.default).parent().show();
  }
}

$(function() {
  header.userInfo.done(function(user) {
    initPage(user);
    getRestaurants(localStorage.getItem('authToken'));
  });

  $('button.change, button.cancel').click(toggleForm);
  $('#change-email').submit(changeEmail);
  $('#change-password').submit(changePassword);
});